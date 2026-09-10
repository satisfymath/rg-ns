# Referee report — caustics and absorption

**Manuscript**: Self-reinforced geometric absorption
**Referee**: A (mathematical physicist: PDE, GR, singularity formation)
**Round**: 1 — new material only
(`docs/theory/06_caustics_and_absorption.md`, `code/absorb/collapse.py`,
`code/absorb/pancake.py`, `code/tests/test_collapse.py`,
`paper/sections/11_defects.tex` §`sec:defects-caustics`,
`paper/sections/03_absorbing_process.tex` `rem:hazard-time-change`,
`paper/sections/13_outlook.tex` §`sec:outlook-caustics`)
**Date**: 2026-09-10

## Summary (3 lines)

The authors retract an earlier conjecture that conversion regularizes a shell
crossing, and replace it with an exact one-line solution of the local
continuity equation from which they read off: (i) a bounded rate cannot beat a
non-integrable compression; (ii) a compression-driven rate
$\Gamma=\kappa[-\Theta]_+$ regularizes the stress tensor iff $\kappa>1$ *and*
the branching ratio $b=0$; (iii) covariance then forces either a useless
dust-to-dust transfer or a momentum transfer with a divergent force density.
They argue the new channel is invisible to FLRW and all of its perturbations,
and support the local analysis with a 1D Zel'dovich pancake in Lagrangian form.

## Recommendation

[ ] Accept  [ ] Minor revision  [x] Major revision  [ ] Reject

The mathematics I was able to check is, with the exceptions listed below,
correct — several results are exactly right and I say so explicitly. The
problems are (a) the regularity criterion is not a singularity criterion and the
generic case addressed is a *weak* singularity, which undercuts the motivation;
(b) the numerical experiment never reaches shell crossing, so the regime the
section is about is untested; (c) two theorems are applied outside the domain
where their hypotheses hold; (d) a second published rate law is not covered by
the boundedness claim; (e) one fluctuation claim is true for the wrong variable.
None of this touches the cosmological fits, and I agree with the authors that no
published number changes — but that conclusion needs a sharper statement than
the one given.

---

## Major points

### M1. The regularity criterion is not a singularity criterion, and the generic case is a *weak* singularity

**Location**: note §2(c), `eq:defects-regularity` (11_defects.tex:201–204),
`SelfSimilarScaling` (collapse.py:302–340), table row "curvature invariant".

The whole section is organized around "$T_{\mu\nu}$ remains finite at the
caustic". Pointwise finiteness of $T_{\mu\nu}$ is neither necessary nor
sufficient for the spacetime to be singular, and the manuscript never says which
notion of singularity it is regularizing (curvature scalars? $C^0$/$C^2$
extendibility? causal geodesic completeness? Tipler strong curvature?).

This matters, because for the case the authors actually treat the answer is
known and goes the other way. With $c=1$ (their own generic Zel'dovich value,
`zeldovich_expansion_exponent()`), $R_{\mu\nu}k^\mu k^\nu \sim \rho \sim s^{-1}$
along a causal geodesic, and the Tipler double integral
$\int^\lambda\!\mathrm{d}\lambda'\int^{\lambda'}\!\mathrm{d}\lambda''\,
R_{\mu\nu}k^\mu k^\nu \sim \int^\lambda \ln\lambda'\,\mathrm{d}\lambda' \to 0$
converges to zero: the singularity is *gravitationally weak* in the sense of
Tipler, and (as is standard for LTB shell crossings) the spacetime is expected
to be extendible through it. The double integral fails to converge only for
$c\ge 2$, i.e. a *degenerate* crossing, which the authors themselves call
non-generic. So the object being "regularized" is, in the generic case, not a
spacetime singularity at all.

The same criticism applies to `SelfSimilarScaling`. $E_{\rm core}=\int\rho
\sqrt{\gamma}\,\mathrm{d}^3x$ is a rest-mass integral, not a GR energy; there is
no local gravitational energy, and the correct quasi-local statement would use
Misner–Sharp or Hawking mass. The docstring's own honest remark ("dimensional
bookkeeping, not a dynamical mechanism") should be promoted into the paper.

