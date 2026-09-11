# Referee report — claims and editorial audit

**Manuscript**: Self-reinforced geometric absorption: a memory-dependent kinetic
framework for vacuum, dark matter and localized structure
**Referee**: H (claims ladder, internal consistency, priority, presentation)
**Round**: 1
**Date**: 2026-09-11

Reviewed against `paper/build/main.pdf` (built 00:50) and `paper/sections/*.tex`,
`paper/generated/*.tex`, `paper/references.bib`, `docs/BIB_VERIFICATION.md`,
`docs/CLAIMS_LADDER.md`, `docs/EDITORIAL_AUDIT.md`, and `scripts/theory_checks.py`.
Excluded by instruction: author email/ORCID, Zenodo DOI, and the in-flight
recomputation of the `reinforced` row of Table 2.

**Note on a moving target.** `00_abstract.tex`, `07_cosmography.tex` and
`14_conclusions.tex` were edited during this review, and `paper/generated/` was
regenerated after `paper/build/main.pdf` was last built. Where the PDF and the
sources disagree I have reviewed the **sources** and said so. Two points below
(M4, M3) were partially overtaken by those edits and are marked; one of the edits
introduced a fresh contradiction, recorded as M14.

---

## Summary (3 lines)

The paper postulates a one-way, self-reinforcing, memory-dependent conversion of
a dark precursor into pressureless defects and an exact vacuum, and works out the
homogeneous, cosmographic, linear and defect consequences under stated
hypotheses. Its cosmological content is a restricted corner of donor-proportional
interacting-vacuum cosmology with a geodesic CDM congruence; its claimed novelty
is the kinetic law itself. The data confrontation is an honest null result, and
the manuscript's discipline about what it does not establish is, in most places,
genuinely better than the field's norm.

## Recommendation

[ ] Accept  [ ] Minor revision  [x] Major revision  [ ] Reject

I do not recommend rejection, and I want to be explicit that this is a closer call
in the paper's favour than the length of the list below suggests. Nothing I found
is a fatal error of physics; the self-auditing machinery is real and the null
result is reported with a candour that is rare. But the single load-bearing novelty
claim is not supported by the manuscript's own literature survey or by its own
results (M1); the paper's central discriminating table cites no competitor at all
(M13); a result adverse to the model is quoted with its adverse clause removed
(M12); two displayed results sit a rung above what their proofs support and
contradict their own restatement elsewhere (M2, M3); and there are hard internal
contradictions, including one wrong displayed formula (M6), one number used for two
different quantities (M5), and an evidence value quoted from a dataset the paper never describes (M4).
Fourteen major points is too many for minor revision. None of them requires new
physics to fix.

---

## Major points

### M1. The paper's only novelty claim is unsupported by its own bibliography, and is undercut by its own results.

**Location**: §1.3 (`01_intro.tex:262–276`), §1.4 item 1, §14 (`14_conclusions.tex`),
`paper/references.bib`.

§1.3 concedes that the interacting vacuum, the constrained clock, the four-form
sector, the open-system description and the jerk/transfer link are all prior work,
and then plants the flag on one thing: *"an absorbing-state kinetics with
self-reinforcement, and a memory variable obeying τ_M Ṁ = f − M, applied to the
dark sector."* Two problems, and they compound.

**(a) The claim rests on "we have not found elsewhere", and the search was not
made.** The bibliography contains exactly **one** kinetics reference: Hinrichsen's
directed-percolation review [16] — a review of a phenomenon the paper explicitly
disclaims ("no universality class is claimed here"). I grepped every title in
`references.bib`: there is **no** entry matching Avrami, Kolmogorov, Johnson–Mehl,
Pólya, urn, reinforced, or autocatalysis. That is the wrong literature, entirely
absent. Specifically:

