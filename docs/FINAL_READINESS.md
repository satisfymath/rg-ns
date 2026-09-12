# Paper I — release readiness

**Status: BLOCKED ONLY ON THE AUTHOR.** Every gate the repository can decide
for itself is green, the full test suite passes, and the manuscript builds
clean. Three placeholders remain and all three need David.

Manuscript: 74 pages (≈52 of main text, the rest references and six
appendices). Commit: `git rev-parse HEAD`.

## Gate table

| gate | status | evidence |
|---|---|---|
| Test suite | **green** | 301 passed |
| LaTeX builds, no undefined refs or cites | **green** | 0 tolerated overfull boxes |
| No hand-typed numbers; no undefined or `nan` macros | **green** | `check_numbers.py` |
| No duplicated lines or words | **green** | `check_prose.py` |
| Every boxed result classified; ladder complete | **green** | 74 classified; every referenced display carries a level |
| Claim ledger: no summary claim untested | **green** | 0 untested |
| Bibliography verified | **green** | 51/51, each stamped with its date |
| Required citations present | **green** | 27 works |
| Chain stability, pinning, move rates | **green** | archived failures reported and exempt |
| Best fits reach what is known reachable | **green** | `check_map_reference.py` |
| Profile floors reach the model's maximum | **green** | −0.000, +0.012, +0.043 |
| Profile grids bracket the maximum | **green** | all three |
| Archived posteriors match their models | **green** | 7 files, priors and seeds checked |
| Evidence table from one sampler configuration | **green** | queue 8, nlive 500, 7 runs |
| Every quoted results file has a `make` target | **green** | `check_reproducible.py` |
| Figures regenerable and placed | **green** | 10 |
| `make reproduce` works end to end | **green** | two crashes in `run_pancake.py` fixed |
| PDF inspected page by page | **green** | `docs/review/pdf_visual_inspection.md` |
| Referee map | **green** | 24 objections, each with a location |
| Three final independent referee reports | **green** | `referee_{F,G,H}`, answered in `RESPONSE_r3.md` |
| Release archive | **blocked** | refuses while placeholders remain |
| Author email and ORCID | **RED (external)** | `paper/main.tex:10` |
| Zenodo DOI | **RED (external)** | `99_acknowledgments.tex:26`, `appF_numerics.tex:341` |

## What the paper now says

ΛCDM is preferred over every extension fitted, at odds between 5:1 and 10:1,
and 4.3:1 with growth data added. That is the result, reported as one. The
memory model — the part with no precedent found in the literature — is the
worst placed of the four, because the parameters it adds are the ones the data
do not identify.

What survives independently of the data: positivity is structural rather than
tuned, and the one coupling out of eight in the published survey that keeps
every density positive is the one satisfying the same criterion; the jerk
bound, whose sign is opposite to running vacuum and to the DESI-favoured
quadrant; path dependence, which no interaction written on the densities can
have; the geodesic realization, which turned out to be forced rather than
assumed; and the vorticity obstruction.

What does not survive: the conjecture that conversion regularizes caustics is
false for the model as published; the deficit–jerk floor does not apply,
its hypothesis failing for every activation tried; and the identification of
the defects with dark matter was never established and is labelled a
conjecture.

## Defects found and fixed in this cycle

Four in displayed results — the snap's activation term, the neutrino jerk
factor, the hysteresis run that could not exhibit its own theorem, and the
solvable family's missing `a_act` factors. Four in provenance — an archived
posterior from the wrong priors, an evidence that depended on the core count,
two concurrent runs overwriting each other, and two crashes that made
`make reproduce-core` unable to finish. Three in profiles — two grids that did
not sample their own minimum and a forward-only sweep that propagated failed
searches. None changed a conclusion. All changed numbers the paper prints.

## What only David can supply

1. Personal email and ORCID, replacing `\TODO{email, ORCID}`.
2. A Zenodo DOI for the code, after tagging the repository.
3. The title decision recorded in `docs/NEEDS_DAVID.md`.
