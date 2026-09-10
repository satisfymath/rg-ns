# Referee report

**Manuscript**: Self-reinforced geometric absorption
**Referee**: B (computational cosmologist / statistician)
**Round**: 2
**Date**: 2026-09-10

> Scope: the new numerical and statistical material only — `code/absorb/pancake.py`,
> `code/absorb/collapse.py`, `code/absorb/resources.py`, `code/absorb/sampling.py`,
> `scripts/run_pancake.py`, `scripts/run_profile.py`, `scripts/check_chain_stability.py`,
> `results/resource_usage.json`, `results/pancake.json`, `results/profile.json`,
> the three chains in `results/chains/`, and the new
> `sec:defects-caustics` / `rem:hazard-time-change`.
>
> Several files changed while this review was being written (`run_pancake.py`
> at 00:04:23, `run_profile.py` and `results/profile.json` at ~00:06,
> `collapse.py` and `test_collapse.py` later still). Where a point was
> overtaken by an edit I say so. Every number below was measured by me, on
> this machine, single-threaded; commands are quoted so the authors can
> repeat them.

## Summary (3 lines)

The paper adds a caustic analysis: a bounded conversion rate provably cannot
regularize a Zel'dovich caustic, only a compression-driven rate with
`kappa > 1` and zero branching can, and a 1D Lagrangian pancake is offered as
numerical confirmation. It also trades the bounded-rate hypothesis of the
deterministic-limit theorem for a hazard-time change, and offers a profile
likelihood in `eps` as a remedy for a badly-mixed MCMC. The analytic
caustic results and the binomial law are correct and I could verify them
independently; the MCMC, the model comparison built on it, and the profile
likelihood offered to repair it are not usable as they stand.

## Recommendation

[ ] Accept  [ ] Minor revision  [x] Major revision  [ ] Reject

The analytic core of `sec:defects-caustics` survived every check I threw at it,
and I say so explicitly below. The statistics did not.

---

## Major points

### M1. The `xi_h` chain is frozen, not slowly mixing. Nothing derived from it is trustworthy, and running it longer will make it worse.

**Location**: `code/absorb/sampling.py:283-295` (initialisation and moves);
`results/chains/xi_h_baseline.h5`; `results/results.json → chains/xi_h__baseline`.

**What I measured.** From the stored backend (`iteration = 72580`, 32 walkers,
`ndim = 6`):

- cumulative acceptance **0.00733** (not 0.01): `accepted` per walker ranges
  341–705, mean **532.2 accepted moves per walker in 72580 steps**;
