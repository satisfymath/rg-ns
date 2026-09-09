"""Collective absorption of ``N`` two-level units as a Lindblad master equation.

The microscopic model
---------------------
Each unit lives in ``span{|I>, |A>}`` (intact / absorbed).  Absorption is an
irreversible quantum jump driven by one Lindblad operator per unit,

    L_i = |A_i><I_i| sqrt( Gamma_0 exp(alpha fhat_{-i}) ),
    fhat_{-i} = (1/(N-1)) sum_{j != i} n_j ,      n_j = |A_j><A_j| ,

so the rate at which unit ``i`` converts depends on how many *other* units have
already converted -- the microscopic origin of the self-reinforcement
``Gamma = Gamma_0 e^{alpha f}`` used in the cosmological model.  ``fhat_{-i}``
is diagonal in the occupation basis, so ``L_i`` maps one basis state to exactly
one basis state.  For ``N = 1`` the empty average is taken to be zero and the
rate is the bare ``Gamma_0``.

The density matrix evolves by

    d rho/dt = sum_i ( L_i rho L_i^dag - {L_i^dag L_i, rho}/2 ) .

Two structural consequences are exploited (and tested):

1. *Populations decouple from coherences.*  ``L_i`` is a single basis-to-basis
   map and ``L_i^dag L_i`` is diagonal, so the Liouvillian never feeds a
   coherence into a population.  The occupation numbers ``<n_i>(t)`` therefore
   depend on the initial state only through its populations -- a coherent
   product state ``((|I> + |A>)/sqrt2)^{tensor N}`` and the maximally mixed
   state give *identical* absorption curves.  Absorption is classical here; the
   quantum-ness of the initial state buys nothing.

2. *Permutation symmetry closes the chain.*  A permutation-symmetric initial
   state stays symmetric, and the dynamics reduces to an ``(N+1)``-state
   birth chain (`dicke_master`) with rates
   ``(N-k) Gamma_0 exp(alpha k/(N-1))``, which can be integrated for
   ``N ~ 10^4`` -- far beyond the ``4^N``-dimensional Liouvillian, which caps
   out around ``N = 8``.

The mean-field closure ``<(1-f) e^{alpha f}> -> (1 - <f>) e^{alpha <f>}`` costs
an error of order ``1/N``; `closure_error_scaling` measures the exponent.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Literal, Sequence

import numpy as np
import scipy.sparse as sps
from scipy.integrate import solve_ivp

#: tolerances of the master-equation integrator
RTOL = 1.0e-10
ATOL = 1.0e-12

#: largest N for which the full 4^N Liouvillian is built by default
MAX_FULL_N = 8

InitialState = Literal["ground", "coherent", "mixed"]


# ---------------------------------------------------------------------------
# Occupation-basis bookkeeping
# ---------------------------------------------------------------------------
def occupation_numbers(N: int) -> np.ndarray:
    """``(2^N, N)`` array of bits: entry ``[s, i]`` is ``n_i`` in basis state ``s``."""
    s = np.arange(1 << N, dtype=np.int64)
    return ((s[:, None] >> np.arange(N)[None, :]) & 1).astype(np.int64)


def converted_counts(N: int) -> np.ndarray:
    """``k(s)``, the number of converted units in each basis state."""
    return occupation_numbers(N).sum(axis=1)


def _environment_fraction(k: np.ndarray | int, N: int) -> np.ndarray:
    """``fhat_{-i} = k/(N-1)``, with the empty average defined as 0 for ``N = 1``."""
    if N == 1:
        return np.zeros_like(np.asarray(k, dtype=float))
    return np.asarray(k, dtype=float) / (N - 1)


def jump_operator(i: int, N: int, Gamma0: float, alpha: float) -> sps.csr_matrix:
    """``L_i`` in the occupation basis, as a sparse ``(2^N, 2^N)`` matrix.

    ``L_i`` takes every basis state with ``n_i = 0`` to the state with that bit
    set, weighted by ``sqrt(Gamma_0 exp(alpha k/(N-1)))`` where ``k`` counts the
    *other* converted units (which, since ``n_i = 0``, is just ``k(s)``).
    """
    D = 1 << N
    s = np.arange(D, dtype=np.int64)
    bit = np.int64(1) << i
    src = s[(s & bit) == 0]
    k = converted_counts(N)[src]
    amp = np.sqrt(Gamma0 * np.exp(alpha * _environment_fraction(k, N)))
    dst = src | bit
    return sps.csr_matrix((amp, (dst, src)), shape=(D, D))


def liouvillian(N: int, Gamma0: float = 1.0, alpha: float = 0.0) -> sps.csr_matrix:
    """Superoperator acting on the row-major vectorisation of ``rho``.

    Using ``vec(A rho B) = (A kron B^T) vec(rho)`` for C-ordered vectorisation
    and the fact that ``L_i^dag L_i`` is diagonal (hence symmetric and real),

        Lsup = sum_i [ L_i kron L_i - (1/2) (L_i^dag L_i) kron 1
                                    - (1/2) 1 kron (L_i^dag L_i) ] .

    Everything is real, so the result is a real sparse matrix of size ``4^N``.
    """
    D = 1 << N
    eye = sps.identity(D, format="csr")
    total = sps.csr_matrix((D * D, D * D))
    for i in range(N):
        L = jump_operator(i, N, Gamma0, alpha)
        LdL = (L.T @ L).tocsr()          # diagonal
        total = total + sps.kron(L, L, format="csr")
        total = total - 0.5 * sps.kron(LdL, eye, format="csr")
        total = total - 0.5 * sps.kron(eye, LdL, format="csr")
    return total.tocsr()


def initial_density_matrix(N: int, kind: InitialState = "ground") -> np.ndarray:
    """Dense ``(2^N, 2^N)`` initial state.

    ``"ground"``
        ``|I...I><I...I|`` -- nothing converted yet.
    ``"coherent"``
        ``((|I> + |A>)/sqrt2)^{tensor N}``, a pure product superposition; every
        matrix element equals ``2^-N``, so it is maximally coherent.
    ``"mixed"``
        ``1/2^N`` times the identity: the *same populations* as ``"coherent"``
        with every coherence removed.
    """
    D = 1 << N
    if kind == "ground":
        rho = np.zeros((D, D))
        rho[0, 0] = 1.0
        return rho
    if kind == "coherent":
        psi = np.full(D, D ** -0.5)
        return np.outer(psi, psi)
    if kind == "mixed":
        return np.eye(D) / D
    raise ValueError(f"unknown initial state {kind!r}")


# ---------------------------------------------------------------------------
# Full master equation
# ---------------------------------------------------------------------------
@dataclass
class LindbladRun:
    """Solution of the ``4^N``-dimensional master equation."""

    t: np.ndarray
    n: np.ndarray
    """``(N, T)`` occupation numbers ``<n_i>(t)``."""
    f: np.ndarray
    """``(T,)`` mean converted fraction ``<fhat>(t) = (1/N) sum_i <n_i>``."""
    populations: np.ndarray
    """``(2^N, T)`` diagonal of ``rho``."""
    coherence: np.ndarray
    """``(T,)`` sum of ``|rho_{s s'}|`` over ``s != s'``: the total coherence."""
    trace: np.ndarray
    """``(T,)`` ``tr rho``; deviation from 1 measures integration error."""
    N: int
    Gamma0: float
    alpha: float


def solve_master(
    N: int,
    t_grid: np.ndarray,
    *,
    Gamma0: float = 1.0,
    alpha: float = 0.0,
    initial: InitialState | np.ndarray = "ground",
    rtol: float = RTOL,
    atol: float = ATOL,
    max_full_N: int = MAX_FULL_N,
) -> LindbladRun:
    """Integrate ``d rho/dt = L[rho]`` with ``solve_ivp(method="DOP853")``.

    The Liouvillian is built once as a sparse ``4^N x 4^N`` matrix and the
    right-hand side is a single sparse mat-vec, so the cost is dominated by the
    ``4^N`` state vector rather than by the (very sparse) operator.

    Parameters
    ----------
    N
        Number of two-level units; ``4^N`` grows fast, hence ``max_full_N``.
    t_grid
        Output times, starting at ``t = 0``.
    Gamma0, alpha
        Bare rate and reinforcement strength.
    initial
        One of the names accepted by `initial_density_matrix`, or an explicit
        density matrix.
    """
    if N > max_full_N:
        raise ValueError(
            f"N = {N} needs a {4 ** N}-dimensional Liouvillian; "
            f"raise max_full_N deliberately or use dicke_master"
        )
    t_grid = np.asarray(t_grid, dtype=float)
    D = 1 << N
    rho0 = (
        initial_density_matrix(N, initial)
        if isinstance(initial, str)
        else np.asarray(initial, dtype=float)
    )
    if rho0.shape != (D, D):
        raise ValueError(f"initial density matrix must have shape {(D, D)}")

    Lsup = liouvillian(N, Gamma0, alpha)

    def rhs(_t: float, y: np.ndarray) -> np.ndarray:
        return Lsup @ y

    sol = solve_ivp(
        rhs,
        (0.0, float(t_grid[-1])),
        rho0.reshape(-1),
        method="DOP853",
        t_eval=t_grid,
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")

    rho = sol.y.reshape(D, D, -1)
    pops = np.einsum("sst->st", rho)
    occ = occupation_numbers(N)                       # (D, N)
    n = occ.T.astype(float) @ pops                    # (N, T)
    offdiag = np.abs(rho).sum(axis=(0, 1)) - np.abs(pops).sum(axis=0)
    return LindbladRun(
        t=sol.t,
        n=n,
        f=n.mean(axis=0),
        populations=pops,
        coherence=offdiag,
        trace=pops.sum(axis=0),
        N=N,
        Gamma0=Gamma0,
        alpha=alpha,
    )


def populations_decouple(N: int, Gamma0: float = 1.0, alpha: float = 0.0) -> bool:
    """Algebraic check that no coherence ever feeds a population.

    Returns True iff every column of the Liouvillian belonging to an off-diagonal
    element ``rho_{s s'}`` (``s != s'``) has zero entries in the rows belonging
    to diagonal elements ``rho_{u u}``.  That is the exact statement behind the
    "coherent and mixed initial states give the same <n_i>(t)" test.
    """
    D = 1 << N
    Lsup = liouvillian(N, Gamma0, alpha).tocoo()
    idx = np.arange(D * D)
    is_diag = (idx // D) == (idx % D)
    bad = is_diag[Lsup.row] & ~is_diag[Lsup.col] & (Lsup.data != 0.0)
    return not bool(bad.any())


# ---------------------------------------------------------------------------
# Mean field and its closure error
# ---------------------------------------------------------------------------
def mean_field(
    t_grid: np.ndarray,
    *,
    Gamma0: float = 1.0,
    alpha: float = 0.0,
    f0: float = 0.0,
    rtol: float = 1e-12,
    atol: float = 1e-14,
) -> np.ndarray:
    """Mean-field absorption curve ``df/dt = (1 - f) Gamma_0 e^{alpha f}``.

    This is the ``N -> inf`` closure of the master equation: it replaces
    ``<(1 - fhat) e^{alpha fhat}>`` by ``(1 - <fhat>) e^{alpha <fhat>}``, which
    discards the ``O(1/N)`` variance of ``fhat``.
    """
    t_grid = np.asarray(t_grid, dtype=float)
    sol = solve_ivp(
        lambda _t, y: [(1.0 - y[0]) * Gamma0 * math.exp(alpha * y[0])],
        (0.0, float(t_grid[-1])),
        [float(f0)],
        method="DOP853",
        t_eval=t_grid,
        rtol=rtol,
        atol=atol,
    )
    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")
    return sol.y[0]


@dataclass
class ClosureScaling:
    """Result of `closure_error_scaling`."""

    N: np.ndarray
    error: np.ndarray
    """``max_t |<fhat>(t) - f_MF(t)|`` for each ``N``."""
    slope: float
    """Least-squares slope of ``log(error)`` against ``log(N)``."""
    intercept: float
    engine: str
    """``"master"`` (full Liouvillian) or ``"dicke"`` (birth chain)."""

    @property
    def prefactor(self) -> float:
        """``exp(intercept)``: the coefficient of ``N^slope``."""
        return math.exp(self.intercept)


def closure_error_scaling(
    N_values: Sequence[int],
    t_grid: np.ndarray,
    *,
    Gamma0: float = 1.0,
    alpha: float = 1.0,
    engine: Literal["master", "dicke"] = "master",
    **kwargs,
) -> ClosureScaling:
    """Measure how the mean-field closure error decays with ``N``.

    For each ``N`` the exact ``<fhat>(t)`` is computed (from the full master
    equation, or from the permutation-symmetric birth chain for large ``N``) and
    compared with `mean_field` on the same grid; the maximum absolute difference
    is regressed against ``N`` on a log-log scale.  A slope of ``-1`` is the
    signature of a genuine ``O(1/N)`` closure error.

    ``engine`` selects which exact solver provides ``<fhat>``: ``"master"``
    builds the full ``4^N`` Liouvillian (so ``N <= 8``), ``"dicke"`` uses the
    permutation-symmetric birth chain (so ``N`` can reach ``10^4``).  Extra
    keyword arguments are forwarded to the chosen solver, e.g.
    ``method="BDF"`` for the stiff large-``N`` chains.
    """
    t_grid = np.asarray(t_grid, dtype=float)
    f_mf = mean_field(t_grid, Gamma0=Gamma0, alpha=alpha)
    errs = []
    for N in N_values:
        if engine == "master":
            f_exact = solve_master(
                N, t_grid, Gamma0=Gamma0, alpha=alpha, **kwargs
            ).f
        else:
            f_exact = dicke_master(N, t_grid, Gamma0=Gamma0, alpha=alpha, **kwargs).f
        errs.append(float(np.max(np.abs(f_exact - f_mf))))
    N_arr = np.asarray(N_values, dtype=float)
    err_arr = np.asarray(errs)
    slope, intercept = np.polyfit(np.log(N_arr), np.log(err_arr), 1)
    return ClosureScaling(
        N=N_arr, error=err_arr, slope=float(slope), intercept=float(intercept),
        engine=engine,
    )


# ---------------------------------------------------------------------------
# Permutation-symmetric (Dicke) reduction
# ---------------------------------------------------------------------------
@dataclass
class DickeRun:
    """Solution of the ``(N+1)``-state birth chain."""

    t: np.ndarray
    p: np.ndarray
    """``(N+1, T)`` probability of having exactly ``k`` converted units."""
    f: np.ndarray
    """``(T,)`` mean converted fraction ``<k>/N``."""
    var_f: np.ndarray
    """``(T,)`` variance of ``k/N``; it is the ``O(1/N)`` term the closure drops."""
    N: int
    Gamma0: float
    alpha: float


def dicke_rates(N: int, Gamma0: float = 1.0, alpha: float = 0.0) -> np.ndarray:
    """Birth rates ``r_k = (N-k) Gamma_0 exp(alpha k/(N-1))`` for ``k = 0..N``.

    These are exactly the rates the full master equation induces on a
    permutation-symmetric state: ``N-k`` units are still able to jump and each
    sees ``k`` converted neighbours out of ``N-1``.
    """
    k = np.arange(N + 1, dtype=float)
    return (N - k) * Gamma0 * np.exp(alpha * _environment_fraction(k, N))


def dicke_master(
    N: int,
    t_grid: np.ndarray,
    *,
    Gamma0: float = 1.0,
    alpha: float = 0.0,
    k0: int = 0,
    rtol: float = RTOL,
    atol: float = ATOL,
    method: str = "DOP853",
) -> DickeRun:
    """Integrate the exact permutation-symmetric birth chain.

        dp_k/dt = r_{k-1} p_{k-1} - r_k p_k ,   r_k = (N-k) Gamma_0 e^{alpha k/(N-1)} .

    The chain is exact for any permutation-symmetric initial state (in
    particular the physical ``k = 0`` state), and its cost is ``O(N)`` per
    right-hand side rather than ``O(4^N)``, which is what lets the ``O(1/N)``
    closure error be tracked up to ``N ~ 10^4``.

    Stiffness.  The fastest rate is ``~ N Gamma_0 e^{alpha}`` while the
    interesting dynamics lasts ``O(1/Gamma_0)``, so the explicit default
    ``DOP853`` needs ``O(N)`` steps and becomes the bottleneck beyond
    ``N ~ 10^3``.  Passing ``method="BDF"`` (or ``"Radau"``) hands the solver
    the *exact* sparse bidiagonal Jacobian and removes the step-size
    restriction; that is the recommended setting for the large-``N`` runs.
    """
    t_grid = np.asarray(t_grid, dtype=float)
    r = dicke_rates(N, Gamma0, alpha)
    # Lower-bidiagonal generator: gain from k-1, loss from k.
    gen = sps.diags([r[:-1], -r], offsets=[-1, 0], format="csr")

    def rhs(_t: float, p: np.ndarray) -> np.ndarray:
        return gen @ p

    p0 = np.zeros(N + 1)
    p0[k0] = 1.0
    extra = {"jac": gen} if method in ("BDF", "Radau") else {}
    sol = solve_ivp(
        rhs, (0.0, float(t_grid[-1])), p0, method=method, t_eval=t_grid,
        rtol=rtol, atol=atol, **extra,
    )
    if not sol.success:
        raise RuntimeError(f"solve_ivp failed: {sol.message}")
    k = np.arange(N + 1, dtype=float)
    mean_k = k @ sol.y
    mean_k2 = (k ** 2) @ sol.y
    return DickeRun(
        t=sol.t,
        p=sol.y,
        f=mean_k / N,
        var_f=(mean_k2 - mean_k ** 2) / N ** 2,
        N=N,
        Gamma0=Gamma0,
        alpha=alpha,
    )


# ---------------------------------------------------------------------------
# Single-unit closed form
# ---------------------------------------------------------------------------
def single_unit_solution(t: np.ndarray, Gamma0: float = 1.0) -> np.ndarray:
    """Exact ``rho_AA(t) = 1 - e^{-Gamma_0 t}`` for one unit started in ``|I>``.

    With ``N = 1`` there is no environment, ``L = sqrt(Gamma_0) |A><I|``, and
    the master equation reduces to ``d rho_II/dt = -Gamma_0 rho_II``.
    """
    return 1.0 - np.exp(-Gamma0 * np.asarray(t, dtype=float))
