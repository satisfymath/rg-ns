"""Figure for the caustic test: scaling of the central density."""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from .style import COLORS, WIDTH_FULL, save_figure

SIMS = Path(__file__).resolve().parents[3] / "results" / "sims"


def _load(tag: str):
    path = SIMS / f"pancake_{tag}.npz"
    return np.load(path) if path.exists() else None


def fig_pancake() -> Path | None:
    """Central precursor density versus distance to the caustic, and the
    converted-fraction profile across the pancake."""
    cases = [("A_none", "no conversion", COLORS["lcdm"], "-"),
             ("B_cosmo", "bounded rate", COLORS["alt"], "--"),
             ("C_collapse_k0p5", r"$\kappa=0.5$", COLORS["warn"], "-."),
             ("C_collapse_k1p5", r"$\kappa=1.5$", COLORS["model"], "-")]
    data = {t: _load(t) for t, *_ in cases}
    if data["A_none"] is None:
        return None

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(WIDTH_FULL, 2.6))

    for tag, label, colour, ls in cases:
        d = data[tag]
        if d is None:
            continue
        s = d["s"]
        y = d["centre_rho_I"]
        m = (s > 0) & (y > 0)
        a1.loglog(s[m], y[m], color=colour, ls=ls, lw=1.5, label=label)
    # reference slopes
    s_ref = np.logspace(-6, -2, 20)
    a1.loglog(s_ref, 3e-3 / s_ref, color=COLORS["grey"], lw=0.8, ls=":")
    a1.text(2e-4, 4e2, r"$s^{-1}$", fontsize=8, color=COLORS["grey"])
    a1.loglog(s_ref, 3e2 * np.sqrt(s_ref), color=COLORS["grey"], lw=0.8, ls=":")
    a1.text(3e-5, 1.0, r"$s^{+1/2}$", fontsize=8, color=COLORS["grey"])
    a1.set_xlabel(r"$s = 1 - D$  (distance to the caustic)")
    a1.set_ylabel(r"$\rho_I$ at the caustic sheet")
    a1.invert_xaxis()
    a1.legend(fontsize=7.5, loc="lower left")

    # Right panel: where the density sits at the final time.  Plotted against
    # the Jacobian rather than the coordinate, because |J| is what measures
    # proximity to the caustic and spans six decades across the sheet.
    for tag, label, colour, ls in cases:
        d = data[tag]
        if d is None:
            continue
        J = np.abs(d["final_J"])
        rho = d["final_rho_I"]
        order = np.argsort(J)
        m = (J[order] > 0) & (rho[order] > 0)
        a2.loglog(J[order][m], rho[order][m], color=colour, ls=ls, lw=1.5,
                  label=label)
    a2.set_xlabel(r"$|J|$  (smaller is nearer the caustic)")
    a2.set_ylabel(r"$\rho_I$ at the final time")
    a2.legend(fontsize=7, loc="lower right")
    fig.tight_layout()
    return save_figure(fig, "pancake")


ALL = (fig_pancake,)
