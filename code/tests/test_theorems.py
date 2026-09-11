"""Numerical checks of the theorems that carried no test.

# covers: thm:no-sign-flip, eq:positivity-no-sign-flip, thm:sandwich, eq:positivity-sandwich, thm:sign-table, eq:positivity-deficit
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py.

These three were listed in ``test_symbolic.py``'s coverage header and tested by
nothing in it. The header was bookkeeping that had drifted from the code, and
two of the three are quoted in the abstract, so the drift mattered: the ledger
reported full coverage of every summary claim while three of them had none.

The checks here are numerical and run against the same background integrator
the fits use, which is the point -- an analytic theorem and an implementation
that disagree is the failure these are meant to catch.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from absorb.params import MODELS                                 # noqa: E402


def _bg(model: str, **over):
    m = MODELS[model]
    d = dict(zip(m.params, [0.5 * (p.low + p.high) for p in m.priors()]))
    d.update(over)
    return m.builder(m.to_dict([d[k] for k in m.params]))


@pytest.mark.parametrize("model", ["xi_h", "reinforce", "memory"])
def test_the_effective_dark_matter_can_only_lose_energy(model):
    """``thm:no-sign-flip``: d ln(rho_dm^eff a^3)/d ln a <= 0 everywhere.

    Computed from the integrated solution by finite differences rather than
    from the closed form the theorem is proved with, so that a defect in the
    integration would show up rather than cancel.
    """
    # Uniform in ln a, because the derivative is taken with respect to ln a:
    # on a grid uniform in z the spacing varies by a factor of 30 across the
    # range and np.gradient loses an order of magnitude of accuracy at the far
    # end, which showed up as a 6e-3 relative mismatch that is not physics.
    N = np.linspace(np.log(1.0 / 31.0), 0.0, 4000)
    a = np.exp(N)
    z = 1.0 / a - 1.0

    for eps in (0.05, 0.3, 0.9):
        b = _bg(model, eps=eps)
        dm = b._omegas(z)[0] - b.p.omega_b * a ** -3     # dark dust, comoving

        # the theorem's closed form, which is where the sign lives
        analytic = -b.Q_V(z) / (b.E(z) * dm)
        # and the same quantity differentiated out of the integrated solution
        numeric = np.gradient(np.log(dm * a ** 3), N)
        scale = float(np.nanmax(np.abs(analytic)))

        # The sign is asserted on the closed form. A finite difference of a
        # nearly constant array is noise at the 1e-8 level, and an earlier
        # version of this test failed on a case whose true value is zero; the
        # residual tolerance is the spline undershoot of Q_V near where it
        # vanishes.
        assert np.nanmax(analytic) < 1e-6 * scale + 1e-9, (
            model, eps, np.nanmax(analytic))
        # the two agree, which is what ties the theorem to the integration
        assert np.nanmax(np.abs(numeric - analytic)) < 2e-3 * scale, (
            model, eps, np.nanmax(np.abs(numeric - analytic)), scale)
        # and the effect is real rather than zero within noise
        assert np.nanmin(analytic) < -1e-5, (model, eps, np.nanmin(analytic))


@pytest.mark.parametrize("model", ["xi_h", "reinforce", "memory"])
def test_the_expansion_history_is_bracketed(model):
    """``thm:sandwich``: two LambdaCDM models bound E^2 from both sides.

    The upper model moves the whole matter deficit from the cosmological
    constant back into matter; the lower one is the fitted LambdaCDM. Equality
    holds at a = 1 on both sides, which is asserted separately, because a
    bound that is loose everywhere would pass the inequality and mean nothing.
    """
    z = np.linspace(0.0, 20.0, 3000)
    a = 1.0 / (1.0 + z)
    for eps in (0.1, 0.5, 0.9):
        bg = _bg(model, eps=eps)
        E2 = bg.E(z) ** 2
        dust, rad, nu, V = bg._omegas(z)
        om0 = float(dust[0])                       # comoving dust today
        ov0 = float(V[0])
        # derived() divides by E0^2 = h^2; _omegas does not, so the deficit
        # has to be brought into the same units before it is added to them.
        delta = float(bg.derived()["matter_deficit"]) * bg.h ** 2
        assert delta >= -1e-12

        def lcdm(om, ov):
            return om * a ** -3 + rad + nu + ov

        lo = lcdm(om0, ov0)
        hi = lcdm(om0 + delta, ov0 - delta)
        assert np.all(E2 >= lo - 1e-9 * np.maximum(lo, 1.0)), (model, eps)
        assert np.all(E2 <= hi + 1e-9 * np.maximum(hi, 1.0)), (model, eps)
        # tight at a = 1
        assert abs(E2[0] - lo[0]) < 1e-9
        assert abs(E2[0] - hi[0]) < 1e-9


def test_the_sign_table_is_right_row_by_row():
    """``thm:sign-table``: the sign of j - 1 for each competing description.

    The first three rows are evaluated with the model's own integrator; the
    last two are the published closed forms for running vacuum and for CPL,
    evaluated over the quadrant the table names. The table is the paper's
    discriminator and appears in the abstract, so each row is checked rather
    than the headline.
    """
    z = np.linspace(0.0, 3.0, 400)

    def transfer_excess(b):
        """j - 1 - 2 Omega_r - (neutrino term): the transfer term alone.

        Subtracting the neutrino pressure term matters: LambdaCDM carries it
        too, so it is not a signature of anything, and leaving it in would let
        this test pass on a model with no transfer at all.
        """
        return 1.5 * b.Q_V(z) / b.E(z) ** 3

    # LambdaCDM: no transfer term at all
    lcdm = _bg("lcdm")
    assert np.allclose(transfer_excess(lcdm), 0.0, atol=1e-12)

    # one-way model: strictly positive wherever the transfer is on
    for model in ("xi_h", "reinforce", "memory"):
        b = _bg(model, eps=0.5)
        ex = transfer_excess(b)
        assert np.nanmin(ex) >= 0.0, model
        assert np.nanmax(ex) > 1e-6, model

    # reverse channel dominant: Q_V, and with it the excess, turns negative
    tb = _bg("track_b", eps=0.5, log10_gamma_down=1.5)
    assert np.nanmin(transfer_excess(tb)) < 0.0

    # running vacuum, nu > 0: j - 1 = -3 nu (1 + q) < 0 while q > -1
    for nu in (0.001, 0.01, 0.1):
        for q in (-0.9, -0.5, 0.0, 0.5):
            assert -3.0 * nu * (1.0 + q) < 0.0

    # CPL in the DESI-preferred quadrant, w0 > -1 and wa < 0
    rng = np.random.default_rng(7)
    w0 = rng.uniform(-1.0, -0.6, 2000)
    wa = rng.uniform(-3.0, 0.0, 2000)
    ode = 0.7
    val = ode * (4.5 * w0 * (1.0 + w0) + 1.5 * wa)
    assert np.all(val < 0.0), val.max()