**Fix**: state the singularity notion explicitly at the top of
`sec:defects-caustics`; add the Tipler/Królak strong-curvature check for
$c=1$ and $c\ge2$; cite the shell-crossing-extendibility literature
(Tipler 1977; Clarke & Królak 1985; Nolan, *CQG* **20** (2003) 575) and say
plainly that for a generic fold the divergence is a weak, integrable,
instantaneous event, so the interest of `eq:defects-regularity` is that it
sharpens *when a stronger criterion would be needed*, not that it removes a
singularity.

### M2. The numerical test never reaches — let alone passes — shell crossing

**Location**: `pancake.py` docstring lines 8–21, `PancakeParams.d_end`
(pancake.py:70), `run_pancake.py:29` (`D_END = 1 - 1e-6`),
11_defects.tex:248–255, `fig:pancake`.

The stated justification for the Lagrangian formulation is that "a single-stream
pressureless fluid ceases to be a solution after shell crossing, so an Eulerian
PDE cannot be continued naively past it. Following sheets avoids the issue."
That machinery is never exercised. With $A=k=1$ the Jacobian is
$J = 1 - D\cos kq \ge 1-D > 0$ for every $D<1$, so no sheet ever crosses another.
I checked the archived runs directly:

```
results/sims/pancake_A_none.npz         min J = 1.018384e-06,  any J<0? False
results/sims/pancake_C_collapse_k1p5.npz min J = 1.018384e-06,  any J<0? False
```

and confirmed on the map itself that the first crossing occurs exactly at $D=1$
(for $D=1+10^{-6}$ the multi-stream region has Lagrangian width
$\Delta q = 2.83\times10^{-3}\sim 2\sqrt2\,s^{1/2}$ and Eulerian width
$1.886\times10^{-9}\sim 1.886\,s^{3/2}$). Every run stops one part in $10^6$
*before* the caustic.

Two consequences.

1. The section's subject — what conversion does *at and after* shell crossing,
   where $\rho_D$ must be treated as pressureless dust and where multi-streaming
   makes that assumption false — is not tested at all. The figure and the
   sentence "carries out the one-dimensional test proposed here"
   (13_outlook.tex:58–59) overstate what was done.
2. Worse for the proposal itself: for the caustic sheet $J=1-D$, so
   $\Theta = \dot D S'/J = -1/(1-D)$ before crossing and $+1/(D-1)$ *after*.
   The candidate channel $\kappa[-\Theta]_+$ therefore switches **off** at the
   instant of crossing and does nothing to the multi-stream configuration; each
   sheet's density falls again on its own. This should be stated: the channel
   acts only on the run-up, which is precisely the regime M1 says is weak.

**Fix**: either continue the runs through $D>1$ (the Lagrangian code already
supports it — `np.abs(J)` is used throughout) and report the multi-stream
behaviour, or delete the claim that the Lagrangian formulation is what makes the
test possible and say explicitly that the experiment is a pre-caustic
approach study. Add the post-crossing sign flip of $\Theta$ to the discussion.

### M3. Theorem D: the topology claim is false as stated, and averaging is not covered

**Location**: note §4 Theorem D; 11_defects.tex:223–229.

The mathematical core — $[-x]_+$ has all derivatives zero at any $x>0$ and is
identically zero on a neighbourhood — is correct, and I certify the conclusion
*for the hypothesis the authors actually need*. But the hypothesis stated is
wrong, in three ways.

1. **"a neighbourhood of it in any reasonable perturbative topology".** False in
   $L^p$ for every $p<\infty$, in $H^{-s}$, and in any topology not controlling
   the sup norm: take $\delta\Theta = -A\,\varphi(x/\ell)$ with $A>3H$ fixed and
   $\ell\to0$; then $\|\delta\Theta\|_{L^2}\propto A\ell^{1/2}\to0$ while
   $\Theta<0$ on a set of positive measure. The correct statement is: the channel
   vanishes identically whenever $\|\delta\Theta\|_{\infty}<3H$ *at the time
   considered*. Only a $C^0$ (or stronger) topology will do.
2. **The neighbourhood shrinks with time.** Perturbation theory is an expansion
   in an amplitude $\varepsilon$ at fixed time; the growing mode means that for
   any fixed $\varepsilon>0$ there is a $t$ at which $\varepsilon\,\delta\Theta$
   exceeds $3H$. The theorem is a statement at fixed $t$ with
   $\varepsilon<\varepsilon_c(t)$, $\varepsilon_c(t)\to0$.
