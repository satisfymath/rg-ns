# Referee report

**Manuscript**: Self-reinforced geometric absorption
**Referee**: G (observational cosmology / Bayesian statistics; data analysis only)
**Round**: 2
**Date**: 2026-09-11

Scope of this report: §10 `sec:observations`, App. F `app:numerics`,
`code/absorb/likelihoods.py`, `code/absorb/data/*.py`, `code/absorb/early.py`,
`code/absorb/sampling.py`, `scripts/run_nested.py`,
`scripts/prior_width_evidence.py`, `scripts/summarise_posteriors.py`, and
`results/*.json`. I have not assessed the theory sections.

Excluded by instruction: author metadata placeholders, the Zenodo DOI, and the
in-flight recomputation of the "reinforce" chi-square row.

---

## Summary (3 lines)

The paper fits a one-way matter-to-vacuum conversion model to Pantheon+, DESI
DR2 BAO, cosmic chronometers and the Planck compressed distance priors, and
reports a null result: no parameter of the mechanism is measured, ΛCDM is
preferred on the Bayesian evidence by a few to one, and the model's two
signatures (jerk excess, matter deficit) are bounded far below present
sensitivity. The likelihood implementation is, with the exceptions below,
unusually careful, and the section is written with more candour than most
papers of this kind; the problems are in the archive, in the profile
optimisation, and in the calibration of two thresholds.

## Recommendation

[ ] Accept  [ ] Minor revision  [x] Major revision  [ ] Reject

The physics conclusion (a null result) is very likely to survive every
correction I ask for. I am nonetheless recommending major revision because one
of the archived results files is demonstrably not what it claims to be, and
because two of the three quoted numerical limits are derived from optimisations
that the authors' own files show did not converge, with thresholds whose
calibration the authors' own argument elsewhere invalidates.

---

## Major points

### M1. `results/posteriors/xi_h_baseline.npz` is not the baseline posterior. It is silently overwritten by the prior-width scan, and the corruption has propagated into two archived results files and into the generated macro file.

**Location**: `scripts/run_nested.py:88-94`; `scripts/prior_width_evidence.py:60-67`;
`scripts/evidence_repeatability.py:56`; `results/posteriors/xi_h_baseline.npz`;
`results/results.json` → `chains.xi_h__baseline`;
`results/prior_sensitivity.json` → `xi_h__baseline`;
`paper/generated/numbers.tex:315-360` (`\numChainsXiHBaseline*`);
App. F `app:numerics-availability`, `app:numerics` opening paragraph.

**What is wrong.** `run_nested.run()` writes
`results/posteriors/{model}_{dataset}.npz` unconditionally, with a filename
that encodes neither the prior box nor the seed.
`scripts/prior_width_evidence.py` mutates `absorb.params.PRIORS["log10_xi"]`,
reloads `run_nested`, and calls `run()` six times (three prior widths × two
seeds) — every call overwrites the same file. `scripts/evidence_repeatability.py`
does the same three more times. The file now on disk is the **last** of those
calls: `log10_xi` prior `[-7, 1]`, seed 12345.

This is not an inference; it is checkable in three independent ways:

| check | file on disk | `evidence.json` `xi_h__baseline` | `prior_width_evidence.json` `low=-7, seed=12345` |
|---|---|---|---|
| `n_samples` | 8936 | 9608 | — |
| `-2 max(logl)` | 1436.407264426867 | 1436.0660985900026 | `chi2_min` = 1436.407264426867 |
| `min(log10_xi)` | −6.9996 | prior floor is −3.0 | prior floor is −7.0 |

The consequences are in the archive, not only in a scratch file:

- `results/results.json` → `chains.xi_h__baseline.parameters.log10_xi` reads
  `value = -4.6054`, `lo95 = -6.7131`, `err = ±1.576`. The manuscript's stated
  baseline prior for `log10_xi` is `[-3, 1]` (`code/absorb/params.py:58`). The
  archived "baseline" posterior for the headline six-parameter model therefore
  lies **outside its own prior**, by more than three decades.
- `results/prior_sensitivity.json` → `xi_h__baseline.ln_bayes_full_prior` =
  −3.4953, against the −1.61 the manuscript quotes for the same quantity in
  `tab:comparison`. Its `n_in_box` at `shrink = 1.0` is 1359 (memory: 9724,
  reinforce: 9770) — the tell-tale signature of samples drawn from a box four
  decades wider than the one being shrunk.
- `paper/generated/numbers.tex` defines twenty-odd `\numChainsXiHBaseline*`
  macros from that entry. They happen not to be cited in the present draft, so
  no printed number is currently wrong. That is luck, not a control: the build
  gate described in App. F fails "if a macro is used that no results file
  defines" and "if the two disagree", neither of which can detect a macro
  *correctly generated from the wrong file*.

App. F states that "the chains' summary statistics and the results file are
archived"; as it stands the archive would ship a baseline posterior for `xi_h`
that is a different run under a different prior.

