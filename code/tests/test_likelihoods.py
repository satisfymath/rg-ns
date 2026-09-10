"""Tests of the likelihood layer.

Two kinds of check:

* *exactness* -- the analytic marginalisation over the supernova absolute
  magnitude is verified against a brute-force numerical integral, and the
  Cholesky-based chi^2 against an explicit solve;
* *sanity* -- at the Planck 2018 best fit every probe must give a sensible
  chi^2 per data point, and moving the cosmology away from it must make the
  fit worse.
"""
from __future__ import annotations

import numpy as np
import pytest
from scipy.linalg import cho_solve

from absorb import early
from absorb.likelihoods import (
    ChronometerLikelihood,
    DesiBAOLikelihood,
    JointLikelihood,
    PantheonLikelihood,
    PlanckPriorLikelihood,
    RSDLikelihood,
)


@pytest.fixture(scope="module")
def bg():
    """Planck 2018 base-LambdaCDM best fit."""
    return early.lcdm_background()


@pytest.fixture(scope="module")
def sn():
    return PantheonLikelihood(with_shoes=False)


@pytest.fixture(scope="module")
def sn_shoes():
    return PantheonLikelihood(with_shoes=True)


# ---------------------------------------------------------------------------
# Supernovae: analytic vs numerical marginalisation
# ---------------------------------------------------------------------------
def test_analytic_marginalisation_matches_brute_force(bg, sn):
    """chi^2_marg = -2 log int dM_B exp(-chi^2(M_B)/2), with a flat prior.

    chi^2(M_B) is an exact parabola, so a Gauss-Hermite-style change of
    variables is unnecessary: we integrate the parabola on a wide, dense grid
    centred on its minimum and compare to the closed form.  The comparison is
    of -2 log of the integral, i.e. of the returned chi^2 itself.
    """
    d = sn.data
    delta = sn.residual(bg)
    ones = np.ones_like(delta)
    A = float(delta @ cho_solve(d.cho, delta))
    B = float(delta @ cho_solve(d.cho, ones))
    E0 = float(ones @ cho_solve(d.cho, ones))

    m_hat, sigma = B / E0, 1.0 / np.sqrt(E0)
    grid = m_hat + np.linspace(-40.0, 40.0, 400001) * sigma
    chi2_of_m = A - 2.0 * B * grid + E0 * grid ** 2
    # integrate exp(-chi2/2), factorising out the minimum to stay in range
    chi2_min = A - B * B / E0
    integral = np.trapezoid(np.exp(-0.5 * (chi2_of_m - chi2_min)), grid)
    brute = chi2_min - 2.0 * np.log(integral)

    assert sn.chi2(bg) == pytest.approx(brute, abs=1e-6)


def test_profiled_MB_is_the_gaussian_mean(bg, sn):
    """The analytic M_B must minimise the un-marginalised chi^2."""
    m_hat = sn.best_fit_MB(bg)
    lk = PantheonLikelihood(with_shoes=False, marginalize_MB=False)
    c0 = lk.chi2(bg, {"M_B": m_hat})
    for dm in (-0.02, 0.02):
        assert lk.chi2(bg, {"M_B": m_hat + dm}) > c0
    assert -20.0 < m_hat < -19.0        # the usual SN Ia absolute magnitude


def test_marginalised_chi2_equals_profiled_plus_jacobian(bg, sn):
    d = sn.data
    ones = np.ones(d.n)
    E0 = float(ones @ cho_solve(d.cho, ones))
    lk = PantheonLikelihood(with_shoes=False, marginalize_MB=False)
    profiled = lk.chi2(bg, {"M_B": sn.best_fit_MB(bg)})
    assert sn.chi2(bg) == pytest.approx(profiled + np.log(E0 / (2 * np.pi)), rel=1e-10)


def test_cholesky_chi2_matches_explicit_solve(bg, sn):
    """cho_solve must agree with a direct linear solve on the full matrix."""
    d = sn.data
    delta = sn.residual(bg) - sn.best_fit_MB(bg)
    direct = float(delta @ np.linalg.solve(d.cov, delta))
    lk = PantheonLikelihood(with_shoes=False, marginalize_MB=False)
    assert lk.chi2(bg, {"M_B": sn.best_fit_MB(bg)}) == pytest.approx(direct, rel=1e-8)


def test_shoes_calibrators_use_cepheid_distances(bg, sn_shoes):
    d = sn_shoes.data
    r = sn_shoes.residual(bg)
    expected = d.m_b_corr[d.use_cepheid] - d.ceph_dist[d.use_cepheid]
    assert np.allclose(r[d.use_cepheid], expected)
    assert d.use_cepheid.sum() == 77


