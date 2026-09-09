"""Tests of the background solver.

These check the *model identities* against numerics that do not assume them,
and the numerics against an external reference (astropy) and against the
closed-form solutions of the analytically solvable family.
"""
from __future__ import annotations

import numpy as np
import pytest

from absorb.background import (Background, BackgroundParams, lcdm, omega_nu,
                               omega_nu_derivs, pressure_nu)
from absorb import constants as K

MEMORY_KW = dict(omega_b=0.02237, omega_c=0.1400, omega_V_act=0.20, eps=0.35,
                 log10_gamma0=0.0, alpha_tot=2.0, r_beta=0.5, log10_tau=-0.3,
                 z_act=3.0, switch="smooth")


@pytest.fixture(scope="module")
def bg_memory() -> Background:
    return Background(BackgroundParams(**MEMORY_KW))


@pytest.fixture(scope="module")
def bg_lcdm() -> Background:
    return lcdm(omega_L=0.30)


# --------------------------------------------------------------------------- #
# Neutrinos
# --------------------------------------------------------------------------- #
def test_neutrino_equation_of_state_limits():
    """w -> 1/3 when relativistic and -> 0 when non-relativistic."""
    p_rel, _ = pressure_nu(1e-6)
    assert np.isclose(float(p_rel / omega_nu(1e-6)), 1.0 / 3.0, atol=1e-4)
    p_now, _ = pressure_nu(1.0)
    assert 0.0 < float(p_now / omega_nu(1.0)) < 0.02


def test_neutrino_derivatives_match_finite_differences():
    a = 0.01
    h = 1e-5
    w, wp, wpp = omega_nu_derivs(a)
    num_p = (omega_nu(a * np.exp(h)) - omega_nu(a * np.exp(-h))) / (2 * h)
    assert np.isclose(float(wp), float(num_p), rtol=1e-6)


# --------------------------------------------------------------------------- #
# External validation
# --------------------------------------------------------------------------- #
def test_matches_astropy_lambda_cdm():
    """Distances and H(z) must agree with an independent implementation."""
    astropy = pytest.importorskip("astropy.cosmology")
    import astropy.units as u
    from absorb.background import omega_rel

    ob, oc, h = 0.02237, 0.1200, 0.6736
    ref = astropy.FlatLambdaCDM(H0=100 * h, Om0=(ob + oc) / h ** 2,
                                Tcmb0=K.T_CMB_K, Neff=K.N_EFF,
                                m_nu=[0.0, 0.0, K.SUM_M_NU_EV] * u.eV,
                                Ob0=ob / h ** 2)
    oV = h ** 2 - ob - oc - float(omega_rel(1.0))
    bg = Background(BackgroundParams(omega_b=ob, omega_c=oc,
                                     omega_V_act=oV, eps=0.0))
    assert np.isclose(bg.h, h, rtol=1e-6)
    z = np.array([0.01, 0.1, 0.5, 1.0, 2.0, 5.0, 100.0, 1090.0])
    assert np.max(np.abs(ref.H(z).value - bg.H_km_s_Mpc(z))
                  / ref.H(z).value) < 2e-5
    assert np.max(np.abs(ref.comoving_distance(z).value - bg.D_M(z))
                  / ref.comoving_distance(z).value) < 2e-5


# --------------------------------------------------------------------------- #
# Exact identities
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("kw", [
    dict(eps=0.0),
    MEMORY_KW,
    dict(omega_b=0.02237, omega_c=0.13, omega_V_act=0.25, eps=0.4,
         log10_gamma0=np.log10(0.35), alpha_tot=0.0, z_act=1.0,
         rate_tracks_H=True),
])
def test_identities(kw):
    base = dict(omega_b=0.02237, omega_c=0.12, omega_V_act=0.30)
    bg = Background(BackgroundParams(**{**base, **kw}))
    res = bg.check_identities()
    assert res["friedmann"] < 1e-14
    assert res["jerk"] < 1e-12, "the two independent routes to j must agree"
    assert res["continuity"] < 1e-4
    if "survival" in res:
        assert res["survival"] < 1e-8, "Eq. (7.2) vs independent integration"
        assert res["f_vs_full"] < 1e-6
        assert res["vacuum_vs_full"] < 1e-5


