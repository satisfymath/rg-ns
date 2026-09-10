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
0.327 at `eps = 0` and **0.000 at every `eps > 0`**: the two are the two
sources of today's vacuum, so transplanting the `eps = 0.05` vector to
`eps = 0` keeps `omega_V_act = 0` and thereby deletes the dark energy. Holding
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
