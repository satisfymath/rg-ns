#!/usr/bin/env python3
"""Zel'dovich pancake experiments: does conversion regularize a caustic?

Writes results/pancake.json (numbers for the manuscript) and
results/sims/pancake_*.npz (curves for the figures).  Deliberately frugal:
each run is O(N) in float64 with no stored history, so the whole suite fits in
tens of megabytes and can share a machine with a long MCMC.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from absorb.pancake import Pancake, PancakeParams          # noqa: E402
from absorb.resources import mem_available_mb, record      # noqa: E402

OUT = ROOT / "results" / "pancake.json"
SIMS = ROOT / "results" / "sims"

#: converged sheet count, from the refinement study (the resolution floor is
#: eps ~ (k dq/2)^2/2, so the exponent is clean while s >> eps)
N_SHEETS = 16384
N_STEPS = 25000
D_END = 1.0 - 1e-6


def fit_exponent(s: np.ndarray, y: np.ndarray, lo: float, hi: float) -> float:
    m = (s > lo) & (s < hi) & (y > 0) & np.isfinite(y)
    if m.sum() < 5:
        return float("nan")
    return float(np.polyfit(np.log(s[m]), np.log(y[m]), 1)[0])


def summarise(r) -> dict:
    s = 1.0 - np.asarray(r.D)
    out = {
        "final_gap": float(s[-1]),
        "centre_rho_I": float(r.centre_rho_I[-1]),
        "centre_rho_D": float(r.centre_rho_D[-1]),
        "centre_V": float(r.centre_V[-1]),
        "centre_f": float(r.centre_f[-1]),
        "centre_theta": float(r.centre_theta[-1]),
        "max_rho_I": float(r.max_rho_I[-1]),
        "max_rho_D": float(r.max_rho_D[-1]),
        "max_abs_theta": float(r.max_abs_theta[-1]),
        "mean_f": float(r.mean_f[-1]),
        "column_rho_I": float(r.column_rho_I[-1]),
        "column_rho_D": float(r.column_rho_D[-1]),
        "integral_V": float(r.integral_V[-1]),
    }
    # mass bookkeeping: dust lost must equal vacuum gained when b = 0
    dust0 = float(r.total_mass[0])
    out["mass_residual"] = abs(
        (float(r.total_mass[-1]) + out["integral_V"]) - dust0) / dust0
    for tag, (lo, hi) in {"far": (1e-3, 1e-2), "near": (1e-5, 1e-4)}.items():
        out[f"exp_rho_I_{tag}"] = fit_exponent(s, np.asarray(r.centre_rho_I), lo, hi)
        out[f"exp_rho_D_{tag}"] = fit_exponent(s, np.asarray(r.centre_rho_D), lo, hi)
    # width of the converted region: fraction of sheets past half conversion
    f_final = r.final["f"]
    out["converted_sheet_fraction"] = float((f_final > 0.5).mean())
    return out


def run(label: str, store_curves: bool = False, **kw) -> dict:
    p = PancakeParams(n_sheets=kw.pop("n_sheets", N_SHEETS),
                      n_steps=kw.pop("n_steps", N_STEPS),
                      d_end=kw.pop("d_end", D_END), **kw)
    r = Pancake(p).run()
    d = summarise(r)
    d["params"] = {k: getattr(p, k) for k in
                   ("rate_mode", "kappa", "b", "gamma0", "alpha", "beta",
                    "tau_M", "n_sheets", "n_steps")}
    if store_curves:
        np.savez(SIMS / f"pancake_{label}.npz",
                 D=r.D, s=1.0 - np.asarray(r.D),
                 centre_rho_I=r.centre_rho_I, centre_rho_D=r.centre_rho_D,
                 centre_V=r.centre_V, centre_f=r.centre_f,
                 max_rho_I=r.max_rho_I, column_rho_I=r.column_rho_I,
                 q=r.q, final_f=r.final["f"], final_rho_I=r.final["rho_I"],
                 final_x=r.final["x"], final_J=r.final["J"])
    return d


def main() -> int:
    SIMS.mkdir(parents=True, exist_ok=True)
    print(f"MemAvailable at start: {mem_available_mb():.0f} MB")
    res: dict[str, dict] = {}

    with record("pancake_suite", f"N={N_SHEETS}, {N_STEPS} graded steps"):
        # A: no absorption; B: the bounded rate of the paper; C: candidates
        res["A_none"] = run("A_none", True, rate_mode="none")
        res["B_cosmo"] = run("B_cosmo", True, rate_mode="cosmo")
        for kappa in (0.5, 1.0, 1.5, 3.0):
            tag = f"C_collapse_k{kappa}".replace(".", "p")
            res[tag] = run(tag, kappa in (0.5, 1.5), rate_mode="collapse",
                           kappa=kappa, b=0.0)
        # branching: does sending the product to defects change anything?
        for b in (0.25, 1.0):
            tag = f"C_collapse_b{b}".replace(".", "p")
            res[tag] = run(tag, False, rate_mode="collapse", kappa=1.5, b=b)
        # memory and reinforcement dependence
        for tau in (0.1, 3.0):
            tag = f"C_tau{tau}".replace(".", "p")
            res[tag] = run(tag, False, rate_mode="collapse", kappa=1.5,
                           b=0.0, tau_M=tau)
        for alpha, beta in ((0.0, 0.0), (4.0, 2.0)):
            tag = f"C_a{alpha}_b{beta}".replace(".", "p")
            res[tag] = run(tag, False, rate_mode="collapse", kappa=1.5, b=0.0,
                           alpha=alpha, beta=beta)

    OUT.write_text(json.dumps(res, indent=2, sort_keys=True))
    print(f"\n{'case':22s} {'centre rho_I':>13} {'exp near':>9} {'centre V':>10} "
          f"{'<f>':>7} {'mass resid':>11}")
    for k, v in res.items():
        print(f"{k:22s} {v['centre_rho_I']:13.4e} {v['exp_rho_I_near']:+9.3f} "
              f"{v['centre_V']:10.4f} {v['mean_f']:7.4f} {v['mass_residual']:11.2e}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
