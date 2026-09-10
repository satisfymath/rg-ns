# Paper I — release readiness

**Status: NOT READY.** Blockers below, ordered by severity. This file is
regenerated as gates close; it is not a plan, it is a statement of what is
currently true.

Working tree at the time of writing: see `git rev-parse HEAD`.

## Gate table

| gate | status | evidence | command |
|---|---|---|---|
| Test suite passes | **green** | 244 passed | `PYTHONPATH=code pytest code/tests -q` |
| LaTeX builds, no undefined refs | **green** | check_log clean | `python3 scripts/check_log.py` |
| No hand-typed numbers; no undefined macros | **green** | — | `python3 scripts/check_numbers.py` |
| No NaN/inf reaching the text | **green** | gate added after one did | `python3 scripts/check_numbers.py` |
| No duplicated lines or words | **green** | one real duplicate removed | `python3 scripts/check_prose.py` |
| Every boxed result classified | **green** | 53 classified | `python3 scripts/check_claims.py` |
| Claim ledger: no summary claim untested | **green** | 133 results, 0 untested | `python3 scripts/claim_ledger.py` |
| Bibliography verified | **green** | 39/39 | `python3 scripts/verify_bib.py` |
| Required citations present | **green** | 27 works | `python3 scripts/check_required_cites.py` |
| Chain stability | **green** | archived failures exempt | `python3 scripts/check_chain_stability.py` |
| Published limits regression-tested | **green** | 8 checks | `pytest code/tests/test_published_limits.py` |
| No missing posterior / empty table | **RED** | `[missing: no posterior for 'memory']` | `python3 scripts/check_numbers.py` |
| Evidence reproducible between seeds | **RED** | not yet measured on `xi_h` | `scripts/evidence_repeatability.py` |
| Prior sensitivity documented both ways | **RED** | narrowing done, widening not | `scripts/prior_width_evidence.py` |
| Maximisation protocol reproducible in reasonable time | **AMBER** | 8.4 h -> ~30 min; lands 0.015 above the frozen reference | `scripts/run_map.py` |
| Chi-square column monotone in the nesting | **AMBER** | was violated by 1.55; seeding added, re-running | `pytest code/tests/test_maximisation.py` |
| Conservation identities across the prior | **green** | Friedmann 2e-16, jerk 4e-13 | `pytest code/tests/test_background.py` |
| All figures regenerable and placed | **RED** | 5 cosmology figures skipped | `scripts/make_figures.py` |
| `make reproduce` documented and tested | **RED** | does not exist | — |
| Release archive + checksums | **RED** | does not exist | — |
| Author metadata | **RED (external)** | `[TODO: email, ORCID]` | needs the author |
| Zenodo DOI | **RED (external)** | `[TODO: Zenodo DOI]` | needs the author |
| PDF inspected page by page | **RED** | not done | — |
| Three final independent referee reports | **RED** | not started | — |

## Blockers by severity

### FATAL SCIENTIFIC
None currently known. The four adversarial reviews found no surviving error
that invalidates a central conclusion; what they found were numbers attached to
it, all of which have been recomputed or withdrawn.

### STATISTICAL

**S1. The evidence is not reproducible for the extended models.** An
independent seed moves `ln Z(xi_h)` by 0.944, 4.5 times its quoted per-run
error, and `ln B` from -1.60 to -2.46. Until the between-seed scatter is
measured and quoted in place of the sampler's internal error, Table 2's error
bars are wrong and `ln B` must not be quoted to two decimals.

**S2. Prior sensitivity is only half measured.** Narrowing every unidentified
direction by a factor of two moves `ln B` by about one unit. Widening was
attempted with a prior Monte Carlo that failed its own convergence test and was
discarded; the sampler-based measurement is queued.

**S3. The wording of the comparison must match S1 and S2.** With an uncertainty
of order one from each source on a central value near -1.6, "modestly
disfavoured" is the strongest defensible phrasing.

### REPRODUCIBILITY

**R1. No posterior for the `memory` model**, so Table 3 is empty and says so.
Either produce it or remove the table and the claim that depends on it.

**R2. Five cosmology figures are generated but never placed**, and currently
cannot regenerate because they need the missing posteriors.

**R3. No `make reproduce` path.** A reader cannot go from a clean checkout to
the manuscript's numbers.

**R4. No release archive, checksums, or environment lock.**

### MANUSCRIPT

**M1. Author metadata and Zenodo DOI are placeholders.** Both are external:
they need the author, and no version may ship carrying them.

**M2. The PDF has not been inspected page by page** for clipped tables,
equations outside margins, or captions separated from their figures.

**M3. Three final referee reports have not been run.**

### RESOLVED THIS CYCLE
- Duplicated sentence in §10.4 (found by the author; a gate now catches the class).
- Claim ledger built; two summary claims with no test closed, including the
  snap theorem, where the historical sign error lived.
- Maximisation protocol that took 8.4 hours replaced with a screened one.