**What would fix it.** (i) Write the prior box and seed into the `.npz`
alongside `samples`, and have `summarise_posteriors.py` assert that the stored
box equals `absorb.params.PRIORS` before summarising; (ii) give
`prior_width_evidence.py` and `evidence_repeatability.py` a distinct output
path (or a `--no-save-samples` flag) so a variant run cannot clobber a
baseline; (iii) re-run `xi_h__baseline`, regenerate `results.json`,
`prior_sensitivity.json` and `numbers.tex`, and state in App. F which results
file each `\num...` family is generated from. A one-line gate that refuses to
summarise samples lying outside the current prior would have caught this.

### M2. The three profile likelihoods do not reach the model's own best fit. Their minima are provably 0.12–0.78 above it, so the two quoted 95% limits are anti-conservative and `\numProfileXiHBaselineMaxDeltaChiT` understates the true range by about a factor of two.

**Location**: `results/profile.json` (`xi_h__baseline`,
`xi_h__baseline__matter_deficit`, `xi_h__baseline__jerk_excess`); §10.3
`eq:observations-deficit-limit`, `eq:observations-jerk-limit`, and the
paragraph "The convertible fraction is not measurable, for a reason".

**What is wrong.** At `eps = 0` (equivalently at zero deficit, or zero jerk
excess) the model *is* ΛCDM with `omega_V_act` free, so the profile's value at
the origin can be no lower than the converged ΛCDM minimum,
`chi2 = 1436.5161` (`map.json.lcdm__baseline`, `converged: true`,
`chi2_spread = 9e-9`, 8 of 8 restarts reaching it, and reproducing the
40-restart brute-force reference). The `xi_h` best fit is 1434.8789
(`map.json`, confirmed independently by
`map_reference.json.xi_h__baseline` = 1434.8789394676678). Hence:

| profile | Δχ² at the origin | ⇒ profile minimum ≥ | shortfall vs. `xi_h` MAP |
|---|---|---|---|
| `eps` | 0.8592 | 1435.657 | **≥ 0.78** |
| `matter_deficit` | 1.5186 | 1434.997 | **≥ 0.12** |
| `jerk_excess` | 1.0802 | 1435.436 | **≥ 0.56** |

Grid coarseness does not explain this. A parabola through the three points
bracketing each minimum puts the true inter-node minimum no more than ~0.03
below the best node in all three cases.

Two consequences:

1. The sentence "Profiling the likelihood in ε over [0,0.6] never raises χ² by
   more than 0.859 above its minimum" is wrong by roughly a factor of two: the
   correct range over that interval is ≥ 1.64. (The stated conclusion — that
   2.71 is never reached — survives.)
2. Both quoted limits are too tight. Re-reading the `Delta chi2 = 2.71`
   contour from a minimum lowered by the shortfall above, and interpolating as
   the code does (linearly in the quantity between grid nodes), gives
   `Delta < 0.0104` instead of `0.01015` (+2%) and `eps_0 < 0.037` instead of
   `0.0306` (**+22%**). A limit quoted to three significant figures cannot
   carry a 22% optimisation bias.

**What would fix it.** Seed each profile node from the model's MAP
(`map.json`/`map_reference.json`) as well as from its neighbour, increase the
local budget until the origin node reproduces `chi2_lcdm = 1436.5161` to
better than 0.01 and the profile minimum reproduces `chi2_xi_h = 1434.8789`,
and add a gate — you already have `check_map_reference.py` for the MAPs — that
fails the build if any profile minimum exceeds the corresponding model's
reference χ² by more than a stated tolerance. Then re-quote both limits.

### M3. The 95% limits use `Delta chi2 = 2.71`, i.e. Wilks' theorem, in exactly the situation the paper argues elsewhere makes Wilks inapplicable. The non-regularity argument is applied where it removes a number that hurt the conclusion and not where it would loosen a number that helps it.

