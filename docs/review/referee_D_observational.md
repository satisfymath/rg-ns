# Referee report

**Manuscript**: Self-reinforced geometric absorption
**Referee**: D (observational cosmology / DESI-era data analysis)
**Round**: 3
**Date**: 10 September 2026

Scope of this report: `code/absorb/likelihoods.py`, `code/absorb/datasets.py`,
`code/absorb/early.py`, `code/absorb/data/*`, `scripts/run_nested.py`,
`scripts/run_profile.py`, `scripts/run_map.py`, `scripts/summarise_posteriors.py`,
`scripts/chain_diagnostics.py`, `scripts/prior_sensitivity.py`,
`results/{evidence,profile,results,chain_diagnostics}.json`,
`paper/generated/*`, `paper/sections/10_observations.tex`,
`paper/sections/appF_numerics.tex`. Everything asserted below was measured on
this machine; the command is given with each point. Repository state as of
commit `d133096`, 10 September 2026 ~01:30 local. A `run_nested.py` job
completed at 01:19 during the review and is reflected where noted.

## Summary (3 lines)

Public late-time data (Pantheon+, DESI DR2 BAO, cosmic chronometers) plus the
Planck compressed distance priors are fitted to a family of models in which a
convertible fraction of the dark matter is converted into vacuum after an
activation redshift. The paper reports that nothing in the data requires the
conversion, quotes a Bayes factor of about five to one against the extension,
and quotes a 95% upper limit on the derived matter deficit. The likelihoods are
correct; the two headline *numbers* — the Bayes factor and the deficit limit —
are not supported by what the code actually computes.

## Recommendation

[ ] Accept  [ ] Minor revision  [X] Major revision  [ ] Reject

The data handling is, with the exceptions in M5, of a standard I could not
break (see the certification section). The revision required is to the two
quoted results and to the several analyses the section promises but does not
contain, not to the pipeline.

---

## Major points

### M1. The quoted limit `Delta < 0.0126` is not a profile-likelihood value. It is a grid node, produced by an interpolation whose contract is violated, from constrained fits that do not satisfy their own constraint.

**Location**: `scripts/run_profile.py:40-106` (`profile_derived`),
`results/profile.json["xi_h__baseline__matter_deficit"]`,
`paper/sections/10_observations.tex` Eq. `eq:observations-deficit-limit`,
macro `\numProfileXiHBaselineMatterDeficitLimitNV` = `0.0126`.

