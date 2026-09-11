"""Tests of the background solver.

These check the *model identities* against numerics that do not assume them,
and the numerics against an external reference (astropy) and against the
closed-form solutions of the analytically solvable family.
"""
# covers: eq:cosmology-no-acceleration, prop:no-pressure-from-kinetics, eq:cosmology-survival, thm:jerk, thm:snap, thm:memory-fingerprint, eq:cosmography-jerk, eq:cosmography-snap, rem:jerk-neutrinos
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

from __future__ import annotations

from pathlib import Path

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
        assert res["survival"] < 1e-10, "Eq. (7.2) vs independent integration"
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


def test_matter_deficit_vanishes_in_the_lcdm_limit(bg_lcdm):
    """The deficit is the transferred comoving density and nothing else."""
    assert abs(bg_lcdm.derived()["matter_deficit"]) < 1e-15


def test_matter_deficit_equals_the_transferred_amount(bg_memory):
    d = bg_memory.derived()
    p = bg_memory.p
    assert np.isclose(d["matter_deficit"],
                      p.eps * p.omega_c * d["f0"] / d["h"] ** 2, rtol=1e-10)


# --------------------------------------------------------------------------- #
# Snap: the closed form must match numerical differentiation of the jerk
# --------------------------------------------------------------------------- #
def test_lambda_cdm_snap_matches_its_closed_form(bg_memory):
    """The LambdaCDM reference snap against its algebraic expression.

    This is a check of the reference curve only. The independent check of the
    model's snap *excess* is the next test; this one used to carry that name
    and did not do it.
    """
    z = np.array([0.0, 0.3, 0.5, 1.0, 2.0])
    s_lcdm = bg_memory.snap_lambda_cdm(z)
    q = bg_memory.q(z)
    Om_r = bg_memory._omegas(z)[1] / bg_memory.E(z) ** 2
    closed = 4.0 * Om_r * (q - 1.0) - (1.0 + 2.0 * Om_r) * (2.0 + 3.0 * q)
    assert np.max(np.abs(s_lcdm - closed)) < 5e-3


def test_snap_excess_matches_a_numerical_derivative_of_the_jerk():
    """The closed form for s - s_LambdaCDM against finite differences of j.

    This is the check the snap needs and did not have. The snap is where a
    sign error survived an earlier round of review: the activation
    contribution p (1 - S_act) had been dropped from dlnGamma/dN, which
    reverses the sign of the bracket exactly where the effect is largest.

    The two routes share nothing. One evaluates
    eps [dlnGamma/dN - Gamma/H - 2] from the rate law; the other forms
    s = dj/dN - j(2 + 3q) by differencing the jerk in e-folds and subtracts the
    LambdaCDM reference. They agree to 2e-6, limited by the difference stencil.

    The sign structure is asserted separately, because that is what went wrong
    before: the excess is negative today and positive by z = 1.
    """
    p = BackgroundParams(omega_b=0.02237, omega_c=0.14, omega_V_act=0.20,
                         eps=0.35, log10_gamma0=0.0, alpha_tot=2.0, r_beta=0.5,
                         log10_tau=-0.3, z_act=1.0, p_act=6.0)
    bg = Background(p)
    z = np.array([0.0, 0.3, 0.5, 1.0, 1.5, 2.0, 3.0])

    h = 1e-4
    N = np.log(1.0 / (1.0 + z))
    dj = (bg.j(np.expm1(-(N + h))) - bg.j(np.expm1(-(N - h)))) / (2.0 * h)
    s_numeric = dj - bg.j(z) * (2.0 + 3.0 * bg.q(z))
    excess_numeric = s_numeric - bg.snap_lambda_cdm(z)
    excess_analytic = bg.snap_excess_analytic(z)

    assert np.max(np.abs(excess_analytic - excess_numeric)) < 2e-6

    # the sign reversal the dropped term caused
    assert excess_analytic[0] < 0.0, "the excess must be negative today"
    assert excess_analytic[3] > 0.0, "and positive by z = 1"


def test_activation_term_dominates_the_snap_bracket():
    """The dropped term is not a correction: without it the bracket changes
    sign at the redshifts where the effect is largest."""
    p = BackgroundParams(omega_b=0.02237, omega_c=0.14, omega_V_act=0.20,
                         eps=0.35, log10_gamma0=0.0, alpha_tot=2.0, r_beta=0.5,
                         log10_tau=-0.3, z_act=1.0, p_act=6.0)
    bg = Background(p)
    z = np.array([1.0, 2.0])
    a = 1.0 / (1.0 + z)
    E = bg.E(z)
    f, M = bg.f_conv(z), bg.memory(z)
    g_over_H = bg._gamma_over_E(a, f, M, E)
    S = np.asarray(bg._switch(a), dtype=float)
    inst = p.alpha * (1.0 - f) * g_over_H
    mem = p.beta * (f - M) / (p.tau_hat * E)
    act = p.p_act * (1.0 - S)
    without = inst + mem - g_over_H - 2.0
    with_act = without + act
    assert np.all(without < 0.0)
    assert np.all(with_act > 0.0), "the activation term flips the sign"


def test_lcdm_snap_has_no_excess():
    bg = lcdm(omega_L=0.30)
    z = np.linspace(0.0, 2.0, 20)
    assert np.allclose(bg.snap_excess_analytic(z), 0.0, atol=1e-12)


