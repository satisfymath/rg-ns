#!/usr/bin/env python3
"""How much of the Bayes factor is the prior?

Replacing the information criteria with the evidence removes an inapplicable
parameter count and replaces it with an honest dependence on the prior volume,
which has to be reported rather than left implicit.  For a uniform prior on a
box ``A`` narrowed to a sub-box ``B``, no new sampling is needed:

    Z_A = (1/|A|) int_A L,        Z_B = (1/|B|) int_B L,
    p_B = int_B L / int_A L       (the posterior mass in B, under prior A)

    =>  ln Z_B = ln Z_A + ln p_B + ln(|A| / |B|).

Every term on the right is available from one run: the evidence it reported and
its equal-weight samples.  The identity is exact; the only error is the Monte
Carlo error on ``p_B``, which is reported alongside and which blows up once B
is so small that few samples land in it.

Reported for each narrowing: the Bayes factor against LambdaCDM under the
narrowed prior, so a reader can see how far the verdict moves when the prior
that the verdict depends on is changed by a factor of a few.
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

from absorb.params import MODELS                                # noqa: E402

POSTERIORS = ROOT / "results" / "posteriors"
EVIDENCE = ROOT / "results" / "evidence.json"
OUT = ROOT / "results" / "prior_sensitivity.json"

#: Parameters that exist only under the alternative.  Narrowing these is the
#: test that matters: they are the ones the data do not identify, so the whole
#: Occam penalty is the volume the model spends on them.
EXTRA = {
    "xi_h": ("eps", "log10_xi", "z_act"),
    "reinforce": ("eps", "log10_gamma0", "alpha_tot", "z_act"),
    "memory": ("eps", "log10_gamma0", "alpha_tot", "r_beta", "log10_tau",
               "z_act"),
}


def narrowed(model: str, samples: np.ndarray, factor: float) -> tuple[float, float, float]:
    """(ln p_B, its standard error, ln|A|/|B|) for shrinking EXTRA by ``factor``.

    Each extra parameter's interval is shrunk about its own centre, keeping the
    prior uniform and keeping the LambdaCDM point eps = 0 inside it.
    """
    m = MODELS[model]
    priors = m.priors()
    inside = np.ones(len(samples), dtype=bool)
    log_volume_ratio = 0.0
    for k, name in enumerate(m.params):
        if name not in EXTRA[model]:
            continue
        p = priors[k]
        lo, hi = p.low, p.high
        if name == "eps":
            # eps is bounded below by zero and the null sits on that boundary;
            # shrink from above only, so the null stays interior to the box.
            new_lo, new_hi = lo, lo + factor * (hi - lo)
        else:
            mid = 0.5 * (lo + hi)
            half = 0.5 * factor * (hi - lo)
            new_lo, new_hi = mid - half, mid + half
        inside &= (samples[:, k] >= new_lo) & (samples[:, k] <= new_hi)
        log_volume_ratio += np.log((hi - lo) / (new_hi - new_lo))
    n_in = int(inside.sum())
    n = len(samples)
    if n_in == 0:
        return float("-inf"), float("nan"), log_volume_ratio
    p_b = n_in / n
    # binomial standard error propagated to the logarithm
    se = float(np.sqrt(p_b * (1 - p_b) / n) / p_b)
    return float(np.log(p_b)), se, float(log_volume_ratio)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="baseline")
    ap.add_argument("--factors", type=float, nargs="+",
                    default=[1.0, 0.5, 0.25, 0.125])
    args = ap.parse_args()

    if not EVIDENCE.exists():
        print("no evidence.json yet")
        return 0
    ev = json.loads(EVIDENCE.read_text())
    ref = ev.get(f"lcdm__{args.data}")
    if ref is None:
        print("no LambdaCDM evidence")
        return 0

    out = {}
    for model in EXTRA:
        key = f"{model}__{args.data}"
        path = POSTERIORS / f"{model}_{args.data}.npz"
        if key not in ev or not path.exists():
            continue
        with np.load(path, allow_pickle=False) as fh:
            samples = np.asarray(fh["samples"])
        rows = []
        print(f"\n{key}  ({len(samples)} samples, "
              f"ln Z = {ev[key]['logz']:.3f})")
        print(f"  {'shrink':>7} {'ln B':>9} {'+/-':>7} {'samples in box':>15}")
        for f in args.factors:
            ln_p, se, ln_vol = narrowed(model, samples, f)
            ln_z = ev[key]["logz"] + ln_p + ln_vol
            ln_b = ln_z - ref["logz"]
            err = float(np.hypot(se, np.hypot(ev[key]["logz_err"],
                                              ref["logz_err"])))
            n_in = int(round(np.exp(ln_p) * len(samples))) if np.isfinite(ln_p) else 0
            rows.append(dict(shrink=f, logz=ln_z, ln_bayes=ln_b, err=err,
                             n_in_box=n_in))
            print(f"  {f:7.3f} {ln_b:+9.3f} {err:7.3f} {n_in:15d}")
        out[key] = dict(model=model, dataset=args.data, rows=rows,
                        ln_bayes_full_prior=rows[0]["ln_bayes"],
                        ln_bayes_span=float(max(r["ln_bayes"] for r in rows)
                                            - min(r["ln_bayes"] for r in rows)))
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"\nwrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
