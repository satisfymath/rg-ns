"""Early-universe quantities: drag epoch, last scattering and the sound horizon.

Everything in this module concerns physics *before* recombination, where the
self-reinforced absorption model is indistinguishable from LambdaCDM: the
activation switch S_act(a) = a^p/(a^p + a_act^p) with p >~ 6 and a_act ~ 1/2
suppresses the conversion rate by more than twenty orders of magnitude at
a ~ 10^-3.  The convertible sector is therefore still entirely in its
precursor (pressureless) form at recombination, and the baryon-photon fluid
sees exactly the standard expansion history.  This is what allows us to

  * use the standard fitting formulae for r_drag and z_star, and
  * treat the calibration offset of the sound-horizon *recipe* (see
    :data:`KAPPA_RS` below) as a model-independent constant.

Conventions follow :mod:`absorb.constants`: reduced densities
omega_X = rho_X / (3 M_Pl^2 H_100^2), E = H/H_100, distances in Mpc.

Notation
--------
``omega_b``   reduced baryon density (= Omega_b h^2)
``omega_cb``  reduced baryon + cold-dark density, *excluding* neutrinos
``omega_m``   total reduced matter density, *including* massive neutrinos
``omega_nu``  reduced density of massive neutrinos today

For the absorption model the relevant omega_c is always the **pre-activation**
value stored in :class:`~absorb.background.BackgroundParams`, because that is
the matter density the acoustic oscillations actually respond to.
"""
from __future__ import annotations

from typing import Literal

import numpy as np

from . import background as bgmod
from . import constants as K

__all__ = [
    "OMEGA_NU0",
    "PLANCK18",
    "KAPPA_RS",
    "r_drag",
    "z_star",
    "sound_horizon",
    "cmb_distance_priors",
    "lcdm_background",
    "recipe_offsets",
    "kappa_rs",
]

#: Reduced density of the massive-neutrino sector today, omega_nu = Omega_nu h^2.
#: For sum m_nu = 0.06 eV this is 0.00064, the value Aubourg et al. (2015) use
#: as the fiducial in their Eq. (16).
OMEGA_NU0: float = float(bgmod.omega_nu(1.0))

#: Planck 2018 TT,TE,EE+lowE+lensing base-LambdaCDM best fit and the derived
#: quantities we calibrate against (Planck 2018 VI, Table 1 & Table 2;
#: R and l_A as compressed by Chen, Huang & Wang 2019, arXiv:1808.05724).
PLANCK18: dict[str, float] = {
    "omega_b": 0.02237,
    "omega_c": 0.1200,
    "h": 0.6736,
    "R": 1.7502,
    "R_sigma": 0.0046,
    "l_A": 301.471,
    "l_A_sigma": 0.090,
    "r_drag": 147.09,        # Mpc
    "z_star": 1089.92,
}

# Gauss-Legendre nodes for the sound-horizon integral.  400 nodes in ln a give
# a relative accuracy better than 1e-10 on a smooth integrand and cost one
# vectorised evaluation of E(z).
_GL_N = 400
_GL_X, _GL_W = np.polynomial.legendre.leggauss(_GL_N)


