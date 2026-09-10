"""Figures built from the stochastic, defect and quantum simulations.

Every panel reads results/sims/*.npz, written by scripts/run_sims.py.  No
figure recomputes physics: if a curve moves, it is because the simulation
changed, not because the plotting code did.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from .style import BAND_ALPHA, COLORS, WIDTH_FULL, WIDTH_HALF, save_figure

SIMS = Path(__file__).resolve().parents[3] / "results" / "sims"


def _load(name: str):
    return np.load(SIMS / name)


# --------------------------------------------------------------------------- #
def fig_gillespie() -> Path:
    """Finite-population runs converging on the deterministic limit.

    The left panel plots the deviation from the limit rather than the fraction
    itself: on the scale of f the four ensembles are indistinguishable from the
    deterministic curve, which is the result, but it makes for a figure in
    which nothing can be seen.
    """
    d = _load("gillespie.npz")
    t, det = d["t"], d["det_f"]
    fig, (ax, axi) = plt.subplots(1, 2, figsize=(WIDTH_FULL, 2.5))

    shades = {100: COLORS["warn"], 1000: COLORS["muted"],
              10000: COLORS["model"], 100000: COLORS["accent"]}
    for N, c in shades.items():
        key = f"f_N{N}"
        if key not in d:
            continue
        f = d[key]
        lo, hi = np.percentile(f - det, [5, 95], axis=0)
        ax.fill_between(t, lo, hi, color=c, alpha=BAND_ALPHA[1], linewidth=0)
        ax.plot(t, f.mean(axis=0) - det, color=c, lw=1.1,
                label=rf"$N=10^{{{int(np.log10(N))}}}$")
    ax.axhline(0.0, color=COLORS["lcdm"], lw=1.4, ls="--")
    ax.set_xlabel(r"$\Gamma_0 t$")
    ax.set_ylabel(r"$f_N - f_{\rm det}$")
    ax.set_xlim(t[0], t[-1])
    ax.legend(loc="lower right", ncol=2, fontsize=7.5)

    # inset: the fraction itself, to show what is being subtracted
    inset = ax.inset_axes([0.60, 0.62, 0.37, 0.34])
    inset.plot(t, det, color=COLORS["lcdm"], lw=1.2)
    inset.set_xticks([0, 2, 4])
    inset.set_yticks([0, 1])
    inset.set_ylabel(r"$f$", fontsize=7, labelpad=1)
    inset.tick_params(labelsize=6)
    inset.grid(False)

    for N, c in shades.items():
        key = f"f_N{N}"
        if key not in d:
            continue
        axi.plot(t, np.sqrt(N) * d[key].std(axis=0), color=c, lw=1.1)
    axi.set_xlabel(r"$\Gamma_0 t$")
    axi.set_ylabel(r"$\sqrt{N}\,\mathrm{std}(f_N)$")
    axi.set_xlim(t[0], t[-1])
    fig.tight_layout()
    return save_figure(fig, "gillespie")


def fig_hysteresis() -> Path:
    """Two histories with the same density and different memory."""
    d = _load("hysteresis.npz")
    t = d["t"]
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(WIDTH_HALF * 1.35, 3.4),
                                 sharex=True,
                                 gridspec_kw=dict(height_ratios=[1.0, 0.8]))
    a1.plot(t, d["f_A"], color=COLORS["model"], lw=1.6, label="history A")
    a1.plot(t, d["f_B"], color=COLORS["alt"], lw=1.6, ls="--", label="history B")
    a1.set_ylabel(r"converted fraction $f$")
    a1.legend(loc="lower right")

    a2.plot(t, d["M_A"], color=COLORS["model"], lw=1.6)
    a2.plot(t, d["M_B"], color=COLORS["alt"], lw=1.6, ls="--")
    a2.set_ylabel(r"memory $M$")
    a2.set_xlabel("time")

    # The two histories are prepared to meet at the first plotted time: the
    # densities agree there exactly, the memories do not.
    a1.plot(t[0], d["f_A"][0], "o", color=COLORS["lcdm"], ms=4.5, zorder=5)
    a1.annotate("prepared to share $f$ here", xy=(t[0], d["f_A"][0]),
                xytext=(0.06, 0.80), textcoords="axes fraction",
                fontsize=7.5, color=COLORS["grey"],
                arrowprops=dict(arrowstyle="->", color=COLORS["grey"], lw=0.7))
    a2.annotate(r"memories differ by $\Delta M$",
                xy=(t[0], 0.5 * (d["M_A"][0] + d["M_B"][0])),
                xytext=(0.10, 0.72), textcoords="axes fraction",
                fontsize=7.5, color=COLORS["grey"],
                arrowprops=dict(arrowstyle="->", color=COLORS["grey"], lw=0.7))
    a1.set_xlim(t[0], t[-1])
    fig.tight_layout()
    return save_figure(fig, "hysteresis")


def fig_skyrmion() -> Path:
    """Solved hedgehog profile against the trial family."""
    d = _load("skyrme_profile.npz")
    x, F = d["x"], d["F"]
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(WIDTH_FULL, 2.4))

    a1.plot(x, F, color=COLORS["model"], lw=1.8, label="solution")
    a1.plot(x, 2.0 * np.arctan(1.0 / np.clip(x, 1e-12, None)),
            color=COLORS["alt"], lw=1.3, ls="--", label=r"trial, $R_s=1$")
    a1.set_xlabel(r"$x = F_* r/\sqrt{\kappa_s}$")
    a1.set_ylabel(r"profile $F(x)$")
    a1.set_xlim(0, 8)
    a1.set_yticks([0, np.pi / 2, np.pi])
    a1.set_yticklabels(["0", r"$\pi/2$", r"$\pi$"])
    a1.legend()

    R = np.linspace(0.35, 3.0, 300)
    a2.plot(R, 6 * np.pi ** 2 * (R + 1.0 / R), color=COLORS["alt"], lw=1.4,
            ls="--", label="trial family")
    a2.axhline(12 * np.pi ** 2, color=COLORS["alt"], lw=0.8, ls=":")
    a2.axhline(103.129108, color=COLORS["model"], lw=1.8, label="solution")
    a2.axhline(6 * np.sqrt(2) * np.pi ** 2, color=COLORS["lcdm"], lw=1.2,
               ls="-.", label="Bogomolny bound")
    a2.set_xlabel(r"trial size $R_s$")
    a2.set_ylabel(r"$E\,/\,F_*\sqrt{\kappa_s}$")
    a2.set_ylim(75, 190)
    a2.legend(loc="upper center", fontsize=7.5)
    fig.tight_layout()
    return save_figure(fig, "skyrmion")


def fig_lindblad() -> Path:
    """Mean-field closure error of the collective Lindblad dynamics."""
    d = _load("lindblad.npz")
    N, err = d["N"], d["error"]
    Nd, errd = d["N_dicke"], d["error_dicke"]
    sl_full = np.polyfit(np.log(N), np.log(err), 1)[0]
    sl_dicke = np.polyfit(np.log(Nd), np.log(errd), 1)[0]
    fig, ax = plt.subplots(figsize=(WIDTH_HALF * 1.35, 2.4))
    ax.loglog(N, err, "o", color=COLORS["model"], ms=4.5,
              label=rf"full Liouvillian, slope ${sl_full:.2f}$")
    ax.loglog(Nd, errd, "s", color=COLORS["alt"], ms=4.0, mfc="none",
              label=rf"Dicke chain, slope ${sl_dicke:.2f}$")
    grid = np.logspace(np.log10(N.min()), np.log10(Nd.max()), 60)
    ax.loglog(grid, errd[0] * (grid / Nd[0]) ** -1.0, color=COLORS["grey"],
              lw=1.0, ls=":", label=r"$N^{-1}$")
    ax.set_xlabel(r"units $N$")
    ax.set_ylabel(r"$\max_t\,|\langle \hat f\rangle - f_{\rm MF}|$")
    ax.legend(fontsize=7.5)
    fig.tight_layout()
    return save_figure(fig, "lindblad")


ALL = (fig_gillespie, fig_hysteresis, fig_skyrmion, fig_lindblad)
