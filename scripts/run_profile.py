#!/usr/bin/env python3
"""Profile likelihood in the conversion parameter.

Why this exists.  The posterior has a funnel at eps -> 0: there the rate
normalisation, the activation redshift and the reinforcement strength all drop
out of the likelihood, so the marginal posterior is dominated by prior volume
and an ensemble sampler mixes badly.  The chains bear this out, with
autocorrelation times of thousands of steps and acceptance fractions of a few
per cent.

The physically meaningful statement, an upper limit on how much conversion the
data allow, does not require the marginal posterior.  It requires the profile
likelihood: for each value of eps, maximise over everything else.  That is
immune to the funnel, needs no prior on the nuisance directions, and is what is
reported.

Cost: a few hundred likelihood evaluations per grid point, single process.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import minimize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from absorb import datasets                                     # noqa: E402
from absorb.params import MODELS, PRIORS                        # noqa: E402
from absorb.resources import mem_available_mb, record           # noqa: E402
from absorb.sampling import Posterior                           # noqa: E402

OUT = ROOT / "results" / "profile.json"


def profile(model: str, dataset: str, n_grid: int = 17,
            n_restarts: int = 3, seed: int = 20260909) -> dict:
    like = datasets.build(dataset)
    post = Posterior(model, like)
    names = list(post.param_names)
    i_eps = names.index("eps")
    lows = np.array([p.low for p in post.model.priors()])
    highs = np.array([p.high for p in post.model.priors()])
    rng = np.random.default_rng(seed)

    grid = np.linspace(0.0, 0.6, n_grid)
    chi2 = np.empty(n_grid)
    best_theta = [None] * n_grid

    free = [j for j in range(len(names)) if j != i_eps]

    for k, eps in enumerate(grid):
        def neg(sub):
            theta = np.empty(len(names))
            theta[i_eps] = eps
            theta[free] = sub
            v = post(theta)
            return 1e10 if not np.isfinite(v) else -2.0 * v

        best = np.inf
        for r in range(n_restarts):
            x0 = lows[free] + rng.random(len(free)) * (highs[free] - lows[free])
            if best_theta[max(k - 1, 0)] is not None and r == 0:
                x0 = best_theta[max(k - 1, 0)][free]      # warm start
            res = minimize(neg, x0, method="Nelder-Mead",
                           options=dict(maxfev=3000, xatol=1e-4, fatol=1e-4))
            if res.fun < best:
                best = res.fun
                th = np.empty(len(names))
                th[i_eps] = eps
                th[free] = res.x
                best_theta[k] = th
        chi2[k] = best
        print(f"  eps={eps:5.3f}   chi2_min={best:10.3f}")

    chi2 -= chi2.min()
    # one-sided 95% limit for one parameter of interest: Delta chi2 = 2.71
    above = np.where(chi2 > 2.71)[0]
    limit = float(np.interp(2.71, chi2[: above[0] + 1], grid[: above[0] + 1])) \
        if above.size else float(grid[-1])
    return {
        "model": model, "dataset": dataset,
        "eps_grid": grid.tolist(), "delta_chi2": chi2.tolist(),
        "eps_limit_95": limit,
        "chi2_at_zero": float(chi2[0]),
        "best_theta": [t.tolist() for t in best_theta],
        "param_names": names,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=["xi_h"])
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--n-grid", type=int, default=17)
    args = ap.parse_args()

    print(f"MemAvailable {mem_available_mb():.0f} MB; single process")
    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    for m in args.models:
        print(f"\n=== profile in eps: {m} / {args.data} ===")
        with record(f"profile_{m}", "profile likelihood in eps"):
            out[f"{m}__{args.data}"] = profile(m, args.data, args.n_grid)
        r = out[f"{m}__{args.data}"]
        print(f"  95% upper limit on eps: {r['eps_limit_95']:.4f}")
        OUT.write_text(json.dumps(out, indent=2))
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