# ---------------------------------------------------------------------------
# Fitting formulae
# ---------------------------------------------------------------------------
def r_drag(
    omega_b: float,
    omega_cb: float,
    omega_nu: float = OMEGA_NU0,
    method: Literal["aubourg", "brieden"] = "aubourg",
) -> float:
    """Comoving sound horizon at the baryon drag epoch, in Mpc.

    Parameters
    ----------
    omega_b
        Reduced baryon density Omega_b h^2.
    omega_cb
        Reduced baryon + CDM density, (Omega_b + Omega_c) h^2, *excluding*
        massive neutrinos.  In the absorption model this is the
        **pre-activation** omega_b + omega_c: at the drag epoch none of the
        convertible sector has been converted yet.
    omega_nu
        Reduced density of massive neutrinos today.
    method
        ``"aubourg"``  -- Aubourg et al. 2015 (PRD 92, 123516), Eq. (16),
        a fit to CAMB accurate to 0.021% over the range covered by their
        chains::

            r_d = 55.154 exp[-72.3 (omega_nu + 0.0006)^2]
                  / (omega_cb^0.25351 omega_b^0.12807)   Mpc

        ``"brieden"`` -- Brieden et al. 2022 (JCAP 2022, 024), the
        N_eff-aware parametrisation normalised on the Planck 2018 fit::

            r_d = 147.05 (omega_m/0.1432)^-0.23
                  (N_eff/3.04)^-0.1 (omega_b/0.02236)^-0.13   Mpc

        where omega_m = omega_cb + omega_nu is the *total* matter density.

    Notes
    -----
    Both are fits to the full Boltzmann calculation at fixed standard
    pre-recombination physics.  They are used instead of the direct integral
    of :func:`sound_horizon` because the latter needs an accurate baryon-drag
    redshift, which is itself only available as a fitting formula; the two
    routes agree to a few tenths of a percent (see :func:`recipe_offsets`).
    """
    if omega_b <= 0.0 or omega_cb <= 0.0:
        raise ValueError("r_drag: omega_b and omega_cb must be positive")

    if method == "aubourg":
        return 55.154 * np.exp(-72.3 * (omega_nu + 0.0006) ** 2) / (
            omega_cb ** 0.25351 * omega_b ** 0.12807
        )
    if method == "brieden":
        omega_m = omega_cb + omega_nu
        return (
            147.05
            * (omega_m / 0.1432) ** -0.23
            * (K.N_EFF / 3.04) ** -0.1
            * (omega_b / 0.02236) ** -0.13
        )
    raise ValueError(f"r_drag: unknown method {method!r}")


def z_star(omega_b: float, omega_m: float) -> float:
    """Redshift of photon last scattering (Hu & Sugiyama 1996, ApJ 471, 542).

    Their Eq. (E1),

        g1 = 0.0783 omega_b^-0.238 / (1 + 39.5 omega_b^0.763)
        g2 = 0.560 / (1 + 21.1 omega_b^1.81)
        z_* = 1048 (1 + 0.00124 omega_b^-0.738) (1 + g1 omega_m^g2),

    is a fit to the peak of the visibility function, accurate at the ~0.1%
    level for the parameter range of interest.  ``omega_m`` is the *total*
    non-relativistic density at recombination, omega_b + omega_c (+ omega_nu;
    massive neutrinos are still relativistic there, so including them shifts
    z_* by well under one, far inside the fit's own accuracy).
    """
    g1 = 0.0783 * omega_b ** -0.238 / (1.0 + 39.5 * omega_b ** 0.763)
    g2 = 0.560 / (1.0 + 21.1 * omega_b ** 1.81)
    return 1048.0 * (1.0 + 0.00124 * omega_b ** -0.738) * (1.0 + g1 * omega_m ** g2)


# ---------------------------------------------------------------------------
# Sound horizon by direct integration
# ---------------------------------------------------------------------------
def _E_below_grid(bg: "bgmod.Background", a: np.ndarray) -> np.ndarray:
    """Expansion rate below the first node of the background grid.

    The background object is solved on a finite grid (by default down to
    z = 3e4).  The sound-horizon integrand behaves like a/sqrt(omega_r) deep
    in radiation domination, so the integral from a = 0 up to the grid edge
    still contributes ~9 Mpc and cannot be dropped; on the other hand a cubic
    spline of E ~ a^-2 must not be extrapolated over five e-folds.

    Below the grid every species is separately conserved -- the conversion
    switch is closed by ~20 orders of magnitude there -- so E is known in
    closed form.  We read the composition off the background *at its own
    edge* rather than from its parameters, which keeps this valid for any
    model with conserved dust, free-streaming radiation and a frozen vacuum:

        E^2(a) = rho_dust(a_e) (a_e/a)^3 + omega_gamma a^-4
                 + omega_nu(a) + omega_V(a_e).

    The continuation matches ``bg.E`` at the edge to machine precision and,
    one e-fold above it, to ~1e-8 relative (asserted in the test suite).
    """
    a_e = float(np.exp(bg.N[0]))
    z_e = 1.0 / a_e - 1.0
    E_e2 = float(np.atleast_1d(bg.E(z_e))[0]) ** 2
    V_e = float(np.atleast_1d(bg.omega_V(z_e))[0])
    dust_e = E_e2 - K.OMEGA_GAMMA * a_e ** -4 - float(bgmod.omega_nu(a_e)) - V_e
    return np.sqrt(
        dust_e * (a_e / a) ** 3 + K.OMEGA_GAMMA * a ** -4 + bgmod.omega_nu(a) + V_e
    )