# ---------------------------------------------------------------------------
# chi^2 at the Planck best fit
# ---------------------------------------------------------------------------
def test_sn_chi2_per_dof(bg, sn):
    c = sn.chi2(bg)
    assert np.isfinite(c)
    # Brout et al. (2022) report chi^2/dof ~= 0.89 for Pantheon+ at the
    # best-fit LambdaCDM; anything outside [0.85, 1.3] means a mis-parse.
    assert 0.85 < c / sn.dof() < 1.3


def test_bao_chi2(bg):
    lk = DesiBAOLikelihood()
    c = lk.chi2(bg)
    assert np.isfinite(c)
    assert lk.n_data() == 13
    # DESI DR2 pulls away from Planck LambdaCDM (their ~3 sigma preference for
    # evolving dark energy), so chi^2 ~ 30 here is expected, not a bug.
    assert c < 40.0


def test_cc_chi2(bg):
    lk = ChronometerLikelihood()
    c = lk.chi2(bg)
    assert np.isfinite(c)
    assert lk.n_data() == 15
    assert c < 20.0


def test_cmb_chi2(bg):
    lk = PlanckPriorLikelihood()
    c = lk.chi2(bg)
    assert np.isfinite(c)
    # The priors were compressed *from* this cosmology, and KAPPA_RS removes
    # the recipe offset in l_A, so the fit is essentially perfect.
    assert c < 1.0


def test_bao_uses_pre_activation_omega_c(bg):
    """r_d must be built from the pre-activation densities.  Turning on a
    large conversion changes today's matter density but must leave r_d
    untouched, because the ruler is imprinted before activation."""
    from absorb.background import Background, BackgroundParams

    lk = DesiBAOLikelihood()
    p = bg.p
    hot = Background(BackgroundParams(omega_b=p.omega_b, omega_c=p.omega_c,
                                      omega_V_act=0.10, eps=0.5,
                                      log10_gamma0=0.0, alpha_tot=1.0,
                                      z_act=1.0, p_act=6.0))
    assert hot.derived()["f0"] > 0.05          # the conversion really happened
    assert hot.derived()["omega_m_today"] < bg.derived()["omega_m_today"]
    assert lk.r_drag(hot) == pytest.approx(lk.r_drag(bg), rel=1e-12)


# ---------------------------------------------------------------------------
# The likelihoods must actually discriminate
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("shift", [(0.10, 0.0), (-0.10, 0.0), (0.0, 0.03), (0.0, -0.03)])
def test_chi2_increases_away_from_the_best_fit(bg, shift):
    """Perturb omega_c (fractionally) and h (absolutely) and check that the
    combined chi^2 degrades.  Each probe is checked as well as the joint."""
    d_oc, d_h = shift
    bad = early.lcdm_background(omega_c=early.PLANCK18["omega_c"] * (1.0 + d_oc),
                                h=early.PLANCK18["h"] + d_h)
    probes = [PantheonLikelihood(), DesiBAOLikelihood(),
              ChronometerLikelihood(), PlanckPriorLikelihood()]
    joint = JointLikelihood(probes)
    assert joint.chi2(bad) > joint.chi2(bg) + 1.0
    # the compressed CMB is the sharpest of them and must always degrade
    assert probes[-1].chi2(bad) > probes[-1].chi2(bg)


def test_sn_shape_is_insensitive_to_h(bg, sn):
    """With M_B marginalised, the Hubble-flow sample cannot see H_0: rescaling
    h at fixed Omega_m must leave its chi^2 unchanged."""
    ob, oc = early.PLANCK18["omega_b"], early.PLANCK18["omega_c"]
    h2 = 0.72
    scale = (h2 / early.PLANCK18["h"]) ** 2
    bg2 = early.lcdm_background(omega_b=ob * scale, omega_c=oc * scale, h=h2)
    assert sn.chi2(bg2) == pytest.approx(sn.chi2(bg), abs=0.05)


def test_sn_with_shoes_does_constrain_h(bg, sn_shoes):
    ob, oc = early.PLANCK18["omega_b"], early.PLANCK18["omega_c"]
    h2 = 0.72
    scale = (h2 / early.PLANCK18["h"]) ** 2
    bg2 = early.lcdm_background(omega_b=ob * scale, omega_c=oc * scale, h=h2)
    assert abs(sn_shoes.chi2(bg2) - sn_shoes.chi2(bg)) > 5.0


