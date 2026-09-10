# Response to referees, round 2

Two reports, obtained independently and not shown to each other: referee A on
the caustic and defect material, referee B on numerics and statistics. Both
recommended major revision.

Every point below was reproduced before it was acted on. Where a measurement of
ours disagreed with the referee's, that is said plainly and the disagreement is
resolved with numbers rather than argument.

---

## Referee B

### M1. The `xi_h` chain is frozen, not slowly mixing

**Reproduced, and the diagnosis is right.** Cumulative acceptance 0.00733; move
rate 0.01498 over the first ten thousand steps and 0.00581 over the last, so
the chain decelerates; zero non-finite values stored; `eps` spanning 0.008 to
0.885 of a `[0, 1]` prior. Reconstructing ensemble proposals from the stored
final ensemble, **57.1%** land outside the prior box at the default scale
(referee: 56.2%), where they are rejected on the prior alone. The `lcdm` chain
by contrast has acceptance 0.4386 and is healthy. Sampling longer would have
made it worse, as the referee says.

**Changed.** The sampler now works in a logit coordinate, so no proposal can be
invalid. It is a change of variables and not of prior: the Jacobian is added to
the target, and `test_logit_map_preserves_the_prior` samples the transformed
target under a constant likelihood and checks by KS that the parameters come
back uniform. Invalid proposals fall from 57.1% to zero.

**Where we disagree, and it matters.** The referee attributes the rest to a
"razor-thin curved ridge" of aspect ratio ~10³, citing a transplant that raises
chi-square from 1436.52 to 167 000. We reproduce that number exactly, and it is
not what it appears to be. In the profile's own best fits, `omega_V_act` is
0.327 at `eps = 0` and **0.000 at every `eps > 0`**. That first figure is a
physical density; as a density parameter it is `Omega_V_act = 0.699`, which is
the *entire* present vacuum (`Omega_V0 = 0.699`). The two are the two sources
of one quantity, so transplanting the `eps = 0.05` vector to `eps = 0` keeps
`omega_V_act = 0` and thereby deletes the dark energy outright. Holding
the nuisance parameters at the MAP instead and varying `eps` alone gives
chi-square 1436.52, 1436.79, 1438.18, 1443.11, 1494.82 at
`eps = 0, 0.02, 0.05, 0.1, 0.3` — a Δχ² of 6.6 at `eps = 0.1`, not 24 821. The
degeneracy is real, strong and *physical*: the data constrain the total vacuum,
not the split between what was present at activation and what conversion
produced. From a fresh ball in the new coordinate, acceptance is **0.40** at
the default scale.

The frozen chains are kept as `*_demove_frozen.h5` so the diagnosis stays
reproducible. They were stopped rather than extended, which is the one thing
this project does not do to a running chain without a reason; the reason is
above and was measured twice.

### M2. The comparison is unfair, and the penalties are wrong in kind

**Reproduced.** We confirm the nesting is exact — at `eps = 0` the chi-square
is bit-identical to LambdaCDM's for every `(log10_xi, z_act)` tried — so two of
six parameters are unidentified under the null. That is Davies' problem, and
both of the referee's errors push toward the paper's own conclusion, which is
the direction that demands the most care.

**Changed, and the headline number moves.** AIC and BIC are replaced by the
Bayesian evidence, which needs no parameter count: a direction along which the
likelihood is flat contributes its prior volume and nothing more, which is the
correct accounting for a parameter the data do not identify. Nested sampling
also handles the geometry described under M1. The result:

| model | ln Z | ln B vs LambdaCDM |
|---|---|---|
| `lcdm` | -732.152 ± 0.195 | — |
| `xi_h` | -733.748 ± 0.207 | **-1.60 ± 0.28** |

The verdict is unchanged in sign and much weaker in size. LambdaCDM is
preferred at about five to one, where the old comparison claimed ΔBIC = 21.4.
The null result stands and is now stated at its true strength. The local
maximiser also has one protocol for every model, with a per-dimension budget.

### M3. The "95% upper limit on eps" was the end of the grid

**Reproduced and removed.** The profile never exceeded Δχ² = 0.0744 and the
code returned `grid[-1]`. It now returns NaN with an explicit `unbounded` flag.

