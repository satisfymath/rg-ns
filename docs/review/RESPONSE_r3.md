# Response to the three final referee reports

Reports: `referee_F_theory.md`, `referee_G_data.md`, `referee_H_claims.md`.
All three returned **major revision**. All three were right about the things
that mattered, and two of them found errors in displayed results that the
implementation had correct and the manuscript did not.

Every item below is marked **fixed**, **partly fixed** or **open**, with the
commit or file that carries the change. Nothing is marked fixed on the
strength of an argument alone: where a claim was replaced by a measurement,
the measurement is in `results/` and reachable from `make`.

---

## The four errors in displayed results

These came first because they were wrong, not merely unclear.

**F-M3 — the snap's explicit form omitted the activation term.**
`eq:cosmography-snap-explicit` dropped `p(1 - S_act)` from the bracket. The
general form, the text on either side, `thm:memory-fingerprint`, the
implementation and its test all carried it; only the boxed equation did not,
and `background.py` even documents that dropping it flips the sign of the
bracket while the switch is opening. **Fixed**: the term is restored, the
derivation of all three contributions is given in the proof, and the
consequence for the "strictly negative" statement below it is stated.

**H-M6 — the massive-neutrino remark contradicted its own theorem.**
It displayed `-(3/2) p-dot / (2 Mpl^2 H^3)` where `thm:jerk` gives
`-p-dot / (2 Mpl^2 H^3)`; applied to radiation the displayed form would give
`3 Omega_r` where the theorem gives `2 Omega_r`. The `3/2` is a reduced-unit
conversion factor that belongs to the code's variables. **Fixed**: both forms
are given, each in its own variables, and the conversion is shown.

**H-M5 — the hysteresis section reported the wrong quantity.** It said the
converted fractions agree to a number that is the *vacuum density* difference.
Chasing that found something worse: the demonstration ran on a flat
background, where the vacuum increment *is* the converted fraction, so
`Delta V = Delta f` identically and the run could not exhibit the theorem it
illustrates. **Fixed**: the run uses `a ~ t^(2/3)`; both histories reach
`f = 1`, agreeing to `6e-13`, while their vacua differ by 8.4 per cent. A test
asserts the degeneracy of the flat case, so the reason for the choice is
checked rather than asserted.

**F-m12 — the solvable family's Friedmann equation dropped factors of
`a_act`.** The powers are in `a/a_act`. The coefficients were right and the
implementation was right. **Fixed**, with the normalisation stated.

## Provenance and reproducibility

**G-M1 — the archived posterior was not the run its name claimed.**
`run_nested.py` wrote `results/posteriors/{model}_{dataset}.npz` on every
call, and the prior-width scan calls it six times with a mutated prior. The
file on disk was the last of those: prior lower edge `-7` instead of `-3`,
seed 12345 instead of the default. It propagated into `results.json`, which
published a 95 per cent interval for `log10_xi` running to `-6.71` — outside
the prior printed in the same table. **Fixed**: those scans pass
`archive=False`; the archive records seed, worker count and prior bounds; and
`check_posteriors.py` compares every archive against its model's priors and
fails the build. The model was re-sampled. No build gate could have caught
this, because every macro was correctly generated from the wrong file.

**G-M4 — the evidence was not reproducible across machines.** Two runs at four
workers agree to the last digit and reproduce the prior-width scan's row for
the same prior and seed exactly; eight workers move `ln Z` by 0.34, larger
than the quoted error. The cause is that dynesty draws proposals in batches of
`queue_size`, which was tied to the worker count. **Fixed**: the queue is
fixed, so a run is determined by its seed; the worker count is recorded.
**Open**: the full evidence set has not yet been recomputed under the fixed
queue, and must be before submission, since a comparison across data sets
requires every run to share the configuration.

**G-M2 — the profiles sat above the model's own maximum.** All three, by up to
0.78 in chi-square, so every `Delta chi2` in them was measured from the wrong
floor; the largest rise quoted for the convertible fraction, 0.859, should be
about 1.64. Neither crosses the 2.71 the limits use, so the conclusions are
unaffected — but the numbers were quoted. **Partly fixed**: the profiles now
seed from the global best fit and polish with direction-set steps, and
`check_map_reference.py` fails the build when a profile's floor exceeds the
model's maximum. **Open** until they are re-run.

**Undetected by any referee**: `run_pancake.py` had two functions named
`summarise`, so the second shadowed the first, every call reached the wrong
one, and the script raised on its first case. `make reproduce-core` runs it
and therefore could not complete. It crashed again at its final print, over
the cross-case summary row. Both **fixed**; the committed results predated the
collision.

## Method

