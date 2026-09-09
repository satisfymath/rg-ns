"""Hedgehog textures of the S^3 -> S^3 sigma model with a Skyrme term.

Physical setting
----------------
The order parameter of the localized defect is a unit four-vector
``n^A(x)``, ``n^A n^A = 1``, i.e. a map ``R^3 (compactified to S^3) -> S^3``.
Maps are labelled by their degree ``B in pi_3(S^3) = Z``.  For the hedgehog
ansatz

    n^4 = cos F(r),      n^a = sin F(r) xhat^a   (a = 1, 2, 3),

the static energy of the two-derivative (sigma) term plus the four-derivative
(Skyrme) term is

    E = 4 pi int r^2 dr [ (F_*^2 / 2) (F'^2 + 2 sin^2 F / r^2)
                          + kappa_s (2 F'^2 sin^2 F / r^2 + sin^4 F / r^4) ].

``F_*`` has mass dimension 1 (a decay constant), ``kappa_s`` is dimensionless
in the sense that ``sqrt(kappa_s)/F_*`` is the only length in the problem.
Rescaling ``r = (sqrt(kappa_s)/F_*) x`` factorises that length out completely,

    E = F_* sqrt(kappa_s) * Etilde,

    Etilde = 4 pi int x^2 dx [ (1/2) (F'^2 + 2 sin^2 F / x^2)
                               + (sin^2 F / x^2) (2 F'^2 + sin^2 F / x^2) ],

so ``Etilde`` is a pure number attached to the topological sector.  Everything
in this module works with ``Etilde`` and its two pieces

    E2 = 4 pi int x^2 dx (1/2) (F'^2 + 2 sin^2 F / x^2)          (two-derivative)
    E4 = 4 pi int x^2 dx (sin^2 F / x^2) (2 F'^2 + sin^2 F / x^2) (four-derivative)

Why the module exists
---------------------
Three numbers are needed by the paper and each is *computed* here rather than
quoted:

1. the variational (trial) energy ``6 pi^2 (R + 1/R)``, minimised by ``12 pi^2``;
2. the Bogomolny/Faddeev bound ``6 sqrt(2) pi^2`` per unit degree;
3. the true ``B = 1`` energy from the Euler-Lagrange boundary-value problem.

The Euler-Lagrange equation is *derived* in `euler_lagrange_residual` and the
derivation is verified symbolically by `check_euler_lagrange_symbolic`.
"""
from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.integrate import quad, solve_bvp

# --- closed-form reference values -------------------------------------------
# All three follow from analytic arguments carried out in the docstrings of the
# functions that expose them; they are assembled from math constants only.
TRIAL_COEFF = 6.0 * math.pi ** 2          # Etilde_trial(R) = TRIAL_COEFF (R + 1/R)
TRIAL_MIN = 2.0 * TRIAL_COEFF             # its minimum, at R = 1
BOGOMOLNY = 6.0 * math.sqrt(2.0) * math.pi ** 2   # per unit degree


