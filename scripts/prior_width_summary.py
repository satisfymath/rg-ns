#!/usr/bin/env python3
"""Collapse the prior-width scan into the numbers the manuscript quotes."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
SCAN = ROOT / "results" / "prior_width_evidence.json"
EVID = ROOT / "results" / "evidence.json"
OUT = ROOT / "results" / "prior_width_summary.json"


def main() -> int:
    if not SCAN.exists():
        print("no scan yet")
        return 0
    scan = json.loads(SCAN.read_text())
    ref = json.loads(EVID.read_text())[f"lcdm__{scan['dataset']}"]["logz"]

    by: dict[float, list[float]] = {}
    for r in scan["rows"]:
        by.setdefault(float(r["low"]), []).append(float(r["logz"]))

    rows = []
    for low in sorted(by, reverse=True):
        v = np.asarray(by[low])
        rows.append(dict(low=low, logz=float(v.mean()), n_seeds=len(v),
                         seed_spread=float(v.max() - v.min()),
                         ln_bayes=float(v.mean() - ref)))
    lnb = [r["ln_bayes"] for r in rows]
    out = dict(model=scan["model"], param=scan["param"], dataset=scan["dataset"],
               rows=rows,
               ln_bayes_baseline=rows[0]["ln_bayes"],
               ln_bayes_widest=rows[-1]["ln_bayes"],
               ln_bayes_range=float(max(lnb) - min(lnb)),
               odds_baseline=float(np.exp(-rows[0]["ln_bayes"])),
               odds_widest=float(np.exp(-rows[-1]["ln_bayes"])))
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True))
    for r in rows:
        print(f"  [{r['low']:5.1f}, ...]: ln Z = {r['logz']:9.3f} "
              f"({r['n_seeds']} seeds, spread {r['seed_spread']:.3f})  "
              f"ln B = {r['ln_bayes']:+6.2f}")
    print(f"  range of ln B over the scan: {out['ln_bayes_range']:.2f}")
    print(f"  odds against, baseline to widest: "
          f"{out['odds_baseline']:.1f}:1 to {out['odds_widest']:.1f}:1")
    return 0


if __name__ == "__main__":
    sys.exit(main())
