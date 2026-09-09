"""Exact stochastic kinetics of a self-reinforced, memory-carrying absorption.

The model
---------
A finite population of ``N`` identical units converts irreversibly, one unit at
a time.  With ``k`` units already converted and ``f = k/N``, the total jump
intensity is

    lambda_k = (N - k) Gamma(f, M),      Gamma(f, M) = Gamma_0 e^{alpha f + beta M},

and a *memory* variable ``M`` relaxes towards the current converted fraction,

    tau_M dM/dt = f - M .

``alpha`` is instantaneous self-reinforcement (the rate feels the present
density), ``beta`` is delayed self-reinforcement (the rate feels a lagged
average of the density).  The mean-field limit ``N -> inf`` is

    df/dt = (1 - f) Gamma(f, M),      tau_M dM/dt = f - M .

Why ``M`` matters: two states with the *same* ``f`` but different ``M`` are
physically distinguishable and evolve differently.  That is not a numerical
artefact, it is the operational content of the memory law, and
`hysteresis_experiment` is built to expose and quantify it.

Exact simulation
----------------
Between jumps ``f`` is frozen, so ``M`` relaxes monotonically,

    M(t) = f + (M_k - f) e^{-(t - t_k)/tau_M},

and therefore ``Gamma`` -- hence the intensity -- is monotone in ``t`` between
jumps.  Two *exact* samplers exploit this in different ways:

`simulate_thinning`
    Ogata / Lewis-Shedler thinning with the tight, provably valid bound
    ``lambda_max = (N-k) Gamma_0 exp(alpha k/N + beta max(M_k, f))``
    (monotonicity means ``M`` never leaves ``[min(M_k, f), max(M_k, f)]``).

`simulate_inversion`
    Direct inversion of the integrated intensity.  With ``c = M_k - f``,
    ``z = beta c`` and ``A = (N-k) Gamma_0 e^{(alpha + beta) f}``, the
    substitution ``u = z e^{-s/tau_M}`` gives in closed form

        Lambda(tau) = A tau_M [ Ei(z) - Ei(z e^{-tau/tau_M}) ] ,

    and the next inter-arrival time solves ``Lambda(tau) = -log U``.  For
    ``z = 0`` (no memory offset, or ``beta = 0``) the intensity is constant and
    ``tau = -log(U)/A``.

The two are algorithmically unrelated, so agreement between their output
distributions is a strong correctness check (see ``tests/test_stochastic.py``).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Callable

import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import expi

from .constants import SEED

# Below this |z| = |beta (M_k - f)| the exponential factor
# exp(z e^{-s/tau_M}) is 1 to within double precision over the whole interval,
# so the constant-rate (exponential) waiting time is exact and no root find is
# needed.  Chosen as ~100x the machine epsilon.
_Z_EPS = 1.0e-14

#: default tolerances of the mean-field integrator (DOP853)
RTOL = 1.0e-12
ATOL = 1.0e-14


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class Kinetics:
    """Kinetic parameters of the absorption process.

    Attributes
    ----------
    Gamma0
        Bare per-unit conversion rate (inverse time).
    alpha
        Instantaneous reinforcement: ``Gamma`` grows as ``e^{alpha f}``.
    beta
        Delayed reinforcement through the memory variable, ``e^{beta M}``.
    tau_M
        Memory relaxation time.  ``tau_M -> 0`` collapses ``M -> f`` and the
        model becomes memoryless with total reinforcement ``alpha + beta``.
    """

    Gamma0: float = 1.0
    alpha: float = 0.0
    beta: float = 0.0
    tau_M: float = 1.0

    def __post_init__(self) -> None:
        if self.Gamma0 <= 0.0:
            raise ValueError("Gamma0 must be positive")
        if self.tau_M <= 0.0:
            raise ValueError("tau_M must be positive")

    def rate(self, f: np.ndarray | float, M: np.ndarray | float) -> np.ndarray:
        """``Gamma(f, M) = Gamma_0 exp(alpha f + beta M)``."""
        return self.Gamma0 * np.exp(self.alpha * np.asarray(f) + self.beta * np.asarray(M))

    @property
    def memoryless(self) -> bool:
        """True if the memory variable does not feed back into the rate."""
        return self.beta == 0.0


# ---------------------------------------------------------------------------
# Results
# ---------------------------------------------------------------------------
@dataclass
class Ensemble:
    """Output of an exact stochastic run."""

    t: np.ndarray
    """Requested time grid, shape ``(T,)``."""
    f: np.ndarray
    """Converted fraction, shape ``(R, T)``."""
    M: np.ndarray
    """Memory variable, shape ``(R, T)``."""
    t_absorb: np.ndarray
    """Time at which each realization reached ``f = 1`` (``nan`` if it did not)."""
    N: int
    params: Kinetics
    sampler: str
    """``"thinning"`` or ``"inversion"``."""
    jump_times: list[np.ndarray] | None = None
    """Per-realization jump times, if requested."""

    @property
    def R(self) -> int:
        return self.f.shape[0]

    @property
    def mean_f(self) -> np.ndarray:
        return self.f.mean(axis=0)

    @property
    def std_f(self) -> np.ndarray:
        """Sample standard deviation across realizations (ddof = 1)."""
        return self.f.std(axis=0, ddof=1)

    @property
    def sem_f(self) -> np.ndarray:
        """Standard error of `mean_f`."""
        return self.std_f / math.sqrt(self.R)


@dataclass
class MeanField:
    """Output of the deterministic (mean-field) integration."""

    t: np.ndarray
    f: np.ndarray
    M: np.ndarray
    params: Kinetics

    def gamma(self) -> np.ndarray:
        return self.params.rate(self.f, self.M)


# ---------------------------------------------------------------------------
# Shared simulation driver
# ---------------------------------------------------------------------------
def _prepare(
    N: int, t_grid: np.ndarray, f0: float, M0: float | None, R: int
) -> tuple[np.ndarray, int, float]:
    if N < 1:
        raise ValueError("N must be a positive integer")
    if R < 1:
        raise ValueError("R must be a positive integer")
    t_grid = np.asarray(t_grid, dtype=float)
    if t_grid.ndim != 1 or t_grid.size == 0:
        raise ValueError("t_grid must be a non-empty 1-d array")
    if np.any(np.diff(t_grid) < 0.0):
        raise ValueError("t_grid must be non-decreasing")
    if t_grid[0] < 0.0:
        raise ValueError("t_grid must start at or after t = 0")
    k0 = int(round(f0 * N))
    if not 0 <= k0 <= N or abs(k0 / N - f0) > 1e-9:
        raise ValueError("f0 must be an integer multiple of 1/N in [0, 1]")
    M_start = f0 if M0 is None else float(M0)
    return t_grid, k0, M_start


def _run(
    N: int,
    t_grid: np.ndarray,
    p: Kinetics,
    *,
    R: int,
    k0: int,
    M_start: float,
    rng: np.random.Generator,
    waiting_times: Callable[..., np.ndarray],
    sampler: str,
    until_absorption: bool,
    store_jump_times: bool,
) -> Ensemble:
    """Advance ``R`` independent chains, one jump per outer iteration.

    ``waiting_times(k, f, M_ref, rng)`` must return an exact sample of the next
    inter-arrival time for each of the supplied (still active) chains.  All the
    bookkeeping -- grid interpolation, absorption times, jump records -- lives
    here so that the two samplers share it verbatim.
    """
    T = t_grid.size
    k = np.full(R, k0, dtype=np.int64)
    t_ref = np.zeros(R)
    M_ref = np.full(R, M_start)
    gi = np.zeros(R, dtype=np.int64)            # next unfilled grid index
    f_out = np.empty((R, T))
    M_out = np.empty((R, T))
    t_abs = np.full(R, np.nan)
    jumps: list[list[float]] | None = [[] for _ in range(R)] if store_jump_times else None
    tau = p.tau_M

    def fill(rows: np.ndarray, t_stop: np.ndarray) -> None:
        """Write grid values on ``[t_ref, t_stop)`` for the given rows."""
        stop_idx = np.searchsorted(t_grid, t_stop, side="left")
        todo = np.nonzero(stop_idx > gi[rows])[0]
        for pos in todo:
            r = int(rows[pos])
            lo, hi = int(gi[r]), int(stop_idx[pos])
            fr = k[r] / N
            f_out[r, lo:hi] = fr
            M_out[r, lo:hi] = fr + (M_ref[r] - fr) * np.exp(
                -(t_grid[lo:hi] - t_ref[r]) / tau
            )
            gi[r] = hi

    while True:
        alive = k < N
        if not until_absorption:
            alive &= gi < T
        rows = np.nonzero(alive)[0]
        if rows.size == 0:
            break

        f_now = k[rows] / N
        dt = waiting_times(k[rows], f_now, M_ref[rows], rng)
        t_new = t_ref[rows] + dt

        fill(rows, t_new)

        # the jump itself
        M_ref[rows] = f_now + (M_ref[rows] - f_now) * np.exp(-dt / tau)
        t_ref[rows] = t_new
        k[rows] += 1
        if jumps is not None:
            for pos, r in enumerate(rows):
                jumps[int(r)].append(float(t_new[pos]))
        done = np.nonzero(k[rows] == N)[0]
        if done.size:
            t_abs[rows[done]] = t_new[done]

    # tail: absorbed chains sit at f = 1 with M relaxing to 1
    remaining = np.nonzero(gi < T)[0]
    for r in remaining:
        lo = int(gi[r])
        fr = k[r] / N
        f_out[r, lo:] = fr
        M_out[r, lo:] = fr + (M_ref[r] - fr) * np.exp(-(t_grid[lo:] - t_ref[r]) / tau)
        gi[r] = T

    return Ensemble(
        t=t_grid,
        f=f_out,
        M=M_out,
        t_absorb=t_abs,
        N=N,
        params=p,
        sampler=sampler,
        jump_times=None if jumps is None else [np.asarray(j) for j in jumps],
    )


# ---------------------------------------------------------------------------
# (a) thinning sampler
# ---------------------------------------------------------------------------
def simulate_thinning(
    N: int,
    t_grid: np.ndarray,
    params: Kinetics = Kinetics(),
    *,
    R: int = 1,
    f0: float = 0.0,
    M0: float | None = None,
    seed: int = SEED,
    until_absorption: bool = False,
    store_jump_times: bool = False,
) -> Ensemble:
    """Exact simulation by Ogata thinning, vectorized over realizations.

    Because ``M`` moves monotonically from ``M_k`` towards ``f`` between jumps,

        Gamma(f, M(s)) <= Gamma_0 exp(alpha f + beta max(M_k, f))   for all s >= 0,

    which gives the dominating (constant) intensity
    ``lambda_max = (N-k) Gamma_0 exp(alpha k/N + beta max(M_k, f))``.  Proposals
    are drawn from a Poisson process of that rate and kept with probability
    ``lambda(s)/lambda_max``; the retained points are exactly the jumps of the
    inhomogeneous process.  The bound is tight -- it is attained at one end of
    every inter-jump interval -- so the acceptance rate is close to one and the
    cost is essentially one exponential draw per jump.

    Parameters
    ----------
    N
        Population size.
    t_grid
        Non-decreasing output times, starting at or after ``t = 0``.
    params
        `Kinetics`.
    R
        Number of independent realizations.
    f0, M0
        Initial converted fraction (a multiple of ``1/N``) and initial memory;
        ``M0 = None`` means an equilibrated memory ``M0 = f0``.
    seed
        Seed of the ``numpy`` Generator.
    until_absorption
        Keep simulating past the end of ``t_grid`` until every chain reaches
        ``f = 1``, so that `Ensemble.t_absorb` is populated.
    store_jump_times
        Record every jump time (memory-hungry for large ``N R``).

    Returns
    -------
    Ensemble
    """
    t_grid, k0, M_start = _prepare(N, t_grid, f0, M0, R)
    p = params
    rng = np.random.default_rng(seed)

    def waiting_times(
        k: np.ndarray, f: np.ndarray, M_ref: np.ndarray, rng: np.random.Generator
    ) -> np.ndarray:
        lam_max = (N - k) * p.Gamma0 * np.exp(
            p.alpha * f + p.beta * np.maximum(M_ref, f)
        )
        s = np.zeros(f.size)
        pending = np.ones(f.size, dtype=bool)
        while True:
            j = np.nonzero(pending)[0]
            if j.size == 0:
                return s
            s[j] -= np.log(rng.random(j.size)) / lam_max[j]
            M_now = f[j] + (M_ref[j] - f[j]) * np.exp(-s[j] / p.tau_M)
            lam = (N - k[j]) * p.Gamma0 * np.exp(p.alpha * f[j] + p.beta * M_now)
            pending[j] = rng.random(j.size) * lam_max[j] >= lam

    return _run(
        N,
        t_grid,
        p,
        R=R,
        k0=k0,
        M_start=M_start,
        rng=rng,
        waiting_times=waiting_times,
        sampler="thinning",
        until_absorption=until_absorption,
        store_jump_times=store_jump_times,
    )


# ---------------------------------------------------------------------------
# (b) inversion sampler
# ---------------------------------------------------------------------------
def integrated_intensity(
    tau: float | np.ndarray, A: float, z: float, tau_M: float
) -> float | np.ndarray:
    """``Lambda(tau)``, the intensity integrated over one inter-jump interval.

    With ``lambda(s) = A exp(z e^{-s/tau_M})`` (``A = (N-k) Gamma_0 e^{(alpha+beta)f}``
    and ``z = beta (M_k - f)``), the substitution ``u = z e^{-s/tau_M}``,
    ``ds = -tau_M du/u`` turns the integral into an exponential integral:

        Lambda(tau) = A tau_M int_{z e^{-tau/tau_M}}^{z} e^u / u du
                    = A tau_M [ Ei(z) - Ei(z e^{-tau/tau_M}) ] .

    The two ``Ei`` terms individually diverge logarithmically as their argument
    goes to zero, but the difference stays finite and grows like ``A tau`` at
    large ``tau``, which is what makes the inversion always solvable.
    """
    if z == 0.0:
        return A * np.asarray(tau, dtype=float)
    return A * tau_M * (expi(z) - expi(z * np.exp(-np.asarray(tau, dtype=float) / tau_M)))


def _inversion_residual(
    s: float, A: float, tau_M: float, z: float, ei_z: float, target: float
) -> float:
    """``Lambda(s) - target`` with ``Ei(z)`` hoisted out of the iteration."""
    return A * tau_M * (ei_z - float(expi(z * math.exp(-s / tau_M)))) - target


def _invert_one(A: float, z: float, tau_M: float, target: float) -> float:
    """Solve ``Lambda(tau) = target`` for ``tau > 0`` (exact next arrival time).

    The intensity is monotone between ``lambda(0) = A e^z`` and
    ``lambda(inf) = A``, so the constant-rate answers at those two extremes
    bracket the true root:

        target / (A max(1, e^z))  <=  tau  <=  target / (A min(1, e^z)) .

    The bracket is tight whenever ``|z| = |beta (M_k - f)|`` is small, which is
    the generic situation once the memory has caught up with ``f``, and
    ``brentq`` then converges in a handful of iterations.
    """
    if abs(z) < _Z_EPS:
        return target / A
    ez = math.exp(z)
    lo = target / (A * max(1.0, ez)) * (1.0 - 1.0e-12)
    hi = target / (A * min(1.0, ez)) * (1.0 + 1.0e-12)
    return brentq(
        _inversion_residual,
        lo,
        hi,
        args=(A, tau_M, z, float(expi(z)), target),
        xtol=1e-15,
        rtol=8.9e-16,
        maxiter=100,
    )


def simulate_inversion(
    N: int,
    t_grid: np.ndarray,
    params: Kinetics = Kinetics(),
    *,
    R: int = 1,
    f0: float = 0.0,
    M0: float | None = None,
    seed: int = SEED,
    until_absorption: bool = False,
    store_jump_times: bool = False,
) -> Ensemble:
    """Exact simulation by inverting the integrated intensity.

    The next inter-arrival time ``tau`` satisfies ``Lambda(tau) = -log U`` with
    ``U ~ Uniform(0,1)`` -- the standard time-rescaling (random time change)
    construction.  `integrated_intensity` gives ``Lambda`` in closed form via
    the exponential integral, and ``scipy.optimize.brentq`` inverts it on a
    bracket derived from the elementary bound ``lambda(s) >= A min(1, e^z)``.

    No approximation is made anywhere: this sampler and `simulate_thinning`
    target exactly the same law by construction, which is what the
    Kolmogorov-Smirnov cross-check in the test suite verifies empirically.

    Parameters are as in `simulate_thinning`.
    """
    t_grid, k0, M_start = _prepare(N, t_grid, f0, M0, R)
    p = params
    rng = np.random.default_rng(seed)
    tau_M = p.tau_M

    def waiting_times(
        k: np.ndarray, f: np.ndarray, M_ref: np.ndarray, rng: np.random.Generator
    ) -> np.ndarray:
        A = (N - k) * p.Gamma0 * np.exp((p.alpha + p.beta) * f)
        z = p.beta * (M_ref - f)
        target = -np.log(rng.random(f.size))
        if p.beta == 0.0:
            return target / A
        out = np.empty(f.size)
        for i in range(f.size):
            out[i] = _invert_one(float(A[i]), float(z[i]), tau_M, float(target[i]))
        return out

    return _run(
        N,
        t_grid,
        p,
        R=R,
        k0=k0,
        M_start=M_start,
        rng=rng,
        waiting_times=waiting_times,
        sampler="inversion",
        until_absorption=until_absorption,
        store_jump_times=store_jump_times,
    )


# ---------------------------------------------------------------------------
# Mean-field limit
# ---------------------------------------------------------------------------
def _mean_field_rhs(
    t: float,
    y: np.ndarray,
    p: Kinetics,
    boost: Callable[[float], float],
    a_inv3: Callable[[float], float],
) -> list[float]:
    """``(f, M, V)`` right-hand side; ``V`` accumulates ``int a^-3 df``."""
    f, M, _ = y
    g = p.Gamma0 * boost(t) * math.exp(p.alpha * f + p.beta * M)
    df = (1.0 - f) * g
    return [df, (f - M) / p.tau_M, a_inv3(t) * df]


def _unit(_t: float) -> float:
    return 1.0


def deterministic(
    t_grid: np.ndarray,
    params: Kinetics = Kinetics(),
    *,
    f0: float = 0.0,
    M0: float | None = None,
    rtol: float = RTOL,
    atol: float = ATOL,
) -> MeanField:
    """Integrate the mean-field pair with ``solve_ivp(method="DOP853")``.

        df/dt = (1 - f) Gamma(f, M),      tau_M dM/dt = f - M .

    Parameters
    ----------
    t_grid
        Output times; the integration starts at ``t = 0``.
    params, f0, M0
        As in `simulate_thinning` (``M0 = None`` means ``M0 = f0``).
    rtol, atol
        Solver tolerances; the defaults are tight enough that the solution can
        be compared with closed forms at the 1e-10 level.
    """
    t_grid = np.asarray(t_grid, dtype=float)
    M_start = f0 if M0 is None else float(M0)
    t_end = float(max(t_grid[-1], 0.0))
    sol = solve_ivp(
        _mean_field_rhs,
        (0.0, t_end if t_end > 0.0 else 1.0),
        [float(f0), M_start, 0.0],
        args=(params, _unit, _unit),
        method="DOP853",
        t_eval=t_grid,
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")
    return MeanField(t=sol.t, f=sol.y[0], M=sol.y[1], params=params)


# ---------------------------------------------------------------------------
# Hysteresis: same density, different memory, different future
# ---------------------------------------------------------------------------
@dataclass
class Hysteresis:
    """Result of `hysteresis_experiment`.

    Histories ``A`` and ``B`` are constructed to carry *identical* converted
    fractions at ``t_checkpoint`` and *different* memories.  From there on they
    evolve under identical conditions, so any subsequent difference is caused by
    ``M`` alone.
    """

    t_checkpoint: float
    f_checkpoint: float
    M_A: float
    M_B: float
    delta_M: float
    t: np.ndarray
    f_A: np.ndarray
    f_B: np.ndarray
    M_A_traj: np.ndarray
    M_B_traj: np.ndarray
    f_final_A: float
    f_final_B: float
    delta_f_final: float
    V_A: float
    V_B: float
    delta_V: float
    relative_delta_V: float
    prep: dict = field(default_factory=dict)
    """How history B was prepared (pulse amplitude, solved initial fraction...)."""

    @property
    def residual_ratio(self) -> float:
        """``(1 - f_B)/(1 - f_A)`` at ``t_final``.

        The converted fractions themselves both approach 1, so the sharpest way
        to state the effect is as a ratio of the *unconverted remainders*: a
        value far from 1 means the two histories are still visibly different
        after the checkpoint.
        """
        num, den = 1.0 - self.f_final_B, 1.0 - self.f_final_A
        return num / den if den != 0.0 else float("inf")


def hysteresis_experiment(
    params: Kinetics = Kinetics(Gamma0=0.15, alpha=2.0, beta=4.0, tau_M=12.0),
    *,
    f_start: float = 0.05,
    f_start_ratio: float = 0.1,
    t_prepare: float = 1.0,
    t_final: float = 5.0,
    pulse_end: float | None = None,
    amplitude_max: float = 1.0e6,
    a: Callable[[float], float] | None = None,
    n_grid: int = 601,
    rtol: float = RTOL,
    atol: float = ATOL,
) -> Hysteresis:
    """Two histories, one density, two futures -- the memory law made operational.

    Construction
    ------------
    *History A* starts at ``(f_start, M = f_start)`` -- an equilibrated memory,
    i.e. no prior history -- and runs at the bare rate up to ``t_prepare``,
    arriving at the checkpoint state ``(f_c, M_A)``.

    *History B* starts *behind*, at ``f_B0 = f_start_ratio * f_start`` with an
    equally equilibrated memory, and is pushed by a temporary pulse
    ``Gamma_0 -> (1 + p) Gamma_0`` acting on ``[0, pulse_end]`` and switched off
    afterwards.  The amplitude ``p`` is solved for with ``brentq`` so that
    ``f_B(t_prepare) = f_c`` to solver tolerance.  Such a root always exists:
    at ``p = 0`` history B is strictly behind (it started lower and the flow is
    monotone in its initial condition), and as ``p`` grows ``f_B(t_prepare)``
    increases continuously towards 1.

    At the checkpoint the two states therefore have *identical* ``f`` and
    *different* ``M``: B spent its past at a lower density and its lagged memory
    still records that.  From ``t_prepare`` on, both are evolved with exactly
    the same parameters and no pulse, and two observables are compared:

    ``f(t_final)``
        the converted fraction at the end of the window.  Both histories tend to
        ``f = 1`` as ``t -> inf`` (the kinetics is irreversible and the rate is
        bounded below by ``Gamma_0``), so memory does not change *whether* the
        population converts -- it changes *when*, and any finite observing
        window sees that as a difference in the converted fraction.

    ``V = int a(t)^-3 df``
        the vacuum-energy-like increment accumulated along the history.  With
        the default ``a = 1`` this is just ``f(t_final) - f_c``, the
        pure-kinetics statement.  With an expanding ``a(t)`` supplied by the
        caller the integrand is damped and the integral converges as
        ``t -> inf``, so ``Delta V`` becomes a genuinely *asymptotic* invariant
        that distinguishes the two histories forever.

    With ``beta = 0`` the memory does not enter the rate, the two futures
    coincide identically, and every reported difference collapses to solver
    noise.  That is the control case, and the test suite checks both branches.

    Parameters
    ----------
    params
        `Kinetics`; ``beta > 0`` for the effect, ``beta = 0`` for the control.
    f_start
        Initial converted fraction of history A.
    f_start_ratio
        History B starts at ``f_start_ratio * f_start``; must be in ``(0, 1)``.
    t_prepare
        Checkpoint time at which the two densities are made equal.
    t_final
        End of the common forward evolution.
    pulse_end
        End of B's pulse; defaults to ``t_prepare / 2``.
    amplitude_max
        Upper limit of the amplitude search.
    a
        Scale factor ``a(t)``; ``None`` means ``a = 1``.
    n_grid
        Number of output times on ``[t_prepare, t_final]``.

    Returns
    -------
    Hysteresis
    """
    if pulse_end is None:
        pulse_end = 0.5 * t_prepare
    if not 0.0 < pulse_end <= t_prepare:
        raise ValueError("require 0 < pulse_end <= t_prepare")
    if t_final <= t_prepare:
        raise ValueError("require t_final > t_prepare")
    if not 0.0 < f_start_ratio < 1.0:
        raise ValueError("require 0 < f_start_ratio < 1")
    a_fn = (lambda t: 1.0) if a is None else a
    a_inv3: Callable[[float], float] = lambda t: float(a_fn(t)) ** -3

    def evolve(
        y0: list[float],
        t0: float,
        t1: float,
        boost: Callable[[float], float],
        t_eval: np.ndarray | None = None,
    ):
        sol = solve_ivp(
            _mean_field_rhs,
            (t0, t1),
            y0,
            args=(params, boost, a_inv3),
            method="DOP853",
            t_eval=t_eval,
            rtol=rtol,
            atol=atol,
        )
        if not sol.success:
            raise RuntimeError(f"solve_ivp failed: {sol.message}")
        return sol

    # --- history A: the reference preparation ------------------------------
    solA = evolve([f_start, f_start, 0.0], 0.0, t_prepare, _unit)
    f_c = float(solA.y[0, -1])
    M_A = float(solA.y[1, -1])

    # --- history B: same f at the checkpoint, reached through a pulse -------
    f_b0 = f_start_ratio * f_start

    def miss(amp: float) -> float:
        boost = lambda t: (1.0 + amp) if t <= pulse_end else 1.0
        s = evolve([f_b0, f_b0, 0.0], 0.0, t_prepare, boost)
        return float(s.y[0, -1]) - f_c

    if miss(0.0) >= 0.0:
        raise RuntimeError("history B is not behind history A at zero pulse")
    hi = 1.0
    while miss(hi) < 0.0:
        hi *= 2.0
        if hi > amplitude_max:
            raise RuntimeError(
                "no pulse amplitude below amplitude_max reaches the checkpoint"
            )
    amp = brentq(miss, 0.0, hi, xtol=1e-14, rtol=8.9e-16, maxiter=200)
    boost_B = lambda t: (1.0 + amp) if t <= pulse_end else 1.0
    solB = evolve([f_b0, f_b0, 0.0], 0.0, t_prepare, boost_B)
    M_B = float(solB.y[1, -1])
    f_c_B = float(solB.y[0, -1])

    # --- identical forward evolution ---------------------------------------
    t = np.linspace(t_prepare, t_final, n_grid)
    fwdA = evolve([f_c, M_A, 0.0], t_prepare, t_final, _unit, t_eval=t)
    fwdB = evolve([f_c_B, M_B, 0.0], t_prepare, t_final, _unit, t_eval=t)

    V_A, V_B = float(fwdA.y[2, -1]), float(fwdB.y[2, -1])
    dV = V_A - V_B
    scale = max(abs(V_A), abs(V_B))
    return Hysteresis(
        t_checkpoint=t_prepare,
        f_checkpoint=f_c,
        M_A=M_A,
        M_B=M_B,
        delta_M=M_A - M_B,
        t=t,
        f_A=fwdA.y[0],
        f_B=fwdB.y[0],
        M_A_traj=fwdA.y[1],
        M_B_traj=fwdB.y[1],
        f_final_A=float(fwdA.y[0, -1]),
        f_final_B=float(fwdB.y[0, -1]),
        delta_f_final=float(fwdA.y[0, -1] - fwdB.y[0, -1]),
        V_A=V_A,
        V_B=V_B,
        delta_V=dV,
        relative_delta_V=dV / scale if scale > 0.0 else 0.0,
        prep={
            "f_start_A": f_start,
            "f_start_B": f_b0,
            "pulse_amplitude": amp,
            "pulse_end": pulse_end,
            "checkpoint_mismatch": f_c_B - f_c,
        },
    )


# ---------------------------------------------------------------------------
# Sensitivity to the initial condition
# ---------------------------------------------------------------------------
@dataclass
class Sensitivity:
    """Tangent (variational) solution of the mean-field flow."""

    t: np.ndarray
    f: np.ndarray
    M: np.ndarray
    J: np.ndarray
    """``J(t) = d f(t) / d f_i`` from the variational equations."""
    J_memory: np.ndarray
    """``d M(t) / d f_i``, the memory component of the same tangent vector."""
    J_closed_form: np.ndarray | None
    """``F(f(t))/F(f_i)`` with ``F(f) = (1-f) Gamma(f)``; only for ``beta = 0``."""
    params: Kinetics

    @property
    def max_abs_error(self) -> float:
        """Largest ``|J - J_closed_form|``; ``nan`` when no closed form exists."""
        if self.J_closed_form is None:
            return float("nan")
        return float(np.max(np.abs(self.J - self.J_closed_form)))


def sensitivity(
    t_grid: np.ndarray,
    params: Kinetics = Kinetics(),
    *,
    f0: float = 0.0,
    M0: float | None = None,
    perturb_memory: bool = False,
    rtol: float = RTOL,
    atol: float = ATOL,
) -> Sensitivity:
    """Integrate the tangent system alongside the mean-field solution.

    With ``y = (f, M)`` and ``y' = F(y)``, the derivative of the flow with
    respect to the initial converted fraction, ``v = dy/df_i``, obeys the
    variational (tangent) equation ``v' = DF(y) v`` with

        DF = [[ (alpha (1-f) - 1) Gamma ,  beta (1-f) Gamma ],
              [ 1/tau_M                 , -1/tau_M          ]] ,

    started from ``v(0) = (1, 0)`` -- or ``(1, 1)`` if ``perturb_memory`` is set,
    i.e. if the memory is taken to be equilibrated with the perturbed initial
    density.

    Closed form.  For ``beta = 0`` the memory decouples from the rate and the
    ``f`` equation is autonomous, ``f' = F(f) := (1-f) Gamma_0 e^{alpha f}``.
    Any autonomous scalar flow has ``d f(t)/d f_i = F(f(t))/F(f_i)`` (both sides
    solve the same linear equation with the same initial value), and that is
    what `Sensitivity.J_closed_form` holds.

    Interpretation: ``J > 1`` means the run-away is amplifying initial
    differences; ``J -> 0`` means the absorption has erased them.
    """
    t_grid = np.asarray(t_grid, dtype=float)
    p = params
    M_start = f0 if M0 is None else float(M0)

    def rhs(t: float, y: np.ndarray) -> list[float]:
        f, M, vf, vM = y
        g = p.Gamma0 * math.exp(p.alpha * f + p.beta * M)
        dvf = (p.alpha * (1.0 - f) - 1.0) * g * vf + p.beta * (1.0 - f) * g * vM
        dvM = (vf - vM) / p.tau_M
        return [(1.0 - f) * g, (f - M) / p.tau_M, dvf, dvM]

    y0 = [float(f0), M_start, 1.0, 1.0 if perturb_memory else 0.0]
    sol = solve_ivp(
        rhs,
        (0.0, float(t_grid[-1])),
        y0,
        method="DOP853",
        t_eval=t_grid,
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")

    closed = None
    if p.memoryless:
        F = lambda x: (1.0 - x) * p.Gamma0 * np.exp(p.alpha * x)
        closed = F(sol.y[0]) / F(float(f0))
    return Sensitivity(
        t=sol.t,
        f=sol.y[0],
        M=sol.y[1],
        J=sol.y[2],
        J_memory=sol.y[3],
        J_closed_form=closed,
        params=p,
    )


# ---------------------------------------------------------------------------
# Phase portrait and the acceleration criterion
# ---------------------------------------------------------------------------
def acceleration_functional(
    f: np.ndarray, M: np.ndarray, p: Kinetics
) -> np.ndarray:
    """``d/dt log Gamma - Gamma`` on the mean-field flow.

    Explicitly ``alpha (1-f) Gamma + (beta/tau_M) (f - M) - Gamma``.  It is
    positive exactly where the reinforcement outruns the depletion of the
    unconverted pool, i.e. where the conversion *accelerates*; the criterion
    quoted in the paper is that this functional be positive.
    """
    g = p.rate(f, M)
    return p.alpha * (1.0 - f) * g + (p.beta / p.tau_M) * (f - M) - g


def phase_portrait_data(
    params: Kinetics = Kinetics(),
    *,
    f_range: tuple[float, float] = (0.0, 1.0),
    M_range: tuple[float, float] = (0.0, 1.0),
    n_f: int = 41,
    n_M: int = 41,
    n_boundary: int = 401,
) -> dict[str, np.ndarray]:
    """Vector field and acceleration boundary on the ``(f, M)`` square.

    Returns a dict with

    ``f``, ``M``
        ``(n_M, n_f)`` meshgrid (``indexing="xy"``);
    ``dfdt``, ``dMdt``
        the mean-field vector field there;
    ``gamma``
        ``Gamma(f, M)`` on the same grid;
    ``accel``
        `acceleration_functional`, whose zero level set is the boundary;
    ``accelerating``
        boolean mask ``accel > 0``;
    ``boundary_f``, ``boundary_M``
        an explicit parametrisation of the boundary, obtained by solving
        ``accel(f, M) = 0`` for ``M`` at each ``f`` with ``brentq``.  Entries
        are ``nan`` where the boundary leaves ``M_range``.  For ``beta = 0`` the
        criterion does not involve ``M`` at all and the boundary is the vertical
        line ``alpha (1 - f) = 1``, which is returned as a constant ``f`` column.
    """
    fs = np.linspace(*f_range, n_f)
    Ms = np.linspace(*M_range, n_M)
    F, Mg = np.meshgrid(fs, Ms, indexing="xy")
    g = params.rate(F, Mg)
    accel = acceleration_functional(F, Mg, params)

    fb = np.linspace(*f_range, n_boundary)
    Mb = np.full(n_boundary, np.nan)
    if params.beta != 0.0:
        for i, fv in enumerate(fb):
            lo = acceleration_functional(np.array(fv), np.array(M_range[0]), params)
            hi = acceleration_functional(np.array(fv), np.array(M_range[1]), params)
            if float(lo) * float(hi) < 0.0:
                Mb[i] = brentq(
                    lambda m: float(
                        acceleration_functional(np.array(fv), np.array(m), params)
                    ),
                    M_range[0],
                    M_range[1],
                    xtol=1e-14,
                )
    elif params.alpha > 1.0:
        # alpha (1 - f) = 1  =>  f = 1 - 1/alpha, independent of M
        fb = np.full(n_boundary, 1.0 - 1.0 / params.alpha)
        Mb = np.linspace(*M_range, n_boundary)

    return {
        "f": F,
        "M": Mg,
        "dfdt": (1.0 - F) * g,
        "dMdt": (F - Mg) / params.tau_M,
        "gamma": g,
        "accel": accel,
        "accelerating": accel > 0.0,
        "boundary_f": fb,
        "boundary_M": Mb,
    }