- Eq. (3.5), `ḟ = (1 − f)Γ(f)` with Γ increasing in f, is the
  Kolmogorov–Johnson–Mehl–Avrami equation of nucleation-and-growth kinetics with
  an autocatalytic rate. KJMA has been the standard model of exactly this — an
  irreversible transformation whose rate rises with the transformed fraction —
  since 1937–1941. Its sigmoidal solutions, its `1 − exp(−Λ)` survival law
  (the paper's Eq. (3.8) and Remark 3.5), and the impingement correction `(1 − f)`
  are textbook. None of this is cited.
- Eq. (3.2), `τ_M Ṁ = f − M`, is a one-pole low-pass filter. The paper itself
  identifies it correctly in §3.2 as "the one-mode Markovian embedding of a
  relaxation process" — i.e. the standard Maxwell/Cattaneo/Debye device for
  turning an exponential memory kernel into an ODE. Presenting a first-order
  linear relaxation as the paper's central novelty requires an argument that no
  one has coupled one to a conversion fraction before, and no such argument is
  given.
- Self-reinforcement in a stochastic counting process is the Pólya-urn /
  reinforced-process tradition. Not cited.
- Non-Markovian / long-memory contact processes exist as a literature. Not cited.

**(b) The manuscript's own analysis shows the memory sector carries no content at
any level the paper computes.** By §9.1 and §13.2, `f`, `M`, `α`, `β`, `τ_M` are
"background bookkeeping rather than local fields" at linear order, and a genuinely
local rate law overdetermines the perturbations (Eq. (9.4)). By Theorem 7.5 the
memory parameters cancel from the jerk and enter the snap only in the combination
`B + p(1 − S_act)`, which cosmography cannot separate. By §10.2 and the current
`tab_parameters.tex`, `α+β` and `log₁₀(τ_M H₁₀₀)` are reported as *unconstrained*,
filling 89% and 87% of their priors. By Table 2 the nine-parameter memory model
(ln B = −2.10) is **worse** than the six-parameter benchmark without it
(ln B = −1.61): the evidence charges the memory parameters their prior volume and
credits them nothing. And Theorem 3.8, the one theorem that is supposed to state
"what the memory buys", holds only along a *prescribed* a(t), which Remark 3.9
concedes cannot be promoted to the coupled system without contradicting its own
hypothesis.

So the paper's unique contribution is a device that is standard in another field,
uncited, non-localizable, unmeasured, penalised by the evidence, and whose
flagship theorem does not apply to the coupled theory.

**(c) The specific prior art.** The following should be engaged with, not merely
listed:

- *Nucleation-and-growth / autocatalytic kinetics*: Kolmogorov (Izv. Akad. Nauk
  SSSR Ser. Mat. **1**, 355 (1937)); Johnson & Mehl (Trans. AIME **135**, 416
  (1939)); Avrami (J. Chem. Phys. **7**, 1103 (1939); **8**, 212 (1940); **9**,
  177 (1941)); Sekimoto (Physica A **135**, 328 (1986)) for the exact treatment;
  Prout & Tompkins (Trans. Faraday Soc. **40**, 488 (1944)) for the canonical
  self-accelerating rate law, which is what `Γ ∝ e^{αf}` is.
- *Reinforced processes*: Pemantle, "A survey of random processes with
  reinforcement", Probability Surveys **4**, 1 (2007), arXiv:math/0610076. This
  is the direct prior art for Theorem 3.8: path dependence and history-dependent
  limits arising from self-reinforcement are the *defining* property of this class
  of processes. Also Hill, Lane & Sudderth (Ann. Prob. **8**, 214 (1980)).
- *Absorbing-state processes with memory*: Jiménez-Dalmaroni & Hinrichsen,
  "Epidemic processes with immunization", Phys. Rev. E **68**, 036103 (2003),
  arXiv:cond-mat/0304113 — a DP process with explicit non-Markovian memory of the
  past, by the author of the one review the paper does cite; Grassberger, Chaté &
  Rousseau, "Spreading in media with long-time memory", Phys. Rev. E **55**, 2488
  (1997); Cardy & Grassberger (J. Phys. A **18**, L267 (1985)) and Janssen
  (Z. Phys. B **58**, 311 (1985)) on the general epidemic process.
- Standard references for the field the paper borrows its formalism from:
  Janssen (1981) / Grassberger (1982) for the DP conjecture; Henkel, Hinrichsen &
  Lübeck, *Absorbing Phase Transitions* (Springer 2008); Marro & Dickman (CUP 1999).

**Change requested**: Either (i) survey the nucleation-kinetics and reinforced-process
literature honestly, cite the above, and restate §1.3's claim as *"the application
of this class of kinetics to the dark sector, together with the exact cosmological
consequences derived here"* — which is defensible and is, I think, the paper's real
contribution — or (ii) drop the memory variable from the headline claims and
re-centre the paper on what it actually establishes, namely the structural
positivity theorem, the parameter-free jerk inequality, and the catalogue of
obstructions of §13.8. Option (i) is the smaller change and the honest one. What is
not acceptable is leaving "what we have not found elsewhere" to stand as a novelty
argument when the relevant literature has demonstrably not been searched.

### M2. Eqs. (8.8)–(8.9) are labelled `C — Theorem of the model`; the same claim is labelled `S — Conjecture` at Eq. (13.1).

**Location**: `08_realizations.tex` (Eqs. (8.8), (8.9)); `13_outlook.tex` Eq. (13.1);
`paper/generated/tab_claims.tex` rows `eq:realizations-lnrate`, `eq:realizations-alpha`.

Level `C` is defined in §1.5 as "Follows from **the postulates** together with the
system specified". Eqs. (8.8)–(8.9) do not follow from Assumptions 4.1, 6.2 or
Eq. (3.4). They follow from a *different* system — a four-form with charged
membranes — under four further hypotheses that the manuscript itself declines to
adopt: the thin-wall limit; a **detailed-balance** relation `Γ↑ = Γ↓ e^{−ΔS}`;
"one nucleation per unit, a common rate, a flux that shifts by a fixed quantum",
which Remark 8.6 explicitly calls "modelling choices, not consequences of the
four-form dynamics"; and thermal nucleation. §13.1 then says in terms:

> "detailed balance is an equilibrium relation, and the nucleation here is
> assumed to be driven by the precursor rather than thermal. Redoing the
> calculation for a driven process is the open problem"

and re-states the surviving content at level `S`, Eq. (13.1). A result cannot be a
theorem of the model in §8 and a conjecture in §13. The commit log
(`cd61a59 Derive the reinforcement coefficient instead of arguing for its sign`)
suggests §8.5 was promoted without the ladder following.

**Change requested**: Demote Eqs. (8.8) and (8.9) to a level that names the
auxiliary system — either `S`, or a new level (e.g. `X — result of an auxiliary
model`) added to the §1.5 table. If the answer is `S`, the build check that
"refuses a conjecture outside Sec. 13" will fire, which is the check working
correctly. The abstract's "a four-form whose membrane nucleation events map onto
absorption events" must then be qualified the same way.

### M3. §13 declares itself entirely conjectural, then proves things; and the abstract and Conclusions rest a headline claim on §13.8.

**Location**: `13_outlook.tex:1–5` ("Everything in this section is conjecture");
§13.6 (`eq:outlook-reynolds-eos`, Eq. (13.3)); §13.8; abstract lines 51–61;
`14_conclusions.tex` final paragraphs.

Three separate failures of the same discipline:

1. **§13.6 contains an unconditional no-go, not a conjecture.** Eq. (13.3) is
   introduced with "exactly", followed by "Both statements are in fact
   unconditional", "The value is an identity", "`w_eff = 2/3` for *any* velocity
   field and any non-negative weight", "its trace cannot be negative whatever the
   correlations", and the conclusion "An averaged quadratic stress of this kind
   therefore **cannot** approach p = −ρ by any choice of amplitudes, correlations
   or number of modes." That is a proved result (and, as far as I can check, a
   correct one). It carries **no level marker** and is absent from
   `tab_claims.tex`. A reader is told the section is conjecture and then handed a
   theorem.
2. **§13.8 is not conjecture either.** "The obstructions are one obstruction" is a
   synthesis of Propositions 4.2, 9.1 and 9.4 — all level `C`, all in the main
   text. Nothing in §13.8 is speculative.
3. **The abstract and Conclusions rely on §13.8 as established.** §14 asserts the
   §13.8 synthesis — "Each descends from the single hypothesis that also makes the
   model work" — and cites `(Sec. 13.8)` for it; the abstract did the same at the
   time of first reading, and its replacement (see M14) still states a synthesis
   whose only derivation is in §13. By the paper's own rule that §13 is conjecture,
   the abstract and Conclusions assert a conjecture as a result. This is exactly
   the leak the ladder exists to prevent, and it is an argument for moving §13.8
   into the body rather than for softening the claim: the synthesis is sound, it is
   simply in the wrong section.

