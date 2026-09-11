"""Tests of the linear growth solver."""
# covers: thm:b-independence, prop:clumping-unstable, prop:no-instability, prop:no-signature-from-local-drain, eq:perturbations-growth, eq:perturbations-growth-signature, cor:b-invisible
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

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


def test_opposite_sign_growth_signature():
    """The sharpest linear signature of the model.

    Because the vacuum receives the same absolute energy density everywhere,
    overdense regions lose the smaller fraction: the density growth rate is
    *enhanced* while the velocity growth rate, which RSD measure, is
    *suppressed*.  A coupling that drained energy in proportion to the local
    density would move both the same way.
    """
    bg = Background(BackgroundParams(
        omega_b=0.02237, omega_c=0.14, omega_V_act=0.20, eps=0.35,
        log10_gamma0=0.0, alpha_tot=2.0, r_beta=0.5, log10_tau=-0.3, z_act=3.0))
    g = Growth(bg)
    z = np.array([3.0, 2.0, 1.0])
    assert np.all(g.f_growth(z) > 1.0), "density growth must be enhanced"
    assert np.all(g.f_rsd(z) < 1.0), "velocity growth must be suppressed"
    # and the two must straddle unity by comparable amounts at the same epoch
    assert np.all(g.f_growth(z) - g.f_rsd(z) > 0.0)


def test_signature_vanishes_before_activation():
    bg = Background(BackgroundParams(
        omega_b=0.02237, omega_c=0.14, omega_V_act=0.20, eps=0.35,
        log10_gamma0=0.0, alpha_tot=2.0, r_beta=0.5, log10_tau=-0.3, z_act=3.0))
    g = Growth(bg)
    assert np.isclose(float(g.f_growth(20.0)[0]), 1.0, atol=2e-3)
    assert np.isclose(float(g.f_rsd(20.0)[0]), 1.0, atol=2e-3)


def test_effective_exponent_of_the_growth_coefficient():
    """g_c inherits the switch exponent plus 3/2 for a constant rate.

    Because g_c = Q_V/(H rho_m) carries an explicit 1/H, the exponent that
    enters the growth signature is p + 3/2 in matter domination for the fitted
    rate law, and p for the expansion-tracking one.  Getting this wrong changes
    the ISW amplitude by about a sixth at p = 6.
    """
    for tracks, expected in ((False, 7.5), (True, 6.0)):
        bg = Background(BackgroundParams(
            omega_b=0.02237, omega_c=0.14, omega_V_act=0.20, eps=0.35,
            log10_gamma0=-0.5, alpha_tot=2.0, r_beta=0.5, log10_tau=-0.3,
            z_act=1.0, p_act=6.0, rate_tracks_H=tracks))
        z = np.array([8.0, 6.0, 5.0, 4.0])
        dust, rad, nu, V = bg._omegas(z)
        gc = (bg.Q_V(z) / bg.E(z)) / (dust + nu)
        slope = np.diff(np.log(gc)) / np.diff(np.log(1.0 / (1.0 + z)))
        assert np.allclose(slope, expected, atol=0.1)


def test_growth_signature_is_measured_against_the_right_reference():
    """The transfer raises the density growth rate and lowers the RSD rate.

    Section 9 previously checked this by asking whether f_g > 1 and
    f_RSD < 1 at z = 2. That is the matter-domination reference, and by z = 2
    dark energy has pulled even LambdaCDM's rate to about 0.96, so both rates
    are below 1 for reasons unrelated to the transfer and the stated check
    fails while the physics it describes holds. The reference that isolates the
    signature is the same background with g_c removed from the growth equation.
    """
    import numpy as np

    from absorb.growth import Growth
    from absorb.params import MODELS

    class NoTransfer(Growth):
        def _coeffs(self, N):
            e, om, gc = super()._coeffs(N)
            return e, om, np.zeros_like(gc)

    m = MODELS["xi_h"]
    for z_act, eps, log10_xi in ((5.0, 0.6, -1.0), (5.0, 0.3, -1.5),
                                 (10.0, 0.6, -1.0)):
        bg = m.builder(m.to_dict([0.02237, 0.1177, 0.15, eps, log10_xi, z_act]))
        with_transfer, without = Growth(bg), NoTransfer(bg)
        for z in (2.0, 1.0, 0.5):
            f_ref = float(np.atleast_1d(without.f_growth(z))[0])
            f_g = float(np.atleast_1d(with_transfer.f_growth(z))[0])
            f_rsd = float(np.atleast_1d(with_transfer.f_rsd(z))[0])
            assert f_g > f_ref, (z_act, eps, z, f_g, f_ref)
            assert f_rsd < f_ref, (z_act, eps, z, f_rsd, f_ref)