def _rs_integrand(a: np.ndarray, E: np.ndarray, omega_b: float) -> np.ndarray:
    """c_s / (a E) in units of c/H_100, i.e. the integrand in N = ln a."""
    R_b = 3.0 * omega_b * a / (4.0 * K.OMEGA_GAMMA)
    return 1.0 / (np.sqrt(3.0 * (1.0 + R_b)) * a * E)


def _gl_quad(N_lo: float, N_hi: float, f) -> float:
    """Gauss-Legendre quadrature of ``f`` over [N_lo, N_hi]."""
    half = 0.5 * (N_hi - N_lo)
    Nq = 0.5 * (N_hi + N_lo) + half * _GL_X
    return float(half * np.dot(_GL_W, f(Nq)))


def sound_horizon(bg: "bgmod.Background", z: float, omega_b: float | None = None) -> float:
    """Comoving sound horizon of the baryon-photon fluid at redshift ``z`` [Mpc].

    .. math::
        r_s(z) = \\int_0^{a(z)} \\frac{c_s(a)\\, da}{a^2 H(a)},
        \\qquad c_s = \\frac{c}{\\sqrt{3 (1 + R_b)}},
        \\qquad R_b = \\frac{3 \\omega_b a}{4 \\omega_\\gamma}.

    In reduced units H = H_100 E, so with the substitution a = e^N

    .. math::
        r_s = \\frac{c}{H_{100}} \\int_{-\\infty}^{N(z)}
              \\frac{dN}{\\sqrt{3(1+R_b)}\\; a\\, E(a)} .

    The integral is split at the first node of the background grid.  Above it
    the rule uses the *model's own* ``bg.E``; below it the closed-form
    continuation :func:`_E_below_grid` is used, because a cubic spline of
    E ~ a^-2 cannot be extrapolated over five e-folds while the integrand,
    which grows like a in radiation domination, still contributes ~9 Mpc there
    (the tail of int e^N dN is *not* negligible).  The remaining truncation at
    a = 1e-9 is below 1e-4 Mpc.

    For a > a_act the absorption model departs from LambdaCDM, but
    recombination is ~3 e-folds earlier and the switch has suppressed the
    conversion to nothing there, so the result is the standard one; the
    routine is nonetheless written generically so that it stays valid for any
    background handed to it.
    """
    if omega_b is None:
        omega_b = bg.p.omega_b
    N_hi = -float(np.log1p(z))
    N_edge = float(bg.N[0])
    if N_hi <= N_edge:
        raise ValueError(
            "sound_horizon: z lies below the first node of the background grid; "
            "rebuild the Background with a larger z_max"
        )

    def f_grid(N: np.ndarray) -> np.ndarray:
        a = np.exp(N)
        return _rs_integrand(a, bg.E(1.0 / a - 1.0), omega_b)

    def f_early(N: np.ndarray) -> np.ndarray:
        a = np.exp(N)
        return _rs_integrand(a, _E_below_grid(bg, a), omega_b)

    # a = 1e-9 is ~1e-4 e-folds' worth of integrand, i.e. far below 1e-4 Mpc.
    total = _gl_quad(np.log(1e-9), N_edge, f_early) + _gl_quad(N_edge, N_hi, f_grid)
    return float(K.HUBBLE_DIST_MPC * total)


