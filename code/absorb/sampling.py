"""Posterior sampling: maximum-a-posteriori search, emcee, and nested sampling.

The likelihood is expensive only through one background solve (~11 ms), so the
sampler is parallelised over walkers with a process pool.  Convergence is
judged by the integrated autocorrelation time rather than a fixed chain length:
sampling stops once the chain is longer than ``N_TAU`` autocorrelation times
*and* the estimate has itself stabilised.
"""
from __future__ import annotations

import os
import time

# Reading a chain file while the sampler holds it takes an HDF5 lock and can
# abort the run.  Disabling file locking for this process makes concurrent
# inspection safe; the sampler is the only writer.
os.environ.setdefault("HDF5_USE_FILE_LOCKING", "FALSE")
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Sequence

import numpy as np

from .constants import SEED
from .params import MODELS, Model

ROOT = Path(__file__).resolve().parents[2]
CHAIN_DIR = ROOT / "results" / "chains"

N_TAU = 50           # require chain length > N_TAU * tau
#: A chain can look converged in its sampled parameters and still give an
#: unstable answer for a derived quantity.  For this model the raw parameters
#: are strongly degenerate near the LambdaCDM boundary, where the rate and the
#: convertible fraction both go to zero and the remaining parameters become
#: unconstrained; what the paper actually quotes is the *derived* converted
#: fraction, so the split-chain stability of its 95th percentile is checked
#: alongside the autocorrelation criterion.
SPLIT_TOL = 0.25     # allowed relative drift of the reported limit
TAU_TOL = 0.02       # and tau stable to 2% between checks
CHECK_EVERY = 500
#: Likelihood evaluations allowed to the local maximiser, per sampled
#: dimension.  A fixed total budget favours the smallest model, which is the
#: null in every comparison the paper makes.
MAP_BUDGET_PER_DIM = 300

#: Resident size of one worker in a long run.  Immediately after forking it is
#: about 260 MB, most of it copy-on-write shared with the parent; it settles
#: near 720 MB over tens of thousands of steps as allocator arenas fragment
#: under the churn of per-call background solves.  The larger figure is the one
#: to budget against, since exhausting memory late in a run wastes the whole
#: chain.
WORKER_RSS_MB = 720
#: Never consume more than this fraction of the memory the OS reports as
#: available; the machine is shared with other work.
MEMORY_BUDGET_FRACTION = 0.5


def available_memory_mb() -> float:
    """Memory the OS reports as available, in MiB."""
    try:
        with open("/proc/meminfo") as fh:
            for line in fh:
                if line.startswith("MemAvailable:"):
                    return float(line.split()[1]) / 1024.0
    except OSError:                                            # pragma: no cover
        pass
    return float("inf")


def safe_n_proc(requested: int | None = None) -> int:
    """Worker count that fits in the memory budget as well as the core count.

    Sampling is embarrassingly parallel, so it is tempting to use every core;
    but each forked worker touches a few hundred MB of private pages, and
    exhausting memory on a shared machine is a far worse outcome than a chain
    that takes twice as long.
    """
    by_cores = os.cpu_count() or 4
    by_memory = int(available_memory_mb() * MEMORY_BUDGET_FRACTION
                    / WORKER_RSS_MB)
    n = min(requested or by_cores, by_cores, max(1, by_memory))
    return max(1, n)


@dataclass
class ChainSummary:
    """Everything needed to reproduce and report a chain."""

    model: str
    dataset: str
    n_walkers: int
    n_steps: int
    burn_in: int
    thin: int
    tau_max: float
    acceptance: float
    converged: bool
    seed: int
    runtime_s: float
    chi2_min: float
    n_data: int
    n_params: int
    #: Acceptance and autocorrelation over the last tenth of the chain.  The
    #: cumulative figures are flattered by the early transient, and for a chain
    #: that is decelerating they hide exactly the pathology one is looking for.
    acceptance_late: float = float("nan")
    move_rate_early: float = float("nan")
    move_rate_late: float = float("nan")
    #: Number of likelihood evaluations the maximiser was allowed, per
    #: dimension.  Recorded because a model comparison between two models
    #: polished with different budgets is not a comparison of the models.
    map_budget_per_dim: int = 0
    parametrisation: str = "logit"

    @property
    def aic(self) -> float:
        return self.chi2_min + 2 * self.n_params

    @property
    def bic(self) -> float:
        return self.chi2_min + self.n_params * np.log(self.n_data)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["aic"] = self.aic
        d["bic"] = self.bic
        return d