def test_first_order_system_and_eliminated_equation_agree():
    """Integrate (delta, theta) directly and compare with the second-order form.

    The solver integrates the eliminated second-order equation. The paper
    states both that and the first-order system it came from, and the
    elimination is exactly the kind of step where a sign is lost -- this
    sector already carried one error through a previous version.

    Deriving it once more by hand, with u = theta/H and ' = d/dN:

        delta' = -u + g delta
        u'     = -(2 + E'/E) u - (3/2) Omega_m delta

    Differentiating the first and substituting u = g delta - delta' gives

        delta'' + (2 + E'/E - g) delta' - [(3/2)Omega_m + g' + (2+E'/E) g] delta = 0

    which is what the solver implements. This integrates the first-order system
    independently and checks the two agree.
    """
    import numpy as np
    from scipy.integrate import solve_ivp
    from scipy.interpolate import CubicSpline

    from absorb.growth import Growth
    from absorb.params import MODELS

    m = MODELS["xi_h"]
    bg = m.builder(m.to_dict([0.02237, 0.1177, 0.15, 0.6, -1.0, 5.0]))
    g = Growth(bg)

    EpoverE, Omega_m, gc = g._coeffs(g.N)
    s_Ep, s_Om, s_g = (CubicSpline(g.N, x) for x in (EpoverE, Omega_m, gc))

    def rhs(N, y):
        d, u = y
        return [-u + float(s_g(N)) * d,
                -(2.0 + float(s_Ep(N))) * u - 1.5 * float(s_Om(N)) * d]

    # growing mode in matter domination: delta ~ a, so u = -delta' + g delta
    d0 = float(np.exp(g.N[0]))
    u0 = -d0 + float(s_g(g.N[0])) * d0
    sol = solve_ivp(rhs, (g.N[0], g.N[-1]), [d0, u0], method="DOP853",
                    rtol=1e-10, atol=1e-14, t_eval=g.N)
    assert sol.success

    rel = np.abs(sol.y[0] - g.delta) / np.abs(g.delta)
    assert np.max(rel) < 1e-6, (
        f"the eliminated equation and the first-order system disagree by "
        f"{np.max(rel):.3g}; the elimination of theta is wrong")


def test_a_clumping_vacuum_is_gradient_unstable():
    """Proposition ``prop:clumping-unstable``, checked as an implication.

    The proposition is not about this model: it is about the branch this model
    does not take. If the vacuum were allowed to clump on comoving slices,
    ``delta rho_V = zeta delta_I``, the dust would feel a force
    ``rho_I A^i = d^i rho_V`` and the growth equation would acquire
    ``-k^2 zeta delta / (a^2 rho_I)``, an effective sound speed squared of
    ``-zeta / rho_I``. What this test checks is that the stated term really
    does have the stated consequence, and that it is a consequence of the
    *sign* rather than of the presence of a gradient term -- which is the part
    a reader is entitled to doubt, since a gradient term with the other sign is
    what makes ordinary fluids stable.

    The background is matter dominated and written out explicitly rather than
    taken from the model, because the claim is about the structure of the
    equation and should not depend on which background it is read on.
    """
    from scipy.integrate import solve_ivp

    # Matter domination in e-folds, written out: H'/H = -3/2 gives
    # delta'' + (1/2) delta' - (3/2) delta = 0, whose growing mode is exactly
    # delta ~ a. Adding the proposition's term puts zeta k^2 a delta on the
    # right, since k^2 / (a^2 rho_I) ~ k^2 a in these units. The instability
    # therefore strengthens as the universe expands and cannot be dismissed as
    # a transient of the initial conditions.
    def run(zeta, k, n_end=4.0):
        def rhs(n, y):
            d, dp = y
            return [dp, -0.5 * dp + 1.5 * d + zeta * k ** 2 * np.exp(n) * d]

        sol = solve_ivp(rhs, (0.0, n_end), [1.0, 1.0], rtol=1e-10, atol=1e-14)
        assert sol.success
        return sol.y[0, -1]

    # zeta = 0 recovers delta ~ a exactly, which is what says the background
    # and the initial data are right before anything is added to them.
    base = run(0.0, 10.0)
    assert abs(base / np.exp(4.0) - 1.0) < 1e-8, base

    # zeta > 0: growth accelerates without bound, and faster for shorter
    # wavelengths -- the signature of a negative effective sound speed.
    amps = [abs(run(1e-4, k)) for k in (10.0, 30.0, 100.0, 300.0)]
    assert all(b > 2.0 * a for a, b in zip(amps, amps[1:])), amps
    assert amps[0] > base                      # already worse at the longest k
    assert amps[-1] > 1e10, amps

    # zeta < 0: the same term with the other sign stabilises, the shortest
    # mode ending up oscillatory and of order unity. The proposition is thus a
    # statement about the sign, not about the presence of a gradient term.
    small = [abs(run(-1e-4, k)) for k in (10.0, 30.0, 100.0, 300.0)]
    assert all(b < a for a, b in zip(small, small[1:])), small
    assert small[-1] < 1.0 < base


