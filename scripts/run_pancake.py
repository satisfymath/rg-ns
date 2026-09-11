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


def fit_exponent(s: np.ndarray, y: np.ndarray, lo: float,
                 hi: float) -> tuple[float, float]:
    """Power-law exponent over a window, with its least-squares uncertainty.

    The uncertainty is reported because the exponent is quoted in the text and
    a bare number there claims a precision the fit does not establish. It is
    the formal error of the straight-line fit and takes no account of the
    residual curvature, which is why the window is stated alongside it.
    """
    m = (s > lo) & (s < hi) & (y > 0) & np.isfinite(y)
    if m.sum() < 5:
        return float("nan"), float("nan")
    (slope, _), cov = np.polyfit(np.log(s[m]), np.log(y[m]), 1, cov=True)
    return float(slope), float(np.sqrt(cov[0, 0]))


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
    # Conservation.  There is no conserved "dust mass plus vacuum integral":
    # the vacuum is not diluted by the flow, so adding its integral to a
    # comoving dust mass compares quantities carried by different measures.
    # What is exact, per sheet, is the pair of survival identities
    #     rho_I |J| = rho_I(0) (1 - f),     rho_D |J| = b rho_I(0) f,
    # whose sum is the comoving dust (1 - f) + b f.  Those are the residuals
    # reported.  The relative form of the first is dominated by catastrophic
    # cancellation wherever f -> 1, so it is quoted in absolute terms.
    J = np.abs(r.final["J"])
    f = r.final["f"]
    b = r.params.b
    out["survival_residual"] = float(np.max(np.abs(r.final["rho_I"] * J - (1.0 - f))))
    out["defect_residual"] = float(np.max(np.abs(r.final["rho_D"] * J - b * f)))
    out["dust_residual"] = float(np.max(np.abs(
        (r.final["rho_I"] + r.final["rho_D"]) * J - ((1.0 - f) + b * f))))
    for tag, (lo, hi) in {"far": (1e-3, 1e-2), "near": (1e-5, 1e-4)}.items():
        for name, series in (("rho_I", r.centre_rho_I), ("rho_D", r.centre_rho_D)):
            val, err = fit_exponent(s, np.asarray(series), lo, hi)
            out[f"exp_{name}_{tag}"] = val
            out[f"exp_{name}_{tag}_err"] = err
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


def summarise_cases(res: dict[str, dict]) -> dict:
    """Cross-case quantities the manuscript quotes.

    Named differently from :func:`summarise` above, which summarises a single
    run. Both were called ``summarise``, so the second definition shadowed the
    first and every call in :func:`run` reached the wrong one: the script
    raised ``AttributeError`` on its first case and ``make reproduce-core``,
    which runs it, could not complete. The committed ``results/pancake.json``
    predates the collision.

    Computed here rather than read off the table by eye, because the paper's
    rule is that no number in it is typed by hand.  The suppression factor is
    the ratio of central precursor densities between the run with no conversion
    and the run with the bounded rate: the two share an exponent, so the ratio
    is the whole effect of the bounded rate, and it is the quantity
    thm:bounded-rate-obstruction predicts to be finite.
    """
    residuals = [v[k] for v in res.values() if isinstance(v, dict) and "params" in v
                 for k in ("survival_residual", "defect_residual", "dust_residual")]
    return {
        "worst_identity_residual": float(max(residuals)),
        "bounded_suppression": float(res["A_none"]["centre_rho_I"]
                                     / res["B_cosmo"]["centre_rho_I"]),
        "n_cases": sum(1 for v in res.values()
                       if isinstance(v, dict) and "params" in v),
    }


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

    res["summary"] = summarise_cases(res)
    OUT.write_text(json.dumps(res, indent=2, sort_keys=True))
    print(f"\n{'case':22s} {'centre rho_I':>13} {'exp near':>9} {'centre V':>10} "
          f"{'<f>':>7} {'dust resid':>11}")
    for k, v in res.items():
        print(f"{k:22s} {v['centre_rho_I']:13.4e} {v['exp_rho_I_near']:+9.3f} "
              f"{v['centre_V']:10.4f} {v['mean_f']:7.4f} {v['dust_residual']:11.2e}")
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