**Change requested**: Move §13.6's derivation and §13.8 wholesale into the main
body (a subsection of §4 or a short §13-prime *before* the Outlook), give Eq. (13.3)
a level `I`, and restrict §13 to items that genuinely require an uncomputed
calculation (§13.1–13.5, §13.7). Alternatively, soften §13's opening sentence —
but then the section header no longer does any work, and the build check that
refuses conjectures outside §13 is enforcing a boundary the prose has abandoned.

### M4. An evidence value is quoted from a dataset and likelihood the paper never describes, for a model it does not name.

**Location**: `10_observations.tex:268–280` (Fig. 5 caption); Table 1
(`paper/generated/tab_datasets.tex`); `14_conclusions.tex:63–66`;
`scripts/growth_comparison.py:48`.

The caption reads: *"Right: fσ₈ against the eBOSS DR16 measurements. Including
these data moves ln B from −1.61 to −1.83: the model's sharpest linear prediction
does not improve its standing."* Four problems:

- **eBOSS DR16 is in no data table, no likelihood description, and no reference.**
  It is absent from Table 1, from §10.1, from App. F.4, and from the bibliography.
  A quantitative evidence value is reported from a likelihood the paper never
  specifies (which measurements? which covariance? which σ₈ normalisation? which
  scale cut?). This alone blocks reproduction.
- **The number is not for "the model".** `scripts/growth_comparison.py:48` computes
  it as `ev["xi_h__rsd"] − ev["lcdm__rsd"]` — the `Γ = ξH` benchmark, not the
  reinforced-with-memory model whose posterior the rest of §10 reports. Attributing
  it to "the model" is wrong.
- **The change is not significant.** −1.61 → −1.83 is Δ ln B = −0.22 against stated
  errors of ±0.29 on each. A caption should not draw a conclusion from it.
- **It contradicted §14.** The Conclusions stated that "the growth signature is not
  confronted with redshift-space data here at all, so of the three sign predictions
  above, one is measured and out of reach and the other two are untested", while
  Fig. 5 said it was confronted and reported the evidence change.
  *Overtaken during review*: `14_conclusions.tex` has since been rewritten to say
  the signature **is** confronted, that the shift is "smaller than the uncertainty
  on either", and that this establishes only that the prediction does not improve
  the model's standing. That is the right resolution and it settles this bullet
  and the previous one. The remaining three problems stand.

**Change requested**: Promote the RSD analysis to a proper subsection — a Table 1
row, a citation for the eBOSS DR16 measurements, a likelihood description in
App. F.4 (measurements, redshifts, covariance, σ₈ convention, scale cuts), and an
explicit statement that the quoted `ln B` is for the `Γ = ξH` benchmark and not for
the full model. A quantitative evidence value that now appears in the Conclusions
cannot rest on a dataset the paper never describes.

### M5. §3.5 reports the wrong quantity for the paper's central novelty claim.

**Location**: `03_absorbing_process.tex:308–311`; `appF_numerics.tex:180–186`;
`paper/generated/numbers.tex:557–564`.

§3.5 reads: *"at the end of the integration window the converted fractions agree to
`\numHysteresisDeltaVacuum` while the vacuum densities differ by
`\numHysteresisRelativeDeltaVacuum` in relative terms."*

