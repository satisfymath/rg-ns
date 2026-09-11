#!/usr/bin/env python3
"""Nested sampling: evidences for the model comparison.

Why this and not the ensemble chain.  The comparison the paper makes is
between LambdaCDM and models that contain it as the boundary eps = 0, where
the rate parameters become entirely unidentified: the likelihood there is
*bit-identical* to LambdaCDM's for every value of log10_xi and z_act.  That is
Davies' problem -- nuisance parameters present only under the alternative --
and it makes the usual penalties wrong in kind, because the effective number
of parameters at the null is not the number of sampled ones.  AIC's 2k and
BIC's k ln n both over-penalise the larger model, in the same direction as the
paper's conclusion, which is the direction one is obliged to be most careful
about.

The Bayesian evidence needs no parameter count.  It integrates the likelihood
over the prior, so a direction along which the likelihood is flat contributes
its prior volume and nothing else, which is exactly the right accounting for a
parameter the data do not identify.  Nested sampling also handles the geometry
that defeated the ensemble sampler: the vacuum present at activation and the
vacuum produced by conversion are two sources of the same quantity, so the
posterior runs along a curved degeneracy into the corner omega_V_act = 0.

Reported: ln Z with its sampling error, and ln B relative to LambdaCDM on the
same data.  A stopping criterion of dlogz = 0.1 is used so that the error on a
difference of two evidences stays well below the scale that would change a
qualitative verdict.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

os.environ.setdefault("HDF5_USE_FILE_LOCKING", "FALSE")
os.environ.setdefault("OMP_NUM_THREADS", "1")

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

import numpy as np                                              # noqa: E402

from absorb import datasets                                     # noqa: E402
from absorb.constants import SEED                               # noqa: E402
from absorb.resources import record, require_workers            # noqa: E402
from absorb.sampling import Posterior, WORKER_RSS_MB            # noqa: E402

RESULTS = ROOT / "results" / "evidence.json"
SAMPLE_DIR = ROOT / "results" / "posteriors"

_POST: Posterior | None = None


def _loglike(theta) -> float:
    """Log-likelihood only: the prior is carried by the unit-cube transform."""
    try:
        c2 = _POST.chi2(theta)
    except Exception:                       # unphysical corner of the prior
        return -1e300
    return -1e300 if not np.isfinite(c2) else -0.5 * c2


def _ptform(u):
    return _POST.prior_transform(np.asarray(u))


def run(model: str, dataset: str, *, nlive: int, dlogz: float, seed: int,
        n_proc: int, archive: bool = True) -> dict:
    """One nested-sampling run.

    ``archive`` controls whether the equal-weight samples are written to
    ``results/posteriors/{model}_{dataset}.npz``, which is the file the
    parameter table, the figures and the published summaries are built from.
    It must be false for any run made under modified priors or a non-default
    seed, because the file name encodes neither.

    That is not a hypothetical precaution. The prior-width scan mutates
    ``PRIORS["log10_xi"]`` and calls this function six times, and the
    repeatability check calls it three more; the archive on disk was therefore
    the *last* of those -- prior lower edge -7 instead of -3, seed 12345
    instead of the default. It propagated into ``results.json``, whose
    published 95% interval for ``log10_xi`` ran to -6.71, outside the prior the
    same table states. A gate now checks the samples against the priors, and
    this flag stops the overwrite at its source.
    """
    import dynesty
    import multiprocessing as mp

    global _POST
    _POST = Posterior(model, datasets.build(dataset))
    ndim = _POST.ndim
    # fork so the workers inherit the ~20 MB supernova covariance through the
    # address space instead of pickling it on every task
    ctx = mp.get_context("fork")
    t0 = time.time()
    with ctx.Pool(n_proc) as pool:
        sampler = dynesty.NestedSampler(
            _loglike, _ptform, ndim, nlive=nlive, pool=pool, queue_size=n_proc,
            rstate=np.random.default_rng(seed), sample="rwalk", bound="multi")
        sampler.run_nested(dlogz=dlogz, print_progress=False)
        res = sampler.results
    runtime = time.time() - t0
    logz = float(res.logz[-1])
    logzerr = float(res.logzerr[-1])
    samples = res.samples_equal(rstate=np.random.default_rng(seed))
    chi2_min = float(-2.0 * res.logl.max())

    # Equal-weight posterior samples, for the figures and the parameter table.
    # These replace the ensemble chains, which for these models were not fit to
    # quote from; see docs/review/RESPONSE_r2.md.
    if archive:
        priors = _POST.model.priors()
        SAMPLE_DIR.mkdir(parents=True, exist_ok=True)
        np.savez_compressed(
            SAMPLE_DIR / f"{model}_{dataset}.npz",
            samples=samples, logl=res.logl,
            param_names=np.array(_POST.param_names),
            # provenance, so that a file can be checked against the run that
            # made it rather than trusted because of its name
            seed=np.array(seed), nlive=np.array(nlive),
            prior_low=np.array([p.low for p in priors]),
            prior_high=np.array([p.high for p in priors]))

    return dict(model=model, dataset=dataset, ndim=ndim, nlive=nlive,
                dlogz_target=dlogz, logz=logz, logz_err=logzerr,
                chi2_min=chi2_min, n_eval=int(res.ncall.sum()),
                n_samples=int(samples.shape[0]), runtime_s=runtime, seed=seed,
                param_names=list(_POST.param_names),
                median=np.median(samples, axis=0).tolist(),
                q05=np.percentile(samples, 5, axis=0).tolist(),
                q95=np.percentile(samples, 95, axis=0).tolist())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--models", nargs="+", default=["lcdm", "xi_h"])
    ap.add_argument("--data", nargs="+", default=["baseline"])
    ap.add_argument("--nlive", type=int, default=500)
    ap.add_argument("--dlogz", type=float, default=0.1)
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args()

    n_proc = require_workers(WORKER_RSS_MB, requested=args.workers,
                             what="nested sampling")
    print(f"nested sampling with {n_proc} workers")

    out = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    for dname in args.data:
        for mname in args.models:
            tag = f"{mname}__{dname}"
            print(f"\n=== {tag} ===", flush=True)
            with record(f"nested_{tag}", notes=f"nlive={args.nlive}"):
                entry = run(mname, dname, nlive=args.nlive, dlogz=args.dlogz,
                            seed=args.seed, n_proc=n_proc)
            out[tag] = entry
            print(f"  ln Z = {entry['logz']:.3f} +/- {entry['logz_err']:.3f}"
                  f"   chi2_min = {entry['chi2_min']:.4f}"
                  f"   ({entry['n_eval']} evals, {entry['runtime_s']:.0f}s)",
                  flush=True)
            RESULTS.write_text(json.dumps(out, indent=2, sort_keys=True))

    # Bayes factors against LambdaCDM on the same data
    for dname in args.data:
        ref = out.get(f"lcdm__{dname}")
        if ref is None:
            continue
        print(f"\nln B against LambdaCDM ({dname}):")
        for tag, e in sorted(out.items()):
            if not tag.endswith(f"__{dname}") or tag.startswith("lcdm__"):
                continue
            lnb = e["logz"] - ref["logz"]
            err = float(np.hypot(e["logz_err"], ref["logz_err"]))
            e["ln_bayes_vs_lcdm"] = lnb
            e["ln_bayes_err"] = err
            print(f"  {tag:24s} ln B = {lnb:+.3f} +/- {err:.3f}")
    RESULTS.write_text(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