3. **Averaged or stochastic $\Theta$.** If $\Theta$ has any distribution with
   support crossing zero, $\mathbb{E}\,\kappa[-\Theta]_+ > 0$ strictly. For
   $\Theta\sim\mathcal N(3H,\sigma^2)$ with $3H=\kappa=1$ I computed
   $\mathbb{E}[\Gamma] = \sigma\phi(\mu/\sigma)-\mu\Phi(-\mu/\sigma)$:

   | $\sigma/3H$ | 1.00 | 0.50 | 0.30 | 0.20 | 0.10 | 0.05 |
   |---|---|---|---|---|---|---|
   | $\mathbb{E}[\Gamma]$ | 8.33e-2 | 4.25e-3 | 3.36e-5 | 1.07e-8 | 7.48e-26 | 6.85e-92 |

   Non-zero for every $\sigma>0$, and decaying like $e^{-\mu^2/2\sigma^2}$ —
   i.e. *non-perturbatively* small, which is exactly why no order of the Taylor
   series sees it. That is a much better statement than "identically zero", and
   it is the honest one: the correction is invisible to perturbation theory, not
   absent. Once $\sigma\sim 3H$ (nonlinear structure, $z\lesssim$ a few) it is
   $O(10\%)$ of $\kappa\,3H$ and there is a substantial volume fraction with
   $\Theta<0$ today.

I agree that **no published number changes**, but the reason is narrower than
the one given: the fits use the background and the linear theory, in both of
which $\delta\Theta$ is small in sup norm on the relevant support. Say that.

**Fix**: restate Theorem D as "$\Gamma_{\rm collapse}\equiv0$ on
$\{\|\delta\Theta\|_\infty<3H\}$, hence every coefficient of the formal
expansion about FLRW vanishes; the channel is a non-perturbative correction,
of order $e^{-(3H)^2/2\sigma^2}$ under Gaussian coarse-graining, not zero."
Delete "any reasonable perturbative topology".

### M4. "The rate of the model as published is bounded" covers only one of the two published rate laws

**Location**: note §1 ("This applies to the model as published");
11_defects.tex:183–184; `test_bounded_rate_is_the_paper_s_case`
(test_collapse.py:68).

For the constant-$\Gamma_0$ family the claim is right: $f\in[0,1]$ (invariant,
since $\dot f=(1-f)\Gamma\ge0$), $M\in[0,1]$ by comparison from
$\tau_M\dot M=f-M$, $S_{\rm act}=a^p/(a^p+a_{\rm act}^p)\in[0,1]$
(`background.py:226–234`), $\alpha+\beta\ge0$, so
$\Gamma\le\Gamma_0 e^{\alpha+\beta}$. Certified.

But the manuscript also fits the $\xi H$ family, $\Gamma=\xi_0 H
S_{\rm act}e^{\alpha f+\beta M}$ (§`sec:solvable-family`; in code
`params.py:125–135`, `BackgroundParams.rate_tracks_H`, `background.py:279–280`),
and the note never mentions it. Its natural local covariantization is
$\Gamma=(\xi_0/3)\Theta\,S_{\rm act}e^{\cdots}$, which at a caustic is (i)
*unbounded*, so Theorem A does not apply, and (ii) *negative*, which violates
$\Gamma\ge0$ in Theorem A, in `prop:survival`, and in the positivity results of
§5. If instead one covariantizes with $|\Theta|$ or $[-\Theta]_+$, one lands
exactly on the compression-driven channel with $\kappa=\xi_0/3$ — so the
$\xi H$ benchmark is not neutral on the caustic question at all, and the
threshold $\kappa>1$ becomes $\xi_0>3$, which is a testable statement about a
parameter the paper already fits.

**Fix**: add a paragraph in `sec:defects-caustics` covering the $\xi H$ family:
state which covariantization is intended, show that $\Gamma\ge0$ survives it,
and — this is the interesting part — report where the fitted $\xi_0$ posterior
sits relative to 3.

### M5. Theorem C is not a dichotomy, and it duplicates an obstruction the paper already states

**Location**: note §3 Theorem C; 11_defects.tex:210–221.