`\numHysteresisDeltaVacuum = 0.00540` is the **vacuum density difference**, not a
converted-fraction agreement: `numHysteresisVacuumA = 0.73488`,
`numHysteresisVacuumB = 0.72948`, difference 0.00540, relative 0.00540/0.73488 =
0.0073 = `\numHysteresisRelativeDeltaVacuum`. App. F.6 uses the same macro
correctly ("Their asymptotic vacuum densities differ by 0.00540, a relative
difference of 0.0073"). §3.5 has taken the vacuum number and asserted it of the
converted fractions.

This is not cosmetic. That sentence is the quantitative support for the paper's
signature claim — "Hysteresis shows up in the accumulated vacuum, not in the
endpoint of the kinetics" — and it currently reports no measurement of the
converted-fraction agreement at all. The paper's own gate ("a build check fails if
a macro is used that no results file defines") does not catch a macro used for the
wrong quantity.

**Change requested**: Report the actual converted-fraction agreement from the
archived run under its own macro, and add a check that each `num*` macro is used
only where its results-file key says it belongs.

### M6. Remark 7.2 displays a formula that contradicts the proof of the theorem it qualifies.

**Location**: `07_cosmography.tex:31–45` (Remark 7.2 and the proof of Theorem 7.1);
`scripts/theory_checks.py:101–118`.

The proof of Theorem 7.1 establishes `j = 1 − ṗ_tot/(2M_Pl² H³)`. A further
conserved species therefore contributes `−ṗ_i/(2M_Pl² H³)`. Remark 7.2 states that
a massive neutrino "contributes `−(3/2) ṗ/(2M_Pl² H³)` to j". The factor 3/2 is
unexplained and is inconsistent with the theorem three lines below: applied to
radiation it would give 3Ω_r, not the 2Ω_r the proof derives.

Checking the code settles it. `theory_checks.py:107` computes
`term = -1.5 * dpnu / E2`, where `dpnu` is a derivative of the *reduced* pressure
`ω_p = p/(3M_Pl² H₁₀₀²)` with respect to `N = ln a`. Then
`−ṗ/(2M_Pl²H³) = −(3/2)(dω_p/dN)/E²`, so the 3/2 is a reduced-unit conversion
factor. The code is right; the manuscript has carried a unit-conversion factor
into a formula already written in physical units. The quoted numbers
(4.9 × 10⁻⁵ today, 0.2528 at z = 1500, 2Ω_r = 1.1 × 10⁻⁴) are consequently correct
and the conclusion is unaffected — but the displayed equation is wrong by 50%.

For a manuscript whose principal methodological claim is that every result is
auditable and every number machine-generated, a displayed formula contradicting
its own proof is a serious defect.

**Change requested**: Write `−ṗ_ν/(2M_Pl² H³)` in Remark 7.2, or state the reduced
units explicitly as `−(3/2)(dω_ν/dN)/E²` and say so. Add a symbolic check of this
term to App. F.8 alongside the existing jerk check.

### M7. Symbol collisions in the load-bearing notation, including one that changes the dimension of a quantity within a single section.

**Location**: `appA_conventions.tex` (Table A.1); `08_realizations.tex:38, 45, 170,
209–213`; `07_cosmography.tex:19–21`; `11_defects.tex:336–339`.

App. A.1 opens with "The draft version of this work reused several symbols for
unrelated objects. The table below is the manuscript's single source of truth."
It is not.

- **`ε` (varepsilon) is not in Table A.1 at all**, despite being the paper's
  headline observable: `ε := Q_V/(2M_Pl²H³)`, the jerk excess, whose bound
  `ε₀ < 0.0306` is one of the two numbers in the abstract. The same glyph is also
  the double-well tilt in §8.2 (`W(s) = W₀ + λ_W s²(1−s)² − ε(3s²−2s³)`,
  `08_realizations.tex:74–76`) and the Zel'dovich sheet-resolution floor in §11.5
  (`ε = 1 − cos(k∆q/2) ≃ 2 × 10⁻⁸`, `11_defects.tex:336–339`).
- **`ϵ` (epsilon) carries three incompatible meanings inside §8 alone**: the
  Levi-Civita symbol `ϵ^{μνρσ}` (lines 38, 45); the dimensionless convertible
  fraction, which is what Table A.1 says it is (line 170); and, 39 lines later,
  *an energy*: "a precursor unit of energy ϵ per patch volume is consumed, with the
  accounting `ϵ = ∆V 𝒱_p + E_wall`" (lines 209–213). The third meaning is not a
  passing aside — it defines `b = E_wall/ϵ`, the bridge's central identification,
  which is quoted in the abstract and carried into Eq. (13.1). A reader who takes
  `ϵ` from Table A.1 reads `b` as an energy divided by a dimensionless fraction.
- Plain `B` denotes the topological degree (§11.2), the Bayes factor (`ln B`,
  Table 2), and the bounce action (`B↓`, §8.5). Table A.1 lists only the memory lag
  `𝓑`, which is a different glyph and not one of the three.

**Change requested**: Add `ε` to Table A.1; rename the §8.2 tilt and the §11.5
resolution floor; rename the §8.5 unit energy (`e_unit` or `E_unit`), and restate
`b = E_wall/E_unit` in §8.5, Eq. (13.1) and the abstract; add the three `B` uses to
the "clashes resolved" paragraph or disambiguate them.

### M8. §14 states Theorem 3.8 without the hypothesis that Remark 3.9 says cannot be removed.

**Location**: `14_conclusions.tex` (paragraph 2); §3.5 Theorem 3.8 and Remark 3.9;
§13.2.

Theorem 3.8 is stated "along a prescribed expansion history", and Remark 3.9 is
emphatic that the hypothesis "is not cosmetic and cannot be removed by rewording…
Stated for the coupled system the theorem would therefore contradict its own
hypothesis." §13.2 reinforces it: "the hysteresis of Theorem 3.8 is a property of
that mode rather than of two regions side by side in one universe."

The Conclusions drop it: *"Its distinguishing property is path dependence: two
histories reaching the same converted fraction with different memory states convert
at different epochs, and therefore accumulate different vacuum energies
(Theorem 3.8)."* No prescribed a(t), no decoupling. A reader of §14 alone will take
this as a statement about the cosmological model. The abstract, to its credit, does
carry the qualifier — which makes the omission in §14 harder to defend, not easier.

**Change requested**: Restore "along a prescribed expansion history" (and, ideally,
"as a property of the kinetics rather than of the coupled system") to the
Conclusions sentence.

### M9. The abstract asserts three things the body qualifies or does not prove, and omits the one result that most damages the headline prediction.

**Location**: `00_abstract.tex`, checked line by line against §5, §7, §9, §10.

- **"a signature of opposite signs that a coupling proportional to the local
  density cannot produce"** (lines 41–42). This is a universal negative over a
  class of couplings. §9.3 supports it with a one-sentence physical argument —
  "A model that removed energy in proportion to the local density would suppress
  both" — and no theorem, no class definition, and no proof. The paper proves
  analogous negatives elsewhere (Prop. 5.2, Prop. 9.1, Prop. 9.4); this one is
  asserted. Either prove it as a proposition or write "which a coupling
  proportional to the local density does not produce, for the reason given in §9.3".
- **"its hypothesis on the transfer profile failing for every activation redshift"**
  (lines 60–62). §7.1 supports this with 399 uniform prior draws and says, correctly,
  "for every activation redshift and every rate **we tried**". The abstract deletes
  the qualifier and converts a numerical survey into a universal claim. Restore it,
  or prove the monotonicity of `q(N)` fails analytically for Eq. (6.4).
- **"enhanced density growth together with suppressed velocity growth"** rests on
  Eq. (9.10), which is level `C` but whose input Eq. (9.9) (`p_g = p + 3/2`) is
  established by "we have checked directly against the numerical solution", and
  whose verification is "9 parameter and redshift combinations". A `C` label
  should not sit on top of a numerically-checked input (see m9).
- **The abstract never mentions the reverse channel.** §5.5 introduces it, §7.2
  gives it the *opposite* sign of `j − 1`, and Table 2 shows it is the best-fitting
  extension in the paper (Δχ² = −6.77, ln B = −1.39, better than every other
  extension). §10.3 is admirably frank: "That is the branch whose jerk excess has
  the opposite sign, and it is the branch a confirmed preference for j₀ < 1 would
  select; the data lean that way weakly." A reader of the abstract alone is told
  the framework predicts `j ≥ 1 + 2Ω_r` and is not told that a branch of the same
  framework predicts the opposite and fits better.

**Change requested**: Fix the two verb overclaims; add one clause to the abstract
noting that the one-way restriction is what carries the sign predictions and that
the reverse-channel variant of the same framework reverses them and is the
best-fitting extension.

### M10. The most directly relevant prior work is in the author's own `.bib`, uncited.

**Location**: `paper/references.bib`; §1.3; §9.1 (`09_perturbations.tex`); §8.5; §11.

Five entries pass `verify_bib.py` and are cited **zero** times anywhere in
`paper/sections/`:

| key | title | where it belongs |
|---|---|---|
| `hogg2020_200210449` | *Constraints on the interacting vacuum — geodesic CDM scenario* | §1.3, §9.1, §10 |
| `martinelli2019_190210694` | *Latest evidence for a late time vacuum — geodesic CDM interaction* | §1.3, §9.1, §10 |
| `kitano2016_160507355` | *Electroweak-Skyrmion as Topological Dark Matter* | §11, §13.4 |
| `albertini2023_230312842` | *Dynamical Henneaux–Teitelboim Gravity* | §8.1/§8.5 |
| `popovic2025_251107517` | DES-SN reanalysis / evolving dark energy | §5.3, §10.4 |

The first two are the problem. "Interacting vacuum — geodesic CDM" is a *named,
published, data-constrained scenario* from precisely the school the paper cites for
everything else. It is what Assumption 9.2 defines and what Proposition 9.4 is
about. The abstract advertises the geodesic realization — "which we show is forced
rather than chosen" — as a contribution. §9.1 gets as close as "the geodesic branch
is the one used in the interacting-vacuum literature [1, 2]" while citing the
general formalism papers rather than the two that constrain this exact scenario
against data. A referee from that group will notice immediately.

Separately, **Brown–Teitelboim is missing**. §8.5 uses `∆V = ±hq + q²/2` for
membrane nucleation shifting four-form flux and attributes it to Bousso–Polchinski
[8] and Kaloper [23]. That mechanism is Brown & Teitelboim (*Neutralization of the
cosmological constant by membrane creation*, Nucl. Phys. B297 (1988) 787; and
Phys. Lett. B195 (1987) 177). Omitting it from a section built on it is a priority
error, not a stylistic one.

**Other priority errors in §1.3 and §8**:

- *"Four-form realizations of a vacuum sector go back to Bousso and Polchinski"*
  (`01_intro.tex:59–60`) is false. They go back to Aurilia, Nicolai & Townsend
  (Nucl. Phys. B**176**, 509 (1980)), Hawking (Phys. Lett. B**134**, 403 (1984)),
  and Brown & Teitelboim. Bousso–Polchinski (2000) is the multi-flux landscape
  refinement.
- *"Interacting vacuum cosmology … was developed by Wands et al."*
  (`01_intro.tex:48–50`). Wands–De-Santiago–Wang (2012) gave it its modern
  covariant form; the idea is Özer & Taha (Nucl. Phys. B**287**, 776 (1987)),
  Freese, Adams, Frieman & Mottola (Nucl. Phys. B**287**, 797 (1987)), Borges &
  Carneiro (GRG **37**, 1385 (2005), gr-qc/0503037). Also missing and directly on
  point: Salvatelli, Said, Bruni, Melchiorri & Wands, PRL **113**, 181301 (2014),
  arXiv:1406.7297 — the observational claim for a late-time vacuum–CDM
  interaction, conspicuously absent from a paper about late-time matter→vacuum
  transfer.
- *Mimetic gravity omits its founding paper*: Chamseddine & Mukhanov, "Mimetic
  Dark Matter", JHEP **1311** (2013) 135, arXiv:1308.5410. The paper cites the
  2014 follow-up and two reviews but not this. Also missing: Firouzjahi, Gorji &
  Hosseini Mansoori, "Instabilities in Mimetic Matter Perturbations", JCAP
  **1707** (2017) 031, arXiv:1703.02923, which makes gradient/kinetic instability
  generic in mimetic perturbations. §8.4's defensive argument — that Eq. (8.3)
  contains no `(□T)²` term and so escapes Ijjas et al. — is scoped against *one*
  paper and must answer this one too. Also Takahashi & Kobayashi
  (arXiv:1708.02951), Golovnev (arXiv:1310.2790), Barvinsky (arXiv:1311.3111).
- *§11 has essentially no prior art at all.* Proposition 11.1 states Derrick's
  theorem without citing Derrick (J. Math. Phys. **5**, 1252 (1964)); "the Skyrme
  mechanism" and the SU(2) Skyrme energy are used without citing Skyrme
  (Proc. R. Soc. A **260**, 127 (1961); Nucl. Phys. **31**, 556 (1962));
  Eq. (11.3) and the remark that the solution "sits above the Bogomolny bound by
  the factor familiar from the Skyrme model" cite neither Faddeev
  (Lett. Math. Phys. **1**, 289 (1976)) nor Bogomol'nyi (1976) nor
  Adkins–Nappi–Witten (Nucl. Phys. B**228**, 552 (1983)) nor Manton & Sutcliffe,
  *Topological Solitons* (CUP 2004) — the source of the ≈1.232 ratio the paper
  reproduces as 1.2314. In a 21 kB section the only two citations are Tipler and
  Clarke–Królak, and those two are used correctly.

**Change requested**: Cite Hogg et al. (2020) and Martinelli et al. (2019) in §1.3
and §9.1, and say explicitly what Proposition 9.4 adds to them (the *derivation*
that the branch is forced, rather than its adoption — a real and defensible
increment, but only once the prior scenario is named). Add Brown–Teitelboim to §1.3
and §8.5, Chamseddine–Mukhanov (2013) and Firouzjahi et al. to §8, and
Derrick/Skyrme/Faddeev/Manton–Sutcliffe plus Kitano–Matsudo (already in the bib) to
§11; repair the two priority sentences. Cite or delete the remaining unused
entries; an unused entry that verifies clean is worse than an absent one, because
it shows the source was found and not used.

### M11. Table 3 quotes 95% upper limits on quantities the text says are not measurable.

**Location**: `paper/generated/tab_parameters.tex`; §10.3 (`10_observations.tex:120–136`);
`paper/build/main.pdf` Table 3.

§10.3 is explicit and correct: *"Profiling the likelihood in ϵ over [0, 0.6] never
raises χ² by more than 0.859 above its minimum, so the one-sided threshold
∆χ² = 2.71 is never reached and there is no upper limit to quote… An earlier
version of this analysis reported a 95% upper limit on ϵ; it was the right-hand end
of the grid, and it is withdrawn."*

The current generated table has been fixed for `ϵ` itself (it now reads
*unconstrained*, 83% prior filled — good). But it still reports
**`f₀ < 0.3338 (95%)`** as a derived quantity. `f₀` is a monotone function of the
same unidentified directions: if the rate can always vanish at any `ϵ`, then `f₀`
has no likelihood-based upper limit either, and 0.3338 is a prior-volume artifact
of exactly the kind the text withdrew one paragraph earlier. The same caution that
was applied to `ϵ` has not propagated to its derived partner.

Note also that **the built PDF is stale**: `paper/build/main.pdf` is timestamped
00:50:04 while `tab_parameters.tex`, `tab_datasets.tex` and `tab_comparison.tex`
were regenerated at 00:56:55. The PDF's Table 3 still shows numeric medians and
`ϵ < 0.8337 (95%)` — i.e. the withdrawn limit — with no *prior filled* column at
all. Whatever is submitted must be rebuilt; a referee reading the PDF is reading
the version the text repudiates.

**Change requested**: Mark `f₀` *unconstrained* with its prior-filled fraction, or
state in the caption that the `f₀` and `ϵ` entries are prior-limited and not
likelihood limits. Rebuild before submission.

### M12. §5's opening strips the conditional that makes its cited survey adverse to this model.

**Location**: `05_positivity_ide.tex:5–12`; `docs/EDITORIAL_AUDIT.md` row C-01.

§5 opens: *"A recent survey of interacting dark energy models found that in seven
of eight standard couplings the energy densities become negative somewhere in the
physical domain [12–14]. This section identifies the structural reason, which is
**not the direction of the flow** but the choice of what the transfer is
proportional to…"*

The cited papers (van der Westhuizen, Abebe & Di Valentino, Phys. Dark Univ. **50**,
102119/102120/102121 (2025)) do not state an unconditional result. Their stated
finding is conditional on the flow direction — negative densities arise in seven of
eight cases *when energy flows from dark matter to dark energy* — from which they
draw a stated preference for transfer in the opposite direction, DE → DM. That
conditional is precisely what makes the cited work **evidence against this paper's
model**, whose flow is precursor → vacuum, i.e. DM → DE. The manuscript deletes the
conditional and then uses the survey as motivating background for a section arguing
that the direction is not the issue.

`docs/EDITORIAL_AUDIT.md` row C-01 records that this opening was deliberately edited
to remove the attribution to flow direction ("opening corrected"). Whatever the
intention, the effect is that a result adverse to the model is quoted with its
adverse clause removed, at the head of the section that rebuts it.

This sits badly against the manuscript's honesty elsewhere: §5.3 and §10.4 report
plainly that DESI-era fits weakly prefer the opposite sign, and §5.3 even
acknowledges that some of those parametrizations are recipient-proportional. §5's
opening should be held to the same standard.

**Change requested**: Restore the conditional — "found that in seven of eight
standard couplings the energy densities become negative *when energy flows from
dark matter to dark energy*, and concluded on that basis in favour of the opposite
direction" — and then make the donor-versus-recipient counter-argument against the
claim as its authors actually stated it. That counter-argument is, as far as I can
judge, correct and worth making; it does not need the elision.

### M13. The paper's headline discriminator cites nothing.

**Location**: `00_abstract.tex:31–34`; `07_cosmography.tex:126–132` (Theorem 7.3
sign table), `:149`, `:233`; `14_conclusions.tex:43–45`.

The abstract sells the model on a sign prediction "opposite to that of running
vacuum and of the currently favoured evolving dark-energy quadrant". Theorem 7.3's
sign table has rows "Running vacuum, ν > 0" with the formula `−3ν(1+q)`, and "CPL
in the DESI-preferred quadrant" with an explicit expression in `w₀`, `w_a`.

I grepped every occurrence of "running vacuum" and "CPL" in `paper/sections/`:
**not one carries a citation, anywhere in the paper.** DESI DR2 is cited only inside
`paper/generated/tab_datasets.tex`, never at any point where a DESI preference is
asserted (§5.3 cites three 2026 preprints for the sign preference, but not DESI).

A table whose entire purpose is to place this model against named competitors, in
which no competitor is cited and no competitor's formula is sourced, is not
checkable by a referee. This is the one result that the abstract, §7.2 and §14 all
lead with.

**Change requested**: At minimum — Chevallier & Polarski, IJMPD **10**, 213 (2001),
gr-qc/0009008 and Linder, PRL **90**, 091301 (2003), astro-ph/0208512 for CPL;
Shapiro & Solà, JHEP **0202**:006 (2002), hep-th/0012227 and Solà, Gómez-Valent &
de Cruz Pérez, ApJ **836**, 43 (2017), arXiv:1602.02103 for running vacuum; and
DESI DR2 at the point where the "DESI-preferred quadrant" is asserted. Give the
derivation of each row of Theorem 7.3, or a reference for it.

### M14. The abstract now says the obstructions have two roots; §13.8 and §14 still say one.

**Location**: `00_abstract.tex:53–62`; `13_outlook.tex:190–196`;
`14_conclusions.tex:104–124`.

This contradiction was introduced by an edit made during this review, which is
itself the point: it is precisely the class of defect the manuscript's own
consistency machinery is supposed to catch and does not.

The abstract now reads: *"The obstructions sort into **two families with two
different roots**, and naming them is what a successor needs. One root is the
recipient… The other root is the localized product, which is dust and is compressed
by the same expansion as everything else… Each family lifts under one modification
and neither lifts under the other's."*

Meanwhile §13.8 is still titled **"The obstructions are one obstruction"** and
still opens *"Every one of them descends from **a single hypothesis** — that the
recipient is a silent exact vacuum"*; and §14 still says *"Each descends from **the
single hypothesis** that also makes the model work"* and closes *"**Three
obstructions with one root**, and one root that is also the source of the model's
only success, is a sharper statement than three separate failures."*

One root or two is not a matter of emphasis. It changes the paper's closing
deliverable — what a successor theory must supply. The one-root version says a
successor needs exactly one new capacity (a recipient that can exert a transverse
force); the two-root version says that capacity fixes only one family and the
localized-product divergence at a caustic survives it. As it happens I think the
**two-root** version is the correct one, and §11.5 already argues it: *"defects
already present on the collapsing sheet are pressureless dust, are compressed by
the same Θ, and carry the divergence by themselves… Pointwise regularity of T_μν at
a fold caustic is therefore incompatible with the presence of any localized product
there, however it was made."* That obstruction plainly does not descend from the
vacuum-recipient hypothesis, so §13.8's "single hypothesis" claim was too strong
and the new abstract is the repair. But the repair has been applied in one place
out of three.

**Change requested**: Propagate the two-root formulation to §13.8 — including its
title and its "What the same hypothesis forbids" enumeration — and to §14's closing
paragraph, and state explicitly which of the three recorded obstructions falls in
which family, and what modification lifts each. Also check that §13.8's "The
consequence for a successor" paragraph ("What all three obstructions require is the
same single capacity") is revised; under the two-root reading it is false as
written.

---

## Minor points

**m1.** `07_cosmography.tex:107` — the sentence beginning *"a class of transfer
histories that this model does not realise, and nothing in this paper may be
inferred from it."* has no subject. Its head clause was deleted in editing. This
appears in the built PDF (p. 24) as a dangling fragment. Restore the subject
(presumably "Eq. (7.3) therefore describes…").

**m2.** Raw machine float formatting appears in the prose in nine places:
`4.9e − 05`, `1.1e − 04`, `3.8e − 08`, `1.42e-02`, `4.81e-04`, `7.931e − 11`,
`2.99e − 11`, `4.54e − 11`, `1.70e − 10`. JCAP will not accept `e-04` notation.
Route these through `\num{}` / `\SI{}` in `gen_numbers.py`.

**m3.** Figure 1 caption claims the rescaled standard deviations "collapse onto a
single curve". App. F.6 records `√N·std(f_N)` = 0.8877, 0.9066, 0.9331 and states
plainly that "the three values drift upwards by about five per cent over the range
rather than sitting on a constant. Whether that drift is a slowly vanishing
correction or a different exponent is not settled by three decades." The caption
should not claim a collapse the appendix disclaims. Reword to "approximately
collapse, with a residual drift documented in App. F.6".

**m4.** `10_observations.tex:241` — paragraph heading "One chain is quoted from and
**three** are not", but Table 2 lists four extensions (`Γ = ξH`, `reinforced β=0`,
`reinforced with memory`, `with reverse channel`). Either the count is wrong or
three of the four extended rows share a chain; say which.

