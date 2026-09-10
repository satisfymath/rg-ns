#!/usr/bin/env python3
"""Run every simulation that feeds a number or a figure in the paper.

Writes results/results.json (merging with whatever the MCMC runner has already
put there) and results/sims/*.npz for the figure scripts.  Every number quoted
in the manuscript comes from this file; nothing is typed by hand.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from absorb import lindblad, skyrme, stochastic, symbolic          # noqa: E402
from absorb.constants import SEED                                  # noqa: E402

RESULTS = ROOT / "results" / "results.json"
SIMS = ROOT / "results" / "sims"


def load() -> dict:
    return json.loads(RESULTS.read_text()) if RESULTS.exists() else {}


def save(d: dict) -> None:
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(d, indent=2, sort_keys=True))


def run_skyrme() -> dict:
    print("skyrme: solving the hedgehog boundary-value problem ...")
    h = skyrme.solve_hedgehog()
    trial_min = 12.0 * np.pi ** 2
    bound = skyrme.bogomolny_bound()
    np.savez(SIMS / "skyrme_profile.npz", x=h.x, F=h.F, Fp=h.Fp)
    out = {
        "energy":        {"value": float(h.Etilde), "fmt": ".3f"},
        "bound":         {"value": float(bound), "fmt": ".3f"},
        "trial_min":     {"value": float(trial_min), "fmt": ".3f"},
        "bound_ratio":   {"value": float(h.bound_ratio), "fmt": ".4f"},
        "trial_ratio":   {"value": float(h.trial_ratio), "fmt": ".3f"},
        "degree":        {"value": float(h.B), "fmt": ".6f"},
        "virial_residual": {"value": float(abs(h.E2 - h.E4) / h.E2), "fmt": ".2e"},
    }
    print(f"  E = {h.Etilde:.4f}  = {h.bound_ratio:.4f} x bound"
          f"  = {h.trial_ratio:.4f} x trial;  B = {h.B:.6f}")
    return out


def run_hysteresis() -> dict:
    print("stochastic: hysteresis experiment ...")
    h = stochastic.hysteresis_experiment()
    np.savez(SIMS / "hysteresis.npz", t=h.t, f_A=h.f_A, f_B=h.f_B,
             M_A=h.M_A_traj, M_B=h.M_B_traj)
    out = {
        "f_checkpoint":     {"value": float(h.f_checkpoint), "fmt": ".5f"},
        "memory_A":         {"value": float(h.M_A), "fmt": ".5f"},
        "memory_B":         {"value": float(h.M_B), "fmt": ".5f"},
        "delta_memory":     {"value": float(h.delta_M), "fmt": ".5f"},
        "vacuum_A":         {"value": float(h.V_A), "fmt": ".5f"},
        "vacuum_B":         {"value": float(h.V_B), "fmt": ".5f"},
        "delta_vacuum":     {"value": float(h.delta_V), "fmt": ".5f"},
        "relative_delta_vacuum": {"value": float(h.relative_delta_V), "fmt": ".4f"},
    }
    print(f"  same f = {h.f_checkpoint:.5f}, memories differ by {h.delta_M:.5f}"
          f"  ->  final vacua differ by {100*h.relative_delta_V:.2f}%")
    return out


def run_convergence() -> dict:
    print("stochastic: law of large numbers and fluctuation scaling ...")
    kin = stochastic.Kinetics(Gamma0=1.0, alpha=2.0, beta=1.0, tau_M=0.7)
    t = np.linspace(0.0, 4.0, 200)
    det = stochastic.deterministic(t, kin)
    rows, out = [], {}
    for N in (100, 1000, 10000):
        ens = stochastic.simulate_thinning(N, t, kin, R=600, seed=SEED)
        mean = ens.f.mean(axis=0)
        std = ens.f.std(axis=0)
        err = float(np.max(np.abs(mean - det.f)))
        scaled = float(np.max(np.sqrt(N) * std))
        rows.append((N, err, scaled))
        out[f"lln_error_N{N}"] = {"value": err, "fmt": ".2e"}
        out[f"scaled_std_N{N}"] = {"value": scaled, "fmt": ".4f"}
        print(f"  N={N:6d}  max|mean - ODE| = {err:.2e}   max sqrt(N) std = {scaled:.4f}")
    # store the ensembles needed by the fan-chart figure
    ens_store = {}
    for N in (100, 1000, 10000, 100000):
        ens = stochastic.simulate_thinning(N, t, kin, R=40, seed=SEED + N)
        ens_store[f"f_N{N}"] = ens.f
    np.savez(SIMS / "gillespie.npz", t=t, det_f=det.f, det_M=det.M, **ens_store)
    return out


def run_lindblad() -> dict:
    """Mean-field closure error against N, two ways.

    The full Liouvillian is only tractable to N = 8, and over that range the
    fitted exponent is still contaminated by small-N curvature.  The
    permutation-symmetric (Dicke) chain is exact for the symmetric initial
    states used here and reaches N = 512, which is what actually demonstrates
    the O(1/N) law; both are reported rather than only the convenient one.
    """
    print("lindblad: mean-field closure error versus N ...")
    t = np.linspace(0.0, 4.0, 300)
    full = lindblad.closure_error_scaling(tuple(range(2, 9)), t, engine="master")
    dicke = lindblad.closure_error_scaling(
        (8, 16, 32, 64, 128, 256, 512), t, engine="dicke")
    local = np.diff(np.log(dicke.error)) / np.diff(np.log(dicke.N))
    np.savez(SIMS / "lindblad.npz", N=full.N, error=full.error,
             N_dicke=dicke.N, error_dicke=dicke.error)
    print(f"  full Liouvillian, N = 2..8   : slope {full.slope:.4f}")
    print(f"  Dicke chain,      N = 8..512 : slope {dicke.slope:.4f} "
          f"(local slope at the largest N: {local[-1]:.4f})")
    return {
        "closure_slope_full": {"value": float(full.slope), "fmt": ".3f"},
        "closure_slope_dicke": {"value": float(dicke.slope), "fmt": ".3f"},
        "closure_slope_local": {"value": float(local[-1]), "fmt": ".3f"},
        "closure_error_N8": {"value": float(full.error[-1]), "fmt": ".2e"},
        "closure_N_max": {"value": int(dicke.N[-1])},
    }


def run_symbolic() -> dict:
    print("symbolic: verifying the analytic claims with sympy ...")
    checks = {}
    for name in dir(symbolic):
        if not name.startswith("check_"):
            continue
        fn = getattr(symbolic, name)
        if not callable(fn):
            continue
        try:
            fn()
            checks[name] = True
            print(f"  {name}: ok")
        except Exception as exc:                                  # noqa: BLE001
            checks[name] = False
            print(f"  {name}: FAILED -- {exc}")
    if not all(checks.values()):
        raise SystemExit("symbolic verification failed")
    return {"n_checks": {"value": len(checks), "fmt": "d"}}


def merge_pancake(data: dict) -> dict:
    """Fold the caustic experiments into the results file, if they have run.

    Only the handful of numbers the manuscript quotes are promoted; the rest
    stay in results/pancake.json for inspection.
    """
    src = ROOT / "results" / "pancake.json"
    if not src.exists():
        print("pancake: results/pancake.json not present, skipping")
        return data
    pk = json.loads(src.read_text())
    def grab(case, key, fmt=".4g"):
        return {"value": float(pk[case][key]), "fmt": fmt}
    out = {}
    if "A_none" in pk:
        out["control_exponent"] = grab("A_none", "exp_rho_I_near", ".4f")
        out["control_peak"] = grab("A_none", "centre_rho_I", ".4g")
    if "B_cosmo" in pk:
        out["bounded_exponent"] = grab("B_cosmo", "exp_rho_I_near", ".4f")
        out["bounded_peak"] = grab("B_cosmo", "centre_rho_I", ".4g")
        out["bounded_suppression"] = {
            "value": float(pk["A_none"]["centre_rho_I"]
                           / pk["B_cosmo"]["centre_rho_I"]), "fmt": ".4g"}
    for tag, label in (("C_collapse_k0p5", "kappa_half"),
                       ("C_collapse_k1p5", "kappa_onepointfive"),
                       ("C_collapse_k3p0", "kappa_three")):
        if tag in pk:
            out[f"{label}_exponent"] = grab(tag, "exp_rho_I_near", ".4f")
    if "A_none" in pk:
        res = [v["dust_residual"] for v in pk.values() if "dust_residual" in v]
        if res:
            out["dust_residual"] = {"value": max(res), "fmt": ".2e"}
        out["final_gap"] = grab("A_none", "final_gap", ".1e")
    data["pancake"] = out
    print(f"pancake: promoted {len(out)} numbers")
    return data


def main() -> int:
    SIMS.mkdir(parents=True, exist_ok=True)
    data = load()
    data = merge_pancake(data)
    data["skyrme"] = run_skyrme()
    data["hysteresis"] = run_hysteresis()
    data["convergence"] = run_convergence()
    data["lindblad"] = run_lindblad()
    data["symbolic"] = run_symbolic()
    save(data)
    print(f"\nwrote {RESULTS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
