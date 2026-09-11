#!/usr/bin/env python3
"""Is Delta chi-square = 2.71 the right threshold for these limits?

The manuscript drops AIC and BIC because the rate parameters are unidentified
when the convertible fraction vanishes -- Davies' problem -- and then reads its
95% limits off the regular-theory threshold 2.71. A referee pointed out that
this applies non-regularity where it removes an unfavourable number and ignores
it where it would loosen a favourable one, and the objection is sound: under
Davies' problem the null distribution of the likelihood-ratio statistic is the
supremum of a random field over the unidentified directions, not a chi-square
mixture, and its upper quantiles are *larger*. A threshold that is too small
makes the limits too tight.

The size of that effect is measurable rather than arguable, so this measures
it. Synthetic data are generated at the LambdaCDM best fit with the real
covariances, both models are maximised on each, and the distribution of
``Delta chi2 = chi2(LambdaCDM) - chi2(extension)`` under the null is
accumulated. Its 90th percentile is the threshold a 95% one-sided limit should
use; 2.71 is what regular theory would give.

This is the Davies statistic for the *unconstrained* comparison, which is the
quantity the comparison table reports. It is an upper bound on the correction
needed for the profiles, which fix a derived quantity and therefore explore
less of the unidentified space; the manuscript says so where it quotes the
result.
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

from absorb import datasets                                     # noqa: E402
from absorb.constants import SEED                               # noqa: E402
from absorb.sampling import Posterior                           # noqa: E402
from run_map import embed                                       # noqa: E402

OUT = ROOT / "results" / "threshold_calibration.json"


def _best(post, x0, lo, hi, budget, n_restarts, rng):
    from scipy.optimize import minimize

    def neg(theta):
        if np.any(theta < lo) or np.any(theta > hi):
            return 1e10
        v = post(theta)
        return 1e10 if not np.isfinite(v) else -2.0 * v

    best, best_x = np.inf, None
    starts = [x0] + [np.clip(x0 + 0.05 * (hi - lo) * rng.normal(size=len(x0)),
                             lo, hi) for _ in range(n_restarts)]
    for s in starts:
        for method, opts in (("Nelder-Mead",
                              dict(maxfev=budget, xatol=1e-7, fatol=1e-7)),
                             ("Powell",
                              dict(maxfev=budget, xtol=1e-7, ftol=1e-7))):
            r = minimize(neg, s, method=method, options=opts)
            if r.fun < best:
                best, best_x = r.fun, r.x
            s = r.x
    return float(best), best_x


#: Set by :func:`main` before the pool forks; the workers inherit it through
#: the address space. A closure cannot be used because Pool pickles the
#: function it maps, and a local one is not picklable.
_W: dict = {}


def _one_draw(i: int) -> float:
    """One synthetic data set, both maximisations, one statistic.

    Each worker forks with the real data loaded and mutates only its own copy,
    so no restore is needed inside the worker; the parent restores its own.
    """
    a = _W["args"]
    r = np.random.default_rng([a.seed, i])
    _W["like"].simulate(_W["bg_null"], r)
    c_null, x_null = _best(_W["null"], _W["theta_null"], _W["lo_n"],
                           _W["hi_n"], a.budget, a.restarts, r)
    # Seed the alternative with the null's answer embedded, exactly as the
    # main maximisation does. The alternative contains the null, so the
    # statistic cannot be negative; without the seed it was, which measures
    # the optimiser rather than the data.
    seed_alt = embed(list(_W["null"].param_names), x_null, a.model)
    c_a, _ = _best(_W["alt"], seed_alt, _W["lo_a"], _W["hi_a"], a.budget,
                   a.restarts, r)
    c_b, _ = _best(_W["alt"], _W["theta_alt"], _W["lo_a"], _W["hi_a"],
                   a.budget, a.restarts, r)
    c_alt = min(c_a, c_b)
    if c_null - c_alt < -1e-6:
        raise RuntimeError(
            f"draw {i}: the nested model fits worse than the null by "
            f"{c_alt - c_null:.4f}; the maximisation failed")
    return max(c_null - c_alt, 0.0)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--draws", type=int, default=100)
    ap.add_argument("--model", default="xi_h")
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--budget", type=int, default=1200)
    ap.add_argument("--restarts", type=int, default=1)
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--workers", type=int, default=None)
    args = ap.parse_args()

    like = datasets.build(args.data)
    null = Posterior("lcdm", like)
    alt = Posterior(args.model, like)

    maps = json.loads((ROOT / "results" / "map.json").read_text())
    theta_null = np.asarray(maps[f"lcdm__{args.data}"]["theta"], dtype=float)
    theta_alt = np.asarray(maps[f"{args.model}__{args.data}"]["theta"],
                           dtype=float)

    rng = np.random.default_rng(args.seed)
    lo_n = np.array([p.low for p in null.model.priors()])
    hi_n = np.array([p.high for p in null.model.priors()])
    lo_a = np.array([p.low for p in alt.model.priors()])
    hi_a = np.array([p.high for p in alt.model.priors()])

    # The synthetic data are drawn by resampling each likelihood's residuals
    # under its own covariance around the LambdaCDM prediction; the likelihood
    # objects expose that through `simulate`, and a likelihood that cannot
    # simulate is skipped with a note rather than faked.
    if not like.can_simulate():
        print("calibrate_threshold: the likelihood cannot generate synthetic "
              "data; add a `simulate` method to run this calibration")
        return 2

    # the background the null data are drawn from, built once
    bg_null = null.model.builder(
        null.model.to_dict(theta_null[:null.model.ndim]))

    _W.update(args=args, like=like, null=null, alt=alt, bg_null=bg_null,
              theta_null=theta_null, theta_alt=theta_alt,
              lo_n=lo_n, hi_n=hi_n, lo_a=lo_a, hi_a=hi_a)

    import multiprocessing as mp

    from absorb.resources import require_workers                # noqa: E402
    from absorb.sampling import WORKER_RSS_MB                   # noqa: E402

    n_proc = require_workers(WORKER_RSS_MB, requested=args.workers,
                             what="the threshold calibration")
    print(f"calibrating with {n_proc} workers, {args.draws} draws")
    try:
        if n_proc > 1:
            ctx = mp.get_context("fork")
            with ctx.Pool(n_proc) as pool:
                stats = pool.map(_one_draw, range(args.draws), chunksize=1)
        else:
            stats = [_one_draw(i) for i in range(args.draws)]
    finally:
        like.restore()

    a = np.asarray(stats)
    out = {
        "model": args.model, "dataset": args.data, "n_draws": int(a.size),
        "delta_chi2": a.tolist(),
        "pct50": float(np.percentile(a, 50)),
        "pct90": float(np.percentile(a, 90)),
        "pct95": float(np.percentile(a, 95)),
        "regular_threshold": 2.71,
        "inflation_factor": float(np.percentile(a, 90) / 2.71),
    }
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"\n  90th percentile under the null: {out['pct90']:.3f}"
          f"  against the regular-theory 2.71"
          f"  (factor {out['inflation_factor']:.2f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
