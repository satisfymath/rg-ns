"""Tests of the linear growth solver."""
from __future__ import annotations

import numpy as np

from absorb.background import Background, BackgroundParams, lcdm
from absorb.growth import Growth


def test_lcdm_growth_index():
    """f = Omega_m^gamma with gamma ~ 0.55 is the standard LambdaCDM result."""
    g = Growth(lcdm(omega_L=0.30))
    assert 0.54 < float(g.growth_index(0.0)[0]) < 0.57


def test_lcdm_rsd_equals_growth_rate():
    """Without transfer the two definitions of the growth rate coincide."""
    g = Growth(lcdm(omega_L=0.30))
    z = np.linspace(0, 2, 20)
    assert np.allclose(g.f_growth(z), g.f_rsd(z), atol=1e-12)


def test_matter_domination_limit():
    """Deep in matter domination delta grows like a and f -> 1."""
    g = Growth(lcdm(omega_L=0.30), z_init=200.0)
    assert np.isclose(float(g.f_growth(50.0)[0]), 1.0, atol=0.02)


def test_transfer_suppresses_the_rsd_growth_rate():
    """Sourcing the dust makes f_RSD fall below the density growth rate."""
    bg = Background(BackgroundParams(
        omega_b=0.02237, omega_c=0.14, omega_V_act=0.20, eps=0.35,
        log10_gamma0=0.0, alpha_tot=2.0, r_beta=0.5, log10_tau=-0.3, z_act=3.0))
    g = Growth(bg)
    z = np.linspace(0, 2, 20)
    assert np.all(g.f_rsd(z) < g.f_growth(z))
    assert np.all(g.f_rsd(z) > 0.0)


def test_growth_normalization():
    g = Growth(lcdm(omega_L=0.30))
    assert np.isclose(float(g.D(0.0)[0]), 1.0, atol=1e-12)
    assert np.all(np.diff(g.D(np.linspace(0, 3, 50))) < 0.0)