(i) *Dust to dust.* Certified as stated. The two continuity equations do sum to
the unmodified one, and I confirm the consistency question you did not raise
explicitly: since $Q^\nu=\Gamma\rho_I u^\nu$ has no part orthogonal to $u$, the
orthogonal projection of $\nabla_\mu T^{\mu\nu}_{(i)}$ still forces
$a^\nu=0$ for each sector separately, so "both sectors geodesic" is consistent,
not an extra assumption. State that; a reader will ask.

What *is* an extra assumption, and is not stated, is that the product sector is
comoving with the precursor **and pressureless**. The product is a gas of
massive solitons (§`sec:defects`). At a caustic the congruence multi-streams,
and a soliton gas with any velocity dispersion is not dust — pressurelessness is
exactly the hypothesis that fails at the place the theorem is applied. The
$\rho_D\sim s^{-c}$ result and the "nothing removes it" sentence are both
conditional on it.

(ii) *Dust to vacuum.* The derivation is correct — $Q^\nu=-\nabla^\nu V$ is a
gradient hence closed; $q^\nu=0$ makes $u^\flat$ proportional to an exact form,
hence hypersurface-orthogonal; with a geodesic clock $u_\mu=-\partial_\mu T$ one
gets $V=V(T)$ and $Q=Q(T)$. Certified.

But it is presented as exhausting the options, and it does not.

- A receiver that is **not an exact vacuum** ($p\ne-\rho$: a scalar field with a
  potential, a defect network, anything with anisotropic stress) makes
  $\nabla_\mu T^{\mu\nu}_{\rm rec}$ *not* a pure gradient and the closedness
  constraint disappears entirely. This is the standard interacting-dark-energy
  construction and it deserves a line in the theorem, not only a footnote in the
  note's summary table.
- Two sectors with **different four-velocities** is a third case not covered by
  the $Q^\nu=Qu^\nu+q^\nu$ split relative to a single $u$.
- The paper's own **four-form/membrane** realization (`prop:four-form`,
  `sec:realizations-bridge`) changes $V=h^2/2$ by nucleation, i.e. by a
  transfer supported distributionally on a membrane worldvolume. For that
  $Q^\nu$, "the force *density* diverges" is not the right diagnostic — the
  integrated impulse across the membrane is what must be finite. Theorem C
  should say whether the membrane channel evades it.

Finally, §13.2 (`sec:outlook-local-rate`) already states this obstruction in
full generality — the local rate law overdetermines the perturbations by
`eq:perturbations-compatibility`, with exactly the same two escape routes
(momentum transfer, or a receiver with its own dynamics). Theorem C is that
statement specialized to a caustic. Presenting it as a new caustic-specific
dichotomy overstates the novelty, and the two passages must cross-reference.

Related and unstated: the constraint $Q=Q(T)$ kills the paper's *published*
bounded rate too, the moment $f$ or $M$ varies across a comoving slice — not
just a $\Theta$-dependent rate. The note attributes the incompatibility to
$\Theta$-dependence alone (§3(ii), first bullet), which is too kind to the
existing law.

### M6. Theorem C(ii) is derived from a structure that fails exactly where it is applied

**Location**: note §3(ii); 11_defects.tex:211–214.

The derivation of $Q=Q(T)$ needs a globally smooth clock $u_\mu=-\partial_\mu T$
with $T$ a good foliation label. At a caustic that is precisely what breaks: the
mimetic/geodesic clock develops a caustic in $\nabla T$ (the manuscript itself
cites `babichev2017_170403367` for this at 13_outlook.tex:52). So the theorem's
hypothesis holds on the smooth part and the conclusion is drawn *at* the
singular point. I do not think the conclusion is wrong, but the argument as
written does not reach it: a limiting or distributional statement is needed
(e.g. that $Q=Q(T)$ holds on $\{s>0\}$ and the obstruction is that no
$\Theta$-dependent rate has a limit compatible with it).

**Fix**: add "on the region where $T$ is a smooth foliation label" to the
hypothesis, and give the limiting argument that carries it to $s\to0$.

### M7. `rem:hazard-time-change`: the "no boundary layer" claim is true for $f$ and false for $1-f$

**Location**: 03_absorbing_process.tex:144–166, `eq:process-binomial`;
`binomial_law_in_hazard_time` docstring (collapse.py:240–265);
`test_root_n_scaling_survives_the_singularity`.

Two separate problems.

