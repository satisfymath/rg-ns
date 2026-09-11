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

from absorb import datasets
from absorb import jsonstore as store                                     # noqa: E402
from absorb.constants import SEED                               # noqa: E402
from absorb.resources import record                             # noqa: E402
from absorb.sampling import (MAP_BUDGET_PER_DIM, Posterior,      # noqa: E402
                             find_map)

OUT = ROOT / "results" / "map.json"

#: The frozen brute-force answer: forty full Nelder-Mead runs from random prior
#: points, eight hours of compute, kept so that a cheaper protocol cannot
#: silently return a worse maximum. A chi-square is a value attained at an
#: actual point in parameter space, so the reference is a *ceiling*: any run
#: that lands above it has failed to find something already known to exist.
#: LambdaCDM reproduces to 1e-9, which is what certifies that the likelihood
#: has not changed since the reference was taken.
REFERENCE = ROOT / "results" / "map_reference.json"

#: How far above the reference a run may land before it counts as a failure.
#: The reference was itself an optimisation, so exact equality is not expected;
#: 0.01 is a hundredth of the smallest chi-square difference in the comparison
#: table and a tenth of the profile-likelihood step.
REFERENCE_TOL = 0.01


def reference_ceiling(model: str, dataset: str, ref: dict) -> tuple[float, str]:
    """The lowest chi-square this model is already known to be able to reach.

    A model cannot fit worse than any model it contains, so a submodel's
    reference constrains it too. That is how the reverse-channel and memory
    models get a ceiling even though the brute-force run only covered three.
    """
    best, via = float("inf"), ""
    for name in [model] + CONTAINS.get(model, []):
        entry = ref.get(f"{name}__{dataset}")
        if entry and entry["chi2_min"] < best:
            best, via = float(entry["chi2_min"]), name
    return best, via

#: Which models contain which, as submodels. A model that contains another
#: cannot fit worse than it, so the larger search is seeded with the smaller
#: model's answer embedded. Without this the nine-parameter model returned a
#: chi-square 1.55 *worse* than the seven-parameter model it contains, which is
#: impossible and would have gone into the comparison table.
CONTAINS = {
    "xi_h": ["lcdm"],
    "reinforce": ["lcdm"],
    "memory": ["lcdm", "reinforce"],
    "track_b": ["lcdm", "reinforce", "memory"],
}

#: Values that switch a parameter off, so that a larger model reduces to a
#: smaller one when the extra parameters take them.
NEUTRAL = {
    "eps": 0.0, "r_beta": 0.0, "log10_tau": 0.0, "alpha_tot": 0.0,
    "log10_gamma_down": None,          # None means "the bottom of its prior"
}


def embed(sub_names, sub_theta, model: str) -> np.ndarray:
    """Put a submodel's best fit into the larger model's parameter vector."""
    from absorb.params import MODELS, PRIORS

    have = dict(zip(sub_names, sub_theta))
    out = []
    for name in MODELS[model].params:
        if name in have:
            out.append(have[name])
        elif name in NEUTRAL:
            v = NEUTRAL[name]
            out.append(PRIORS[name].low if v is None else v)
        else:
            pr = PRIORS[name]
            out.append(0.5 * (pr.low + pr.high))
    return np.asarray(out, dtype=float)