- move rate (fraction of steps at which a walker's `log_prob` changed)
  **0.01498 over the first 10 000 steps, 0.00581 over the last 10 000**. The
  chain is *decelerating*, not equilibrating;
- `tau_max = 2853`, so the chain is 25.4 tau long against the code's own
  `N_TAU = 50` criterion; `converged = False`;
- **zero** non-finite entries in the stored `log_prob` (72580 x 32), and **no**
  stored sample outside the prior box in any of the six parameters.

So the two hypotheses in the brief are both **false**: walkers are not stuck
outside the prior, and resumption did not feed a degenerate state (the backend
stores `random_state_0 = 'MT19937'` with the full 624-word state, and emcee
restores it on resume).

**The actual cause.** I reconstructed real `DEMove` proposals from the stored
final ensemble and evaluated the true posterior. At emcee's default
`gamma0 = 2.38/sqrt(2*6) = 0.687`:

| gamma | acceptance | -inf fraction | median Δlog p |
|---|---|---|---|
| **0.687 (default)** | **0.000** | **0.510** | **-2193** |
| 0.300 | 0.052 | 0.323 | -568 |
| 0.100 | 0.094 | 0.219 | -60.2 |
| 0.030 | 0.167 | 0.062 | -6.63 |
| 0.010 | 0.417 | 0.083 | -0.99 |

Splitting the rejections at the default scale (n = 128 proposals):

- **56.2 % fall outside the prior box** → rejected with probability 1;
- **0.0 %** fail for physics reasons (no likelihood exception ever fires);
- 43.8 % are inside the box, and **none** of them was accepted.

Two geometric facts explain this, both measured from the chain:

1. **Three of six parameters have posterior widths comparable to their prior
   widths.** Over the last two thirds of the chain, `eps` has
   5th/50th/95th percentiles **0.0064 / 0.2976 / 0.8837** on a `[0, 1]` prior;
   `z_act` **1.04 / 7.39 / 23.66** on `[0.3, 30]`; `log10_xi`
   **-2.93 / -2.31 / -0.71** on `[-3, 1]`. A DE difference vector scaled by
   0.687 therefore leaves the box more often than not. `DEMove` has no boundary
   handling.
2. **The remaining direction is a razor-thin curved ridge.** Taking the
   profile's own best-fit nuisance vector at `eps = 0.05` and transplanting it
   to `eps = 0.00` raises chi2 from 1436.52 to **167 000**; from `eps = 0.10`
   to `eps = 0.05`, to **24 821**. Moving `eps` by 0.05 off the ridge costs
   Δchi2 ~ 1e5, i.e. the ridge has an aspect ratio of order 1e3 in the `eps`
   direction. Affine invariance buys nothing here: it linearises a *curved*
   degeneracy, and a linear difference vector lands off the ridge, where the
   penalty is exactly the ~4400 in Δchi2 (median Δlog p -2193) measured above.

This is a runaway, which is why the move rate halves over the run: as the
ensemble spreads to fill the box, DE steps grow, so acceptance falls, so the
ensemble spreads only along the widest direction. **Sampling longer makes it
worse.**

**Is 1 % consistent with a funnel at `eps -> 0`?** Partly, but the stated cause
is not the measured cause. `run_profile.py`'s docstring attributes the poor
mixing to a funnel at `eps -> 0`. The dominant single mechanism is
prior-boundary rejection (56 %), which has nothing to do with the funnel.

**Which quantities from that chain are trustworthy? None.** Not the medians,
not the 95th percentiles quoted as upper limits, not `tau` (estimated from a
chain 25 tau long, where emcee's own estimator is documented as unreliable),
not `chi2_min` (see M2). The `reinforce` chain has the same pathology:
acceptance **0.00984** over 15 501 steps.

**Fix.** (a) Sample in an unbounded reparametrisation — map each uniform prior
through a logit so no proposal can leave the box; this alone removes 56 % of
the rejections. (b) The codebase already implements
`Posterior.prior_transform` for nested sampling and never uses it: a nested
sampler handles a bounded curved ridge far better than an affine-invariant
ensemble. (c) Report acceptance and `tau` over the **last 10 %** of each chain,
not cumulatively — the cumulative 0.73 % is flattered by the early transient.

---

### M2. The `chi2_min` / AIC / BIC comparison is not fair between models, and the AIC/BIC penalties are the wrong ones for this nesting.

**Location**: `scripts/run_mcmc.py:127-137`; `code/absorb/sampling.py:207-210`;
`results/results.json`.

**Unequal optimisation.** `chi2_min` is not the chain's best sample: it is a
`find_map` Nelder-Mead polish of it, with a fixed `maxfev = 2*900 = 1800`.
Measured:

| model | -2 max log p from chain | reported `chi2_min` | polish gained | ndim |
|---|---|---|---|---|
| `lcdm` | 1436.5192 | 1436.5161 | 0.0031 | 3 |
| `xi_h` | 1435.8239 | 1435.6982 | **0.1257** | 6 |
| `reinforce` | 1436.4672 | — | — | 7 |

The same 1800-evaluation budget is spent in 3 dimensions for LambdaCDM and in 6
for `xi_h`. The larger model, whose chain is the badly-mixed one, needs the
polish forty times more and gets no more budget. The `lcdm` chain, by contrast,
is genuinely healthy — 2000 steps, acceptance **0.4386**, `tau_max = 12.7`,
`converged = True`. **A 2000-step well-mixed chain is being compared against a
72 580-step frozen one, and whichever explored better wins.**

**The residual optimiser error is measurable.** The profile-likelihood run
maximises the same `xi_h` likelihood at `eps = 0` and reports Δchi2(0) =
**0.8420**; `results.json` implies 1436.5161 - 1435.6982 = **0.8179**. Two
independent maximisations of the same function disagree by **0.024** in Δchi2.
That is the numerical noise floor on the whole model comparison.

**The penalties are invalid in kind.** I verified the nesting directly: at
`eps = 0`, `xi_h`'s chi2 is **bit-identical** to LambdaCDM's for every
`(log10_xi, z_act)` I tried — 12 combinations spanning `log10_xi` in
`{-3, -1, 0, 1}` and `z_act` in `{0.3, 5, 30}`, all giving a difference of
**exactly 0.000e+00** against `chi2_lcdm = 1436.5192003515585`. The nesting is
therefore exact (good — see the certification section), but it means that under
the null **two of the six parameters are entirely unidentified**. This is
Davies' problem (nuisance parameters present only under the alternative), not a
regular nested comparison and not Chernoff's boundary case. Consequently:

- the reference distribution of Δchi2 is neither chi2_3 nor the 50:50 boundary
  mixture, but the supremum of a chi-square random field over the unidentified
  `(log10_xi, z_act)` plane, whose 95th percentile is materially larger;
- AIC's `2k` and BIC's `k ln n` with `k = 6` **over-penalise** `xi_h`, because
  the effective parameter count at the LambdaCDM point is 4, not 6.

Both errors — the under-optimised `chi2_min` and the over-counted `k` — push in
the **same** direction, inflating the paper's preference for LambdaCDM. The
conclusion may well be right; the quoted margin (ΔAIC = 5.18, ΔBIC = 21.35) is
not defensible.

**Fix.** One optimisation protocol for every model, with a per-dimension
evaluation budget, reported alongside its own convergence check. State the
Davies problem explicitly. Either calibrate the likelihood-ratio statistic by
simulation under the null, or drop AIC/BIC in favour of a statement that does
not require a parameter count.

---

### M3. `profile()` reports a "95 % upper limit on eps" that is nothing but the right-hand end of the grid.

**Location**: `scripts/run_profile.py:148-152` (and the same construction at
`:98-101` in `profile_derived`); `results/profile.json`.

`results/profile.json`, written at 00:06:

```
eps    : 0.00   0.05   0.10   0.15   0.20   0.25   0.30   0.35   0.40   0.45   0.50   0.55   0.60
Δchi2  : 0.842  0.000  0.028  0.039  0.058  0.074  0.050  0.050  0.051  0.052  0.052  0.053  0.054
eps_limit_95 = 0.6
```

Above `eps = 0` the profile never exceeds **0.0744** and never approaches 2.71.
`above` is therefore empty and the code executes `limit = float(grid[-1])` =
**0.6**, which is stored in a field named `eps_limit_95` and printed by `main()`
as "95 % upper limit on eps: 0.6000". Change `np.linspace(0.0, 0.6, ...)` to
run to 1.0 and the "limit" becomes 1.0. **The number is an artefact of the grid
presented as a constraint** — the single most embarrassing kind of silent
failure, because the output is plausible.

The authors' own new docstring (`:44-49`) already states the reason: `eps` is
the convertible fraction, the optimiser can always send the rate to zero and
recover LambdaCDM at no cost, so "the likelihood is therefore flat in eps by
construction, which is a statement about the parametrisation and not about the
data". `profile_derived`, added at the same time, handles this correctly —
`limit_95 = NaN` plus an explicit `"unbounded": true` flag. `profile()` was not
given the same treatment and is still what `main()` runs by default.

**Fix.** Make `profile()` return NaN with an `unbounded` flag, exactly as
`profile_derived` does, or delete it. Never fall back to a grid endpoint.

---

### M4. The new subsection quotes seven numbers through LaTeX macros that do not exist, from a results file no script reads, one of which has never been computed.

**Location**: `paper/sections/11_defects.tex`, "Numerical test" paragraph:
`\numPancakeControlExponent`, `\numPancakeBoundedExponent`,
`\numPancakeBoundedSuppression`, `\numPancakeKappaHalfExponent`,
`\numPancakeKappaOnepointfiveExponent`, `\numPancakeKappaThreeExponent`,
`\numPancakeDustResidual`.

- `grep -rn numPancake paper/ build/ scripts/` finds these strings **only in
  `11_defects.tex`**. None is defined anywhere. The document as committed
  cannot compile them.
- `scripts/gen_numbers.py` reads **only** `results/results.json`.
  `results/pancake.json` is read by **no script in the repository**:
  `grep -rn pancake scripts/gen_numbers.py scripts/check_numbers.py
  scripts/gen_tables.py scripts/check_claims.py Makefile` returns nothing.
- The names do not follow the generator's own convention either. `camel()`
  would produce `numPancakeANoneExpRhoINear`, not `numPancakeControlExponent`,
  so these are hand-invented placeholders.
- `\numPancakeDustResidual` refers to `dust_residual`, which **does not exist
  in `results/pancake.json`**. That file was written at 00:02:56 and still
  contains the superseded `mass_residual`; `run_pancake.py` was changed at
  00:04:23 to emit `survival_residual` / `defect_residual` / `dust_residual`
  and **has not been re-run**. The number the paragraph wants to quote has
  never been computed.

This breaks the project's own stated invariant — `gen_numbers.py`'s docstring:
"No number in the manuscript is typed by hand: every quoted value is a
`\newcommand` generated here from the JSON that the analysis scripts write." And
`check_numbers.py` cannot catch it, because it only regenerates from
`results.json`.

**Fix.** Re-run the pancake suite; teach `gen_numbers.py` to ingest
`results/pancake.json`; name the macros by the generator's convention; add
`pancake.json` to `check_numbers.py`'s comparison so this class of drift fails
the build.

---

### M5. `check_chain_stability.py` passes the frozen chain, and has no power to fail it.

**Location**: `scripts/check_chain_stability.py:75-86`.

Run against the real `xi_h` chain, the gate's own arithmetic:

- burn-in is `series.shape[0] // 3` = 605 thinned rows = **24 200 raw steps =
  8.5 tau**. It is a fixed one third and **ignores `tau` entirely**; a
  tau-based burn would be `3*tau = 8559`;
- split-half drift of the 95th percentile: `eps` **0.9 %**, `omega_V_act`
  **0.0 %**, against `TOL = 25 %`. **The gate passes.**

Meanwhile the same chain has acceptance 0.0073, `converged = False`, a move
rate that has halved over the run, and a median `eps` that wanders across eight
consecutive blocks:

```
block    0      1      2      3      4      5      6      7
median 0.394  0.318  0.273  0.246  0.303  0.346  0.274  0.323
```

The gate is blind to all of it. It cannot fail, because the statistics it
watches are the *least* sensitive ones available: `eps`'s 95th percentile sits
at ~0.88 pinned against a hard prior edge at 1.0, so it cannot drift much no
matter how badly the chain mixes. A 25 % tolerance on a percentile is also
enormous for a number quoted in the abstract as an upper limit.

Two silent passes in the same block: `if post.size < 200: continue` skips the
check with no message and no failure; and
`post = post[np.isfinite(post).all(axis=1)]` discards an entire time slice if
any **one** of the 32 walkers has a non-finite derived value.

And nothing anywhere gates on convergence: `grep -rn converged scripts/` shows
`converged` is printed by `run_mcmc.py` and tabulated by `gen_tables.py`, and
**never checked**. A chain with `converged = False` flows straight into the
paper's tables.

**Fix.** The gate must fail on `converged = False`, on chain length
`< N_TAU * tau`, and on acceptance below a floor measured over the last 10 % of
the chain. Use a tau-based burn-in. Make the "too few samples" branch a
failure, not a skip.

---

## Minor points

### m1. The pancake convergence claim is arithmetically true but tests nothing about the physics.

**Location**: `scripts/run_pancake.py:26-30`; `code/absorb/pancake.py:113-121`.

I verified the resolution-floor formula independently, without using the
module. For the staggered grid `q_j = (j + 1/2) L/N` the sheet nearest the
caustic centre sits at `q = dq/2`, so `J = 1 - D cos(k dq/2) = s + (1-s) eps`
with `eps = 1 - cos(k dq/2)`. The claimed `(k dq/2)^2 / 2` matches to eight
significant figures (ratio 0.99999999 at N = 16384). Fitting `log(1/(s+eps))`
by OLS on the code's own output grid — **no ODE solved at all** — gives:

| N | eps | far (1e-3,1e-2) | near (1e-5,1e-4) |
|---|---|---|---|
| 1024 | 4.706e-06 | -0.998315 | -0.857315 |
| 4096 | 2.941e-07 | -0.999894 | -0.989343 |
| **16384** | 1.838e-08 | **-0.999993** | **-0.999325** |
| 65536 | 1.149e-09 | -1.000000 | -0.999958 |
| 262144 | 7.181e-11 | -1.000000 | -0.999997 |

Reported `A_none`: far **-0.9999934028**, near **-0.9993253982**. Six-digit
agreement with a closed-form expression. Three consequences:

1. The "-1.0000 at 65536" statement is correct arithmetic.
2. But the production suite runs at **`N_SHEETS = 16384`**
   (`run_pancake.py:28`), where the near-window exponent is **-0.99933** and
   does *not* round to -1.0000. The convergence figure is quoted from a
   resolution the suite does not use.
3. The whole refinement study measures the discretisation of a **known
   kinematic solution** (`rho_I = 1/J`), not the absorption dynamics. It is a
   solver self-test, and should be described as one.

The control's absolute agreement is also slightly weaker than a "twelve digits"
claim would support: `centre_rho_I = 981948.3020230634` against the exact
`1/J = 981948.302068`, a relative error of **4.6e-11**. (That wording has
already been removed from the tex — good.)

### m2. The log-log OLS fit: the spacing concern is unfounded, but the fit is reported without any uncertainty.

I checked whether the output points are unevenly spaced in `log s`, since the
grid is graded in `u = -ln(1-D)`. **They are not a problem.** The graded grid is
uniform in `u` and `out_idx` is uniform in step index, so the recorded points
are uniform in `log s` with spacing **0.07231** (min 0.07196, max 0.07253) and
**32 points per decade** in both fit windows. OLS is not endpoint-dominated by
uneven spacing, and I withdraw that concern.

What remains: the deviation from the analytic exponent is a *systematic*
curvature (the `eps` floor), not noise, so OLS returns a leverage-weighted
average slope — and `fit_exponent` records **no residual, no R^2, no
uncertainty**. Quoting an exponent to four decimals from an unweighted OLS with
no error bar is over-precise. It also returns a bare `NaN` when fewer than five
points pass the mask (`run_pancake.py:35-36`) with no warning.

**Fix.** Report a bootstrap or fit uncertainty on every exponent; better, fit
`y = C (s + eps)^n` and let the known floor be a fitted nuisance rather than a
bias; make the `NaN` path emit a warning.

### m3. The old mass residual was indeed the wrong conservation statement; the replacement is correct but no longer tests the vacuum at all.

**Location**: `scripts/run_pancake.py:57-71` (new); `code/absorb/collapse.py:140-144`.

The version I was asked to review computed
`|(dust + vacuum) - initial dust| / initial dust`. Measured in
`results/pancake.json` it reports **0.1199 for `B_cosmo`** and **0.0963–0.1440**
across the collapse cases — a 10–14 % violation, presented as a conservation
check. The only two cases that passed, at 8.199e-15, are exactly the two in
which the vacuum is identically zero: `A_none`, and `C_collapse_b1p0` where
`b = 1` sends everything to defects. **The check passed only when there was
nothing to check.**

The comparison was indeed inconsistent, for the reason the brief suspected. With
`rho` an Eulerian density, the comoving mass element is `rho |J| dq`; but `V`
obeys `dV/dt = (1-b) Gamma rho_I` with **no** `-Theta V` term (deliberate —
`collapse.py:140-144`: the vacuum "is not diluted by the flow"). Neither
weighting conserves:

```
d/dt[ (rho_I + rho_D)|J| + V|J| ] = Theta V |J|          != 0
d/dt[ (rho_I + rho_D)|J| + V     ] = (1-b) Gamma rho_I (|J| - 1)  != 0
```

and the discrepancy is concentrated exactly at the caustic, where `|J| -> 0`.

The authors replaced this while the review was in progress, and the new comment
states the reason correctly. I verified the new identities are exact:
`d(rho_I J)/dt = -Gamma rho_I J` and `d(1-f)/dt = -(1-f) Gamma` share an ODE
and an initial condition, so `rho_I|J| = 1-f`; and
`d(rho_D J)/dt = b Gamma rho_I J = b df/dt`, so `rho_D|J| = b f`. Two remarks
survive the fix:

1. These identities are **internal to the per-sheet ODE system**. They check
   RK4 consistency and the Jacobian weighting — worth having — but they are not
   a conservation law of the physical system, and should not be described as
   one.
2. There is now **no conserved total at all**, and in particular the vacuum is
   no longer checked by anything. That is a genuine physical feature of an
   interacting vacuum, not a bug, but the paper should say it plainly rather
   than leave a diagnostic that has quietly become a solver self-test.

The Jacobian weighting in `column_rho_I` / `column_rho_D` is **correct**
(`rho` is an Eulerian density and `|J| dq` the Eulerian length element).
`integral_V` uses the same weighting and is, given the `V` equation, the one
integral that is not a meaningful conserved quantity.

### m4. The binomial claim is exactly right, and the two objections I had were fixed mid-review. What remains is a missing cross-reference that bites the paper's headline case.

**Location**: `paper/sections/03_absorbing_process.tex`, `rem:hazard-time-change`,
`rem:residual-boundary-layer`, `eq:process-binomial`,
`eq:process-breakdown-gap`; `code/absorb/collapse.py:240-268`.

**`eq:process-binomial` verified by an independent route.** I solved the master
equation `dP_k/dΛ = (N-k+1) P_{k-1} - (N-k) P_k`, `P_k(0) = δ_{k0}`, with Radau
at `rtol = 1e-12`, and compared to `scipy.stats.binom.pmf(k, N, 1-e^{-Λ})`:

| N | Λ = 0.3 | 1.0 | 3.0 | 10.0 |
|---|---|---|---|---|
| 3 | 7.8e-16 | 1.4e-15 | 1.8e-15 | 2.4e-15 |
| 8 | 3.9e-16 | 8.9e-16 | 1.4e-15 | 2.8e-15 |
| 20 | 2.5e-16 | 1.3e-16 | 8.9e-16 | 2.4e-15 |

(max absolute pmf discrepancy). **The law is exact, as claimed.**

**Two objections, both already addressed.** I had drafted (i) that "Nothing is
lost" was an overclaim because the escape needs a state-independent `Gam` while
the paper's own `eq:process-rate` depends on `f` and `M`; and (ii) that "no
boundary layer" was false for the quantity that carries the physics, since
`rho_I ∝ 1-f` has relative fluctuation `sqrt(p/[N(1-p)])`, which diverges. The
authors revised both during this review. The remark now says explicitly "The
hypothesis that matters here is that `Gam` does not depend on the state; the
reinforced law `eq:process-rate` does, so the statement applies to a
compression-driven channel and not to the reinforcement", and the new
`rem:residual-boundary-layer` states the fluctuation formula and the breakdown
scale. **Both are correct and both match my numbers.** I verified the new
`eq:process-breakdown-gap`: for `Gam = g/(T-t)`, `N e^{-Λ} = 1` at
`s_* = N^{-1/g}` exactly (residual `N e^{-Λ} = 1.0000000000` at every
`g ∈ {0.5, 1, 1.5, 3}` and `N ∈ {1e2, 1e4, 1e6}`), with
`sd(1-f)/(1-f) = 0.99999` and `P(all N converted) = 0.368` there — i.e. the
relative fluctuation is exactly unity at `s_*`, as the remark asserts.

**What remains.** Three small things:

1. **`rem:residual-boundary-layer` is never cross-referenced from
   `sec:defects-caustics`, and it bites the paper's headline case hardest.**
   The remark ends "Any statement about the regularity of `rhoI` at a caustic is
   a statement about the continuum model, and holds only outside `s_*`". For the
   compression channel `g = kappa c`, `s_* = N^{-1/(kappa c)}`, so **larger
   `kappa` makes the continuum window smaller**. Measured: at `N = 10^6` units,
   `s_* = 1e-6` for `kappa = 1` but `s_* = 1e-2` for `kappa = 3`. The pancake
   suite integrates to `s = 1e-6`, i.e. **four decades inside the breakdown
   layer** for the `kappa = 3` case that `sec:defects-caustics` and
   `fig:pancake` advertise as removing the divergence. The caveat should be
   cited where the regularity conclusion is drawn (`eq:defects-regularity` and
   the "Numerical test" paragraph), with an explicit statement of what `N` is
   assumed, or the conclusion restricted to `s > s_*`.
2. `eq:process-breakdown-gap` is written for `T - t_i = 1`. The general result
   is `s_* = s_0 N^{-1/g}`; state the normalisation.
3. `rem:hazard-time-change` still contains the sentence "the `N^{-1/2}` law
   holds uniformly with no boundary layer where the rate diverges" three lines
   above a remark titled "But the residual density has a boundary layer". It is
   defensible as written, because it is a statement about `fconv` — but qualify
   it as such ("no boundary layer *in* `fconv`") or a reader will take the two
   remarks to contradict each other.

Also minor: `binomial_law_in_hazard_time` is named and documented for the count
`K` but returns `K/N`, the fraction.

### m5. `resources.py`: the copy-on-write question is a non-issue, but the utility can never refuse.

**Location**: `code/absorb/resources.py:52-72`; `code/absorb/sampling.py:66-78`.

**On the COW question in the brief — `safe_workers` errs in the safe
direction.** Budgeting the full measured peak per worker **over**-estimates
demand and therefore **under**-estimates the worker count. `peak_rss_mb()`
returns `max(self, children)`, so for a forked pool the per-worker figure
includes the parent's whole baseline (numpy/scipy plus the ~20 MB supernova
covariance), and `n` workers are budgeted `n` copies of pages that exist once —
again conservative. Neither is a correctness problem; both cost cores, which on
a shared machine is the right error. **I certify the direction.**

**The correctness problem is `return max(1, n)` (`:72`).** Measured right now:
`MemAvailable = 1854 MB`, `MemTotal = 15331 MB`, so the margin is
`max(1500, 0.20 * 15331) = ` **3066 MB** and `usable = ` **-1213 MB**. Yet:

```
safe_workers(100)    -> 1   (by_memory = -13)
safe_workers(720)    -> 1   (by_memory = -2)
safe_workers(100000) -> 1   (by_memory = -1)
```

The function **can never say "not now"**, so the hard floor its docstring
describes is unenforceable, and a caller that trusts it will start work below
the floor — as it would do at this moment. Note also that the effective reserve
is 3066 MB, twice the 1.5 GB the docstring foregrounds.

**`peak_rss_mb` does not capture pool workers.**
`getrusage(RUSAGE_CHILDREN).ru_maxrss` is populated only for children that have
been **reaped**, and it is the maximum over children of a **single** child's
peak, **not the sum** — so for a pool of `n` workers it under-reports the
aggregate by roughly a factor of `n`. Separately, `ru_maxrss` is a monotone
high-water mark; measured, a process at 32 MB that allocates and *touches*
320 MB then frees it still reports **337 MB** afterwards, and still 337 MB after
a later small allocation. So `record()` reports the **process lifetime peak**,
not the peak of its `with` block, and `max(peak_rss_mb(), rss0)` in the
`finally` clause is a no-op. Every entry in `results/resource_usage.json`
(35–60 MB) is a single-process figure where this happens not to matter — but
the utility would silently mis-measure the very MCMC pool it was written for.

**Two inconsistent budgets.** `resources.safe_workers` (margin 3066 MB) and
`sampling.safe_n_proc` (`MEMORY_BUDGET_FRACTION = 0.5`,
`WORKER_RSS_MB = 720`, **no margin at all**), and the largest consumer — the
MCMC — uses the one with no floor. At `MemAvailable = 5000 MB`, `safe_n_proc`
allows `int(5000*0.5/720) = 3` workers = 2160 MB, leaving 2840 MB, **below the
3066 MB `resources.py` reserves**. One implementation, please, returning 0 when
nothing fits and letting callers decline.

### m6. The chains are not reproducible from the recorded seed.

`ChainSummary.seed` records `SEED = 20260909` and `results.json` quotes it, but
`emcee.EnsembleSampler` is constructed at `sampling.py:302` with **no**
`random_state`, so it seeds itself from OS entropy. The recorded seed controls
only `find_map` and the initial walker ball (`:280-287`). Resumption *is*
RNG-continuous — I confirmed the backend stores `random_state_0 = 'MT19937'`
with the full 624-word state — so the defect is confined to the first session,
but that is enough: re-running the pipeline from scratch will not reproduce any
chain, while the recorded metadata implies it will. Either seed the sampler or
stop recording a seed that does not determine the output.

### m7. Tautological tests: several assert arithmetic done inside the test body and exercise no code under test.

**Location**: `code/tests/test_collapse.py`.

- **`test_bounded_rate_cannot_regularize` (`:42-65`)** — the test of the
  manuscript's flagship theorem — calls **nothing** from the module. It sets
  `log_suppression = -gamma_bound`, `log_s_star = -gamma_bound`, then asserts
  `-log_s + log_suppression > 0` for `log_s = log_s_star - 1`, i.e.
  `gamma_bound + 1 - gamma_bound > 0`. It is `1 > 0`, parametrised over four
  values of `gamma_bound`. `bounded_rate_factor` is imported at the top of the
  file and **never called anywhere in it**.
- **`test_variance_formula_is_exact_through_the_singularity` (`:231-248`)**
  defines `var = p*(1-p)/N` two lines above and asserts
  `sqrt(N*var) == sqrt(p*(1-p))` — algebra in the test, not a property of the
  module.
- **`test_zeldovich_exponent_is_one`** asserts that a function whose body is
  `return 1.0` returns 1.0.
- **`test_stress_tensor_regular_only_for_kappa_gt_one_and_b_zero`** and
  **`test_planar_table_agrees_with_the_local_solution`** restate the one-line
  definitions inside `regularity_conditions` and `planar_scaling_table`; the
  latter's docstring claims it checks against `LocalSector`, which it never
  constructs.

The same file contains genuinely informative tests —
`test_closed_form_matches_quadrature`, `test_vacuum_needs_a_strictly_stronger_condition`,
`test_defects_inherit_the_divergence`, `test_binomial_law_matches_the_direct_chain`
(an independent jump-chain simulation compared by KS test). The authors clearly
know how to write one. Make the bounded-rate test call `density_ratio` with a
genuinely bounded `Gamma` and assert the crossing scale, as
`test_bounded_rate_is_the_paper_s_case` already does two functions below.

### m8. No test coverage for three of the modules under review.

`grep -rln "pancake\|resources\|sampling" code/tests/` returns only
`test_collapse.py`, and that only because it matches the word "collapse". There
is no `test_pancake.py`, no `test_resources.py`, no `test_sampling.py`.
`pancake.py` is the entire numerical basis of `sec:defects-caustics`;
`resources.py` is the safety utility guarding a shared machine. At minimum,
`pancake.py` needs a test asserting `rho_I|J| = 1-f` and `rho_D|J| = b f` to
1e-12, and one asserting the control run reproduces `1/J`.

### m9. Silent numerical hygiene in `pancake.py`.

- **`np.clip(f, 0, 1, out=f)` and `np.clip(M, 0, 1, out=M)` (`:200-201`)** are
  non-conservative fixups applied after **every** RK4 step. Analytically
  `df/dt = (1-f)Gamma` and `dM/dt = (f-M)/tau_M` both preserve `[0,1]`, so they
  should be no-ops; if one ever bites it silently destroys the accuracy the
  section claims, with no record. Replace with an assertion, or a counter that
  is reported.
- **The suite never crosses the caustic.** `D_END = 1 - 1e-6 < 1`, so the
  module's stated motivation ("a single-stream pressureless fluid ceases to be
  a solution after shell crossing ... Following sheets avoids the issue") is
  never exercised. Either run past `D = 1` and show the multi-stream sum, or
  reduce the claim to what is actually done, which is an approach to the
  caustic.
- `out_idx` includes index `n_steps`, which the loop
  `for i, D in enumerate(D_grid[:-1])` never reaches; the final record is
  appended separately. Harmless, but confusing to a reader checking the output
  count.

### m10. `run_profile.py` details, including the threshold question.

- **`np.interp` on a possibly non-monotone profile** (`:151` and `:100`)
  requires `xp` to be increasing. A profile carries no such guarantee, and the
  actual output is not monotone — `results/profile.json` falls from 0.0744 at
  `eps = 0.25` to 0.0499 at `eps = 0.30`. Here the non-monotonicity happens to
  lie outside the bracket so the answer is unaffected, but the guard is absent
  and the failure would be silent. Bracket the crossing between the last point
  below and the first point above.
- `chi2_at_zero` is written **after** `chi2 -= chi2.min()`, so it is a Δchi2,
  not a chi2. The name will mislead whoever reads the JSON.
- `lows`/`highs` are built from `post.model.priors()` only, omitting nuisance
  parameters. Harmless while `nuisance = ()`; a latent index bug the moment one
  is added.
- Because `neg` calls `post()`, the maximisation is confined to the prior box.
  Every `Prior` is uniform (`params.py:33-49`; `log_prior` returns `0.0`
  inside), so `-2*post` **is** exactly chi2 there and this is a genuine profile
  *likelihood*, not a penalised posterior — I certify that, and the paper
  should state it, together with the fact that it is profiled over a bounded
  region.
- **On Δchi2 = 2.71.** It is the right number for a one-sided 95 % upper limit
  on one **interior** parameter (`sqrt(2.71) = 1.645`). The `eps >= 0` boundary
  modifies the null distribution *at* `eps = 0` (Chernoff's 50:50 mixture) and
  therefore the p-value for **rejecting** `eps = 0`; it does not invalidate
  2.71 for an upper limit, which merely over-covers, i.e. errs conservative.
  **The threshold is not the problem here.** The problems are (a) that this
  profile never reaches any threshold at all (M3), and (b) that the real
  irregularity is Davies', not Chernoff's — at `eps = 0` two parameters are
  *exactly* unidentified (12/12 combinations differ by exactly 0.000e+00), so
  no fixed chi2 quantile is the correct calibration. Say so, and calibrate by
  simulation if a limit is to be quoted at all.

### m11. Nelder-Mead in the profile: getting stuck is demonstrable, and the profile's shape is barely above its own noise.

The profile's own output is non-monotone by **0.0245** between `eps = 0.25` and
`eps = 0.30`, and from `eps = 0.30` onward the values rise in an almost
arithmetic ramp — 0.0499, 0.0503, 0.0508, 0.0515, 0.0524, 0.0532, 0.0542
(successive differences 0.0004–0.0010) — the signature of **one warm-started
solution being tracked rather than re-found**. The total variation of the curve
above `eps = 0` is **0.074**; the optimiser noise floor is at least **0.024**,
from that non-monotonicity and independently from the 0.024 disagreement with
`run_mcmc.py`'s maximisation at `eps = 0` (M2). The shape of the profile is
barely above its own numerical noise.

**On hysteresis I ran a test rather than asserting it.** For each grid point `k`
I transplanted the stored `best_theta[k+1]` nuisance vector back to
`eps = grid[k]` and re-evaluated. In **0 of 12** cases did the transplant beat
the reported value, so the ascending sweep is not demonstrably missing a better
basin found later — I report that in the authors' favour. But the same test
showed *why* the optimisation is hard: the transplants are catastrophically
worse (chi2 = **167 000** at `eps = 0` from the `eps = 0.05` solution; **24 821**
at `eps = 0.05` from the `eps = 0.10` solution). Nelder-Mead with 3000
evaluations in 5 dimensions, on a ridge with an aspect ratio of ~1e3, is not a
reliable maximiser.

**Concrete validation to propose:**
1. **Run the sweep in both directions** (ascending and descending in `eps`) and
   require the two profiles to agree to better than 0.01 in Δchi2 at every grid
   point. This is the direct hysteresis test and costs one extra sweep.
2. Draw restarts from the **chain's own samples** at nearby `eps` rather than
   uniformly from the prior box, and use a trust-region optimiser with the
   ridge direction preconditioned out.
3. At two or three grid points, verify the profile minimum against a long
   dedicated minimisation, and **quote the residual as the profile's error
   bar**. A profile whose error bar exceeds its total variation should be
   reported as uninformative, not as a limit.

### m12. The likelihood cost quoted in the code is understated by ~1.5x.

`sampling.py`'s module docstring says "one background solve (~11 ms)". Measured
here, single-threaded, over 20 consecutive evaluations of the `xi_h` posterior
on the baseline dataset: **16.6 ms** per call (38 ms on a cold first call).
Minor in itself, but the runtime and worker-count arguments elsewhere in the
module rest on the 11 ms figure.

### m13. `check_chain_stability.py` model-name parsing is fragile and fails silently.

`model = name.rsplit("_", 1)[0]` splits `"xi_h_baseline"` correctly only because
the dataset name contains no underscore. Any dataset named with one makes
`model not in MODELS`, and the file is skipped by `continue` with **no
message**. Match against the known model and dataset names instead.

---

## What I checked and found correct

A report that only attacks is not doing its job either. These I tried to break
and could not:

1. **The resolution-floor formula.** `eps = (k dq/2)^2/2` reproduces the exact
   `1 - cos(k dq/2)` to eight significant figures at every N from 1024 to
   65536 (ratio 0.99999999 at N = 16384).
2. **The control run's time integration.** `A_none` gives
   `centre_rho_I = 981948.3020230634` against the analytic
   `1/J = 981948.302068` — a relative error of **4.6e-11** over 25 000 RK4
   steps. The graded grid is well chosen for the reason claimed: `|Theta| dt`
   is held at `du = 5.756e-4` uniformly through the approach, which is exactly
   what keeps a fixed-order explicit method accurate against a `1/s`
   singularity.
3. **The output grid is uniform in `log s`**, spacing 0.07231 (min 0.07196,
   max 0.07253), 32 points per decade in both fit windows. My prior concern
   about a graded grid biasing a log-log fit was wrong.
4. **The measured exponents do reproduce the analytic values.** Near-window
   fits: `kappa = 0.5 -> -0.4992` (theory -0.5), `kappa = 1.0 -> +0.0005`
   (theory 0), `kappa = 1.5 -> +0.5002` (theory +0.5), `kappa = 3.0 -> +1.9992`
   (theory +2.0), and the residuals are of the same order as the
   resolution-floor bias computed in m1. Independence of `b`, `tau_M`, `alpha`
   and `beta` holds as the analysis requires.
5. **The defect exponent is measured, in the only two cases where it is
   defined.** `exp_rho_D_near = -0.99933` for both `b = 0.25` and `b = 1.0`,
   against the predicted `-c = -1`. The `NaN` in the other ten cases is correct
   behaviour: `rho_D` is identically zero when `b = 0`.
6. **`eq:process-binomial` is exact**, verified by master equation to
   **2.4e-15** (max pmf discrepancy) across N in {3, 8, 20} and Λ in
   {0.3, 1, 3, 10}.
6b. **`eq:process-breakdown-gap` is exact**, and its two companion statements
   with it: `N e^{-Λ} = 1` holds to 1.0000000000 at `s_* = N^{-1/g}` for every
   `g` in {0.5, 1, 1.5, 3} and `N` in {1e2, 1e4, 1e6}, and at that point
   `sd(1-f)/(1-f) = 0.99999` and `P(all N converted) = 0.368`. The
   state-independence caveat now in `rem:hazard-time-change` is also exactly
   the right one.
7. **The new survival identities in `run_pancake.py` are the right ones**, and
   I derived both independently.
8. **The nesting is exact.** `xi_h` at `eps = 0` reproduces LambdaCDM's chi2
   bit-for-bit (difference exactly 0.000e+00) for all 12 `(log10_xi, z_act)`
   combinations tested. This is a real and non-trivial property of the
   implementation, even though — as M2 argues — it is precisely what makes the
   AIC/BIC penalties wrong.
9. **The `lcdm` chain is genuinely converged**: 2000 steps, acceptance 0.4386,
   `tau_max = 12.7`, comfortably past the `N_TAU = 50` criterion.
10. **The prescribed-trajectory caveat is now stated clearly.** The revised
    "Numerical test" paragraph says the trajectories "are prescribed by the
    Zel'dovich map, so the test isolates the effect of conversion from the
    gravitational back-reaction, and it is not a self-consistent solution."
    That is exactly right, and the earlier "twelve digits" wording has been
    removed. This part of point 7 in my brief is resolved.
11. **`safe_workers` errs conservative** on the copy-on-write question, which
    is the correct direction for a shared machine (see m5 for what is actually
    wrong with it).

---

## Questions the authors must answer

1. What is the acceptance fraction over the **last 10 %** of each chain, and
   what is `tau` estimated on the second half alone? The cumulative figures are
   flattered by the early transient.
2. **Is any number in the manuscript taken from `xi_h_baseline.h5`?** If so,
   which, and how is it defended given M1? If the answer is "only `chi2_min`",
   say so explicitly and M2 becomes the whole issue.
3. Under what reference distribution is Δchi2 = 0.82 (or 0.84) to be
   interpreted, given that `log10_xi` and `z_act` are *exactly* unidentified at
   `eps = 0`? What is the effective parameter count used in AIC and BIC?
4. What is `eps_limit_95` intended to mean when the profile never crosses 2.71,
   and what would change in the manuscript if the grid ran to `eps = 1`?
5. Was `results/pancake.json` regenerated after `run_pancake.py` changed at
   00:04:23, and from what file are the `\numPancake*` macros meant to be
   generated?
6. Is there any conserved quantity for the pancake system that includes `V`? If
   not — which I believe is the correct answer — is that stated anywhere in the
   manuscript?
7. `run_pancake.py` sets `N_SHEETS = 16384` while the convergence claim is
   quoted at 65536. Which resolution produced the numbers in the figure and in
   the text?
8. What value of `N` is assumed when `rem:residual-boundary-layer` is applied to
   the caustic? For `kappa = 3` and `N = 10^6` the breakdown scale is
   `s_* = 1e-2`, while the pancake runs to `s = 1e-6` — four decades inside the
   layer where, by the paper's own new remark, the continuum description of
   `rhoI` does not hold.
