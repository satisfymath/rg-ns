# Referee report

**Manuscript**: Self-reinforced geometric absorption
**Referee**: F (mathematical relativist; 1+3 covariant formalism, relativistic
fluids, cosmological perturbation theory)
**Round**: 1
**Date**: 2026-09-11

---

## Summary (3 lines)

A pressureless "precursor" converts irreversibly, at a self-reinforced rate with
an exponentially-lagged memory, into a pressureless localized product and an
exact vacuum; the paper derives the homogeneous consequences (positivity, a de
Sitter attractor, a jerk inequality, a snap relation), the linear perturbations
under a geodesic transfer condition, a covariant mimetic realization, a solved
Skyrme-type defect, and a null observational result. It also records three
"obstructions" and argues in §13.8 and §14 that they share a single root.
The mathematics that I could check by hand is, with the exceptions listed below,
correct; what is not correct is several of the paper's claims about what that
mathematics means.

## Recommendation

[ ] Accept  [ ] Minor revision  [x] Major revision  [ ] Reject

I do not recommend rejection: the core identities are right, and the paper is
unusually candid about its own limits. But three of its headline framing claims
— that the geodesic closure is *forced*, that the three obstructions have *one*
root, and one displayed key result in §7 — are stronger than the proofs support,
and one displayed equation is simply wrong. These are not matters of taste; each
has a specific, checkable fix.

---

## What I checked

So that the scope of the negative findings is clear. I verified by hand, in
index notation or by direct integration:

- `eq:setup-raychaudhuri` reduction to `eq:setup-friedmann` (§2.5). Correct.
- `prop:vorticity-obstruction`: the full 1+3 decomposition, the
  antisymmetrisation, and the double `h`-projection. **Correct** (see m10 for a
  wording issue only).
- `prop:geodesic-forced`, parts (1), (2), (3): the projection
  `h^λ_ν [u^ν ∇_μ(ρ u^μ) + ρ a^ν + Q_V u^ν] = (ρ_I+ρ_D) a^λ`, the closure of `u`,
  and the Frobenius/one-clock step. **The algebra is correct.** The framing is not
  (M2).
- `cor:one-transition` `eq:cosmology-monotone-acceleration`: recomputed
  `Ȧ = (3Q_V + 3Hρ_m + 8Hρ_r)/(6M_pl²)`. Correct.
- `thm:sandwich`, both bounds, including the asymmetric split
  `eq:positivity-sandwich-upper`. **Correct**, and the remark
  `rem:sandwich-naive` is well taken.
- `thm:jerk`: `j = 1 - ṗ_tot/(2M_pl²H³)` and the assembly into `1 + 2Ω_r + ε`.
  Correct. The neutrino remark is not (m2).
- `eq:cosmography-deficit-floor` and the exact relation
  `ε_0 = (3/2)(p_eff+3)Δ`. Correct.
- `thm:snap` `eq:cosmography-snap`: rederived `s = j' - j(2+3q)` from
  `a⃜/(aH⁴)`, and `ε'/ε = dlnΓ/dN - Γ/H + 3q`. Correct.
  `eq:cosmography-snap-explicit` is **not** (M3).
- `thm:b-independence`, `eq:perturbations-growth`, `eq:perturbations-growth-N`,
  `eq:perturbations-peff` and `eq:perturbations-growth-signature`: rederived the
  first-order coefficient `(2p_g+3)/(2p_g+5)` from
  `φ' + (5/2)φ = (3/2)g_c + g_c'`. **Correct.** The numeric gloss on
  `eq:perturbations-isw` is not (m3).
- `eq:solvable-closed-form` and `eq:solvable-friedmann`, including the
  `3(1-b)/(3+ξ)` coefficient (which is right, and is *not* what one gets by
  forgetting the `ρ_D` term — I checked). `prop:activation`'s exponents `p>1`,
  `p>3`. Correct.
- `eq:defects-regularity`: solved the `ρ_D` transport equation explicitly with
  `Θ = -c/(T-t)`, `Γ = g/(T-t)`; the "iff" including the `b=0` and `ρ_D(t_0)=0`
  conditions is **correct** within that ansatz (m5).
- `thm:hysteresis`: Kamke–Müller applies as claimed; the vacuum ordering follows
  by parts with the decreasing weight `a^{-3}`. Correct.

