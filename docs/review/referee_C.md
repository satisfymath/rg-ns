# Referee report

**Manuscript**: Self-reinforced geometric absorption
**Referee**: C (mathematical relativist / mimetic gravity, solitons)
**Round**: 1
**Date**: 2026-09-09

## Summary (3 lines)

A dark-sector precursor converts irreversibly into pressureless defects and an
exact vacuum at a rate that is reinforced by the converted fraction and by an
exponentially-lagged memory of it; the paper derives the deterministic limit of
the underlying jump process, couples it to FLRW, and proves positivity, a de
Sitter attractor, a jerk inequality $j\ge 1+2\Omega_r$, a snap relation carrying
the memory, and a linear growth system in which the branching ratio cancels.
Covariant realizations (four-form, constrained mimetic clock), a solved Skyrme
defect and a collective Lindblad model are offered as existence proofs for the
ingredients, and the background is fitted to Pantheon+/DESI/CC/CMB priors.

## Recommendation

[ ] Accept  [ ] Minor revision  [x] Major revision  [ ] Reject

The framework is carefully built and unusually honest about its own limits in
most places. But several displayed results are stated with hypotheses that are
not the ones their proofs use, one headline result (the memory fingerprint) is
invalidated by a term dropped from the rate law, and the one genuinely
unresolved structural problem in the perturbation sector — which the authors'
own supporting note states plainly — has been removed in condensation. These
are fixable, and most of the fixes are short.

## What I checked and found sound

So that the major points below are read in proportion, the following were
checked line by line or re-run, and are correct.

- **`thm:jerk`.** $j=1+3\dot H/H^2+\ddot H/H^3$, $j=1-\dot p_{\rm tot}/(2M_{\rm
  Pl}^2H^3)$, and with $p_{\rm tot}=\rho_r/3-V$ the assembly into
  $j=1+2\Omega_r+\varepsilon$ is right, as is the inversion
  $Q_V=2M_{\rm Pl}^2(\ddot H+3H\dot H)-\tfrac43H\rho_r$ used in §7.2.
  `absorb/symbolic.check_jerk_identity()` returns `True`.