# --------------------------------------------------------------------------- #
# Posterior
# --------------------------------------------------------------------------- #
class Posterior:
    """Callable log-posterior for one (model, likelihood) pair.

    Held at module scope by the runner so that a forked worker inherits it
    without pickling the data.
    """

    def __init__(self, model: str, likelihood, nuisance: Sequence[str] = ()) -> None:
        self.model_name = model
        self.model: Model = MODELS[model]
        self.likelihood = likelihood
        self.nuisance = tuple(nuisance)

    @property
    def param_names(self) -> tuple[str, ...]:
        return self.model.params + self.nuisance

    @property
    def ndim(self) -> int:
        return len(self.param_names)

    def _split(self, theta: Sequence[float]):
        n = self.model.ndim
        return np.asarray(theta[:n], float), dict(zip(self.nuisance, theta[n:]))

    def chi2(self, theta: Sequence[float]) -> float:
        core, nus = self._split(theta)
        bg = self.model.builder(self.model.to_dict(core))
        return float(self.likelihood.chi2(bg, nus))

    def log_prior(self, theta: Sequence[float]) -> float:
        from .params import PRIORS
        core, _ = self._split(theta)
        lp = self.model.log_prior(core)
        if not np.isfinite(lp):
            return -np.inf
        for name, value in zip(self.nuisance, theta[self.model.ndim:]):
            if not PRIORS[name].contains(value):
                return -np.inf
        return lp

    def __call__(self, theta: Sequence[float]) -> float:
        lp = self.log_prior(theta)
        if not np.isfinite(lp):
            return -np.inf
        try:
            c2 = self.chi2(theta)
        except Exception:                       # unphysical corner of the prior
            return -np.inf
        if not np.isfinite(c2):
            return -np.inf
        return lp - 0.5 * c2

    def prior_transform(self, u: np.ndarray) -> np.ndarray:
        from .params import PRIORS
        core = self.model.prior_transform(u[:self.model.ndim])
        rest = [PRIORS[n].unit_to_value(ui)
                for n, ui in zip(self.nuisance, u[self.model.ndim:])]
        return np.concatenate([core, rest]) if rest else core


# --------------------------------------------------------------------------- #
# MAP search
# --------------------------------------------------------------------------- #
def find_map(post: Posterior, n_screen: int = 400, seed: int = SEED,
             x0: np.ndarray | None = None, max_local: int = 900) -> np.ndarray:
    """Locate a good starting point for the sampler, cheaply.

    Two regimes.  With ``x0`` given -- normally the best sample of a finished
    chain -- a single local refinement is run from it and the result is a
    genuine maximum-a-posteriori estimate.  Without it, the routine screens a
    Latin hypercube and refines only the best point.

    The screening design matters for cost.  A full multi-start Powell search
    over the prior volume spends most of its budget in regions where the
    background integration is several times slower than at the best fit,
    because large rates and strong reinforcement stiffen the system; measured
    over random prior draws the cost per evaluation rises from about 20 ms to
    as much as 80 ms.  Running such a search to convergence took roughly twenty
    minutes per model and produced a starting point no better, for the purpose
    of placing a walker ball, than the one below.
    """
    from scipy.optimize import minimize
    from scipy.stats import qmc

    def neg(theta):
        v = post(theta)
        return 1e10 if not np.isfinite(v) else -v

    if x0 is not None:
        r = minimize(neg, np.asarray(x0, dtype=float), method="Nelder-Mead",
                     options=dict(maxfev=2 * max_local, xatol=1e-5, fatol=1e-6))
        return np.asarray(r.x, dtype=float)

    lows = np.array([p.low for p in _priors_of(post)])
    highs = np.array([p.high for p in _priors_of(post)])
    design = qmc.LatinHypercube(d=post.ndim, seed=seed).random(n_screen)
    candidates = lows + design * (highs - lows)
    values = np.array([neg(c) for c in candidates])
    best = candidates[int(np.argmin(values))]
    if not np.isfinite(values.min()) or values.min() >= 1e10:
        # nothing in the screen was admissible; fall back to the prior centre
        return 0.5 * (lows + highs)
    r = minimize(neg, best, method="Nelder-Mead",
                 options=dict(maxfev=max_local, xatol=1e-4, fatol=1e-5))
    return np.asarray(r.x if r.fun < values.min() else best, dtype=float)