I did **not** independently re-derive: the four-form computation (§8.5), the
Skyrme Bogomolny constant `6√2π²`, or the Lindblad mean-field closure. Those are
flagged where relevant but are not the basis of any major point.

---

## Major points

### M1. "Three obstructions, one root" is false as stated in the abstract, and trivial as stated in §13.8

**Location**: `00_abstract.tex:53`; `sec:outlook-one-obstruction`
(`13_outlook.tex:193-235`); `14_conclusions.tex:100-118`; against
`11_defects.tex:234-238`.

Three different triples are advertised under the same slogan, and the claim is
true of at most one of them.

- The **abstract** (`00_abstract.tex:48-56`) names: (i) conversion does not
  regularize caustics; (ii) the branching ratio required for regularity
  vanishes while an abundance requires it not to; (iii) the compression-driven
  repair has a covariant obstruction. It then asserts "all three ... follow from
  the one hypothesis ... that the recipient is an exact vacuum receiving energy
  with no momentum transfer".
- **§13.8** enumerates a *different* triple: no vorticity; `Q_V`, `ρ_V`
  functions of one clock; the geodesic closure forced.
- **§14** (`14_conclusions.tex:105-109`) repeats §13.8's triple but, at
  `14_conclusions.tex:93-96`, has just listed the abstract's.

The abstract's claim is refuted by the paper's own §11. At
`11_defects.tex:234-238` the authors prove that the `ρ_D` divergence at a fold
caustic is carried by the homogeneous part `ρ_D(t_0)|J_0/J|` and conclude, in
their own words, that pointwise regularity "is incompatible with the presence of
*any* localized product there, **however it was made**", and that the remedy is
that "the localized sector acquires pressure". That obstruction therefore has
nothing to do with the recipient being a silent exact vacuum: it descends from
`asm:closure`'s stipulation that the **localized product** is pressureless dust.
I verified this by integrating the transport equation: with
`Θ = -c/(T-t)`, `Γ = g/(T-t)`, `ρ_D(t) = bρ_*[u_0^g u^{-c} - u^{g-c}]` with
`u = T-t`, whose first term diverges as `u^{-c}` for *any* `b>0` and for any
`ρ_D(t_0)>0`, irrespective of the vacuum's stress tensor. Consequently §13.8's
"successor requirement" — "the recipient must be able to exert a transverse
force" (`13_outlook.tex:230-233`) — **does not lift this obstruction at all**.
Giving `ρ_V` a transverse force does not stop dust from being compressed.

Separately, obstruction (i) rests on `Γ ≤ Γ_0 e^{α+β}`, i.e. on `asm:activation`,
a kinetic postulate with no connection to the vacuum's stress tensor; `thm:bounded-rate-obstruction`
would hold verbatim for a recipient with pressure, provided the donor is still
geodesic dust and the rate is still bounded.