**(a) It does not apply to the model.** The remark is titled "The boundedness
hypothesis can be dropped". It does not drop it; it *replaces* it by
state-independence of $\Gamma$. The paper's rate is state-dependent by
construction — $\Gamma\propto e^{\alpha f+\beta M}$ with $\alpha,\beta>0$ *is*
the self-reinforcement the paper is named after — so the remark covers neither
the published law, nor the collapse channel added to it (the sum is again
state-dependent), but only the artificial case $\alpha=\beta=0$. The single
sentence "If $\Gam$ does not depend on the state" is present and honest, and I
credit that; the *title* and "Nothing is lost" are not. For $\alpha>0$, Jensen
on the convex $e^{\alpha f}$ gives $\mathbb E[\dot f_N] >$ the mean-field
right-hand side, so "the mean is the deterministic solution exactly at every
finite $N$" fails at $O(1/N)$ for the actual model.

**(b) The $N^{-1/2}$ claim is made for the wrong variable.** In the local
problem $\rho_I \propto (1-f)$. Under the exact binomial law the *survivor*
count is $\mathrm{Bin}(N,q)$, $q=e^{-\Lambda}$, whose relative standard
deviation is $\sqrt{(1-q)/(Nq)}$ and blows up as $s^{-g/2}/\sqrt N$. With
$g=1.5$:

| | $s=10^{-1}$ | $s=10^{-3}$ | $s=10^{-6}$ |
|---|---|---|---|
| $N=10^2$ | 0.55 | 17.8 | 3.16e3 |
| $N=10^4$ | 0.055 | 1.78 | 3.16e2 |
| $N=10^6$ | 0.0055 | 0.178 | 31.6 |

(expected survivors at $N=10^6$, $s=10^{-6}$: $10^{-3}$.) So there *is* a
boundary layer, in the one quantity the caustic analysis is about: the
deterministic $\rho_I\to0$ is not attained by any realization until the last
discrete unit converts, at a random time. `test_root_n_scaling...` sidesteps
this by restricting to $N(1-p)>5$ and
`test_variance_formula_is_exact_through_the_singularity` checks only the
identity $\mathrm{Var}=p(1-p)/N$, which is not in dispute.

**Fix**: retitle the remark ("A time change for a state-independent rate");
add one sentence saying it does not cover `asm:activation` with
$\alpha+\beta>0$; and add the $\sqrt{(1-q)/(Nq)}$ line, with the explicit
warning that the mean-field description of the *precursor* fails once
$Ne^{-\Lambda}\lesssim1$.

### M8. $b=0$ is required for regularity and $b>0$ is required for the paper's dark matter

**Location**: `eq:defects-regularity` vs. `sec:defects-abundance`
(11_defects.tex:257–263), `eq:cosmology-survival`.

Within one section, the manuscript establishes that the stress tensor is regular
at a caustic only if $b=0$, and then that the defect comoving abundance is
$\rho_{D,\rm act}+b\rho_{I,\rm act}$, i.e. that a non-trivial relic requires
$b>0$. The two halves of §11 pull in opposite directions and neither mentions
the other.

**Fix**: state the tension explicitly. It is a genuine (and interesting) result:
in this framework a defect dark matter produced by the conversion is
incompatible with regular caustics, whatever $\kappa$ is. Verified numerically —
`planar_scaling_table(kappa, b=0.25)` gives a divergent curvature invariant for
$\kappa=1.5,5,50$.

---

## Minor points

**m1.** Note §2(a): "the vacuum increases by exactly $\ln 100$ per two decades of
$s$". The coefficient is $(1-b)g\ln100$, not $\ln100$. Measured two-decade
increments: $(c,g,b)=(1,1,0)\to 4.605170$; $(1,1,0.25)\to 3.453878$;
$(2,2,0)\to 9.210340$; $(0.5,0.5,0)\to 2.302585$; all equal $(1-b)g\ln 100$ to
six digits. `test_vacuum_needs_a_strictly_stronger_condition` only exercises
$b=0$, $g=1$. Add the factor to the sentence, and a $b>0$ case to the test.

**m2.** The note's header says "The numerical checks are in
`code/tests/test_collapse.py` and `code/tests/test_pancake.py`".
**`code/tests/test_pancake.py` does not exist.** Nor does
`results/pancake.json`, which `scripts/run_pancake.py` is supposed to write —
only four of the twelve `.npz` files are archived. And `run_pancake.py:26`
cites "the refinement study" for $N=16384$; there is no refinement study in the
repository. I ran one ($n_{\rm steps}=5000$, $d_{\rm end}=1-10^{-6}$,
`rate_mode="none"`, fit over $s\in[10^{-5},10^{-4}]$):

