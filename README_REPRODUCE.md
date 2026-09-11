# Reproducing the results in this paper

Everything quoted in the manuscript is produced by the code in this repository
from public data. Nothing is typed by hand: the analysis scripts write JSON to
`results/`, the LaTeX macros and tables are generated from those files, and the
build fails if the two disagree, if a macro is used that no results file
defines, if one expands to `nan`, or if a generated table is missing its input.

## What you need

- Python 3.12 or later (developed on 3.14.4)
- `pip install --user -r requirements.txt`
- about 2 GB of disk for the public datasets
- for `reproduce-full`, a machine with at least 8 GB of free RAM

Exact versions, seeds, data checksums and the commit that produced the shipped
results are recorded in `results/provenance.json`.

## Two tiers

```
make reproduce-core     # ~25 minutes
make reproduce-full     # hours; re-runs every sampler
```

`reproduce-core` re-derives everything that does not need a sampler: the
symbolic identities, the stochastic simulations, the caustic and pancake runs,
the theory checks, the figures, the tables and the paper, and then runs every
quality gate. It **reuses** the nested-sampling artifacts in `results/`, which
is why it is quick.

`reproduce-full` additionally re-runs the evidences for all five models on both
data combinations, the maximisations, the between-seed reproducibility check,
the prior-width scan and both profile likelihoods. Budget several hours. The
numbers it produces will not be bit-identical to the shipped ones — see
"Expected variation" below.

## Step by step, if you prefer not to use make

```bash
pip install --user -r requirements.txt
python3 scripts/download_data.py          # downloads and verifies checksums
cd code && python3 -m pytest -q && cd ..  # 250+ tests
python3 scripts/run_sims.py               # stochastic, Skyrme, Lindblad, symbolic
python3 scripts/theory_checks.py          # the numbers the theory sections quote
python3 scripts/run_pancake.py            # Zel'dovich caustic suite
python3 scripts/provenance.py
make tables figures pdf check
```

## Expected variation

Two quantities are **not** expected to reproduce to the digit, and the paper
says so where it quotes them:

- **Log-evidences.** Nested sampling is stochastic. Independent seeds move
  `ln Z` for LambdaCDM by about 0.1 and for the six-parameter model by
  roughly 0.9, which is larger than the sampler's own internal error estimate.
  `scripts/evidence_repeatability.py` measures this, and the manuscript quotes
  the between-seed scatter rather than the internal estimate.
- **Maximum-likelihood values.** The extended models' maxima sit on a curved
  ridge that is hard to locate. `scripts/run_map.py` screens a Latin hypercube
  and refines the best points; it reports how many independent refinements
  agreed and how much the final polishing added, so a failed search is visible
  rather than silent.

Everything else — the symbolic identities, the caustic exponents, the pancake
conservation residuals, the profile limits, the defect solution — is
deterministic to the tolerances the tests assert.

## What is not included

The MCMC chain files and the equal-weight posterior samples are large and are
not distributed. `make reproduce-full` regenerates them. The summaries derived
from them are in `results/`, which is distributed.

## If a gate fails

That is the intended behaviour, not a bug in the build. Each gate names the
file and the reason. The gates are:

| gate | what it refuses |
|---|---|
| `check_log.py` | undefined references, citations, control sequences |
| `check_numbers.py` | hand-typed numbers, undefined or `nan` macros, empty tables |
| `check_claims.py` | a boxed result with no evidential level |
| `claim_ledger.py` | a claim quoted in a summary with no test covering it |
| `check_prose.py` | duplicated lines or words |
| `check_figures.py` | a referenced figure that does not exist |
| `verify_bib.py` | a reference whose metadata does not match arXiv or Crossref |
| `check_chain_stability.py` | a chain not fit to quote from |
| `check_required_cites.py` | a work the manuscript must engage with and does not cite |
| `check_map_reference.py` | a best fit above the frozen brute-force reference, or above a model it contains |
| `check_reproducible.py` | a results file the paper quotes that no `make` target produces |
| `make_release.py` | a placeholder or missing input in the deposit archive |
