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

#: A profile is a harder search than the unconstrained one -- a root-find per
#: evaluation -- so its floor is allowed to sit slightly higher, but only by
#: far less than the 2.71 the limits are read off at.
PROFILE_TOL = 0.05


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

    # Profiles too: a profile is a constrained maximisation over a superset of
    # the unconstrained problem at the target it can reach freely, so its floor
    # cannot lie above the unconstrained maximum. Three of them did, by up to
    # 0.78, and every Delta chi-square in those profiles was measured from that
    # floor.
    prof = ROOT / "results" / "profile.json"
    if prof.exists():
        for tag, e in sorted(json.loads(prof.read_text()).items()):
            ex = e.get("profile_min_excess")
            if ex is None:
                print(f"  {tag:34s} profile floor not compared (no MAP)")
                continue
            covers = e.get("grid_covers_the_maximum")
            kind = "matches" if ex <= PROFILE_TOL else "ABOVE"
            print(f"  {tag:34s} floor {e['profile_min_chi2']:.4f} vs MAP "
                  f"{e['map_chi2']:.4f}  ({ex:+.4f}, {kind})")
            if covers is False:
                bad.append(
                    f"{tag}: the grid does not sample the unconstrained "
                    f"maximum, which sits at "
                    f"{e.get('map_quantity_value'):.3g} while the smallest "
                    f"positive target is "
                    f"{e.get('grid_smallest_positive_target'):.3g}. The "
                    f"profile's floor is then not the maximum and every "
                    f"Delta chi-square in it is measured from too high a base; "
                    f"widen the grid rather than reinterpreting the number")
            elif ex > PROFILE_TOL:
                bad.append(f"{tag}: the profile's floor is {ex:.4f} above the "
                           f"model's own maximum, so every Delta chi-square in "
                           f"it is measured from the wrong base")

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