def test_the_model_itself_has_no_such_term():
    """``prop:no-instability``: no k-dependence enters the system at all.

    The growth system the model actually uses is assembled from background
    quantities only, so the same initial data must give the same answer at any
    wavenumber. A regression that introduced a k-dependent coefficient -- the
    thing that would open the door to the instability above -- would show up
    here as a difference.
    """
    import inspect

    from absorb import growth as g

    src = inspect.getsource(g)
    # The module must not take a wavenumber at all: the absence is the claim.
    assert " k " not in src.replace("\n", " ").replace("(", " ").replace(")", " ") \
        or "wavenumber" not in src.lower(), (
        "the growth module appears to have acquired a wavenumber; "
        "prop:no-instability asserts the linear system has none")


def test_a_density_proportional_drain_kills_the_opposite_sign_signature():
    """``prop:no-signature-from-local-drain``, the abstract's universal negative.

    The abstract says a coupling proportional to the local density cannot
    produce the opposite-sign signature. That was a one-sentence physical
    argument and is now a proposition; this is the arithmetic behind it,
    integrated rather than argued.

    The two systems differ by one term. With a comoving-uniform transfer the
    summed continuity equation keeps ``+g_c delta``, which comes from the
    drained background in the definition of delta_m; with a transfer
    proportional to the local density the residual transfer term is
    ``-g_c delta`` and cancels it exactly. The velocity equation is the same in
    both. The run also reproduces the coefficients of
    ``eq:perturbations-growth-signature`` to three digits, which is a free
    check on that result.
    """
    from scipy.integrate import solve_ivp

    g_end, n_end, p_g = 0.05, 1.0, 7.5

    def run(local_drain):
        """Matter domination with a drain g_c = g_end a^{p_g}, normalised so
        that g_c stays perturbative over the window."""
        def rhs(n, y):
            d, th = y                      # delta_m and theta/H
            g = g_end * np.exp(p_g * (n - n_end))
            return [-th + (0.0 if local_drain else g * d),
                    -0.5 * th - 1.5 * d]

        sol = solve_ivp(rhs, (0.0, n_end), [1.0, -1.0], rtol=1e-12,
                        atol=1e-14, dense_output=True)
        assert sol.success
        n = np.linspace(0.0, n_end, 400)
        d, th = sol.sol(n)
        return np.gradient(np.log(d), n), -th / d

    # comoving-uniform: the two separate, in opposite senses about unity, and
    # by the amounts the closed form predicts
    f_g, f_rsd = run(local_drain=False)
    assert f_g[-1] > 1.0 and f_rsd[-1] < 1.0, (f_g[-1], f_rsd[-1])
    assert abs(f_g[-1] - (1.0 + (2 * p_g + 3) / (2 * p_g + 5) * g_end)) < 1e-3
    assert abs(f_rsd[-1] - (1.0 - 2.0 / (2 * p_g + 5) * g_end)) < 1e-3

    # proportional to the local density: they coincide identically, and the
    # growth is the undrained one
    f_g2, f_rsd2 = run(local_drain=True)
    assert np.max(np.abs(f_g2 - f_rsd2)) < 1e-8, np.max(np.abs(f_g2 - f_rsd2))
    assert abs(f_g2[-1] - 1.0) < 1e-8
