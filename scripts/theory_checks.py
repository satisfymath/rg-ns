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
from absorb.growth import Growth                                # noqa: E402
from absorb.params import MODELS                                # noqa: E402

OUT = ROOT / "results" / "theory_checks.json"
FLOOR_COEFFICIENT = 4.5          # the 9/2 in the bound
#: Deficits below this are numerically indistinguishable from zero and
#: their ratio to the jerk excess is meaningless.
MIN_DEFICIT = 1e-6


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
        # A draw whose deficit is at the numerical floor has a ratio of
        # nothing over nothing: the raw minimum over the prior came out as
        # -4e-150, which is a roundoff artefact and not a physical extreme.
        if d["matter_deficit"] <= MIN_DEFICIT:
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
        # percentiles, not extremes: with 400 draws the extremes are single
        # samples and move by orders of magnitude between seeds
        "ratio_p05": float(np.percentile(ratios, 5)),
        "ratio_p95": float(np.percentile(ratios, 95)),
        "min_ratio": float(ratios.min()),
        "max_ratio": float(ratios.max()),
        "min_deficit_used": MIN_DEFICIT,
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


class _NoTransferGrowth(Growth):
    """The same background, with the growth equation blind to the transfer.

    ``g_c`` is what the transfer contributes to growth, so switching only it
    off on an otherwise identical expansion history separates the transfer's
    effect on the growth of structure from its effect on H(z).
    """

    def _coeffs(self, N):
        EpoverE, Omega_m, gc = super()._coeffs(N)
        return EpoverE, Omega_m, np.zeros_like(gc)


def growth_signature(model: str = "xi_h", z: float = 2.0) -> dict:
    """The opposite-sign growth signature, tested against the right reference.

    Section 9 asserted that "at z = 2 in a representative fit" the density
    growth rate exceeds unity while the redshift-space rate falls below it,
    naming neither the fit nor the numbers. The comparison is also against the
    wrong reference: ``eq:perturbations-growth-signature`` is an expansion
    about matter domination, where the unperturbed rate is 1, and by z = 2 dark
    energy has already pulled LambdaCDM's own rate down to about 0.96. Both
    rates are then below 1 for reasons that have nothing to do with the
    transfer, and the stated check fails while the physics it describes holds.

    The reference that isolates the signature is the same background with
    ``g_c`` removed from the growth equation. Against it the prediction is
    reproduced: the density growth rate is raised and the redshift-space rate
    lowered, at every parameter point and redshift tried.
    """
    m = MODELS[model]
    theta = [0.02237, 0.1177, 0.15, 0.6, -1.0, 5.0]
    bg = m.builder(m.to_dict(theta))
    g, g0 = Growth(bg), _NoTransferGrowth(bg)

    def at(gr, zz):
        return float(np.atleast_1d(gr.f_growth(zz))[0])

    f_g = at(g, z)
    f_ref = at(g0, z)
    f_rsd = float(np.atleast_1d(g.f_rsd(z))[0])

    # and check it is not a one-point accident
    ok = True
    for za, eps, lx in ((5.0, 0.6, -1.0), (5.0, 0.3, -1.5), (10.0, 0.6, -1.0)):
        b2 = m.builder(m.to_dict([0.02237, 0.1177, 0.15, eps, lx, za]))
        ga, gb = Growth(b2), _NoTransferGrowth(b2)
        for zz in (2.0, 1.0, 0.5):
            ok &= (at(ga, zz) > at(gb, zz)
                   and float(np.atleast_1d(ga.f_rsd(zz))[0]) < at(gb, zz))

    return {
        "model": model, "z": z,
        "params": dict(zip(m.params, theta)),
        "f_growth": f_g,
        "f_growth_no_transfer": f_ref,
        "f_rsd": f_rsd,
        "raises_growth": bool(f_g > f_ref),
        "lowers_rsd": bool(f_rsd < f_ref),
        "holds_at_every_point_tried": bool(ok),
        "n_points_tried": 9,
    }


