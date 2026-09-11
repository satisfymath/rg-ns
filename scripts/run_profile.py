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


def _solve_eps_for(post, quantity: str, target: float, theta, i_eps: int,
                   lo: float, hi: float):
    """Set ``eps`` so that the derived quantity hits ``target`` exactly.

    Both quantities profiled here -- the matter deficit and the jerk excess --
    are strictly increasing in ``eps`` at fixed values of everything else and
    vanish at ``eps = 0``, so the constraint has at most one solution and a
    bracketed root-find is exact.

    This replaces a quadratic penalty, which did not work and did not fail
    loudly.  A penalty of 1e6 on a quantity of order 1e-2 contributes about 1
    to chi-square for a ten per cent miss, far too weak to hold the constraint:
    grid points missed their targets by up to 250 per cent, and the resulting
    profile was not monotone -- 0.09, then 298, then 22, then 127 -- because
    each point was really maximising a different function.  A limit read off
    such a curve means nothing.
    """
    from scipy.optimize import brentq

    def value_at(e):
        th = np.array(theta, dtype=float)
        th[i_eps] = e
        try:
            bg = post.model.builder(post.model.to_dict(th[:post.model.ndim]))
            return bg.derived()[quantity] - target
        except Exception:                                       # noqa: BLE001
            return np.nan

    f_lo, f_hi = value_at(lo), value_at(hi)
    if not (np.isfinite(f_lo) and np.isfinite(f_hi)):
        return None
    if f_lo == 0.0:
        return float(lo)
    if f_lo * f_hi > 0:
        return None            # target unreachable at these parameters
    try:
        return float(brentq(value_at, lo, hi, xtol=1e-11))
    except Exception:                                           # noqa: BLE001
        return None


def _with(names, free, sub, i_eps):
    """Assemble a full parameter vector from the free block, eps set to zero."""
    th = np.empty(len(names))
    th[free] = sub
    th[i_eps] = 0.0
    return th