- **`thm:sandwich`.** Both inequalities hold. The upper bound is
  $3M_{\rm Pl}^2(H^2_{\rm high}-H^2)=\int_{t_e}^{t}Q_Va'^3(a^{-3}-1)\,dt'
  +\int_{t}^{t_0}Q_V(1-a'^3)\,dt'$, and both terms are non-negative for
  $a\le1$ and vanish at $a=1$ (see m6 on the proof text).
- **`cor:one-transition`.** $\mathcal A=(2V-\rho_m-2\rho_r)/(6M_{\rm Pl}^2)$ and
  $\dot{\mathcal A}=(3Q_V+3H\rho_m+8H\rho_r)/(6M_{\rm Pl}^2)$ — correct.
- **`thm:quasi-positivity`** and `app:proofs-positivity`. The integral-form
  argument is the right one and does hold for merely locally integrable
  $\Gamma$; the Nagumo language is decoration but not wrong.
- **`prop:four-form`.** The contractions
  $\epsilon_{\mu\alpha\beta\gamma}\epsilon_\nu{}^{\alpha\beta\gamma}=-3!\,g_{\mu\nu}$,
  $\epsilon^2=-4!$, and hence $T_{\mu\nu}=-h^2g_{\mu\nu}+\tfrac12h^2g_{\mu\nu}
  =-(h^2/2)g_{\mu\nu}$, $\rho_4=+h^2/2$, are correct in $(-+++)$.
  `absorb/symbolic.check_four_form()` returns `True` and verifies
  $\mathcal H^2=-24h^2$ and $T_{\mu\nu}=-(h^2/2)g_{\mu\nu}$ on a general
  diagonal metric. The polarization count is right: a massless $p$-form has
  $\binom{D-2}{p}$ physical polarizations, so $\binom{2}{3}=0$ at $D=4$.
  Crucially, the proof varies the metric *before* imposing $\mathcal H=h\epsilon$,
  which is exactly the step at which the sign of the induced $\Lambda$ is
  usually lost; the authors get it right (see m14).
- **`prop:clock`.** $T_{\mu\nu}=\lambda\,\partial_\mu T\partial_\nu T+g_{\mu\nu}
  \mathcal L|_{\rm on-shell}=\lambda u_\mu u_\nu-Vg_{\mu\nu}$, geodesy from the
  symmetry of $\nabla_\mu\nabla_\nu T$, and $\nabla_\mu(\lambda u^\mu)=-V_{,T}$
  are all correct. `check_clock_action()` returns `True`.
- **§9.1 integrability.** The step from "no spatial force in $u$",
  $-\nabla^\nu V=Q_Vu^\nu$, to $\nabla_{[\mu}(Q_Vu_{\nu]})=0$ is correct: the
  one-form $Q_Vu_\mu=-\partial_\mu V$ is exact, hence closed. With
  $u_\mu=-\partial_\mu T$ this is $dQ_V\wedge dT=0$, and since the constraint
  $(\partial T)^2=-1$ guarantees $dT\ne0$ everywhere, $Q_V=Q_V(T)$ follows
  locally by Frobenius. The logic is right. The caveat is not innocent — see M7(c).
- **§9.2–9.3 algebra.** I re-derived
  $\dot\delta_m=-\vartheta+\gamma_c\delta_m$,
  `eq:perturbations-growth`, its $N$-form,
  $f_{\rm RSD}=d\ln\delta_m/d\ln a-g_c$, the first-order matter-domination
  coefficients $(2n+3)/(2n+5)$ and $-2/(2n+5)$ (with $n$ the log-slope of
  $g_c$; see m13), and
  $d\ln\Phi/d\ln a=2+d\ln\bar\rho_m/dN+d\ln\delta_m/dN=f_{\rm RSD}-1$.
  All correct, including the non-obvious ISW factor $2/(2p+5)$ and the fact
  that it is $f_{\rm RSD}$, not $f_g$, that appears there.
  `check_growth_equation()` returns `True`.
- **`prop:derrick` and App E.** The Derrick scaling
  $E(\sigma)=\sigma^{-1}E_2+\sigma^{-3}E_0$ is right. The Bogomolny step is
  correct: with $X=\sigma_1\sigma_2\sigma_3$, AM–GM gives
  $\tfrac12F_*^2\sum\sigma_i^2\ge\tfrac32F_*^2X^{2/3}$ and
  $\kappa_s\sum_{i<j}\sigma_i^2\sigma_j^2\ge3\kappa_sX^{4/3}$, and AM–GM on
  those two gives $2\sqrt{\tfrac92F_*^2\kappa_s}\,X=3\sqrt2F_*\sqrt{\kappa_s}X$,
  which integrates to $6\sqrt2\pi^2F_*\sqrt{\kappa_s}|B|$ using
  $\int X=2\pi^2|B|$. The trial-family quadratures
  ($E=6\pi^2(F_*^2R_s+\kappa_s/R_s)$, $E_{\rm trial}=12\pi^2F_*\sqrt{\kappa_s}$)
  also check out.
- **The solved defect.** `absorb.skyrme.solve_hedgehog()` gives
  $E_2=51.5645537459$, $E_4=51.5645537546$, $\tilde E=103.129107$,
  $B=0.9999999958$ ($1.0000000964$ by independent quadrature), virial residual
  $-8.5\times10^{-11}$. `bogomolny_bound()` $=83.74637=6\sqrt2\pi^2$;
  `trial_energy(1.0)` $=118.43525=12\pi^2$. So
  $E/E_{\rm Bog}=1.23144$ (the standard Skyrme $1.232$) and
  $E/E_{\rm trial}=0.87076$. Every number in `eq:defects-solved` and
  `fig:skyrmion` reproduces. §11.3 is also honest about what a hedgehog minimum
  does and does not prove ("not a proof of stability against all deformations:
  that would require the full Hessian") — that paragraph is exactly right and I
  have no complaint about it.
- **`prop:classical-reduction`, population sector.** Correct. $L_i$ maps each
  occupation basis state to a single basis state and $L_i^\dagger L_i$ is
  diagonal, so the diagonal block is closed; and a coherence $|n\rangle\langle m|$
  with $n\ne m$ can only map to $|n'\rangle\langle m'|$ with $n'\ne m'$ (the
  dangerous case $m=n+e_i$ is killed because $L_i|m\rangle=0$). The reduced
  chain rate $(N-k)\Gamma_0e^{\alpha k/(N-1)}$ is right for *any* diagonal
  state, not only symmetric ones. `lindblad.populations_decouple(4, alpha=1.0)`
  returns `True`. See m9 for the coherence half of the statement.
- **`prop:unitary-obstruction`, `prop:no-rolling`, `check_solvable_family()`,
  `check_flrw()`** — all fine.

## Major points

### M1. `thm:snap`, `eq:cosmography-snap-explicit`, `thm:memory-fingerprint`: the activation factor has been dropped from $d\ln\Gamma/dN$, and it is exactly degenerate with the memory term

**Location.** §7.3, `eq:cosmography-snap-explicit`, `eq:cosmography-fingerprint`;
propagated to the abstract ("the $(j_0,s_0)$ plane is their cosmographic
fingerprint"), §1.4 item 4, and §14.

`eq:cosmography-snap` is correct:
$s-s_{\Lambda\rm CDM}=\varepsilon[d\ln\Gamma/dN-\Gamma/H-2]$. The explicit form
is then obtained for $\Gamma=\Gamma_0e^{\alpha f+\beta M}$ — that is, for the
rate law *without* the activation switch, which is the law the paper's own
`thm:no-go` has just proved inadmissible. For the rate law actually adopted
(`eq:process-rate` / `asm:activation`, which carries $S_{\rm act}(a)$),

$$\frac{d\ln\Gamma}{dN}=\alpha(1-f)\frac{\Gamma}{H}+\mathcal B+p\,[1-S(a)]
\quad(+\ \text{a further }-(1+q)\ \text{if}\ \Gamma\propto H,\ \text{see M4}),$$

so the bracket is
$-\varepsilon\big[2+(1-\alpha(1-f))\Gamma/H-\mathcal B-p(1-S)\big]$ and not
what is printed.

Two consequences.

(a) *Quantitative.* $p(1-S)=p\,a_{\rm act}^p/(a^p+a_{\rm act}^p)$. With the
paper's own reference values $p=6$, $z_{\rm act}=1$: $p(1-S)=0.092$ at $z=0$,
$0.70$ at $z=0.43$, and $3.0$ at $z=z_{\rm act}$ — the last being larger than
the retained constant $2$. The omitted term is not a correction, it dominates
near activation. The two "limits that check the statement" at the end of §7.3
("without memory the snap excess is strictly negative for $\alpha(1-f)\le1$")
also fail once it is restored.

(b) *Structural, and this is the serious one.* In the corrected bracket
$\mathcal B$ and $p(1-S)$ appear with the **identical coefficient** $-1$. Hence
$\partial s_0/\partial\mathcal B=\partial s_0/\partial[p(1-S_0)]=+\varepsilon_0$:
the snap measures the combination $\mathcal B_0+p(1-S_0)$ and cannot separate
the memory lag from the activation slope. The displayed partial derivatives in
`eq:cosmography-fingerprint` remain true as partial derivatives, but the
proof's non-degeneracy argument ("the coefficient of $\Gamma/H$ is
$1-\alpha(1-f)$ while that of $\mathcal B$ is $-1$, and these are independent
directions") is incomplete, and the claim that $(j_0,s_0)$ is *the memory
parameters'* fingerprint is not established. As it stands the abstract
overstates a result that the manuscript's own rate law contradicts.

This is a condensation loss, not an error of the underlying work:
`docs/theory/04_cosmography.md` (lines 268–270, 304–307) has both extra terms
written out. They were dropped on the way into the paper.

**Fix.** Restore $p[1-S(a)]$ (and $-(1+q)$ if the expansion-tracking
normalization is intended) in `eq:cosmography-snap-explicit`. Restate
`thm:memory-fingerprint` as a statement about the combination
$\mathcal B_0+p(1-S_0)$, or add the hypothesis that $(p,a_{\rm act})$ are fixed
independently — and say so in the abstract. Also delete or qualify the claim in
§6.3 that "all results of `sec:positivity-ide`, `sec:cosmography`,
`sec:perturbations` survive verbatim, because each needs only $\Gamma\ge0$":
`eq:cosmography-snap-explicit`, `eq:cosmography-fingerprint` and
`eq:perturbations-growth-signature` do not.

### M2. `eq:cosmography-deficit-floor`: the monotonicity hypothesis is misstated, and as printed the bound is false

**Location.** §7.1, the paragraph containing `eq:cosmography-deficit-floor`.

The text says: "if the transfer is switching on, so that $Q_Va^3/H$ is
non-decreasing, then the matter deficit sets a floor, $j_0-1\ge2\Omega_{r0}
+\tfrac92\Delta$", and "if $Q_Va^3/H\propto a^{p_{\rm eff}}$ near today the
relation is exact, $\varepsilon_0=\tfrac32(p_{\rm eff}+3)\Delta$".

With $q\equiv Q_V/(3M_{\rm Pl}^2H_0^2H)$ one has
$\Delta=\int_{-\infty}^{0}q\,e^{3N}dN$ and $\varepsilon_0=\tfrac32q_0$. The
floor requires $\Delta\le q_0/3$, which follows from $q\le q_0$, i.e. from
**$Q_V/H$** non-decreasing — the extra $a^3$ belongs to the measure $e^{3N}dN$,
not to the monotone quantity.

The printed pair of statements is internally inconsistent, which can be seen
without leaving the paper: if the monotone/power-law object were really
$Q_Va^3/H\propto a^{p_{\rm eff}}$ then the exact relation would be
$\varepsilon_0=\tfrac32p_{\rm eff}\Delta$, and the floor $\tfrac92\Delta$ would
correspond to $p_{\rm eff}=3$, not to the boundary case $p_{\rm eff}=0$ of a
"switching on" transfer.

Under the hypothesis as printed the bound is false. Counterexample:
$Q_V/H\propto a^{-2}$, so $Q_Va^3/H\propto a$ is non-decreasing as required.
Then $\Delta=\int_{-\infty}^{0}e^{-2N}e^{3N}dN=1$ in units of $q_0=1$, while
$\varepsilon_0=1.5$ and $\tfrac92\Delta=4.5$: the claimed floor is violated by a
factor of three (I checked this numerically as well).

`docs/theory/04_cosmography.md` Prop. 1.5 states the hypothesis correctly on
$q=Q_V/(3M_{\rm Pl}^2H_0^2H)$; the $a^3$ was introduced in condensation.

**Fix.** Replace "$Q_Va^3/H$" by "$Q_V/H$" in both places. Since this is called
"the model's tightest internal consistency test", it should also be stated
whether the model's own $Q_V/H$ is in fact monotone over the fitted range, and
over what range.

### M3. `asm:geodesic` conceals a known over-determination that the supporting note states explicitly

**Location.** §9.1, `asm:geodesic`; everything in §9 depends on it.

`asm:geodesic` says: "the rate law `eq:process-rate` then applies to the
background mode, and the perturbations of the kinetic variables are slaved,
$\delta\Gamma/\bar\Gamma=-\delta_I$, with $\delta f$ and $\delta M$ following by
integration."

That last clause is not true, and the authors know it. The slaving is forced by
$\delta Q_{V,\rm com}=0$ with $Q_V=(1-b)\Gamma\rho_I$. But $\Gamma$ is a
function of $(f,M,a)$ only, so on comoving slices the slaving reads
$\alpha\,\delta f+\beta\,\delta M=-\delta_I$ — an *algebraic* constraint — while
$\delta f$ and $\delta M$ separately obey
$\delta\dot f=-\bar\Gamma\delta f+(1-\bar f)\delta\Gamma$ and
$\tau_M\delta\dot M=\delta f-\delta M$. That is three conditions on two
unknowns. Differentiating the algebraic constraint and substituting the two
evolution equations yields a compatibility condition which is not an identity of
the dust sector, so the system is over-determined by one and "$\delta f$ and
$\delta M$ follow by integration" is precisely what cannot be done.

`docs/theory/03_perturbations.md` says this in as many words: "Equations (1.6)
and (1.7) are *three* conditions on *two* unknowns $(\delta f,\delta M)$: the
system is overdetermined by one … which is not identically satisfied by the dust
dynamics", and it then restates the assumption in a self-consistent form in which
$(f,M)$ are demoted to *diagnostic* variables reconstructed from the constraint
plus whichever evolution equation one chooses to retain, with the residual issue
recorded as open ("an unresolved structural issue"). None of that survives into
the manuscript. What the reader is shown instead is a sentence implying that the
kinetic sector consistently extends off the background.

I do not think this sinks §9 — the point made in the note, that the dust sector
closes on $(\delta_m,\vartheta)$ and sees the kinetics only through
$\bar Q_V$, is correct, and `thm:b-independence` and `eq:perturbations-growth`
are right (I re-derived them). But the paper is elsewhere scrupulous about
labelling assumptions, and this is the one place where a known structural cost
has been silently removed. Given that the model's headline linear prediction
(`eq:perturbations-growth-signature`) rests on it, it must be stated.

**Fix.** Import the note's formulation verbatim: state `asm:geodesic` as
*defining* the theory by $\delta Q_{V,\rm com}=0$, state that the kinetic
variables are thereby diagnostic rather than dynamical at first order, state the
over-determination, and state (with the one-line argument) that no linear
observable depends on which of the kinetic equations is retained.

### M4. Two different rate normalizations are in circulation, and several results are inherited from the one that is not displayed

**Location.** `eq:process-rate` (§3.1), `eq:solvable-activation` /
`prop:activation` (§6.3), `eq:cosmography-snap-explicit` (§7.3),
`eq:perturbations-growth-signature` (§9.3), `app:numerics`.

The manuscript displays $\Gamma=\Gamma_0S_{\rm act}(a)e^{\alpha f+\beta M}$ with
**constant** $\Gamma_0$. Several results, however, are the results for
$\Gamma=\xi_0H\,S_{\rm act}(a)e^{\alpha f+\beta M}$:

- `prop:activation`'s sufficient condition is written in terms of $\xi_0$ and
  $\mathcal I_{S}=\int_0^1S(a)a^{-4}da$. That integral is exactly
  $\int\Gamma\rho_I\,dt$ for $\Gamma\propto H$ (the $H$ cancels against
  $dt=da/(aH)$). For constant $\Gamma_0$ one gets $\int S(a)a^{-4}\,H_0/H\,da$,
  and with $H\propto a^{-2}$ (radiation) or $a^{-3/2}$ (matter) the convergence
  requirement is $p>1$ or $p>3/2$, **not** $p>3$. The sentence "The exponent
  condition $p>3$ is exactly the requirement that the integral generating the
  vacuum converge; it is the analytic content of the repair" is therefore
  correct only for the undisplayed rate.
- `eq:perturbations-growth-signature` assumes "$g_c\propto a^p$ inherited from
  the activation switch". True for $\Gamma\propto HS$; for constant $\Gamma_0$,
  $g_c=Q_V/(H\rho_m)\propto S(a)/H\propto a^{p+3/2}$ in matter domination, which
  turns $2/(2p+5)$ into $2/(2p+8)$ — a 17% change in the ISW amplitude at $p=6$.
- §6.3's two numerical statements mix the two: "$p=6$ … conversion rate at
  recombination below $10^{-21}$ of the expansion rate" is the constant-$\Gamma_0$
  number ($S(10^{-3})\simeq6\times10^{-17}$ divided by $H/H_0\simeq3\times10^4$),
  while the very next sentence says "$p=2$ fails this test **for the
  expansion-tracking form** of the rate, by nine orders of magnitude".
- `code/absorb/background.py` implements both behind a flag ("If True the rate is
  Gamma = xi H rather than a constant floor"), so the ambiguity is real and not
  merely typographical, and it determines which chains in §10 mean what.

**Fix.** Choose one normalization as primary, display it once, and for every
subsequent numbered result either derive it for that rate or state explicitly
which rate it belongs to. A single line in `app:conventions` will not do —
`prop:activation`, `eq:cosmography-snap-explicit` and
`eq:perturbations-growth-signature` each need the choice made in place.

### M5. `thm:hysteresis`: the final conclusion is false under the paper's own hypotheses

**Location.** §3.4, `thm:hysteresis`, last clause: "and the asymptotic converted
fractions differ."

Under `asm:activation`, $S_{\rm act}(a)\to1$ as $a\to\infty$, so
$\Gamma\ge\Gamma_0S_{\rm act}\to\Gamma_0>0$ and $\int^\infty\Gamma\,dt=\infty$ —
which is also exactly the hypothesis of `thm:de-sitter`'s second alternative. By
`prop:survival`, $f\to1$ if and only if $\int^\infty\Gamma\,dt$ diverges.
Therefore both histories have $f\to1$: the asymptotic converted fractions are
**equal**, not different.

The comparison part of the theorem (Kamke–Müller ordering from the cooperativity
of the $(f,M)$ system) is correct, and so is the physical claim the paper wants:
what genuinely differs is the asymptotic *vacuum density*, because by
`eq:cosmology-dVdf` the same amount of conversion deposits different energy
depending on when it happens. That is what `fig:hysteresis` and the code report
(`\numHysteresisRelativeDeltaVacuum` $=0.0073$), and it is what §14 should be
claiming.

**Fix.** Replace "the asymptotic converted fractions differ" by "the asymptotic
vacuum densities differ", with the pointer to `eq:cosmology-dVdf`; or, if a
statement about $f$ is wanted, restrict it to finite times ($f^{(1)}(t)>f^{(2)}(t)$
for all $t>t_*$) and say that both saturate.

### M6. The promised restatement of `thm:regular-future` / `thm:de-sitter` "for $t\ge t_{\rm act}$" does not exist, and the domain claims do not match the use

**Location.** §6.2 last sentence; `thm:regular-future`, `thm:de-sitter` (§4.3,
§4.4); `app:conventions-domain`.

§6.2 states: "`thm:regular-future`, `thm:de-sitter` are restated here for
$t\ge t_{\rm act}$, which is all they are used for." The string $t_{\rm act}$
occurs **exactly once in the whole manuscript** — in that sentence. No
restatement appears. Both theorems as printed are stated from a generic $t_i$
with $a_i=1$, with no activation hypothesis anywhere in them.

The repair to the *rate* hypothesis was genuinely made and is correct:
`thm:de-sitter` now assumes $\int^\infty\Gamma\,dt=\infty$ rather than a floor
$\Gamma\ge g>0$, which is the right weakening (and is satisfied by
`asm:activation`), and `thm:regular-future` needs only $0\le\Gamma\le G$ with
local Lipschitz continuity. So the substance of the repair is there. What is
missing is the domain bookkeeping the paper claims to have done, and it is not
cosmetic:

- Both proofs use $a\ge1$ (the vacuum bound $V_i\le V\le V_i+(1-b)\rho_{I,i}$
  depends on it). Taking $t_i=t_{\rm act}$ therefore normalizes $a=1$ **at
  activation**, whereas $\Delta$, the $\Omega$'s, `eq:positivity-deficit`,
  `eq:cosmography-deficit-floor` and all of §10 normalize $a_0=1$. With
  $z_{\rm act}=1$ these differ by a factor of two in $a$ and eight in the
  comoving densities appearing in `eq:cosmology-bounds`. A reader cannot
  currently tell which normalization each bound is in.
- `app:conventions-domain` says the theorems of §4–§5 "hold to the future of
  activation", but `thm:sandwich` is applied on $[a_e,1]$ with $a_e$ early,
  `eq:positivity-deficit` integrates from $t_e$, `eq:cosmography-deficit-floor`
  integrates from $N=-\infty$, and §10.1 evaluates the sound horizon at the
  *pre-activation* matter density. So the stated domain is simultaneously too
  narrow for §5/§7/§10 and stronger than what the proofs need
  (`thm:quasi-positivity` needs only $\Gamma\ge0$ locally integrable, on any
  interval).
- `prop:determined-V` (§8.4) invokes `thm:regular-future` — a theorem whose name,
  statement and proof are about the *future* — to assert uniqueness of the
  background and boundedness of $V(T)$ for $T<t_0$, i.e. in the past.
  (Backward uniqueness does hold for a locally Lipschitz field, but the bound
  $V\le V_i+(1-b)\rho_{I,i}$ does not follow from `eq:cosmology-bounds` in that
  direction; the past bound is `prop:activation`.)

**Fix.** Either actually restate the two theorems in §6 with $t_i=t_{\rm act}$,
$a_{\rm act}$ explicit and the normalization stated, or delete the claim and
instead attach to each theorem the interval on which it is used. Correct
`app:conventions-domain` to the hypotheses the proofs use rather than to
activation. Point `prop:determined-V` at `prop:activation` for the past bound.

### M7. Mimetic pathologies: two are confronted, the third is answered for a different theory, and the vanishing sound speed is banked twice

**Location.** §8.4 (final two paragraphs), §9.1, §9.4 `prop:no-instability`, §13.

The three known problems of Lim–Sawicki–Vikman / mimetic-with-potential are
named honestly in §1.3 and §8.4, which is more than most papers in this area do.
But the treatment does not hold up on inspection.

(a) **$c_s^2=0$ is used as a pathology in §8.4 and as a virtue in §9.4.** §8.4:
"The scalar sound speed vanishes identically, so there is no scalar sound
horizon." §9.4, `prop:no-instability`: the system "contains no independent
dark-energy degree of freedom, no pressure perturbation, and no $k$-dependent
coefficient. Its coefficients are of order $H$ and $H^2$, so $|\delta_m|$ is
bounded by a power of $a$ on every scale." These are the same fact. The absence
of a $k$-dependent coefficient *is* $c_s^2=0$, and it means there is no
restoring force at any wavelength: the linear system is degenerate rather than
hyperbolic in the scalar sector, and "bounded on every scale" carries no
information about the ultraviolet, because the linear description ceases to hold
at arbitrarily small scales at arbitrarily early times. The paper should say
that `prop:no-instability` establishes the absence of the *Väliviita–Majerotto–
Maartens* super-horizon instability specific to coupled fluids with a sound
speed, and nothing more; it should not be allowed to read as a statement of
stability of the mimetic sector.

(b) **The gradient-instability disclaimer is made for an action that does not
realize §9.** §8.4 argues that `eq:realizations-clock-action` "contains no
higher-derivative term of the form $(\Box T)^2$, so the gradient instabilities
identified by Ijjas et al. in extended mimetic models are absent here". For that
action, correct. But that action does *not* produce the perturbation theory of
§9: its own perturbations give $\delta V_{\rm com}=0$ with $V_{,T}$ an arbitrary
function of $T$ and no rate law at all, whereas §9 additionally requires
$\delta\Gamma/\bar\Gamma=-\delta_I$ with $\Gamma$ built from $(f,M,a)$ — a
relation that is not a consequence of `eq:realizations-clock-action` and that,
by M3, is over-determined. So the theory whose gradient stability has been
argued for is not the theory whose growth and ISW predictions are being fitted
in §10. This needs to be said plainly, and the fitted theory's scalar sector
needs its own statement.

(c) **Caustics are treated as remote, but the paper's own regularity caveat says
they are not.** §9.1 concludes that "$Q_V$ and $\rho_V$ are functions of $T$
alone **wherever the clock is regular**". That caveat is doing real work: the
constraint $(\partial T)^2=-1$ guarantees $dT\ne0$, so the *only* way the
Frobenius step can fail is at a caustic of the congruence, where the level sets
of $T$ self-intersect and $T$ ceases to be a coordinate. Caustics are therefore
not a distant nonlinear question about the theory in general — they are exactly
the locus on which `eq:perturbations-com`, and hence every result of §9 and every
fit in §10 that uses $f\sigma_8$ or the ISW amplitude, is undefined. Deferring
them to `sec:outlook` while using the prescription globally is the one place in
the paper where a hard problem is evaded by placement rather than confronted.

(d) **`prop:clumping-unstable` is a one-sided exclusion presented as a
dichotomy.** It shows that $\delta V_{\rm com}=\zeta\delta_I$ with $\zeta>0$ has
$c_{s,\rm eff}^2=-\zeta/\bar\rho_I<0$ and is ill-posed. It says nothing about
$\zeta<0$, which gives $c_s^2>0$ and is not excluded, nor about the other
extensions the draft listed (momentum transfer with a compensating force; a
genuine dark-energy sector with $c_s^2>0$). The supporting note says exactly
this. The manuscript's "the natural alternative is unstable" should become "the
$\zeta>0$ alternative is unstable; $\zeta<0$ and the momentum-transfer options
are different theories, not excluded here".

**Fix.** Rewrite the last two paragraphs of §8.4 and the last paragraph of §9.4
so that (i) $c_s^2=0$ is identified as the single fact underlying both the "no
sound horizon" concession and the "no $k$-dependence" stability claim; (ii) the
gradient-stability statement is explicitly scoped to
`eq:realizations-clock-action` and *not* to the transfer prescription of §9;
(iii) the caustic caveat in §9.1 is quantified — state the range of $(k,z)$ over
which the authors claim the clock congruence is caustic-free and confirm that
the data used in §10 lie inside it; (iv) `prop:clumping-unstable` is stated as
excluding one branch.

### M8. §12.3: the quoted closure exponent $-1.190$ is a small-$N$ artefact, and the paper's own code produces the right number

**Location.** §12.3, `\numLindbladClosureSlope`, `fig:lindblad`.

The text says the closure error "scales as a power of $N$ with fitted exponent
$-1.190$, consistent with the expected $\mathcal O(N^{-1})$", and claims the
computation used "the full Liouvillian for $N\le8$ **and the
permutation-symmetric chain far beyond that**". The figure caption says
$N=2$ to $8$.

I reproduce $-1.1909$ from the full Liouvillian over $N=2\ldots8$
(errors $3.843\times10^{-2}$, $2.206\times10^{-2}$, $1.562\times10^{-2}$,
$1.212\times10^{-2}$, $9.905\times10^{-3}$, $8.388\times10^{-3}$,
$7.277\times10^{-3}$). But the *local* log-slopes over that range are
$-1.369,\,-1.201,\,-1.138,\,-1.105,\,-1.079,\,-1.064$: monotonically
approaching $-1$. The global fit is dominated by $N=2,3$, where subleading
corrections are of the same size as the leading term.

Running the paper's own permutation-symmetric ("dicke") engine — the one the
text says was used "far beyond" $N=8$ — over $N=8,16,32,64,128,256$ gives
errors $7.277\times10^{-3}$, $3.539\times10^{-3}$, $1.748\times10^{-3}$,
$8.686\times10^{-4}$, $4.330\times10^{-4}$, $2.162\times10^{-4}$, a fitted
exponent of $\mathbf{-1.013}$, and local slopes
$-1.040,\,-1.018,\,-1.009,\,-1.004,\,-1.002$.

So the $\mathcal O(1/N)$ claim is **true**, and the manuscript has printed the
one number in its possession that fails to demonstrate it, while asserting a
computation it does not report. A reader with any scepticism will read
"$-1.190$, consistent with $-1$" as special pleading, and will be wrong to — but
the paper invited it.

**Fix.** Report the large-$N$ fit ($-1.01$ over $N=8$–$256$) as the evidence for
the exponent, keep the $N\le8$ full-Liouvillian points as the exactness check on
the Dicke reduction, and either plot the local slope or state the fitted range
explicitly in both text and caption.

## Minor points

**m1.** `eq:defects-solved` is classified **Level P**, "Phenomenological
(fitted)", in `paper/generated/tab_claims.tex`. It is a numerical solution of a
two-point boundary-value problem in flat space with no data anywhere near it.
Level P is defined in §1.5 as "a number obtained by fitting to data, valid
within the stated likelihood and priors". Since the paper advertises that the
classification is machine-checked as part of the build, a wrong label that the
checker has certified is worse than an unchecked one. Add a level for
"numerically solved model equation" or reclassify as C with a numerical
qualifier.

**m2.** §11.3: "satisfies the virial identity $E_2=E_4$ to machine precision".
I get $E_2-E_4=-8.8\times10^{-9}$ on $E\approx103$, relative residual
$\sim10^{-10}$ (the appendix's `\numSkyrmeVirialResidual` is $1.70\times10^{-10}$).
That is collocation tolerance, not machine precision; say "to $2\times10^{-10}$".
Also "the trial family therefore overestimates the energy by about thirteen per
cent" is ambiguous: $E_{\rm trial}/E_{B=1}=118.435/103.129=1.148$, so the
overestimate is 14.8% of the true energy (12.9% of the trial value). State which.

**m3.** `thm:no-go`: (i) the hypotheses list $\Gamma\ge\Gamma_0>0$, but the
proof's final claim ($\Delta f\lesssim H_0/H_i$) uses
$\Gamma\le\Gamma_0e^{\alpha+\beta}$, an *upper* bound that belongs to
`eq:process-rate` and is not among the theorem's stated hypotheses. State it.
(ii) The constant "$c=\mathcal O(1)$ set by the precursor fraction at $a_i$" is
$c=\Omega_{I0}(a_i^{-3}-1)H_0^2/H_i^2$, which is $\approx\Omega_{I0}/\Omega_m$
in matter domination but $\approx\Omega_{I0}a_i/\Omega_r$ in radiation
domination — smaller by $\sim a_i/\Omega_r\sim10^{-4}$ at $a_i=10^{-8}$. The
text then instructs the reader to anchor $a_i$ "anywhere in the radiation era",
where the displayed $\Gamma_0\lesssim H_0^2/H_i$ does not follow from the proof.
The conclusion is unharmed (the honest radiation-era bound,
$\Gamma_0\lesssim3H_ia_i^3/[(1-b)\Omega_{I0}]\sim10^{-10}H_0$ at $a_i=10^{-8}$,
is still fatal), but either restrict $a_i$ to matter domination or carry $c$
explicitly.

**m4.** `thm:no-go`'s proof: "The second inequality follows from
$\rho_V(a_i)\ge0$, which is `thm:quasi-positivity`." Two problems. First,
`thm:quasi-positivity` is explicitly *not* a past statement — §5.1 says so:
"run backwards, $\rho_V$ decreases and can reach zero at a finite scale
factor". Second, $\rho_V(a_i)\ge0$ is already a hypothesis of `thm:no-go`
("the solution exists with non-negative densities on $[a_i,1]$"), so the
citation is redundant as well as out of domain. Delete it and point at the
hypothesis.

**m5.** `thm:de-sitter`'s proof, second alternative: "the source $Q_V$ is
strictly positive initially" does not follow from the stated hypotheses —
$\int^\infty\Gamma\,dt=\infty$ permits $\Gamma(t_i)=0$, which is what
`asm:activation` actually gives at early times. The repair is one clause:
divergence of the integral supplies $t_1$ with $\int_{t_i}^{t_1}\Gamma>0$, hence
$\rho_V(t_1)>0$.

**m6.** `thm:sandwich`'s proof disposes of the upper bound with "the same
integral with the roles of the endpoints exchanged". That is not a proof, and the
correct decomposition is not the one the phrase suggests: it is
$3M_{\rm Pl}^2(H^2_{\rm high}-H^2)=\int_{t_e}^{t}Q_Va'^3(a^{-3}-1)\,dt'
+\int_{t}^{t_0}Q_V(1-a'^3)\,dt'$, two terms of *different* structure, each
non-negative for $a\le1$. Write it out (two lines). Also state in the theorem
that both comparison $\Lambda$CDM models carry the same radiation density —
the proof uses it.

**m7.** `thm:snap` writes $s_{\Lambda\rm CDM}(q)$ as a function of $q$ alone,
but at $Q_V=0$ it is $2\Omega_r'-(1+2\Omega_r)(2+3q)$, which depends on
$\Omega_r$ too. `docs/theory/04_cosmography.md` defines it "at the same $q$
**and $\Omega_r$**"; restore the second argument, or state that radiation is
neglected in this subsection (which §7.2 does but §7.3 does not).

**m8.** `prop:determined-V`. (i) It is called "a five-parameter family", but the
proposition itself fixes $(\Gamma_0,\alpha,\beta,\tau_M,b)$ *and* the activation
law ($a_{\rm act}$, $p$) *and* the initial data — at least seven parameters plus
initial conditions. (ii) As an answer to the "mimetic can mimic anything"
objection it is question-begging rather than circular: it replaces a free
function $V(T)$ by a free function $\Gamma(f,M,a)$ and then restricts the latter
by a *postulated* parametric ansatz. The same manoeuvre applied directly to
$V(T)$ would give an equally "determined" potential. The paper's genuine,
ansatz-independent answer to that objection is `thm:sandwich`, which bounds the
achievable $E^2(a)$ by the single number $\Delta$; that is what §8.4 should lead
with, demoting `prop:determined-V` to the (true, useful, but weaker) statement
that the map from rate parameters to $V$ is well defined and monotone.

**m9.** `prop:classical-reduction`, second clause: "coherences decay at rate at
least $\Gamma/2$". $\Gamma$ is not defined for the $N$-unit system (it depends
on $\hat f_{\neg i}$), and the decay rate of $|n\rangle\langle m|$ is
$\tfrac12(\lambda_n+\lambda_m)$ with
$\lambda_n=\sum_i\langle n|L_i^\dagger L_i|n\rangle=(N-k_n)\Gamma_0
e^{\alpha k_n/(N-1)}$, which tends to zero as the state approaches full
absorption. Either state the correct rate or drop the clause; the
population-decoupling half is correct and is the part that matters.

**m10.** `thm:b-independence`'s proof states the intermediate result wrongly:
"the terms proportional to $b$ cancel in the sum, leaving $-\bar Q_V\delta_I$
distributed over the total". The residual is $-\delta Q_V$, which is **zero** by
`eq:perturbations-com`. Taken literally the printed proof would give
$\dot\delta_m=-\vartheta+\gamma_c\delta_m-(\bar Q_V/\bar\rho_m)\delta_I$, a
$\delta_I$-dependent term that would contradict `cor:b-invisible`. The theorem
is correct; the derivation is not, and the $\gamma_c\delta_m$ term comes from
$\dot{\bar\rho}_m=-3H\bar\rho_m-\bar Q_V$ in the denominator, not from the
transfer perturbation. Rewrite the two sentences.

**m11.** `prop:derrick` concludes "a single static canonical scalar therefore has
no *stable* localized solution". The argument given (no non-trivial stationary
point of $E$ under dilations) excludes any non-trivial *static solution*, which
is both stronger and what is actually needed. Say "no non-trivial static
localized solution".

**m12.** §9.3 reuses the symbol $p$ for the log-slope of $g_c$, while
`asm:activation` fixes $p$ as the switch exponent with $p>3$, and
`app:conventions` does not list $p$ at all. Introduce a separate symbol for the
local slope of $g_c$ and give its relation to $p$ for each rate normalization
(see M4). Add $p$, $a_{\rm act}$, $\xi_0$ and $\mathcal B$ to the symbol table.

**m13.** `prop:ide-map`'s last sentence, "It can never take the form
$Q\propto\rho_{\rm de}$", relies on $\Gamma$ being a function of $(f,M,a)$ only.
That is true of `eq:process-rate` but is not among the proposition's hypotheses,
and the proposition is stated under `asm:closure`, which does not fix the rate
law. Add the hypothesis.

**m14.** `prop:four-form`: the proof's phrase "Varying the metric before
imposing the solution" is doing important work — it is precisely the step whose
omission produces the wrong sign for the induced $\Lambda$ in much of the
four-form literature. One added clause saying *why* the order matters, and that
no additional boundary term at fixed flux is being assumed beyond
$S_\partial$ of `eq:setup-action`, would spare the reader a well-known trap and
cost two lines. (The result itself is right; I verified it symbolically.)

**m15.** §8.5, `prop:bridge`: the identification $\alpha=N\mathsf q\,d\log
\Gamma/dh$ presumes $\log\Gamma$ linear in $h$ "over the relevant range", which
is stated, but $N$ here is the number of precursor units *per patch* and is the
same $N$ that §3 sends to infinity in `thm:deterministic-limit`. If $\alpha$ is
to be $\mathcal O(1)$ then $\mathsf q\,d\log\Gamma/dh=\mathcal O(1/N)$ and the
deterministic limit and the bridge are pulling in opposite directions. Say a
word about it.

## Questions the authors must answer

**Q1.** In `asm:geodesic`, is the compatibility condition obtained by
differentiating $\alpha\delta f+\beta\delta M=-\delta_I$ and substituting the
perturbed kinetic equations satisfied by the dust dynamics, or is it not? If
not, which of the three relations is retained, and is it demonstrable that no
linear observable depends on the choice? (The supporting note asserts the
latter; the manuscript should carry the assertion and its one-line argument.)

**Q2.** Which rate normalization — constant $\Gamma_0$ or $\Gamma=\xi_0H$ — is in
force in `eq:process-rate`, `prop:activation`, `eq:cosmography-snap-explicit`,
`eq:perturbations-growth-signature`, and in the chains of §10? If the chains use
one and the analytic results the other, which numbers in §10 are affected?

**Q3.** Over what range of comoving wavenumber and redshift do the authors claim
the clock congruence is caustic-free, and does the data used in §10 — in
particular the $f\sigma_8$ points and any ISW-sensitive quantity — lie inside
it? "Nonlinear, recorded as open" is not an answer when the transfer
prescription itself is defined only on the regular set.

**Q4.** After restoring $p[1-S(a)]$ to `eq:cosmography-snap-explicit`, is
$\mathcal B_0$ separately identifiable from $(p,a_{\rm act})$ by any
cosmographic measurement, or only the sum $\mathcal B_0+p(1-S_0)$? If only the
sum, the abstract's "the $(j_0,s_0)$ plane is their cosmographic fingerprint"
must be weakened.

**Q5.** With $a_i=1$ in `thm:regular-future` and $a_0=1$ everywhere else, in
which normalization is the bound $V_i\le\rho_V\le V_i+(1-b)\rho_{I,i}$ to be
read, and what does it say numerically at $z=0$ for the fitted parameters?

---

*Code run for this report (single-threaded, `code/` on `PYTHONPATH`):
`absorb.symbolic.check_four_form/check_clock_action/check_jerk_identity/
check_growth_equation/check_solvable_family` (all `True`);
`absorb.skyrme.solve_hedgehog`, `bogomolny_bound`, `trial_energy`;
`absorb.lindblad.closure_error_scaling` with `engine="master"` ($N=2$–$8$) and
`engine="dicke"` ($N=8$–$256$), and `populations_decouple(4, alpha=1.0)`.
Numbers quoted above are the values returned.*
