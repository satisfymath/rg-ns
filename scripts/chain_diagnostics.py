#!/usr/bin/env python3
"""Mixing diagnostics for every stored chain, as a results file.

The manuscript quotes the numbers that condemned the first sampling attempt --
acceptance, move rate early and late, the fraction of ensemble proposals that
fall outside the prior box. They describe chains that have been superseded and
will never change, which is exactly the argument for writing them down once and
generating the macros from them rather than typing them into the text, where
inline maths hides them from check_numbers.

Cheap by construction: everything here is read from the stored chain, and the
proposal test replays differential-evolution moves against the prior box
without evaluating a single likelihood.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

import numpy as np                                              # noqa: E402

from absorb.constants import SEED                               # noqa: E402
from absorb.params import MODELS                                # noqa: E402

OUT = ROOT / "results" / "chain_diagnostics.json"
#: emcee's default differential-evolution scale, 2.38 / sqrt(2 ndim).
DE_GAMMA0 = 2.38


def outside_prior_fraction(ensemble: np.ndarray, low: np.ndarray,
                           high: np.ndarray, gamma: float,
                           n_trials: int = 4000, seed: int = SEED) -> float:
    """Fraction of differential-evolution proposals that leave the prior box."""
    rng = np.random.default_rng(seed)
    n = ensemble.shape[0]
    out = 0
    for _ in range(n_trials):
        i, j, k = rng.choice(n, 3, replace=False)
        prop = ensemble[i] + gamma * (ensemble[j] - ensemble[k])
        out += int(np.any(prop < low) or np.any(prop > high))
    return out / n_trials


def diagnose(path: Path) -> dict | None:
    import h5py

    name = path.stem
    model = next((m for m in MODELS if name.startswith(m + "_")), None)
    if model is None:
        return None
    with h5py.File(path, "r", locking=False) as fh:
        g = fh["mcmc"]
        it = int(g.attrs["iteration"])
        if it < 200:
            return None
        log_prob = np.array(g["log_prob"][:it])
        accepted = np.array(g["accepted"])
        last = np.array(g["chain"][it - 1])
    n_walk = log_prob.shape[1]
    moved = np.diff(log_prob, axis=0) != 0
    try:
        from emcee.autocorr import integrated_time
        with h5py.File(path, "r", locking=False) as fh:
            chain = np.array(fh["mcmc"]["chain"][:it])
        tau = float(np.max(integrated_time(chain, tol=0)))
    except Exception:                                           # noqa: BLE001
        tau = float("nan")
    w = max(1, moved.shape[0] // 10)

    priors = MODELS[model].priors()
    low = np.array([p.low for p in priors])
    high = np.array([p.high for p in priors])
    gamma = DE_GAMMA0 / np.sqrt(2.0 * len(priors))
    return {
        "model": model,
        "n_steps": it,
        "n_walkers": n_walk,
        "acceptance": float(accepted.sum() / (it * n_walk)),
        "move_rate_early": float(moved[:w].mean()),
        "move_rate_late": float(moved[-w:].mean()),
        "outside_prior_fraction": outside_prior_fraction(
            last[:, :len(priors)], low, high, gamma),
        "de_gamma": float(gamma),
        "n_nonfinite_log_prob": int((~np.isfinite(log_prob)).sum()),
        "tau_max": tau,
        "length_in_tau": float(it / tau) if tau == tau and tau > 0 else float("nan"),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.parse_args()
    out = {}
    for p in sorted(glob.glob(str(ROOT / "results" / "chains" / "*.h5"))):
        d = diagnose(Path(p))
        if d is None:
            continue
        key = Path(p).stem
        out[key] = d
        print(f"  {key:34s} acc {d['acceptance']:.4f}  move "
              f"{d['move_rate_early']:.4f} -> {d['move_rate_late']:.4f}  "
              f"outside prior {d['outside_prior_fraction']:.3f}")
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
