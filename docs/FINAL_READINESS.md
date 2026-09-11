# Paper I — release readiness

**Status: BLOCKED ON THE AUTHOR, and on one running job.** Everything the
repository can decide for itself is green or is listed below with the command
that shows it. This file is regenerated as gates close; it is a statement of
what is currently true, not a plan.

Working tree at the time of writing: `git rev-parse HEAD`. Manuscript: 65
pages (about 52 of main text, the rest references and six appendices).

## Gate table

| gate | status | evidence | command |
|---|---|---|---|
| Test suite passes | **amber** | 274 passed, 1 failing — the failure is the maximisation gate below, and it is correct to fail | `cd code && pytest tests -q` |
| LaTeX builds, no undefined refs or cites | **green** | 0 tolerated overfull boxes | `python3 scripts/check_log.py` |
| No hand-typed numbers; no undefined macros | **green** | whitelist in `docs/NUMBERS_WHITELIST.txt` | `python3 scripts/check_numbers.py` |
| No NaN/inf reaching the text | **green** | gate added after one did | `python3 scripts/check_numbers.py` |
| No duplicated lines or words | **green** | one real duplicate removed | `python3 scripts/check_prose.py` |
| Every boxed result classified | **green** | 57 classified | `python3 scripts/check_claims.py` |
| Claim ledger: no summary claim untested | **green** | 144 results, 23 cited in a summary, 0 untested | `python3 scripts/claim_ledger.py` |
| Bibliography verified against arXiv/DOI | **green** | 39/39 | `python3 scripts/verify_bib.py` |
| Required citations present | **green** | 27 works | `python3 scripts/check_required_cites.py` |
| Chain stability, pinning, move rates | **green** | archived failures reported and exempt | `python3 scripts/check_chain_stability.py` |
| Published limits regression-tested | **green** | 9 checks, incl. no number for an unconstrained parameter | `pytest code/tests/test_published_limits.py` |
| Posterior present for every model in a table | **green** | `memory` posterior produced | `python3 scripts/check_numbers.py` |
| Evidence reproducible between seeds | **green** | spread 0.146 vs reported 0.208; the larger is quoted | `results/evidence_repeatability.json` |
| Prior sensitivity measured both ways | **green** | `ln B` from −1.93 to −0.55 across widths | `results/prior_width_summary.json` |
| Conservation identities across the prior | **green** | Friedmann 2e−16, jerk 4e−13 | `pytest code/tests/test_background.py` |
| Chi-square column monotone in the nesting | **green** | submodel seeding; gated | `python3 scripts/check_map_reference.py` |
| Best fits reach the frozen brute-force reference | **RED, running** | `reinforce` was 0.137 above it; re-running with the repaired polish | `python3 scripts/check_map_reference.py` |
| All figures regenerable and placed | **green** | 10 figures | `python3 scripts/check_figures.py` |
| `make reproduce` documented and tested | **green** | two tiers, core ≈25 min | `make reproduce-core` |
| PDF inspected page by page | **green** | `docs/review/pdf_visual_inspection.md` | — |
| Referee map | **green** | 24 anticipated objections, each with a location | `docs/review/REFEREE_MAP.md` |
| Three final independent referee reports | **in progress** | theory, data, claims — running | `docs/review/referee_{F,G,H}_*.md` |
| Release archive + checksums | **blocked** | refuses to build while placeholders remain | `python3 scripts/make_release.py` |
| Author metadata | **RED (external)** | `paper/main.tex:10` | needs the author |
| Zenodo DOI | **RED (external)** | `99_acknowledgments.tex:26`, `appF_numerics.tex:208` | needs the author |

## Blockers by severity

### FATAL SCIENTIFIC
None known. Seven adversarial reviews have now been run against the
manuscript. What they found were numbers attached to conclusions, not
conclusions; every one has been recomputed, withdrawn, or gated.

### STATISTICAL
None open. The three that were open are closed and the closures are in the
manuscript rather than in this file: between-seed scatter is measured and the
larger error is quoted; prior width is varied in both directions and the range
is reported; and the wording of the comparison is held to what survives both.

### REPRODUCIBILITY
**R1 (running).** `run_map.py` documented a comparison against the frozen
brute-force maximisation in its docstring without performing it. Performing it
found the reinforced model 0.137 above a chi-square this repository had already
recorded, while reporting its own search as converged. The polish now
alternates simplex with direction-set steps and kicks the best point until the
known ceiling is reached; `xi_h` reproduces the reference exactly and the
remaining models are re-running. `check_map_reference.py` fails the build until
they do.

### MANUSCRIPT
**M1 (external).** Author metadata and the archive DOI are placeholders. Both
need the author, and `make_release.py` refuses to assemble anything while they
are present.

**M2 (in progress).** Three final referee reports are running. Their findings
will be answered in `docs/review/RESPONSE_r3.md` before any submission.

## Resolved this cycle
- The geodesic realization was presented as an assumption; it is a theorem
  (`prop:geodesic-forced`), and the abstract, §9, §13 and §14 now say so.
- The three obstructions are collected under their common root
  (`sec:outlook-one-obstruction`), and the successor's requirement is stated as
  one capacity with two rungs of cost rather than as a demand for a new sector.
- The parameter table quoted `< 0.8337` for a fraction the text explicitly
  withdraws a limit on. It now marks prior-dominated parameters as
  unconstrained and prints, for every sampled parameter, the fraction of its
  prior the posterior covers. A test enforces it.
- The caustic check integrated in a coordinate where the endpoint was not
  representable; it now integrates in the distance to the singularity and is
  verified against the closed form, including two decades deeper than the old
  assertion reached.
- `check_map_reference.py` and the referee map are new.
