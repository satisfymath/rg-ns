"""Behaviour of the precursor along a flow line that is being compressed.

The covariant continuity equation for the precursor, along a flow line with
proper time tau and expansion scalar Theta = nabla_mu u^mu, is

    D rho_I / D tau + Theta rho_I = - Gamma rho_I ,

so that

    d ln rho_I / d tau = -(Theta + Gamma)                                 (1)

and therefore, exactly and with no approximation,

    rho_I(tau) = rho_I(tau_0) exp[ - int_{tau_0}^{tau} (Theta + Gamma) ds ].  (2)

Equation (2) is the whole content of the local problem: whether the precursor
density blows up, tends to a finite value, or vanishes is decided by the
*divergence structure of a single integral*.  In particular the conversion
term enters only through its integral, which is why a bounded rate cannot
regularize a compression whose integral diverges: it can shift rho_I by a
bounded factor and nothing more.

This module contains the exact statements and the numerical checks of them.
It deliberately contains no cosmology: Theta is supplied as a function.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import numpy as np
from scipy.integrate import quad, solve_ivp


# --------------------------------------------------------------------------- #
# Exact solution of the local equation
# --------------------------------------------------------------------------- #
def log_density_change(theta: Callable[[float], float],
                       gamma: Callable[[float], float],
                       t0: float, t: float, **kw) -> float:
    """Return ln[rho_I(t)/rho_I(t0)] = -int_{t0}^{t} (Theta + Gamma) ds."""
    # points= tells the quadrature where the integrand is singular; without it
    # a 1/(T-t) integrand triggers a bad-behaviour warning near the endpoint.
    val, _ = quad(lambda s: theta(s) + gamma(s), t0, t,
                  limit=kw.pop("limit", 400), points=kw.pop("points", None),
                  **kw)
    return -val


def density_ratio(theta, gamma, t0: float, t: float, **kw) -> float:
    return float(np.exp(log_density_change(theta, gamma, t0, t, **kw)))


@dataclass(frozen=True)
class CollapseModel:
    """A self-similar collapse with an optional compression-driven rate.

    Theta(t)  = -c/(T - t)                 (compression, c > 0)
    Gamma(t)  =  g/(T - t) + Gamma_b(t)    (collapse channel plus a bounded part)

    Only the combination c - g controls the leading behaviour: from (2),

        rho_I(t) ~ (T - t)^{-(c - g)} x  [bounded factor]                 (3)

    so the precursor diverges for g < c, tends to a finite non-zero limit for
    g = c, and vanishes for g > c.  The bounded part of the rate contributes a
    factor exp(-int Gamma_b), which is bounded away from zero and infinity
    whenever Gamma_b is integrable on [t0, T]; it therefore cannot change which
    of the three cases occurs.
    """

    c: float
    g: float = 0.0
    T: float = 1.0
    gamma_bounded: float = 0.0

    def theta(self, t: float) -> float:
        return -self.c / (self.T - t)

    def gamma(self, t: float) -> float:
        return self.g / (self.T - t) + self.gamma_bounded

    def exponent(self) -> float:
        """The exponent p in rho_I ~ (T-t)^{-p}."""
        return self.c - self.g

    def rho_exact(self, t: float, t0: float = 0.0, rho0: float = 1.0) -> float:
        """Closed form of (2) for this model."""
        s0, s = self.T - t0, self.T - t
        power = (s / s0) ** (-(self.c - self.g))
        return rho0 * power * np.exp(-self.gamma_bounded * (t - t0))

    def rho_numeric(self, t: float, t0: float = 0.0, rho0: float = 1.0) -> float:
        return rho0 * density_ratio(self.theta, self.gamma, t0, t)


# --------------------------------------------------------------------------- #
# The obstruction: a bounded rate changes nothing qualitative
# --------------------------------------------------------------------------- #
def bounded_rate_factor(gamma_bound: float, t0: float, T: float) -> float:
    """The most a rate bounded by ``gamma_bound`` can suppress rho_I.

    From (2) the conversion contributes exp(-int Gamma), and if
    0 <= Gamma <= G on [t0, T] then that factor lies in
    [exp(-G (T - t0)), 1].  It is bounded below by a positive number, so it
    cannot convert a divergent power into a finite limit.
    """
    return float(np.exp(-gamma_bound * (T - t0)))


def converted_fraction_singular(g: float, T: float, t: float,
                                t0: float = 0.0, f0: float = 0.0) -> float:
    """Exact solution of df/dt = (1-f) g/(T-t).

    Integrating, 1 - f = (1 - f0) [(T - t)/(T - t0)]^{g}, so the fraction
    reaches one exactly at t = T for every g > 0: a rate that diverges like
    1/(T-t) absorbs the population completely, and does so in finite time.
    """
    return 1.0 - (1.0 - f0) * ((T - t) / (T - t0)) ** g


def cumulative_hazard(gamma: Callable[[float], float], t0: float,
                      t: float, **kw) -> float:
    """int_{t0}^{t} Gamma ds, the natural time variable for the jump process."""
    val, _ = quad(gamma, t0, t, limit=kw.pop("limit", 400), **kw)
    return float(val)


# --------------------------------------------------------------------------- #
# The full local sector, not just the precursor
# --------------------------------------------------------------------------- #
@dataclass
class LocalSector:
    """All three densities along one collapsing flow line.

        d rho_I/dt = -(Theta + Gamma) rho_I
        d rho_D/dt = -Theta rho_D + b Gamma rho_I
        d V    /dt = (1 - b) Gamma rho_I

    with Theta = -c/(T-t) and Gamma = g/(T-t) + Gamma_b.  The vacuum has no
    Theta term because it is not diluted by the flow, which is exactly why its
    regularity condition turns out to be *stronger* than the precursor's: the
    source it integrates carries the full divergence of Gamma rho_I with
    nothing to compensate it.
    """

    c: float
    g: float
    b: float = 0.25
    T: float = 1.0
    gamma_bounded: float = 0.0

    def rhs(self, t, y):
        rI, rD, V = y
        s = max(self.T - t, 1e-300)
        Theta = -self.c / s
        Gam = self.g / s + self.gamma_bounded
        return [-(Theta + Gam) * rI, -Theta * rD + self.b * Gam * rI,
                (1.0 - self.b) * Gam * rI]

    def integrate(self, t_end: float, y0=(1.0, 0.0, 0.0), rtol=1e-11,
                  atol=1e-14, n_out: int = 400):
        t_eval = np.linspace(0.0, t_end, n_out)
        sol = solve_ivp(self.rhs, (0.0, t_end), list(y0), method="Radau",
                        rtol=rtol, atol=atol, t_eval=t_eval)
        if not sol.success:                                    # pragma: no cover
            raise RuntimeError(sol.message)
        return sol

    # --- the exponents, read off analytically -----------------------------
    @property
    def precursor_exponent(self) -> float:
        """rho_I ~ (T-t)^{-(c-g)}."""
        return self.c - self.g

    @property
    def vacuum_source_exponent(self) -> float:
        """dV/dt ~ (T-t)^{g-c-1}; the integral converges iff this exceeds -1."""
        return self.g - self.c - 1.0

    @property
    def column_exponent(self) -> float:
        """rho_I times the proper width ~ (T-t)^{g} for a planar collapse."""
        return self.g

    def regularity(self) -> dict[str, bool]:
        """Which quantities stay finite as t -> T."""
        return {
            "rho_I_finite": self.g >= self.c,
            "rho_I_vanishes": self.g > self.c,
            "V_finite": self.g > self.c,          # strict: g = c diverges as log
            "column_finite": self.g >= 0.0,
            "source_integrable": self.vacuum_source_exponent > -1.0,
        }


# --------------------------------------------------------------------------- #
# Compression-driven rate
# --------------------------------------------------------------------------- #
def collapse_rate_coefficient(kappa: float, c: float) -> float:
    """The exponent ``g`` produced by Gamma_collapse = kappa [-Theta]_+.

    With Theta = -c/(T-t) the positive part is c/(T-t), so
    Gamma_collapse = kappa c/(T-t) and g = kappa c.  The regularity condition
    g > c therefore reduces to the dimensionless statement kappa > 1,
    independently of c: the conversion must remove a larger fraction of the
    precursor per unit time than the compression adds.
    """
    return kappa * c


def zeldovich_expansion_exponent() -> float:
    """c = 1 for a generic Zel'dovich pancake.

    With x = q + D(t) psi(q) the Jacobian is J = 1 + D psi', which crosses zero
    linearly in (T - t) whenever dD/dt does not vanish there.  Since
    Theta = d ln J/dt, this gives Theta ~ -1/(T-t), i.e. c = 1.  Higher c
    requires a degenerate (non-generic) crossing.
    """
    return 1.0


def regularity_conditions(kappa: float, b: float, c: float = 1.0) -> dict:
    """Full regularity verdict for a compression-driven rate at a caustic."""
    g = collapse_rate_coefficient(kappa, c)
    return {
        "g": g,
        "precursor_finite": g >= c,
        "precursor_vanishes": g > c,
        "vacuum_finite": g > c,
        "defects_finite": b == 0.0,
        "stress_tensor_regular": (g > c) and (b == 0.0),
        "kappa_threshold": 1.0,
    }


# --------------------------------------------------------------------------- #
# The finite-population chain when the rate is unbounded
# --------------------------------------------------------------------------- #
def binomial_law_in_hazard_time(N: int, hazard: float, rng=None,
                                size: int = 1) -> np.ndarray:
    """Exact law of the converted count for a state-independent rate.

    The deterministic-limit theorem of the manuscript assumes a bounded rate,
    which fails for Gamma ~ g/(T-t).  Nothing is lost, because a time change
    removes the singularity exactly.  Let

        Lambda(t) = int_{t0}^{t} Gamma(s) ds

    be the cumulative hazard.  If Gamma does not depend on the state, then in
    Lambda-time every unit carries an independent unit-rate exponential clock,
    so the number converted is exactly binomial:

        K ~ Binomial(N, 1 - exp(-Lambda)) ,

    with no approximation and for every Lambda, including Lambda -> infinity at
    the singularity.  Consequently E[f_N] = 1 - exp(-Lambda) is exactly the
    deterministic solution, and

        sqrt(N) * std(f_N) = sqrt(p (1 - p)),   p = 1 - exp(-Lambda),

    so the N^{-1/2} scaling holds uniformly, with no boundary layer near T.
    The mean-field limit is therefore not merely recovered: it is exact in the
    mean at every finite N.
    """
    rng = np.random.default_rng() if rng is None else rng
    p = 1.0 - np.exp(-hazard)
    return rng.binomial(N, p, size=size) / N


def residual_relative_fluctuation(N: int, hazard: float) -> float:
    """Relative standard deviation of 1 - f, and hence of the precursor.

    The deterministic limit describes the converted fraction, whose relative
    fluctuation vanishes as p -> 1.  It does *not* describe the residual
    density: rho_I is proportional to 1 - f, whose relative standard deviation
    is sqrt(p / (N (1-p))) and diverges at the caustic.  So there is a boundary
    layer after all, in exactly the quantity the regularity question is about.
    """
    q = np.exp(-hazard)
    p = 1.0 - q
    return float(np.sqrt(p / (N * q)))


def mean_field_breakdown_gap(N: int, g: float, gap0: float = 1.0) -> float:
    """The gap s* at which the expected number of unconverted units falls to one.

    N e^{-Lambda} = 1 with Lambda = g ln(gap0/s) gives s* = gap0 N^{-1/g}.
    Below it the precursor is exhausted discretely: the continuum value of
    rho_I is smaller than one unit, so the mean field describes an average over
    realisations in which the density is typically exactly zero.
    """
    return float(gap0 * N ** (-1.0 / g))


def deterministic_fraction_in_hazard_time(hazard: float, f0: float = 0.0) -> float:
    """f = 1 - (1 - f0) exp(-Lambda); the solution of df/dLambda = 1 - f."""
    return 1.0 - (1.0 - f0) * np.exp(-hazard)


def hazard_of_collapse_rate(g: float, T: float, t: float,
                            t0: float = 0.0) -> float:
    """Lambda for Gamma = g/(T-t): exactly g ln[(T-t0)/(T-t)].

    It is finite for every t < T and diverges logarithmically at T, which is
    why the time-changed process is well defined on every compact subinterval
    of [t0, T) and reaches f = 1 exactly at T.
    """
    return hazard_from_gap(g, T - t, T - t0)


def hazard_from_gap(g: float, gap: float, gap0: float = 1.0) -> float:
    """Lambda expressed through the gap s = T - t directly.

    Passing t and forming T - t loses every significant digit once s falls
    below the spacing of floats near T (for T = 1 that is about 1e-16), so the
    gap is the numerically meaningful variable near a singularity.
    """
    if gap <= 0.0:
        return float("inf")
    return g * np.log(gap0 / gap)


# --------------------------------------------------------------------------- #
# Self-similar scaling: which quantities may diverge, and which must not
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class SelfSimilarScaling:
    """Exponents of an anisotropically contracting core.

    Write s = T - t and posit
        rho ~ s^{-p},        l_i ~ s^{q_i}   (i = 1, 2, 3),
    so that the proper volume of the core is  s^{q_1+q_2+q_3}.  Then

        E_core = int rho sqrt(gamma) d^3 x ~ s^{Q - p},   Q = sum_i q_i ,

    and the integrated energy of the core is finite iff Q >= p and vanishes iff
    Q > p.  This is the whole content of "a divergent density can carry a finite
    mass": it is dimensional bookkeeping, not a dynamical mechanism, and it is
    satisfied automatically by any collapse that conserves mass, for which
    p = Q exactly.

    For a planar (Zel'dovich) caustic one contracting direction gives
    q_1 = c and q_2 = q_3 = 0, so Q = c.
    """

    p: float
    q: tuple[float, float, float]

    @property
    def Q(self) -> float:
        return float(sum(self.q))

    @property
    def energy_exponent(self) -> float:
        """E_core ~ s^{Q - p}."""
        return self.Q - self.p

    def verdict(self) -> dict[str, bool]:
        return {
            "density_diverges": self.p > 0.0,
            "energy_finite": self.energy_exponent >= 0.0,
            "energy_vanishes": self.energy_exponent > 0.0,
            "mass_conserving": abs(self.energy_exponent) < 1e-12,
        }


def planar_scaling_table(kappa: float, b: float, c: float = 1.0) -> dict[str, dict]:
    """Exponents of every quantity at a planar caustic, for
    Gamma_collapse = kappa [-Theta]_+ against Theta = -c/(T-t).

    Each entry gives the exponent n in (T-t)^n and whether the quantity stays
    finite.  Distinguishing these is the point: the density, the integrated
    mass, the vacuum, the expansion and the curvature do not stand or fall
    together.
    """
    g = kappa * c
    rows = {
        "precursor density":     -(c - g),
        "precursor column":      g,
        "defect density":        -c if b > 0 else float("inf"),
        "defect column":         0.0 if b > 0 else float("inf"),
        "vacuum increment":      (g - c) if g != c else 0.0,
        "expansion Theta":       -1.0,
        "velocity":              float("inf"),      # bounded
        "core width":            c,
    }
    out = {}
    for name, n in rows.items():
        if name == "vacuum increment":
            finite = g > c
        elif name == "velocity":
            finite = True
        elif np.isinf(n):
            finite = True                            # sector absent
        else:
            finite = n >= 0.0
        out[name] = {"exponent": n, "finite": bool(finite)}
    out["curvature invariant"] = {
        "exponent": min(out["precursor density"]["exponent"],
                        out["defect density"]["exponent"]),
        "finite": bool((g > c) and (b == 0.0)),
    }
    return out
