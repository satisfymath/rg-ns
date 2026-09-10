"""Tests of the Zel'dovich pancake, including its scope limits.

The referee report on this material made two points that these tests now pin:
the runs approach the caustic but never cross it, and the candidate
compression-driven channel switches itself off at the crossing.  Both are
properties of the construction, not bugs, but they bound what the experiment
can be said to show.
"""
# covers: thm:bounded-rate-obstruction, eq:defects-local-exact
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

from __future__ import annotations

import numpy as np
import pytest

from absorb.pancake import D_CROSS, Pancake, PancakeParams


def test_runs_approach_but_never_cross_the_caustic():
    """With the fiducial profile J = 1 - D cos(kq) >= 1 - D > 0 for D < 1, so
    the caustic sits exactly at D = 1 and every run stops short of it.  The
    experiment therefore probes the approach to shell crossing, not the
    multi-stream regime beyond it."""
    for N in (512, 4096):
        gap = 1e-6
        p = PancakeParams(n_sheets=N, d_end=1.0 - gap)
        pc = Pancake(p)
        J = pc.jacobian(p.d_end * D_CROSS)
        assert J.min() > 0.0, "no sheet has crossed"
        # the smallest Jacobian is the gap plus the resolution floor, and at
        # modest N the floor dominates
        eps = np.pi ** 2 / (2.0 * N ** 2)
        assert np.isclose(J.min(), gap + eps, rtol=1e-3), (N, J.min())


def test_collapse_channel_switches_off_at_the_crossing():
    """After crossing, |J| grows again, so Theta becomes positive and
    [-Theta]_+ vanishes.  The candidate channel is therefore active only on the
    approach; what happens in the multi-stream region is a separate question
    this construction does not answer."""
    p = PancakeParams(n_sheets=256, rate_mode="collapse", kappa=1.5)
    pc = Pancake(p)
    before = pc.theta(0.99, 1.0)[pc._centre]
    after = pc.theta(1.01, 1.0)[pc._centre]
    assert before < 0.0 and after > 0.0
    assert max(-before, 0.0) > 0.0
    assert max(-after, 0.0) == 0.0


def test_control_reproduces_the_exact_solution():
    """With no conversion the sheet density is exactly 1/|J|."""
    p = PancakeParams(n_sheets=1024, rate_mode="none", d_end=1.0 - 1e-6,
                      n_steps=15000)
    r = Pancake(p).run()
    exact = 1.0 / np.abs(r.final["J"])
    err = np.max(np.abs(r.final["rho_I"] - exact) / exact)
    assert err < 1e-10, err


def test_survival_identities_hold_per_sheet():
    """rho_I |J| = 1 - f and rho_D |J| = b f exactly, which is the conservation
    statement for this system.  There is no conserved 'dust plus vacuum'
    quantity, because the vacuum is not diluted by the flow."""
    p = PancakeParams(n_sheets=1024, rate_mode="collapse", kappa=1.5, b=0.25,
                      d_end=1.0 - 1e-6, n_steps=15000)
    r = Pancake(p).run()
    J = np.abs(r.final["J"])
    f = r.final["f"]
    assert np.max(np.abs(r.final["rho_I"] * J - (1.0 - f))) < 1e-8
    assert np.max(np.abs(r.final["rho_D"] * J - p.b * f)) < 1e-8


@pytest.mark.parametrize("kappa,expected", [(0.5, -0.5), (1.0, 0.0), (1.5, 0.5)])
def test_measured_exponent_matches_theory(kappa, expected):
    """The central density follows (T-t)^{kappa-1}."""
    p = PancakeParams(n_sheets=4096, rate_mode="collapse", kappa=kappa, b=0.0,
                      d_end=1.0 - 1e-6, n_steps=15000)
    r = Pancake(p).run()
    s = 1.0 - np.asarray(r.D)
    y = np.asarray(r.centre_rho_I)
    m = (s > 1e-4) & (s < 1e-3) & (y > 0)
    slope = np.polyfit(np.log(s[m]), np.log(y[m]), 1)[0]
    assert abs(slope - expected) < 0.02, (slope, expected)


def test_bounded_rate_leaves_the_exponent_unchanged():
    """The obstruction, measured: the bounded rate lowers the amplitude by a
    large factor and leaves the slope at -1."""
    common = dict(n_sheets=4096, d_end=1.0 - 1e-6, n_steps=15000)
    a = Pancake(PancakeParams(rate_mode="none", **common)).run()
    b = Pancake(PancakeParams(rate_mode="cosmo", **common)).run()
    s = 1.0 - np.asarray(a.D)
    m = (s > 1e-4) & (s < 1e-3)
    sa = np.polyfit(np.log(s[m]), np.log(np.asarray(a.centre_rho_I)[m]), 1)[0]
    sb = np.polyfit(np.log(s[m]), np.log(np.asarray(b.centre_rho_I)[m]), 1)[0]
    assert abs(sa - (-1.0)) < 0.02 and abs(sb - (-1.0)) < 0.02
    assert a.centre_rho_I[-1] / b.centre_rho_I[-1] > 50.0


def test_resolution_floor_is_the_predicted_one():
    """The caustic centre is offset by half a sheet spacing, giving
    J = s + eps with eps = (k dq/2)^2/2 = pi^2/(2 N^2) for k = 1."""
    for N in (512, 2048, 8192):
        p = PancakeParams(n_sheets=N, k=1.0)
        pc = Pancake(p)
        eps_predicted = np.pi ** 2 / (2.0 * N ** 2)
        J_at_D1 = pc.jacobian(1.0)[pc._centre]
        assert np.isclose(J_at_D1, eps_predicted, rtol=1e-3), (N, J_at_D1)
