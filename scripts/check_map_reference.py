#!/usr/bin/env python3
"""Gate: no reported best fit may sit above one already known to be reachable.

Two things are checked, and each corresponds to a defect this repository
actually shipped at some point.

*Against the frozen reference.*  ``results/map_reference.json`` holds the
brute-force maximisation -- forty full Nelder-Mead runs from random prior
points.  A chi-square is attained at a real point, so the reference is a
ceiling, not an estimate: a cheaper protocol landing above it has failed to
find something already recorded here.  ``run_map.py`` documented this
comparison in its docstring for some time without performing it, and the
comparison, once written, found the six- and nine-parameter models sitting
0.14 above a value the reference had reached.

*Against containment.*  A model cannot fit worse than a model it contains.
The nine-parameter model once reported a chi-square 1.55 worse than the seven
it contains, which is impossible, and that number was on its way into the
comparison table.

Both are failures of the search, never of the physics, so they are gated
rather than reported.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from run_map import CONTAINS, REFERENCE, REFERENCE_TOL, OUT  # noqa: E402

#: Containment is exact arithmetic, so the tolerance only absorbs the
#: optimiser's own noise on two separate searches for the same maximum.
CONTAIN_TOL = 0.01


def main() -> int:
    if not OUT.exists():
        print("check_map_reference: results/map.json absent; nothing to check")
        return 0
    maps = json.loads(OUT.read_text())
    ref = json.loads(REFERENCE.read_text()) if REFERENCE.exists() else {}
    bad = []

    for tag, e in sorted(maps.items()):
        model, _, dataset = tag.partition("__")
        chi2 = e["chi2_min"]

        entry = ref.get(tag)
        if entry is not None:
            d = chi2 - entry["chi2_min"]
            kind = "reproduces" if d <= REFERENCE_TOL else "ABOVE"
            print(f"  {tag:24s} {chi2:.4f}  reference {entry['chi2_min']:.4f}"
                  f"  ({d:+.4f}, {kind})")
            if d > REFERENCE_TOL:
                bad.append(f"{tag}: {chi2:.4f} is {d:.4f} above the frozen "
                           f"reference {entry['chi2_min']:.4f}")
        else:
            print(f"  {tag:24s} {chi2:.4f}  (no direct reference)")

        for sub in CONTAINS.get(model, []):
            for source, label in ((maps, "best fit"), (ref, "reference")):
                s = source.get(f"{sub}__{dataset}")
                if s is None:
                    continue
                d = chi2 - s["chi2_min"]
                if d > CONTAIN_TOL:
                    bad.append(f"{tag}: {chi2:.4f} is {d:.4f} worse than the "
                               f"{label} of {sub}, which it contains")

    if bad:
        print("\ncheck_map_reference: FAILED")
        for line in bad:
            print(f"  - {line}")
        print("\nThe maximisation, not the model, is at fault: raise --screen "
              "or --restarts in scripts/run_map.py and re-run.")
        return 1
    print("check_map_reference: every best fit reaches what is known reachable")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