**G-M3 — Wilks' threshold in Davies' regime.** The paper drops AIC and BIC
because the rate parameters are unidentified under the null, then reads its
limits off 2.71. The objection is sound. **Partly fixed**: rather than argue
the direction, the size is being measured. Every likelihood gained `simulate`,
which draws synthetic data from the model under the true covariance;
`calibrate_threshold.py` generates data at the LambdaCDM best fit, maximises
both models on each — seeding the alternative with the null's answer embedded,
so the statistic cannot come out negative — and accumulates the null
distribution. Two tests guard it: the empirical covariance of the draws
against the stated one, and that simulate/restore returns the data bit for
bit. **Open**: the run is in progress; the result goes in the manuscript
either way.

**G-M5 — the sound-horizon calibration is a constant.** Measured rather than
defended: the recombination-redshift formula gives `z_* = 1091.71` against
Planck's `1089.92`, and switching to the Planck value shifts `l_A` by 0.30 on
average over the posterior — absorbed by the calibration — with that shift
*varying* by 1.5 sigma of `l_A` across the same range, which is not, and by
11.5 sigma over the prior box. **Fixed** as a disclosure with the numbers in
`theory_checks.py`; **open** is the refit under an alternative `z_*` that
would confirm the cancellation between models, and the appendix says so.

**G-M8 — the chronometer covariance.** The appendix and the data table called
the reduced Moresco budget "full covariance". **Fixed**: both now say which
terms are included, that the conservative variant is implemented and not used,
and that it doubles the effective error on a coherent offset in `H(z)`. The
combination is wired as a data set so the robustness run is one command away;
**open** is running it.

**G-M7 — the chi-square column.** It comes from searches whose restarts mostly
disagree and whose maxima sit on prior edges. **Fixed**: a new appendix
subsection gives the protocol, the two that failed before it, the two gates,
and what it does not achieve; the caption says the column is what the search
reached and not a converged fit. The ordering among the four extensions is now
reported as indistinguishable on the evidence, and the reverse channel is said
to be carried for the theoretical reason and not because the data prefer it.

## Claims, priority and scope

**H-M1 — the novelty claim stood on a bibliography with no kinetics in it.**
**Fixed**: section 1.3 now states that the autocatalytic rate is Prout and
Tompkins, the conversion-fraction theory is Avrami's, the absorbing-state
setting is Hinrichsen's, and path dependence from self-reinforcement is the
defining property of reinforced processes from the Polya urn onward. What is
claimed is the combination used as a dark-sector law, weighed against section
10's finding that the data do not measure it.

**H-M10 and priority.** Five verified entries were cited nowhere, two of them
the interacting-vacuum--geodesic-CDM papers that constrain precisely the
scenario `asm:geodesic` defines. Brown and Teitelboim were missing from a
subsection built on their mechanism. "Four-form realizations go back to
Bousso and Polchinski" was false. All **fixed**; `verify_bib.py` now reports
entries that verify and are never cited.

**H-M12 — the survey quoted with its conditional removed.** The survey
concludes that negative densities arise *if energy flows from dark matter to
dark energy*, and reads that as a preference for the opposite direction —
which is this model's direction. **Fixed**: the opening states it, states that
the model is on the disfavoured side, and argues the case from the survey's
own result: exactly one of its eight couplings keeps every density positive,
and it is the one whose outflow vanishes on each face, which is the criterion
this section states. The editorial audit records the elision as C-08 and
records that the audit missed it.

**F-M1 — "three obstructions, one root" was false as stated.** The caustic and
branching-ratio obstructions are carried by the localized product, which is
dust, and no change to the recipient lifts them. **Fixed**: two roots and two
modifications, in the abstract, in section 13.8 and in the conclusions, with
section 13.8 also saying that its own three are corollaries of one line and
claiming no depth for the derivation.

**F-M2, F-M7, F-M5, F-M6 and the eleven minors** — an internal contradiction
about `zeta`, a caustic-free assumption described as "not established" when it
is false throughout the fitted range, a local activation switch inconsistent
with the closure it is used beside, and a proposition whose conclusion needed
a hypothesis it did not state — all **fixed**, several with new tests. The
positivity proposition now separates the failure of forward invariance from
the crossing and gives the condition for each, with the referee's stiff-recipient
counterexample as a test.

**H-M2 — a result cannot be a theorem of the model in section 8 and a
conjecture in section 13.** **Fixed** by adding a level to the ladder: X,
"result of an auxiliary model", for something proved rigorously about a
different system. **H-M18** — level P was defined and never used; the two
profile limits now carry it. **H-M10, H-M9, H-M11, H-M13** — all fixed, and
the abstract's universal negative about density-proportional couplings is now
a proposition with a proof and a test rather than a sentence.

## What remains open

1. The evidence set has not been recomputed under the fixed queue size.
2. The two profiles have not been re-run from the corrected floor.
3. The threshold calibration is running.
4. The conservative-chronometer and alternative-`z_*` robustness runs are
   wired but not run.
5. Author metadata and the archive DOI, which need the author.

None of these changes a conclusion of the paper. All five change numbers that
the paper prints, which is why none of them is being written up before it is
run.