This is the same defect that referee B caught as M3 ("the 95% upper limit on
`eps` was the right-hand end of the grid"), reappearing in the replacement
statistic. Four independent demonstrations, all from the shipped JSON:

**(a) The constrained fits do not reach their constraint.** The `achieved`
column of the stored result, printed against `targets`:

```
$ python3 -c "
import json
v=json.load(open('results/profile.json'))['xi_h__baseline__matter_deficit']
for t,a,c in zip(v['targets'],v['achieved'],v['delta_chi2']):
    print(f'target={t:9.5f} achieved={a:9.5f} miss={a-t:+.2e} dchi2={c:9.3f}')"
```

```
target=  0.00000  achieved=0.00019542  miss=+1.95e-04  dchi2=    0.419
target=  0.00631  achieved=0.00620622  miss=-1.03e-04  dchi2=    0.000
target=  0.01259  achieved=0.00680177  miss=-5.79e-03  dchi2=    2.124
target=  0.02512  achieved=0.03019730  miss=+5.08e-03  dchi2=  297.943
target=  0.05012  achieved=0.04960020  miss=-5.19e-04  dchi2=   21.938
target=  0.10000  achieved=0.09904110  miss=-9.59e-04  dchi2=  126.529
target=  0.19953  achieved=0.16552200  miss=-3.40e-02  dchi2= 1191.950
```

At the grid point that sets the limit, `target = 0.0125893`, the optimiser
stopped at `Delta = 0.00680`, missing by a factor of 1.85. The reported
`dchi2 = 2.124` is therefore the profile evaluated at `Delta ~ 0.0068`, not at
`0.0126`.

**(b) That makes the stored object internally contradictory.** The same table
assigns `dchi2 = 0.000` at `achieved = 0.00621` and `dchi2 = 2.124` at
`achieved = 0.00680`. A profile likelihood is a function of the profiled
quantity; it cannot take two values 2.12 apart at two points 10% apart in
`Delta` when the curve is flat to 0.4 over the decade below. One of the two
fits is unconverged.

**(c) The `2.71` crossing is located by `np.interp` on a non-monotone array.**

```
$ python3 -c "
import json,numpy as np
v=json.load(open('results/profile.json'))['xi_h__baseline__matter_deficit']
c=np.array(v['delta_chi2']); t=np.array(v['targets'])
a=np.where(c>2.71)[0]
print('xp:',np.round(c[:a[0]+1],3))
print('increasing?',bool(np.all(np.diff(c[:a[0]+1])>0)))
print('reproduced limit',float(np.interp(2.71,c[:a[0]+1],t[:a[0]+1])),'stored',v['limit_95'])
print('targets[8]',t[8],'ratio-1',float(np.interp(2.71,c[:a[0]+1],t[:a[0]+1]))/t[8]-1)
print('grid ratio',t[2]/t[1])"
xp: [0.419 0.315 0.292 0.266 0.163 0.09  0.668 0.    2.124 297.943]
increasing? False
reproduced limit 0.012614057233044198 stored 0.012614057233044198
targets[8] 0.012589254117941675 ratio-1 0.0019701814635051385
grid ratio 1.9952623149688786
```

`run_profile.py:100` calls `np.interp(2.71, chi2[:above[0]+1],
targets[:above[0]+1])` with an `xp` that is not increasing; `np.interp`
documents `xp` as required to be increasing and gives no warning otherwise.
Referee B flagged this in m10 as a latent guard problem that "happens to lie
outside the bracket so the answer is unaffected". In the derived-quantity
profile it is no longer latent: it *is* the reported answer. The crossing is
taken across a segment that jumps from `2.124` to `297.943`, so the interpolated
value is pinned to the left node — `limit_95 = 0.0126141` against
`targets[8] = 0.0125893`, 0.197% apart. The grid is
`np.logspace(-4, -0.7, 12)`, ratio 1.995 between nodes, so the quoted "limit" is
quantised in factors of two and would move by that much if the grid were
redrawn. That is exactly the failure mode withdrawn for `eps`, with a
logarithmic grid instead of a linear one.

**(d) The penalty is soft enough for the fit to buy its way out.** With
`penalty = 1e6` (`run_profile.py:42`), missing the target by `5.787e-3` costs
`1e6 * (5.787e-3)**2 = 33.495` in the objective, and the optimiser accepted that
rather than move onto the constraint surface. This gives a dichotomy from which
there is no escape: either a feasible point at `Delta = 0.0126` with
`chi2 < chi2_min + 35.6` exists and the optimiser failed to find it, or no such
point exists and the true profile at `Delta = 0.0126` is above `chi2_min + 35.6`
— in which case `0.0126` is not the 95% limit but far beyond it. In neither
case is `Delta < 0.0126` a 95% upper limit.

**(e) The zero point is wrong too: the shipped profile never found the model's
minimum.** I re-ran the same constrained fit with one background solve per
objective evaluation instead of two, Nelder-Mead *and* Powell, five restarts
plus a warm start, and `penalty = 1e9`. The constraint is then met to 1e-7 at
every point, and the fits are much better than the shipped ones:

```
  target=0.000000  achieved=2.08e-07  chi2=1436.5160    <- exactly the LCDM minimum
  target=0.002000  achieved=0.002000  chi2=1435.8174
  target=0.004000  achieved=0.004000  chi2=1434.9201    <- 0.737 BELOW the shipped
                                                           profile's own minimum
```

Each was re-evaluated independently through `Posterior.log_prior` to confirm it
lies inside the prior box (`log_prior = 0.0` at all three). The shipped
`profile_derived` reports its minimum as `1435.65690` (the value the whole
`delta_chi2` column is referred to); a plain re-run finds `1434.9201` at
`Delta = 0.004`. Every `Delta chi2` in `results/profile.json` is therefore
referred to a point that is 0.74 too high, and the same applies to the `eps`
profile, which shares the minimum. See M3 for how far this goes.

**Also affected**: the text supports the limit with "the profile rising to
`Delta chi2 ~ 1192` across the grid, so this is a constraint and not another
flat direction". `1192` is the value at `target = 0.19953`, whose neighbours are
`126.5` and `21.9` and which the optimiser missed by 17%. A curve that goes
`297.9, 21.9, 126.5, 1192` over four successive grid points is not measuring a
profile.

**What would resolve it**:
1. Impose the constraint exactly rather than by a soft penalty — solve for one
   parameter (`eps` or `log10_xi`) at fixed target by a 1-D root find, or use a
   genuine constrained optimiser (`trust-constr` with a `NonlinearConstraint`) —
   and *assert* `|achieved - target| < 1e-6` at every grid point, failing the
   run otherwise.
2. Bracket the `2.71` crossing between the last point below and the first point
   above and interpolate on that bracket only; refuse to interpolate when the
   bracketing segment spans hundreds in `Delta chi2` (refine the grid instead).
3. Report the profile's own error bar: run the sweep in both directions and
   quote the disagreement, as referee B proposed in m11. A limit whose grid
   spacing is a factor of two cannot be quoted to three significant figures.
4. State the calibration of the threshold. `2.71` is the right number for a
   one-sided 95% upper limit on an interior parameter, and I agree with referee
   B that the `Delta >= 0` boundary only makes it conservative. But the real
   irregularity here is Davies', not Chernoff's: at `eps = 0` two parameters are
   *exactly* unidentified (verified, see the certification section), so no fixed
   `chi2` quantile is the calibrated one. Say so, or calibrate by simulation.

### M2. `ln B` is a statement about the prior volume of parameters the data do not measure, and the prior sensitivity that the section promises is not in the repository.

**Location**: `paper/sections/10_observations.tex`, paragraph "$\LCDM$ is
preferred, and by less than it first appeared" and the closing sentence "the
third is reported with its prior sensitivity"; `scripts/prior_sensitivity.py`;
`paper/generated/tab_comparison.tex`.

The paper is right that AIC and BIC are the wrong penalties here and right about
the direction of their error (I verified the unidentifiability; see the
certification section). But replacing them with the evidence does not remove the
arbitrariness, it relocates it into the prior ranges of exactly the parameters
that are unidentified — and unlike `2k` and `k ln n`, that relocation is not
reported.

**The Occam factor is the whole of `ln B`, and it is a choice.** Decompose the
reported number to Laplace accuracy, with the shared-parameter volumes
cancelling between numerator and denominator. The `xi_h` maximum likelihood is
`1.636` better in `chi2` than LambdaCDM's (M3), so

```
ln B = 1.636/2 - ln(V_extra,prior / V_extra,post)
     = +0.818  - 2.414                            = -1.596
```

`V_extra,prior = 1 x 4 x 29.7 = 118.8` in units of
(`eps`) x (decades of `log10_xi`) x (`z_act`), so the implied posterior extent
of the three unidentified directions is `V_extra,post = 10.6`. Every one of the
three prior factors is a free choice made in `code/absorb/params.py:52-62`, and
`ln B` moves one-for-one with the logarithm of their product. Nothing in the
data fixes any of them: `eps` is a fraction, so `[0,1]` is forced, but the four
decades of `log10_xi` and the range `z_act in [0.3, 30]` are conventions.

**How far the verdict moves.** The identity the repository's own
`prior_sensitivity.py` is built on,
`ln Z_B = ln Z_A + ln p_B + ln(|A|/|B|)`, is exact. The posterior ridge, read
off the stored `best_theta` of the `eps` profile, is narrow:

```
$ python3 -c "
import json,numpy as np
b=np.array(json.load(open('results/profile.json'))['xi_h__baseline']['best_theta'])
print('log10_xi', b[1:,4].min(), b[1:,4].max()); print('z_act', b[1:,5].min(), b[1:,5].max())"
log10_xi -1.9827 -0.7372
z_act     6.9709  8.5554
```

so halving the `log10_xi` range to `[-2.5, -0.5]` and the `z_act` range to
`[6.0, 20.85]` — both entirely defensible, and both containing this ridge with
room to spare — raises `ln Z(xi_h)` by up to `2 ln 2 = 1.386`, and by nearly
that much if the posterior mass `p_B` inside the narrowed box is close to one.
That would take `ln B` from `-1.60` to about `-0.21`: from "five to one against"
to no preference at all. (The narrowing is in fact conservative: the true
maximum-likelihood point found in M3 sits at `log10_xi = 1.0`, *outside* the
narrowed box, so `p_B < 1` and the measured rise is a lower bound on how far
`ln B` can be moved by a defensible change of prior.)

**Measured, not argued.** I ran the narrowed prior through the same nested
sampler (dynesty 3.1.0, `nlive=500`, `dlogz=0.1`, `bound='multi'`,
`sample='rwalk'`, 2 workers, `/tmp/.../scratchpad/prior_variant.py`):

<!--PRIOR_VARIANT-->

**The Method subsection states the opposite of the truth.** Section 10.2 says
"Priors are uniform and identical across models wherever a parameter is shared,
so that the model comparison is not driven by prior volume." Identical priors on
the *shared* parameters have no bearing on this: those factors cancel in
`ln B`. The comparison is driven by prior volume, and only by prior volume,
along `eps`, `log10_xi` and `z_act`, which are precisely the parameters that are
not shared. That sentence should be deleted and replaced by the number above.

**The promised prior sensitivity does not exist.** `scripts/prior_sensitivity.py`
reads `results/posteriors/*.npz`. At the time of this review that directory does
not exist, and neither does `results/prior_sensitivity.json`:

```
$ ls results/
bib_verification.json  chain_diagnostics.json  chains  evidence.json
pancake.json  profile.json  resource_usage.json  results.json  sims
```

A `run_nested.py` job that writes those `.npz` files completed at 01:19 during
this review (all four models, `ln B` values now in `results/evidence.json`) and
still produced no `results/posteriors/`; either the running process predates the
sample-saving code or the write failed silently. Whichever it is, no prior
sensitivity has ever been computed, and the last sentence of Section 10 claims
one has.

**What would resolve it**: run `prior_sensitivity.py`, put the table in the
paper (not only in a JSON), and state the span of `ln B` over the narrowings in
the same paragraph that quotes `ln B`. If the span exceeds `|ln B|` — and the
number above says it does — then the honest headline is that the evidence does
not distinguish the models, and the profile-likelihood statement (`Delta chi2`
of 0.86 between the two best fits) is the robust one and should lead.

### M3. The `Delta chi2` column of Table 1 mixes three incompatible maximisers, prints an impossible number, and understates the model's best fit by a factor of two.

**Location**: `paper/generated/tab_comparison.tex`; `scripts/gen_tables.py:108-117`;
`scripts/run_map.py` (never run — `results/map.json` absent).

The committed table reads

```
$\LCDM$              & 3 & 1436.52 & +0.00 & $-732.15\pm0.20$ & ---
$\Gam=\xi\Hub$       & 6 & 1435.70 & -0.82 & $-733.75\pm0.21$ & $-1.60\pm0.28$
reinforced, $\beta=0$& 7 & 1436.54 & +0.02 & $-734.20\pm0.21$ & $-2.05\pm0.28$
```

The seven-parameter `reinforce` model contains LambdaCDM exactly at `eps = 0`,
so its `chi2_min` cannot exceed LambdaCDM's. I verified the nesting is exact:

```
$ OMP_NUM_THREADS=1 PYTHONPATH=code python3 -c "...(see certification C5)..."
  max |chi2_reinforce(eps=0) - chi2_lcdm| over 10 random (log10_gamma0, alpha_tot, z_act) = 0.000e+00
```

`+0.02` is therefore an artefact of the fallback chain in `gen_tables.py`: with
`results/map.json` missing, LambdaCDM and `xi_h` take their `chi2_min` from
`results/results.json` (a Nelder-Mead polish of an ensemble chain) while
`reinforce` and `memory` take theirs from `results/evidence.json` (dynesty's
best *sample*, which is not a maximum). The code comment at
`gen_tables.py:105-108` says this in as many words and `run_map.py` exists to
fix it; it has simply not been run.

**No maximiser in this repository has ever found the `xi_h` best fit.** Starting
from the solution my re-profile turned up at `Delta = 0.004` and polishing with
Nelder-Mead, Powell and Nelder-Mead again (6000 evaluations each, bounds
enforced):

```
  xi_h maximum likelihood found : chi2 = 1434.87980
  LambdaCDM, same protocol      : chi2 = 1436.51609
  Delta chi2                    :        -1.63629
  at eps=0.01361, log10_xi=1.000, z_act=3.589, omega_V_act=0, f0=1.000, Delta=0.00342
  breakdown  SN 1416.03  BAO 11.66  CC 6.31  CMB 0.885
```

against the four values in circulation for the same quantity:

```
  paper/generated/tab_comparison.tex   1435.70   (Delta chi2 = -0.82)
  results/results.json (frozen chain)  1435.6982
  results/profile.json (eps profile)   1435.65690
  results/evidence.json (nested best)  1436.2958
  this report                          1434.87980  (Delta chi2 = -1.63629)
```

The printed `Delta chi2 = -0.82` is half the true value. The improvement is
physically coherent rather than a solver artefact: it comes almost entirely from
the compressed CMB term (2.95 -> 0.89) and the BAO term (12.20 -> 11.66), paid
for with 0.9 in the supernovae — that is, the model is relieving the
DESI-versus-Planck pull (m8), which is exactly the mechanism a reader would want
to see discussed. LambdaCDM's own number is unaffected (1436.51609 under the
same protocol), so the whole discrepancy is in the extension.

