"""Background cosmology for self-reinforced geometric absorption.

Model
-----
A pressureless precursor rho_I is irreversibly converted, at rate

    Gamma(f, M) = Gamma_0 exp(alpha f + beta M) S_act(a),

into localized defects rho_D (branching ratio b) and vacuum energy V (p = -V):

    d rho_I/dt + 3 H rho_I = -Gamma rho_I
    d rho_D/dt + 3 H rho_D = +b Gamma rho_I
    d V    /dt             = (1 - b) Gamma rho_I  ==  Q_V        [Track A]
                           - Gamma_down V                        [Track B, optional]
    df/dt = (1 - f) Gamma ,   tau_M dM/dt = f - M .

Baryons and radiation are separately conserved.

Integration strategy
--------------------
The exact survival identities (draft Eqs. 7.2-7.3) let us eliminate rho_I and
rho_D analytically in favour of the converted fraction f, so only the
three-vector (f, M, omega_V) is integrated and the Friedmann constraint is
evaluated in closed form at every step.  Setting ``full_system=True`` instead
integrates all five densities, turning those identities into *checks* on the
numerical solution rather than inputs to it.

Parameters actually sampled (see ``params.py``) are the reduced densities
omega_b, omega_c and omega_V_act, the convertible fraction eps, and the kinetic
parameters; h is a derived quantity, h^2 = E^2(N=0).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, replace
from typing import Literal

import numpy as np
from scipy.integrate import cumulative_simpson, solve_ivp
from scipy.interpolate import CubicSpline

from . import constants as K

ArrayLike = np.ndarray | float


# ---------------------------------------------------------------------------
# Relativistic species
# ---------------------------------------------------------------------------
def _nu_shape(a: ArrayLike) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Massive-neutrino shape function g(y) and its first two N-derivatives.

    With y = m a / (k_B T_nu0) and u = (A y)^p, the Komatsu et al. (2011)
    interpolation is g = (1 + u)^{1/p}.  Since u is a pure power of a,
    du/dN = p u, so both derivatives are closed-form; this keeps the pressure
    (and hence the jerk parameter) analytic rather than finite-differenced.
    """
    a = np.asarray(a, dtype=float)
    y0 = K.SUM_M_NU_EV / K.N_NU_MASSIVE / K.KB_TNU0_EV
    pw = K.NU_FIT_P
    u = (K.NU_FIT_A * y0 * a) ** pw
    one_u = 1.0 + u
    g = one_u ** (1.0 / pw)
    gp = u * one_u ** (1.0 / pw - 1.0)
    gpp = pw * u * one_u ** (1.0 / pw - 1.0) \
        + pw * u ** 2 * (1.0 / pw - 1.0) * one_u ** (1.0 / pw - 2.0)
    return g, gp, gpp


def _nu_C() -> float:
    """Common prefactor of a single neutrino species."""
    return K.NU_PREFACTOR * (K.N_EFF / 3.0) * K.OMEGA_GAMMA


def omega_nu(a: ArrayLike) -> np.ndarray:
    """Reduced density of the neutrino sector at scale factor ``a``.

    One massive eigenstate of mass ``SUM_M_NU_EV`` plus ``3 - N_massive``
    massless ones, each carrying N_eff/3 effective degrees of freedom.
    """
    a = np.asarray(a, dtype=float)
    g, _, _ = _nu_shape(a)
    F = (3 - K.N_NU_MASSIVE) + K.N_NU_MASSIVE * g
    return _nu_C() * a ** -4 * F


def omega_nu_derivs(a: ArrayLike) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return (omega_nu, d omega_nu/dN, d^2 omega_nu/dN^2)."""
    a = np.asarray(a, dtype=float)
    g, gp, gpp = _nu_shape(a)
    C = _nu_C()
    F = (3 - K.N_NU_MASSIVE) + K.N_NU_MASSIVE * g
    Fp = K.N_NU_MASSIVE * gp
    Fpp = K.N_NU_MASSIVE * gpp
    pref = C * a ** -4
    return pref * F, pref * (-4.0 * F + Fp), pref * (16.0 * F - 8.0 * Fp + Fpp)


def pressure_nu(a: ArrayLike) -> tuple[np.ndarray, np.ndarray]:
    """Neutrino pressure and its N-derivative, both in reduced units.

    Uses the exact consequence of separate conservation for a decoupled
    species, d rho/dN = -3 (rho + p), which gives p = -rho - (1/3) d rho/dN.
    This reproduces p = rho/3 in the relativistic limit and p = 0 in the
    non-relativistic one, with no additional fitting function.
    """
    w, wp, wpp = omega_nu_derivs(a)
    return -w - wp / 3.0, -wp - wpp / 3.0


_NU_C = K.NU_PREFACTOR * (K.N_EFF / 3.0) * K.OMEGA_GAMMA
_NU_Y0 = K.SUM_M_NU_EV / K.N_NU_MASSIVE / K.KB_TNU0_EV
_NU_AY = K.NU_FIT_A * _NU_Y0
_NU_NML = 3 - K.N_NU_MASSIVE


def omega_nu_scalar(a: float) -> float:
    """Scalar fast path for :func:`omega_nu`, used inside the ODE right-hand
    side where NumPy's array machinery dominates the cost."""
    u = (_NU_AY * a) ** K.NU_FIT_P
    g = (1.0 + u) ** (1.0 / K.NU_FIT_P)
    return _NU_C * a ** -4 * (_NU_NML + K.N_NU_MASSIVE * g)


