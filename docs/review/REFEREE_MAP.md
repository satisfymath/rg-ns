# Referee map — one page

Every objection a referee is likely to raise, with the place in the manuscript
that answers it and the answer in one line. The point of this file is that no
objection should require the author to write new physics during the review;
if a row has no location, that is a gap and it is marked as one.

Ordered by how likely the objection is to be the *first* one made.

## Scope and framing

| # | Objection | Where | The answer |
|---|---|---|---|
| 1 | "This is an omnibus: cosmology, defects, quantum, four-form." | §1, App. A.2 | Every displayed result carries an evidential level printed beside it, and the ladder is a table. The conjectural sectors are labelled S and confined to §13. |
| 2 | "The title promises a unification." | §1, §14 | No unification is claimed anywhere; the closing paragraph states explicitly that identification with the physical universe and any unification remain open. |
| 3 | "Navier–Stokes / turbulence is marketing." | §13.6 `sec:outlook-turbulence` | The Reynolds-stress statement is an identity about a quadratic form, with the positivity result there proved unconditionally and its scope stated; no claim about the regularity problem appears. |
| 4 | "Another mimetic model with a free potential." | §8.4 `prop:determined-V` | The potential is not free: the kinetics fix it to a five-parameter monotone bounded family. This narrows, and does not remove, the standard objection — said in those words. |

## Statistics and data

| # | Objection | Where | The answer |
|---|---|---|---|
| 5 | "Where are AIC and BIC?" | caption of `tab:comparison` | Davies' problem: the rate parameters are unidentified under the null, so neither penalty describes the model at the point being tested, and both would err toward the paper's own conclusion. The evidence needs no parameter count. |
| 6 | "Your evidence is prior dependent." | §10.4 `sec:observations-reading`, `scripts/prior_width_evidence.py` | Measured, not asserted: `ln B` moves from -1.93 to -0.55 across the widths tried, and the conclusion is stated only to the precision that survives. |
| 7 | "Nested sampling is not reproducible between seeds." | §10.4 `sec:observations-reading`, App. F | Measured: seed scatter 0.146 against a per-run error of 0.208, and the larger of the two is what is quoted. |
| 8 | "The best fits are optimiser noise." | App. F, `check_map_reference.py` | The slow brute-force maximisation is frozen in the repository and compared against on every run; a gate fails the build if any model lands above it or above a model it contains. |
| 9 | "DESI favours the opposite direction of flow." | §5.5 `sec:positivity-track-b`, §10.3 | Stated, and the reverse channel is carried through the comparison as its own model rather than mentioned and dropped. It fits better and is still disfavoured on the evidence. |
| 10 | "The compressed CMB likelihood is not Planck." | §10.1 `sec:observations-data`, App. F | The recipe is calibrated against the Planck ΛCDM best fit and the calibration factor is reported; the limitation is stated where the priors are introduced. |
| 11 | "Pantheon+ analytic marginalisation is wrong." | App. F | Verified against a brute-force one-dimensional scan over the absolute magnitude; the Jacobian is quoted in the table caption and cancels from differences. |
| 12 | "You report a null result as if it were a finding." | §10.4, §14 | It is reported as a null result in those words; ΛCDM is preferred against every extension fitted. |
| 13 | "Growth data would kill it." | §10.3, §10.4 | Added: growth data give `ln B = -1.83` against -1.61 without. The sharpest linear signature does not improve the model's standing, and this is stated. |
| 14 | "Half your parameters are unconstrained." | §10.3, `check_chain_stability.py` | Reported per parameter as the fraction of prior filled; where that fraction is large no limit is quoted, and the gate refuses to let one be quoted. |

## Theory

| # | Objection | Where | The answer |
|---|---|---|---|
| 15 | "Interacting vacuum models have negative densities." | §5.1 `thm:quasi-positivity` | Positivity is structural here: every outflow is proportional to the density of the sector it leaves, which is precisely the property the catalogued pathological couplings lack. |
| 16 | "Interacting dark energy has the Väliviita instability." | §9.4 `sec:perturbations-stability` | No independent degree of freedom, no pressure perturbation, no scale dependence: the instability's hypothesis fails. |
| 17 | "The geodesic closure is an assumption you chose." | §9.1 `prop:geodesic-forced` | It is forced. A pressureless donor whose only source points along its four-velocity cannot be accelerated, and the rest follows. |
| 18 | "Vorticity could drive the vacuum." | §9.1 `prop:vorticity-obstruction` | It cannot: the source is a gradient, so the congruence is irrotational wherever the transfer is on. |
| 19 | "Mimetic models form caustics." | §11.5 | They do, and this one is not saved by conversion: a bounded rate cannot change the exponent of the divergence. Recorded as an obstruction, not repaired. |
| 20 | "Then the model is inconsistent at caustics." | §11.5 | Pointwise finiteness of the stress is not singularity avoidance; a fold caustic of dust is not a strong-curvature singularity in Tipler's sense, and what the conditions control is the applicability of the effective description. |
| 21 | "Is any of this actually new?" | §1.3, §3 | The memory law and its path dependence: no interaction written as a function of the densities and the expansion rate can reproduce hysteresis, whatever its sign behaviour. That is a statement about the dimension of the state space and it is proved. |
| 22 | "The defects are not shown to be dark matter." | §11, §14 | Said outright: the identification is a conjecture, the configuration is solved but not quantised, and no relic abundance is computed. |
| 23 | "The jerk bound is unobservable." | §7, §10.4 | Quantified: profiling puts the excess more than an order of magnitude below what late-time cosmography resolves. Refutable in principle, not in practice, and stated that way. |
| 24 | "The obstructions look like a list of excuses." | §13.8 `sec:outlook-one-obstruction` | They are one obstruction. All three follow from the hypothesis that also supplies the model's only source of acceleration, and the successor's requirement is identified and graded by cost. |

## Known gaps — no location, by design

| Gap | Status |
|---|---|
| Microscopic derivation of the rate law | Open. §8.5 proposes a mechanism and derives α from it; §13.1 lists the calculation that would settle it. |
| Closure for the anisotropic stress Π that would lift the obstructions | Open, and stated as a well-posed problem in §13.8. |
| Relic abundance of the localized sector | Not computed. §11.6 states the requirements only. |
| Nonlinear regime, N-body, structure formation | Not attempted. |
| Author metadata and archive DOI | External; `make_release.py` refuses to build without them. |