| $N$ | 512 | 2048 | 8192 | 16384 (archived) |
|---|---|---|---|---|
| exponent | $-0.6157$ | $-0.9591$ | $-0.9973$ | $-0.99933$ |

so the convergence claim is **true and I certify it**, but it is not reproducible
from the repository as shipped. Add `test_pancake.py`, commit
`results/pancake.json`, and add the refinement table.

**m3.** The resolution-floor argument is **correct and I certify it
quantitatively**. The staggered grid puts the caustic sheet at $q=\Delta q/2$,
giving a floor $\epsilon = A k^2\Delta q^2/8 = \pi^2/(2N^2)$; the measured
$J(D{=}1)$ at the centre sheet is $1.8825{\rm e}{-}5$, $1.1765{\rm e}{-}6$,
$7.3534{\rm e}{-}8$ for $N=512,2048,8192$, matching $\pi^2/(2N^2)=
1.88248{\rm e}{-}5$, $1.17655{\rm e}{-}6$, $7.3534{\rm e}{-}8$. With
$\rho\propto(s+\epsilon)^{-1}$ the fitted slope should be
$-1+\epsilon\langle 1/s\rangle_{\log}$; for $N=16384$ over $[10^{-5},10^{-4}]$
that is $-1+7.2\times10^{-4}=-0.99928$ against the measured $-0.99933$. Put this
estimate in the paper — it is what makes the exponent trustworthy.

**m4.** 11_defects.tex:252 claims the control "reproduces $\rho_I=1/J$ to twelve
digits". I measure $|\rho_I J-1|$ at the caustic sheet at the final time:
$1.0\times10^{-13}$ at $N=512$, $n_{\rm steps}=5000$; $3.6\times10^{-11}$ at
$N=8192$, $n_{\rm steps}=5000$; $3.1\times10^{-11}$ at $N=4096$,
$n_{\rm steps}=25000$ — i.e. 10–11 digits at the production resolution, and the
error *grows* with $N$ at fixed step count (RK4 error $\propto$ the largest
$|\Theta|\sim1/\epsilon$). State the configuration and the norm, or weaken to
"ten digits".

**m5.** `run_pancake.py:58–62` computes `mass_residual` under the comment "dust
lost must equal vacuum gained when b = 0". **That identity is false.** With
$\dot V=(1-b)\Gamma\rho_I$ and no dilution term,
$\frac{d}{dt}\big[(\rho_I+\rho_D+V)|J|\big] = -b\Gamma\rho_I|J| + \Theta V|J|$,
so the sum is not conserved: the vacuum created is subsequently compressed at
constant density and the $pdV$ work is unaccounted. Measured at $N=4096$,
$n_{\rm steps}=25000$: residual $1.3\times10^{-14}$ for `none` (where it is just
dust conservation and therefore meaningless as a check of the conversion), but
$1.38\times10^{-1}$ for `collapse` $\kappa=1.5,b=0$, $1.04\times10^{-1}$ for
$b=0.25$, and $1.20\times10^{-1}$ for `cosmo`. This is physically correct
behaviour and a wrong diagnostic — but it means **there is currently no working
global conservation check on any run with conversion**. Replace it with
$\Delta\!\int(\rho+V)|J| = \int\!\!\int(\Theta V - b\Gamma\rho_I)|J|$, which is
exact and would actually validate the integrator.

**m6.** "Proper width" is used with three different meanings and the paper needs
one symbol per meaning: (i) the single-sheet slab thickness $\propto J\propto
s^{c}$, which is what `column_exponent` and note §2(b) use; (ii) the Lagrangian
thickness of the multi-stream slab, $\propto s^{1/2}$ (measured $2.83\times
10^{-3}$ at $s=10^{-6}$); (iii) the **Eulerian caustic width**, $\propto s^{3/2}$
(measured $1.886\times10^{-9}$ at $s=10^{-6}$, $5.29\times10^{-3}$ at
$s=2\times10^{-2}$, both matching $1.886\,s^{3/2}$). Note §3(ii) says the force
density "scales as $V/w$ with $w$ the caustic width" — if $w$ is (iii) the force
density goes as $s^{-3/2}$, not $s^{-c}=s^{-1}$. Related: the *acceleration*
$A^\nu = D^\nu V/\rho_I$ diverges faster still, as $s^{-3/2-(\kappa-1)}$ in the
regularized case, since $\rho_I\to0$ there. The manuscript quotes the milder of
the two; the acceleration is the quantity that decides whether the prescribed
Zel'dovich $\Theta$ can be maintained.