def omega_rel(a: ArrayLike) -> np.ndarray:
    """Photons plus neutrinos."""
    return K.OMEGA_GAMMA * np.asarray(a, dtype=float) ** -4 + omega_nu(a)


# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class BackgroundParams:
    """Background parameters.

    omega_b, omega_c   reduced baryon and cold-dark densities *before* activation
                       (omega_c lumps precursor + pre-existing defects)
    omega_V_act        vacuum density before activation
    eps                (1 - b) rho_I,act / omega_c: the convertible fraction of
                       omega_c.  eps = 0 reduces the model to LambdaCDM exactly.
    log10_gamma0       log10 of Gamma_0 / H_100
    alpha_tot          alpha + beta, total reinforcement strength
    r_beta             beta / alpha_tot in [0, 1]; r_beta = 0 is memoryless
    log10_tau          log10 of tau_M H_100
    z_act              activation redshift
    p_act              activation sharpness; p_act > 3 is required for a
                       finite vacuum increment down to a -> 0 (see docs/theory)
    log10_gamma_down   Track B reverse channel V -> defects; None disables it
    switch             'hard' (Heaviside in a) or 'smooth' (a^p / (a^p + a_act^p))
    """

    omega_b: float = 0.02237
    omega_c: float = 0.1200
    omega_V_act: float = 0.30
    eps: float = 0.0
    log10_gamma0: float = 0.0
    alpha_tot: float = 0.0
    r_beta: float = 0.0
    log10_tau: float = -0.5
    z_act: float = 1.0
    p_act: float = 6.0
    log10_gamma_down: float | None = None
    switch: Literal["hard", "smooth"] = "smooth"
    rate_tracks_H: bool = False
    """If True the rate is Gamma = xi H rather than a constant floor, with
    xi = 10**log10_gamma0.  Then df/dN = (1-f) xi S(a) is independent of the
    expansion rate, which is what makes this family analytically solvable
    (draft Sec. 8) and why it is used as the numerical benchmark."""

    # --- derived kinetic quantities -----------------------------------------
    @property
    def gamma0(self) -> float:
        return 10.0 ** self.log10_gamma0

    @property
    def alpha(self) -> float:
        return self.alpha_tot * (1.0 - self.r_beta)

    @property
    def beta(self) -> float:
        return self.alpha_tot * self.r_beta

    @property
    def tau_hat(self) -> float:
        return 10.0 ** self.log10_tau

    @property
    def a_act(self) -> float:
        return 1.0 / (1.0 + self.z_act)

    @property
    def gamma_down(self) -> float:
        return 0.0 if self.log10_gamma_down is None else 10.0 ** self.log10_gamma_down


