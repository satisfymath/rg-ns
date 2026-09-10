"""Tests of the early-universe recipes.

The reference numbers are Planck 2018 base-LambdaCDM (Planck Collaboration
VI, 2020, Table 1/2) evaluated at omega_b = 0.02237, omega_c = 0.1200,
h = 0.6736:  r_drag = 147.09 Mpc, z_* = 1089.92, r_s(z_*) = 144.43 Mpc.
"""
# covers: eq:observations-rdrag
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

from __future__ import annotations

import numpy as np
import pytest

from absorb import early
from absorb.background import BackgroundParams, Background

OB = early.PLANCK18["omega_b"]
OC = early.PLANCK18["omega_c"]
ONU = early.OMEGA_NU0


@pytest.fixture(scope="module")
def bg():
    return early.lcdm_background()


# ---------------------------------------------------------------------------
# Fitting formulae
# ---------------------------------------------------------------------------
def test_r_drag_at_planck():
    rd = early.r_drag(OB, OB + OC, ONU)
    assert rd == pytest.approx(147.0, abs=0.3)


def test_r_drag_methods_agree():
    rd_a = early.r_drag(OB, OB + OC, ONU, method="aubourg")
    rd_b = early.r_drag(OB, OB + OC, ONU, method="brieden")
    assert abs(rd_b / rd_a - 1.0) < 0.005


@pytest.mark.parametrize("scale", [0.9, 0.95, 1.05, 1.1])
def test_r_drag_methods_agree_away_from_the_fiducial(scale):
    """The two fits are calibrated on different chains; they should still
    track each other over the range the sampler explores."""
    oc = OC * scale
    rd_a = early.r_drag(OB, OB + oc, ONU, method="aubourg")
    rd_b = early.r_drag(OB, OB + oc, ONU, method="brieden")
    assert abs(rd_b / rd_a - 1.0) < 0.005


def test_r_drag_scaling_is_monotonic():
    """More matter or more baryons -> smaller sound horizon."""
    base = early.r_drag(OB, OB + OC, ONU)
    assert early.r_drag(OB, OB + 1.1 * OC, ONU) < base
    assert early.r_drag(1.1 * OB, OB + OC, ONU) < base


def test_r_drag_rejects_nonsense():
    with pytest.raises(ValueError):
        early.r_drag(-OB, OB + OC)
    with pytest.raises(ValueError):
        early.r_drag(OB, OB + OC, method="nope")


def test_z_star_at_planck():
    assert early.z_star(OB, OB + OC + ONU) == pytest.approx(1089.0, abs=3.0)


# ---------------------------------------------------------------------------
# Sound horizon
# ---------------------------------------------------------------------------
def test_sound_horizon_at_last_scattering(bg):
    zs = early.z_star(OB, OB + OC + ONU)
    rs = early.sound_horizon(bg, zs, omega_b=OB)
    # Planck quotes r_s(z_*) = 144.43 Mpc; the two-fluid recipe reproduces it
    # to a couple of tenths of a percent (this is what KAPPA_RS corrects).
    assert rs == pytest.approx(144.43, rel=0.005)


def test_sound_horizon_decreases_with_redshift(bg):
    assert early.sound_horizon(bg, 2000.0) < early.sound_horizon(bg, 1000.0)


def test_sound_horizon_quadrature_is_converged(bg):
    """Halving the number of nodes must not move the answer: the Gauss-
    Legendre rule is far inside its asymptotic regime on this integrand."""
    zs = early.z_star(OB, OB + OC + ONU)
    ref = early.sound_horizon(bg, zs, omega_b=OB)
    x, w = early._GL_X, early._GL_W
    try:
        early._GL_X, early._GL_W = np.polynomial.legendre.leggauss(200)
        coarse = early.sound_horizon(bg, zs, omega_b=OB)
    finally:
        early._GL_X, early._GL_W = x, w
    assert coarse == pytest.approx(ref, rel=1e-9)


def test_sub_grid_continuation_matches_the_background(bg):
    """The closed-form E used below the first grid node must agree with the
    solved background in the region where both are defined."""
    a_edge = float(np.exp(bg.N[0]))
    a = a_edge * np.array([1.0, 1.5, 3.0, 10.0])
    E_cont = early._E_below_grid(bg, a)
    E_bg = bg.E(1.0 / a - 1.0)
    assert np.max(np.abs(E_cont / E_bg - 1.0)) < 1e-6


def test_sound_horizon_rejects_z_below_the_grid(bg):
    with pytest.raises(ValueError):
        early.sound_horizon(bg, 1e6)


# ---------------------------------------------------------------------------
# Distance priors and calibration
# ---------------------------------------------------------------------------
def test_cmb_distance_priors_reproduce_planck(bg):
    R, l_A = early.cmb_distance_priors(bg, OB, OB + OC + ONU)
    assert R == pytest.approx(early.PLANCK18["R"], abs=3 * early.PLANCK18["R_sigma"])
    assert l_A == pytest.approx(early.PLANCK18["l_A"],
                                abs=3 * early.PLANCK18["l_A_sigma"])


def test_recipe_offsets_reports_the_calibration(capsys):
    off = early.recipe_offsets(verbose=True)
    out = capsys.readouterr().out
    assert "kappa_rs" in out and "r_drag" in out

    # The shift parameter needs no calibration ...
    assert abs(off["dR_sigma"]) < 0.5
    # ... and the Aubourg drag scale is within 0.1% of the published value.
    assert abs(off["dr_drag_frac"]) < 1e-3
    # The acoustic scale is where the two-fluid recipe is imperfect; the
    # correction is a fraction of a percent and, being pre-recombination
    # physics, the same for every model considered.
    assert 0.99 < off["kappa_rs"] < 1.01

    kappa = early.KAPPA_RS
    assert kappa == early.kappa_rs()
    if abs(off["dl_A_sigma"]) > 0.5:
        assert kappa == pytest.approx(off["kappa_rs"])
        # applying it reproduces the published l_A exactly at the fiducial
        R, l_A = early.cmb_distance_priors(early.lcdm_background(), OB,
                                           OB + OC + ONU)
        assert l_A == pytest.approx(early.PLANCK18["l_A"], rel=1e-9)
    else:
        assert kappa == 1.0


def test_kappa_is_model_independent():
    """KAPPA_RS is applied as a constant, so it must not be re-derived per
    model: two very different backgrounds share the same correction."""
    k1 = early.kappa_rs()
    bg2 = Background(BackgroundParams(omega_b=OB, omega_c=OC, omega_V_act=0.20,
                                      eps=0.3, log10_gamma0=-0.3, alpha_tot=2.0,
                                      z_act=1.0, p_act=6.0))
    R, l_A = early.cmb_distance_priors(bg2, OB, OB + OC + ONU)
    assert np.isfinite(R) and np.isfinite(l_A)
    assert early.kappa_rs() == k1


def test_lcdm_background_hits_the_requested_h():
    for h in (0.65, 0.6736, 0.73):
        assert early.lcdm_background(h=h).h == pytest.approx(h, rel=1e-9)
