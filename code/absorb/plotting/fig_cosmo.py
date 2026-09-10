"""Figures of the background cosmology and its confrontation with data.

Posterior bands are built by sampling the stored chains, not by propagating
errors linearly: the model is nonlinear in its parameters and the derived
quantities are strongly non-Gaussian.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from ..background import Background, BackgroundParams
from ..data import cc as cc_data
from ..data import desi as desi_data
from ..params import MODELS
from .style import BAND_ALPHA, COLORS, WIDTH_FULL, WIDTH_HALF, save_figure

ROOT = Path(__file__).resolve().parents[3]
CHAINS = ROOT / "results" / "chains"
N_BAND = 300          # posterior draws used per band


def _chain(model: str, dataset: str = "baseline") -> np.ndarray | None:
    """Flattened chain, or None if it has not been run."""
    import h5py
    path = CHAINS / f"{model}_{dataset}.h5"
    if not path.exists():
        return None
    with h5py.File(path, "r") as fh:
        it = int(fh["mcmc"].attrs["iteration"])
        if it < 200:
            return None
        chain = fh["mcmc"]["chain"][: it]
    return chain[it // 3:].reshape(-1, chain.shape[-1])


def _backgrounds(model: str, n: int = N_BAND, seed: int = 0):
    flat = _chain(model)
    if flat is None:
        return []
    rng = np.random.default_rng(seed)
    idx = rng.choice(len(flat), size=min(n, len(flat)), replace=False)
    m = MODELS[model]
    out = []
    for theta in flat[idx]:
        try:
            out.append(m.builder(m.to_dict(theta[:m.ndim])))
        except Exception:                                      # noqa: BLE001
            continue
    return out


def _band(ax, z, curves, color, label=None, ls="-"):
    """68 and 95 per cent posterior bands plus the median."""
    arr = np.asarray(curves)
    for lev, alpha in zip((95, 68), BAND_ALPHA[::-1]):
        lo, hi = np.percentile(arr, [50 - lev / 2, 50 + lev / 2], axis=0)
        ax.fill_between(z, lo, hi, color=color, alpha=alpha, linewidth=0)
    ax.plot(z, np.median(arr, axis=0), color=color, lw=1.6, ls=ls, label=label)


# --------------------------------------------------------------------------- #
def fig_background(model: str = "memory") -> Path | None:
    """Densities, converted fraction, memory and deceleration."""
    bgs = _backgrounds(model)
    if not bgs:
        return None
    z = np.linspace(0.0, 6.0, 200)
    fig, axes = plt.subplots(2, 2, figsize=(WIDTH_FULL, 4.0), sharex=True)

    _band(axes[0, 0], z, [b.f_conv(z) for b in bgs], COLORS["model"],
          r"$f$")
    _band(axes[0, 0], z, [b.memory(z) for b in bgs], COLORS["accent"],
          r"$M$", ls="--")
    axes[0, 0].set_ylabel("converted fraction, memory")
    axes[0, 0].legend(loc="upper right")

    _band(axes[0, 1], z, [b.omega_V(z) / b.E(z) ** 2 for b in bgs],
          COLORS["model"], r"$\Omega_V$")
    _band(axes[0, 1], z,
          [(b._omegas(z)[0] + b._omegas(z)[2]) / b.E(z) ** 2 for b in bgs],
          COLORS["alt"], r"$\Omega_{\rm m}$", ls="--")
    axes[0, 1].set_ylabel("density parameters")
    axes[0, 1].legend(loc="center right")

    _band(axes[1, 0], z, [b.Q_V(z) / b.E(z) ** 3 for b in bgs], COLORS["model"])
    axes[1, 0].set_ylabel(r"$Q_V/(3M_{\rm Pl}^2H^3)$")
    axes[1, 0].set_xlabel(r"redshift $z$")

    _band(axes[1, 1], z, [b.q(z) for b in bgs], COLORS["model"], "model")
    lcdm = _backgrounds("lcdm")
    if lcdm:
        _band(axes[1, 1], z, [b.q(z) for b in lcdm], COLORS["lcdm"],
              r"$\Lambda$CDM", ls=":")
    axes[1, 1].axhline(0.0, color=COLORS["grey"], lw=0.7)
    axes[1, 1].set_ylabel(r"deceleration $q(z)$")
    axes[1, 1].set_xlabel(r"redshift $z$")
    axes[1, 1].legend(loc="lower right")
    for ax in axes.flat:
        ax.set_xlim(0, 6)
    fig.tight_layout()
    return save_figure(fig, "background")


def fig_hubble() -> Path | None:
    """H(z) against the cosmic chronometers, as a ratio to LambdaCDM."""
    bgs, ref = _backgrounds("memory"), _backgrounds("lcdm")
    if not bgs or not ref:
        return None
    d = cc_data.load_cc()
    z = np.linspace(0.0, 2.2, 200)
    ref_med = np.median([b.H_km_s_Mpc(z) for b in ref], axis=0)
    ref_at_data = np.median([b.H_km_s_Mpc(d.z) for b in ref], axis=0)

    fig, ax = plt.subplots(figsize=(WIDTH_FULL * 0.72, 2.6))
    _band(ax, z, [b.H_km_s_Mpc(z) / ref_med for b in bgs], COLORS["model"],
          "model")
    _band(ax, z, [b.H_km_s_Mpc(z) / ref_med for b in ref], COLORS["lcdm"],
          r"$\Lambda$CDM", ls=":")
    err = np.sqrt(np.diag(d.cov))
    ax.errorbar(d.z, d.Hz / ref_at_data, yerr=err / ref_at_data, fmt="o",
                color=COLORS["data"], ms=3.5, lw=1.0, label="cosmic chronometers")
    ax.set_xlabel(r"redshift $z$")
    ax.set_ylabel(r"$H(z)\,/\,H_{\Lambda\rm CDM}(z)$")
    ax.set_xlim(0, 2.2)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    return save_figure(fig, "hubble")


def fig_bao() -> Path | None:
    """DESI DR2 distance ratios relative to the LambdaCDM best fit."""
    from ..early import r_drag
    bgs, ref = _backgrounds("memory"), _backgrounds("lcdm")
    if not bgs or not ref:
        return None
    d = desi_data.load_desi()
    z = np.linspace(0.15, 2.5, 200)

    def ratio(b, zz, kind):
        rd = r_drag(b.p.omega_b, b.p.omega_b + b.p.omega_c)
        return {"DM": b.D_M(zz), "DH": b.D_H(zz)}[kind] / rd

    fig, axes = plt.subplots(1, 2, figsize=(WIDTH_FULL, 2.5), sharex=True)
    for ax, kind, lab in zip(axes, ("DM", "DH"),
                             (r"$D_M/r_{\rm d}$", r"$D_H/r_{\rm d}$")):
        base = np.median([ratio(b, z, kind) for b in ref], axis=0)
        _band(ax, z, [ratio(b, z, kind) / base for b in bgs], COLORS["model"],
              "model")
        _band(ax, z, [ratio(b, z, kind) / base for b in ref], COLORS["lcdm"],
              r"$\Lambda$CDM", ls=":")
        sel = d.quantity == f"{kind}_over_rs"
        if sel.any():
            base_at = np.median([ratio(b, d.z[sel], kind) for b in ref], axis=0)
            err = np.sqrt(np.diag(d.cov))[sel]
            ax.errorbar(d.z[sel], d.value[sel] / base_at, yerr=err / base_at,
                        fmt="s", color=COLORS["data"], ms=3.5, lw=1.0,
                        label="DESI DR2")
        ax.set_xlabel(r"redshift $z$")
        ax.set_ylabel(lab + r" (ratio to $\Lambda$CDM)")
        ax.set_xlim(0.15, 2.5)
    axes[0].legend(loc="lower left", fontsize=8)
    fig.tight_layout()
    return save_figure(fig, "bao")


def fig_jerk() -> Path | None:
    """The jerk bound: j(z) posterior against 1 + 2 Omega_r."""
    bgs = _backgrounds("memory")
    if not bgs:
        return None
    z = np.linspace(0.0, 3.0, 200)
    fig, ax = plt.subplots(figsize=(WIDTH_HALF * 1.4, 2.5))
    _band(ax, z, [b.j(z) for b in bgs], COLORS["model"], "model")
    ax.plot(z, np.median([b.jerk_lambda_cdm_bound(z) for b in bgs], axis=0),
            color=COLORS["lcdm"], lw=1.4, ls="--",
            label=r"bound $1+2\Omega_\gamma-\tfrac32 p'_\nu/E^2$")
    ax.set_xlabel(r"redshift $z$")
    ax.set_ylabel(r"jerk $j(z)$")
    ax.set_xlim(0, 3)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    return save_figure(fig, "jerk")


ALL = (fig_background, fig_hubble, fig_bao, fig_jerk)