**m5.** `11_defects.tex:362` — "the largest violation of the **three exact
identities** of Eq. (11.8)". Eq. (11.8) is a single displayed equation. Name the
three identities or fix the cross-reference.

**m6.** §10.3 reports that on the baseline combination ΛCDM has "the jerk
identically unity to the precision of the integration". By the paper's own
Theorem 7.1 and Remark 7.2, ΛCDM with radiation and one 0.06 eV eigenstate has
`j₀ = 1 + 2Ω_r₀ + 4.9×10⁻⁵ ≈ 1.00016`. Remark 7.2 insists this "is not negligible
at the precision the fits reach". Two passages, two answers. Quote the integrated
value.

**m7.** Excessive significant figures throughout: `α+β = 5.6571 ⁺¹·⁹⁴⁵⁵₋₃.₈₁₉₉`
(five figures on a quantity the same table calls unconstrained),
`z_act = 7.7003 ⁺¹⁰·⁵⁶⁶⁰₋₆.₄₀₀₇`, `E_{B=1} = 103.129`, `χ²_min = 1436.52`. Round to
the precision the uncertainties support.

**m8.** §1.6 says "Sec. 11 solves the localized configuration numerically and
**bounds its stability**". No stability bound is derived. §11.3 says the opposite:
"A minimum within the hedgehog ansatz is not a proof of stability against all
deformations: that would require the full Hessian." Proposition 11.1 is a
non-existence (Derrick) argument and Eq. (11.3) is an energy bound; neither bounds
stability. Reword §1.6.

