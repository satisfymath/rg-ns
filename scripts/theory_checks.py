#!/usr/bin/env python3
"""Numerical checks the manuscript quotes in its theory sections.

Two claims in the theory sections rest on measurements rather than on algebra,
and the paper quotes their numbers, so they are computed here and reach the
text as macros like everything else.

1. *The deficit-to-jerk floor does not apply to this model.* The bound
   ``j0 - 1 >= 2 Omega_r0 + (9/2) Delta`` holds when the reduced transfer
   ``q = Q_V/(3 Mpl^2 H0^2 H)`` is non-decreasing up to today. The activation
   switch turns the transfer on at ``z_act`` and the rate then falls relative
   to the expansion, so q peaks at the activation redshift and declines. This
   records how often the hypothesis holds over the prior, and how badly the
   floor fails when it does not.

2. *Massive neutrinos strengthen the jerk bound rather than threatening it.*
   The jerk theorem's hypotheses omitted the one massive eigenstate every fit
   carries. Its contribution is non-negative because the pressure of a species
   going non-relativistic falls monotonically, and this records its size.
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

from absorb.background import pressure_nu                       # noqa: E402
from absorb.params import MODELS                                # noqa: E402

OUT = ROOT / "results" / "theory_checks.json"
FLOOR_COEFFICIENT = 4.5          # the 9/2 in the bound


def deficit_floor(model: str = "xi_h", n_draws: int = 400,
                  seed: int = 20260909) -> dict:
    m = MODELS[model]
    priors = m.priors()
    lo = np.array([p.low for p in priors])
    hi = np.array([p.high for p in priors])
    rng = np.random.default_rng(seed)

    ratios, held = [], 0
    for _ in range(n_draws):
        theta = lo + rng.random(len(lo)) * (hi - lo)
        try:
            bg = m.builder(m.to_dict(theta))
            d = bg.derived()
        except Exception:                                       # noqa: BLE001
            continue
        if d["matter_deficit"] <= 1e-10:
            continue
        ratios.append(d["jerk_excess"] / d["matter_deficit"])
        held += int(bg.transfer_diagnostics()["q_nondecreasing"])

    ratios = np.asarray(ratios)
    violated = int(np.sum(ratios < FLOOR_COEFFICIENT))
    return {
        "model": model,
        "n_draws_with_transfer": int(ratios.size),
        "n_hypothesis_holds": held,
        "n_floor_violated": violated,
        "median_ratio": float(np.median(ratios)),
        "min_ratio": float(ratios.min()),
        "max_ratio": float(ratios.max()),
        "floor_coefficient": FLOOR_COEFFICIENT,
    }


def peak_at_activation(model: str = "xi_h") -> dict:
    """Where the reduced transfer peaks, over a range of activation redshifts."""
    m = MODELS[model]
    worst = 0.0
    for z_act in (0.3, 0.5, 1.0, 2.0, 5.0, 10.0, 25.0):
        bg = m.builder(m.to_dict([0.02237, 0.1177, 0.30, 0.5, -2.0, z_act]))
        d = bg.transfer_diagnostics()
        worst = max(worst, abs(d["z_of_peak"] - z_act) / z_act)
    return {"max_relative_offset_of_peak": float(worst),
            "n_activation_redshifts": 7}


def neutrino_jerk_term(z_max: float = 1500.0) -> dict:
    m = MODELS["lcdm"]
    bg = m.builder(m.to_dict([0.02237, 0.1177, 0.3266]))
    z = np.linspace(0.0, z_max, 4000)
    a = 1.0 / (1.0 + z)
    dust, rad, nu, V = bg._omegas(z)
    E2 = dust + rad + nu + V
    _, dpnu = pressure_nu(a)
    term = -1.5 * dpnu / E2
    return {
        "today": float(term[0]),
        "max": float(term.max()),
        "z_of_max": float(z[int(np.argmax(term))]),
        "min": float(term.min()),
        "non_negative_everywhere": bool(np.all(term >= 0.0)),
        "two_omega_r_today": float(2.0 * rad[0] / E2[0]),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--draws", type=int, default=400)
    args = ap.parse_args()

    out = {
        "deficit_floor": deficit_floor(n_draws=args.draws),
        "transfer_peak": peak_at_activation(),
        "neutrino_jerk_term": neutrino_jerk_term(),
    }
    f = out["deficit_floor"]
    print(f"  deficit floor: hypothesis holds in {f['n_hypothesis_holds']} of "
          f"{f['n_draws_with_transfer']} draws; floor violated in "
          f"{f['n_floor_violated']}; median ratio {f['median_ratio']:.3f} "
          f"against the required {f['floor_coefficient']}")
    n = out["neutrino_jerk_term"]
    print(f"  neutrino jerk term: {n['today']:.3e} today, max {n['max']:.3e} "
          f"at z = {n['z_of_max']:.0f}, non-negative: "
          f"{n['non_negative_everywhere']}")
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