def profile_derived(model: str, dataset: str, quantity: str = "matter_deficit",
                    targets=None, n_restarts: int = 2,
                    n_screen: int = 200, maxfev: int = 800,
                    seed: int = 20260909) -> dict:
    """Profile the likelihood in a derived quantity, imposing the target exactly.

    Profiling in eps alone is uninformative, and it is worth saying why: eps is
    the convertible fraction, not the converted one.  At any eps the optimiser
    can send the rate to zero, recover LambdaCDM exactly, and pay nothing.  The
    likelihood is therefore flat in eps by construction, which is a statement
    about the parametrisation and not about the data.

    The constrained directions are the amount actually converted, measured by
    the matter deficit, and the jerk excess.  At each grid point every
    parameter other than eps is free and eps is solved for so that the derived
    quantity equals the target exactly; see :func:`_solve_eps_for`.  Points at
    which no eps reaches the target are reported unreachable rather than
    quietly filled with the nearest attainable value, and the returned record
    carries the worst target miss and the number of decreasing steps, so a
    failed optimisation cannot pass for a likelihood shape.
    """
    like = datasets.build(dataset)
    post = Posterior(model, like)
    names = list(post.param_names)
    i_eps = names.index("eps")
    priors = post.model.priors()
    lows = np.array([p.low for p in priors])
    highs = np.array([p.high for p in priors])
    rng = np.random.default_rng(seed)
    if targets is None:
        targets = np.concatenate([[0.0], np.logspace(-4, -0.7, 12)])
    targets = np.asarray(targets, dtype=float)

    # Seed every target with the global best fit, which is the one point
    # guaranteed to be at least as good as anything the screen will find. A
    # profile whose own minimum lies above the model's maximum likelihood is
    # measuring Delta chi-square from the wrong floor: the three profiles run
    # before this was added sat 0.78, 0.12 and 0.56 above it, and the largest
    # rise reported for the convertible fraction was 0.859 where the correct
    # figure from the true floor is about 1.64. Neither crosses the 2.71 the
    # limit uses, so the conclusions were unaffected -- but the numbers were
    # quoted, and they were wrong.
    map_theta = None
    map_path = ROOT / "results" / "map.json"
    if map_path.exists():
        entry = json.loads(map_path.read_text()).get(f"{model}__{dataset}")
        if entry is not None and list(entry["param_names"]) == names:
            map_theta = np.asarray(entry["theta"], dtype=float)

    free = [j for j in range(len(names)) if j != i_eps]
    chi2 = np.full(len(targets), np.nan)
    achieved = np.full(len(targets), np.nan)
    best_theta = [None] * len(targets)

    for k, target in enumerate(targets):

        def neg(sub):
            if np.any(sub < lows[free]) or np.any(sub > highs[free]):
                return 1e10
            th = np.empty(len(names))
            th[free] = sub
            th[i_eps] = 0.0
            e = _solve_eps_for(post, quantity, target, th, i_eps,
                               lows[i_eps], highs[i_eps])
            if e is None:
                return 1e10
            th[i_eps] = e
            v = post(th)
            return 1e10 if not np.isfinite(v) else -2.0 * v

        # Most of the prior cannot reach a given target for any eps, so a
        # random start is almost always infeasible and Nelder-Mead sees a flat
        # penalty in every direction.  Screen for feasibility first -- two
        # background solves per candidate, since feasibility is just the sign
        # of the constraint at the two ends of the eps interval -- and start
        # only from points that admit a solution.
        starts = []
        if map_theta is not None:
            starts.append(map_theta[free])
        if k > 0 and best_theta[k - 1] is not None:
            starts.append(np.asarray(best_theta[k - 1])[free])
        screen = lows[free] + rng.random((n_screen, len(free))) * (
            highs[free] - lows[free])
        feasible = []
        for cand in screen:
            th = np.empty(len(names))
            th[free] = cand
            th[i_eps] = 0.0
            if _solve_eps_for(post, quantity, target, th, i_eps,
                              lows[i_eps], highs[i_eps]) is not None:
                feasible.append(cand)
        if feasible:
            vals = [neg(c) for c in feasible]
            order = np.argsort(vals)
            starts.extend(feasible[i] for i in order[:n_restarts])

        best, best_sub = np.inf, None
        for x0 in starts:
            # Each objective evaluation costs a root-find, measured at 12
            # background solves and 160 ms, so the budget is set deliberately
            # rather than left at a default: maxfev = 4000 would be seven hours
            # for one profile. The warm start from the previous target does the
            # work a larger budget would.
            res = minimize(neg, x0, method="Nelder-Mead",
                           options=dict(maxfev=maxfev, xatol=1e-5, fatol=1e-4))
            if res.fun < best:
                best, best_sub = res.fun, res.x
            # One direction-set pass from the simplex's answer. On this
            # objective the simplex contracts across the rate/activation ridge
            # instead of following it, exactly as in the unconstrained
            # maximisation, and Powell recovers what it leaves behind.
            res = minimize(neg, res.x, method="Powell",
                           options=dict(maxfev=maxfev, xtol=1e-6, ftol=1e-6))
            if res.fun < best:
                best, best_sub = res.fun, res.x

        if best_sub is None or best >= 1e10:
            print(f"  target {quantity}={target:11.6f}  unreachable")
            continue
        th = np.empty(len(names))
        th[free] = best_sub
        e = _solve_eps_for(post, quantity, target, th, i_eps,
                           lows[i_eps], highs[i_eps])
        th[i_eps] = e
        chi2[k] = best
        achieved[k] = post.model.builder(
            post.model.to_dict(th[:post.model.ndim])).derived()[quantity]
        best_theta[k] = th.tolist()
        print(f"  target {quantity}={target:11.6f}  achieved {achieved[k]:11.6f}"
              f"  eps={e:7.4f}  chi2={chi2[k]:10.3f}")

    # A second sweep, from the far end back. The forward sweep warm-starts
    # each target from the previous one, which helps only in one direction: a
    # target whose search fails is then seeded from a failure, and the profile
    # acquires local minima that are artefacts of the optimiser rather than
    # features of the likelihood. On the jerk profile the forward sweep left
    # three grid points sitting at the LambdaCDM value while their neighbours
    # sat 1.6 lower, which is impossible for a profile and is what the
    # monotonicity diagnostic was built to catch.
    #
    # A profile is the lower envelope of what is attainable, so taking the
    # better of two sweeps can only improve it, and the sweep costs one more
    # local optimisation per grid point.
    n_improved = 0
    for k in range(len(targets) - 2, -1, -1):
        if best_theta[k + 1] is None:
            continue
        target = float(targets[k])

        def neg_back(sub, target=target):
            if np.any(sub < lows[free]) or np.any(sub > highs[free]):
                return 1e10
            th = np.empty(len(names))
            th[free] = sub
            th[i_eps] = 0.0
            e = _solve_eps_for(post, quantity, target, th, i_eps,
                               lows[i_eps], highs[i_eps])
            if e is None:
                return 1e10
            th[i_eps] = e
            v = post(th)
            return 1e10 if not np.isfinite(v) else -2.0 * v

        x0 = np.asarray(best_theta[k + 1])[free]
        for method, opts in (("Nelder-Mead",
                              dict(maxfev=maxfev, xatol=1e-5, fatol=1e-4)),
                             ("Powell",
                              dict(maxfev=maxfev, xtol=1e-6, ftol=1e-6))):
            r = minimize(neg_back, x0, method=method, options=opts)
            x0 = r.x
            if np.isfinite(chi2[k]) and r.fun >= chi2[k] - 1e-9:
                continue
            if r.fun >= 1e10:
                continue
            e = _solve_eps_for(post, quantity, target, _with(names, free, r.x,
                                                             i_eps),
                               i_eps, lows[i_eps], highs[i_eps])
            if e is None:
                continue
            th = _with(names, free, r.x, i_eps)
            th[i_eps] = e
            chi2[k] = r.fun
            achieved[k] = post.model.builder(
                post.model.to_dict(th[:post.model.ndim])).derived()[quantity]
            best_theta[k] = th.tolist()
            n_improved += 1
    if n_improved:
        print(f"  backward sweep improved {n_improved} grid point(s)")

    ok = np.isfinite(chi2)
    base = {"model": model, "dataset": dataset, "quantity": quantity,
            "n_improved_by_backward_sweep": n_improved,
            "targets": targets.tolist(), "achieved": achieved.tolist(),
            "best_theta": best_theta, "param_names": names,
            "n_unreachable": int((~ok).sum())}
    if not ok.any():
        base.update({"delta_chi2": chi2.tolist(), "limit_95": float("nan"),
                     "unbounded": False, "all_unreachable": True})
        return base

    # The floor the profile is measured from, against the floor the
    # unconstrained maximisation found. These must agree: the profile ranges
    # over a superset of the unconstrained problem at the target it can reach
    # freely, so a positive excess means the constrained search failed, and
    # every Delta chi-square below is then measured from too high a base.
    profile_min = float(np.nanmin(chi2))
    map_chi2 = map_value = None
    if map_path.exists():
        entry = json.loads(map_path.read_text()).get(f"{model}__{dataset}")
        if entry is not None:
            map_chi2 = float(entry["chi2_min"])
            # Where the unconstrained maximum sits in the profiled quantity.
            # If the grid does not sample near it, the profile's floor is not
            # the maximum and every Delta chi-square below is measured from
            # too high a base -- which is how the jerk grid, whose smallest
            # non-zero target was 1e-4, missed a maximum at 1.4e-8.
            bg = post.model.builder(
                post.model.to_dict(np.asarray(entry["theta"])[:post.model.ndim]))
            map_value = float(bg.derived()[quantity])
    excess = None if map_chi2 is None else profile_min - map_chi2
    positive = targets[targets > 0]
    grid_covers = (map_value is not None and positive.size > 0
                   and map_value <= float(targets.max())
                   and map_value >= float(positive.min()))

    chi2 = chi2 - np.nanmin(chi2)
    seq = chi2[ok]
    # Only decreases *above the minimum* count. A profile is expected to fall
    # on its way into the minimum, and counting those made the diagnostic fire
    # on a healthy profile whose grid happens to start on the far side of it.
    i_min = int(np.nanargmin(seq))
    rising = seq[i_min:]
    non_monotone = int(np.sum(np.diff(rising) < -0.5))
    miss = float(np.nanmax(np.abs(achieved[ok] - targets[ok])
                           / np.maximum(np.abs(targets[ok]), 1e-12)))

    above = np.where(chi2 > 2.71)[0]
    unbounded = not above.size
    limit = (float(np.interp(2.71, chi2[: above[0] + 1], targets[: above[0] + 1]))
             if above.size else float("nan"))
    base.update({"delta_chi2": chi2.tolist(), "limit_95": limit,
                 "profile_min_chi2": profile_min,
                 "map_chi2": map_chi2,
                 "map_quantity_value": map_value,
                 "grid_smallest_positive_target": (float(positive.min())
                                                   if positive.size else None),
                 "grid_covers_the_maximum": bool(grid_covers),
                 "profile_min_excess": excess,
                 "max_delta_chi2": float(np.nanmax(chi2)),
                 "n_non_monotone_steps": non_monotone,
                 "max_target_miss_rel": miss,
                 "unbounded": bool(unbounded)})
    return base


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

    # Seed every target with the global best fit, which is the one point
    # guaranteed to be at least as good as anything the screen will find. A
    # profile whose own minimum lies above the model's maximum likelihood is
    # measuring Delta chi-square from the wrong floor: the three profiles run
    # before this was added sat 0.78, 0.12 and 0.56 above it, and the largest
    # rise reported for the convertible fraction was 0.859 where the correct
    # figure from the true floor is about 1.64. Neither crosses the 2.71 the
    # limit uses, so the conclusions were unaffected -- but the numbers were
    # quoted, and they were wrong.
    map_theta = None
    map_path = ROOT / "results" / "map.json"
    if map_path.exists():
        entry = json.loads(map_path.read_text()).get(f"{model}__{dataset}")
        if entry is not None and list(entry["param_names"]) == names:
            map_theta = np.asarray(entry["theta"], dtype=float)

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
    # One-sided 95% limit for one parameter of interest: Delta chi2 = 2.71.
    # If the profile never reaches it, there is no limit, and saying so is the
    # only honest option: an earlier version returned the right-hand end of the
    # grid, which produced a plausible-looking "95% upper limit on eps" of 0.6
    # that was nothing but the value of ``grid[-1]`` and would have become 1.0
    # had the grid been drawn to 1.0.
    above = np.where(chi2 > 2.71)[0]
    unbounded = not above.size
    limit = (float(np.interp(2.71, chi2[: above[0] + 1], grid[: above[0] + 1]))
             if above.size else float("nan"))
    if unbounded:
        print(f"  no limit: the profile never exceeds "
              f"Delta chi2 = {chi2.max():.3f} over [{grid[0]}, {grid[-1]}]")
    return {
        "model": model, "dataset": dataset,
        "eps_grid": grid.tolist(), "delta_chi2": chi2.tolist(),
        "eps_limit_95": limit,
        "unbounded": bool(unbounded),
        "max_delta_chi2": float(chi2.max()),
        "chi2_at_zero": float(chi2[0]),
        "best_theta": [t.tolist() for t in best_theta],
        "param_names": names,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="+", default=["xi_h"])
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--n-grid", type=int, default=17)
    ap.add_argument("--quantity", default=None,
                    help="profile a derived quantity instead of eps")
    ap.add_argument("--log-range", type=float, nargs=2, default=None,
                    metavar=("LO", "HI"),
                    help="log10 range of the target grid; the default suits "
                         "the matter deficit, and the jerk excess is an order "
                         "of magnitude smaller, so a shared grid wastes most "
                         "of its points on unreachable targets")
    args = ap.parse_args()

    print(f"MemAvailable {mem_available_mb():.0f} MB; single process")
    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    for m in args.models:
        what = args.quantity or "eps"
        print(f"\n=== profile in {what}: {m} / {args.data} ===")
        if args.quantity:
            key = f"{m}__{args.data}__{args.quantity}"
            with record(f"profile_{m}_{args.quantity}", "profile in a derived quantity"):
                targets = None
                if args.log_range:
                    lo, hi = args.log_range
                    targets = np.concatenate([[0.0], np.logspace(lo, hi, 12)])
                out[key] = profile_derived(m, args.data, args.quantity,
                                           targets=targets)
            r = out[key]
            msg = ("unbounded within the grid" if r["unbounded"]
                   else f"{r['limit_95']:.5f}")
            print(f"  95% upper limit on {args.quantity}: {msg}")
        else:
            key = f"{m}__{args.data}"
            with record(f"profile_{m}", "profile likelihood in eps"):
                out[key] = profile(m, args.data, args.n_grid)
            r = out[key]
            msg = ("unbounded within the grid" if r["unbounded"]
                   else f"{r['eps_limit_95']:.5f}")
            print(f"  95% upper limit on eps: {msg}")
        OUT.write_text(json.dumps(out, indent=2))
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
