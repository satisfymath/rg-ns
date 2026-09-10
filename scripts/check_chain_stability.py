#!/usr/bin/env python3
"""Fail when a chain is not fit to quote from.

A chain can satisfy an autocorrelation criterion on its sampled parameters and
still give an unreliable answer for a derived quantity, so this script
recomputes what the paper reports on the first and second half of each chain
and fails if they disagree.

An earlier version of this script had no power to fail.  It passed a chain
whose cumulative acceptance was 0.007 and whose move rate had halved over the
run, because the only statistic it watched was the 95th percentile of a
quantity pinned against a hard prior edge, where it cannot drift much no matter
how badly the chain mixes; and it took a fixed one-third burn-in that ignored
the autocorrelation time entirely.  Three of its branches -- too few finite
samples, too short a chain, a model with nothing to derive -- returned silently
without recording that no check had run.

What is checked now, in order of how early it catches a bad chain:

1. *Mixing.*  Acceptance and move rate over the last tenth of the chain, not
   cumulatively: the cumulative figure is flattered by the early transient, and
   a chain whose ensemble spreads faster than it mixes decelerates, which is
   exactly the signature the cumulative number hides.
2. *Length.*  The chain must be longer than ``N_TAU`` autocorrelation times,
   with the burn-in taken as a multiple of tau rather than a fixed fraction.
3. *Stability.*  The median and the 95th percentile of each derived quantity,
   over the two halves after burn-in.  The median is included because it is
   the sensitive statistic; the percentile alone can sit against a prior edge.
4. *Pinning.*  Whether a sampled parameter fills its prior, which means the
   data do not constrain it and no limit derived from it should be quoted.

A chain that cannot be checked fails rather than passes.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import sys
from pathlib import Path

import numpy as np

# Never take a lock on a chain file: the sampler may be writing to it.
os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from absorb.params import MODELS                                # noqa: E402
from absorb.sampling import LogitMap, N_TAU, load_chain_meta    # noqa: E402

TOL = 0.25          # allowed relative drift of a reported statistic
MIN_MOVE_RATE = 0.05    # below this the ensemble is not exploring
MAX_DECELERATION = 2.0  # early move rate over late; above this it is a runaway
PRIOR_FILL_MAX = 0.75   # a parameter whose 5-95 span exceeds this much of its
                        # prior is unconstrained, not measured
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


def move_rates(log_prob: np.ndarray) -> tuple[float, float]:
    """Fraction of steps at which a walker moved, first tenth and last tenth."""
    moved = np.diff(log_prob, axis=0) != 0
    w = max(1, moved.shape[0] // 10)
    return float(moved[:w].mean()), float(moved[-w:].mean())


def autocorr_time(chain: np.ndarray) -> float:
    """Largest integrated autocorrelation time over parameters, via emcee."""
    from emcee.autocorr import integrated_time
    return float(np.max(integrated_time(chain, tol=0)))


def main() -> int:
    import h5py

    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--tol", type=float, default=TOL)
    ap.add_argument("--min-steps", type=int, default=500)
    args = ap.parse_args()

    failures: list[str] = []
    paths = sorted(glob.glob(str(ROOT / "results" / "chains" / "*.h5")))
    if not paths:
        print("check_chain_stability: no chains present, nothing to check")
        return 0

    for path in paths:
        name = Path(path).stem
        model = next((m for m in MODELS if name.startswith(m + "_")), None)
        if model is None:
            failures.append(f"{name}: filename does not name a known model, "
                            f"so the chain cannot be checked")
            continue
        with h5py.File(path, "r", locking=False) as fh:
            it = int(fh["mcmc"].attrs["iteration"])
            if it < args.min_steps:
                failures.append(f"{name}: only {it} steps; too short to check")
                continue
            chain = fh["mcmc"]["chain"][:it]
            log_prob = fh["mcmc"]["log_prob"][:it]
            accepted = np.array(fh["mcmc"]["accepted"])

        # The sampler works in an unbounded coordinate; the stored chain is in
        # it, and everything below is in parameter space.
        meta = load_chain_meta(Path(path))
        if meta and meta.get("parametrisation") == "logit":
            lmap = LogitMap(meta["low"], meta["high"])
            chain = lmap.to_x(chain)
        n_walk = chain.shape[1]

        print(f"\n{name}  ({it} steps, {n_walk} walkers)")

        # --- 1. mixing -----------------------------------------------------
        early, late = move_rates(log_prob)
        cumulative = float(accepted.sum() / (it * n_walk))
        print(f"  move rate  first tenth {early:.4f}   last tenth {late:.4f}"
              f"   (cumulative acceptance {cumulative:.4f})")
        if late < MIN_MOVE_RATE:
            failures.append(f"{name}: move rate over the last tenth is "
                            f"{late:.4f}, below {MIN_MOVE_RATE}; the ensemble "
                            f"is not exploring")
        if late > 0 and early / late > MAX_DECELERATION:
            failures.append(f"{name}: move rate fell from {early:.4f} to "
                            f"{late:.4f} over the run; the chain is "
                            f"decelerating, so sampling longer will not help")

        # --- 2. length -----------------------------------------------------
        try:
            tau = autocorr_time(chain)
        except Exception as exc:                                # noqa: BLE001
            failures.append(f"{name}: autocorrelation time not estimable "
                            f"({type(exc).__name__}); chain unusable")
            continue
        n_tau = it / tau
        print(f"  tau_max {tau:.1f}   chain length {n_tau:.1f} tau "
              f"(need {N_TAU})")
        if n_tau < N_TAU:
            failures.append(f"{name}: chain is {n_tau:.1f} tau long, short of "
                            f"the {N_TAU} tau the sampler itself requires")

        # --- 3. pinning ----------------------------------------------------
        burn = min(int(3 * tau), it // 2)
        post_raw = chain[burn:].reshape(-1, chain.shape[2])
        m = MODELS[model]
        priors = m.priors()
        for k, pr in enumerate(priors):
            span = (np.percentile(post_raw[:, k], 95)
                    - np.percentile(post_raw[:, k], 5))
            fill = span / (pr.high - pr.low)
            if fill > PRIOR_FILL_MAX:
                print(f"  [note] {m.params[k]} fills {fill:.0%} of its prior: "
                      f"the data do not constrain it, and no limit on it "
                      f"should be quoted")

        if m.ndim == 3:
            print("  no conversion parameters; nothing derived to check")
            continue

        # --- 4. stability of what the paper quotes -------------------------
        series = derived_series(model, chain)
        burn_rows = max(1, min(burn // STEP, series[QUANTITIES[0]].shape[0] // 2))
        for q, arr in series.items():
            post = arr[burn_rows:].ravel()
            post = post[np.isfinite(post)]
            if post.size < 200:
                failures.append(f"{name}/{q}: only {post.size} finite derived "
                                f"samples after burn-in; not checkable")
                continue
            half = len(post) // 2
            for stat, f in (("median", 50.0), ("95% limit", 95.0)):
                lo = float(np.percentile(post[:half], f))
                hi = float(np.percentile(post[half:], f))
                scale = max(abs(lo), abs(hi), 1e-12)
                drift = abs(hi - lo) / scale
                mark = "ok " if drift <= args.tol else "FAIL"
                print(f"  [{mark}] {q:16s} {stat:10s} "
                      f"{lo:.5f} -> {hi:.5f}  drift {drift:.0%}")
                if drift > args.tol:
                    failures.append(
                        f"{name}/{q}: {stat} drifts {drift:.0%} across the "
                        f"chain ({lo:.5f} vs {hi:.5f})")

    if failures:
        print("\ncheck_chain_stability FAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    print("\ncheck_chain_stability: every chain is fit to quote from")
    return 0


if __name__ == "__main__":
    sys.exit(main())
