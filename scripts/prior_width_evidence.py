#!/usr/bin/env python3
"""How much of the Bayes factor is the width of the rate prior? Measured properly.

The extension contains LambdaCDM in two ways: exactly on the face eps = 0, and
asymptotically as the rate goes to zero at any eps. The second means the region
of parameter space where the extension is indistinguishable from LambdaCDM is
unbounded below in log-rate, so how much prior is given to it is a choice, and
the Bayes factor depends on that choice.

Quantifying it needs the sampler re-run with the widened prior. A cheap prior
Monte Carlo over the added slab does not work and is not used: tested on this
problem, the single best draw of two thousand carried 100% of the sum and
estimates scattered by 26 in the log across seeds, which is an estimate of the
maximum of a sample, not of an integral.
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

from absorb import params as P                                  # noqa: E402
from absorb.constants import SEED                               # noqa: E402
from absorb.resources import require_workers                    # noqa: E402
from absorb.sampling import WORKER_RSS_MB                       # noqa: E402

OUT = ROOT / "results" / "prior_width_evidence.json"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--model", default="xi_h")
    ap.add_argument("--param", default="log10_xi")
    ap.add_argument("--lows", type=float, nargs="+",
                    default=[-3.0, -5.0, -7.0])
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--nlive", type=int, default=500)
    ap.add_argument("--seeds", type=int, nargs="+", default=[20260909, 12345])
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args()

    n_proc = require_workers(WORKER_RSS_MB, requested=args.workers,
                             what="the prior-width scan")
    original = P.PRIORS[args.param]
    rows = []
    try:
        for low in args.lows:
            P.PRIORS[args.param] = P.Prior(original.name, low, original.high,
                                           original.latex)
            import importlib
            import run_nested
            importlib.reload(run_nested)
            for seed in args.seeds:
                r = run_nested.run(args.model, args.data, nlive=args.nlive,
                                   dlogz=0.1, seed=seed, n_proc=n_proc,
                                   archive=False)
                rows.append(dict(low=low, seed=seed, logz=r["logz"],
                                 logz_err=r["logz_err"],
                                 chi2_min=r["chi2_min"]))
                print(f"  {args.param} in [{low:5.1f}, {original.high:.0f}], "
                      f"seed {seed}: ln Z = {r['logz']:.3f} "
                      f"+/- {r['logz_err']:.3f}", flush=True)
                OUT.write_text(json.dumps(
                    dict(model=args.model, param=args.param,
                         dataset=args.data, rows=rows), indent=2))
    finally:
        P.PRIORS[args.param] = original

    by_low = {}
    for r in rows:
        by_low.setdefault(r["low"], []).append(r["logz"])
    print("\n  prior width -> ln Z (mean over seeds, spread):")
    for low, vals in sorted(by_low.items()):
        v = np.asarray(vals)
        print(f"    [{low:5.1f}, {original.high:.0f}]: {v.mean():9.3f}"
              f"   spread {v.max()-v.min():.3f} over {len(v)} seed(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