**m9.** The ladder is not discriminating in the conservative direction, which
weakens the case that it discriminates at all. Level `C` is applied to pure
definitions and kinematic identities: Eq. (5.3) is a definition of `∆` plus a sign
statement; Eq. (7.1) is a kinematic identity plus a definition of `ε`; Eq. (9.2) is
"the curl of a gradient vanishes" projected. All three read `I` more naturally.
A ladder on which a definition and a four-hypothesis auxiliary-model calculation
(M2) carry the same label is not conveying information.

**m10.** "Every displayed **key** result carries an evidential level" (§1.5, §A.2)
is unfalsifiable as written, because "key" is never defined. There are ~82 numbered
equations in the main text and 51 levelled entries. The gap includes Eq. (9.9),
`p_g = p + 3/2`, which is (i) numbered, (ii) the input to the level-`C` Eq. (9.10),
(iii) the basis of an abstract claim, and (iv) established by "we have checked
directly against the numerical solution" — i.e. it deserves level `N` and has none.
Either state the criterion for "key" or extend the ladder to every numbered display.

**m11.** §13.6 asserts `w_eff = 2/3` holds "for *any* velocity field and any
non-negative weight", then four sentences later: "The same computation for
high-frequency gravitational waves gives p = ρ/3." It is not the same computation,
and the juxtaposition invites the reader to think one of the two is wrong. Reword.