def _priors_of(post: Posterior):
    from .params import PRIORS
    return post.model.priors() + [PRIORS[n] for n in post.nuisance]


# --------------------------------------------------------------------------- #
# Unbounded reparametrisation
# --------------------------------------------------------------------------- #
class LogitMap:
    """Bijection between a box of uniform priors and all of R^n.

    Every prior in this project is uniform on a finite interval, and the
    ensemble move used by ``emcee`` is a difference vector between two walkers
    with no knowledge of those edges.  Once the posterior is wide compared with
    its prior in any direction -- which is exactly what happens here, because
    the rate parameters are unconstrained under the null -- most proposals land
    outside the box and are rejected on the prior alone, at a rate that *grows*
    as the ensemble spreads.  Measured on the frozen ``xi_h`` chain, 57.1% of
    proposals at the default scale left the box, and the move rate fell from
    0.0150 to 0.0058 over the run.

    Sampling the logit-transformed coordinate removes the edges: no proposal
    can be invalid, so a rejection carries information about the posterior
    rather than about the parametrisation.

    This is a change of coordinates, not a change of prior.  With

        u = (x - low) / (high - low),   z = log(u / (1 - u)),

    the Jacobian is dx/dz = (high - low) u (1 - u), and adding its logarithm to
    the target reproduces the original measure on ``x`` exactly.  The test
    ``test_logit_map_preserves_the_prior`` samples the transformed target with
    a constant likelihood and checks that the induced distribution of ``x`` is
    uniform.
    """

    def __init__(self, lows: Sequence[float], highs: Sequence[float]) -> None:
        self.low = np.asarray(lows, dtype=float)
        self.high = np.asarray(highs, dtype=float)
        self.width = self.high - self.low
        if np.any(self.width <= 0):
            raise ValueError("every prior must have positive width")

    def to_z(self, x: np.ndarray) -> np.ndarray:
        u = np.clip((np.asarray(x, float) - self.low) / self.width, 1e-12, 1 - 1e-12)
        return np.log(u / (1.0 - u))

    def to_x(self, z: np.ndarray) -> np.ndarray:
        return self.low + self.width / (1.0 + np.exp(-np.asarray(z, float)))

    def log_jacobian(self, z: np.ndarray) -> float:
        """log|dx/dz| summed over coordinates, computed stably for large |z|."""
        za = np.asarray(z, float)
        # log u + log(1-u) = -|z| - 2 log(1 + e^-|z|), exact and overflow-free
        a = np.abs(za)
        return float(np.sum(np.log(self.width) - a - 2.0 * np.log1p(np.exp(-a))))


class UnboundedPosterior:
    """``Posterior`` seen through :class:`LogitMap`; the sampler's target."""

    def __init__(self, post: "Posterior") -> None:
        self.post = post
        priors = _priors_of(post)
        self.map = LogitMap([p.low for p in priors], [p.high for p in priors])
        self.model_name = post.model_name
        self.ndim = post.ndim

    def __call__(self, z: Sequence[float]) -> float:
        x = self.map.to_x(z)
        lp = self.post(x)
        if not np.isfinite(lp):
            return -np.inf
        return lp + self.map.log_jacobian(z)


