#!/usr/bin/env python3
"""Does adding growth data change where the model stands?

The model's sharpest linear signature is that density growth is enhanced while
the velocity growth that redshift-space distortions measure is suppressed
(``eq:perturbations-growth-signature``).  If any data set were going to move
the comparison in the model's favour, it is that one, so the manuscript reports
what happens when it is included rather than leaving the reader to wonder.

This derives the comparison from ``results/evidence.json``; it runs no sampler
of its own.  It exists because the three numbers it writes were quoted in the
manuscript for a while with no script behind them: the file they came from had
been produced by hand, so the documented reproduction path could not regenerate
them and a reader could not check them.  Deriving them here is the whole job,
and the point is that it is now reachable from ``make reproduce-full``.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "results" / "evidence.json"
OUT = ROOT / "results" / "growth_comparison.json"


def main() -> int:
    if not EVIDENCE.exists():
        print("growth_comparison: results/evidence.json not present; "
              "run `python3 scripts/run_nested.py` first")
        return 1
    ev = json.loads(EVIDENCE.read_text())

    missing = [k for k in ("xi_h__baseline", "xi_h__rsd", "lcdm__baseline",
                           "lcdm__rsd") if k not in ev]
    if missing:
        print("growth_comparison: missing evidences " + ", ".join(missing)
              + "\n  run: python3 scripts/run_nested.py --models lcdm xi_h "
                "--data rsd")
        return 1

    # Each ln B is computed against LambdaCDM *on the same data*, which is the
    # only comparison that means anything: the two data sets have different
    # numbers of points, so the log-evidences themselves are not comparable
    # across them and only their differences within a data set are.
    base = ev["xi_h__baseline"]["logz"] - ev["lcdm__baseline"]["logz"]
    with_growth = ev["xi_h__rsd"]["logz"] - ev["lcdm__rsd"]["logz"]

    def err(a, b):
        return (ev[a]["logz_err"] ** 2 + ev[b]["logz_err"] ** 2) ** 0.5

    out = {
        "ln_bayes_baseline": base,
        "ln_bayes_with_growth": with_growth,
        "change": with_growth - base,
        "ln_bayes_baseline_err": err("xi_h__baseline", "lcdm__baseline"),
        "ln_bayes_with_growth_err": err("xi_h__rsd", "lcdm__rsd"),
        "model": "xi_h",
        "datasets": ["baseline", "rsd"],
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"  ln B (baseline)      = {base:+.4f} +/- "
          f"{out['ln_bayes_baseline_err']:.4f}")
    print(f"  ln B (with growth)   = {with_growth:+.4f} +/- "
          f"{out['ln_bayes_with_growth_err']:.4f}")
    print(f"  change               = {out['change']:+.4f}")
    print(f"  -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