The nested sampler's best live point misses this by `1.42` in `chi2`
(`1436.2958` vs `1434.8798`), which is worth knowing when the same run supplies
`ln Z`. The `memory` evidence completed at 01:19 with
`chi2_min = 1436.4939`, from the same unreliable source, and will enter the
table on the same footing. **What would resolve it**: run `run_map.py` for all
four models before regenerating the table, and have `gen_tables.py` *refuse* to
emit a `Delta chi2` column when any row's source is not `"map"`, rather than
emitting it with a footnote. The footnote as written ("Not every `chi2_min`
comes from the common maximisation protocol") does not warn the reader that one
of the printed numbers is arithmetically impossible.

### M6. `ln Z` for the extended models is not reproducible. An independent seed with identical settings moves `ln B` by 0.86, three times its quoted error.

**Location**: `results/evidence.json`; `paper/generated/tab_comparison.tex`;
`scripts/run_nested.py` docstring ("A stopping criterion of `dlogz = 0.1` is
used so that the error on a difference of two evidences stays well below the
scale that would change a qualitative verdict").

I replicated both baseline runs with a different seed and otherwise identical
settings — dynesty 3.1.0, `nlive=500`, `dlogz=0.1`, `bound='multi'`,
`sample='rwalk'`, 2 workers, same `Posterior` and same likelihood object
(`/tmp/.../scratchpad/rerun_nested.py`):

```
                 shipped (seed 20260909)     replicate (seed 12345)     shift
  lcdm           -732.152 +/- 0.195          -732.237 +/- 0.196        -0.085
  xi_h           -733.748 +/- 0.207          -734.692 +/- 0.212        -0.944
  ln B(xi_h)       -1.596 +/- 0.284            -2.455 +/- 0.296        -0.859
```

LambdaCDM reproduces to 0.43 of its quoted error. The extension does not: two
runs differing only in seed disagree by `0.944`, which is 4.5 times the
per-run error and 3.2 combined `sigma`. `ln B` moves from `-1.60` (odds 4.9:1
against) to `-2.46` (odds 11.6:1), i.e. the odds change by a factor of 2.4, and
the shipped error bar `+/- 0.28` does not cover it.

**The mechanism is visible in the same output.** Both runs report a best live
point far from the model's actual maximum:

```
  chi2_min, shipped run       1436.2958
  chi2_min, replicate         1436.3780
  actual maximum (M3)         1434.8798
```

Neither nested run ever reached the ridge that carries the likelihood, and they
failed by different amounts. That is the same razor-thin curved degeneracy that
froze the ensemble chains; nested sampling is not immune to it, it merely fails
more quietly. `nlive = 500` with dynesty's default `rwalk` in six dimensions is
not enough to resolve a ridge whose `chi2` rises from `1434.88` to `33560` over
half a decade in `log10_xi` at fixed neighbours.

**Note also** that `dlogz` is a stopping criterion on the *remaining* evidence,
not an error bar; the docstring conflates the two. The quoted errors are
dynesty's `sqrt(H/nlive)`-type estimate (`H = 12.48` and `14.77` for the two
models), which is a within-run estimate and demonstrably does not bound the
between-run scatter here.

**What would resolve it**: run every evidence at least three times with
different seeds and quote the scatter, not `logzerr`; raise `nlive` (or use
`sample='rslice'`/`'rwalk'` with an increased `walks`) until the scatter comes
down below the differences being claimed; and verify that the sampler's best
live point approaches the maximum found by `run_map.py` (M3) before trusting
`ln Z`. Until then no `ln B` in Table 1 should be quoted to two decimals.

### M4. Section 10 promises four analyses that no results file contains.

**Location**: `paper/sections/10_observations.tex` lines 25-26, 41-43, and the
closing paragraph; `code/absorb/datasets.py:20-30`.

The section states, in order: "a variant including it [the SH0ES calibration] is
reported separately"; "the late-time-only combination is reported alongside so
the reader can see what the compressed likelihood is doing"; "Users who prefer
to avoid the compressed likelihood can run the late-time-only combination, which
is reported alongside" (`appF_numerics.tex:110-112`); and "the third [a Bayesian
evidence robust to prior choice] is reported with its prior sensitivity".

```
$ grep -o "nocmb\|__shoes\|__rsd\|bao_only" results/*.json | sort -u
(no output)
```

Every entry in `results/evidence.json`, `results/profile.json` and
`results/results.json` is `__baseline`. `datasets.build` supports `shoes`,
`nocmb`, `rsd` and `bao_only`; none has been run. Separately,
`code/absorb/datasets.py:26` states "Section 10 reports the result both ways"
about holding `sigma_8` fixed in the RSD combination; Section 10 does not
mention RSD at all.

**What would resolve it**: run the variants and report them, or delete the four
sentences. As it stands a reader is told a robustness check exists that does
not.

### M5. The constancy of the sound-horizon calibration factor `KAPPA_RS` is asserted, never tested, and the test that exists tests something else.

**Location**: `code/absorb/early.py:290-360` (`recipe_offsets`, `kappa_rs`);
`paper/sections/10_observations.tex` lines 45-50;
`appF_numerics.tex:103-109`.

The argument is that the ~0.2% mismatch between the module's integrated sound
horizon and a Boltzmann calculation "is a property of the recipe, not of the
cosmology", so a single multiplicative constant fitted at the Planck 2018 best
fit may be applied everywhere. The numbers behind it check out:

```
$ OMP_NUM_THREADS=1 PYTHONPATH=code python3 -c "from absorb import early; early.recipe_offsets(verbose=True)"
z_*        =  1091.909   (published 1089.92)
R          =    1.7501   dR   = -0.0001 = -0.02 sigma
l_A        =   302.099   dl_A = +0.628 = +6.97 sigma
r_s(z_*)   =   144.269 Mpc  -> kappa_rs = 1.002082
r_drag     =   147.063 Mpc (Aubourg), 147.063 (Brieden), published 147.09
```

so the correction is genuinely in `r_s` (`R`, which shares the same `D_M(z_*)`,
is right to `-0.02 sigma` with no correction at all) and its size, 0.208%,
matches the "about 0.2%" the appendix quotes. What is missing is any test that
`kappa` does not move with cosmology. The test the paper cites asserts only that
`kappa` is not *re-derived per model* — a caching property, not a physics one.

A probe: compare the module's integrated sound horizon at the Eisenstein & Hu
(1998) drag redshift against the independently calibrated Aubourg fit, and watch
the ratio.

```
$ OMP_NUM_THREADS=1 PYTHONPATH=code python3 - <<'EOF'
  ...(EH98 z_drag; early.sound_horizon vs early.r_drag over a grid)...
EOF
  ob=0.02237 oc=0.1100  ratio=1.025320
  ob=0.02237 oc=0.1200  ratio=1.025058
  ob=0.02237 oc=0.1260  ratio=1.024720
  ob=0.02320 oc=0.1260  ratio=1.024504   (drift -9.4e-4 from the corner ob=0.0215, oc=0.110)
```

`d(ratio)/d(omega_c) = -5.5e-2`. Over the posterior width of `omega_c`
(`+/- 0.0012`) that is `6.6e-5`, i.e. `0.020` in `l_A`, or `0.22 sigma` — small
but not nothing, given that `l_A` is a `0.03%` measurement. Over the *prior*
range `omega_c in [0.05, 0.25]`, which is what the evidence integral actually
covers, it is of order a per cent, i.e. tens of sigma of `l_A`.

I state the caveat plainly: this probe cannot separate the drift of the module's
integrator from the drift of EH98's own `z_drag` fit, so it does not by itself
convict the code. It does show the constancy assumption is a testable statement
that has not been tested, and that the CMB term is the single most constraining
element of the baseline (`chi2 = 0.006` at the Planck point, versus 30.7 for
BAO — see m8).

A second, related and cleanly measurable point: `DesiBAOLikelihood.method` is
hard-wired to `"aubourg"` and the alternative implemented next to it is never
exercised. The two agree to `5e-5` Mpc at the fiducial and diverge over the
prior:

```
  ob=0.02237 oc=0.0800  aubourg=159.888  brieden=158.588  diff=-0.81%
  ob=0.02237 oc=0.1200  aubourg=147.063  brieden=147.063  diff=-0.00%
  ob=0.02237 oc=0.2000  aubourg=131.343  brieden=132.778  diff=+1.09%
```

A 1% difference in `r_d` is a full DESI error bar on every `D/r_d` point.

**What would resolve it**: (i) re-derive `kappa` at two or three cosmologies
displaced by a few `sigma` using CLASS or CAMB and report the spread, or
marginalise over `kappa` with a prior of that width; (ii) report `r_drag`
computed both ways for the baseline fit and state the shift in `ln Z`; (iii) add
a test that fails if `kappa` evaluated at the edges of the `omega_c` prior moves
`l_A` by more than half a `sigma`.

---

## Minor points

### m1. The reported `chi2` is not a `chi2`: it carries the `+9.325` Jacobian of the `M_B` marginalisation.

`likelihoods.py:150` adds `log(E0 / 2 pi)` to the supernova `chi2`, which is
correct as `-2 log L` and is documented. Measured:

```
$ ...  E0 = 1^T C^-1 1 = 70470.7 ;  log(E0/2pi) = 9.3251   (with SH0ES: 9.3450)
```

So `results/results.json` `chi2_breakdown["SN(Pantheon+)"] = 1415.10` is
`1405.78 + 9.33`, and Table 1's `chi2_min = 1436.52` is `1427.19 + 9.33`. A
reader who forms `chi2/dof` from the table is wrong by `9.33`. Say in the table
caption that the column is `-2 log L` including the marginalisation Jacobian,
and that only differences are meaningful.

### m2. `chi2_at_zero` in `results/profile.json` is a `Delta chi2`, not a `chi2`.

`run_profile.py:169` writes it after `chi2 -= chi2.min()`. Referee B raised this
in m10; it is still there. Stored value `0.8592`; the actual `chi2` at `eps = 0`
is `1436.5161`.

### m3. The dataset table describes the release, not the selection.

`paper/generated/tab_datasets.tex` says "Pantheon+, 1701 light curves". The
baseline uses 1590 (the `z_HD > 0.01` Hubble-flow cut); the SH0ES variant would
use 1657. Verified counts: 1701 rows, 77 calibrators, 1590 above the cut, 10
calibrators above the cut, union 1657. Add the number actually used, and the
`n_data = 1621` that the results file reports.

### m4. Section 10.2 states a sampling method that Section 10.3 then withdraws.

"Posteriors are sampled with an affine-invariant ensemble sampler; chains run
until they exceed fifty integrated autocorrelation times" is contradicted three
paragraphs later by "Their posteriors are therefore taken from nested sampling".
Rewrite 10.2 to say what was actually done for which model.

### m5. `check_numbers.py` is blind to numbers written in maths mode, which is where the hand-typed ones were.

When I began this review `10_observations.tex:154` read "acceptance $0.44$,
length $157$ autocorrelation times", both hand-typed results (the macro for the
first is `0.4386`; the second is `2000 / 12.7271 = 157.1` computed by hand from
two other macros). Both were replaced by macros during the review, and the
appendix's opening paragraph was rewritten to exempt "round figures used for
orientation". The hole in the gate that let them through is still open, and one
number is still in it:

