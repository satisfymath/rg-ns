#!/usr/bin/env python3
"""How far apart are the extensions, against how well they are measured?

Section 10 says the ordering among the extensions is not a result. That
sentence needs three numbers -- the spread of their Bayes factors, the error on
a difference between two of them, and the prior-width range -- and the first
two were typed by hand while the third came from a results file. This derives
all three from ``results/evidence.json``, so the sentence cannot drift from the
table above it.

The error on a *difference* between two extensions is not the error on either:
the LambdaCDM reference cancels, leaving the two log-evidence errors added in
quadrature.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "results" / "evidence.json"
OUT = ROOT / "results" / "evidence_spread.json"


def main() -> int:
    if not EVIDENCE.exists():
        print("evidence_spread: results/evidence.json not present")
        return 1
    ev = json.loads(EVIDENCE.read_text())
    rows = {k: v for k, v in ev.items()
            if k.endswith("__baseline") and "ln_bayes_vs_lcdm" in v}
    if len(rows) < 2:
        print("evidence_spread: fewer than two extensions on the baseline")
        return 1

    values = {k: float(v["ln_bayes_vs_lcdm"]) for k, v in rows.items()}
    best = max(values, key=values.get)
    worst = min(values, key=values.get)
    errs = [float(rows[k]["logz_err"]) for k in (best, worst)]
    out = {
        "n_extensions": len(values),
        "best_model": best.split("__")[0],
        "worst_model": worst.split("__")[0],
        "ln_bayes_best": values[best],
        "ln_bayes_worst": values[worst],
        "spread": values[best] - values[worst],
        "error_on_a_difference": float((errs[0] ** 2 + errs[1] ** 2) ** 0.5),
    }
    out["spread_in_sigma"] = out["spread"] / out["error_on_a_difference"]
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"  best {out['best_model']} at {out['ln_bayes_best']:+.3f}, "
          f"worst {out['worst_model']} at {out['ln_bayes_worst']:+.3f}")
    print(f"  spread {out['spread']:.3f} against "
          f"{out['error_on_a_difference']:.3f} on a difference "
          f"({out['spread_in_sigma']:.2f} sigma)")
    print(f"  -> {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