The underlying fact deserves stating rather than patching: `eps` is the
*convertible* fraction, and the rate can always go to zero, so no limit on it
exists to be found. What the data do constrain is the derived matter deficit,
and profiling that gives a genuine limit — **Δ < 0.0126 at 95%**, with the
profile rising to Δχ² = 1192 across the grid. That is the number the paper
should have been quoting, and now does.

### M4. Seven macros that existed nowhere

**Reproduced.** They were hand-invented names, from a results file no script
read; the document compiled only because latexmk was in force mode.

**Changed.** The generator ingests every registered results file; the
cross-case quantities are computed in the analysis script rather than read off
a table; and `check_numbers.py` now fails on any `\num...` the generator does
not define. We verified the new gate fails when a macro name is corrupted, so
it has power. The suite had in fact been re-run before the report was written,
so `dust_residual` exists; the plumbing was the real defect.

### M5. The stability gate could not fail

**Reproduced.** Fixed one-third burn-in ignoring tau, and the only statistic
watched was a percentile pinned against a prior edge.

**Changed.** It now checks the move rate over the last tenth against the first,
requires the chain to exceed the sampler's own tau criterion, reports the
median as well as the percentile, notes any parameter that fills its prior, and
fails rather than skipping when a chain cannot be checked.

Run against the frozen chains, the new gate confirms the referee's diagnosis
sharply. The **drift statistic still passes**: on `reinforce` the median and
95th percentile of both derived quantities drift by 4–11% against a 25%
tolerance. Every one of the new criteria fails instead — move rate 0.0170 →
0.0087 and 0.0160 → 0.0064, both below the floor and both decelerating; chain
lengths 24.6 and 25.4 tau against the 50 required — and the pinning note fires
on `eps` (84% and 90% of its prior), `alpha_tot` (89%) and `z_act` (88%, 76%).
So the old gate did not merely fail to catch this chain; the quantity it
watched is insensitive to the failure by construction.

### Minor points

**m1, the pancake convergence claim.** Accepted, and it goes further than the
report says: with no conversion the solution is the exact kinematic
`rho_I = 1/J`, so that run is a solver self-test and is now described as one.
The manuscript never quoted the N = 65536 figure — that was in our working
notes — and quotes the suite's own value. The discretisation floor
`eps = (k dq/2)²/2`, which is what limits how close to the caustic an exponent
can be read, is now stated in the text. The collapse runs are not closed-form,
because the compression channel acts there together with the bounded
reinforcing rate and its memory, so their exponents do carry content.

**m5, resources.** All three sub-points accepted. `safe_workers` returns 0 when
nothing fits and `require_workers` refuses; the two budgets are now one, the
strict one, and the sampler uses it; and `record()` samples the summed resident
size of the whole process tree on a thread, since `ru_maxrss` is a lifetime
high-water mark and its children figure is a maximum over one child rather than
a sum over the pool. We accept the certification that the sizing errs in the
safe direction.

**m6, the seed.** Accepted: emcee seeded itself from OS entropy while the
metadata recorded a seed. The sampler is now seeded explicitly on a fresh
chain.

**The tautological test.** Accepted. `test_bounded_rate_cannot_regularize`
asserted an inequality between two numbers it computed itself and called
nothing. It now measures the exponent the module returns and compares the
amplitude to the predicted bound at each distance. Reaching the interesting
case required log-space forms, because at a bound of 10⁴ the amplitude
underflows float64 to exactly zero — which is the artefact the theorem is
about, so no linear test could have got there.

---

## Referee A (caustics)

All findings verified and acted on; recorded in `referee_A_caustics.md` and in
the commits of 10 September.

**Theorem D's topology claim was false.** "Any reasonable perturbative
topology" fails in every `L^p` with `p` finite — shrink the support, keep the
amplitude — and fails under coarse-graining, where `E[kappa(-Theta)_+]` is
positive for every width and suppressed only as `exp(-9H²/2σ²)`:
8.33e-2 at σ = 3H, 7.39e-26 at σ = 0.3H. Both counterexamples were computed.
The statement is now pointwise, in `L^∞`, which is still enough for the
perturbative sections and now says why.

**The channel switches itself off at a crossing.** After shell crossing the
Jacobian grows again, so the expansion turns positive and `kappa[-Theta]_+`
vanishes exactly where it was meant to act. Stated in the text: whatever the
channel can do, it must do on the approach.