def best_fit(model: str, dataset: str, n_restarts: int, seed: int,
             n_screen: int = 3000, n_polish: int = 8,
             known: dict | None = None) -> dict:
    """Best fit under one protocol: screen cheaply, then refine what is worth it.

    Three protocols have been tried here and two failed, so the history is
    worth recording. A per-dimension budget from a handful of random starts
    returned 1435.807 for the six-parameter model where the maximum is
    1434.879. Forty full Nelder-Mead runs from random prior points did find it,
    but took over eight hours for five models, because a random draw usually
    lands where the background integration is stiff -- the cost per likelihood
    call rises from about 15 ms near the fit to 80 ms out in the prior -- and
    the simplex then spends its whole budget there.

    What this does instead: evaluate a Latin hypercube once, which pays the
    high per-call cost only once per point, then run the simplex only from the
    best few, which are by construction in the cheap region, and polish the
    winner until it stops moving. The recorded diagnostics are unchanged, and
    ``reproduces_reference`` compares against the brute-force answer where one
    is known, so the cheaper protocol cannot silently return a worse maximum.
    """
    from scipy.optimize import minimize
    from scipy.stats import qmc

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

    design = qmc.LatinHypercube(d=post.ndim, seed=seed).random(n_screen)
    screen = lo + design * (hi - lo)
    values = np.array([neg(x) for x in screen])
    order = np.argsort(values)

    starts = [screen[i] for i in order[:n_restarts]]
    # Seed with every submodel's answer, embedded. This is what makes the
    # chi-square column monotone in the nesting rather than accidentally so.
    seeded = 0
    for sub in CONTAINS.get(model, []):
        entry = (known or {}).get(f"{sub}__{dataset}")
        if entry is None:
            continue
        x = embed(entry["param_names"], entry["theta"], model)
        if np.all(x >= lo) and np.all(x <= hi):
            starts.insert(0, x)
            seeded += 1
    best, best_x = np.inf, None
    reached = []
    for x0 in starts:
        r = minimize(neg, x0, method="Nelder-Mead",
                     options=dict(maxfev=budget, xatol=1e-8, fatol=1e-8))
        reached.append(r.fun)
        if r.fun < best:
            best, best_x = r.fun, r.x

    # Polish. Nelder-Mead alone stalls on the curved degeneracy between the
    # rate normalisation and the activation redshift: it contracts along the
    # ridge instead of following it, and stops 0.14 above a point the
    # brute-force run is known to have reached. Alternating with Powell, which
    # searches along directions rather than by reflection, follows the ridge;
    # the two together reach the reference where either alone does not.
    for _ in range(n_polish):
        improved = False
        for method, opts in (("Nelder-Mead",
                              dict(maxfev=2 * budget, xatol=1e-10, fatol=1e-10)),
                             ("Powell",
                              dict(maxfev=2 * budget, xtol=1e-10, ftol=1e-10))):
            r = minimize(neg, best_x, method=method, options=opts)
            if r.fun < best - 1e-9:
                best, best_x, improved = r.fun, r.x, True
        if not improved:
            break

    # If a value is already known to be attainable and we are above it, the
    # search has failed rather than converged, so spend more on it: kick the
    # best point along each axis in turn and re-polish. Silence here was the
    # defect -- the previous protocol reported "converged" while sitting above
    # a maximum recorded in this repository.
    ref_all = json.loads(REFERENCE.read_text()) if REFERENCE.exists() else {}
    target, _via = reference_ceiling(model, dataset, ref_all)
    rng = np.random.default_rng(seed + 1)
    n_kicks = 0
    while np.isfinite(target) and best > target + REFERENCE_TOL and n_kicks < 40:
        n_kicks += 1
        scale = 10.0 ** (-rng.integers(1, 4))          # 0.1, 0.01 or 0.001
        x0 = np.clip(best_x + scale * (hi - lo) * rng.normal(size=post.ndim),
                     lo, hi)
        for method, opts in (("Nelder-Mead", dict(maxfev=budget, xatol=1e-10,
                                                  fatol=1e-10)),
                             ("Powell", dict(maxfev=budget, xtol=1e-10,
                                             ftol=1e-10))):
            r = minimize(neg, x0, method=method, options=opts)
            if r.fun < best - 1e-9:
                best, best_x = r.fun, r.x
            x0 = r.x

    reached = np.asarray([v for v in reached if v < 1e9])
    spread = float(reached.max() - reached.min()) if reached.size > 1 else float("nan")
    # How many independent refinements agreed with the best refinement, and
    # separately how much the final polishing added. Comparing the refinements
    # against the *polished* value counts none of them whenever polishing helps
    # at all, which says nothing about whether the search was reliable.
    best_refined = float(reached.min()) if reached.size else float("nan")
    n_at_best = int(np.sum(reached < best_refined + 0.01)) if reached.size else 0
    polish_gain = float(best_refined - best) if reached.size else float("nan")
    ceiling, via = target, _via
    shortfall = float(best - ceiling) if np.isfinite(ceiling) else float("nan")

    on_edge = [n for n, x, l, h in zip(post.param_names, best_x, lo, hi)
               if abs(x - l) < 1e-6 * (h - l) or abs(x - h) < 1e-6 * (h - l)]
    return dict(model=model, dataset=dataset, ndim=post.ndim,
                chi2_min=float(best), chi2_spread=spread,
                n_screen=n_screen, n_refined=len(starts),
                n_seeded_from_submodels=seeded,
                n_reaching_best=n_at_best,
                best_before_polish=best_refined,
                polish_gain=polish_gain,
                n_reference_kicks=n_kicks,
                converged=bool(n_at_best >= 2),
                reference_chi2=(None if not np.isfinite(ceiling) else ceiling),
                reference_via=via,
                reference_shortfall=(None if not np.isfinite(shortfall)
                                     else shortfall),
                reproduces_reference=(True if not np.isfinite(shortfall)
                                      else bool(shortfall <= REFERENCE_TOL)),
                budget_evals=budget, budget_per_dim=MAP_BUDGET_PER_DIM,
                on_prior_edge=on_edge,
                theta=np.asarray(best_x).tolist(),
                param_names=list(post.param_names))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="+",
                    default=["lcdm", "xi_h", "reinforce", "memory"])
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--restarts", type=int, default=8,
                    help="how many screened points get a simplex")
    ap.add_argument("--screen", type=int, default=3000)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    out = json.loads(OUT.read_text()) if OUT.exists() else {}
    for m in args.models:
        tag = f"{m}__{args.data}"
        with record(f"map_{tag}", f"{args.restarts} restarts"):
            out[tag] = best_fit(m, args.data, args.restarts, args.seed,
                                n_screen=args.screen, known=out)
        # Persist before reporting. The other order cost a validation run: a
        # KeyError in the print discarded a completed maximisation, left the
        # previous protocol's value in place, and the comparison that was
        # supposed to check the new protocol compared the old answer with
        # itself.
        out = store.update(OUT, {tag: out[tag]})
        e = out[tag]
        edge = (f", on the prior edge in {','.join(e['on_prior_edge'])}"
                if e["on_prior_edge"] else "")
        mark = "" if e["converged"] else "   [NOT CONVERGED]"
        if e.get("reference_chi2") is not None and not e["reproduces_reference"]:
            mark += (f"   [ABOVE THE {e['reference_via']} REFERENCE BY "
                     f"{e['reference_shortfall']:.4f}]")
        seed_note = (f", {e['n_seeded_from_submodels']} submodel seed(s)"
                     if e.get("n_seeded_from_submodels") else "")
        print(f"  {tag:24s} chi2_min = {e['chi2_min']:.4f}  "
              f"({e['n_reaching_best']}/{e['n_refined']} refinements agreed, "
              f"polish gained {e['polish_gain']:.4f}{seed_note}{edge}){mark}",
              flush=True)

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