def marginalisation_jacobian() -> dict:
    """The constant the reported -2 log L carries from marginalising over M_B.

    Correct as -2 log L, and it cancels from every difference, but it means the
    quantity is not a chi-square. The comparison table's caption says so and
    quotes this number, so this is where the number comes from.
    """
    from scipy.linalg import cho_solve

    from absorb.data import pantheon

    out = {}
    for label, sh0es in (("baseline", False), ("with_sh0es", True)):
        d = pantheon.load_pantheon(sh0es)
        ones = np.ones(d.n)
        e0 = float(ones @ cho_solve(d.cho, ones))
        out[label] = float(np.log(e0 / (2.0 * np.pi)))
    return out


def recombination_recipe_systematic() -> dict:
    """How much of the compressed-CMB recipe's error the calibration absorbs.

    The sound horizon is corrected by a single constant calibrated at one
    reference cosmology. That is defensible only if the recipe's error is
    close to constant over the range the fits explore, and the claim should be
    measured rather than asserted: a referee pointed out that the recipe's
    ``z_*`` sits about two units above the Planck value, and that the acoustic
    scale is measured to 0.030 per cent.

    The measurement isolates the ``z_*`` formula by recomputing the priors with
    ``z_*`` forced to the Planck value, over the prior box and over the much
    smaller posterior range. What matters is not the mean offset, which the
    calibration absorbs, but the *variation*, which it cannot.
    """
    from absorb import early
    from absorb.params import MODELS

    m = MODELS["lcdm"]
    sigma_lA = 0.090          # Planck compressed-prior error on l_A

    def spread(obs, ocs):
        vals = []
        for ob in obs:
            for oc in ocs:
                bg = m.builder(m.to_dict([ob, oc, 0.3266]))
                om = ob + oc + early.OMEGA_NU0
                _, lA = early.cmb_distance_priors(bg, ob, om)
                orig = early.z_star
                early.z_star = lambda *a, **k: early.PLANCK18["z_star"]
                try:
                    _, lA_planck = early.cmb_distance_priors(bg, ob, om)
                finally:
                    early.z_star = orig
                vals.append(lA - lA_planck)
        v = np.asarray(vals)
        return float(v.mean()), float(v.max() - v.min())

    prior_mean, prior_range = spread((0.0215, 0.02237, 0.0232),
                                     (0.10, 0.1177, 0.14))
    post_mean, post_range = spread((0.0223, 0.0225, 0.0227),
                                   (0.1167, 0.1177, 0.1188))
    return {
        "z_star_recipe": float(early.z_star(0.02237,
                                            0.02237 + 0.1177 + early.OMEGA_NU0)),
        "z_star_planck": float(early.PLANCK18["z_star"]),
        "sigma_lA": sigma_lA,
        "prior_box_mean_shift": prior_mean,
        "prior_box_range": prior_range,
        "prior_box_range_sigma": prior_range / sigma_lA,
        "posterior_mean_shift": post_mean,
        "posterior_range": post_range,
        "posterior_range_sigma": post_range / sigma_lA,
        "posterior_mean_shift_sigma": post_mean / sigma_lA,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--draws", type=int, default=400)
    args = ap.parse_args()

    out = {
        "deficit_floor": deficit_floor(n_draws=args.draws),
        "transfer_peak": peak_at_activation(),
        "neutrino_jerk_term": neutrino_jerk_term(),
        "growth_signature": growth_signature(),
        "marginalisation_jacobian": marginalisation_jacobian(),
        "recombination_recipe": recombination_recipe_systematic(),
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
    g = out["growth_signature"]
    print(f"  growth signature at z = {g['z']:.0f}: f_growth = {g['f_growth']:.4f} "
          f"against {g['f_growth_no_transfer']:.4f} with no transfer, "
          f"f_rsd = {g['f_rsd']:.4f}; holds at every point tried: "
          f"{g['holds_at_every_point_tried']}")
    rr = out["recombination_recipe"]
    print(f"  recombination recipe: z_* = {rr['z_star_recipe']:.2f} against "
          f"Planck's {rr['z_star_planck']:.2f}; the l_A offset varies by "
          f"{rr['posterior_range_sigma']:.2f} sigma over the posterior and "
          f"{rr['prior_box_range_sigma']:.2f} sigma over the prior box")
    j = out["marginalisation_jacobian"]
    print(f"  M_B marginalisation Jacobian: {j['baseline']:.4f} "
          f"(with SH0ES {j['with_sh0es']:.4f})")
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True))
    print(f"wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
