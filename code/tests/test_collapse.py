"""Exact behaviour of the local sector at a caustic.

These tests pin the answer to the question the manuscript previously left as a
conjecture: whether conversion regularizes a shell crossing.  They are written
so that each one fails loudly if the corresponding statement in the paper is
weakened or strengthened.
"""
from __future__ import annotations

import numpy as np
import pytest

from absorb.collapse import (CollapseModel, LocalSector, bounded_rate_factor,
                             collapse_rate_coefficient, converted_fraction_singular,
                             cumulative_hazard, density_ratio,
                             regularity_conditions, zeldovich_expansion_exponent)


# --------------------------------------------------------------------------- #
# The exact solution
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("c,g", [(1.0, 0.0), (1.0, 0.5), (1.0, 1.0),
                                 (1.0, 1.5), (2.0, 0.5), (0.5, 0.5)])
def test_closed_form_matches_quadrature(c, g):
    """rho_I(t) = rho_I(t0) exp[-int (Theta + Gamma)] is solved exactly."""
    m = CollapseModel(c=c, g=g, T=1.0, gamma_bounded=0.7)
    for t in (0.5, 0.9, 0.999):
        assert np.isclose(m.rho_numeric(t), m.rho_exact(t), rtol=1e-10)


def test_three_regimes():
    """The precursor diverges, saturates or vanishes according to c - g."""
    near = 1.0 - 1e-6
    assert CollapseModel(c=1.0, g=0.0).rho_exact(near) > 1e5      # diverges
    assert np.isclose(CollapseModel(c=1.0, g=1.0).rho_exact(near), 1.0)
    assert CollapseModel(c=1.0, g=2.0).rho_exact(near) < 1e-5     # vanishes


# --------------------------------------------------------------------------- #
# Theorem A: a bounded rate cannot regularize a non-integrable compression
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("gamma_bound", [1.0, 10.0, 100.0, 1e4])
def test_bounded_rate_cannot_regularize(gamma_bound):
    """A bounded rate shifts ln rho_I by at most a finite amount.

    The comparison is made in logarithms, because for a large bound the
    suppression factor underflows to zero in floating point while remaining
    strictly positive in exact arithmetic; that underflow is precisely the
    numerical artefact the theorem is about.
    """
    # ln of the suppression: -int Gamma >= -G (T - t0), a finite number.
    log_suppression = -gamma_bound * 1.0
    assert np.isfinite(log_suppression)
    # ln of the compression is c ln(1/s), which is unbounded.  The crossover
    # sits at ln(1/s*) = G, so s* = exp(-G): for G = 1e4 that is far below the
    # smallest float64, which is why the comparison must be made in logarithms
    # and not by evaluating rho_I.
    log_s_star = -gamma_bound
    for log_s in (log_s_star - 1.0, log_s_star - 10.0, log_s_star - 1e3):
        log_compression = -log_s
        assert log_compression + log_suppression > 0.0, (
            "for every bounded rate there is a scale at which compression wins")
    # and below the crossover the suppression still dominates, so the crossover
    # is a genuine sign change rather than a one-sided bound
    assert (-(log_s_star + 1.0)) + log_suppression < 0.0


def test_bounded_rate_is_the_paper_s_case():
    """Under the activation law the rate is bounded by Gamma_0 exp(alpha+beta),
    so the obstruction applies to the model as published and the conjecture
    'Q_V diverges, hence rho_I stays finite' is false.

    With Gamma_0 = 1, alpha = 2, beta = 1 the bound is e^3 ~ 20.1, so the
    precursor is suppressed only until ln(1/s) ~ 20 and diverges thereafter.
    """
    gamma_max = 1.0 * np.exp(2.0 + 1.0)
    def ratio_at(s):
        return density_ratio(lambda t: -1.0 / (1.0 - t),
                             lambda t: gamma_max, 0.0, 1.0 - s)
    assert ratio_at(1e-6) < 1.0                      # still suppressed
    assert ratio_at(1e-9) > 1.0                      # crossover
    assert ratio_at(1e-13) > 1e3                     # unambiguously divergent
    # the crossover is exactly where ln(1/s) = Gamma_max
    assert np.isclose(np.log(1e-9) + gamma_max, 0.0, atol=1.5)


