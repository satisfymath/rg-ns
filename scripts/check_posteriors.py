#!/usr/bin/env python3
"""Gate: an archived posterior must belong to the run its name claims.

``results/posteriors/{model}_{dataset}.npz`` is the file the parameter table,
the figures and the published summaries are built from, and its name encodes
neither the priors nor the seed. Two scripts legitimately call the sampler with
modified priors -- the prior-width scan -- or with other seeds -- the
repeatability check -- and both wrote to that name.

What was on disk for the six-parameter model on the baseline combination was
therefore the last of those calls: prior lower edge -7 where the model states
-3, and seed 12345 where the default is used everywhere else. It propagated:
``results.json`` published a 95% interval for ``log10_xi`` running to -6.71,
outside the prior printed in the same table, and the derived summaries built
from it are the ones a reader would have checked.

No build gate could have caught it, because every macro was correctly generated
from the wrong file. This is the gate that can: it compares the samples against
the priors the model declares, and the recorded seed against the default.
Files written before the provenance fields existed are checked on the samples
alone and reported as such, which is enough to catch this failure.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from absorb.constants import SEED                                # noqa: E402
from absorb.params import MODELS                                 # noqa: E402

SAMPLES = ROOT / "results" / "posteriors"

#: Samples may sit on a prior edge, so the comparison needs a tolerance; it is
#: a fraction of the prior width and not an absolute number, because the widths
#: here span four orders of magnitude.
EDGE_TOL = 1e-6


def main() -> int:
    if not SAMPLES.exists():
        print("check_posteriors: results/posteriors absent; nothing to check")
        return 0

    bad, n = [], 0
    for path in sorted(SAMPLES.glob("*.npz")):
        # Model names contain underscores ("xi_h", "track_b"), so splitting on
        # the first one gives "xi" and a dataset of "h_baseline". Match the
        # longest model name the stem starts with instead.
        model = max((m for m in MODELS if path.stem.startswith(m + "_")),
                    key=len, default=None)
        if model is None:
            bad.append(f"{path.name}: no known model matches this file name")
            continue
        dataset = path.stem[len(model) + 1:]
        d = np.load(path, allow_pickle=True)
        names = [str(x) for x in d["param_names"]]
        samples = d["samples"]
        priors = MODELS[model].priors()
        declared = list(MODELS[model].params)
        n += 1

        if names != declared:
            bad.append(f"{path.name}: parameters {names} are not the model's "
                       f"{declared}")
            continue

        notes = []
        for k, pr in enumerate(priors):
            width = pr.high - pr.low
            lo, hi = samples[:, k].min(), samples[:, k].max()
            if lo < pr.low - EDGE_TOL * width or hi > pr.high + EDGE_TOL * width:
                bad.append(
                    f"{path.name}: {pr.name} ranges [{lo:.4g}, {hi:.4g}], "
                    f"outside its prior [{pr.low:g}, {pr.high:g}]. The file is "
                    f"from a run under different priors and is not the "
                    f"posterior this name claims.")

        if "seed" in d.files:
            s = int(d["seed"])
            if s != SEED:
                bad.append(f"{path.name}: recorded seed {s} is not the default "
                           f"{SEED}; the archive must come from the default run")
            stored_low = d["prior_low"]
            if not np.allclose(stored_low, [p.low for p in priors]):
                bad.append(f"{path.name}: the priors recorded in the file are "
                           f"not the model's current priors")
        else:
            notes.append("no provenance fields; checked on samples alone")

        note = f"   ({'; '.join(notes)})" if notes else ""
        print(f"  {path.name:28s} {samples.shape[0]:6d} samples, "
              f"{len(names)} parameters{note}")

    if bad:
        print("\ncheck_posteriors: FAILED")
        for line in bad:
            print(f"  - {line}")
        print("\nRe-run the affected model with `scripts/run_nested.py` and "
              "re-run `scripts/summarise_posteriors.py`.")
        return 1
    print(f"check_posteriors: {n} archived posteriors match their models")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
