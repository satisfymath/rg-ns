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
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Callable, Sequence

import numpy as np

from .constants import SEED
from .params import MODELS, Model

ROOT = Path(__file__).resolve().parents[2]
CHAIN_DIR = ROOT / "results" / "chains"

N_TAU = 50           # require chain length > N_TAU * tau
TAU_TOL = 0.02       # and tau stable to 2% between checks
CHECK_EVERY = 500

#: Measured resident size of one worker after the data are loaded and one
#: likelihood has been evaluated.  Most of it is copy-on-write shared with the
#: parent under the fork start method, so this is a conservative upper bound.
WORKER_RSS_MB = 260
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
def find_map(post: Posterior, n_starts: int = 4, seed: int = SEED,
             x0: np.ndarray | None = None) -> np.ndarray:
    """Best-fit parameters.

    If ``x0`` is given, normally the best sample of an existing chain, a single
    local refinement is run from it: the chain has already located the mode, so
    repeating a global search wastes more time than the chain itself took.
    Otherwise a short multi-start Latin-hypercube search seeds the walkers.
    The iteration caps matter, because an uncapped Powell run on a 13 ms
    likelihood dominates the total runtime.
    """
    from scipy.optimize import minimize
    from scipy.stats import qmc

    lows = np.array([p.low for p in _priors_of(post)])
    highs = np.array([p.high for p in _priors_of(post)])
    if x0 is not None:
        starts = np.atleast_2d(np.asarray(x0, dtype=float))
    else:
        starts = qmc.LatinHypercube(d=post.ndim, seed=seed).random(n_starts)
        starts = lows + starts * (highs - lows)

    def neg(theta):
        v = post(theta)
        return 1e10 if not np.isfinite(v) else -v

    best, best_val = None, np.inf
    for start in starts:
        try:
            r = minimize(neg, start, method="Powell",
                         options=dict(maxiter=40, maxfev=4000,
                                      xtol=1e-4, ftol=1e-6))
            r = minimize(neg, r.x, method="Nelder-Mead",
                         options=dict(maxiter=1500, maxfev=1500,
                                      xatol=1e-5, fatol=1e-6))
        except Exception:                                          # pragma: no cover
            continue
        if r.fun < best_val:
            best, best_val = r.x, r.fun
    if best is None:                                               # pragma: no cover
        raise RuntimeError("MAP search failed from every start")
    return np.asarray(best, dtype=float)


def _priors_of(post: Posterior):
    from .params import PRIORS
    return post.model.priors() + [PRIORS[n] for n in post.nuisance]


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
    if not resume or backend.iteration == 0:
        backend.reset(n_walkers, ndim)
        theta0 = find_map(post, seed=seed)
        rng = np.random.default_rng(seed)
        widths = np.array([(p.high - p.low) for p in _priors_of(post)])
        p0 = theta0 + 1e-3 * widths * rng.standard_normal((n_walkers, ndim))
        # reject starting points outside the prior
        for i in range(n_walkers):
            while not np.isfinite(post.log_prior(p0[i])):
                p0[i] = theta0 + 1e-3 * widths * rng.standard_normal(ndim)
    else:
        p0 = None

    moves = [(emcee.moves.DEMove(), 0.8), (emcee.moves.DESnookerMove(), 0.2)]
    t0 = time.time()
    old_tau = np.inf
    converged = False
    global _WORKER_POST
    _WORKER_POST = post
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
    flat = sampler.get_chain(discard=burn, thin=thin, flat=True)
    logp = sampler.get_log_prob(discard=burn, thin=thin, flat=True)
    best = flat[int(np.argmax(logp))]

    summary = ChainSummary(
        model=post.model_name, dataset=dataset, n_walkers=n_walkers,
        n_steps=int(sampler.iteration), burn_in=burn, thin=thin,
        tau_max=tau_max, acceptance=float(np.mean(sampler.acceptance_fraction)),
        converged=converged, seed=seed, runtime_s=runtime,
        chi2_min=float(post.chi2(best)),
        n_data=int(post.likelihood.n_data()), n_params=ndim)
    return flat, summary


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