**Pointwise finiteness of the stress tensor is not a singularity criterion.**
A generic fold caustic of a dust congruence is a weak singularity in Tipler's
sense and is expected to be extendible. The conditions control the divergence
of the source, not the existence of a singularity, and the text now says so.

**A rate proportional to the expansion has no positive local extension.**
Covariantizing `xi_0 H` as `Theta/3` gives a negative rate wherever the
expansion is negative, violating the non-negativity assumed in `prop:survival`.
That family is now explicitly a statement about the homogeneous mode.

**The `b = 0` requirement contradicts `b > 0` for a relic abundance.** Named as
an unresolved tension rather than left for the reader to notice.

**The residual fluctuation claim was for the wrong variable.** Fixed, with the
breakdown gap `s* = N^{-1/g}` added to the code, the tests and the manuscript.

**`test_pancake.py` was missing.** Written; nine tests.

---

## Found by us, after the reports

Two defects we found while acting on the reports above, recorded here because
both had already reached the manuscript.

### The deficit-to-jerk floor does not apply to this model

`eq:cosmography-deficit-floor`, `j0 - 1 >= 2 Omega_r0 + (9/2) Delta`, is proved
under the hypothesis that the reduced transfer `q = Q_V/(3 Mpl^2 H0^2 H)` is
non-decreasing up to today, and §7 said that hypothesis had to be checked for
the activation profile in use. It had not been. Checked, it fails everywhere:
the activation switch turns the transfer on at `z_act`, after which the rate
falls relative to the expansion, so **q peaks exactly at the activation
redshift** for every activation redshift and rate tried. The floor is violated
in **399 of 400** uniform prior draws, median ratio **0.46** where the bound
requires 4.5, and the hypothesis holds in **none** of them.

Referee E separately caught that the abstract, §10 and §14 were using the
relation *backwards* — inferring an upper bound on the jerk excess from an
upper bound on the deficit, which a floor cannot give. Both faults are fixed at
the source in §7, the jerk excess is now computed directly, and ten tests in
`test_deficit_floor.py` hold the finding in place.

### The derived-quantity profile was not imposing its constraint

Worse, and ours alone. `profile_derived` imposed the target with a quadratic
penalty of `1e6`. On a quantity of order `1e-2` that contributes about 1 to
chi-square for a ten per cent miss, which is far too weak to hold a constraint.
The consequences were visible in the stored output and had not been looked at:

- grid points missed their targets by up to **250%** (target 1.0e-4, achieved
  3.5e-4; target 0.0126, achieved 0.0068);
- the profile was grossly **non-monotone** — Delta chi-square running 0.09,
  0.67, 0.00, 2.12, **297.9**, 21.9, 126.5, 1192 — because each grid point was
  really maximising a different function.

**The published limit `Delta < 0.0126` was read off that curve and is
therefore not trustworthy.** It appeared in the abstract, in
`eq:observations-deficit-limit` and in the conclusions.

The penalty is replaced by an exact constraint: both profiled quantities are
strictly increasing in `eps` at fixed values of everything else and vanish at
`eps = 0`, so `eps` is solved for by a bracketed root-find at each candidate
point, and the target is hit to machine precision. Because most of the prior
cannot reach a given target for any `eps`, candidates are screened for
feasibility before the optimiser is started. The returned record now carries
the worst target miss, the number of decreasing steps and the count of
unreachable points, so this class of failure cannot be silent again.


---

## Referee E (claims and honesty)

Eleven majors, fifteen minors, recommendation major revision. The report's
closing observation is the one we have taken most seriously, so it goes first:

> "the *mathematics* of this paper is more careful than its *summaries*. Every
> one of my major points is a failure of §§00, 01, 10 or 14 to report
> accurately what §§3–13 actually establish ... the gap is systematic rather
> than random: in every instance I found, the overclaim runs in the direction
> that flatters the model."

We accept that, including the diagnosis. Every major below was a summary
claiming more than a body section proves, and the corrections all move in the
same direction.

### The findings we consider most serious

**An inequality used backwards, in three places (M2).** The deficit-to-jerk
relation is a *floor*, so an upper limit on the deficit gives no upper bound on
the jerk excess. One of the three places was added by us during the review
while rewriting the conclusions, which is a fair illustration of the referee's
point about summaries.

