"""Whether the deficit-to-jerk floor is usable for this model. It is not.

The manuscript boxes

    j_0 - 1 >= 2 Omega_r0 + (9/2) Delta

as a relation between two anchor-free observables, and calls it the model's
tightest internal consistency test. The bound is proved under the hypothesis
that the reduced transfer q = Q_V / (3 Mpl^2 H0^2 H) is non-decreasing up to
today, and the text says that hypothesis "has to be checked for the activation
profile in use rather than assumed".

Checked here, it fails --- not marginally and not in a corner, but everywhere.
The activation switch turns the transfer on at z_act, after which the rate
falls relative to the expansion, so q peaks at the activation redshift and
declines from there for every activation redshift and every rate. The floor is
correspondingly violated across the prior, with a median ratio near 0.46 where
the bound claims at least 4.5. These tests hold that finding in place, so that
the manuscript cannot quietly start using the floor again.
"""
from __future__ import annotations

import numpy as np
import pytest

from absorb.params import MODELS

MODEL = "xi_h"


def _background(z_act=2.0, log10_xi=-2.0, eps=0.5, omega_V_act=0.30):
    m = MODELS[MODEL]
    return m.builder(m.to_dict([0.02237, 0.1177, omega_V_act, eps,
                                log10_xi, z_act]))


@pytest.mark.parametrize("z_act", [0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 25.0])
def test_transfer_peaks_at_activation_and_then_falls(z_act):
    """q peaks at z_act, which is exactly why the hypothesis fails."""
    bg = _background(z_act=z_act)
    d = bg.transfer_diagnostics()
    assert not d["q_nondecreasing"], (
        f"the hypothesis unexpectedly holds at z_act = {z_act}; if this ever "
        f"passes, the deficit floor becomes available and the manuscript "
        f"should say so")
    assert d["z_of_peak"] == pytest.approx(z_act, rel=0.02), (
        f"q peaks at z = {d['z_of_peak']}, not at the activation redshift")


def test_floor_is_violated_across_the_prior():
    """Over uniform prior draws the floor fails, and by a wide margin."""
    m = MODELS[MODEL]
    priors = m.priors()
    lo = np.array([p.low for p in priors])
    hi = np.array([p.high for p in priors])
    rng = np.random.default_rng(0)

    ratios = []
    for _ in range(120):
        theta = lo + rng.random(len(lo)) * (hi - lo)
        try:
            d = m.builder(m.to_dict(theta)).derived()
        except Exception:                                       # noqa: BLE001
            continue
        if d["matter_deficit"] > 1e-10:
            ratios.append(d["jerk_excess"] / d["matter_deficit"])

    assert len(ratios) > 50
    violated = sum(r < 4.5 for r in ratios)
    assert violated / len(ratios) > 0.9, (
        "the floor now holds across the prior; the manuscript's statement that "
        "its hypothesis fails would need revisiting")
    assert np.median(ratios) < 4.5


def test_jerk_excess_matches_the_transfer_today():
    """eps_0 = (3/2) q_0, up to the massive-neutrino pressure term.

    This pins the normalisation the whole argument depends on: if q were
    defined differently the ratio above would mean nothing.
    """
    for z_act in (0.5, 5.0):
        bg = _background(z_act=z_act)
        d = bg.derived()
        assert d["jerk_excess"] == pytest.approx(
            1.5 * bg.transfer_diagnostics()["q0"], rel=0.05)


def test_deficit_is_the_weighted_integral_of_the_transfer():
    """Delta = int q e^{3N} dN, the other half of the normalisation."""
    bg = _background(z_act=2.0)
    q = bg.transfer_q()
    predicted = float(np.trapezoid(q * np.exp(3 * bg.N), bg.N))
    assert bg.derived()["matter_deficit"] == pytest.approx(predicted, rel=1e-4)
