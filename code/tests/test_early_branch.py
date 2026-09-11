"""Tests of the early-universe branch.

The rate law of the original draft has a positive floor, which forces the
vacuum density negative in the past.  The repair is an activation switch
S(a) = a^p/(a^p + a_act^p).  These tests pin the two conditions the repair has
to satisfy: the conversion must be negligible at recombination, and the
integral that generates the vacuum must converge as a -> 0.
"""
# covers: thm:no-go, asm:activation, eq:solvable-activation-local, rem:activation-local, eq:solvable-activation, eq:solvable-exponent
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

from __future__ import annotations

import numpy as np
import pytest

from absorb.background import Background, BackgroundParams

Z_RECOMBINATION = 1089.9
#: Conversion must be this far below the expansion rate at recombination for
#: the standard early-universe treatment (BBN, the sound horizon) to be intact.
GAMMA_OVER_H_MAX = 1e-15


def _bg(p_act: float, tracks: bool, z_act: float = 1.0) -> Background:
    return Background(BackgroundParams(
        omega_b=0.02237, omega_c=0.14, omega_V_act=0.22, eps=0.4,
        log10_gamma0=-0.3, alpha_tot=2.0, r_beta=0.5, log10_tau=-0.3,
        z_act=z_act, p_act=p_act, switch="smooth", rate_tracks_H=tracks),
        z_max=1.0e6)


def _gamma_over_H_at(bg: Background, z: float) -> float:
    a = np.array([1.0 / (1.0 + z)])
    zero = np.zeros(1)
    return float(bg._gamma_over_E(a, zero, zero, bg.E(z))[0])


@pytest.mark.parametrize("tracks", [False, True])
def test_activation_switches_off_before_recombination(tracks):
    """With p = 6 the rate is utterly negligible when the CMB is formed."""
    bg = _bg(6.0, tracks)
    assert _gamma_over_H_at(bg, Z_RECOMBINATION) < GAMMA_OVER_H_MAX


def test_shallow_switch_is_not_safe_for_the_hubble_tracking_rate():
    """p must exceed 3 for Gamma = xi H S(a): p = 2 leaves a rate at
    recombination that is 9 orders of magnitude too large."""
    assert _gamma_over_H_at(_bg(2.0, True), Z_RECOMBINATION) > GAMMA_OVER_H_MAX


@pytest.mark.parametrize("p_act", [4.0, 6.0, 8.0])
@pytest.mark.parametrize("tracks", [False, True])
def test_vacuum_stays_positive_and_monotone(p_act, tracks):
    bg = _bg(p_act, tracks)
    assert np.all(bg.V_grid >= 0.0)
    assert np.all(np.diff(bg.V_grid) >= -1e-15)


@pytest.mark.parametrize("p_act", [4.0, 6.0, 8.0])
def test_vacuum_generated_fraction_is_bounded(p_act):
    """The model is in the partially generated regime: some vacuum predates
    activation.  A fully generated vacuum would require the whole of Omega_V
    to come from conversion, which the matter deficit forbids."""
    bg = _bg(p_act, False)
    generated = 1.0 - bg.V_grid[0] / bg.V_grid[-1]
    assert 0.0 < generated < 1.0


def test_sharper_switch_generates_less_vacuum():
    """Monotonicity check: a later, sharper activation converts less."""
    frac = [1.0 - _bg(p, False).V_grid[0] / _bg(p, False).V_grid[-1]
            for p in (2.0, 4.0, 6.0, 8.0)]
    assert all(x > y for x, y in zip(frac, frac[1:]))


def test_matter_deficit_is_non_negative():
    """Theorem: the early matter density exceeds the late one by the integrated
    transfer, so the deficit cannot be negative."""
    for p_act in (4.0, 6.0):
        d = _bg(p_act, False).derived()
        assert d["matter_deficit"] >= -1e-12
        assert d["omega_m_early"] >= d["omega_m_today"] - 1e-12


def test_activation_switch_has_an_exact_local_form():
    """S_act(a) can be written with no reference to the scale factor.

    The switch as published refers to the FLRW scale factor, which is not a
    local scalar, so the rate law is a statement about the homogeneous mode.
    The survival identity rho_I a^3 = rho_I,act (1-f) is exact, so a can be
    eliminated: with rho_* = rho_I,act / a_act^3,

        S_act = [1 + (rho_I / ((1-f) rho_*))^(p/3)]^-1.

    This checks the two forms agree identically, not approximately.
    """
    import numpy as np

    rng = np.random.default_rng(0)
    worst = 0.0
    for _ in range(500):
        p = rng.uniform(1.1, 12.0)
        a_act = rng.uniform(0.01, 0.9)
        a = rng.uniform(1e-4, 1.0)
        f = rng.uniform(0.0, 0.95)
        rho_I_act = rng.uniform(0.01, 1.0)

        rho_I = rho_I_act * (1.0 - f) / a**3
        rho_star = rho_I_act / a_act**3

        from_a = a**p / (a**p + a_act**p)
        from_density = 1.0 / (1.0 + (rho_I / ((1.0 - f) * rho_star)) ** (p / 3.0))
        worst = max(worst, abs(from_a - from_density))
    assert worst < 1e-12, f"the two forms differ by {worst:.3g}"


def test_the_local_switch_closes_under_compression():
    """Compression suppresses the rate rather than enhancing it.

    Near a fold caustic rho_I ~ |J|^-1, so the local switch behaves as
    |J|^(p/3) and the rate vanishes. Theorem A assumes only that the rate stays
    bounded on the approach; the model's own rate, written locally, does worse
    than that.
    """
    import numpy as np

    p, f, rho_star = 6.0, 0.3, 1.0
    ratios = np.array([1e2, 1e4, 1e6])
    S = 1.0 / (1.0 + (ratios / ((1.0 - f) * rho_star)) ** (p / 3.0))

    assert np.all(np.diff(S) < 0), "the switch must close as the density rises"
    # asymptotically S ~ rho^-(p/3): the measured slope must match
    slope = np.polyfit(np.log(ratios), np.log(S), 1)[0]
    assert abs(slope + p / 3.0) < 1e-3, f"slope {slope}, expected {-p/3}"