**Location**: caption of `tab:comparison`; `scripts/run_nested.py` docstring
("That is Davies' problem — nuisance parameters present only under the
alternative"); §10.3, `eq:observations-deficit-limit`,
`eq:observations-jerk-limit`.

**What is wrong.** The caption's justification for dropping AIC and BIC is
correct and is the honest choice (both would have over-favoured ΛCDM, i.e. the
paper's own conclusion — I checked: `\numChainsLcdmBaselineAic` and `...Bic`
are computed and stored, and simply not printed). But the stated reason is
that the rate parameters are unidentified at `eps = 0`, so the asymptotic
parameter counting fails. That is precisely the Davies/Chernoff regime in
which the asymptotic χ²₁ null distribution of the profile-likelihood ratio
also fails, and `Delta chi2 = 2.71` is nothing but the 95th percentile of
χ²₁ for a one-sided limit. The manuscript takes the non-regularity as decisive
in the one place where it removes an unfavourable number, and ignores it in
the two places where it would loosen a favourable one. A referee will read
that as selective.

To be clear about the direction: the boundary at `Delta >= 0` on its own is
handled correctly by 2.71. The problem is the *additional* unidentified
nuisance directions (`log10_xi`, `z_act`, and `omega_V_act` along the
degeneracy) present only when the constrained quantity is non-zero.

**What would fix it.** Either (a) calibrate the threshold by Monte Carlo:
generate ~200 synthetic data vectors from the ΛCDM best fit with the true
covariances, run the identical constrained profile on each, and take the 95th
percentile of the resulting `Delta chi2` — then quote *that* threshold and the
limits it gives; or (b) drop the profile limits and quote the posterior
95% upper limits instead, which need no asymptotic theory (you already
have `Delta < 0.0109` in `tab:parameters` from the nested samples), stating
plainly that they are prior-dependent. Option (a) is the stronger paper.
Whichever is chosen, one sentence must reconcile it with the `tab:comparison`
caption.

### M4. `ln Z` is not reproducible at the precision quoted, not even at fixed seed, and the manuscript prints two different values of the same Bayes factor two pages apart without comment.

**Location**: §10.3 `tab:comparison` (`ln B = -1.61 ± 0.29` for `Gamma = xi H`);
§10.3 prior-width table (`[-3,1]` baseline row, `\numWidthLnBayesBaseline` =
`-1.93`); §10.3 "By contrast the sampler's own noise is small";
`results/evidence.json`, `results/evidence_repeatability.json`,
`results/prior_width_evidence.json`.

**What is wrong.** The archive contains six independent estimates of `ln Z`
for the *same* quantity — model `xi_h`, dataset `baseline`, prior
`log10_xi in [-3,1]`, `nlive = 500`, `dlogz = 0.1`:

| source | seed | ln Z |
|---|---|---|
| `evidence.json` | 20260909 | −733.895 |
| `evidence_repeatability.json` | (3 seeds) | −733.935, −734.088, −733.796 |
| `prior_width_evidence.json` `low=-3` | 20260909 | −734.169 |
| `prior_width_evidence.json` `low=-3` | 12345 | −734.264 |

Full range 0.468; sample s.d. 0.18. Two of these used **the same seed**
(20260909) and differ by **0.274** — `dynesty` with `sample="rwalk"` and a
process pool is not deterministic in the number of workers (`run_nested.py`
takes it from `require_workers`; `prior_width_evidence.py` defaults to
`--workers 6`), so the recorded seed does not pin the answer. App. F states
"Random seeds are fixed and recorded" and that "the build is reproducible with
a single command"; for `ln Z` that is not true as the scripts stand.

The consequence for the manuscript is visible on the page: `tab:comparison`
gives `ln B = -1.61` and the prior-width table on the next page gives `-1.93`
for the identical configuration, a difference of 0.32 — larger than the
0.146 the text immediately afterwards offers as the sampler's noise, and
comparable to the ±0.29 error bar. A reader who notices will not trust either.

The repeatability evidence itself is thinner than the text implies: `n = 3`,
one model, `ndim = 6`. The two hardest cases — `memory` (9 parameters) and
`track_b` (10, and the one the physics discussion leans on) — have no
repeatability run at all, and it is exactly in those that `nlive = 500` with a
degenerate, prior-edge-hugging posterior is most likely to break the
information-based `logzerr`.

**What would fix it.** (i) Either fix the worker count and the `rstate` so a
seed reproduces `ln Z` bit-for-bit, or stop claiming seed reproducibility for
`ln Z` and quote instead the empirical run-to-run scatter as the error;
(ii) pool all six existing `[-3,1]` runs and quote `ln B` as their mean with
the empirical s.d. (that is `-1.9 ± 0.2` on the numbers above, not
`-1.61 ± 0.29`), or explain why the `evidence.json` run is preferred to the
other five; (iii) run at least two seeds for `memory` and `track_b` before
quoting their `ln B` to two decimals; (iv) make the two tables in §10.3 agree
or say in one sentence why they do not.

### M5. `KAPPA_RS` is a 0.21% multiplicative correction applied to a quantity measured to 0.030%, calibrated at a single cosmology, and its constancy across the prior volume — the entire basis for calling it legitimate — is asserted and never tested.

**Location**: `code/absorb/early.py`, `recipe_offsets()` and `kappa_rs()`;
`cmb_distance_priors()`; §10.1 third "choice that deserves to be stated";
App. F `app:numerics-likelihoods`.

**What is wrong.** Running `recipe_offsets()` gives:

```
z_*        = 1091.909   (Planck 2018: 1089.92)      offset +0.183%
l_A(raw)   =  302.099   (published 301.471)         offset +6.97 sigma
r_s(z_*)   =  144.269 Mpc  ->  kappa_rs = 1.0020819
R(raw)     =    1.75010  (published 1.7502)         offset -0.02 sigma
```

So the correction is +0.208%, while `sigma(l_A)/l_A = 0.0299%`. The recipe is
being repaired by seven standard deviations of the datum it is used to fit.
That is defensible **only** if `kappa` is genuinely a constant of the recipe
over the region the sampler visits. The sensitivity is brutal: differentiating
the recipe at the fiducial background, moving `z_*` by **0.48** moves `l_A` by
one sigma. The Hu–Sugiyama (1996) fit used for `z_*` is quoted in the module's
own docstring as accurate "at the ~0.1% level", i.e. ±1.1 in `z_*`, i.e.
**±2.3 sigma of `l_A`**, and its error is a function of `omega_b` and
`omega_m`, not a constant. Over the `omega_b in [0.019, 0.026]`,
`omega_c in [0.05, 0.25]` prior box the recipe's `z_*` ranges over
1089.97–1093.84 in the corner sample I ran; there is no reason for the *error*
in that fit to be the same at both ends, and the analysis has no way to know.

A second, related problem: `kappa` is not a pure sound-horizon correction. It
is defined as `pi D_M(z_*^recipe) / (l_A^published * r_s^recipe)`, so it
absorbs the `z_*` error twice over — once through `r_s(z_*)` and once through
`D_M(z_*)` — and then re-expresses the whole of it as a rescaling of `r_s`.
Those two pieces do **not** scale together in a model whose `D_M(z)` is
modified at low redshift, which is the entire point of the analysis.

Two things I checked and found *not* to be problems, which the authors should
say explicitly rather than leave a referee to discover: `R` is not
`kappa`-corrected, but it does not need to be — `D_M(z_*)` changes by only
0.0027% over `Delta z_* = 2`, against `sigma(R)/R = 0.263%`, so the `z_*` fit
error is a 0.01-sigma effect in `R`. And the neutrino term in `z_star()`
shifts `z_*` by 0.056 (0.1 sigma of `l_A`), consistent with the docstring.

**What would fix it.** The honest and cheap fix is to stop pretending the
correction is exact: add a systematic to the `l_A` entry of the compressed
covariance equal to a stated fraction of the correction itself — e.g.
`sigma(l_A)^2 -> sigma(l_A)^2 + (f * 0.00208 * l_A)^2` with `f = 0.25`, which
inflates `sigma(l_A)` from 0.090 to 0.17 — and show the conclusions are
unchanged. The better fix is to replace `z_star()` and the two-fluid `r_s`
recipe with a Boltzmann-calibrated fitting formula valid over the prior box
(several exist post-2018), recalibrate `kappa` at three or four widely
separated cosmologies inside the prior, and report `max|kappa_i/kappa_0 - 1|`
against `sigma(l_A)/l_A = 0.030%`. Either way, quote the numerical value of
`KAPPA_RS` in the text — §10.1 and App. F currently describe it without
printing it.

### M6. The compressed CMB likelihood is used where its derivation does not apply: the conversion is active at redshifts that generate CMB lensing and the late ISW, and the compression's covariance assumes one matter density where this model has two.

**Location**: `code/absorb/likelihoods.py`, `PlanckPriorLikelihood.model()`;
`code/absorb/data/planck_priors.py` module docstring; §10.1 second "choice that
deserves to be stated".

**What is wrong.** The manuscript's defence is that the pre-recombination
physics is identical, "the conversion rate at recombination is below 1e-21 of
the expansion rate". That is necessary and I accept it. It is not sufficient,
for two reasons.

(a) *Redshift range.* The posterior for `z_act` is not confined to the very
late universe: median 7.7 (memory), 11.6 (`xi_h`), 11.9 (reinforce), 19.7
(track_b), with `q95` reaching 21.5–27.8 (`results/evidence.json`). Conversion
of CDM into vacuum beginning at `z ~ 20–28` changes the growth of the lensing
potential over the whole range that Planck's lensing reconstruction and the
smoothing of the acoustic peaks are sensitive to, and it changes the late ISW.
A three-number geometric summary `(R, l_A, omega_b)` carries none of that.
Whether the compression over- or under-constrains the model here is not
obvious, and the paper cannot claim it is conservative without showing it.

(b) *Which `omega_m`.* The choice to evaluate `R` and `z_*` with the
pre-activation `omega_b + omega_c + omega_nu` rather than today's is, I agree,
the right one for the role those densities play in the acoustic physics, and
the docstrings argue it well. But the Chen–Huang–Wang compression and
especially its correlation matrix (`rho(R, omega_b) = -0.66`) were derived from
chains in which a *single* `omega_m` plays both the early and the late role.
In this model they differ by the deficit `Delta`. Using the published
covariance for a model that breaks that identification is an extrapolation of
the compression outside its validation set, and it should be labelled as one.

There is also an internal inconsistency in the provenance of these numbers:
`code/absorb/data/planck_priors.py` attributes them to "Planck 2018
TT,TE,EE+lowE", while `code/absorb/early.py`'s `PLANCK18` comment attributes
the very same `R` and `l_A` — which are then used to define `KAPPA_RS` — to
"TT,TE,EE+lowE+lensing". One of the two is wrong, and since `kappa` is tuned
to reproduce `l_A` exactly, it matters which chain `301.471` came from.

**What would fix it.** State the validity limitation explicitly in §10.1,
including the `z_act` posterior range that makes it live rather than academic;
reconcile the two provenance strings; and report the `nocmb` combination (it
is already implemented in `datasets.py`) as a headline robustness row rather
than only mentioning that it exists. If the conclusions are identical without
the compressed likelihood — I expect they are, since the result is null — that
row does more for the paper's credibility than the calibration argument does.

### M7. Every number in the `chi2_min` and `Delta chi2` columns of `tab:comparison` for an extended model comes from a maximisation the authors' own `map.json` records as not converged, at a point sitting on one or more prior boundaries; and a physics inference is drawn from a ranking that is not significant.

**Location**: `paper/generated/tab_comparison.tex`; `results/map.json`;
§10.3, paragraph beginning "Two features of the table are worth more than the
headline".

**What is wrong.** `results/map.json` reports, for the four extended models:

| model | `converged` | `chi2_spread` | `n_reaching_best` / `n_refined` | `on_prior_edge` |
|---|---|---|---|---|
| `xi_h` | false | 18.5 | 1 / 9 | `omega_V_act`, `log10_xi` |
| `reinforce` | false | 5.77 | 1 / 9 | `omega_V_act` |
| `memory` | false | 1.62 | 1 / 10 | `omega_V_act`, `alpha_tot` |
| `track_b` | false | **75.4** | 1 / 11 | `omega_V_act`, `alpha_tot` |

The `Delta chi2` differences being reported are 1.6–6.8. For `track_b`, whose
`Delta chi2 = -6.77` carries the paragraph "the model that does best is the one
with the *most* parameters ... the data lean that way weakly", the spread among
restarts is **eleven times** the effect, and exactly one restart out of eleven
found it. The reported `xi_h` optimum has `log10_xi = 0.99999997` against a
prior ceiling of 1.0 and `omega_V_act = 1.5e-9` against a floor of 0; the
`reinforce`/`memory` optimum has `alpha_tot = 7.99999` against a ceiling of 8.
These are not maxima of the likelihood; they are corners of the prior box, and
`Delta chi2` values read off them are prior-limited numbers presented as
goodness-of-fit numbers. Nothing in §10 says so.

Separately, the physics inference does not survive its own error bars. The
evidences for the four extensions are `-1.39 ± 0.28` (track_b),
`-1.61 ± 0.29` (`xi_h`), `-2.10 ± 0.29` (memory), `-2.15 ± 0.29` (reinforce).
The gap between the best and the worst is 0.77, and the error on a *difference*
between two extensions (the ΛCDM reference cancels) is `sqrt(0.21^2+0.21^2) =
0.30`. That is 2.6 sigma at best, before M4's run-to-run scatter of ~0.2 and
before the prior-width range of 1.39 documented in the same section. "The data
lean that way weakly" is being used to justify carrying the reverse channel and
to connect to the DESI-era `delta_eff > 0` literature; a 2-sigma ordering among
four evidences whose common prior dependence is five times larger will not
support that.

**What would fix it.** (i) Add `converged`, `chi2_spread` and `on_prior_edge`
to `tab:comparison` or to its caption, or state in the caption that the
`Delta chi2` column is a lower bound from a bounded search and should not be
read as a fit quality; (ii) either re-run the extended MAPs to convergence
(you have `map_reference.json` showing a 40-restart protocol exists) or drop
the `Delta chi2` column; (iii) rewrite the "leans that way weakly" sentence to
say that the four extensions are indistinguishable on the evidence at the
precision available, and that the reverse channel is carried for the
theoretical reason, not because the data prefer it.

### M8. The cosmic-chronometer covariance is the reduced Moresco systematic budget, not the "full covariance" App. F claims; the conservative variant that does match the published budget is implemented, tested, and never run.

**Location**: `code/absorb/data/cc.py:55-57` (`VARIANTS`);
`ChronometerLikelihood(variant="default")` via `datasets.py:37`;
App. F `app:numerics-likelihoods` ("Cosmic chronometers use the Moresco
compilation with the full covariance built from the published systematic
budget"); `tab:datasets` ("15 measurements of H(z), full covariance").

**What is wrong.** The `default` variant builds
`C = diag(err^2) + C_IMF + C_mod_ooo`. The `conservative` variant adds `stlib`
and `mod`. Running both:

| variant | effective sigma on a coherent H(z) offset |
|---|---|
| `default` (used everywhere) | 4.88 km/s/Mpc |
| `conservative` (never run) | 11.80 km/s/Mpc |

a factor 2.4. Calling the smaller of the two "the full covariance built from
the published systematic budget" is not accurate, and the paper's own
`cc.py` docstring says as much: the conservative variant "adds the stellar
library (`stlib`) and the full model spread (`mod`), which roughly doubles the
error bars". The docstring's defence of the default — "the combination used in
the Moresco et al. (2020) baseline and in most subsequent analyses" — is
asserted without an equation or table reference, and is contestable; MM20's
recommended total does include the stellar-library and SPS-model terms.

A second, smaller point in the same construction: the quoted `errHz` column
already contains the metallicity systematic (`errHz^2 ≈ stat^2 + met^2`, which
I verified on every row), and it is put in the diagonal, i.e. treated as
uncorrelated between redshifts. MM20 treats the metallicity term as partly
coherent. This makes the CC constraint tighter than MM20 would allow.

**What would fix it.** Change App. F and `tab:datasets` to say which
contributions enter the baseline covariance (name them), give the equation or
table number in Moresco et al. (2020) that the default combination
corresponds to, and add a `conservative` robustness row to `tab:comparison` or
at least a sentence reporting `ln B` under it. The run is cheap and the result
is almost certainly unchanged, which is the point.

### M9. The Bayes factor cannot falsify the preference it reports: by construction it tends to zero as the log-rate prior widens. This is half-stated and then used anyway.

**Location**: §10.3, paragraph "How much of that is the prior" and its table;
`results/prior_width_summary.json`; `code/absorb/params.py:58`.

**What is wrong.** The statistic is monotone in a quantity the data do not
determine, and in only one direction. Widening `log10_xi` downward adds prior
volume in which the likelihood is *bit-identical* to ΛCDM's, so `Z_model`
tends to `Z_LCDM` and `ln B` tends to 0 from below:

```
[-3,1]  ln B = -1.93   (odds 6.9:1)
[-5,1]  ln B = -0.80   (odds 2.2:1)
[-7,1]  ln B = -0.55   (odds 1.7:1)
```

The manuscript's gloss — "The verdict does not change sign anywhere in it —
ΛCDM is preferred under every prior we would defend" — is true but vacuous:
the sign *cannot* change by this mechanism, because the supremum of `ln B`
over prior widths is 0. So the statement "ΛCDM is preferred" carries no
information beyond "the model contains ΛCDM", and the *magnitude* of the
preference is a pure statement about the author's choice of `-3` rather than
`-7`. The section does then say "its strength is not determined by the data",
which is the right sentence — but it is followed by a paragraph that ranks four
models by exactly this statistic (M7) and by a figure caption that reports
`ln B` moving from `-1.61` to `-1.83` on adding growth data as if 0.22 were a
result.

**What would fix it.** Say, in one sentence, that `ln B < 0` is guaranteed here
and therefore not a test, and that the reportable content is the *rate* at
which `ln B` approaches 0 with prior width — which is a statement about how
much of the prior the data exclude. Better: replace the headline with a
Savage–Dickey density ratio at `eps = 0`, which `params.py`'s own docstring
already anticipates ("the nested point used for the Savage-Dickey density
ratio") but which appears nowhere in the results; it is the prior-normalised
quantity appropriate to a nested comparison and it does not suffer this
pathology in the same form. Whatever is chosen, the four-model ranking and the
growth `Delta ln B` must be withdrawn or given errors that show them to be
null.

---

## Minor points

**m1.** §10.3, prior-width table, row `[-5,1]`: `-0.80` and `2.2:1` are typed
decimal literals, while the rows above and below use
`\numWidthLnBayesBaseline` / `\numWidthLnBayesWidest` /
`\numWidthOddsBaseline` / `\numWidthOddsWidest`. Both values are correct
(`results/prior_width_summary.json` gives −0.7988 and `exp(0.7988) = 2.223`),
but App. F states that the build "fails ... if a decimal literal appears in the
prose outside a short whitelist". Either the gate does not cover tables or the
whitelist is being used. Generate the middle row from the results file like
the others.

**m2.** §10.3, paragraph heading "One chain is quoted from and three are not."
`results/chains/` contains three files (`lcdm_baseline`,
`reinforce_baseline_demove_frozen`, `xi_h_baseline_demove_frozen`) and
`results/chain_diagnostics.json` three entries. One is quoted from and **two**
are not. Either the count is wrong or two chains are missing from the archive
that the sentence relies on.

**m3.** `tab:parameters` presents `z_act = 7.7003 (+10.5660, -6.4007)` at 71%
prior filled and `beta/(alpha+beta) = 0.5000 (+0.2659, -0.2518)` at 75% as
measurements, while `eps` (83%), `log10(tau_M H_100)` (87%) and `alpha+beta`
(89%) are correctly marked *unconstrained*. The `r_beta` median is the prior
midpoint to five digits. §10.2 says of these same five parameters "They are not
measured here"; the table contradicts it for two of them. Worse,
`log10(Gamma_0/H_100) = -1.5970 (+0.4812, -0.2558)` is shown at only 34%
prior filled and reads as the one rate parameter that *is* measured — but its
`q05 = -1.964` sits 0.036 from the prior floor of `-2.0`, and 9.5% of the
posterior samples lie in the lowest 2% of the prior. It is a distribution
truncated by its prior, not a measurement, and the section's own prior-width
study on the identical parameter of `xi_h` proves the point. Report it as an
upper limit with the prior floor stated, and either mark `z_act` and `r_beta`
unconstrained or lower the threshold that decides.

**m4.** `results/profile.json`, `xi_h__baseline__matter_deficit`:
`n_unreachable = 1` — the largest target, `Delta = 0.1995`, has
`achieved = nan`. §10.3 reports the two diagnostics that succeeded
(`max_target_miss_rel`, `n_non_monotone_steps`) and not this one. The 95%
limit lies well inside the reached range so nothing is affected, but a
diagnostic that is reported when it passes and omitted when it fails is the
kind of thing this section otherwise avoids. Report it.

**m5.** The BAO ruler and the CMB ruler come from different, mutually
uncalibrated recipes. `DesiBAOLikelihood` uses the raw Aubourg et al. (2015)
Eq. (16) fit, which at the Planck fiducial gives `r_d = 147.063` against
147.09 (−0.019%, entirely acceptable, and I confirmed the formula is
transcribed correctly). `PlanckPriorLikelihood` uses the `kappa`-corrected
integral, giving `r_s(z_*) = 144.569` against Planck's 144.43 (+0.096%). The
ratio `r_s(z_*)/r_d` in this pipeline is therefore 0.11% larger than Planck's,
which is a coherent ~0.4-sigma shift of the DESI distance scale that is neither
propagated nor mentioned. Additionally, no uncertainty at all is assigned to
`r_d`. Add an `r_d` calibration nuisance with a stated width (0.2% is the
conventional choice) and marginalise it, or state in App. F that it is
neglected and why.

**m6.** `datasets.py:18-30`: the RSD likelihood holds `sigma_8 = 0.8111`, the
Planck ΛCDM value, fixed. The docstring's justification — "letting sigma_8
float would absorb precisely the effect being tested" — is backwards: in this
model the matter density falls after activation, so `sigma_8(z=0)` is a derived
quantity that *must* change, and pinning it at the ΛCDM value imports the null
hypothesis into the alternative's prediction. The result that growth data move
`ln B` from −1.61 to −1.83 is therefore not a fair test of the model's growth
signature. The docstring also promises "Section 10 reports the result both
ways"; §10 contains no discussion of `sigma_8` at all. Either marginalise
`sigma_8` (it is already in `PRIORS`) or state the choice and its direction in
§10 and in the caption of `fig:signatures`.

**m7.** `fig:signatures` caption: "Including these data moves `ln B` from
−1.61 to −1.83: the model's sharpest linear prediction does not improve its
standing." The change is −0.217 against per-evidence errors of ±0.29 and the
run-to-run scatter of M4. This is consistent with zero. Say so.

**m8.** `JointLikelihood` treats its components as independent
(`likelihoods.py`, class docstring). For the `rsd` combination that is not
right: the SDSS DR16 LRG and QSO `f sigma_8` points come from volumes that
overlap DESI DR2's LRG and QSO samples on the sky. `RSDLikelihood`'s docstring
correctly drops the DR16 *geometric* entries for this reason but then adds the
`f sigma_8` entries from the same catalogues to a likelihood that already
contains DESI BAO. Quantify or acknowledge.

**m9.** `cc.py`, `_sigma_percent`: `np.interp` clamps the MM20 percentages to
their z = 1.475 values for the z = 1.965 chronometer. The docstring calls this
"the intended behaviour". It is the only available behaviour, not the correct
one; the SPS spread is not flat beyond the tabulation. One sentence noting the
extrapolation, or dropping that point as a robustness check, would close it.

**m10.** `planck_priors.py` attributes `(R, l_A, omega_b)` to Planck 2018
"TT,TE,EE+lowE"; `early.py`'s `PLANCK18` dict attributes the identical `R` and
`l_A` to "TT,TE,EE+lowE+lensing". See M6.

**m11.** §10.3: the `eps` profile covers `[0, 0.6]` while the prior is
`[0, 1]` and the posterior fills 83–92% of it. The text states the range, so
this is not hidden, but the conclusion "there is no upper limit to quote"
would be stronger if the profile covered the prior.

**m12.** Two different `chi2_min` values for each model live in the archive:
`evidence.json` stores `-2 max(logl)` over the nested live points
(`xi_h`: 1436.066; `track_b`: 1434.187) while `map.json` stores the optimiser's
value (1434.879; 1429.748), differing by up to 4.44. `tab:comparison` uses the
latter. A reader who opens `evidence.json` first will get a different table.
Name the source in the caption. (The gap itself is also worth a sentence: a
nested run with `nlive = 500` in 10 dimensions that never gets within
`Delta chi2 = 4.4` of the optimum is a hint that the peak is
under-resolved, which bears on M4.)

---

## What I checked and could *not* break

Listing these so the adequacy of the search can be judged, and because several
are done better here than in most submissions of this kind.

- **Pantheon+ analytic marginalisation over `M_B`.** Verified against a
  brute-force numerical integral over `M_B` at the Planck fiducial background:
  `chi2_marg = 1413.0608714` from the code, `1413.0608714` from
  `-2 ln integral exp(-chi2(M)/2) dM`, agreeing to `2.4e-8`. The Jacobian
  `ln(E_0/2pi) = 9.3251` matches `\numCheckMarginalisationJacobianBaseline`
  and is correctly flagged in the `tab:comparison` caption as not a chi-square.
  The `A - B^2/E_0` construction, the caching of `C^-1 1`, and the use of one
  triangular solve for `A` are all correct.
- **Pantheon+ covariance handling.** The `STATSYS` file is parsed correctly,
  the selection is applied as `C[ix_(idx, idx)]` (a sub-block, which is the
  correct marginalisation over dropped rows), symmetry is checked with a
  tolerance justified by the file's own ASCII precision, and positive
  definiteness is tested. No explicit inverse anywhere.
- **Pantheon+ selection and redshift frames.** `z_HD > 0.01` gives n = 1590,
  matching Brout et al. (2022); with SH0ES, n = 1657 with all 77 calibrators
  and `use_cepheid` set only for them. The 10 calibrators that survive the
  Hubble-flow cut are correctly treated as ordinary supernovae in the SN-only
  sample. `D_L = (1 + z_hel) D_M(z_hd)` is the correct Pantheon+ convention
  (mean `|z_hd - z_hel| = 9.3e-4`, max `2.9e-3`, so this matters and is right).
- **DESI DR2 data vector and ordering.** I reconstructed the published values
  and correlations from `desi_dr2_bao_mean.txt` and `desi_dr2_bao_cov.txt` and
  they match DESI DR2 to the digits published: BGS `D_V/r_d = 7.942 ± 0.076`;
  LRG1 `13.588 ± 0.168`, `21.863 ± 0.429`, `rho = -0.45`; QSO `30.512 ± 0.764`,
  `12.817 ± 0.518`, `rho = -0.49`; Lya `D_H/r_d = 8.632 ± 0.101`,
  `D_M/r_d = 38.989 ± 0.532`, `rho = -0.43`. The Lya block does have `D_H`
  before `D_M`, as the docstring warns, and the likelihood dispatches on the
  quantity string rather than on position, so the ordering trap is avoided.
  Cross-tracer blocks are zero, which is what DESI publishes.
  `D_V = (z D_M^2 D_H)^(1/3)` is correct.
- **`r_drag` fitting formula.** Aubourg et al. (2015) Eq. (16) is transcribed
  correctly, including the `exp[-72.3 (omega_nu + 0.0006)^2]` factor, and is
  called with `omega_cb` excluding neutrinos as that equation requires. The
  Brieden alternative is present and agrees to 5e-5 Mpc at the fiducial. The
  argument for using the pre-activation density is sound and is stated in three
  places. (The missing calibration *uncertainty* is m5, not an error.)
- **The shift parameter `R`.** Insensitive to the `z_*` recipe error at the
  0.01-sigma level (see M5), correctly normalised by `100/c`, and evaluated
  with the pre-activation `omega_m` for a defensible and clearly stated reason.
  `dR_sigma = -0.02` at the Planck best fit.
- **`z_star`.** Hu & Sugiyama (1996) Eq. (E1) transcribed correctly; the
  neutrino inclusion shifts it by 0.056, consistent with the docstring's claim
  of "well under one".
- **The sound-horizon integral.** The split at the background grid edge with a
  closed-form radiation-era continuation is correct and necessary (the sub-grid
  tail really is ~9 Mpc), and the Gauss–Legendre rule is more than adequate.
- **The Moresco rank-one construction.** Given the choice of contributions,
  `C += outer(s, s)` with `s = H * sigma_pct / 100` is the right way to encode
  a fully coherent percentage systematic. (The issue is *which* contributions —
  M8.)
- **RSD sub-block extraction.** `fs8_block()` takes rows *and* columns of the
  covariance, which is the correct marginalisation over the dropped geometric
  entries, not the common error of taking only the diagonal.
- **The decision to omit AIC and BIC.** Correct, correctly justified, and
  against the authors' own interest — both are computed
  (`\numChainsLcdmBaselineAic` = 1443, `...Bic` = 1459) and both would have
  favoured ΛCDM more strongly. My objection (M3) is that the same argument is
  not applied to the `Delta chi2 = 2.71` thresholds, not that this choice is
  wrong.
- **Honesty of the null result, in the main.** The withdrawn `eps` upper limit,
  the withdrawn earlier AIC/BIC comparison, the withdrawn earlier penalty-based
  profile, the "prior filled" column, the explicit statement that five of nine
  parameters are unmeasured, the disclosure that the extended ensemble chains
  failed and why, and the `theory_checks.json` entry recording that the
  deficit-floor hypothesis fails at **every one of 399** draws tested — with
  §10 saying so in the text rather than quietly dropping the relation — are all
  to the paper's credit and are unusual. The problems above are failures of
  numerical control and of threshold calibration, not, with the possible
  exception of M3, of candour.

---

## Questions the authors must answer

1. Which run produced `results/results.json` → `chains.xi_h__baseline`, and how
   does a posterior whose 5th percentile in `log10_xi` is −6.71 come to be
   recorded under a prior of `[-3, 1]`? (M1)
2. Why do `tab:comparison` and the prior-width table in the same section report
   `ln B = -1.61` and `ln B = -1.93` for the same model, prior and data, and
   which is the paper's number? (M4)
3. What is the numerical value of `KAPPA_RS`, and what is
   `max|kappa(theta)/kappa(theta_fid) - 1|` over the prior box, in units of
   `sigma(l_A)/l_A = 0.030%`? (M5)
4. If the rate parameters are unidentified at `eps = 0` — which is why AIC and
   BIC are dropped — on what grounds is `Delta chi2 = 2.71` the right 95%
   threshold for `eq:observations-deficit-limit` and
   `eq:observations-jerk-limit`? (M3)
5. Why is the `eps`-profile minimum 0.78 above the `xi_h` maximum-likelihood
   value that `map_reference.json` independently confirms? (M2)
6. What is `ln B` for `xi_h` on the `nocmb` combination, and under the
   `conservative` chronometer covariance? Both are implemented and neither is
   reported. (M6, M8)
7. Does any conclusion in §10 change if `sigma_8` is marginalised rather than
   held at the Planck ΛCDM value in the `rsd` combination? (m6)