def cmb_distance_priors(
    bg: "bgmod.Background",
    omega_b: float,
    omega_m: float,
    apply_kappa: bool = True,
) -> tuple[float, float]:
    """CMB shift parameter ``R`` and acoustic scale ``l_A``.

    .. math::
        R = \\frac{\\sqrt{\\omega_m}\\, H_{100}}{c}\\, D_M(z_*),
        \\qquad l_A = \\pi \\frac{D_M(z_*)}{r_s(z_*)} .

    ``omega_m`` is the reduced matter density *at recombination* (so, in the
    absorption model, the pre-activation one) and enters R through
    sqrt(Omega_m H_0^2) = H_100 sqrt(omega_m).  ``D_M`` is in Mpc, hence the
    factor 100/c that makes R dimensionless.

    With ``apply_kappa=True`` (the default) the directly integrated sound
    horizon is multiplied by :data:`KAPPA_RS`, the fixed calibration factor
    described in :func:`recipe_offsets`.
    """
    zs = z_star(omega_b, omega_m)
    D_M = float(np.atleast_1d(bg.D_M(zs))[0])
    r_s = sound_horizon(bg, zs, omega_b=omega_b)
    if apply_kappa:
        r_s *= kappa_rs()
    R = np.sqrt(omega_m) * D_M * 100.0 / K.C_LIGHT_KM_S
    l_A = np.pi * D_M / r_s
    return float(R), float(l_A)


# ---------------------------------------------------------------------------
# Fiducial background and calibration of the recipe
# ---------------------------------------------------------------------------
def lcdm_background(
    omega_b: float = PLANCK18["omega_b"],
    omega_c: float = PLANCK18["omega_c"],
    h: float = PLANCK18["h"],
    **kw,
) -> "bgmod.Background":
    """LambdaCDM background with a prescribed ``h``.

    :class:`~absorb.background.Background` treats h as *derived*
    (h^2 = E^2(a=1)), so a target h is imposed by choosing the vacuum density
    that closes the Friedmann constraint today,

        omega_V = h^2 - omega_b - omega_c - omega_gamma - omega_nu(a=1).
    """
    omega_V = h ** 2 - omega_b - omega_c - K.OMEGA_GAMMA - OMEGA_NU0
    return bgmod.lcdm(omega_b=omega_b, omega_c=omega_c, omega_L=omega_V, **kw)


_KAPPA_CACHE: dict[str, float] = {}