Investigating it produced a worse result, which we now report rather than
repair: **the floor's hypothesis fails for this model, always.** The bound needs
the reduced transfer `q = Q_V/(3 Mpl^2 H0^2 H)` to be non-decreasing to today.
The activation switch turns the transfer on at `z_act` and the rate then falls
relative to the expansion, so **q peaks exactly at the activation redshift**
for every activation redshift and rate tried. Over 400 uniform prior draws with
a non-zero deficit, the hypothesis holds in **0**, the floor fails in **398**,
and the median ratio is **0.48** where the bound requires **4.5**. It is a true
theorem about a class of transfer histories this model does not realise, and
nothing in the paper may now be inferred from it. Where the jerk excess is
wanted it is computed. Ten tests hold the finding.

**The growth signature was verified against the wrong reference (m5).** §9 said
"at z = 2 in a representative fit, f_g > 1 while f_RSD < 1", naming neither fit
nor numbers. Computed, both are below 1 — and f_g is below LambdaCDM's own rate
— so the stated check does not pass. The signature is an expansion about matter
domination, where the unperturbed rate is 1, and by z = 2 dark energy has
already pulled LambdaCDM to 0.956. Against the reference that isolates it — the
same background with `g_c` removed from the growth equation — the prediction
holds at every one of nine parameter and redshift combinations: at z = 2,
f_g = 0.9310 against 0.8973 with the transfer off, f_RSD = 0.8833.

**A theorem with a hypothesis it could not satisfy (M7).** `thm:hysteresis`
concluded that two histories accumulate different vacuum, which through the
Friedmann constraint gives them different expansion histories — contradicting
its own "along a common expansion history" in the coupled system it was invoked
for. It is now stated for a prescribed `a(t)`, which is what the comparison
argument needs and what the figure computes, with a remark saying why the
hypothesis cannot be reworded away. The abstract and introduction had restated
it as "identical densities"; the hypothesis is equal *converted fraction*, and
the vacuum densities differ by the theorem's own conclusion.

**A ladder that did less than advertised (M5, M6).** The check enforced only
that no bare `\boxed` escaped, so unboxed displayed results and every numbered
theorem went unclassified; the level argument was discarded by the environment,
so the level was invisible at the point of the claim; and there was no level for
a *postulate*, so the paper's own defining rate law was stamped "theorem of the
model: follows from the new postulates", which is circular. Levels are now
printed beside each result, the ladder has postulate and numerical levels, and
the wording says what the check enforces — presence and placement, not
correctness.

### Answers to the referee's seven questions

1. **Was `memory` fitted?** It had not been when the report was written. It has
   now: `ln B = -2.01 ± 0.29` against LambdaCDM. Whether the memory parameters
   are constrained is being read off the posterior; the sentence asserting they
   are will be replaced by whatever the posterior shows, which on the evidence
   of the other rate parameters we expect to be "they are not".
2. **Was `track_b` fitted?** No, and two sections said it was. §5 is corrected,
   and the run is queued.
3. **Intended reading of the deficit floor in §10?** Neither reading: it does
   not apply, for the reason above, and §10 no longer uses it.
4. **`tab:parameters` is empty.** Because it drew on the `memory` chain, which
   was not fit to quote from. It is now populated from the nested posterior.
5. **Is `a(t)` prescribed in `thm:hysteresis`?** Prescribed. The theorem now
   says so.
6. **Does the `q` non-decreasing hypothesis hold for the fitted profile?** No,
   and not for any activation profile of this family. See above.
7. **Why no growth data?** No good reason: the fσ8 likelihood, the data and a
   dataset combination including them were already implemented and had never
   been run. The comparison is queued rather than disclaimed.

### Also fixed

`p_eff` denoted three different quantities — an exponent of the transfer, a
different exponent of the growth coupling differing from it by exactly 3, and a
Reynolds pressure — so a reader substituting one into the other's formula would
have been wrong by tens of per cent. The jerk theorem's hypotheses omitted the
massive neutrino every fit carries; its contribution is non-negative, so the
bound survives, and the hypothesis list now admits it. Tipler's criterion was
invoked with no reference; Tipler (1977) and Clarke–Królak (1985) are added,
verified against Crossref. The "no number typed by hand" guarantee is narrowed
to what the build actually enforces, and the numbers that motivated the
narrowing are now generated instead.