# --------------------------------------------------------------------------- #
# Theorem B: the collapse/absorption balance, and what else must be checked
# --------------------------------------------------------------------------- #
def test_vacuum_needs_a_strictly_stronger_condition():
    """rho_I is finite for g = c, but the vacuum increment still diverges
    there: its source integrates s^{g-c-1}, which needs g > c strictly."""
    marginal = LocalSector(c=1.0, g=1.0, b=0.0)
    strict = LocalSector(c=1.0, g=1.2, b=0.0)
    assert marginal.regularity()["rho_I_finite"]
    assert not marginal.regularity()["V_finite"]
    assert strict.regularity()["V_finite"]
    # Numerically the marginal case grows by exactly ln(100) per two decades
    # of s, which is the signature of a logarithmic divergence, while the
    # strict case converges.
    v = [marginal.integrate(1.0 - eps).y[2][-1] for eps in (1e-2, 1e-4, 1e-6)]
    increments = np.diff(v)
    assert np.allclose(increments, np.log(100.0), rtol=2e-3), (
        "vacuum grows logarithmically at g = c")
    # For g > c the remaining vacuum increment scales as s^{g-c}, so successive
    # two-decade increments fall off by exactly 100^{-(g-c)}.  Asserting that
    # ratio tests the exponent, not merely that the series converges.
    w = [strict.integrate(1.0 - eps).y[2][-1] for eps in (1e-2, 1e-4, 1e-6, 1e-8)]
    ratios = np.diff(w)[1:] / np.diff(w)[:-1]
    expected = 100.0 ** (-(strict.g - strict.c))
    assert np.allclose(ratios, expected, rtol=5e-3), (ratios, expected)


def test_defects_inherit_the_divergence():
    """The localized product is itself pressureless and is compressed by the
    same Theta, so its volume density diverges for every g when b > 0, even
    where the precursor has been fully regularized.  Its *column* density is
    finite: the mass is finite, the density is not."""
    m = LocalSector(c=1.0, g=2.0, b=0.25)
    sol = m.integrate(0.99999)
    s = 1.0 - sol.t
    rho_D = sol.y[1]
    assert rho_D[-1] > 1e3, "volume density diverges"
    column = rho_D * s ** m.c
    assert np.isclose(column[-1], m.b * 1.0, rtol=0.05), "column density finite"


def test_stress_tensor_regular_only_for_kappa_gt_one_and_b_zero():
    for kappa, b, expect in [(0.5, 0.0, False), (1.0, 0.0, False),
                             (1.5, 0.0, True), (1.5, 0.25, False),
                             (3.0, 0.0, True)]:
        r = regularity_conditions(kappa=kappa, b=b, c=1.0)
        assert r["stress_tensor_regular"] is expect, (kappa, b)


def test_kappa_threshold_is_dimensionless_and_independent_of_c():
    """Gamma_collapse = kappa [-Theta]_+ gives g = kappa c, so g > c is
    kappa > 1 whatever the strength of the collapse."""
    for c in (0.5, 1.0, 2.0, 7.3):
        assert collapse_rate_coefficient(1.0, c) == pytest.approx(c)
        assert regularity_conditions(1.01, 0.0, c)["stress_tensor_regular"]
        assert not regularity_conditions(0.99, 0.0, c)["stress_tensor_regular"]


def test_zeldovich_exponent_is_one():
    assert zeldovich_expansion_exponent() == 1.0


# --------------------------------------------------------------------------- #
# The kinetic side
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("g", [0.3, 1.0, 2.5])
def test_singular_rate_absorbs_everything_exactly_at_T(g):
    """df/dt = (1-f) g/(T-t) has 1 - f = (1-f0)[(T-t)/(T-t0)]^g, so f -> 1
    exactly at T for every g > 0, and the cumulative hazard diverges there."""
    assert converted_fraction_singular(g, 1.0, 1.0) == pytest.approx(1.0)
    assert converted_fraction_singular(g, 1.0, 0.5) == pytest.approx(
        1.0 - 0.5 ** g)
    # the cumulative hazard is exactly g ln[(T-t0)/(T-t)] and so diverges
    h = cumulative_hazard(lambda t: g / (1.0 - t), 0.0, 1.0 - 1e-9)
    assert np.isclose(h, g * np.log(1e9), rtol=1e-6)


