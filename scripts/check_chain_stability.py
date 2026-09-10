#!/usr/bin/env python3
"""Check that the quantities the paper quotes are stable across the chain.

A chain can satisfy an autocorrelation criterion on its sampled parameters and
still give an unreliable answer for a derived quantity.  In this model the raw
parameters are strongly degenerate near the LambdaCDM boundary, where the rate
and the convertible fraction both vanish and the remaining parameters become
unconstrained.  What the paper reports is the derived converted fraction and
the matter deficit, as one-sided upper limits, so this script recomputes those
limits on the first and second half of each chain and fails if they disagree by
more than a stated tolerance.
"""
from __future__ import annotations

import argparse
import glob
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from absorb.params import MODELS                                # noqa: E402

TOL = 0.25          # allowed relative drift of the 95th percentile
QUANTITIES = ("f0", "matter_deficit")
STEP = 40           # thinning used when re-deriving along the chain


def derived_series(model: str, chain: np.ndarray) -> dict[str, np.ndarray]:
    m = MODELS[model]
    sub = chain[::STEP]
    out = {q: np.full(sub.shape[:2], np.nan) for q in QUANTITIES}
    for i in range(sub.shape[0]):
        for j in range(sub.shape[1]):
            try:
                d = m.builder(m.to_dict(sub[i, j])).derived()
            except Exception:                                   # noqa: BLE001
                continue
            for q in QUANTITIES:
                out[q][i, j] = d.get(q, np.nan)
    return out


def main() -> int:
    import h5py

    ap = argparse.ArgumentParser()
    ap.add_argument("--tol", type=float, default=TOL)
    args = ap.parse_args()

    failures = []
    for path in sorted(glob.glob(str(ROOT / "results" / "chains" / "*.h5"))):
        name = Path(path).stem
        model = name.rsplit("_", 1)[0]
        if model not in MODELS:
            continue
        with h5py.File(path, "r") as fh:
            it = int(fh["mcmc"].attrs["iteration"])
            if it < 500:
                print(f"  {name}: only {it} steps, skipped")
                continue
            chain = fh["mcmc"]["chain"][:it]
        if MODELS[model].ndim == 3:            # LambdaCDM has nothing to derive
            print(f"  {name}: no conversion parameters, skipped")
            continue

        series = derived_series(model, chain)
        burn = series[QUANTITIES[0]].shape[0] // 3
        for q, arr in series.items():
            post = arr[burn:]
            post = post[np.isfinite(post).all(axis=1)]
            if post.size < 200:
                continue
            flat = post.ravel()
            half = len(flat) // 2
            lo = float(np.percentile(flat[:half], 95))
            hi = float(np.percentile(flat[half:], 95))
            scale = max(abs(lo), abs(hi), 1e-12)
            drift = abs(hi - lo) / scale
            mark = "ok " if drift <= args.tol else "FAIL"
            print(f"  [{mark}] {name:24s} {q:16s} "
                  f"95% limit {lo:.4f} -> {hi:.4f}  drift {drift:.0%}")
            if drift > args.tol:
                failures.append(f"{name}/{q}: 95% limit drifts {drift:.0%} "
                                f"across the chain ({lo:.4f} vs {hi:.4f})")

    if failures:
        print("\ncheck_chain_stability FAILED:")
        for f in failures:
            print("  - " + f)
        print("\nThe reported limits are not converged; run longer chains.")
        return 1
    print("\ncheck_chain_stability: reported limits stable across each chain")
    return 0


if __name__ == "__main__":
    sys.exit(main())