# --------------------------------------------------------------------------- #
# Worker plumbing
# --------------------------------------------------------------------------- #
#: Set before the process pool is created.  On Linux the pool is forked, so the
#: workers inherit this object through the address space.  Passing the
#: Posterior itself as the sampler callable would instead pickle its ~20 MB
#: supernova covariance on every task, which costs two orders of magnitude
#: more than the likelihood evaluation itself.
_WORKER_POST = None


def _log_prob(theta):
    """Top-level, trivially picklable proxy for the worker posterior."""
    return _WORKER_POST(theta)


# --------------------------------------------------------------------------- #
# emcee driver
# --------------------------------------------------------------------------- #
def run_mcmc(post: Posterior, dataset: str, *, n_walkers: int | None = None,
             max_steps: int = 40000, seed: int = SEED, n_proc: int | None = None,
             resume: bool = True, quick: bool = False,
             progress: bool = False) -> tuple[np.ndarray, ChainSummary]:
    """Sample the posterior; return (flat chain, summary)."""
    import emcee
    import multiprocessing as mp

    # Python 3.14 defaults to the "forkserver" start method on Linux, which
    # re-imports the module and pickles the callable for every task.  With a
    # 20 MB supernova covariance attached to the posterior that costs two
    # orders of magnitude more than the likelihood itself, so we request "fork"
    # explicitly: the workers then inherit the posterior through the address
    # space and send only the parameter vector.
    ctx = mp.get_context("fork")

    os.environ.setdefault("OMP_NUM_THREADS", "1")
    if quick:
        max_steps = min(max_steps, 6000)
    ndim = post.ndim
    n_walkers = n_walkers or max(32, 4 * ndim + (-(4 * ndim) % 16))
    n_proc = safe_n_proc(n_proc)
    print(f"  sampling with {n_proc} workers "
          f"({available_memory_mb():.0f} MB available)")

    CHAIN_DIR.mkdir(parents=True, exist_ok=True)
    path = CHAIN_DIR / f"{post.model_name}_{dataset}.h5"
    backend = emcee.backends.HDFBackend(str(path))

    # The sampler works in the unbounded coordinate; everything reported is
    # transformed back.  See LogitMap for why.
    target = UnboundedPosterior(post)
    lmap = target.map
    _write_chain_meta(path, post, lmap)

    if not resume or backend.iteration == 0:
        backend.reset(n_walkers, ndim)
        theta0 = find_map(post, seed=seed, max_local=MAP_BUDGET_PER_DIM * ndim)
        rng = np.random.default_rng(seed)
        z0 = lmap.to_z(theta0)
        p0 = z0 + 1e-2 * rng.standard_normal((n_walkers, ndim))
        for i in range(n_walkers):
            while not np.isfinite(target(p0[i])):
                p0[i] = z0 + 1e-2 * rng.standard_normal(ndim)
    else:
        # Resuming: emcee needs the last stored state explicitly.  A fresh
        # sampler object has no memory of a previous session, so passing None
        # would be interpreted as an empty initial state.
        p0 = backend.get_last_sample()
        print(f"  resuming from step {backend.iteration}")

    moves = [(emcee.moves.DEMove(), 0.8), (emcee.moves.DESnookerMove(), 0.2)]
    t0 = time.time()
    old_tau = np.inf
    converged = False
    global _WORKER_POST
    _WORKER_POST = target
    with ctx.Pool(n_proc) as pool:
        sampler = emcee.EnsembleSampler(n_walkers, ndim, _log_prob, pool=pool,
                                        moves=moves, backend=backend)
        for _ in sampler.sample(p0, iterations=max_steps, progress=progress):
            if sampler.iteration % CHECK_EVERY:
                continue
            tau = sampler.get_autocorr_time(tol=0)
            if np.all(tau * N_TAU < sampler.iteration) and \
               np.all(np.abs(old_tau - tau) / tau < TAU_TOL):
                converged = True
                break
            old_tau = tau
    runtime = time.time() - t0

    tau = sampler.get_autocorr_time(tol=0)
    tau_max = float(np.max(tau))
    burn = int(3 * tau_max)
    thin = max(1, int(tau_max / 2))
    flat_z = sampler.get_chain(discard=burn, thin=thin, flat=True)
    logp = sampler.get_log_prob(discard=burn, thin=thin, flat=True)
    flat = lmap.to_x(flat_z)
    best = flat[int(np.argmax(logp))]
    # One maximisation protocol for every model: the budget scales with the
    # dimension, so a larger model is not polished less well than a smaller one.
    best = find_map(post, x0=best, max_local=MAP_BUDGET_PER_DIM * ndim)

    lp_all = sampler.get_log_prob()
    early, late = _move_rates(lp_all)
    summary = ChainSummary(
        model=post.model_name, dataset=dataset, n_walkers=n_walkers,
        n_steps=int(sampler.iteration), burn_in=burn, thin=thin,
        tau_max=tau_max, acceptance=float(np.mean(sampler.acceptance_fraction)),
        converged=converged, seed=seed, runtime_s=runtime,
        chi2_min=float(post.chi2(best)),
        n_data=int(post.likelihood.n_data()), n_params=ndim,
        acceptance_late=late, move_rate_early=early, move_rate_late=late,
        map_budget_per_dim=MAP_BUDGET_PER_DIM)
    return flat, summary


