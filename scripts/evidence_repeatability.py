#!/usr/bin/env python3
"""Is the quoted error on ln Z honest?

The model comparison rests on differences of log-evidences of order 1.5 against
quoted errors of about 0.2, so whether those errors mean anything is not a
detail. A nested sampler's internal error estimate comes from the statistics of
the shrinkage of the prior volume, and it is an estimate, not a measurement.

This measures it: the same model, on the same data, with the same settings, run
several times from different seeds. The spread of the answers is compared with
the error the sampler reports for a single run. If the reported error is
honest, the two agree.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

os.environ.setdefault("OMP_NUM_THREADS", "1")
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np                                              # noqa: E402

from absorb.constants import SEED                               # noqa: E402
from absorb.resources import require_workers                    # noqa: E402
from absorb.sampling import WORKER_RSS_MB                       # noqa: E402
from run_nested import run                                      # noqa: E402

OUT = ROOT / "results" / "evidence_repeatability.json"


def _load():
    import json as _j
    return _j.loads(OUT.read_text()) if OUT.exists() else {}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="lcdm")
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--repeats", type=int, default=4)
    ap.add_argument("--nlive", type=int, default=500)
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    n_proc = require_workers(WORKER_RSS_MB, requested=args.workers,
                             what="the repeatability check")
    logz, errs = [], []
    for i in range(args.repeats):
        seed = SEED + 1000 * (i + 1)
        r = run(args.model, args.data, nlive=args.nlive, dlogz=0.1,
                seed=seed, n_proc=n_proc, archive=False)
        logz.append(r["logz"])
        errs.append(r["logz_err"])
        print(f"  seed {seed}: ln Z = {r['logz']:.3f} +/- {r['logz_err']:.3f}",
              flush=True)

    logz = np.asarray(logz)
    spread = float(np.std(logz, ddof=1)) if len(logz) > 1 else float("nan")
    reported = float(np.mean(errs))
    out = {
        "model": args.model, "dataset": args.data, "nlive": args.nlive,
        "n_repeats": args.repeats,
        "logz_values": logz.tolist(),
        "logz_spread": spread,
        "logz_reported_error": reported,
        "ratio_spread_to_reported": spread / reported if reported else float("nan"),
        "max_pairwise_difference": float(logz.max() - logz.min()),
    }
    print(f"\n  spread over {args.repeats} runs: {spread:.3f}")
    print(f"  error the sampler reports:  {reported:.3f}")
    print(f"  ratio: {out['ratio_spread_to_reported']:.2f} "
          f"(1 means the reported error is honest)")
    store = _load()
    store[f"{args.model}__{args.data}"] = out
    OUT.write_text(json.dumps(store, indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