**m7.** `planar_scaling_table` (collapse.py:343–379) uses `float("inf")` as a
sentinel for "sector absent" and for "velocity is bounded", and then special-
cases `finite=True` for it. No current test passes for the wrong reason, but
`min(out["precursor density"], out["defect density"])` for the curvature row is
fragile under this convention, and the `finite` flag for the curvature row is
hardcoded rather than derived from the exponent. Use `None` and a separate
`present` field.

**m8.** `test_bounded_rate_is_the_paper_s_case` uses $\alpha=2,\beta=1$, bound
$e^3\approx20$. The manuscript's prior is `alpha_tot` $\in[0,8]$
(`params.py:59`), so the bound is $\Gamma_0e^8\approx 2981\,\Gamma_0$ and the
crossover sits at $s^*=e^{-G(T-t_0)}$, i.e. below $e^{-2981}$ — utterly
unreachable physically. This *strengthens* Theorem A's practical relevance (the
bounded rate wins over any observationally accessible range of $s$) and the
paper should say so rather than leaving the reader with the $e^3$ example.

**m9.** `SelfSimilarScaling`: with cosmological expansion $\ell_i = a(t)
\lambda_i(s)$, so $E_{\rm core}\sim a(T)^Q s^{Q-p}$. Since the caustic forms at
finite $T$ with $a(T)$ finite and non-zero, the exponents are unchanged and the
claim "$E_{\rm core}\sim s^{Q-p}$, finite iff $Q\ge p$" survives — **certified**,
but the docstring should say why (a bounded, non-vanishing prefactor), because a
referee will otherwise ask.

