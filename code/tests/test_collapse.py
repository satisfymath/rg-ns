"""Exact behaviour of the local sector at a caustic.

These tests pin the answer to the question the manuscript previously left as a
conjecture: whether conversion regularizes a shell crossing.  They are written
so that each one fails loudly if the corresponding statement in the paper is
weakened or strengthened.
"""
# covers: thm:bounded-rate-obstruction, eq:defects-local-exact, eq:defects-regularity, rem:hazard-time-change, rem:residual-boundary-layer
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

from __future__ import annotations

import numpy as np
import pytest

from absorb.collapse import (CollapseModel, LocalSector, bounded_rate_factor,
                             log_bounded_rate_factor,
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
    """A bounded rate leaves the exponent alone and buys only an amplitude.

    This is the flagship claim, so it is tested against the module's own
    solution of the local system rather than against the algebra of the proof.
    An earlier version of this test asserted an inequality between two
    quantities it had itself computed from ``gamma_bound``, which made it a
    restatement of arithmetic: it called nothing and could not have failed.

    What is checked here is that ``LocalSector`` -- which integrates
    d rho_I/dt = -(Theta + Gamma) rho_I with the bounded rate, and knows
    nothing about the theorem -- returns a density whose logarithmic slope in
    the distance to the caustic is the compression exponent ``c`` to four
    decimals for every bound, while the amplitude it loses is exactly the
    finite factor ``bounded_rate_factor`` predicts.
    """
    c, T = 1.0, 1.0
    m = CollapseModel(c=c, g=0.0, T=T, gamma_bounded=gamma_bound)
    free = CollapseModel(c=c, g=0.0, T=T, gamma_bounded=0.0)

    # Measured slope of ln rho_I against ln s, close to the caustic.  Taken in
    # logarithms throughout: at gamma_bound = 1e4 the density itself is the
    # float 0.0 and every ratio formed from it is nan.
    # The bounded term contributes -G(T - s) = -G T + G s, so its finite-s
    # part biases a slope fit unless G s << 1; the window is therefore scaled
    # by the bound.  At G = 1e4 a window at s ~ 1e-6 returns -0.9979, which is
    # the measurement being too coarse and not the exponent having moved.
    s = np.array([1e-6, 1e-7, 1e-8]) / max(1.0, gamma_bound)
    ln_rho = np.array([m.log_rho_exact(T - si) for si in s])
    slope = np.polyfit(np.log(s), ln_rho, 1)[0]
    assert abs(slope + c) < 1e-4, (
        f"a rate bounded by {gamma_bound} changed the exponent to {slope}")

    # The whole effect is an amplitude, and it is exactly the factor over the
    # interval actually traversed, [0, T - s]; it approaches the bound over
    # [0, T] from above, as exp(+ gamma_bound * s), so the two are compared at
    # each s and not only in the limit.
    ln_free = np.array([free.log_rho_exact(T - si) for si in s])
    ln_ratio = ln_rho - ln_free
    exact = np.array([log_bounded_rate_factor(gamma_bound, 0.0, T - si) for si in s])
    assert np.allclose(ln_ratio, exact, rtol=1e-12, atol=1e-12)
    ln_limit = log_bounded_rate_factor(gamma_bound, 0.0, T)
    assert np.all(ln_ratio > ln_limit)
    assert abs(ln_ratio[-1] - ln_limit) < gamma_bound * 1e-8 + 1e-12
    assert np.isfinite(ln_limit), (
        "the suppression is bounded below by a positive number; in float64 "
        "bounded_rate_factor itself underflows to 0.0 for gamma_bound > 745")

    # and the divergence survives it: for every bound there is a distance at
    # which the compression has won.  Compared in logarithms, because for
    # G = 1e4 the amplitude underflows float64 while remaining positive in
    # exact arithmetic -- which is the artefact the theorem is about.
    log_amplitude = -gamma_bound * T
    log_s_star = log_amplitude / c
    assert -c * (log_s_star - 1.0) + log_amplitude > 0.0
    assert -c * (log_s_star + 1.0) + log_amplitude < 0.0


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


# --------------------------------------------------------------------------- #
# Self-similar scaling: what may diverge and what must not
# --------------------------------------------------------------------------- #
def test_energy_criterion_is_the_sum_of_length_exponents():
    """E_core ~ s^{Q-p} with Q the sum of the three length exponents, so a
    divergent density carries finite energy iff Q >= p.  A mass-conserving
    collapse has p = Q exactly, which is why 'divergent density, finite mass'
    is automatic rather than a mechanism."""
    from absorb.collapse import SelfSimilarScaling
    for p, q in [(3.0, (1, 1, 1)), (1.0, (1, 0, 0)), (2.0, (1, 0.5, 0.5))]:
        sc = SelfSimilarScaling(p=p, q=q)
        assert sc.verdict()["mass_conserving"], (p, q)
        assert sc.energy_exponent == pytest.approx(0.0)
    assert SelfSimilarScaling(p=4.0, q=(1, 1, 1)).verdict()["energy_finite"] is False
    assert SelfSimilarScaling(p=2.0, q=(1, 1, 1)).verdict()["energy_vanishes"] is True


def test_planar_table_agrees_with_the_local_solution():
    """The table's exponents must reproduce the exponents of LocalSector."""
    from absorb.collapse import planar_scaling_table
    for kappa in (0.0, 0.5, 1.5, 3.0):
        tab = planar_scaling_table(kappa, b=0.0, c=1.0)
        assert tab["precursor density"]["exponent"] == pytest.approx(kappa - 1.0)
        assert tab["precursor column"]["exponent"] == pytest.approx(kappa)
        assert tab["vacuum increment"]["finite"] is (kappa > 1.0)
        assert tab["curvature invariant"]["finite"] is (kappa > 1.0)


def test_expansion_always_diverges():
    """The point most easily missed: Theta diverges in every case, including
    those where the stress tensor is finite.  What conversion can remove is the
    gravitational effect of the caustic, not the caustic of the congruence."""
    from absorb.collapse import planar_scaling_table
    for kappa in (0.0, 0.5, 1.5, 3.0, 10.0):
        for b in (0.0, 0.25):
            tab = planar_scaling_table(kappa, b=b, c=1.0)
            assert tab["expansion Theta"]["finite"] is False


def test_defect_channel_never_helps():
    """With b > 0 the curvature diverges however strong the conversion is."""
    from absorb.collapse import planar_scaling_table
    for kappa in (1.5, 5.0, 50.0):
        tab = planar_scaling_table(kappa, b=0.25, c=1.0)
        assert tab["defect density"]["finite"] is False
        assert tab["defect column"]["finite"] is True
        assert tab["curvature invariant"]["finite"] is False


def test_residual_density_has_a_boundary_layer():
    """The mean-field limit describes f but not rho_I.

    rho_I is proportional to 1 - f, whose relative fluctuation is
    sqrt(p/(N(1-p))) and diverges as the caustic is approached, so the
    N^{-1/2} statement does not transfer to the quantity the regularity
    question is about.  The continuum description of rho_I fails once the
    expected number of unconverted units drops below one, at s* = N^{-1/g}.
    """
    from absorb.collapse import (hazard_from_gap, mean_field_breakdown_gap,
                                 residual_relative_fluctuation)
    g = 1.5
    for N in (10 ** 3, 10 ** 6, 10 ** 9):
        s_star = mean_field_breakdown_gap(N, g)
        assert np.isclose(s_star, N ** (-1.0 / g))
        # at the breakdown gap the relative fluctuation is of order one
        rel = residual_relative_fluctuation(N, hazard_from_gap(g, s_star))
        assert 0.5 < rel < 2.0, (N, rel)
        # and well inside it the fluctuation is large
        deep = residual_relative_fluctuation(N, hazard_from_gap(g, s_star / 100))
        assert deep > 5.0, (N, deep)
    # while the converted fraction itself remains sharply determined
    from absorb.collapse import binomial_law_in_hazard_time
    from absorb.constants import SEED
    rng = np.random.default_rng(SEED)
    L = hazard_from_gap(g, 1e-6)
    draws = binomial_law_in_hazard_time(10 ** 6, L, rng, size=2000)
    assert draws.std() < 1e-4


@pytest.mark.parametrize("rho_D0", [0.1, 1.0])
def test_zero_branching_does_not_make_the_defect_density_finite(rho_D0):
    """b = 0 removes the source, not the compression of what is already there.

    The regularity condition in the manuscript once read "g > c and b = 0". It
    is incomplete: the defect equation's homogeneous part is
    rho_D(t_0) |J_0/J|, which diverges as (T-t)^-c for any non-zero initial
    defect density whatever b is. This test is the counterexample -- b is zero
    throughout, g > c so the precursor and the vacuum are both regular, and the
    defect density still diverges with exponent exactly -c.

    It also closes an apparent escape from the obstruction: forming the defects
    through an earlier channel does not save regularity, because defects
    already present are dust on the collapsing sheet.
    """
    c, g, T = 1.0, 1.5, 1.0
    sector = LocalSector(c=c, g=g, T=T, b=0.0, gamma_bounded=0.0)

    distances = np.array([1e-4, 1e-5, 1e-6])
    values = np.array([sector.integrate(T - s, y0=(1.0, rho_D0, 0.0)).y[1][-1]
                       for s in distances])

    # it grows without bound as the caustic is approached; the exponent below
    # is the real statement, this only rules out a finite limit
    assert values[-1] > 10.0 * values[0] > 0.0, "the defect density did not diverge"
    slope = np.polyfit(np.log(distances), np.log(values), 1)[0]
    assert abs(slope + c) < 1e-3, (
        f"expected rho_D ~ (T-t)^-{c}, measured exponent {slope}")

    # and with no defects present it stays exactly zero, which is the other half
    clean = sector.integrate(T - distances[-1], y0=(1.0, 0.0, 0.0)).y[1][-1]
    assert clean == 0.0
