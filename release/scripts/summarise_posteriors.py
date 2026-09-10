#!/usr/bin/env python3
"""Posterior summaries for the manuscript, from the nested samples.

The ensemble chains for the extended models were not fit to quote from: along
the directions that are unidentified when the model reduces to LambdaCDM they
filled their priors instead of sampling them, so a median or a percentile taken
from one describes the prior. Those entries are replaced here by summaries of
the equal-weight nested samples, and the entry records which sampler it came
from so that the two can never be confused again.

LambdaCDM keeps its ensemble chain, which is healthy: acceptance 0.44, 157
autocorrelation times long, and it passes the stability gate.
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

from absorb.params import MODELS                                # noqa: E402
from run_mcmc import derived_summary                            # noqa: E402

POSTERIORS = ROOT / "results" / "posteriors"
RESULTS = ROOT / "results" / "results.json"


def summarise(model: str, samples: np.ndarray) -> dict:
    m = MODELS[model]
    params = {}
    for i, name in enumerate(m.params):
        col = samples[:, i]
        med = float(np.median(col))
        lo, hi = np.percentile(col, [16, 84])
        params[name] = {"value": med, "err_lo": med - float(lo),
                        "err_hi": float(hi) - med,
                        "hi95": float(np.percentile(col, 95)),
                        "lo95": float(np.percentile(col, 5))}
    return {"sampler": "nested", "n_samples": int(samples.shape[0]),
            "n_params": m.ndim, "parameters": params,
            "derived": derived_summary(model, samples)}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", default="baseline")
    args = ap.parse_args()

    results = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    chains = results.setdefault("chains", {})

    files = sorted(POSTERIORS.glob(f"*_{args.data}.npz"))
    if not files:
        print(f"no posterior samples in {POSTERIORS}")
        return 0
    for path in files:
        model = path.name[: -len(f"_{args.data}.npz")]
        if model not in MODELS:
            continue
        if model == "lcdm":
            print(f"  {model}: keeping the ensemble chain (it is healthy)")
            continue
        with np.load(path, allow_pickle=False) as fh:
            samples = np.asarray(fh["samples"])
        key = f"{model}__{args.data}"
        old = chains.get(key, {})
        entry = summarise(model, samples)
        # keep the fields that describe the data, drop the frozen chain's
        # convergence metadata rather than carrying it beside nested summaries
        for k in ("n_data",):
            if k in old:
                entry[k] = old[k]
        chains[key] = entry
        d = entry["derived"]
        print(f"  {key}: {entry['n_samples']} samples; "
              f"Delta < {d['matter_deficit']['hi95']:.4f} (95%), "
              f"f0 < {d['f0']['hi95']:.4f} (95%)")
    RESULTS.write_text(json.dumps(results, indent=2, sort_keys=True))
    print(f"wrote {RESULTS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