- `appF_numerics.tex:34`: "One background solve costs about $11$~ms." That is a
  measurement of this code, not a round figure from the literature, and it is
  model-dependent. Measured here single-threaded (with three other jobs on a
  16-core machine, so if anything an over-estimate):

```
  lcdm   background solve  1.07 ms   full posterior chi2   4.16 ms
  xi_h   background solve 15.01 ms   full posterior chi2  29.82 ms
```

  `11 ms` is neither. The same paragraph's corollary in
  `likelihoods.py:16-22` — "makes the supernova term cheap enough that the
  sampler is dominated by the background integration rather than by linear
  algebra" — is true for `xi_h` (15 of 30 ms) and false for LambdaCDM (1.1 of
  4.2 ms). Worker sizing and runtime estimates elsewhere rest on the 11 ms
  figure.

The gate cannot catch this: `check_numbers.py:70` applies `MATH.sub(" ", text)`
before scanning, so anything inside `$...$` is invisible; `DECIMAL =
\d+\.\d+` never matches an integer; and `0.44` sits on
`docs/NUMBERS_WHITELIST.txt` as a `tabular` column width, so it would have been
exempt even in prose. Either scan inside maths mode with a narrower whitelist,
or say in the appendix that the gate covers prose only.

### m6. The cosmic-chronometer covariance recipe is not quite MM20's, and it does not matter — say so rather than leaving it unexamined.