**m10.** Note §5, "expansion $\Theta$: diverges" and
`test_expansion_always_diverges`. This is a tautology of the prescription
$\Theta=-c/(T-t)$, not a result. Its stated significance
("what conversion can remove is the gravitational effect of the caustic, not the
caustic of the congruence") appears only in a test docstring
(test_collapse.py:279–283). Promote it into the paper, and say the words: a
caustic of the congruence is a singularity of the *flow*, not of the spacetime.

**m11.** Claims-ladder discipline. `eq:defects-regularity` is registered at level
C, whose definition is "the hypotheses are named in the statement". The displayed
equation names none of them (prescribed self-similar $\Theta$; a single flow
line; no back-reaction of $V$ or of $D^\nu V$ on $\Theta$; $\rho_D$ pressureless
and comoving). `eq:process-binomial` likewise omits state-independence from the
display. Either put the hypotheses in the display or demote.

**m12.** `test_defects_inherit_the_divergence` asserts the column tends to
$b\times1.0$. The exact solution is $\rho_D s^c = b\,(s_0^{\,g}-s^{\,g})\to
b\,s_0^{\,g}$, i.e. it depends on the arbitrary initial gap $s_0$ (=1 here). I
verified $0.250000$, $1.000000$, $0.500000$ for $(c,g,b)=(1,2,.25),(1,3,1),
(2,4,.5)$. "Finite" is right; "$=b$" is an artefact of $s_0=1$. Worth one word
in the docstring.

---

## What I checked and certify

For the record, and because the template asks for it:

- **Theorem A, and the necessity of $T-\tau_0<\infty$.** The hypothesis *is*
  stated, in both the note and 11_defects.tex:172 — good. It is genuinely
  needed: with $\Theta=-1/\tau$ on $[1,\infty)$ (so $\int\Theta=-\infty$) and a
  *bounded* $\Gamma=0.1$, I get $\int_1^\tau(\Theta+\Gamma)= -1.40, +5.29,
  +990.7, +99986.1$ at $\tau=10,10^2,10^4,10^6$, so $\rho_I\to0$: a bounded rate
  *does* regularize a non-integrable compression over infinite proper time.
  Add one sentence saying this, so the reader sees the hypothesis is not decorative.
- **Boundedness of the constant-$\Gamma_0$ rate**: $f,M,S_{\rm act}\in[0,1]$ all
  verified from the equations and from `background.py`; $\Gamma\le\Gamma_0
  e^{\alpha+\beta}$ holds. (See M4 for the family it does not cover.)
- **The three regularity conditions.** $\rho_I$ finite iff $g\ge c$; vacuum
  source exponent $g-c-1$ and hence $g>c$ strictly, with a logarithm at $g=c$
  (coefficient corrected in m1); $\rho_D$: I solved it exactly,
  $\rho_D = b(s_0^{\,g}-s^{\,g})s^{-c}\to b s_0^{\,g}s^{-c}$, confirming
  divergence for **every** $g>0$ when $b>0$, and confirmed it numerically
  (column $\to 0.250000$, $1.000000$, $0.500000$). Certified.
- **The $\kappa>1$ threshold, including robustness to corrections in $\Theta$.**
  $g=\kappa c$ and $g>c\iff\kappa>1$ independent of $c$: certified. With
  $\Theta=-c/s + A\ln(1/s)$ and $A=0,+5,-5$, the measured
  $\mathrm{d}\ln\rho_I/\mathrm{d}\ln s$ between $s=10^{-6}$ and $10^{-8}$ is
  $-0.1000/+0.0000/+0.1000/+0.5000$ for $\kappa=0.9/1.0/1.1/1.5$ in every case —
  the threshold is insensitive to subleading corrections. Certified.
- **The pancake exponents.** From the archived runs, fitted on
  $s\in[10^{-5},10^{-4}]$: `A_none` $-0.9993$, `B_cosmo` $-0.9989$ (bounded rate
  lowers the amplitude from $9.82\times10^5$ to $3.58\times10^3$ but not the
  exponent — Theorem A, as advertised), `C_collapse_k0p5` $-0.4992$ (predicted
  $\kappa-1=-0.5$), `C_collapse_k1p5` $+0.5002$ (predicted $+0.5$). Certified.
- **The test suite.** `pytest tests/test_collapse.py`: **29 passed** in 7.2 s
  (one `IntegrationWarning` from `quad` in
  `test_bounded_rate_is_the_paper_s_case`, harmless but worth silencing with the
  `points=` argument the module already supports).
- **Dust-to-dust covariance** and the exactness of `eq:defects-local-exact`:
  certified (see M5(i)).

I did not run the full test suite, the MCMC, or a self-gravitating sheet
calculation. Everything above was single-threaded, under 20 s per run, peak RSS
39 MB.

---

## Questions the authors must answer

**Q1.** Which notion of singularity is being regularized? Please give the Tipler
strong-curvature integral for $c=1$ and for $c\ge2$, with and without the
conversion channel. If the generic caustic is Tipler-weak and the spacetime
extendible, say so — it reframes the whole section, and in my view improves it.

**Q2.** Define $w$ in "the force density $D^\nu V$ scales as $V/w$". Is it the
sheet thickness ($\propto s$), the Lagrangian slab ($\propto s^{1/2}$) or the
Eulerian caustic width ($\propto s^{3/2}$)? And why is the force *density*, and
not the acceleration $D^\nu V/\rho_I$, the right diagnostic when $\rho_I\to0$ in
exactly the case you call regular?

**Q3.** Which sign does $\rho_I A^\nu = D^\nu V$ give? Does the induced
acceleration oppose or enhance the collapse? If it enhances it, the $\kappa>1$
branch is self-defeating and that should be recorded alongside "no
self-consistent solution is exhibited".

**Q4.** For $\kappa>1$ the converted fraction reaches $f=1$ *before* the caustic
(`converted_fraction_singular`: $1-f=(s/s_0)^{g}\to0$). The Zel'dovich
trajectories are the trajectories of the dust. In what sense is there still a
caustic to regularize once all the dust has become vacuum, and what carries
$\Theta=-c/(T-t)$ then?

**Q5.** How does the $\xi H$ family behave at a caustic (M4), and where does the
fitted $\xi_0$ posterior sit relative to $\xi_0=3$?

**Q6.** Does the four-form/membrane realization of §8 evade Theorem C(ii),
given that its transfer is supported on a hypersurface rather than being a
smooth $D^\nu V$?
