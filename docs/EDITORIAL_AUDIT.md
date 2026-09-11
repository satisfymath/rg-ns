# Editorial audit

Run after the first referee round. The purpose is not to find new physics
errors, which is the referees' job, but to make sure the manuscript says the
same thing in every place it says anything.

## 1. Executive summary

The paper develops one kinetic law and follows it to exact cosmological
consequences, three falsifiable sign predictions, and a data confrontation. Its
main strength is that it separates what is proved from what is assumed and from
what is conjectured, and now does so mechanically rather than rhetorically.

The two weakest points, both now stated in the text rather than left for a
reader to discover: the perturbation sector is defined by a transfer
prescription that makes the kinetic variables diagnostic at linear order, so
the locality of the rate law is a statement about the homogeneous mode; and the
clock congruence forms caustics, which is exactly where the linear analysis
becomes undefined rather than a remote nonlinear concern.

Ready to submit once the data section reports converged chains.

## 2. Canonical narrative decisions

Where the manuscript could say two different things, this table fixes which one
it says. Every occurrence must match.

| Question | Canonical answer | Enforced in |
|---|---|---|
| Is this a unified theory? | No. An effective framework with an explicit claims ladder. "Unified" appears only qualified, or in the negative. | title, abstract, Sec. 1, Sec. 14 |
| Is the clock action new? | No. It is Lim-Sawicki-Vikman. What is new is that its potential is fixed by the kinetics to a five-parameter family. | Sec. 1, Sec. 8 |
| Does that answer the mimetic objection? | No. It narrows it. The kinetic law is imposed from outside the action. | Sec. 8.4, abstract |
| Is the interacting vacuum new? | No. Wands, De-Santiago and Wang. | Sec. 1, Sec. 5 |
| What is new? | The absorbing-state kinetics with self-reinforcement, and the memory law with its hysteresis consequence. | Sec. 1, Sec. 3, Sec. 14 |
| Is the memory law derived? | No. It is equivalent to a per-unit local law; averaging does not derive it. | Sec. 3.2, abstract, Sec. 14 |
| What does hysteresis change? | The accumulated vacuum, not the asymptotic converted fraction, which is the same for both histories. | Sec. 3.5, abstract, Sec. 14 |
| Does the snap isolate memory? | No. It constrains the memory lag together with the activation profile. | Sec. 7.3, abstract |
| Which rate law is the model? | The constant-rate law with an activation switch. The expansion-tracking law is a separate benchmark, and the required switch exponent differs between them. | Sec. 3.1, Sec. 6.3, App. F |
| Which direction of transfer do the data prefer? | The opposite one, weakly. Stated plainly, not buried. | Sec. 5.3, Sec. 10.4 |
| Is the jerk bound confirmed? | No. It is a falsifiable prediction about ten times below current cosmographic errors. | Sec. 7.1, Sec. 7.2, Sec. 10 |
| Are the defects dark matter? | Conjecture. | Sec. 11, Sec. 13 |
| Does the data prefer the model? | To be filled from `results/results.json` when the chains converge; must read the same way in the abstract, Sec. 10 and Sec. 14. | abstract, Sec. 10.3, Sec. 14 |

## 3. Contradiction table

| ID | Location A | Location B | Type | Resolution | Confidence |
|---|---|---|---|---|---|
| C-01 | Sec. 5 opening: negative densities attributed to the direction of flow | Sec. 5.3: rebuttal uses donor-versus-recipient | logical | opening corrected; the converse half is now `prop:recipient-proportional` | high |
| C-02 | Sec. 8.4: vanishing sound speed conceded as a pathology | Sec. 9.4: same fact used as the basis of a stability claim | scope | identified as one fact in both places; the proposition is scoped to one instability | high |
| C-03 | Sec. 3.1: rate law is local, depending only on the causal past | Sec. 9.1: transfer uniform on comoving slices | logical | overdetermination stated, kinetic variables demoted to diagnostics at linear order, locality scoped to the homogeneous mode | high |
| C-04 | Sec. 3.1: rate law displayed with a constant amplitude | Sec. 6.3: convergence analysed for the expansion-tracking law | scope | both laws named, each exponent derived, the fitted one identified | high |
| C-05 | Sec. 8.5: entropy said to increase with the vacuum density | standard de Sitter result | numerical | corrected; the surviving argument is the second-order one | high |
| C-06 | abstract: "classified as an identity, a theorem, or a conjecture" | ladder has four levels | numerical | abstract corrected | high |
| C-08 | Sec. 5 opening: survey quoted without its flow-direction conditional | the survey's own abstract, which concludes a preference for DE->DM | elision | conditional restored; the section now states that this model flows the disfavoured way and argues that the preference is a property of the recipient-dependent couplings surveyed, not of the direction | high |
| C-07 | App. F: residual bounds tighter than the tests assert | test suite | numerical | table aligned to the asserted bounds; survival test tightened | high |

No high-confidence contradictions remain open. C-08 was found by an
independent referee, not by this audit, which is worth recording: the audit
had passed over a quotation that removed the clause cutting against the
manuscript's own model.

## 4. Placeholder and reference audit

- [x] No `\CITE` remains
- [ ] `\TODO` remains in three places, all awaiting information only the author
      can supply: email, ORCID, Zenodo DOI
- [x] No `[to be filled]`, `XXX` or `TBD` outside the results subsection, which
      is marked and awaits the chains
- [x] Every `\cref` resolves; zero undefined references
- [x] Every figure referenced before it appears
- [x] `docs/BIB_VERIFICATION.md` shows 37/37 entries verified

## 5. Claims audit

- [x] All 50 displayed results appear in `docs/CLAIMS_LADDER.md`
- [x] Three level-S results, all in the Outlook, so the check is not vacuous
- [x] No claim in the abstract stronger than its section states, after the
      round-one corrections to the memory law, the snap and the mimetic
      objection
- [x] Every theorem names the assumptions it uses

## 6. Numerical consistency

- [x] Every number in the abstract, introduction and conclusions is a generated
      macro or comes from a cited source
- [x] `make check` green except the chain-stability gate, which is the point of
      the remaining work

## 7. Action plan

**Critical** (blocks submission)

1. Converged chains, then the results subsection of Sec. 10, the five cosmology
   figures, and the canonical answer to "does the data prefer the model".
2. A second referee round limited to the corrected snap, the restated geodesic
   assumption, and the data section.

**Important**

3. Author email, ORCID and affiliation; Zenodo deposit and DOI.
4. The `nocmb` robustness combination promised in Sec. 10.1.

**Nice to have**

5. The one-dimensional Zel'dovich test of the caustic conjecture, which is
   cheap and would move that item off the conjecture list.