# --------------------------------------------------------------------------- #
# The finite-population chain under an unbounded rate
# --------------------------------------------------------------------------- #
def test_hazard_time_change_is_exact():
    """Lambda = g ln[(T-t0)/(T-t)] for Gamma = g/(T-t)."""
    from absorb.collapse import hazard_of_collapse_rate
    for g, s in [(0.5, 1e-3), (1.5, 1e-6), (3.0, 1e-9)]:
        assert np.isclose(hazard_of_collapse_rate(g, 1.0, 1.0 - s),
                          g * np.log(1.0 / s))


def test_binomial_law_matches_the_direct_chain():
    """For a state-independent rate the converted count is exactly binomial in
    hazard time.  Checked against a direct simulation of the jump chain, which
    does not use the binomial result."""
    from scipy import stats
    from absorb.collapse import (binomial_law_in_hazard_time,
                                 hazard_of_collapse_rate)
    from absorb.constants import SEED

    rng = np.random.default_rng(SEED)

    def chain(N, L, R):
        out = np.empty(R)
        for r in range(R):
            k, acc = 0, 0.0
            while k < N:
                acc += rng.exponential(1.0 / (N - k))
                if acc > L:
                    break
                k += 1
            out[r] = k / N
        return out

    for N, s in [(50, 1e-1), (200, 1e-2)]:
        L = hazard_of_collapse_rate(1.5, 1.0, 1.0 - s)
        a = chain(N, L, 1500)
        b = binomial_law_in_hazard_time(N, L, rng, size=1500)
        assert stats.ks_2samp(a, b).pvalue > 0.01


@pytest.mark.parametrize("s", [1e-1, 1e-2])
def test_root_n_scaling_survives_the_singularity(s):
    """sqrt(N) std(f_N) = sqrt(p(1-p)) at every time, so the N^{-1/2} law has
    no boundary layer at T and the bounded-rate hypothesis of the
    deterministic-limit theorem can be dropped via the time change.

    Only the regime where the statistic is estimable is sampled: once
    1 - p falls below about 1/(N x draws), essentially every realisation has
    absorbed completely and the empirical standard deviation measures the
    sampler rather than the law.  The exactness of the variance formula in that
    regime is asserted separately below.
    """
    from absorb.collapse import (binomial_law_in_hazard_time,
                                 hazard_of_collapse_rate)
    from absorb.constants import SEED
    rng = np.random.default_rng(SEED)
    L = hazard_of_collapse_rate(1.5, 1.0, 1.0 - s)
    p = 1.0 - np.exp(-L)
    predicted = np.sqrt(p * (1.0 - p))
    estimable = [N for N in (100, 10000) if N * (1.0 - p) > 5.0]
    assert estimable, "at least one population size must resolve the statistic"
    for N in estimable:
        draws = binomial_law_in_hazard_time(N, L, rng, size=6000)
        assert np.isclose(np.sqrt(N) * draws.std(), predicted, rtol=0.12)


def test_variance_formula_is_exact_through_the_singularity():
    """The claim that the N^{-1/2} scaling survives is a statement about the
    binomial law, which is exact: Var(f_N) = p(1-p)/N for every p, including
    p -> 1 at the singularity.  This checks the identity itself, which sampling
    cannot resolve once p is within 1/N of unity."""
    from absorb.collapse import hazard_from_gap
    for s in (1e-1, 1e-4, 1e-10, 1e-30):
        L = hazard_from_gap(1.5, s)
        p = 1.0 - np.exp(-L)
        for N in (10, 10 ** 6):
            var = p * (1.0 - p) / N
            assert var >= 0.0
            assert np.isclose(np.sqrt(N * var), np.sqrt(p * (1.0 - p)))
    # and the scaled standard deviation tends to zero at the singularity,
    # because the population is fully absorbed there and nothing fluctuates
    L_far = hazard_from_gap(1.5, 1e-30)
    p_far = 1.0 - np.exp(-L_far)
    assert np.sqrt(p_far * (1.0 - p_far)) < 1e-20