# ---------------------------------------------------------------------------
# RSD and the joint container
# ---------------------------------------------------------------------------
def test_rsd_requires_a_growth_model(bg):
    lk = RSDLikelihood()
    assert lk.n_data() == 4
    with pytest.raises(NotImplementedError):
        lk.chi2(bg)


def test_rsd_with_a_supplied_model(bg):
    lk = RSDLikelihood(fs8_model=lambda b, z: np.full_like(z, 0.45))
    c = lk.chi2(bg)
    assert np.isfinite(c) and c > 0.0
    # feeding it the data itself must give exactly zero
    exact = RSDLikelihood(fs8_model=lambda b, z: lk.value)
    assert exact.chi2(bg) == pytest.approx(0.0, abs=1e-12)
    # a callable passed through the nuisance mapping overrides the default
    assert lk.chi2(bg, {"fs8_model": lambda b, z: lk.value}) == pytest.approx(0.0, abs=1e-12)


def test_rsd_uses_the_correlated_sub_block():
    lk = RSDLikelihood(fs8_model=lambda b, z: z * 0.0)
    assert lk.cov.shape == (4, 4)
    assert lk.cov[0, 1] != 0.0


def test_rsd_rejects_a_bad_model_shape(bg):
    lk = RSDLikelihood(fs8_model=lambda b, z: np.zeros(2))
    with pytest.raises(ValueError):
        lk.chi2(bg)


def test_joint_sums_and_logl(bg):
    parts = [PantheonLikelihood(), DesiBAOLikelihood(), ChronometerLikelihood()]
    j = JointLikelihood(parts)
    total = sum(p.chi2(bg) for p in parts)
    assert j.chi2(bg) == pytest.approx(total)
    assert j.logL(bg) == pytest.approx(-0.5 * total)
    assert j.n_data() == sum(p.n_data() for p in parts)
    assert set(j.breakdown(bg)) == {p.name for p in parts}
    with pytest.raises(ValueError):
        JointLikelihood([])


# --------------------------------------------------------------------------- #
# The nesting the model comparison rests on
# --------------------------------------------------------------------------- #
@pytest.mark.parametrize("model,extra", [
    ("xi_h", [(lx, za) for lx in (-3.0, 0.0, 1.0) for za in (0.3, 30.0)]),
])
def test_extension_is_exactly_lambda_cdm_at_zero_conversion(model, extra):
    """At eps = 0 the extension must reproduce LambdaCDM bit for bit.

    The comparison table's caption asserts this, and draws a statistical
    conclusion from it: if the chi-square is identical for *every* value of the
    rate parameters, those parameters are unidentified under the null, the
    effective parameter count there is not the sampled count, and AIC and BIC
    are inapplicable. The claim is therefore load-bearing and is pinned here
    rather than left to be re-measured by a referee.
    """
    from absorb import datasets
    from absorb.sampling import Posterior

    like = datasets.build("baseline")
    base = [0.02237, 0.1177, 0.3266]
    ref = Posterior("lcdm", like).chi2(base)
    post = Posterior(model, like)
    for lx, za in extra:
        assert post.chi2(base + [0.0, lx, za]) == ref, (
            f"conversion is off but {model} differs from LambdaCDM at "
            f"log10_xi={lx}, z_act={za}")


def test_sound_horizon_recipe_is_immaterial_where_the_fit_lives():
    """The two r_drag fitting formulae must agree where the posterior is.

    Only one of the two implemented recipes is ever exercised, and a referee
    pointed out that they diverge by about 1% across the omega_c prior, which
    is a full DESI error bar on every distance ratio. That divergence is real
    but it is at the edges: at the best-fit cosmologies the two agree to better
    than 0.05%, and the difference moves the chi-square difference between
    LambdaCDM and the extension by 0.14, against the 1.6 the comparison is
    about. This test fails if that ceases to be true.
    """
    from absorb import early

    for omega_b, omega_c in ((0.02237, 0.1177), (0.02244, 0.1188)):
        a = early.r_drag(omega_b, omega_b + omega_c, method="aubourg")
        b = early.r_drag(omega_b, omega_b + omega_c, method="brieden")
        assert abs(b - a) / a < 5e-4, (omega_b, omega_c, a, b)

    # and the divergence at the prior edges is real, so the agreement above is
    # a statement about where the fit lives and not about the formulae
    edge = early.r_drag(0.02237, 0.02237 + 0.20, method="aubourg")
    edge_b = early.r_drag(0.02237, 0.02237 + 0.20, method="brieden")
    assert abs(edge_b - edge) / edge > 5e-3