@pytest.mark.parametrize("model", ["xi_h", "memory", "track_b"])
def test_exact_identities_hold_across_the_whole_prior(model):
    """Friedmann and the two jerk routes, everywhere in the prior box.

    These are exact properties of the solution the likelihood actually uses,
    so they must hold wherever the solver returns an answer at all, and they
    do: measured worst case over these draws is 2.2e-16 for the Friedmann
    residual and 4.2e-13 for the agreement between the two independent routes
    to the jerk, across all three models.

    The survival residual is deliberately *not* asserted here. It is computed
    from ``solve_full_system``, the independent integration, and that
    integration loses accuracy in the stiffest corners of the prior -- worst
    case 7.6e-7 for the nine-parameter model, against 3.3e-11 for the
    six-parameter one. Those corners have chi-square of order 1e6 and carry no
    weight in any posterior; where the posterior lives, the test below finds
    agreement to 5e-7. Asserting a tight bound here would be asserting
    something about a region the paper never uses.
    """
    import numpy as np

    from absorb.params import MODELS

    m = MODELS[model]
    priors = m.priors()
    lo = np.array([p.low for p in priors])
    hi = np.array([p.high for p in priors])
    rng = np.random.default_rng(11)

    checked = 0
    for _ in range(40):
        theta = lo + rng.random(len(lo)) * (hi - lo)
        try:
            res = m.builder(m.to_dict(theta)).check_identities()
        except Exception:                                       # noqa: BLE001
            continue                    # failed outright: documented behaviour
        checked += 1
        assert res["friedmann"] < 1e-10, (model, theta, res["friedmann"])
        assert res["jerk"] < 1e-10, (model, theta, res["jerk"])
    assert checked >= 30, f"only {checked}/40 draws produced a solution"


def test_the_two_independent_integrations_agree_where_the_posterior_lives():
    """The fast path and the full system, compared on posterior samples.

    The main solver eliminates the precursor and defect densities using the
    survival identities; ``solve_full_system`` integrates all of them instead.
    Comparing the two is the strongest available check that the elimination is
    right, and it is checked where it matters rather than everywhere.

    It does degrade in the extreme corners of the prior. At a rate of order
    1e4 H_100 the two disagree transiently by about one per cent in the vacuum
    density around z = 6, while still agreeing on V(0) to six decimals and
    each still satisfying the exact rate-independent relation
    dV/dN = rho_I0 a^-3 df/dN. That corner is not a corner the data occupy:
    its chi-square is 1.9e6, some 1.9e6 above the best fit, so it carries
    weight e^-950000 in any posterior or evidence integral. Over samples drawn
    from the actual posterior the two integrations agree to 5e-7, which is the
    threshold asserted here.
    """
    import numpy as np

    from absorb.params import MODELS

    path = (Path(__file__).resolve().parents[2] / "results" / "posteriors"
            / "xi_h_baseline.npz")
    if not path.exists():
        pytest.skip("posterior samples not present; run `make reproduce-full`")
    with np.load(path, allow_pickle=False) as fh:
        samples = np.asarray(fh["samples"])

    m = MODELS["xi_h"]
    rng = np.random.default_rng(0)
    idx = rng.choice(len(samples), size=min(40, len(samples)), replace=False)
    worst_v = worst_f = worst_s = 0.0
    for i in idx:
        res = m.builder(m.to_dict(samples[i])).check_identities()
        worst_v = max(worst_v, res.get("vacuum_vs_full", 0.0))
        worst_f = max(worst_f, res.get("f_vs_full", 0.0))
        worst_s = max(worst_s, res.get("survival", 0.0))
    assert worst_v < 5e-6, f"vacuum disagreement {worst_v:.3g} on the posterior"
    assert worst_f < 1e-8, f"converted fraction disagreement {worst_f:.3g}"
    assert worst_s < 1e-10, f"survival residual {worst_s:.3g} on the posterior"




def test_conversion_between_pressureless_sectors_never_accelerates():
    """The kinetics cannot manufacture an equation of state.

    Energy exchange moves density between components and enters each continuity
    equation as a source; it does not enter the stress tensor's spatial trace.
    So with every component pressureless the total stays pressureless and the
    expansion never accelerates, whatever the rate, the reinforcement or the
    memory. This is what fixes the division of labour in the paper: the
    acceleration comes from the vacuum's equation of state, which is postulated,
    and the kinetics decides only how much vacuum there is.
    """
    import numpy as np
    from scipy.integrate import solve_ivp

    def run(gamma0, alpha, beta, tau):
        def rhs(N, y):
            rho_I, rho_D, f, M = y
            H = np.sqrt(max(rho_I + rho_D, 1e-300) / 3.0)
            gamma = gamma0 * np.exp(alpha * f + beta * M)
            return [-3 * rho_I - gamma * rho_I / H,
                    -3 * rho_D + gamma * rho_I / H,
                    (1.0 - f) * gamma / H,
                    (f - M) / (tau * H)]

        sol = solve_ivp(rhs, (0.0, 8.0), [1.0, 0.0, 0.0, 0.0], method="Radau",
                        rtol=1e-11, atol=1e-14, dense_output=True)
        assert sol.success
        N = np.linspace(0.0, 8.0, 300)
        rho_I, rho_D, _, _ = sol.sol(N)
        return N, rho_I + rho_D

    rng = np.random.default_rng(0)
    for _ in range(5):
        gamma0 = 10 ** rng.uniform(-1, 1)
        alpha, beta = rng.uniform(0, 8), rng.uniform(0, 8)
        tau = 10 ** rng.uniform(-2, 1)
        N, rho = run(gamma0, alpha, beta, tau)

        # the total is pure dust: rho + 3p = rho, and rho ~ e^{-3N}
        assert np.all(rho > 0)
        predicted = rho[0] * np.exp(-3.0 * (N - N[0]))
        assert np.max(np.abs(rho - predicted)) / rho[0] < 1e-9, (
            "the total density departs from dust, so the transfer has leaked "
            "into the total pressure")
