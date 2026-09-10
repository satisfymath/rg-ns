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


def best_fit(model: str, dataset: str, n_restarts: int, seed: int,
             n_polish: int = 6) -> dict:
    """Best fit under one protocol, with enough budget to actually find it.

    The first version of this ran ``find_map`` a few times with a per-dimension
    budget and reported the best. On the six-parameter model that returned
    1435.807 where the maximum is 1434.879, and its own spread-over-restarts
    diagnostic said so: 1.04, which is larger than the chi-square difference
    the model comparison is about. An optimiser whose scatter exceeds the
    effect being measured has not measured it.

    What works, and is what this does: many random starts, then repeated
    Nelder-Mead polishing of the winner until it stops improving. The spread is
    still reported, and ``converged`` records whether it is small enough for the
    answer to mean anything.
    """
    from scipy.optimize import minimize

    post = Posterior(model, datasets.build(dataset))
    priors = post.model.priors()
    lo = np.array([p.low for p in priors])
    hi = np.array([p.high for p in priors])
    budget = MAP_BUDGET_PER_DIM * post.ndim

    def neg(theta):
        if np.any(theta < lo) or np.any(theta > hi):
            return 1e10
        v = post(theta)
        return 1e10 if not np.isfinite(v) else -2.0 * v

    rng = np.random.default_rng(seed)
    values = []
    best, best_x = np.inf, None
    for _ in range(n_restarts):
        x0 = lo + rng.random(post.ndim) * (hi - lo)
        r = minimize(neg, x0, method="Nelder-Mead",
                     options=dict(maxfev=budget, xatol=1e-8, fatol=1e-8))
        values.append(r.fun)
        if r.fun < best:
            best, best_x = r.fun, r.x

    # polish the winner until it stops moving
    for _ in range(n_polish):
        r = minimize(neg, best_x, method="Nelder-Mead",
                     options=dict(maxfev=2 * budget, xatol=1e-10, fatol=1e-10))
        if r.fun < best - 1e-9:
            best, best_x = r.fun, r.x
        else:
            break

    finite = np.array([v for v in values if v < 1e9])
    spread = float(finite.max() - finite.min()) if finite.size > 1 else float("nan")
    # how many independent starts landed within 0.01 of the winner
    n_at_best = int(np.sum(finite < best + 0.01))
    on_edge = [n for n, x, l, h in zip(post.param_names, best_x, lo, hi)
               if abs(x - l) < 1e-6 * (h - l) or abs(x - h) < 1e-6 * (h - l)]
    return dict(model=model, dataset=dataset, ndim=post.ndim,
                chi2_min=float(best),
                chi2_spread=spread,
                n_restarts=n_restarts, n_reaching_best=n_at_best,
                converged=bool(n_at_best >= 2),
                budget_evals=budget, budget_per_dim=MAP_BUDGET_PER_DIM,
                on_prior_edge=on_edge,
                theta=np.asarray(best_x).tolist(),
                param_names=list(post.param_names))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="+",
                    default=["lcdm", "xi_h", "reinforce", "memory"])
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--restarts", type=int, default=40)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    for m in args.models:
        tag = f"{m}__{args.data}"
        with record(f"map_{tag}", f"{args.restarts} restarts"):
            out[tag] = best_fit(m, args.data, args.restarts, args.seed)
        e = out[tag]
        edge = (f", on the prior edge in {','.join(e['on_prior_edge'])}"
                if e["on_prior_edge"] else "")
        mark = "" if e["converged"] else "   [NOT CONVERGED]"
        print(f"  {tag:24s} chi2_min = {e['chi2_min']:.4f}  "
              f"({e['n_reaching_best']}/{e['n_restarts']} starts reached it, "
              f"spread {e['chi2_spread']:.3f}{edge}){mark}", flush=True)
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