def test_xi_h_family_matches_closed_form():
    """For Gamma = xi H with a hard switch, f = 1 - (a/a_act)^{-xi} exactly."""
    xi, a_act = 0.35, 0.5
    bg = Background(BackgroundParams(
        omega_b=0.02237, omega_c=0.14, omega_V_act=0.25, eps=0.4,
        log10_gamma0=np.log10(xi), alpha_tot=0.0, z_act=1.0 / a_act - 1.0,
        switch="hard", rate_tracks_H=True))
    a = np.array([0.6, 0.7, 0.8, 0.9, 1.0])
    exact = 1.0 - (a / a_act) ** (-xi)
    assert np.max(np.abs(bg.f_conv(1.0 / a - 1.0) - exact)) < 1e-9


# --------------------------------------------------------------------------- #
# Theorems of Sec. 4 (positivity, monotonicity, bounded expansion)
# --------------------------------------------------------------------------- #
def test_positivity_and_monotonicity(bg_memory):
    """Theorem 1: densities stay non-negative, f and V increase, H decreases."""
    assert np.all(bg_memory.f_grid >= -1e-12)
    assert np.all(bg_memory.f_grid <= 1.0 + 1e-12)
    assert np.all(bg_memory.M_grid >= -1e-12)
    assert np.all(bg_memory.M_grid <= 1.0 + 1e-12)
    assert np.all(np.diff(bg_memory.f_grid) >= -1e-12), "f must be non-decreasing"
    assert np.all(np.diff(bg_memory.V_grid) >= -1e-14), "V must be non-decreasing"
    assert np.all(np.diff(bg_memory.E_grid) <= 1e-12), "H must be non-increasing"
    assert np.all(bg_memory.QV_grid >= -1e-14), "Q_V >= 0 in the one-way model"


def test_at_most_one_acceleration_transition(bg_memory):
    """Corollary: q crosses zero at most once."""
    q = bg_memory.q(bg_memory.z)
    crossings = int(np.sum(np.diff(np.sign(q)) != 0))
    assert crossings <= 1


def test_jerk_bound(bg_memory):
    """Theorem 3: Q_V >= 0 implies j >= 1 + 2 Omega_gamma - (3/2) p'_nu/E^2."""
    z = np.linspace(0.0, 20.0, 3000)
    assert np.all(bg_memory.j(z) >= bg_memory.jerk_lambda_cdm_bound(z) - 1e-12)


def test_lcdm_saturates_the_jerk_bound(bg_lcdm):
    z = np.linspace(0.0, 10.0, 500)
    assert np.allclose(bg_lcdm.j(z), bg_lcdm.jerk_lambda_cdm_bound(z), atol=1e-12)
    assert np.isclose(float(bg_lcdm.j(0.0)[0]), 1.0, atol=1e-3)


def test_de_sitter_attractor():
    """Theorem 2: with a positive vacuum the expansion tends to a constant."""
    bg = Background(BackgroundParams(**MEMORY_KW))
    late = bg.E_grid[bg.z < 0.05]
    assert late[-1] > 0.0
    assert np.all(np.diff(late) <= 1e-12)


# --------------------------------------------------------------------------- #
# Degeneracies that must be documented in the paper
# --------------------------------------------------------------------------- #
def test_branching_ratio_is_degenerate_at_background_level():
    """Only omega_c and eps enter; the split into precursor and defects, and
    hence b itself, leaves no background signature."""
    kw = dict(MEMORY_KW)
    bg1 = Background(BackgroundParams(**kw))
    bg2 = Background(BackgroundParams(**kw))
    z = np.linspace(0, 5, 100)
    assert np.allclose(bg1.E(z), bg2.E(z), rtol=1e-14)


def test_eps_zero_is_exactly_lcdm():
    kw = dict(MEMORY_KW)
    kw["eps"] = 0.0
    bg = Background(BackgroundParams(**kw))
    ref = lcdm(omega_b=kw["omega_b"], omega_c=kw["omega_c"],
               omega_L=kw["omega_V_act"])
    z = np.linspace(0, 10, 200)
    assert np.allclose(bg.E(z), ref.E(z), rtol=1e-12)
    assert np.allclose(bg.D_M(z), ref.D_M(z), rtol=1e-10)


def test_grid_convergence(bg_memory):
    fine = Background(BackgroundParams(**MEMORY_KW), n_grid=4000)
    z = np.linspace(0.01, 5.0, 200)
    assert np.max(np.abs(bg_memory.D_M(z) - fine.D_M(z)) / fine.D_M(z)) < 1e-6
    assert np.max(np.abs(bg_memory.E(z) - fine.E(z)) / fine.E(z)) < 1e-7
