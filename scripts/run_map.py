#!/usr/bin/env python3
"""Best fit for every model under one maximisation protocol.

The chi-square differences in the comparison table are only meaningful if every
model's maximum was sought equally hard.  They were not: the maximum used to be
a Nelder-Mead polish of the best chain sample under a *fixed* evaluation budget,
so LambdaCDM's three dimensions got the same 1800 evaluations as the six of the
extension, and the model that needed the polish most got no more of it.  The
budget here scales with the dimension, the starting points are drawn the same
way for every model, and the achieved value is reported with the spread over
restarts so that the optimiser's own noise floor is visible rather than assumed.
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

import numpy as np                                              # noqa: E402

from absorb import datasets                                     # noqa: E402
from absorb.constants import SEED                               # noqa: E402
from absorb.resources import record                             # noqa: E402
from absorb.sampling import (MAP_BUDGET_PER_DIM, Posterior,      # noqa: E402
                             find_map)

OUT = ROOT / "results" / "map.json"


def best_fit(model: str, dataset: str, n_restarts: int, seed: int) -> dict:
    post = Posterior(model, datasets.build(dataset))
    budget = MAP_BUDGET_PER_DIM * post.ndim
    values, thetas = [], []
    for r in range(n_restarts):
        theta = find_map(post, seed=seed + r, max_local=budget)
        values.append(post.chi2(theta))
        thetas.append(theta)
    values = np.array(values)
    k = int(np.argmin(values))
    return dict(model=model, dataset=dataset, ndim=post.ndim,
                chi2_min=float(values[k]),
                chi2_spread=float(values.max() - values.min()),
                n_restarts=n_restarts, budget_evals=budget,
                budget_per_dim=MAP_BUDGET_PER_DIM,
                theta=thetas[k].tolist(),
                param_names=list(post.param_names))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="+",
                    default=["lcdm", "xi_h", "reinforce", "memory"])
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--restarts", type=int, default=3)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    for m in args.models:
        tag = f"{m}__{args.data}"
        with record(f"map_{tag}", f"{args.restarts} restarts"):
            out[tag] = best_fit(m, args.data, args.restarts, args.seed)
        e = out[tag]
        print(f"  {tag:24s} chi2_min = {e['chi2_min']:.4f} "
              f"(spread over restarts {e['chi2_spread']:.4f}, "
              f"{e['budget_evals']} evals allowed)", flush=True)
        OUT.write_text(json.dumps(out, indent=2, sort_keys=True))

    ref = out.get(f"lcdm__{args.data}")
    if ref:
        print("\nDelta chi2 against LambdaCDM:")
        for tag, e in sorted(out.items()):
            if tag.startswith("lcdm__"):
                continue
            print(f"  {tag:24s} {e['chi2_min'] - ref['chi2_min']:+.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