**m12.** The Fig. 5 caption describes a left panel and a right panel; `growth.pdf`
contains two stacked right-hand panels (`fσ₈(z)` with eBOSS points, and a lower
`growth rate` panel with `f_g` and `f_RSD`). The lower panel — which carries the
paper's actual opposite-sign signature — is undescribed.

**m13.** The abstract's "which we show is **forced** rather than chosen" (of the
geodesic realization) is true only given the hypothesis that the source is purely
longitudinal, `∇_μ T_V^{μν} = Q_V u^ν`. §13.8 is clear about this; the abstract's
supporting clause ("since a pressureless donor whose only source points along its
own flow cannot be accelerated") restates the hypothesis rather than justifying it,
which reads as circular at abstract length. Add "given the no-momentum-transfer
hypothesis".

**m14.** `paper/references.bib:1–2` begins with an orphan fragment (`,` then `}`)
before the first `@article`, left behind by a badly deleted entry. Remove it.

**m15.** `docs/BIB_VERIFICATION.md` claims "Every entry … is resolved … and the
fetched title is compared with the stored one" and that "the build gate fails if
any entry is unverified or mismatched". The check is **title-only**: it does not
compare authors, year, or journal reference. In this case the authors and journals
happen to be correct (I spot-checked twenty entries against arXiv independently and
found no fabrication or mis-attribution), but the document overstates what it
verifies, and a referee told "the bibliography was verified" is entitled to say so.
Either extend the check or describe it accurately.

**m16.** §8.4 attributes to Chamseddine et al. the *objection* that `V(T)` can be
reverse-engineered to reproduce any expansion history. Those authors present that
reconstruction freedom as a feature of mimetic matter, not as an objection to it.
The citation is the right source for the fact and the wrong source for the framing;
attribute the objection to whoever makes it, or make it in the paper's own voice.

**m17.** §7.1 attributes to Szydlowski "the connection between j > 1 and a transfer
from matter to the vacuum". His stated result is the weaker, two-sided one that
matter–vacuum interaction shows up in the third and higher derivatives of the scale
factor; his own data analysis reports transfer in the *opposite* direction to this
paper's. Citing it as the precedent for this paper's sign, without noting that the
precedent found the other sign, is tendentious given how carefully §5.3 handles the
same issue for the DESI-era literature.

**m18.** `docs/CLAIMS_LADDER.md` describes itself as generated by
`scripts/check_claims.py` and lists 57 entries; `paper/generated/tab_claims.tex`
lists the same 57. Neither contains a `P — Phenomenological` entry, yet §1.5
defines level `P` and §10 is full of fitted numbers (Eq. (10.1), Eq. (10.2),
Table 3). Either the fitted results should carry `P` or level `P` should be dropped
from the §1.5 table. As it stands the paper defines a level it never uses on
precisely the results a reader most needs it for.

---

## Questions the authors must answer

**Q1.** Does the archived code compute the massive-neutrino jerk contribution as
`−ṗ_ν/(2M_Pl²H³)` or as `−(3/2)ṗ_ν/(2M_Pl²H³)`? My reading of
`theory_checks.py:107` is the former (with the 3/2 a reduced-unit factor), which
makes Remark 7.2's displayed formula wrong and its numbers right. Confirm, and say
which of the two the symbolic check of App. F.8 verifies.

**Q2.** For Fig. 5: which eBOSS DR16 `fσ₈` measurements, at which redshifts, with
what covariance and what σ₈ convention? Which model does `ln B = −1.83` refer to,
and what is the error on the *difference* −0.22?

**Q3.** In §3.5, to what precision do the two hysteresis histories' converted
fractions actually agree? The number currently printed is the vacuum-density
difference (M5).

**Q4.** How many extended-model chains were run — three or four (m4)? And were all
four extended rows of Table 2 obtained from nested sampling, or only some?

**Q5.** Was the nucleation-kinetics literature (KJMA/Avrami) searched before the
novelty claim of §1.3 was written? If so, what distinguishes Eq. (3.5) with
Eq. (3.4) from KJMA with an autocatalytic rate constant? If the distinction is the
memory variable alone, please say so explicitly, and address whether a first-order
relaxation coupled to a conversion fraction is novel in the kinetics literature
rather than only in the cosmology literature.

**Q6.** Proposition 9.4 establishes that the geodesic realization is forced. How
does this relate to the "interacting vacuum — geodesic CDM" scenario of
Martinelli et al. (2019) and Hogg et al. (2020), both of which are in the
manuscript's own bibliography (M10)? Was it there assumed, or derived?

**Q7.** §5's opening states the van der Westhuizen et al. result without the flow-direction
conditional that those papers attach to it, and `EDITORIAL_AUDIT.md` C-01 records that
the conditional was removed deliberately. What was the reasoning? If the authors
believe the conditional is not in the cited work, please quote the passage they are
relying on; if it is, the sentence must be restored (M12).

**Q8.** Where do the two non-ΛCDM rows of the Theorem 7.3 sign table come from?
Specifically, is `−3ν(1+q)` for running vacuum derived in this paper, taken from a
source, or asserted; and what defines the "DESI-preferred quadrant" numerically
(which `w₀`, `w_a` region, from which analysis)? (M13)

---

## What I checked and did not find fault with

So that the majors above are read in proportion:

- **The "what this section does not establish" discipline holds.** Every one of
  §§2–12 closes with a paired establishes/does-not-establish paragraph, and in each
  case I checked, the disclaimer is accurate and non-trivial (§4's "not a global
  existence result for the Einstein equations", §8's "not… that caustics of the
  clock congruence are benign", §10's "not a full CMB analysis", §12's "measured on
  a numerical family, not bounded by a proof"). This is better than the field's
  norm and should be kept.
- **The abstract's negative claims are accurate.** "We do not derive quantum
  mechanics, electromagnetism, or any Standard-Model content, and we do not claim
  that the defects are the dark matter" is borne out by §12.1, §13.5, §13.7 and
  §11.6.
- **The null result is reported as one**, including the prior-sensitivity of ln B
  (1.39 in ln B across defensible priors, comparable to ln B itself), the
  withdrawal of the earlier ϵ limit, the withdrawal of the AIC/BIC comparison with
  a statement that both errors favoured the authors' conclusion, and the disclosure
  that the sampler's own diagnostic had "no power to fail". These are unusual and
  creditable.
- **The sandwich theorem (5.6) is correct.** I checked the split of Eq. (5.6):
  `∫ Q_V a'³(a⁻³ − 1)` and `∫ Q_V(1 − a'³)` are both non-negative for `a ≤ 1`, as
  claimed. (A PDF text extraction can make the first integrand look non-positive;
  the source at `05_positivity_ide.tex:199–203` groups it correctly.)
- **The Skyrme numbers are internally consistent**: `12π² = 118.435`,
  `6√2π² = 83.746`, `103.129/83.746 = 1.2314`, `103.129/118.435 = 0.871`.
- **The bibliography is not fabricated.** I independently re-verified twenty of the
  39 entries against arXiv — prioritising every 2026 preprint and every
  unusual-looking identifier — checking title, author list, year and journal
  reference. All twenty matched exactly, including the ones most likely to look
  invented (`2604.03363` "Topolons", IJTP **65**, 237 (2026); `2608.21938`;
  `2609.03062`; the three consecutive van der Westhuizen IDs 2509.04494/95/96,
  which are a genuine three-paper series in Phys. Dark Univ. **50**). The
  bibliography's problems are omission (M1, M10, M13) and one material elision
  (M12), not invention. This should be said plainly, because it is unusual.
- **Most citations are unusually well scoped.** Of the 34 citation sites, the
  prose repeatedly limits what the citation is asked to do, and I found the
  following correct on checking: `hinrichsen2000` (explicitly disclaims a
  universality class), `rideout1999`, `valiviita2008` (the characterisation
  "propagating dark energy component and a constant equation of state" matches
  exactly), `tipler1977`/`clarke1985` (shell crossings genuinely are not
  strong-curvature singularities), `babichev2017`, `ijjas2016` (correctly
  restricted to extended/higher-derivative mimetic), `bemfica2020`, `worsley2026`,
  `carroll1997`, `lesgourgues2012`.
- **Levels spot-checked against content** (18 of 57): `eq:setup-einstein`,
  `eq:setup-vacuum-transfer`, `eq:process-rate`, `eq:process-binomial`,
  `eq:process-breakdown-gap`, `eq:process-survival`, `eq:cosmology-no-acceleration`,
  `eq:cosmology-survival`, `eq:cosmology-dVdf`, `eq:cosmology-desitter`,
  `eq:positivity-map`, `eq:positivity-no-sign-flip`, `eq:solvable-nogo`,
  `eq:solvable-activation`, `eq:realizations-four-form`, `eq:realizations-determined-V`,
  `eq:defects-bound`, `eq:defects-solved`, `eq:quantum-two-state`. All are at or
  below the level their proofs support except `eq:realizations-lnrate` and
  `eq:realizations-alpha` (M2), with the conservative-direction slippage noted in m9.