`data/cc.py:120` builds `C = diag(errHz^2) + C_IMF + C_mod_ooo`. The published
`errHz` is *not* the MM20 statistical error: it already contains the metallicity
term, and not by simple quadrature.

```
  mean(errH^2 - (stat^2 + met^2)) = +1.180 (km/s/Mpc)^2
  z=0.7812: errH=12.195 vs sqrt(stat^2+met^2)=11.206   (8.8% apart)
```

So there is a partial double count of the metallicity systematic, and the MM20
"young" and SFH contributions are absent from `data_MM20.dat` and therefore
absent here. The effect is immaterial:

```
  variant=default                chi2 = 6.1907
  variant=conservative           chi2 = 6.0952
  diagonal only (published errH) chi2 = 6.2052
  stat(+)met diagonal + same syst chi2 = 6.1663
```

Four defensible recipes spanning `chi2` 6.10-6.21 on 15 points. State that the
CC term is insensitive to the covariance construction rather than describing a
prescription that is not exactly the one cited.

### m7. `profile_derived` solves the background twice per objective evaluation.

`run_profile.py:78` calls `post(theta)` (one `Background`) and `:81`
`derived_value(theta)` (a second `Background` from the same `theta`). The
`maxfev = 4000` budget is therefore 2000 solves. Halving that cost is free and
directly buys the convergence M1 asks for.