def recipe_offsets(verbose: bool = False) -> dict[str, float]:
    """Calibrate this module's recipes against published Planck 2018 values.

    Evaluates (R, l_A, r_drag, z_*) for the Planck 2018 base-LambdaCDM best
    fit (omega_b = 0.02237, omega_c = 0.1200, h = 0.6736) with the *raw*
    recipes (no kappa correction) and compares them to

        R      = 1.7502  +/- 0.0046
        l_A    = 301.471 +/- 0.090      (Chen, Huang & Wang 2019)
        r_drag = 147.09 Mpc             (Planck 2018 VI, Table 2)

    Why a fixed multiplicative correction is legitimate
    ---------------------------------------------------
    The direct integral of :func:`sound_horizon` uses a two-fluid
    baryon-photon sound speed and the Hu & Sugiyama fit for z_*; it therefore
    misses the ~1% effects that a Boltzmann code includes (finite
    recombination width, the small photon-diffusion/He-recombination
    corrections that shift the effective last-scattering surface).  Those are
    *pre-recombination* effects, and every model considered in this work has
    identical pre-recombination physics -- the activation switch is
    completely closed at a ~ 10^-3.  The mismatch is thus a property of the
    recipe, not of the cosmology, and is removed once and for all by

        KAPPA_RS = r_s^published / r_s^recipe,

    with r_s^published = pi D_M(z_*) / l_A^published evaluated on the same
    fiducial background.  By construction the corrected l_A reproduces
    301.471 exactly at the Planck best fit and scales with the model
    elsewhere.  We quote KAPPA_RS in the paper together with this argument.

    Returns
    -------
    dict with the raw values, the published values, the absolute differences,
    the differences in units of the quoted sigma, and ``kappa_rs``.
    """
    bg = lcdm_background()
    ob, oc = PLANCK18["omega_b"], PLANCK18["omega_c"]
    omega_m = ob + oc + OMEGA_NU0

    zs = z_star(ob, omega_m)
    R_raw, lA_raw = cmb_distance_priors(bg, ob, omega_m, apply_kappa=False)
    rs_raw = sound_horizon(bg, zs, omega_b=ob)
    rd_aub = r_drag(ob, ob + oc, OMEGA_NU0, method="aubourg")
    rd_bri = r_drag(ob, ob + oc, OMEGA_NU0, method="brieden")

    D_M = float(np.atleast_1d(bg.D_M(zs))[0])
    rs_pub = np.pi * D_M / PLANCK18["l_A"]
    kappa = rs_pub / rs_raw

    out = {
        "h": bg.h,
        "z_star": zs,
        "z_star_published": PLANCK18["z_star"],
        "D_M_zstar_Mpc": D_M,
        "R_recipe": R_raw,
        "R_published": PLANCK18["R"],
        "dR": R_raw - PLANCK18["R"],
        "dR_sigma": (R_raw - PLANCK18["R"]) / PLANCK18["R_sigma"],
        "l_A_recipe": lA_raw,
        "l_A_published": PLANCK18["l_A"],
        "dl_A": lA_raw - PLANCK18["l_A"],
        "dl_A_sigma": (lA_raw - PLANCK18["l_A"]) / PLANCK18["l_A_sigma"],
        "r_s_zstar_recipe_Mpc": rs_raw,
        "r_s_zstar_implied_Mpc": rs_pub,
        "kappa_rs": kappa,
        "r_drag_aubourg_Mpc": rd_aub,
        "r_drag_brieden_Mpc": rd_bri,
        "r_drag_published_Mpc": PLANCK18["r_drag"],
        "dr_drag": rd_aub - PLANCK18["r_drag"],
        "dr_drag_frac": rd_aub / PLANCK18["r_drag"] - 1.0,
    }
    if verbose:                                              # pragma: no cover
        print(f"z_*        = {zs:9.3f}   (published {PLANCK18['z_star']:.2f})")
        print(f"R          = {R_raw:9.4f}   dR   = {out['dR']:+.4f} "
              f"= {out['dR_sigma']:+.2f} sigma")
        print(f"l_A        = {lA_raw:9.3f}   dl_A = {out['dl_A']:+.3f} "
              f"= {out['dl_A_sigma']:+.2f} sigma")
        print(f"r_s(z_*)   = {rs_raw:9.3f} Mpc  -> kappa_rs = {kappa:.6f}")
        print(f"r_drag     = {rd_aub:9.3f} Mpc (Aubourg), {rd_bri:9.3f} (Brieden), "
              f"published {PLANCK18['r_drag']:.2f}")
    return out


def kappa_rs() -> float:
    """Fixed multiplicative correction of the integrated sound horizon.

    Computed once on first use from :func:`recipe_offsets`; returns exactly
    1.0 if the raw recipe already reproduces l_A to better than half of the
    quoted sigma (0.045 in l_A), in which case no correction is warranted.
    """
    if "value" not in _KAPPA_CACHE:
        off = recipe_offsets()
        _KAPPA_CACHE["value"] = (
            off["kappa_rs"] if abs(off["dl_A_sigma"]) > 0.5 else 1.0
        )
        _KAPPA_CACHE["raw"] = off["kappa_rs"]
    return _KAPPA_CACHE["value"]


def __getattr__(name: str) -> float:
    """Lazy module-level :data:`KAPPA_RS` (PEP 562).

    Exposed as a constant because it *is* one for the whole analysis, but
    evaluated on first access so that importing this module stays cheap.
    """
    if name == "KAPPA_RS":
        return kappa_rs()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