# ---------------------------------------------------------------------------
# Background solution
# ---------------------------------------------------------------------------
class Background:
    """Solve and interpolate the background history.

    After construction the object exposes E(z), distances, the kinetic
    variables f(z), M(z), the transfer Q_V(z) and the cosmographic parameters
    q(z), j(z).  ``check_identities`` returns the residuals of the exact
    survival/continuity/jerk identities and is used by the test suite.
    """

    #: relative and absolute tolerances of the ODE solver
    RTOL = 1e-9
    ATOL = 1e-12

    def __init__(
        self,
        p: BackgroundParams,
        n_grid: int = 600,
        z_max: float = 3.0e4,
        full_system: bool = False,
    ) -> None:
        self.p = p
        self.full_system = full_system
        self._splines: dict[int, CubicSpline] = {}
        self._z_max = z_max
        self._solve(n_grid, z_max)

    # -- activation switch ---------------------------------------------------
    def _switch(self, a: ArrayLike) -> ArrayLike:
        p = self.p
        if p.eps == 0.0:
            return np.zeros_like(np.asarray(a, dtype=float))
        if p.switch == "hard":
            return (np.asarray(a, dtype=float) >= p.a_act).astype(float)
        ap = np.asarray(a, dtype=float) ** p.p_act
        return ap / (ap + p.a_act ** p.p_act)

    def _gamma(self, a: ArrayLike, f: ArrayLike, M: ArrayLike) -> ArrayLike:
        """Conversion rate in units of H_100."""
        p = self.p
        return p.gamma0 * np.exp(p.alpha * f + p.beta * M) * self._switch(a)

    def _gamma_over_E(self, a: ArrayLike, f: ArrayLike, M: ArrayLike,
                      E: ArrayLike) -> ArrayLike:
        """Gamma/H_100/E, the combination that enters df/dN.

        For the xi-H family this is xi S(a) exp(...) with no explicit E, which
        is the origin of the closed-form solutions of Sec. 8.
        """
        g = self._gamma(a, f, M)
        return g if self.p.rate_tracks_H else g / E

    # -- Friedmann closure ---------------------------------------------------
    def _E2_from_state(self, N: ArrayLike, f: ArrayLike, omega_V: ArrayLike,
                       omega_D_extra: ArrayLike = 0.0) -> ArrayLike:
        """E^2 given the converted fraction and the vacuum density."""
        p = self.p
        a = np.exp(N)
        dust = (p.omega_b + p.omega_c * (1.0 - p.eps * f)) * a ** -3
        dust = dust + np.asarray(omega_D_extra, dtype=float) * a ** -3
        return dust + omega_rel(a) + omega_V

    # -- right-hand side -----------------------------------------------------
    def _rhs(self, N: float, y: np.ndarray) -> np.ndarray:
        """Scalar right-hand side; written with plain floats because the ODE
        solver calls it ~700 times per solve and NumPy scalar overhead would
        otherwise dominate the likelihood evaluation."""
        p = self.p
        f, M, omega_V, omega_D_extra = y
        a = math.exp(N)
        a3 = a ** -3
        dust = (p.omega_b + p.omega_c * (1.0 - p.eps * f) + omega_D_extra) * a3
        E2 = dust + K.OMEGA_GAMMA * a ** -4 + omega_nu_scalar(a) + omega_V
        E = math.sqrt(E2 if E2 > 1e-300 else 1e-300)
        if p.switch == "hard":
            sw = 1.0 if a >= p.a_act else 0.0
        else:
            ap = a ** p.p_act
            sw = ap / (ap + p.a_act ** p.p_act)
        gam = p.gamma0 * math.exp(p.alpha * f + p.beta * M) * sw
        if p.rate_tracks_H:
            gam *= E                      # Gamma = xi H  =>  gamma/E = xi S

        df = (1.0 - f) * gam / E
        dM = (f - M) / (p.tau_hat * E) if p.tau_hat > 0 else 0.0
        # dV/dN = (1-b) rho_I a^-3 df  =  eps omega_c a^-3 df    (Track A)
        dV = p.eps * p.omega_c * a3 * df
        dD = 0.0
        if p.gamma_down > 0.0:                       # Track B reverse channel
            back = p.gamma_down * omega_V / E
            dV -= back
            dD += back / a3                          # comoving defect density
        return np.array([df, dM, dV, dD])

    # -- solve ---------------------------------------------------------------
    def _solve(self, n_grid: int, z_max: float) -> None:
        p = self.p
        N_end = 0.0
        # Before activation the switch is negligible; start the ODE early enough
        # that the neglected tail is far below numerical tolerance.
        # Start early enough that the neglected pre-activation conversion,
        # which scales as S(a) ~ (a/a_act)^p, is below the ODE tolerance.
        N_start = np.log(p.a_act) - 26.0 / max(p.p_act, 1.0) if p.eps > 0 else -1e-8
        N_start = min(N_start, -1e-8)
        N_start = max(N_start, np.log(1.0 / (1.0 + z_max)))

        y0 = np.array([0.0, 0.0, p.omega_V_act, 0.0])
        if p.eps > 0.0:
            sol = solve_ivp(
                self._rhs, (N_start, N_end), y0, method="DOP853",
                rtol=self.RTOL, atol=self.ATOL, dense_output=True,
            )
            if not sol.success:                                   # pragma: no cover
                raise RuntimeError(f"background ODE failed: {sol.message}")
            self._sol = sol
        else:
            self._sol = None

        # Grid: uniform in N = ln a over the full range, with extra refinement
        # after activation (where f and V vary) and at low z (where the
        # distance integrals are most sensitive).
        N_lo = np.log(1.0 / (1.0 + z_max))
        pieces = [np.linspace(N_lo, 0.0, n_grid)]
        if p.eps > 0.0 and N_start > N_lo:
            pieces.append(np.linspace(N_start, 0.0, n_grid // 2))
        pieces.append(np.linspace(np.log(1.0 / 3.0), 0.0, n_grid // 2))
        grid = np.unique(np.concatenate(pieces))
        self.N = grid
        self.a = np.exp(grid)
        self.z = 1.0 / self.a - 1.0

        state = np.zeros((4, grid.size))
        state[2, :] = p.omega_V_act
        if self._sol is not None:
            after = grid >= N_start
            state[:, after] = self._sol.sol(grid[after])
        self.f_grid, self.M_grid, self.V_grid, self.Dx_grid = state
        # Numerical noise can push f a hair outside [0, 1]; clip for safety.
        self.f_grid = np.clip(self.f_grid, 0.0, 1.0)

        self.E_grid = np.sqrt(self._E2_from_state(
            grid, self.f_grid, self.V_grid, self.Dx_grid))
        self.h = float(self.E_grid[-1])

        # Q_V from the ODE right-hand side (no finite differences), vectorised:
        # dV/dN = Q_V / (H_100 E) in reduced units.
        df_dN = (1.0 - self.f_grid) * self._gamma_over_E(
            self.a, self.f_grid, self.M_grid, self.E_grid)
        dV_dN = p.eps * p.omega_c * self.a ** -3 * df_dN
        if p.gamma_down > 0.0:
            dV_dN = dV_dN - p.gamma_down * self.V_grid / self.E_grid
        self.QV_grid = dV_dN * self.E_grid          # Q_V / (3 M_Pl^2 H_100^3)

        self._build_distances()

    # -- distances -----------------------------------------------------------
    def _build_distances(self) -> None:
        """Comoving distance by cumulative Simpson integration in N = ln a.

        With dz = -e^{-N} dN,  D_C(N) = (c/H_100) int_N^0 e^{-N'}/E(N') dN'.
        The cumulative integral runs over the increasing grid and is then
        referenced to its value today.
        """
        integrand = 1.0 / (self.a * self.E_grid)         # e^{-N} / E
        G = cumulative_simpson(integrand, x=self.N, initial=0.0)
        self.DC_grid = (G[-1] - G) * K.HUBBLE_DIST_MPC   # Mpc, zero at z = 0

    # -- public interpolators ------------------------------------------------
    def _interp(self, z: ArrayLike, values: np.ndarray) -> np.ndarray:
        """Cubic interpolation in N = ln a, which is the variable the solution
        is smooth in.  Linear interpolation in z is not accurate enough for the
        distance integrals at the 1e-5 level required by the likelihoods."""
        z = np.atleast_1d(np.asarray(z, dtype=float))
        key = id(values)
        spline = self._splines.get(key)
        if spline is None:
            spline = CubicSpline(self.N, values, extrapolate=True)
            self._splines[key] = spline
        return spline(np.log1p(-z / (1.0 + z)))

    def E(self, z: ArrayLike) -> np.ndarray:
        """H(z)/H_100."""
        return self._interp(z, self.E_grid)

    def H_km_s_Mpc(self, z: ArrayLike) -> np.ndarray:
        return 100.0 * self.E(z)

    def f_conv(self, z: ArrayLike) -> np.ndarray:
        return self._interp(z, self.f_grid)

    def memory(self, z: ArrayLike) -> np.ndarray:
        return self._interp(z, self.M_grid)

    def omega_V(self, z: ArrayLike) -> np.ndarray:
        return self._interp(z, self.V_grid)

    def Q_V(self, z: ArrayLike) -> np.ndarray:
        """Energy transfer rate in units of 3 M_Pl^2 H_100^3."""
        return self._interp(z, self.QV_grid)

    def D_C(self, z: ArrayLike) -> np.ndarray:
        """Line-of-sight comoving distance [Mpc]."""
        return self._interp(z, self.DC_grid)

    # flat universe: transverse comoving distance = line-of-sight
    D_M = D_C

    def D_H(self, z: ArrayLike) -> np.ndarray:
        """Hubble distance c/H(z) [Mpc]."""
        return K.HUBBLE_DIST_MPC / self.E(z)

    def D_V(self, z: ArrayLike) -> np.ndarray:
        """Spherically averaged BAO distance [Mpc]."""
        z = np.atleast_1d(np.asarray(z, dtype=float))
        return np.cbrt(z * self.D_M(z) ** 2 * self.D_H(z))

    def D_L(self, z_hd: ArrayLike, z_hel: ArrayLike | None = None) -> np.ndarray:
        """Luminosity distance [Mpc]; heliocentric z used for the (1+z) factor."""
        z_hel = z_hd if z_hel is None else z_hel
        return (1.0 + np.asarray(z_hel, dtype=float)) * self.D_M(z_hd)

    def distance_modulus(self, z_hd: ArrayLike, z_hel: ArrayLike | None = None):
        return 5.0 * np.log10(self.D_L(z_hd, z_hel)) + 25.0

    # -- cosmography ---------------------------------------------------------
    def _omegas(self, z: ArrayLike) -> tuple[np.ndarray, ...]:
        z = np.atleast_1d(np.asarray(z, dtype=float))
        a = 1.0 / (1.0 + z)
        f = self.f_conv(z)
        V = self.omega_V(z)
        dust = (self.p.omega_b + self.p.omega_c * (1.0 - self.p.eps * f)) * a ** -3
        dust = dust + self._interp(z, self.Dx_grid) * a ** -3
        rad = K.OMEGA_GAMMA * a ** -4
        nu = omega_nu(a)
        return dust, rad, nu, V

    def q(self, z: ArrayLike) -> np.ndarray:
        """Deceleration parameter.

        Neutrinos are treated with their exact pressure via the interpolation
        derivative; at the redshifts probed here they are non-relativistic and
        the correction is at the 1e-4 level.
        """
        zz = np.atleast_1d(np.asarray(z, dtype=float))
        a = 1.0 / (1.0 + zz)
        dust, rad, nu, V = self._omegas(zz)
        E2 = dust + rad + nu + V
        pnu, _ = pressure_nu(a)
        p_tot = rad / 3.0 + pnu - V
        return 0.5 * (E2 + 3.0 * p_tot) / E2

    def j(self, z: ArrayLike) -> np.ndarray:
        """Jerk parameter, from the exact identity j = 1 - p'_tot/(2 Mpl^2 H^3).

        In reduced units this is j = 1 - (3/2) (dp/dN) / E^2 with
        p = omega_gamma a^-4/3 + p_nu - V, so

            j = 1 + 2 Omega_gamma - (3/2) p'_nu / E^2 + (3/2) Q_V / E^3,

        which is the draft's Eq. (9.3) with the massive-neutrino pressure
        restored.  For Q_V >= 0 the last term is non-negative: this is the
        content of the jerk bound.
        """
        zz = np.atleast_1d(np.asarray(z, dtype=float))
        a = 1.0 / (1.0 + zz)
        dust, rad, nu, V = self._omegas(zz)
        E2 = dust + rad + nu + V
        _, pnu_p = pressure_nu(a)
        QV = self.Q_V(zz)
        return 1.0 + 2.0 * rad / E2 - 1.5 * pnu_p / E2 + 1.5 * QV / E2 ** 1.5

    def snap(self, z: ArrayLike) -> np.ndarray:
        """Snap parameter, s = dj/dN - j(2 + 3q).

        Computed from a spline of j on the solution grid rather than from a
        closed form, so that it tests the analytic expression in the paper
        instead of restating it.
        """
        zz = np.atleast_1d(np.asarray(z, dtype=float))
        m = (self.z < 60.0) & (self.z > 1e-4)
        Ng, jg = self.N[m], self.j(self.z[m])
        order = np.argsort(Ng)
        spline = CubicSpline(Ng[order], jg[order])
        Nq = np.log(1.0 / (1.0 + zz))
        return spline(Nq, 1) - self.j(zz) * (2.0 + 3.0 * self.q(zz))

    def snap_excess_analytic(self, z: ArrayLike) -> np.ndarray:
        """The model's closed form for s - s_LambdaCDM(q).

        With epsilon = Q_V/(2 Mpl^2 H^3) the general result is
        eps * [dlnGamma/dN - Gamma/H - 2].  For the rate law used here,

            dlnGamma/dN = alpha (1-f) Gamma/H + beta (f-M)/(tau_M H)
                          + p (1 - S_act(a)),

        the last term coming from the activation switch.  Dropping it changes
        the sign of the bracket once the switch is still opening, which is
        exactly where the effect is largest.
        """
        zz = np.atleast_1d(np.asarray(z, dtype=float))
        a = 1.0 / (1.0 + zz)
        p = self.p
        E = self.E(zz)
        f, M = self.f_conv(zz), self.memory(zz)
        gamma_over_H = self._gamma_over_E(a, f, M, E)
        eps = 1.5 * self.Q_V(zz) / E ** 3
        S = np.asarray(self._switch(a), dtype=float)
        dlnGamma = (p.alpha * (1.0 - f) * gamma_over_H
                    + p.beta * (f - M) / (p.tau_hat * E)
                    + p.p_act * (1.0 - S))
        if p.rate_tracks_H:
            dlnGamma = dlnGamma - (1.0 + self.q(zz))
        return eps * (dlnGamma - gamma_over_H - 2.0)

    def snap_lambda_cdm(self, z: ArrayLike) -> np.ndarray:
        """s for the same q with no transfer, i.e. the reference the excess is
        measured against."""
        return self.snap(z) - self.snap_excess_analytic(z)

    def jerk_lambda_cdm_bound(self, z: ArrayLike) -> np.ndarray:
        """The bound 1 + 2 Omega_gamma - (3/2) p'_nu/E^2 that j must exceed
        whenever the transfer to the vacuum is non-negative."""
        zz = np.atleast_1d(np.asarray(z, dtype=float))
        a = 1.0 / (1.0 + zz)
        dust, rad, nu, V = self._omegas(zz)
        E2 = dust + rad + nu + V
        _, pnu_p = pressure_nu(a)
        return 1.0 + 2.0 * rad / E2 - 1.5 * pnu_p / E2

    def w_V_eff(self, z: ArrayLike) -> np.ndarray:
        """Bookkeeping equation of state of the vacuum.

        Defined by dV/dt + 3H(1 + w_eff) V = 0, i.e. w_eff = -1 - Q_V/(3 H V).
        In reduced units H -> E, so w_eff = -1 - Q_V/(3 E V).  This is a
        *counting* quantity: the physical vacuum stress tensor still has
        p_V = -V exactly (draft Sec. 7.7).
        """
        V = self.omega_V(z)
        E = self.E(z)
        return -1.0 - self.Q_V(z) / (3.0 * E * V)

    def w_dark_eff(self, z: ArrayLike) -> np.ndarray:
        """Equation of state an observer would infer for a *conserved* dark
        sector, i.e. attributing all of Q_V to an effective dark-energy fluid
        while holding the matter density fixed at its present value."""
        dust, rad, nu, V = self._omegas(z)
        zz = np.atleast_1d(np.asarray(z, dtype=float))
        a = 1.0 / (1.0 + zz)
        dust0 = float(self._omegas(0.0)[0][0])
        rho_de = dust + V - dust0 * a ** -3
        p_de = -V
        return p_de / rho_de

    def transfer_q(self) -> np.ndarray:
        """The reduced transfer q(N) = Q_V / (3 Mpl^2 H0^2 H) on the solver grid.

        This is the quantity the deficit bound places its hypothesis on: the
        deficit is ``Delta = int q e^{3N} dN`` and the jerk excess is
        ``eps_0 = (3/2) q_0``, both to the accuracy of the massive-neutrino
        pressure term.
        """
        return self.QV_grid / self.E_grid / self.E_grid[-1] ** 2

    def transfer_diagnostics(self, z_max: float = 3.0) -> dict:
        """Whether the deficit bound's hypothesis holds, and where q peaks.

        The bound ``j_0 - 1 >= 2 Omega_r0 + (9/2) Delta`` needs q to be
        non-decreasing up to today.  For the activation law of this model it is
        not: the switch turns the transfer on at ``z_act`` and the rate then
        falls relative to the expansion, so q peaks at the activation redshift
        and declines from there.  The bound is therefore unavailable here, and
        the jerk excess has to be computed rather than inferred.
        """
        q = self.transfer_q()
        sel = self.N > np.log(1.0 / (1.0 + z_max))
        qs = q[sel]
        scale = max(float(np.max(np.abs(qs))), 1e-300)
        peak = int(np.argmax(q))
        return {
            "q_nondecreasing": bool(np.all(np.diff(qs) >= -1e-9 * scale)),
            "z_of_peak": float(np.expm1(-self.N[peak])),
            "q0": float(q[-1]),
        }

    def derived(self) -> dict[str, float]:
        """Summary quantities quoted in the paper."""
        E0 = self.h
        dust, rad, nu, V = (float(x[0]) for x in self._omegas(0.0))
        f0 = float(self.f_conv(0.0)[0])
        out = {
            "h": E0,
            "H0": 100.0 * E0,
            "Omega_m0": (dust + nu) / E0 ** 2,
            "Omega_V0": V / E0 ** 2,
            "Omega_r0": rad / E0 ** 2,
            "f0": f0,
            "M0": float(self.memory(0.0)[0]),
            "q0": float(self.q(0.0)[0]),
            "j0": float(self.j(0.0)[0]),
            # Comoving dust density before and after activation.  The
            # neutrino contribution is the same at both ends and is excluded,
            # so that the deficit is exactly the transferred amount and
            # vanishes identically when eps = 0.
            "omega_m_today": dust,
            "omega_m_early": self.p.omega_b + self.p.omega_c,
            "V0_minus_Vact": float(self.V_grid[-1] - self.p.omega_V_act),
        }
        # Delta = (rho_m^early - rho_m0)/rho_crit,0 = eps omega_c f0 / E0^2,
        # the single number that sets the width of the sandwich bound.
        out["matter_deficit"] = (out["omega_m_early"] - out["omega_m_today"]) / E0 ** 2
        # The model's contribution to the jerk, eps_0 = Q_V / (2 Mpl^2 H^3),
        # computed directly rather than inferred from the deficit, because the
        # inequality relating them is a floor whose hypothesis this model's
        # activation law does not satisfy; see transfer_diagnostics.
        #
        # This is the transfer term alone, not j0 - 1 - 2 Omega_r0.  The latter
        # also contains the massive-neutrino pressure term, which LambdaCDM has
        # too and which is therefore not a signature of anything: with it
        # included the quantity cannot reach zero even at zero conversion,
        # where it equals 4.9e-5, so a profile in it has no null point and its
        # limit is a limit on the wrong thing.
        out["jerk_excess"] = 1.5 * float(self.Q_V(0.0)[0]) / E0 ** 3
        out["jerk_neutrino_term"] = (out["j0"] - 1.0 - 2.0 * out["Omega_r0"]
                                     - out["jerk_excess"])
        # acceleration onset
        qz = self.q(self.z)
        sign = np.sign(qz)
        idx = np.flatnonzero(np.diff(sign) != 0)
        out["z_acc"] = float(self.z[idx[-1]]) if idx.size else float("nan")
        # half-conversion redshift
        if f0 > 0.5:
            out["z_half"] = float(np.interp(0.5, self.f_grid, self.z))
        else:
            out["z_half"] = float("nan")
        return out

    # -- consistency checks --------------------------------------------------
    def E2_derivatives(self, z: ArrayLike) -> tuple[np.ndarray, ...]:
        """Return (E^2, dE^2/dN, d^2E^2/dN^2) analytically.

        The transfer terms cancel identically between the dust and vacuum
        sectors, leaving the total continuity equation

            dE^2/dN = -3 (dust) - 4 omega_gamma a^-4 + d omega_nu/dN,

        which is Eq. (7.6) of the draft.  Verifying that the *integrated*
        solution obeys this is an independent check on the numerics.
        """
        zz = np.atleast_1d(np.asarray(z, dtype=float))
        a = 1.0 / (1.0 + zz)
        p = self.p
        f = self.f_conv(zz)
        Dx = self._interp(zz, self.Dx_grid)
        dust = (p.omega_b + p.omega_c * (1.0 - p.eps * f) + Dx) * a ** -3
        gam_a = K.OMEGA_GAMMA * a ** -4
        wnu, wnu_p, wnu_pp = omega_nu_derivs(a)
        V = self.omega_V(zz)

        E2 = dust + gam_a + wnu + V
        E = np.sqrt(E2)
        # f' and Dx' from the ODE right-hand side (no finite differences)
        Mm = self.memory(zz)
        fp = (1.0 - f) * self._gamma_over_E(a, f, Mm, E)
        Dxp = np.zeros_like(fp)
        if p.gamma_down > 0.0:
            Dxp = p.gamma_down * V / E * a ** 3

        dE2 = -3.0 * dust - 4.0 * gam_a + wnu_p
        d_dust = -3.0 * dust + a ** -3 * (-p.omega_c * p.eps * fp + Dxp)
        d2E2 = -3.0 * d_dust + 16.0 * gam_a + wnu_pp
        return E2, dE2, d2E2

    def j_from_expansion(self, z: ArrayLike) -> np.ndarray:
        """Jerk from derivatives of E, j = 1 + 3E'/E + (E'^2 + E E'')/E^2.

        Independent of :meth:`j`, which uses the total-pressure identity.
        Agreement of the two is a genuine test, not a tautology.
        """
        E2, dE2, d2E2 = self.E2_derivatives(z)
        E = np.sqrt(E2)
        Ep = dE2 / (2.0 * E)
        Epp = (d2E2 - 2.0 * Ep ** 2) / (2.0 * E)
        return 1.0 + 3.0 * Ep / E + (Ep ** 2 + E * Epp) / E2

    def solve_full_system(self, n_eval: int = 400) -> dict[str, np.ndarray]:
        """Integrate all five densities separately, without using the exact
        survival identities.  Used only to *test* Eqs. (7.2)-(7.3); the main
        solver eliminates rho_I and rho_D analytically.
        """
        p = self.p
        N0 = float(self.N[0])
        a0 = np.exp(N0)
        # split omega_c into precursor and pre-existing defects using eps and b;
        # with b = 0 the convertible part is exactly eps * omega_c
        rho_I0 = p.eps * p.omega_c
        rho_D0 = p.omega_c - rho_I0
        y0 = np.array([rho_I0 * a0 ** -3, rho_D0 * a0 ** -3,
                       p.omega_V_act, p.omega_b * a0 ** -3,
                       float(K.OMEGA_GAMMA * a0 ** -4), 0.0, 0.0])

        # b = 0 branch: all converted energy goes to the vacuum
        def rhs_b0(N, y):
            rI, rD, V, rb, rr, f, M = y
            a = np.exp(N)
            E = np.sqrt(max(rI + rD + V + rb + rr + float(omega_nu(a)), 1e-300))
            g_over_E = float(self._gamma_over_E(a, f, M, E))
            return np.array([-3.0 * rI - g_over_E * rI,
                             -3.0 * rD,
                             g_over_E * rI,
                             -3.0 * rb,
                             -4.0 * rr,
                             (1.0 - f) * g_over_E,
                             (f - M) / (p.tau_hat * E)])

        sol = solve_ivp(rhs_b0, (N0, 0.0), y0, method="DOP853",
                        rtol=1e-11, atol=1e-14, dense_output=True, max_step=0.05)
        if not sol.success:                                       # pragma: no cover
            raise RuntimeError(sol.message)
        Ns = np.linspace(N0, 0.0, n_eval)
        rI, rD, V, rb, rr, f, M = sol.sol(Ns)
        return {"N": Ns, "rho_I": rI, "rho_D": rD, "V": V, "rho_b": rb,
                "rho_r": rr, "f": f, "M": M}

    def check_identities(self) -> dict[str, float]:
        """Relative residuals of the exact identities.  All should be at the
        level of the ODE tolerance; the test suite asserts this."""
        p = self.p
        res: dict[str, float] = {}

        # (i) Friedmann closure actually used by the solver
        E2 = self._E2_from_state(self.N, self.f_grid, self.V_grid, self.Dx_grid)
        res["friedmann"] = float(np.max(np.abs(self.E_grid ** 2 - E2) / E2))

        # (ii) total continuity: dE^2/dN from the solution vs the analytic form
        zc = self.z[(self.z < 30.0) & (self.z > 1e-3)]
        E2c, dE2c, _ = self.E2_derivatives(zc)
        spline = CubicSpline(self.N, self.E_grid ** 2)
        dE2_num = spline(np.log(1.0 / (1.0 + zc)), 1)
        res["continuity"] = float(np.max(np.abs(dE2_num - dE2c) / np.abs(E2c)))

        # (iii) jerk: pressure identity vs expansion derivatives
        m = (self.z < 10.0) & (self.z > 1e-3)
        zj = self.z[m]
        res["jerk"] = float(np.max(np.abs(self.j(zj) - self.j_from_expansion(zj))))

        # (iv) survival and product identities against the full system (b = 0)
        if p.eps > 0.0 and p.gamma_down == 0.0:
            full = self.solve_full_system()
            a = np.exp(full["N"])
            rho_I0 = p.eps * p.omega_c
            surv = full["rho_I"] * a ** 3 - rho_I0 * (1.0 - full["f"])
            res["survival"] = float(np.max(np.abs(surv)) / max(rho_I0, 1e-30))
            Vs = CubicSpline(self.N, self.V_grid)(full["N"])
            fs = CubicSpline(self.N, self.f_grid)(full["N"])
            res["vacuum_vs_full"] = float(np.max(np.abs(full["V"] - Vs)))
            res["f_vs_full"] = float(np.max(np.abs(full["f"] - fs)))
        return res


def lcdm(omega_b: float = 0.02237, omega_c: float = 0.1200,
         omega_L: float = 0.3, **kw) -> Background:
    """Convenience constructor for the LambdaCDM limit (eps = 0)."""
    return Background(BackgroundParams(
        omega_b=omega_b, omega_c=omega_c, omega_V_act=omega_L, eps=0.0, **kw))
