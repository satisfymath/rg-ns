"""One-dimensional Zel'dovich pancake with absorption, in Lagrangian form.

Purpose
-------
The manuscript conjectured that conversion regularizes a caustic and recorded
that the test had not been done.  This module does it.

Why Lagrangian
--------------
A single-stream pressureless fluid ceases to be a solution after shell
crossing, so an Eulerian PDE cannot be continued naively past it.  Following
sheets avoids the issue: the Zel'dovich map

    x(q, t) = q + D(t) S(q),        v = D'(t) S(q)

is a well-defined kinematic map for all t, and each sheet carries its own
densities.  The Eulerian density is then the sum over the streams covering a
point.  What is *not* claimed is that this remains a solution of the
Vlasov--Poisson system after crossing: it is exact kinematics with prescribed
trajectories, which is precisely what is needed to isolate the effect of the
absorption term from the gravitational back-reaction.

The local system carried along each sheet is

    d rho_I/dt = -(Theta + Gamma) rho_I
    d rho_D/dt = -Theta rho_D + b Gamma rho_I
    d V    /dt = (1 - b) Gamma rho_I
    d f    /dt = (1 - f) Gamma
    tau_M dM/dt = f - M

with Theta = d ln|J|/dt evaluated on the sheet, J = 1 + D S'(q).

Memory
------
Everything is O(N) in float64 with in-place updates and no stored history
beyond the requested diagnostics; N = 4096 costs well under a megabyte.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import numpy as np

#: shell crossing of the fiducial profile occurs at D = 1
D_CROSS = 1.0


@dataclass
class PancakeParams:
    """Configuration of a run.

    rate_mode selects which conversion channel is active:
      "none"      no absorption at all (the control);
      "cosmo"     the bounded rate of the paper, Gamma_0 exp(alpha f + beta M);
      "collapse"  the bounded rate plus kappa [-Theta]_+, the candidate
                  compression-driven channel.
    """

    n_sheets: int = 1024
    amplitude: float = 1.0           # A; shell crossing when A D = 1
    k: float = 1.0                   # wavenumber of the perturbation
    rate_mode: Literal["none", "cosmo", "collapse"] = "none"
    gamma0: float = 1.0
    alpha: float = 2.0
    beta: float = 1.0
    tau_M: float = 0.7
    kappa: float = 1.5               # strength of the compression channel
    b: float = 0.0                   # branching into defects
    d_end: float = 0.999             # final growth factor, in units of D_CROSS
    n_steps: int = 20000
    time_grid: Literal["uniform", "graded"] = "graded"
    """A caustic is approached self-similarly, so the natural step variable is
    u = -ln(1 - D): uniform steps in u are geometrically refined steps in D and
    resolve every decade of the approach at the same relative accuracy.  A
    uniform grid would need ~1/s_min steps to reach the same place."""
    seed: int = 20260909

    def __post_init__(self) -> None:
        if self.amplitude <= 0 or self.k <= 0:
            raise ValueError("amplitude and k must be positive")


@dataclass
class PancakeResult:
    """Diagnostics of a run; deliberately small."""

    D: np.ndarray
    max_rho_I: np.ndarray
    centre_rho_I: np.ndarray         # at the sheet that forms the caustic
    centre_rho_D: np.ndarray
    centre_V: np.ndarray
    centre_f: np.ndarray
    centre_theta: np.ndarray
    max_rho_D: np.ndarray
    max_abs_theta: np.ndarray
    mean_f: np.ndarray
    max_V: np.ndarray
    total_mass: np.ndarray           # comoving, should be conserved
    column_rho_I: np.ndarray         # integral of rho_I over x, per period
    column_rho_D: np.ndarray
    integral_V: np.ndarray
    params: PancakeParams
    q: np.ndarray = field(repr=False)
    final: dict[str, np.ndarray] = field(default_factory=dict, repr=False)


class Pancake:
    """Evolve the local sector along Zel'dovich sheets."""

    def __init__(self, p: PancakeParams) -> None:
        self.p = p
        # Lagrangian coordinates over one period, staggered to avoid landing
        # exactly on the caustic centre.
        n = p.n_sheets
        self.q = (np.arange(n, dtype=np.float64) + 0.5) * (2 * np.pi / p.k) / n
        self.S = -p.amplitude * np.sin(p.k * self.q) / p.k
        self.Sp = -p.amplitude * np.cos(p.k * self.q)      # dS/dq
        self.dq = (2 * np.pi / p.k) / n
        #: index of the sheet that forms the caustic (J vanishes first there)
        self._centre = int(np.argmin(self.Sp))

    # -- kinematics ---------------------------------------------------------
    def jacobian(self, D: float) -> np.ndarray:
        return 1.0 + D * self.Sp

    def theta(self, D: float, Ddot: float) -> np.ndarray:
        """Theta = d ln|J|/dt = Ddot S'/J."""
        J = self.jacobian(D)
        return Ddot * self.Sp / J

    def positions(self, D: float) -> np.ndarray:
        return self.q + D * self.S

    # -- rate ---------------------------------------------------------------
    def gamma(self, theta: np.ndarray, f: np.ndarray, M: np.ndarray) -> np.ndarray:
        p = self.p
        if p.rate_mode == "none":
            return np.zeros_like(f)
        g = p.gamma0 * np.exp(p.alpha * f + p.beta * M)
        if p.rate_mode == "collapse":
            g = g + p.kappa * np.maximum(-theta, 0.0)
        return g

    # -- evolution ----------------------------------------------------------
    def run(self) -> PancakeResult:
        p = self.p
        n_out = 200
        # D(t) = t is the simplest growth law; Ddot = 1.  Time and growth
        # factor then coincide, which keeps the scaling analysis transparent.
        if p.time_grid == "uniform":
            D_grid = np.linspace(0.0, p.d_end * D_CROSS, p.n_steps + 1)
        else:
            # uniform in u = -ln(1 - D) over the last decades, preceded by a
            # coarse uniform stretch where nothing is happening
            s_end = 1.0 - p.d_end
            n_coarse = p.n_steps // 5
            coarse = np.linspace(0.0, 0.9, n_coarse, endpoint=False)
            u = np.linspace(-np.log(0.1), -np.log(s_end), p.n_steps - n_coarse + 1)
            D_grid = np.concatenate([coarse, 1.0 - np.exp(-u)])
        Ddot = 1.0

        rho_I = np.ones_like(self.q)
        rho_D = np.zeros_like(self.q)
        V = np.zeros_like(self.q)
        f = np.zeros_like(self.q)
        M = np.zeros_like(self.q)

        out_idx = np.unique(np.linspace(0, p.n_steps, n_out).astype(int))
        rec = {k: [] for k in ("D", "max_rho_I", "centre_rho_I", "centre_rho_D",
                               "centre_V", "centre_f", "centre_theta",
                               "max_rho_D", "max_abs_theta",
                               "mean_f", "max_V", "total_mass",
                               "column_rho_I", "column_rho_D", "integral_V")}

        def deriv(D, rI, rD, Vv, ff, MM):
            th = self.theta(D, Ddot)
            gam = self.gamma(th, ff, MM)
            d_rI = -(th + gam) * rI
            d_rD = -th * rD + p.b * gam * rI
            d_V = (1.0 - p.b) * gam * rI
            d_f = (1.0 - ff) * gam
            d_M = (ff - MM) / p.tau_M
            return d_rI, d_rD, d_V, d_f, d_M

        for i, D in enumerate(D_grid[:-1]):
            dt = D_grid[i + 1] - D_grid[i]
            if i in out_idx:
                self._record(rec, D, Ddot, rho_I, rho_D, V, f)
            # classical RK4 on the five local variables
            k1 = deriv(D, rho_I, rho_D, V, f, M)
            k2 = deriv(D + dt / 2, *(a + dt / 2 * b for a, b in
                                     zip((rho_I, rho_D, V, f, M), k1)))
            k3 = deriv(D + dt / 2, *(a + dt / 2 * b for a, b in
                                     zip((rho_I, rho_D, V, f, M), k2)))
            k4 = deriv(D + dt, *(a + dt * b for a, b in
                                 zip((rho_I, rho_D, V, f, M), k3)))
            for arr, a1, a2, a3, a4 in zip((rho_I, rho_D, V, f, M), k1, k2, k3, k4):
                arr += (dt / 6.0) * (a1 + 2 * a2 + 2 * a3 + a4)
            np.clip(f, 0.0, 1.0, out=f)
            np.clip(M, 0.0, 1.0, out=M)

        self._record(rec, D_grid[-1], Ddot, rho_I, rho_D, V, f)
        arrays = {k: np.asarray(v) for k, v in rec.items()}
        return PancakeResult(
            **arrays, params=p, q=self.q,
            final={"rho_I": rho_I, "rho_D": rho_D, "V": V, "f": f, "M": M,
                   "x": self.positions(D_grid[-1]),
                   "J": self.jacobian(D_grid[-1]),
                   "theta": self.theta(D_grid[-1], Ddot)})

    def _record(self, rec, D, Ddot, rho_I, rho_D, V, f) -> None:
        J = self.jacobian(D)
        th = self.theta(D, Ddot)
        # The sheet that forms the caustic is the one where J first vanishes,
        # i.e. where S' is most negative.  The *global* maximum of rho_I is a
        # different quantity: once the centre is depleted it migrates away from
        # the caustic, so the two must be recorded separately.
        j0 = self._centre
        rec["centre_rho_I"].append(float(rho_I[j0]))
        rec["centre_rho_D"].append(float(rho_D[j0]))
        rec["centre_V"].append(float(V[j0]))
        rec["centre_f"].append(float(f[j0]))
        rec["centre_theta"].append(float(th[j0]))
        # Lagrangian measure: the comoving mass element is uniform in q, so a
        # column density is an integral over q with no Jacobian factor.
        rec["D"].append(D)
        rec["max_rho_I"].append(float(rho_I.max()))
        rec["max_rho_D"].append(float(rho_D.max()))
        rec["max_abs_theta"].append(float(np.abs(th).max()))
        rec["mean_f"].append(float(f.mean()))
        rec["max_V"].append(float(V.max()))
        # total comoving mass of the two dust sectors plus what became vacuum
        rec["total_mass"].append(float(((rho_I + rho_D) * np.abs(J)).sum() * self.dq))
        rec["column_rho_I"].append(float((rho_I * np.abs(J)).sum() * self.dq))
        rec["column_rho_D"].append(float((rho_D * np.abs(J)).sum() * self.dq))
        rec["integral_V"].append(float((V * np.abs(J)).sum() * self.dq))