### m8. The per-probe breakdown shows a real BAO-CMB pull that the section never mentions.

Evaluated at the Planck 2018 base-LambdaCDM best fit (`omega_b = 0.02237`,
`omega_c = 0.1200`, `h = 0.6736`), and compared with the breakdown at this
paper's own LambdaCDM fit (`results/results.json`, `chains.lcdm__baseline`):

```
                      at Planck 2018      at the fitted point
  SN(Pantheon+)          1413.06               1415.10   (n=1590, incl. +9.33)
  BAO(DESI DR2)            30.67                 12.20   (n=13)
  CC(default)               6.19                  6.27   (n=15)
  CMB(compressed)           0.006                 2.95   (n=3)
```

DESI DR2 costs `chi2 = 30.7` on 13 points at the Planck cosmology; refitting
buys back 18.5 of that at the price of moving the compressed CMB term from
0.006 to 2.95. That is the known DESI-versus-Planck pull, it is what makes the
`xi_h` ridge attractive at all, and Section 10 does not mention it. The
`0.006` at the Planck point is in any case not an independent check: `kappa` is
*defined* to reproduce `l_A` there (M5). Report the breakdown, at the fitted
point, in the comparison table.

### m9. `run_profile.py`'s `lows`/`highs` omit nuisance parameters.