def _move_rates(log_prob: np.ndarray) -> tuple[float, float]:
    """Fraction of steps at which a walker moved, over the first and last tenth.

    A healthy chain has the two roughly equal.  A chain whose ensemble is
    spreading faster than it mixes has the late rate well below the early one,
    and its cumulative acceptance is then meaningless.
    """
    n = log_prob.shape[0]
    if n < 20:
        return float("nan"), float("nan")
    moved = np.diff(log_prob, axis=0) != 0
    w = max(1, n // 10)
    return float(moved[:w].mean()), float(moved[-w:].mean())


def _write_chain_meta(path: Path, post: "Posterior", lmap: "LogitMap") -> None:
    """Record the coordinates the stored chain is in, next to the chain.

    The HDF5 file holds the unbounded coordinate; anything reading it directly
    needs this to get back to parameter values.
    """
    import json
    meta = dict(parametrisation="logit", model=post.model_name,
                params=list(post.param_names),
                low=lmap.low.tolist(), high=lmap.high.tolist())
    path.with_suffix(".meta.json").write_text(json.dumps(meta, indent=2))


def load_chain_meta(path: Path) -> dict | None:
    """Companion of :func:`_write_chain_meta`; ``None`` for legacy chains."""
    import json
    meta = Path(path).with_suffix(".meta.json")
    return json.loads(meta.read_text()) if meta.exists() else None


def credible_intervals(flat: np.ndarray, names: Sequence[str],
                       levels: Sequence[float] = (0.68, 0.95)) -> dict:
    """Median and equal-tailed credible intervals for every column.

    Both 68 and 95 per cent levels are stored, because parameters that vanish
    in the LambdaCDM limit pile up against their prior boundary and are
    reported as one-sided upper limits rather than as intervals.
    """
    out: dict[str, dict] = {}
    for i, name in enumerate(names):
        col = flat[:, i]
        entry = {"median": float(np.median(col)), "mean": float(np.mean(col))}
        for lev in levels:
            lo, hi = np.percentile(col, [50 * (1 - lev), 50 * (1 + lev)])
            entry[f"lo{int(lev * 100)}"] = float(lo)
            entry[f"hi{int(lev * 100)}"] = float(hi)
        out[name] = entry
    return out