# ---------------------------------------------------------------------------
# Energy densities
# ---------------------------------------------------------------------------
def energy_densities(
    x: np.ndarray, F: np.ndarray, Fp: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Radial integrands of ``E2`` and ``E4`` (the ``4 pi`` is *included*).

    Parameters
    ----------
    x, F, Fp
        Rescaled radius, profile and ``dF/dx``, broadcastable to a common shape.

    Returns
    -------
    (e2, e4)
        Densities such that ``E2 = int e2 dx`` and ``E4 = int e4 dx``.
    """
    x = np.asarray(x, dtype=float)
    s2 = np.sin(F) ** 2
    e2 = 4.0 * np.pi * (0.5 * x ** 2 * Fp ** 2 + s2)
    e4 = 4.0 * np.pi * (2.0 * s2 * Fp ** 2 + s2 ** 2 / x ** 2)
    return e2, e4


def trial_profile(x: np.ndarray | float, R: float = 1.0) -> np.ndarray:
    """Conformal (``instanton-like``) trial profile ``F = 2 arctan(R/x)``.

    It interpolates between ``F(0) = pi`` and ``F(inf) = 0`` and has the special
    property ``F'^2 = sin^2 F / x^2`` pointwise, which is why its energy is
    exactly quadratic in the scale ``R`` (see `trial_energy`).
    """
    return 2.0 * np.arctan(R / np.asarray(x, dtype=float))


def trial_profile_derivative(x: np.ndarray | float, R: float = 1.0) -> np.ndarray:
    """``dF/dx`` of `trial_profile`, ``-2R/(x^2 + R^2)``."""
    x = np.asarray(x, dtype=float)
    return -2.0 * R / (x ** 2 + R ** 2)


def trial_energy(R: float, quadrature: bool = True) -> float:
    """Energy of `trial_profile`; equals ``6 pi^2 (R + 1/R)`` exactly.

    Derivation.  For ``F = 2 arctan(R/x)`` one has
    ``F' = -2R/(x^2+R^2)`` and ``sin F = 2 R x/(x^2+R^2)``, hence

        F'^2 = sin^2 F / x^2 = 4 R^2 / (x^2 + R^2)^2 =: G(x).

    Therefore ``E2 = 4 pi (3/2) int x^2 G dx = 6 pi^2 R`` using
    ``int_0^inf x^2/(x^2+R^2)^2 dx = pi/(4R)``, and
    ``E4 = 4 pi * 3 int x^2 G^2 dx = 6 pi^2 / R`` using
    ``int_0^inf x^2/(x^2+R^2)^4 dx = pi/(32 R^5)``.

    Parameters
    ----------
    R
        Scale of the trial profile (units of ``sqrt(kappa_s)/F_*``).
    quadrature
        If True (default) the value is obtained by numerical quadrature of the
        energy functional, so the closed form is a *prediction* to be checked.
        If False the closed form is returned directly.
    """
    if R <= 0.0:
        raise ValueError("trial scale R must be positive")
    if not quadrature:
        return TRIAL_COEFF * (R + 1.0 / R)

    def integrand(x: float) -> float:
        e2, e4 = energy_densities(x, trial_profile(x, R), trial_profile_derivative(x, R))
        return float(e2 + e4)

    # The density peaks near x ~ R and falls off as x^-4, so split the range at
    # R and use quad's infinite-interval transformation for the tail.
    inner, _ = quad(integrand, 0.0, R, limit=200, epsabs=1e-12, epsrel=1e-12)
    outer, _ = quad(integrand, R, np.inf, limit=200, epsabs=1e-12, epsrel=1e-12)
    return inner + outer


def bogomolny_bound() -> float:
    """Topological lower bound ``6 sqrt(2) pi^2`` on ``Etilde`` per unit degree.

    Let ``sigma_1 = |F'|`` and ``sigma_2 = sigma_3 = |sin F| / x`` be the
    singular values of ``dn`` in the hedgehog sector.  Then

        e2 density / (4 pi x^2) = (1/2) sum_i sigma_i^2,
        e4 density / (4 pi x^2) = sum_{i<j} sigma_i^2 sigma_j^2,
        degree density          = (2/pi) x^2 sigma_1 sigma_2 sigma_3 .

    AM-GM on each group gives, with ``u = sigma_1 sigma_2 sigma_3``,

        (1/2) sum sigma_i^2 + sum_{i<j} sigma_i^2 sigma_j^2
              >= (3/2) u^{2/3} + 3 u^{4/3} >= 3 sqrt(2) u ,

    the last step by minimising ``(3/2) u^{-1/3} + 3 u^{1/3}`` at ``u = 2^{-3/2}``.
    Integrating, ``Etilde >= 12 sqrt(2) pi * (pi/2) B = 6 sqrt(2) pi^2 B``.
    """
    return BOGOMOLNY


def degree(F: np.ndarray, x: np.ndarray | None = None) -> float:
    """Topological degree ``B`` of a hedgehog profile.

    The degree density integrates to a total derivative,

        B = -(1/pi) [ F - sin F cos F ]_{x_min}^{x_max},

    so ``B`` depends on the profile only through its boundary values.  ``x`` is
    accepted for signature symmetry with the rest of the module and is used
    only to orient the endpoints.
    """
    F = np.asarray(F, dtype=float)
    if x is not None:
        order = np.argsort(np.asarray(x, dtype=float))
        F = F[order]

    def g(u: float) -> float:
        return u - math.sin(u) * math.cos(u)

    return (g(float(F[0])) - g(float(F[-1]))) / math.pi


def degree_by_quadrature(F: np.ndarray, x: np.ndarray) -> float:
    """Same degree, obtained by integrating the density ``-(2/pi) F' sin^2 F``.

    Unlike `degree` this is sensitive to the whole profile and therefore acts
    as an independent check that the numerical solution is a genuine
    single-covering map.
    """
    x = np.asarray(x, dtype=float)
    F = np.asarray(F, dtype=float)
    Fp = np.gradient(F, x, edge_order=2)
    return float(-2.0 / math.pi * np.trapezoid(Fp * np.sin(F) ** 2, x))


# ---------------------------------------------------------------------------
# Euler-Lagrange equation
# ---------------------------------------------------------------------------
def euler_lagrange_residual(
    x: np.ndarray, F: np.ndarray, Fp: np.ndarray, Fpp: np.ndarray
) -> np.ndarray:
    """Residual ``d/dx(de/dF') - de/dF`` of the rescaled energy density.

    With ``e = (1/2) x^2 F'^2 + sin^2 F + 2 sin^2 F F'^2 + sin^4 F / x^2``
    (the bracket of ``Etilde`` times ``x^2``, with the ``4 pi`` dropped),

        de/dF'      = x^2 F' + 4 sin^2 F F' ,
        de/dF       = sin 2F + 2 sin 2F F'^2 + 2 sin^2 F sin 2F / x^2 ,

    hence the Euler-Lagrange equation is

        (x^2 + 4 sin^2 F) F'' + 2 x F' + 2 sin 2F F'^2
            - sin 2F - 2 sin^2 F sin 2F / x^2 = 0 .

    `check_euler_lagrange_symbolic` verifies this by symbolic differentiation.
    """
    s = np.sin(F)
    s2f = np.sin(2.0 * F)
    return (
        (x ** 2 + 4.0 * s ** 2) * Fpp
        + 2.0 * x * Fp
        + 2.0 * s2f * Fp ** 2
        - s2f
        - 2.0 * s ** 2 * s2f / x ** 2
    )


def _rhs(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """First-order form of the Euler-Lagrange equation, ``y = (F, F')``."""
    F, Fp = y
    s = np.sin(F)
    s2f = np.sin(2.0 * F)
    Fpp = (s2f * (1.0 + 2.0 * s ** 2 / x ** 2 - 2.0 * Fp ** 2) - 2.0 * x * Fp) / (
        x ** 2 + 4.0 * s ** 2
    )
    return np.vstack((Fp, Fpp))


def check_euler_lagrange_symbolic() -> bool:
    """Verify `euler_lagrange_residual` against sympy's variational derivative.

    Returns True or raises ``AssertionError``.  This is the guarantee that the
    ODE actually solved is the one belonging to the energy functional coded in
    `energy_densities`, rather than a form copied from the literature.
    """
    import sympy as sp

    x = sp.symbols("x", positive=True)
    F = sp.Function("F")(x)
    Fp = sp.Derivative(F, x)

    # e = (energy integrand of Etilde) / (4 pi), i.e. x^2 * [ ... ].
    e = (
        sp.Rational(1, 2) * x ** 2 * sp.diff(F, x) ** 2
        + sp.sin(F) ** 2
        + 2 * sp.sin(F) ** 2 * sp.diff(F, x) ** 2
        + sp.sin(F) ** 4 / x ** 2
    )
    el = sp.diff(sp.diff(e, Fp), x) - sp.diff(e, F)

    s2f = sp.sin(2 * F)
    coded = (
        (x ** 2 + 4 * sp.sin(F) ** 2) * sp.diff(F, x, 2)
        + 2 * x * sp.diff(F, x)
        + 2 * s2f * sp.diff(F, x) ** 2
        - s2f
        - 2 * sp.sin(F) ** 2 * s2f / x ** 2
    )
    residual = sp.simplify(sp.expand_trig(sp.expand(el - coded)))
    assert residual == 0, f"coded ODE is not the Euler-Lagrange equation: {residual}"
    return True


# ---------------------------------------------------------------------------
# Boundary-value solution
# ---------------------------------------------------------------------------
@dataclass
class Hedgehog:
    """Solution of the ``B = 1`` hedgehog boundary-value problem."""

    x: np.ndarray
    """Radial mesh (rescaled units ``sqrt(kappa_s)/F_*``)."""
    F: np.ndarray
    """Profile ``F(x)``, monotone from ``pi`` to ``0``."""
    Fp: np.ndarray
    """``dF/dx``."""
    E2: float
    """Two-derivative energy."""
    E4: float
    """Four-derivative (Skyrme) energy."""
    Etilde: float
    """Total ``E2 + E4``."""
    B: float
    """Topological degree from the boundary values."""
    B_quadrature: float
    """Topological degree from the density integral (independent check)."""
    slope: float
    """``s`` in the regular series ``F ~ pi - s x`` at the origin."""
    tail: float
    """``C`` in the asymptotic tail ``F ~ C / x^2``."""
    virial: float
    """``(E2 - E4)/(E2 + E4)``; zero at a genuine stationary point (Derrick)."""
    sol: Callable[[np.ndarray], np.ndarray]
    """Dense-output callable of ``solve_bvp`` returning ``(F, F')``."""

    @property
    def bound_ratio(self) -> float:
        """``Etilde / (B * Bogomolny bound)``."""
        return self.Etilde / (self.B * BOGOMOLNY)

    @property
    def trial_ratio(self) -> float:
        """``Etilde`` divided by the best conformal trial energy ``12 pi^2``."""
        return self.Etilde / TRIAL_MIN


def tail_energies(C: float, x_max: float) -> tuple[float, float]:
    """Energy stored in the analytic tail ``F ~ C/x^2`` beyond ``x_max``.

    Substituting ``F = C/x^2`` (so ``F' = -2C/x^3`` and ``sin F ~ F``) in
    `energy_densities` gives ``e2 -> 12 pi C^2 x^-4`` and
    ``e4 -> 36 pi C^4 x^-10``, hence

        E2_tail = 4 pi C^2 / x_max^3 ,      E4_tail = 4 pi C^4 / x_max^9 .

    The second is utterly negligible; it is kept so that both integrals are
    treated on the same footing and the virial identity is not biased.
    """
    return 4.0 * np.pi * C ** 2 / x_max ** 3, 4.0 * np.pi * C ** 4 / x_max ** 9


def solve_hedgehog(
    x_min: float = 1.0e-4,
    x_max: float = 40.0,
    n_nodes: int = 1200,
    R_guess: float = 1.0,
    tol: float = 1.0e-8,
    max_nodes: int = 200_000,
) -> Hedgehog:
    """Solve the ``B = 1`` Euler-Lagrange problem with ``scipy.solve_bvp``.

    Boundary conditions.  Regularity at the origin forces the series
    ``F = pi - s x + O(x^3)``, so ``F(x_min) = pi`` up to an error ``O(x_min)``;
    the fitted ``s`` is returned in `Hedgehog.slope` so the series can be
    checked a posteriori.  (The induced energy error is ``O(x_min^4)``, since
    the boundary term ``(x^2 + 4 sin^2 F) F' dF`` vanishes as ``x^3`` there.)

    At large ``x`` the linearised equation is ``F'' + 2F'/x - 2F/x^2 = 0`` with
    decaying solution ``F ~ C/x^2`` -- the massless dipole tail.  Imposing
    ``F(x_max) = 0`` would amputate it and unbalance the virial identity at the
    1e-4 level, so the *Robin* condition

        x_max F'(x_max) + 2 F(x_max) = 0

    is used instead: it is exactly satisfied by ``C/x^2`` for any ``C``, leaves
    ``C`` to be determined by the solution, and lets the remaining energy be
    added in closed form by `tail_energies`.

    Parameters
    ----------
    x_min, x_max
        Radial window.  Must satisfy ``0 < x_min << 1 << x_max``.
    n_nodes
        Size of the initial (logarithmic) mesh.
    R_guess
        Scale of the `trial_profile` used as the initial guess.
    tol, max_nodes
        Passed through to ``solve_bvp``.

    Returns
    -------
    Hedgehog
    """
    if not 0.0 < x_min < x_max:
        raise ValueError("require 0 < x_min < x_max")

    x = np.geomspace(x_min, x_max, n_nodes)
    y0 = np.vstack((trial_profile(x, R_guess), trial_profile_derivative(x, R_guess)))

    def bc(ya: np.ndarray, yb: np.ndarray) -> np.ndarray:
        return np.array([ya[0] - np.pi, x_max * yb[1] + 2.0 * yb[0]])

    sol = solve_bvp(_rhs, bc, x, y0, tol=tol, max_nodes=max_nodes, verbose=0)
    if not sol.success:
        raise RuntimeError(f"solve_bvp failed: {sol.message}")

    def _e2(xx: float) -> float:
        F, Fp = sol.sol(xx)
        return float(energy_densities(xx, F, Fp)[0])

    def _e4(xx: float) -> float:
        F, Fp = sol.sol(xx)
        return float(energy_densities(xx, F, Fp)[1])

    # Break the quadrature at x = 1, where the densities turn over.
    def _integrate(fn: Callable[[float], float]) -> float:
        a, _ = quad(fn, x_min, 1.0, limit=400, epsabs=1e-13, epsrel=1e-13)
        b, _ = quad(fn, 1.0, x_max, limit=400, epsabs=1e-13, epsrel=1e-13)
        return a + b

    C = float(sol.sol(x_max)[0]) * x_max ** 2
    t2, t4 = tail_energies(C, x_max)
    E2 = _integrate(_e2) + t2
    E4 = _integrate(_e4) + t4

    xf = np.geomspace(x_min, x_max, 20_000)
    Ff, Fpf = sol.sol(xf)

    # F ~ pi - s x near the origin: read s off the innermost decade.
    inner = xf < 10.0 * x_min
    slope = float(np.mean((np.pi - Ff[inner]) / xf[inner]))

    B = degree(Ff, xf)
    return Hedgehog(
        x=xf,
        F=Ff,
        Fp=Fpf,
        E2=E2,
        E4=E4,
        Etilde=E2 + E4,
        B=B,
        B_quadrature=degree_by_quadrature(Ff, xf),
        slope=slope,
        tail=C,
        virial=(E2 - E4) / (E2 + E4),
        sol=sol.sol,
    )