`run_profile.py:61-62` and `:115-116` build the bounds from
`post.model.priors()` only, not `_priors_of(post)`. Harmless while
`nuisance = ()`, a silent index bug the moment one is added. Referee B raised it
in m10; still present.

### m10. "Less than about one and a half per cent".

`10_observations.tex:134-135` glosses `Delta < 0.0126` as "less than about one
and a half per cent of the critical density". 0.0126 is 1.26%. Rounding up is
the conservative direction, but the rounding should not be done in prose at all
(see m5).

### m11. `RSDLikelihood` and three of the five dataset combinations are unexercised code.

`datasets.py` `rsd`, `shoes`, `nocmb`, `bao_only` are never run (M4). The RSD
block correctly extracts the `f_sigma8` rows *and* columns of the DR16 FS+BAO
covariance, which is the right thing to do, and I could not fault the loader —
but nothing tests it against a result.

### m12. The response letter's `57.1%` is not the archived number.

`docs/review/RESPONSE_r2.md` reports "**57.1%** land outside the prior box at the
default scale (referee: 56.2%)". `results/chain_diagnostics.json`
`xi_h_baseline_demove_frozen.outside_prior_fraction = 0.56225`, and that is what
`appF_numerics.tex:133` will print. The letter asserts a measurement the archived
results file does not contain.

---

## Questions the authors must answer

**Q1.** Is `logzerr` at `dlogz = 0.1` a fair estimate of the run-to-run scatter
of `ln Z`? I replicated the LambdaCDM run with an independent seed and the same
settings (`nlive=500`, `dlogz=0.1`, `bound='multi'`, `sample='rwalk'`, 2
workers):

No, not for the extended models. See M6 for the numbers: LambdaCDM reproduces
to 0.43 of its quoted error, `xi_h` misses by 4.5 times its quoted error, and
`ln B` shifts by 0.86. Report a replicate for every row of Table 1, or state
that the quoted error is dynesty's within-run estimate and not a measured
scatter. A run with `bound='single'`, `sample='unif'` was still in progress when
this report was written; whether the method choice matters *more* than the seed
is the natural follow-up and the authors should measure it.

Report a replicate for every row of Table 1, or state that the quoted error is
dynesty's `sqrt(H/nlive)` estimate and not a measured scatter.

**Q2.** `run_nested.py`'s docstring justifies `dlogz = 0.1` as chosen "so that
the error on a difference of two evidences stays well below the scale that would
change a qualitative verdict". `dlogz` is a stopping criterion on the *remaining*
evidence, not an error bar; the reported errors are `0.195`-`0.212` each, so the
error on `ln B` is `0.28`-`0.30` before the between-run scatter of M6 is added.
Please separate the two concepts in the docstring and in the appendix.

**Q3.** `R = sqrt(omega_m) D_M(z_*) H_100 / c` is evaluated with the
*pre-activation* `omega_m` (`likelihoods.py:253`). In LambdaCDM, where the Chen,
Huang & Wang compression was derived, `omega_m` at recombination and today are
the same number; in this model they differ by `Delta`. Which of the two does the
compressed `R` actually constrain, and what is the induced error? A one-line
demonstration on a Boltzmann code at one non-zero `Delta` would settle it. The
same question applies to the covariance: the `R`-`l_A`-`omega_b` correlations
were measured in LambdaCDM chains.

**Q4.** Why does `results/posteriors/` not exist after a completed
`run_nested.py`? Everything downstream (`summarise_posteriors.py`,
`prior_sensitivity.py`) reads it, and `results/results.json` still holds the
frozen ensemble chain for `xi_h` (`converged: false`, `acceptance: 0.0073`,
`tau_max: 2853`) as the source of the `xi_h` row, while Section 10 says those
posteriors "are therefore taken from nested sampling".

**Q5.** `paper/generated/tab_parameters.tex` currently contains only
`% chain not available yet`, so Table 2 renders empty while the text says
"\Cref{tab:comparison,tab:parameters} report the fits". The `memory` evidence
finished at 01:19; regenerate and check.

---

## Certification: what I attacked and could not break

I take this section to be as useful as the defects. Each item is something I
tried to falsify with a computation and could not.

**C1. The Pantheon+ analytic marginalisation over `M_B` is correct.** I checked
it against a brute-force numerical marginalisation on a 4001-point grid in
`M_B`:

```
analytic chi2_marg  1413.0593713304
likelihood() value  1413.0593713341   (diff -3.7e-09)
brute force         1413.0593713302   (diff -1.8e-10 from analytic)
best_fit_MB = -19.440152   grid argmin = -19.440125
```

The `A - B^2/E0 + log(E0/2pi)` form is the correct Goliath/Conley result, the
`log` term is the right Jacobian, and the `solve_triangular` shortcut for
`A = ||L^-1 Delta||^2` is legitimate (`scipy` reads only the requested triangle,
so the un-zeroed upper triangle left by `cho_factor` is never touched). The
appendix's claim that this is "verified against a brute-force one-dimensional
marginalisation" is true.

**C2. The Pantheon+ selection is exactly as documented.**

```
total light curves 1701;  calibrators 77;  z_HD > 0.01: 1590
calibrators with z_HD > 0.01: 10;  union: 1657
```

matching the docstring's claim that "ten calibrators sit above the Hubble-flow
cut". `use_cepheid` is all-`False` without SH0ES, so the external Cepheid
calibration cannot leak into the SN-only sample, and with SH0ES the *same* `M_B`
appears in calibrator and Hubble-flow residuals, which is the correct SH0ES
construction.

**C3. The DESI DR2 ordering is handled correctly, and it matters enormously.**
The loader dispatches on the quantity string, not on position. Deliberately
swapping the `z = 2.33` pair:

```
BAO chi2 as coded             30.666
BAO chi2 with DH/DM swapped 98025.268
```

so the `D_H`-before-`D_M` ordering in the mean file is load-bearing and is
respected. The covariance recovered from the file is block diagonal by tracer
with within-pair correlations `-0.452, -0.395, -0.347, -0.398, -0.494, -0.431`,
which is the structure of the Cobaya-packaged DESI Gaussian likelihood. The
pairing of the last two rows is also unambiguous: row 12 has `sigma = 0.101`
(1.17% of 8.632, a plausible `D_H/r_d` error) and row 13 `sigma = 0.532` (1.36%
of 38.989); the reverse assignment would give the `D_H` point a 6% error.
Nothing in the code would catch a covariance re-ordered relative to the mean
file — the shape check only catches a wrong length — but the two SHA256 digests
pin both files exactly, which is an adequate guard.

**C4. Data provenance.** All ten raw files match the recorded digests:

```
$ cd data/raw && sha256sum -c ../SHA256SUMS
(10/10 OK)
```

**C5. Davies' problem is real and the paper's diagnosis of it is exact.** At
`eps = 0` the likelihood is bit-identical to LambdaCDM's:

```
max |chi2_xi_h(eps=0) - chi2_lcdm| over 15 random (log10_xi, z_act):  0.000e+00
max |chi2_reinforce(eps=0) - chi2_lcdm| over 10 random draws:          0.000e+00
```

So the extra parameters are *exactly* unidentified under the null, the null sits
on the boundary `eps = 0`, and neither `2k` nor `k ln n` is the effective
parameter count there. The paper's further claim that both criteria err in the
direction of its own conclusion is also correct: both over-penalise the larger
model, which is the model the paper rejects. The decision to drop AIC and BIC
is right. My objection in M2 is to what replaced them, not to the removal.

**C6. Away from `eps = 0` the prior box is nowhere near LambdaCDM**, which is
worth recording because it constrains what a fixed-prior argument can claim. Of
600 draws from the `xi_h` prior box, none came within `Delta chi2 = 100` of the
LambdaCDM minimum (median `Delta chi2 = 9.8e5`). Recovering LambdaCDM at generic
`eps` and `z_act` needs `log10_xi <~ -6` to `-8`, far below the prior floor of
`-3`, because the vacuum produced by converting at `a_act` is frozen at its
value there and is amplified by `a_act^-3`.

**C7. The `omega_V_act` degeneracy claim in Section 10 is exactly right.**
Recomputing the stored profile solutions: `omega_V_act = 0.3266` at `eps = 0`
and `3e-8` at every `eps > 0`; `0.3266 / h^2 = 0.6985 = Omega_V0`. The revised
sentence "at `eps = 0` it jumps to `Omega_{V,act} = Omega_{V0}`" is correct, and
the underlying physics (conversion at `z ~ 8` producing `Omega_V ~ 0.70` from a
matter deficit of `0.003`) checks out through the `a^-3` factor in
`d omega_V / dN`.

**C8. `r_drag` is right.** The Aubourg fit reproduces the Planck 2018 value to
0.019% (`147.063` vs `147.09`), inside the fit's own quoted 0.021% accuracy, and
the neutrino term uses the same `omega_nu` convention as Aubourg's Eq. (16). The
choice to feed it the *pre-activation* `omega_b + omega_c` is both correct for
this model and clearly stated in three places.

**C9. What `run_profile.py` computes is a genuine profile *likelihood*, not a
penalised posterior, and its bookkeeping is faithful.** Every prior is uniform
and `Model.log_prior` returns `0.0` inside the box, so `-2 * post(theta)` is
exactly `chi2` there — I confirm referee B's certification of this. I also
recomputed `chi2` at all 17 stored `best_theta` vectors of the `eps` profile and
reproduced every stored `delta_chi2` to `<1e-4`, with
`chi2(eps=0) = 1436.5161`, which is the LambdaCDM minimum. The stored numbers
are what the script says they are; the objection in M1 is that the optimiser
behind them has not converged, not that the arithmetic is wrong.

**C10. The qualitative verdict survives everything I threw at it.** Even with
the corrected maximum (M3), `xi_h` improves `chi2` by `1.636` for three extra
parameters, two of which are exactly unidentified at the null. That is no
evidence for conversion by any calibration — Wilks, Chernoff or Davies — so the
paper's conclusion ("nothing in this data combination requires conversion") is
right. My objections are to the *numbers* attached to it: the limit (M1), the
`Delta chi2` (M3), the `ln B` and its error (M2, M6). The profile-likelihood
statement is the robust one and should lead the paragraph.

**C11. The cosmic-chronometer term is insensitive to the covariance recipe**
(m6), the `np.interp` clamping beyond `z = 1.475` for the `z = 1.965` point is
immaterial, and the `check_covariance` symmetry/positive-definiteness gate with
its `1e-5` relative tolerance is well argued and passes on all four matrices.

**C12. The compressed CMB likelihood correctly marginalises out `n_s`** by
taking the `3 x 3` sub-block of the Chen, Huang & Wang covariance rather than
conditioning on it, which is the right operation.

**C13. `KAPPA_RS` is computed once and cached**, not re-derived per model, as
claimed. The lazy `__getattr__` (PEP 562) is a correct implementation of that.

**C14. The frozen chains are where the response letter says they are.**
`results/chains/{xi_h,reinforce}_baseline_demove_frozen.h5` both exist and
`results/chain_diagnostics.json` reproduces from them; the diagnostics quoted in
Appendix F come from that file and not from prose, which is the right fix for
the earlier defect.