Meanwhile §13.8's own triple is not three obstructions but three immediate
corollaries of the single line `dρ_V = -Q_V u ⟹ d(Q_V u) = 0`. Saying that three
corollaries of one equation "share one root" is a tautology, not a finding. So
the unification claim is either **false** (abstract's triple) or **vacuous**
(§13.8's triple).

**Requested change.** Pick one and be consistent. Either (a) restrict the claim
to §13.8's triple and demote it from a "result" to what it is — an observation
that three statements are corollaries of one equation — and delete
"These are not three independent failures" from the abstract; or (b) keep the
abstract's triple and state honestly that it has **two** independent roots: the
silent exact vacuum *and* the pressureless localized product, with the second
requiring the remedy §11 already names (`Π^{μν}` for the *localized* sector, not
for the recipient). Either way, `13_outlook.tex:230-233` must be corrected: the
"single capacity" claim is false for the branching-ratio obstruction.

### M2. `prop:geodesic-forced` is not a proof that the geodesic realization is forced; it assumes the negation of the alternatives it claims to exclude

**Location**: `prop:geodesic-forced`, `09_perturbations.tex:151-206`; abstract
`00_abstract.tex:31-34`; `13_outlook.tex:224-228`; `14_conclusions.tex:108-109`.

The proposition's second hypothesis is `∇_μ T_V^{μν} = Q_V u^ν`. Since
`∇_μ T_V^{μν} = -∇^ν ρ_V` for an exact vacuum, that hypothesis says precisely
that `ρ_V` has no spatial gradient in the frame `u` — i.e. that the vacuum
exerts no transverse force. This *is* the geodesic / energy-transfer-only
prescription of Wands–De-Santiago–Wang; the proposition does not derive it, it
restates its consequences. The paper's own gloss makes this plain
(`09_perturbations.tex:195-199`): "a pressureless fluid whose only source points
along its own four-velocity feels no transverse force, so it cannot be
accelerated". That is a tautology dressed as a theorem.

The circularity becomes an outright error at `09_perturbations.tex:200-202`:
"the third completion listed above, a compensating acceleration of the donor, is
excluded rather than merely untried, and the first, `ζ≠0`, is excluded by (3)."
Both of those "completions" are defined by `∇_μ T_V^{μν} ≠ Q_V u^ν`: a nonzero
`δρ_V,com = ζδ_I` means `∇ρ_V` has a spatial part, which is exactly what
`prop:clumping-unstable` itself uses when it writes `ρ_I A^i = ∂^i ρ_V`
(`09_perturbations.tex:133-135`). So they are excluded *by hypothesis*, not by
the proposition. As written, §9.1 contains both "`ζ<0` ... is not excluded"
(`09_perturbations.tex:139-142`) and "`ζ≠0` is excluded by (3)"
(`09_perturbations.tex:201`), five lines apart.

Note also that §13.8 and §14 elsewhere treat this very hypothesis as *the*
hypothesis a successor theory would have to abandon
(`13_outlook.tex:249-251`: "`prop:geodesic-forced` is what breaks first, since
its hypothesis is exactly what fails"). One cannot simultaneously say that a
statement is forced by the physics and that it rests on a hypothesis a successor
must drop.

What *is* genuinely new and worth keeping: given the silent-vacuum hypothesis,
parts (1)–(3) show the hypothesis is far more restrictive than it looks — it
forces geodesy, irrotationality, hypersurface-orthogonality and a single clock
all at once. That is a real result about the *consequences* of the hypothesis.

**Requested change.** Retitle to something like "Consequences of a silent exact
vacuum for a pressureless donor". In the statement, add the hypotheses actually
used in the proof but missing from it: (a) baryons and radiation separately
conserved (used at `09_perturbations.tex:173`, nowhere in the statement — it is
in `asm:closure` but `prop:geodesic-forced` does not invoke `asm:closure`);
(b) `T^{μν}_{I,D} = ρ_{I,D} u^μ u^ν` exactly, i.e. no heat flux — "pressureless"
alone admits `2u^{(μ}q^{ν)}` and then (1) fails. Replace
`09_perturbations.tex:200-202` with a statement that completions (i) and (iii)
violate the hypothesis rather than being excluded by the conclusion. Delete
"which we show is forced rather than chosen" from the abstract, and
"forced outright" from `13_outlook.tex:226-227` and `14_conclusions.tex:108-109`.

### M3. `eq:cosmography-snap-explicit` is missing a term, and the next theorem depends on the missing term

**Location**: `07_cosmography.tex:169-177` (boxed key result, level C) and
`07_cosmography.tex:203-207`.

`eq:cosmography-snap-explicit` is stated as holding "for the rate law
`eq:process-rate`". By `03_absorbing_process.tex:62-65`, that rate law is
`Γ = Γ_0 e^{αf+βM} S_act(a)`, i.e. it **includes** the activation switch.
Substituting into the (correct) `eq:cosmography-snap`:

```
dlnΓ/dN = dln S_act/dN + α(1-f)Γ/H + B,      B = β(f-M)/(τ_M H)
```

so

```
s - s_ΛCDM = -ε[ 2 + (1 - α(1-f))Γ/H - B - dln S_act/dN ]
```

and for `S_act = a^p/(a^p + a_act^p)` one has `dln S_act/dN = p(1 - S_act)`
exactly. The displayed equation omits `-p(1-S_act)` from the bracket.

This is not cosmetic. Immediately afterwards, `thm:memory-fingerprint`
(`07_cosmography.tex:203-205`) says "The activation term **of**
`eq:cosmography-snap-explicit` ... enters the same bracket with the same
coefficient as `B`, so what the snap measures is the sum `B + p(1-S_act)`" — a
term that does not appear in the equation it cites. My derivation confirms
`thm:memory-fingerprint` is right and the boxed equation is wrong. With the
paper's adopted `p=6`, `p(1-S_act)` is up to 6, against the retained constant 2
and against `Γ/H ≪ 1`: at and before activation the omitted term **dominates the
bracket**, and therefore controls the sign of the snap excess. The claim two
paragraphs later that "Without memory, `B=0` and the snap excess is strictly
negative for `α(1-f) ≤ 1`" (`07_cosmography.tex:222-224`) is false once the
activation term is restored, since `p(1-S_act) > 2` for `S_act < 1 - 2/p`.

**Requested change.** Add `- p(1-\actS)` to the bracket in
`eq:cosmography-snap-explicit`; restate the "strictly negative" limit with the
correct condition `2 + (1-α(1-f))Γ/H > B + p(1-S_act)`; and check whether
`thm:memory-fingerprint`'s `∂s_0/∂B = +ε_0` survives (it does, but the
sign discussion around it does not).

### M4. §14 contradicts §10 and the archived code about whether the growth signature was confronted with data

**Location**: `14_conclusions.tex:63-67` against `10_observations.tex:268-282`
(`fig:signatures`) and `code/absorb/growth.py:117`,
`code/absorb/likelihoods.py:333`.

§14 states: "the growth signature is not confronted with redshift-space data
here at all, so of the three sign predictions above, one is measured and out of
reach and the other two are untested."

§10's `fig:signatures` caption says the opposite: "*Right:* `fσ8` against the
eBOSS DR16 measurements. Including these data moves `ln B` from ... to ...: the
model's sharpest linear prediction does not improve its standing." The code
implements exactly the predicted observable —
`growth.py:117 f_rsd()` returns `f_growth - g_c/H`, which is
`eq:perturbations-frsd` — and `likelihoods.py:333` defines an
`RSD(DR16 fsigma8)` likelihood that is used.

So the paper both does and does not confront `eq:perturbations-growth-signature`
with RSD data, depending on which section one reads. This is the kind of
inconsistency that makes a referee re-open every other summary statement.

**Requested change.** Correct `14_conclusions.tex:63-67` to match §10: two of
the three predictions are measured and both are consistent with (and unimproved
by) present data; one — the sign of `δ_eff` — is not isolated by any present
measurement.

### M5. §6's "local" activation switch is inconsistent with `asm:geodesic`, and §11 draws a physical conclusion from it anyway

**Location**: `rem:activation-local`, `06_solvable_early.tex:112-148`
(esp. `eq:solvable-activation-local` and lines 130-136); against `asm:geodesic`,
`09_perturbations.tex:84-95`, and `prop:geodesic-forced` (3).

`asm:geodesic` requires `δΓ/Γ̄ = -δ_I` exactly, and `prop:geodesic-forced` (3)
asserts this is forced, not assumed. Now take the paper's own preferred local
completion,

```
S_act = [1 + (ρ_I/((1-f)ρ_*))^{p/3}]^{-1}
```

and linearise at fixed `f`:

```
δ ln Γ = δ ln S_act = -(p/3)(1 - S_act) δ_I .
```

Matching `asm:geodesic` requires `(p/3)(1-S_act) = 1`, i.e.
`S_act = 1 - 3/p`, which for the adopted `p = 6` is `S_act = 1/2` — a **single
instant**, the activation epoch itself. Everywhere else
`eq:solvable-activation-local` violates the transfer condition the paper proves
is forced.

This matters because §11 uses that completion to draw a physical conclusion:
"Under compression at fixed `f` the switch *closes*, ... and near a fold caustic
`ρ_I ~ |J|^{-1}`, so `Γ ~ |J|^{p/3} → 0`. The rate does not merely stay bounded
on the approach, as `thm:bounded-rate-obstruction` assumes; it vanishes, which is
strictly worse" (`06_solvable_early.tex:130-136`). Under the theory as actually
defined in §9, the requirement is `δQ_V = 0`, i.e. `Γ ∝ 1/ρ_I ∝ |J|` — exponent
1, not `p/3 = 2`. The qualitative conclusion (the rate vanishes, so the
obstruction is if anything sharper) survives; the stated exponent and the route
to it do not.

The caveat paragraph at `06_solvable_early.tex:140-148` anticipates a *different*
objection (that a `Θ`-based switch would behave oppositely) and never notes that
`eq:solvable-activation-local` is inconsistent with `asm:geodesic`.

**Requested change.** Either derive the caustic behaviour of `Γ` from
`δQ_V = 0` — which is what the theory says — and quote the exponent that gives;
or state explicitly in `rem:activation-local` that
`eq:solvable-activation-local` defines a theory in which the transfer is *not*
comoving-uniform, so that it lies outside `asm:geodesic` and outside
`prop:geodesic-forced`, and that §11's "strictly worse" is therefore a statement
about that other theory.

### M6. `prop:recipient-proportional` proves less than it states, and the "donor vs recipient" dichotomy is not the right criterion

**Location**: `prop:recipient-proportional`, `05_positivity_ide.tex:39-56`;
abstract `00_abstract.tex:22-25`; `14_conclusions.tex:29-33`.

Two separate problems.

(a) **The conclusion is stronger than the proof.** The proof establishes only
that the Nagumo subtangent condition fails on `{ρ_1 = 0}`, i.e. that the
non-negative orthant is not forward invariant. It then asserts "`ρ_1` is driven
through zero", which requires additionally that a trajectory *reach* the face.
That is not automatic. Counterexample within the proposition's own hypotheses:
take `w = 1` so `ρ_2 ∝ a^{-6}`, and write `ρ_1 = a^{-3}u`; then
`du/dN = -ξρ_{2i}e^{-3N}`, which is integrable, so
`u → u_i - ξρ_{2i}/3 > 0` for small enough `ξ` and `ρ_1` never reaches zero.
The correct additional hypothesis is something like
`∫ ξ H ρ_2 a³ dt = ∞` (satisfied for `w = -1`, which is the case the cited
survey studies, but not in general).

(b) **The dichotomy is not the structural criterion the paper claims.** The
sharp condition for forward invariance of `{ρ_1 ≥ 0}` is that the outflow vanish
on the face, i.e. `Q = O(ρ_1)` as `ρ_1 → 0`. Donor-proportionality is
*sufficient*, not necessary. `Q = ξH√(ρ_1ρ_2)` depends on the recipient's
density and is nonetheless positivity-safe; `Q = ξHρ_1^{1/2}` is
donor-*dependent* and is not. Since `sec:positivity-structural` and the abstract
both advertise this as "the structural reason" why seven of eight catalogued
couplings fail, the criterion should be stated in the form that is actually
necessary and sufficient.

**Requested change.** Restate the dichotomy as "`Q/ρ_1` bounded as `ρ_1 → 0`",
note that proportionality is the simplest sufficient case and is what this model
realises, and add the divergence hypothesis needed for "driven through zero" (or
weaken the conclusion to "the orthant is not forward invariant, and for a
recipient with `w ≤ -1/3` the crossing occurs at finite `a`").

### M7. The caustic-free assumption that licenses all of §9 is stated as "not established" when it is known to be false over the data range

**Location**: `09_perturbations.tex:68-78`.

§9 is admirably sharp about where the theory is undefined: "Caustics are ...
precisely the locus on which `eq:perturbations-com`, and with it every result of
this section, is undefined." It then writes: "We proceed on the assumption that
the congruence is caustic-free over the range of scales and redshifts probed by
the data of `sec:observations`, which is a physical assumption about when shell
crossing first occurs and is not established here."

But the clock congruence is the *dark-sector dust* congruence. In any universe
with the observed matter power spectrum, dark-matter shell crossing begins at
`z ~ 20-30` on the smallest collapsing scales and is ubiquitous by `z ~ 1`. The
assumption is therefore not merely unestablished: it is false, throughout the
redshift range of Pantheon+, DESI DR2, the chronometers, and the eBOSS `fσ8`
points that §10 actually fits. "Not established here" understates this to the
point of misdirection.

The defence available to the authors is a *measure* argument — the caustic set
has small volume fraction, the linear modes at the scales fitted are supported
away from it, and the observables are averages — but that argument is nowhere
made, and it is not obviously available for a congruence with `c_s² = 0` and no
mechanism to regularize multi-streaming.

**Requested change.** Replace the sentence with an honest one: shell crossing
occurs within the fitted range; state the volume-fraction or scale-separation
argument under which the linear results are nevertheless used, or state that no
such argument is supplied and that §9 is therefore an approximation of
uncontrolled error on nonlinear scales. This is the one place where I think the
paper, which is elsewhere scrupulous, softens a known pathology rather than
confronting it.

---

## Minor points

**m1.** `07_cosmography.tex:106-107`. A sentence fragment begins mid-clause:
"... and neither bounds the other. / a class of transfer histories that this
model does not realise, and nothing in this paper may be inferred from it."
Text corruption from an incomplete edit; a clause or sentence is missing.

**m2.** `rem:jerk-neutrinos`, `07_cosmography.tex:35`. "Such a species
contributes `-3/2 ṗ/(2M_pl²H³)` to `j`" is wrong by a factor `3/2`. The identity
proved four lines below is `j = 1 - ṗ_tot/(2M_pl²H³)`, so *every* species
contributes `-ṗ_i/(2M_pl²H³)`. Check against radiation: `ṗ_r = -4Hρ_r/3` gives
`+2Ω_r`, which is what the theorem states; the quoted formula would give `3Ω_r`.
The `3/2` presumably migrated from the equivalent form
`(3/2)Ω_i[3w_i(1+w_i) - dw_i/dN]`, which is correct. Fix the displayed
expression; the *conclusion* (the contribution is non-negative, so the bound
survives) is right.

**m3.** `09_perturbations.tex:345-351`. "reduces it by the factor `2/(2p_g+5)`,
which for the fitted rate law and `p=6` is about one seventh." The fitted law is
the constant-rate law, for which `eq:perturbations-peff` gives
`p_g = p + 3/2 = 7.5`, so `2/(2p_g+5) = 2/20 = 1/10` — about one **tenth**.
(Even `p_g = 6` would give `2/17`, about one eighth.)

**m4.** `thm:jerk`, `07_cosmography.tex:13-27`. The theorem admits "any further
conserved species whose pressure is non-increasing", but `eq:cosmography-jerk`
is boxed as an *identity* `j = 1 + 2Ω_r + ε`, which holds only when no such
species is present. With one, the displayed relation is an inequality
(`j ≥ 1 + 2Ω_r + ε`). Either box the inequality or move the extra species into a
separate corollary.

**m5.** `eq:defects-regularity`, `11_defects.tex:204-208`. This is boxed as a
level-C key result with **no hypotheses attached**. The "iff" is true (I checked
it by integrating the `ρ_D` equation) but only for the ansatz
`Θ = -c/(T-t)`, `Γ = g/(T-t) + bounded`, a geodesic pressureless congruence, and
`T_{μν}` meaning the dark sector's alone. As displayed, a reader is entitled to
read it as a general theorem about caustics. Put the hypotheses in the box or in
an immediately preceding theorem environment.

**m6.** `eq:cosmography-deficit-floor`, `07_cosmography.tex:80-86`. Boxed at
level C ("theorem of the model") although the paragraph that follows shows its
hypothesis fails for *every* activation redshift tried, i.e. it is never a
theorem *of this model*. Demote to a remark, or add the hypothesis to the box.

**m7.** `prop:no-pressure-from-kinetics`, `04_homogeneous_cosmology.tex:47-70`.
Two unstated hypotheses. (a) `ä ≤ 0` needs `ρ_tot ≥ 0`, which is not among the
hypotheses; the paper itself worries elsewhere (§5.1, §6.2) about `ρ_V` going
negative in the past, exactly where this proposition would then fail. (b) "the
total pressure is `Σ p_i`" requires the components to share a rest frame;
perfect fluids with distinct four-velocities generate an effective isotropic
pressure from their relative motion, so "each a perfect fluid" is not enough.
Add "with a common four-velocity" and "with non-negative total density".

**m8.** `thm:quasi-positivity`, `05_positivity_ide.tex:16-37`. The theorem
explicitly disclaims continuity of `Γ`, then proves itself with the Nagumo
subtangent criterion, which is a statement about continuous vector fields. The
appeal to "the integral form of the equations" is hand-waving. The result is
true and has a one-line proof that *does* work under local integrability alone:
`ρ_I(t) = ρ_I(t_i) exp[-∫(3H+Γ)] ≥ 0`, after which `ρ_D` and `ρ_V` have
non-negative sources and their integrating-factor solutions preserve sign. Use
that. Also, "for as long as the solution exists" leaves existence unaddressed
under hypotheses that do not supply it.

**m9.** `thm:de-sitter`, `04_homogeneous_cosmology.tex:198-200`. "Under the
second alternative the source `Q_V` is strictly positive initially" does not
follow from `∫^∞ Γ dt = ∞`. Under `asm:activation` — the law actually used —
`Γ → 0` as `a → 0`, so `Q_V` is *not* positive initially. The repair is trivial
(there exists `t_1` with `Γ(t_1) > 0`, and `ρ_V(t) > 0` for `t > t_1`) but it
should be written, since `H > 0` before `t_1` then has to come from
`thm:regular-future` rather than from this proof.

**m10.** `09_perturbations.tex:118-123`. `prop:vorticity-obstruction` is
described as "stronger than the clock argument of `sec:realizations-clock`". It
is more *general* (no realization assumed) but its conclusion is *weaker*:
`Q_V ω_{μν} = 0` permits `ω ≠ 0` wherever `Q_V = 0`, whereas
`u_μ = -∂_μ τ` gives `ω = 0` everywhere. Say "more general", not "stronger".

**m11.** `thm:b-independence` proof, `09_perturbations.tex:220-227`. The proof
writes the transfer perturbations as `-Γ̄ρ̄_I δ_I` and `+b Γ̄ρ̄_I δ_I`, which
implicitly sets `δΓ = 0` — inconsistent with `asm:geodesic`'s
`δΓ/Γ̄ = -δ_I`, under which both vanish identically. The `b`-cancellation does
not depend on this: writing the perturbation as `δ(Γρ_I)` throughout gives
`-δ(Γρ_I) + bδ(Γρ_I) = -δQ_V` with no commitment. Rewrite to avoid an
expression that contradicts the assumption in force.

**m12.** `eq:solvable-closed-form` / `eq:solvable-friedmann`,
`06_solvable_early.tex:14-30`. The `a^{-3}` and `a^{-(3+ξ)}` coefficients in
`eq:solvable-friedmann` are consistent with `eq:solvable-closed-form` only if
`a_act = 1`; as written the factors `a_act³` and `a_act^{3+ξ}` are missing.
(The `3(1-b)/(3+ξ)` coefficient itself is correct — I checked it, including the
`ρ_D` contribution that is easy to drop.) State the normalization.

**m13.** Claim-coverage bookkeeping. `results/claim_ledger.json` attributes
`thm:no-sign-flip`, `prop:recipient-proportional` and `thm:sign-table` to
`test_symbolic.py` via that file's `# covers:` header at
`code/tests/test_symbolic.py:7`; none of the three is tested anywhere in
`code/tests/`. Two of them are quoted in the abstract. They are analytic
statements and need no test, but the ledger asserts machine coverage that does
not exist, and every one of its 144 entries is `"status": "UNREVIEWED"`.
Relatedly, `appF_numerics.tex:198` says "Six analytic claims are verified
independently with a computer algebra system" against seven entries in
`symbolic.ALL_CHECKS` (`code/absorb/symbolic.py:507`).

**m14.** `01_intro.tex:175-176`: "`sec:defects` solves the localized
configuration numerically and bounds **its stability**". No stability
computation exists — only the Derrick scaling argument and the virial identity
`E_2 = E_4` within the hedgehog ansatz (`code/tests/test_skyrme.py:92`). §11
says this correctly ("A minimum within the hedgehog ansatz is not a proof of
stability against all deformations"); the introduction should not say otherwise.

**m15.** Numerical claims quoted from result files rather than from gated tests:
the `κ = 3` pancake exponent (`11_defects.tex:357`) and the claim that the
caustic exponent is "independent of the branching ratio, the memory time and the
reinforcement strengths" (`11_defects.tex:358-360`) come from
`results/pancake.json` and are guarded by no test
(`code/tests/test_pancake.py:73` parametrizes only `κ ∈ {0.5, 1, 1.5}`).

**m16.** No fitted exponent in the paper carries an uncertainty:
`lindblad.py:354` and the pancake/stochastic fits call `np.polyfit` without
`cov=True`, and `paper/generated/numbers.tex:567` publishes `-1.011` bare.
For a paper whose abstract says the closure error is "measured to scale as
`N^{-1}`", the error on the exponent should be quoted.
Relatedly, `code/tests/test_stochastic.py:59`
(`test_finite_size_bias_is_order_one_over_N`) asserts a threshold of 12.0
against an observed `N·|bias|` that is itself inside its own Monte-Carlo error
at the largest `N`; the test cannot distinguish `O(1/N)` from zero and its name
claims a measurement it does not make.

**m17.** `code/absorb/skyrme.py`: `solve_hedgehog` raises
`RuntimeError: solve_bvp failed` at `tol=1e-10` and at `x_min=1e-5`, and
`test_skyrme.py:134` varies only `x_max`, never `n_nodes` or `tol`. The
published `E_{B=1}` is in fact converged (I confirmed ~1e-9 relative stability
across `n_nodes` 300–2400), but nothing in the suite establishes it. Add a mesh
convergence test.

---

## Questions the authors must answer

1. **On M1.** Does the `ρ_D(t_0) ≠ 0` divergence at a caustic follow from the
   silent-vacuum hypothesis in any sense you can make precise? If not, why does
   §13.8's "single capacity" claim include it? If you believe it does, give the
   step.

2. **On M2.** State plainly whether `∇_μ T_V^{μν} = Q_V u^ν` is (a) a
   consequence of something prior, or (b) a defining hypothesis of the model. If
   (b) — which is what §13.8 and §14 assume when they identify it as what a
   successor must change — then in what sense is anything "forced"?

3. **On M5 and `asm:geodesic`.** `asm:geodesic` says the local rate must satisfy
   `δΓ/Γ̄ = -δ_I` exactly. Is there *any* local scalar functional of the model's
   own variables that does this, at all times rather than at one instant? If
   not, is the correct statement that the model has no local rate law at all,
   and that `Γ`, `f`, `M`, `α`, `β`, `τ_M` are background parameters — in which
   case `thm:hysteresis`'s "two histories" are two universes, not two regions?
   §13.2 (`sec:outlook-local-rate`) half-says this; it should be said in §3.

4. **On M7.** What is the volume fraction of the caustic set at the redshifts
   and scales fitted in §10, and what controls the error the linear results
   inherit from it?

5. **On `prop:no-instability`.** The proposition establishes boundedness for a
   2×2 ODE system. §8.4 concedes `c_s² = 0` makes the scalar sector "degenerate
   rather than hyperbolic". What is the Cauchy problem for
   `eq:realizations-clock-action` + `asm:geodesic`, and in what function space
   is it well-posed? "No `k`-dependent coefficient" is not by itself an answer;
   it is a symptom.

6. **On the evidential ladder.** Level C is defined as "Theorem of the model ...
   the hypotheses are named in the statement" (`01_intro.tex:141-143`).
   `eq:defects-regularity` (m5), `eq:cosmography-deficit-floor` (m6) and
   `eq:perturbations-vorticity` carry no hypotheses in their boxes. Does the
   build check verify the *presence* of hypotheses, or only of a level letter?
   The text at `01_intro.tex:129-133` suggests only the latter.

---

## What I could not fault

For the record, since the brief asked for it. The mimetic pathologies are
confronted rather than evaded: `sec:realizations-determined`
(`08_realizations.tex:174-200`) states `c_s² = 0` outright, states that it is
*the same fact* as the absence of `k`-dependence in §9 and must not be counted
twice as a virtue, scopes the Ijjas–Steinhardt gradient-instability result
correctly to actions without `(□τ)²`, and explicitly concedes that
`asm:geodesic`'s scalar sector "has not been shown free of gradient
instabilities by the argument just given". `prop:determined-V` is honest that
the mimetic objection stands. `thm:bounded-rate-obstruction` and the retraction
of the earlier caustic conjecture are exemplary. `rem:hysteresis-prescribed`
correctly identifies why `thm:hysteresis` cannot be stated for the coupled
system. `thm:sandwich` is a genuinely useful anchoring-free statement and its
asymmetric upper bound is right. My objection under M7 is to one sentence, not
to the treatment.
