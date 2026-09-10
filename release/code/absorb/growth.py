"""Linear growth of matter perturbations with transfer to the vacuum.

In the geodesic realization of the interacting vacuum the integrability
condition forces the vacuum to be unperturbed on comoving hypersurfaces,
delta V_com = delta Q_com = 0.  Summing the continuity equations of all
pressureless species then gives a closed pair for the *total* dust contrast,

    d(delta_m)/dt = -theta + g_c delta_m ,
    d(theta)/dt + 2 H theta = -rho_m delta_m / (2 Mpl^2) ,      g_c = Q_V/rho_m,

in which the branching ratio b cancels identically: b is not observable in
linear theory.  Eliminating theta and changing to N = ln a,

    delta'' + (2 + E'/E - g_c/E) delta'
            - [ (3/2) Omega_m + (g_c/E)' + (2 + E'/E)(g_c/E) ] delta = 0 ,

with primes denoting d/dN and g_c/E = omega_V' / omega_m in reduced units.
Setting g_c = 0 recovers the standard growth equation.

Redshift-space distortions measure the velocity divergence, not the density
growth rate, so the observable is

    f_RSD = -theta/(H delta_m) = f_growth - g_c/H ,

which is what :func:`f_sigma8` returns.
"""
from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline

from .background import Background

Z_INIT = 100.0          # deep in matter domination, well after activation onset


class Growth:
    """Solve the linear growth equation for a given background."""

    def __init__(self, bg: Background, z_init: float = Z_INIT,
                 n_out: int = 600) -> None:
        self.bg = bg
        self.z_init = z_init
        self._solve(n_out)

    # -- coefficients --------------------------------------------------------
    def _coeffs(self, N: np.ndarray):
        """Return (E'/E, Omega_m, gc, gc') on a grid of N."""
        bg = self.bg
        a = np.exp(N)
        z = 1.0 / a - 1.0
        E2, dE2, _ = bg.E2_derivatives(z)
        E = np.sqrt(E2)
        EpoverE = dE2 / (2.0 * E2)
        dust, rad, nu, V = bg._omegas(z)
        # Massive neutrinos are counted with the clustering matter.  They are
        # not sourced by the transfer, so including them in the denominator of
        # g_c slightly dilutes it; at the redshifts probed here they are half a
        # per cent of the matter budget and the effect on g_c is 0.5%, well
        # below the precision of the growth data.  Treating them as fully
        # clustering also overstates their contribution on small scales, which
        # a Boltzmann treatment would resolve.
        omega_m = dust + nu
        Omega_m = omega_m / E2
        # g_c/E = omega_V' / omega_m, with omega_V' = Q_V/E
        gc = (bg.Q_V(z) / E) / omega_m
        return EpoverE, Omega_m, gc

    def _solve(self, n_out: int) -> None:
        N_i = np.log(1.0 / (1.0 + self.z_init))
        grid = np.linspace(N_i, 0.0, n_out)
        # pre-tabulate coefficients and spline them, so the RHS is cheap and
        # gc' is analytic rather than finite-differenced inside the solver
        EpoverE, Omega_m, gc = self._coeffs(grid)
        s_Ep = CubicSpline(grid, EpoverE)
        s_Om = CubicSpline(grid, Omega_m)
        s_gc = CubicSpline(grid, gc)

        def rhs(N, y):
            d, dp = y
            Ep = float(s_Ep(N))
            Om = float(s_Om(N))
            g = float(s_gc(N))
            gp = float(s_gc(N, 1))
            ddp = -(2.0 + Ep - g) * dp + (1.5 * Om + gp + (2.0 + Ep) * g) * d
            return [dp, ddp]

        # growing mode in matter domination: delta ~ a, so delta' = delta
        sol = solve_ivp(rhs, (N_i, 0.0), [np.exp(N_i), np.exp(N_i)],
                        method="DOP853", rtol=1e-9, atol=1e-12,
                        dense_output=True, t_eval=grid)
        if not sol.success:                                       # pragma: no cover
            raise RuntimeError(f"growth ODE failed: {sol.message}")
        self.N = grid
        self.z = 1.0 / np.exp(grid) - 1.0
        self.delta, self.delta_p = sol.y
        self.gc = gc
        self._s_delta = CubicSpline(grid, self.delta)
        self._s_deltap = CubicSpline(grid, self.delta_p)
        self._s_gc = CubicSpline(grid, gc)

    # -- observables ---------------------------------------------------------
    def _N_of_z(self, z):
        z = np.atleast_1d(np.asarray(z, dtype=float))
        return np.log(1.0 / (1.0 + z))

    def D(self, z) -> np.ndarray:
        """Growth factor normalized to unity today."""
        return self._s_delta(self._N_of_z(z)) / float(self._s_delta(0.0))

    def f_growth(self, z) -> np.ndarray:
        """d ln delta_m / d ln a."""
        N = self._N_of_z(z)
        return self._s_deltap(N) / self._s_delta(N)

    def f_rsd(self, z) -> np.ndarray:
        """The growth rate actually probed by redshift-space distortions.

        Equals ``f_growth`` minus Q_V/(H rho_m); the two differ precisely
        because the dust is being sourced.
        """
        N = self._N_of_z(z)
        return self.f_growth(z) - self._s_gc(N)

    def f_sigma8(self, z, sigma8_0: float) -> np.ndarray:
        """f sigma_8 (z) with sigma_8 normalized today."""
        return self.f_rsd(z) * sigma8_0 * self.D(z)

    def growth_index(self, z=0.0) -> np.ndarray:
        """Effective index gamma in f = Omega_m^gamma (LambdaCDM: ~0.55)."""
        zz = np.atleast_1d(np.asarray(z, dtype=float))
        _, Om, _ = self._coeffs(self._N_of_z(zz))
        return np.log(self.f_growth(zz)) / np.log(Om)
