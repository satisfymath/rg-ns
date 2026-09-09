#!/usr/bin/env python3
"""Run the posterior sampling for one or more models and data combinations.

Results are appended to results/results.json, which is the single source of
truth for every number quoted in the paper.

    python scripts/run_mcmc.py --models lcdm --data baseline
    python scripts/run_mcmc.py --models lcdm memory --data baseline nocmb
    python scripts/run_mcmc.py --quick            # short chains, for iteration
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from absorb import datasets                                    # noqa: E402
from absorb.constants import SEED                              # noqa: E402
from absorb.params import MODELS                               # noqa: E402
from absorb.sampling import (Posterior, credible_intervals,    # noqa: E402
                             find_map, run_mcmc)

RESULTS = ROOT / "results" / "results.json"


def load_results() -> dict:
    if RESULTS.exists():
        return json.loads(RESULTS.read_text())
    return {}


def save_results(data: dict) -> None:
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(data, indent=2, sort_keys=True))


def derived_summary(model: str, flat: np.ndarray, n_max: int = 4000) -> dict:
    """Posterior of the derived quantities quoted in the paper."""
    from absorb.params import MODELS as M
    m = M[model]
    rng = np.random.default_rng(SEED)
    idx = rng.choice(len(flat), size=min(n_max, len(flat)), replace=False)
    keys, rows = None, []
    for theta in flat[idx]:
        try:
            d = m.builder(m.to_dict(theta[:m.ndim])).derived()
        except Exception:                                       # noqa: BLE001
            continue
        if keys is None:
            keys = [k for k, v in d.items() if np.isfinite(v)]
        rows.append([d.get(k, np.nan) for k in keys])
    arr = np.asarray(rows, dtype=float)
    out = {}
    for i, k in enumerate(keys or []):
        col = arr[:, i]
        col = col[np.isfinite(col)]
        if col.size < 10:
            continue
        lo, hi = np.percentile(col, [16, 84])
        out[k] = {"value": float(np.median(col)),
                  "err_lo": float(np.median(col) - lo),
                  "err_hi": float(hi - np.median(col))}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=["lcdm"],
                    choices=sorted(MODELS))
    ap.add_argument("--data", nargs="+", default=["baseline"],
                    choices=list(datasets.DATASETS))
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--map-only", action="store_true",
                    help="find the best fit without sampling")
    ap.add_argument("--max-steps", type=int, default=40000)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    results = load_results()
    results.setdefault("chains", {})

    for dname in args.data:
        like = datasets.build(dname)
        for mname in args.models:
            post = Posterior(mname, like)
            tag = f"{mname}__{dname}"
            print(f"\n=== {tag}  (ndim={post.ndim}, n_data={like.n_data()}) ===")

            if args.map_only:
                theta = find_map(post, seed=args.seed)
                bg = MODELS[mname].builder(MODELS[mname].to_dict(theta))
                print("  MAP:", dict(zip(post.param_names, np.round(theta, 5))))
                print(f"  chi2 = {post.chi2(theta):.2f}")
                print("  breakdown:", {k: round(v, 2)
                                       for k, v in like.breakdown(bg).items()})
                print("  derived:", {k: round(v, 4)
                                     for k, v in bg.derived().items()})
                continue

            flat, summary = run_mcmc(post, dname, seed=args.seed,
                                     quick=args.quick, resume=False,
                                     max_steps=args.max_steps)
            ci = credible_intervals(flat, post.param_names)
            entry = summary.to_dict()
            entry["parameters"] = ci
            entry["derived"] = derived_summary(mname, flat)
            theta_map = find_map(post, seed=args.seed)
            bg = MODELS[mname].builder(MODELS[mname].to_dict(theta_map))
            entry["chi2_breakdown"] = {k: float(v)
                                       for k, v in like.breakdown(bg).items()}
            entry["chi2_min"] = float(post.chi2(theta_map))
            entry["aic"] = entry["chi2_min"] + 2 * post.ndim
            entry["bic"] = entry["chi2_min"] + post.ndim * np.log(like.n_data())
            results["chains"][tag] = entry

            print(f"  steps={summary.n_steps} tau={summary.tau_max:.0f} "
                  f"converged={summary.converged} accept={summary.acceptance:.2f} "
                  f"[{summary.runtime_s:.0f} s]")
            print(f"  chi2_min={entry['chi2_min']:.2f}  "
                  f"AIC={entry['aic']:.2f}  BIC={entry['bic']:.2f}")
            for k, v in ci.items():
                print(f"    {k:18s} {v['median']:+.5f} "
                      f"[{v['lo68']:+.5f}, {v['hi68']:+.5f}]")
            for k, v in entry["derived"].items():
                print(f"    ~{k:17s} {v['value']:+.5f} "
                      f"-{v['err_lo']:.5f}/+{v['err_hi']:.5f}")
            save_results(results)

    save_results(results)
    print(f"\nwrote {RESULTS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
