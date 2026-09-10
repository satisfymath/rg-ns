# Referee report

**Manuscript**: Self-reinforced geometric absorption
**Referee**: A (interacting-vacuum / dark-sector theorist)
**Round**: 1
**Date**: 2026-09-09

---

## Summary (3 lines)

A pressureless "precursor" is irreversibly converted, at a rate that grows with the
already-converted fraction and with an exponentially-lagged memory of it, into pressureless
localized remnants and an exact interacting vacuum. Coupled to FLRW this yields exact survival
identities, structural positivity, a de Sitter attractor, a bracketing of \(H(z)\) by two
\(\Lambda\)CDM models, a one-signed jerk excess, and a linear growth sector in which the branching
ratio cancels. Covariant realizations (four-form, constrained clock) and a defect/open-quantum
sector are exhibited, and the model is fitted to Pantheon+, DESI DR2, chronometers and the Planck
distance priors.

That summary was possible to write, which is more than I can say for most submissions of this
length, and the manuscript's habit of ending each section with "what this does not establish" is
genuinely good practice. My objections below are almost all of the same kind: the *theory notes*
supplied with the manuscript are more careful than the manuscript, and in several places the
transcription into the paper has either dropped a hypothesis, dropped a term, or dropped a
disclaimer that the note insisted on. That is not a presentational matter — in two cases the
displayed result as printed is false, and in one case a theorem is built on a structural
inconsistency that the note flags as unresolved and the paper does not mention at all.

## Recommendation

[ ] Accept  [ ] Minor revision  [x] Major revision  [ ] Reject

---

## Major points

### M1. Eq. (`eq:cosmography-snap-explicit`) is wrong for the paper's own rate law, and it breaks Theorem `thm:memory-fingerprint`

**Location.** Sec. 7.3, Theorem `thm:snap`, second displayed result
(`eq:cosmography-snap-explicit`); knock-on to Theorem `thm:memory-fingerprint`,
Eq. (`eq:cosmography-fingerprint`), and to the abstract ("The memory parameters cancel from the
jerk and reappear in the snap, so the \((j_0,s_0)\) plane is their cosmographic fingerprint").

**What is wrong.** The general form (`eq:cosmography-snap`),
\(s-s_{\Lambda{\rm CDM}}=\varepsilon[\,\mathrm{d}\ln\Gamma/\mathrm{d}N-\Gamma/H-2\,]\), is correct;
I re-derived it and it matches the numerics. The specialisation to "the rate law
(`eq:process-rate`)" is not. The rate law of the paper is
\(\Gamma=\Gamma_0e^{\alpha f+\beta M}S_{\rm act}(a)\), so

\[
\frac{\mathrm{d}\ln\Gamma}{\mathrm{d}N}=\alpha(1-f)\frac{\Gamma}{H}+\mathcal B
+\underbrace{\frac{\mathrm{d}\ln S_{\rm act}}{\mathrm{d}N}}_{=\;p\,[1-S_{\rm act}(a)]},
\]

and the term \(\varepsilon\,p[1-S_{\rm act}]\) has simply been dropped. It is not a correction: it
is the largest term in the bracket over most of the range where \(\varepsilon\) is appreciable.
Note 04 has this right — its Eq. (3.4) is the activated version, and its Eq. (3.3), which is what
the paper has transcribed, is explicitly labelled there as being "for the draft's rate law
\(\Gamma=\Gamma_0e^{\alpha f+\beta M}\) (no explicit \(a\)-dependence)". The paper has transcribed
(3.3) and attached it to a rate law that does have explicit \(a\)-dependence.

**Verified numerically.** I integrated the reduced background (matter + exact vacuum, \(\Omega_r\to0\),
\(\Gamma_0/H_{100}=0.6\), \(\alpha=1\), \(\beta=1.5\), \(\tau_M=0.5\), \(b=0\), \(z_{\rm act}=1\),
\(p=6\)) and computed \(s-s_{\Lambda{\rm CDM}}(q)\) by spline differentiation of \(j=1+\varepsilon\):

| \(z\) | \(\varepsilon\) | numeric \(s-s_{\Lambda{\rm CDM}}\) | paper (`eq:cosmography-snap-explicit`) | with the \(\varepsilon p(1-S)\) term restored | dropped term |
|---|---|---|---|---|---|
| 2.00 | 0.0228 | **+0.080275** | \(-0.045594\) | +0.080275 | +0.125868 |
| 1.00 | 0.2006 | **+0.208549** | \(-0.392932\) | +0.208549 | +0.601481 |
| 0.50 | 0.3353 | \(-0.317505\) | \(-0.621543\) | \(-0.317505\) | +0.304037 |
| 0.00 | 0.2266 | \(-0.375457\) | \(-0.396372\) | \(-0.375457\) | +0.020915 |

The restored formula reproduces the numerics to solver tolerance at every redshift; the printed
formula has the **wrong sign** at \(z\gtrsim1\).

**Why it matters beyond an erratum.** \(\mathcal B\) and \(p[1-S_{\rm act}]\) enter the bracket with
*the same coefficient* \(+1\). Therefore

\[
\frac{\partial s_0}{\partial \mathcal B_0}=\frac{\partial s_0}{\partial\,[p(1-S_{\rm act}(1))]}=+\varepsilon_0,
\]

and \(s_0\) constrains only the sum \(\mathcal B_0+p[1-S_{\rm act}(1)]\), never \(\mathcal B_0\)
alone. Theorem `thm:memory-fingerprint` as stated ("at fixed \((H_0,q_0,j_0)\) the memory parameters
are ... constrained by the snap") is therefore false: the memory lag is exactly degenerate in the
snap with the activation slope, which is a parameter of the same model and is *not* fixed by
\((H_0,q_0,j_0)\). At the paper's own fiducial \(z_{\rm act}=1,\ p=6\) the contamination at \(z=0\)
is \(p[1-S]=0.092\) against \(\mathcal B_0=0.537\), i.e. \(\sim17\%\); it grows without limit as
\(z_{\rm act}\) is lowered, and dominates at \(z\gtrsim0.5\).

**Fix.** (i) Print the correct bracket in (`eq:cosmography-snap-explicit`). (ii) Restate
`thm:memory-fingerprint` as: at fixed \((H_0,q_0,j_0)\) the snap constrains the single combination
\(\mathcal B_0+p[1-S_{\rm act}(1)]\), and separating memory from activation requires either an
independent determination of \((a_{\rm act},p)\) or the redshift dependence \(s(z)\). (iii) Amend
the abstract, Sec. 1.4 contribution 4, and the conclusions accordingly — "the \((j_0,s_0)\) plane is
their cosmographic fingerprint" is not, on the corrected algebra, a statement the paper can make.

### M2. The deficit floor (`eq:cosmography-deficit-floor`) is false under the hypothesis the paper states

**Location.** Sec. 7.1, text between Theorem `thm:jerk` and Sec. 7.2; used again in Sec. 10.4
("a matter deficit consistent with it through `eq:cosmography-deficit-floor`") and advertised as
"the model's tightest internal consistency test".

**What is wrong.** The paper writes: "if the transfer is switching on, so that \(Q_Va^3/H\) is
non-decreasing, then the matter deficit sets a floor, \(j_0-1\ge2\Omega_{r0}+\tfrac92\Delta\); and
if \(Q_Va^3/H\propto a^{p_{\rm eff}}\) near today the relation is exact,
\(\varepsilon_0=\tfrac32(p_{\rm eff}+3)\Delta\)."

Note 04, Prop. 1.5, states the hypothesis on \(q(N)\equiv Q_V/(3M_{\rm Pl}^2H_0^2H)\), i.e. on
\(Q_V/H\), *not* on \(Q_Va^3/H\). The extra \(a^3\) has been inserted in transcription, in both the
monotonicity hypothesis and the power law. Since \(\Delta=\int q\,e^{3N}\mathrm dN\) and
\(\varepsilon_0=\tfrac32q_0\), the bound needs \(q\le q_0\), which is monotonicity of
\(Q_V/H\); monotonicity of \(Q_Va^3/H\) is strictly weaker and gives no floor at all.

**Verified numerically.** Take \(q(N)=e^{-N}\), so \(Q_Va^3/H\propto e^{2N}\) is strictly increasing
and the paper's stated hypothesis holds:

| \(a_e\) | \(\Delta\) | \(\varepsilon_0\) | \(\tfrac92\Delta\) | floor holds? |
|---|---|---|---|---|
| 0.368 | 0.43233 | 1.50000 | 1.94550 | **no** |
| 0.050 | 0.49876 | 1.50000 | 2.24442 | **no** |
| 0.0025 | 0.50000 | 1.50000 | 2.24999 | **no** |

With the note's hypothesis (\(q\) non-decreasing, e.g. \(q=e^{N}\)) the floor holds in every case.
The "exact" relation fails the same way: for \(Q_Va^3/H\propto a^{p}\) with \(q_0=1\), the true
\(\varepsilon_0=1.5\) while \(\tfrac32(p+3)\Delta\) gives \(6.00,\ 3.75,\ 2.25\) for \(p=1,2,6\)
(the correct value under the paper's own reading of \(p\) would be \(\tfrac32p\Delta\)).

**Fix.** State the hypothesis as "\(Q_V/H\) is non-decreasing up to today" (equivalently,
\(Q_Va^3/H\) grows at least as fast as \(a^3\)), and correspondingly define \(p_{\rm eff}\) by
\(Q_V/H\propto a^{p_{\rm eff}}\). Then \(\varepsilon_0=\tfrac32(p_{\rm eff}+3)\Delta\) and the floor
follow. Please also check that this hypothesis actually holds for the activation profiles used in
Sec. 10 rather than asserting it in a subordinate clause.

### M3. The geodesic realization is overdetermined, and the manuscript does not say so

**Location.** Sec. 9.1, Assumption `asm:geodesic`; Theorem `thm:b-independence` and everything
downstream of it (Eqs. `eq:perturbations-system`, `-growth`, `-frsd`, `-growth-signature`, `-isw`);
also Sec. 2.3.

**What is wrong.** `asm:geodesic` states that the rate law "applies to the background mode, and the
perturbations of the kinetic variables are slaved, \(\delta\Gamma/\bar\Gamma=-\delta_I\), with
\(\delta f\) and \(\delta M\) following by integration". That reads as though one imposes the
slaving and then integrates. It is not consistent. Once \(\Gamma=\Gamma_0e^{\alpha f+\beta M}S(a)\)
is a *local* function of the local kinetic state, \(\delta\Gamma/\bar\Gamma=\alpha\delta f+\beta\delta M\)
is an algebraic constraint, while \(\delta\dot f=-\bar\Gamma\delta f+(1-\bar f)\delta\Gamma\) and
\(\tau_M\delta\dot M=\delta f-\delta M\) are two evolution equations: three conditions on two
unknowns. With adiabatic data \(\delta f(t_i)=\delta M(t_i)=0\) the homogeneous pair forces
\(\delta f=\delta M\equiv0\), hence \(\delta\Gamma=0\), hence
\(\delta Q_{V,\rm com}/\bar Q_V=\delta_I\ne0\) — which contradicts (`eq:perturbations-com`), destroys
the integrability condition (`eq:perturbations-integrability`), and with it the entire linear
sector of Sec. 9.

Note 03 knows this. After its Prop. 1.3 it writes, in bold, "Honest statement of the structural
cost… the system is overdetermined by one… which is not identically satisfied by the dust dynamics
of Sec. 3", and resolves it by *demoting the kinetic variables to diagnostics*: (P4) as stated
there says the theory is *defined* by imposing \(\delta Q_{V,\rm com}=0\), and that
"\((f,M)\) are then diagnostic: their perturbations are reconstructed from (1.5) plus **whichever of
the equations (1.7) one retains**". Note 03's closing caveat 1 calls the overdetermination "an
unresolved structural issue". None of this appears in the manuscript.

This is the point on which I am least willing to be moved, because it is exactly the
bookkeeping/physics conflation that Sec. 2.3 promises to avoid. The paper cannot have it both ways:

* If the rate law is a local law — which is what Sec. 3 asserts, with a covariant memory equation
  \(\tau_M u^\mu\nabla_\mu M=f-M\) along flow lines and the explicit reassurance that "the rate at a
  point depends only on that point's causal past" — then \(\delta Q_V\ne0\), the vacuum acquires a
  comoving perturbation, and Sec. 9 does not apply to this model.
* If instead \(Q_V\) is *defined* to be uniform on comoving slices, then \(f\), \(M\), \(\alpha\),
  \(\beta\) and \(\tau_M\) have no local meaning at all: they are background bookkeeping, the
  "causal past" sentence in Sec. 3.1 is empty, and Theorem `thm:hysteresis` — advertised as "the
  sharpest way to state what is new here" — is a statement about a homogeneous ODE system, not
  about two universes that could actually be prepared side by side.

**Fix.** Import Note 03's honest version verbatim. Specifically: (i) state (P4) in the paper in the
form the note gives it, including the sentence that the kinetic variables are diagnostic at linear
order; (ii) state the overdetermination explicitly, with the compatibility condition displayed, and
add it to Sec. 13 as an open problem; (iii) weaken `asm:geodesic`'s "following by integration" to
what is actually true; (iv) reconcile Sec. 3.1's locality claim with it, or drop that claim.

### M4. Section 6 states one rate law and analyses a different one; the "\(p>3\)" repair is not a property of the law as printed

**Location.** Sec. 6.3, Assumption `asm:activation` (`eq:solvable-activation`), Prop. `prop:activation`,
and the sentence "The exponent condition \(p>3\) is exactly the requirement that the integral
generating the vacuum converge; it is the analytic content of the repair." Also Sec. 3.1,
Eq. (`eq:process-rate`).

**What is wrong.** Three separate symptoms of one problem.

1. \(\xi_0\) appears in `prop:activation`'s sufficient condition and is **never defined anywhere in
   the manuscript**. (Sec. 6.1 defines \(\xi\) for \(\Gamma=\xi H\); Sec. 5 defines \(\xi_{\rm eff}\);
   \(\xi_0\) is neither.) It comes from Note 02's rate law
   \(\Gamma=\xi_0 H S(a)e^{\alpha f+\beta M}\).
2. \(\mathcal I_{S}=\int_0^1 S(a)a^{-4}\mathrm da\) is the integral one obtains for
   \(\Gamma\propto H\): \(\int\Gamma\rho_I\mathrm dt=\xi_0\rho_{I0}\int S a^{-4}\mathrm da\). For the
   law actually printed in (`eq:process-rate`)/(`eq:solvable-activation`), with \(\Gamma_0\) a constant
   rate, the corresponding integral is \(\propto\int S a^{-2}\mathrm da\) in the radiation era
   (\(\int S a^{-5/2}\mathrm da\) in matter domination).
3. Consequently the convergence exponent is **\(p>1\)**, not \(p>3\), for the law as printed.

**Verified numerically** (\(a_{\rm act}=0.5\), cutoffs \(10^{-6}/10^{-8}/10^{-10}\)):

| \(p\) | \(\int_{\rm lo}^1 S a^{-2}\mathrm da\) (printed law) |
|---|---|
| 0.5 | divergent (2801, \(-14.7\), \(-21.7\): quadrature failing) |
| 0.8 | divergent (126, 335, \(-11.9\)) |
| 1.2 | 8.9027 / 9.6275 / 9.6275 — **convergent** |
| 2.0 | 2.2143 / 2.2143 / 2.2143 — **convergent** |

So \(p=2\) is perfectly admissible for the rate law the paper displays. The paper half-concedes this
("A switch with \(p=2\) fails this test *for the expansion-tracking form of the rate*") without ever
telling the reader that there are two rate laws in play, which of them Sec. 6.3, Sec. 7 and Sec. 10
use, or which one `params.py` samples (it implements both, via `rate_tracks_H`).

**Fix.** Decide which rate law is the model. If it is \(\Gamma\propto H\), print that in
(`eq:process-rate`) and define \(\xi_0\); if it is constant \(\Gamma_0\), rederive
`prop:activation` for that law and correct "\(p>3\)" to the right exponent. Either way, state
explicitly in Sec. 6.3 and in App. F which family the fits of Sec. 10 use, and drop the claim that
\(p>3\) is "exactly the requirement" unless it is.

### M5. The four-form bridge's one substantive argument rests on a sign error

**Location.** Sec. 8.5, the paragraph beginning "This is a genuine constraint rather than a
decoration".

**What is wrong.** The paper argues that reinforcement (\(\alpha>0\)) is not a free choice because
"the ratio of up to down rates is governed by the difference of horizon entropies,
\(S=24\pi^2\Mpl^4/V\), which does increase with \(V\)."

The formula is right (\(S_{\rm dS}=A/4G=8\pi^2\Mpl^2/H^2=24\pi^2\Mpl^4/V\)); the monotonicity is
backwards. \(S\) is manifestly a *decreasing* function of \(V\): a larger vacuum energy means a
larger \(H\), a smaller horizon and less entropy. Upward nucleation therefore lowers the de Sitter
entropy and is exponentially *suppressed* relative to downward nucleation, by
\(\Gamma_\uparrow/\Gamma_\downarrow=e^{-\Delta S}\) with \(\Delta S>0\).

The conclusion may well be rescuable — the suppression \(S(V)-S(V+\mathsf q h)\simeq
24\pi^2\Mpl^4\,\mathsf qh/V^2\) itself *decreases* as flux accumulates, so the upward rate does grow
with \(h\) — but that is a different argument from the one printed, it is one order more delicate,
and the paper does not make it. Since this is the only place in Sec. 8.5 where the manuscript claims
to have a constraint rather than a picture, it needs to be right.

Two further problems in the same subsection: `prop:bridge` is stated as a Proposition with **no
proof**, not even a sketch (the "exactly the chain of (`eq:process-intensity`)" claim needs the
identification \(N\mathsf q\,\mathrm d\log\Gamma/\mathrm dh=\alpha\) and the statement that each unit
nucleates at most once to be checked against \(\lambda_k=(N-k)\Gamma(k/N)\)); and the memory
variable, which is the paper's distinguishing ingredient, is not bridged at all — \(\tau_M\) is
offered as "the light-crossing time of the correlated patch" in Sec. 3.2 and Sec. 13.1 but nothing
in Sec. 8.5 produces it.

**Fix.** Correct the monotonicity statement and, if the conclusion survives, display the corrected
argument (the second derivative of \(S(V)\), with the sign made explicit). Give `prop:bridge` a
proof or demote it to a Remark. State plainly that the bridge covers \(\alpha\) and \(b\) but not
\(\beta\) or \(\tau_M\).

### M6. "The potential is determined, not chosen" does not answer the objection it claims to answer

**Location.** Sec. 8.4, Prop. `prop:determined-V` and the paragraph after it; abstract ("the
constrained-clock potential is shown to be determined by the kinetics rather than chosen, which
answers the standard objection to mimetic constructions").

**What is wrong.** The standard objection to (`eq:realizations-clock-action`) is that the *action*
does not constrain \(V(T)\), so the construction has no predictive content. The paper's reply is
that, once one fixes \((\Gamma_0,\alpha,\beta,\tau_M,b)\), the activation law and initial data,
\(V(T)=V_0+(1-b)\int_{t_0}^{T}\Gamma\rho_I\,\mathrm dt\) is determined. But \(\Gamma\rho_I\) is not
determined by the action: the kinetic law is an *additional postulate imposed from outside it*.
What has been shown is that a five-parameter ansatz for \(V(T)\) is a five-parameter family — which
is true of any five-parameter ansatz. The mimetic objection is conceded, not answered.

There is a real and defensible claim available here, and it is a weaker one: the kinetic
parametrization of \(V\) is *natural* (monotone non-decreasing, bounded above by
(`eq:cosmology-bounds`), with a specified early-time cutoff) and is not tuned to any dataset. Say
that instead.

Related, and worth stating in the same place: in the only covariant action the paper offers, the
matter tensor is \(\lambda u_\mu u_\nu-Vg_{\mu\nu}\) with \(\lambda=\rho_I+\rho_D\). Nothing in that
action distinguishes \(T_I\) from \(T_D\). So the five-sector split announced in Sec. 2.3 — which
Sec. 2.3 defends against the charge of bookkeeping precisely by pointing forward to
"\cref{sec:realizations} exhibits actions whose field equations produce it" — is *not* produced by
that action; only the sum is. Given that \(b\) is also invisible in the background (degenerate with
\(\epsilon\)) and in linear theory (`thm:b-independence`), the honest statement is that
\(\rho_I\)/\(\rho_D\) is bookkeeping at every level the paper computes. Sec. 2.3's forward reference
should be corrected.

**Fix.** Rewrite the abstract sentence and the paragraph after `prop:determined-V`; amend Sec. 2.3's
forward reference; relabel (`eq:realizations-determined-V`) as level I (it is the integral of the
third line of (`eq:cosmology-system`)) and put the five-parameter counting in the surrounding text
where it belongs.

### M7. Section 5's opening paragraph and Section 5.3's rebuttal contradict each other, and the positivity theorem is carrying less weight than the paper implies

**Location.** Sec. 5, opening paragraph; Theorem `thm:quasi-positivity` and the paragraph after its
proof; Sec. 5.3, the confrontation with data.

**(a) The contradiction.** The opening paragraph says the surveyed negative densities occur "specifically
when energy is taken to flow from dark matter to dark energy" — this model's direction — and the
next sentence embraces that ("Our model transfers energy in exactly that direction"). Sec. 5.3 then
rebuts the DESI-era preference, which is for the *opposite* direction, on the ground that "some of
the parametrizations carrying that preference are precisely the ones that admit negative densities".
Both cannot be true as stated.

Note 01's Prop. 2.1 is unambiguous and is the correct statement: family (A)
(\(Q\propto\rho_{\rm de}\), draining dark matter) fails on \(\{\rho_{\rm dm}=0\}\), family (B)
(\(Q\propto\rho_{\rm dm}\), draining dark energy) fails on \(\{\rho_{\rm de}=0\}\). The diagnostic is
**donor vs recipient**, not the direction of flow. The paper's opening sentence mischaracterises the
cited work (arXiv:2509.04494/95/96) in a way that happens to set up the paper's own rhetorical move,
and Sec. 5.3's rebuttal then quietly uses the correct version. A referee reading only the paper
cannot tell that both statements are attempts at the same underlying proposition.

**(b) Is the theorem doing work?** Theorem `thm:quasi-positivity` is correct. It is also, by itself,
close to trivial: the Nagumo faces are \(\dot\rho_I|_{\rho_I=0}=0\), \(\dot\rho_D|_{\rho_D=0}\ge0\),
\(\dot V|_{V=0}\ge0\), which is the observation that a system with non-negative sources and outflows
proportional to their own donors has an invariant orthant. App. B concedes as much: the actual proof
that survives merely-\(L^1_{\rm loc}\) \(\Gamma\) is the integrating-factor representation
(`eq:appb-integral`), not Nagumo (whose classical statement requires a continuous field). What makes
the comparison with arXiv:2509.0449x non-trivial is the *other half* of the dichotomy — Note 01's
Prop. 2.1, the demonstration that the recipient-proportional families violate the subtangent
condition on a codimension-one face, so that the catalogued failures are structural rather than
parameter accidents. **That half is not in the paper.** It appears only as one informal sentence
after the proof ("A coupling of the form \(Q\propto\rho_{\rm de}\) that drains dark matter … does not
have this property"). As it stands, the paper proves the easy half as a Theorem and asserts the hard
half in prose, and then Sec. 1.4 and the conclusions cite the Theorem as "what distinguishes this
coupling from the interacting dark energy models catalogued as admitting negative densities". That
is a straw man in its current form; it would not be one if Prop. 2.1 were stated and proved.

**Fix.** (i) Correct the opening paragraph to the donor/recipient statement, and check it against
what arXiv:2509.04494/95/96 actually report. (ii) Promote Note 01 Prop. 2.1 into Sec. 5.1 as a
proposition with its two-line proof; then `thm:quasi-positivity` is one half of a genuine dichotomy
and the comparison is fair. (iii) Carry over Note 01's caveat 3 ("We claim no priority for the
Nagumo/Kamke criterion, which is classical") and caveat 6 ("Prop. 2.1 does not refute the DESI-era
IDE preference … that is an open computation"), neither of which survives into the manuscript.

On the narrower question the brief asks: **yes, Sec. 5.3 is honest about the data.** It states
plainly that DESI-era fits weakly prefer the opposite sign, cites three of them, says a robust
detection falsifies the model, and explicitly says the qualifications are "not a defence of the
model". Sec. 10.4 repeats it. I have no complaint about the framing; my complaint is that the
supporting proposition is missing, which is what would make the second qualification more than
self-serving.

---

## Minor points

**m1. Claims-ladder misuse.** The ladder (Sec. 1.5) has no level for a *postulate*, and the two
central postulates of the paper are consequently stamped "C — Theorem of the model. Follows from the
new postulates": (`eq:process-rate`) is the rate law, and (`eq:solvable-activation`) is literally the
displayed content of Assumption `asm:activation`. Also: (`eq:positivity-deficit`) is a definition plus
an identity and should be I; (`eq:realizations-determined-V`) likewise (see M6); (`eq:defects-solved`)
is stamped P = "Phenomenological. A number obtained by fitting to data", but it is the numerical
solution of a boundary-value problem, fitted to nothing. Add a level D (definition/postulate) and
re-audit. Note also that `check_claims.py` passes (47 classified results, no unclassified `\boxed`)
but its only semantic rule — level S confined to the Outlook — is vacuous, because there are **zero**
level-S results in the manuscript while Sec. 13 opens "Everything in this section is conjecture".
Either give the Outlook's conjectures displayed level-S statements, or stop advertising the check as
if it constrained the conjectures. Finally, the abstract says results are classified "as an
identity, a theorem of the model, or a conjecture" — three levels; the ladder has four.

**m2. \(\rho_{\rm m}^{\rm early}\) is undefined.** In (`eq:positivity-deficit`) it must mean the
*comoving* dust \(m(t_e)=\rho_{\rm m}(t_e)a_e^3\) (Note 01 defines it that way); as printed, next to
\(\rho_{\rm m0}\), it reads as a density at \(t_e\) and is then wrong by \(a_e^{-3}\). Define it.

**m3. The sandwich proof sketch is too short, and drops the trap it was written to avoid.** *For the
record, I checked the item the brief flags: the paper has transcribed the corrected version.* Both
comparison models are \((\Omega_{\rm m0},\Omega_{V0})\) and \((\Omega_{\rm m0}+\Delta,\Omega_{V0}-\Delta)\),
both flat, both with \(E^2(1)=1\), hence both sharing the observed \(H_0\); this is Note 01
Thm. 5.1 and not the naive \((\rho_{\rm m}^{\rm early},V_{\rm early})\) pair of its Remark 5.2. I
also verified both inequalities independently: the lower bound is
\(\int_t^{t_0}Q_V[(a'/a)^3-1]\,\mathrm dt'\ge0\) as printed, and the upper bound is
\(a^{-3}A(1-a^3)-B\ge0\) with \(A=\int_{t_e}^tQ_Va'^3\mathrm dt'\ge0\) and
\(B=\int_t^{t_0}Q_V(a'^3-1)\mathrm dt'\le0\), with equality at \(a=1\) on both sides. However:
(i) "the upper bound follows from the same integral with the roles of the endpoints exchanged" is
*not* the argument — it is a sum of two integrals of different origin, and this hand-wave is
precisely the manoeuvre that produced the wrong version in the first place; print Note 01's Eq. (5.6).
(ii) Remark 5.2 of the note — the early-anchored model is a *lower* bound and does not share \(H_0\) —
belongs in the paper as a remark, for exactly the reason the note gives ("the naive version is easy
to write down and is wrong"). (iii) \(\Omega_{V0}-\Delta\) can be negative; either add the hypothesis
\(\Delta\le\Omega_{V0}\) or state that the upper comparison model may have \(\Lambda<0\).

**m4. `prop:clumping-unstable` excludes only half the alternatives.** It rules out \(\zeta>0\).
\(\zeta<0\) gives \(c_{\rm eff}^2=-\zeta/\bar\rho_I>0\) and is gradient-*stable*; Note 03's
Cor. 2.2 says so explicitly, and offers a separate (and, I think, weak — under (P4) \(Q_V\) is
uniform on comoving slices, not "concentrated in overdense regions") reason to reject it. The
geodesic realization is therefore the *boundary* of a stable half-line, not the unique stable point,
and Sec. 9.1's "the natural alternative is unstable" and "the geodesic choice is the one that keeps
the theory viable" overstate. Import Cor. 2.2's argument, or weaken the sentences. The sign argument
itself I checked and it is correct: \(\nabla_\mu T^{\mu\nu}_{\rm dust}=+\nabla^\nu V\) gives
\(\rho_IA^i=\partial^iV\), so with \(\zeta>0\) dust is accelerated *up* the vacuum gradient, i.e. into
overdensities — anti-restoring, \(c_{\rm eff}^2<0\), \(\lambda\propto k\).

**m5. "The memory law is derived, not postulated" is false as stated.** Sec. 3.2 opens
"\Cref{eq:process-memory} looks like an extra assumption. It is not," and `prop:memory-origin` then
*assumes* that each unit carries an internal \(m_i\) relaxing towards its own state with a *common*
\(\tau_M\). Averaging a linear ODE is not a derivation of the ODE; one postulate has been replaced by
another, arguably a stronger one (it now asserts a universal relaxation time across units). The
abstract ("the memory variable is not an extra postulate but the population mean of an eliminated
per-unit degree of freedom") and the conclusions repeat the claim. Reword to what is true: the
mean-field memory law is the exact population average of a per-unit relaxation law, so the
mean-field postulate is equivalent to a microscopically local one — which is a genuinely useful
statement, and a much weaker one.

**m6. Two hypotheses used by `thm:b-independence` are not stated.** Note 03 lists them as (P2)
single-flow (\(\rho_I,\rho_D,\rho_b\) share one four-velocity, and the \(I\to D\) conversion carries no
momentum relative to it) and (P5) no anisotropic stress, \(\Phi=\Psi\). The paper's proof silently
uses the first (it adds contrasts and applies one linearised Raychaudhuri equation) and
(`eq:perturbations-isw`) uses the second ("the relativistic Poisson equation"). This matters more than
usual here because the clock action of Sec. 8.3 contains only \(\lambda\) and \(V\) — baryons are not
part of it, so their comoving alignment with the clock congruence is an extra assumption, not a
consequence. State both hypotheses in the theorem.

**m7. `thm:quasi-positivity` states weaker hypotheses than it can support and cites the wrong tool.**
It asserts "no continuity" is required, but the Nagumo subtangent criterion in its classical form
requires a continuous vector field; what actually survives is the Carathéodory/integral argument of
App. B.3. Cite a Carathéodory-form invariance theorem, or say (as App. B effectively does) that
Nagumo is used to *organise* the argument and the integrating-factor representation is what proves
it. The theorem also does not state that a solution exists or that \(H>0\), both of which the proof
uses.

**m8. Mis-citation in Sec. 10.2.** "The branching ratio \(b\) does not appear in the background
separately from the combination \(\epsilon\) (`prop:ide-map`)". The statement is true — from
\(\mathrm d[(\rho_I+\rho_D)a^3]/\mathrm dt=-(1-b)\Gamma\rho_Ia^3\) and \(\rho_Ia^3=\rho_{I,i}(1-f)\)
only the product \((1-b)\rho_{I,i}\) enters, exactly as `background.py` implements it — but
`prop:ide-map` does not contain it. Give it its own one-line proposition in Sec. 4, where it belongs;
it is a useful result and it is currently homeless.

**m9. The hysteresis novelty claim needs a qualifier.** "No interaction written as a function of the
densities and the expansion rate, including one whose sign switches with redshift, has that
property" (abstract, Sec. 3.4, conclusions) is true but is a statement about the dimension of the
state space, not about physics. Any dark-energy model with internal degrees of freedom —
quintessence \((\phi,\dot\phi)\), elastic dark energy, and the fractional models the paper already
mentions — is path-dependent in the same sense. What is specific here is the *exponential-kernel*
memory with a single relaxation time and its Markovian embedding. Say that.

**m10. Track B and the abstract.** The abstract lists the sign predictions unqualified ("prove that
the effective dark matter can only lose energy"; "\(j\ge1+2\Omega_r\)"), but Sec. 5.5 introduces a
reverse channel that flips both, and Sec. 10 fits it "alongside rather than after the fact". A
reader is entitled to know from the abstract that the falsifiable sign prediction belongs to Track A
and that Track B is fitted in the same paper. One clause suffices.

**m11.** Sec. 9.3 asserts "A model that removed energy in proportion to the local density would
suppress both [\(f_g\) and \(f_{\rm RSD}\)]". This is the contrast that the abstract sells as the
signature; it is stated without proof or reference. Add the one-line calculation (it should follow
from \(\gamma_c\to0\) in the first of (`eq:perturbations-system`) with the drain moved into the
\(\delta\)-equation).

**m12.** Sec. 7.2, `thm:sign-table` is stated as a Theorem with no proof and no per-row hypotheses.
Note 04's caveat 4 is important and missing: the running-vacuum row assumes \(V\propto H^2\) with
constant \(\nu\) and other running laws give other signs; the CPL row assumes a single
non-interacting \(w\)-fluid. As printed, "the two families currently favoured by the data predict
opposite signs" is broader than what is proved.

**m13.** Typographic/consistency: `preamble.tex` documents level P as "phenomenological / fitted" and
S as "speculative (Outlook only)", while `check_claims.py` renders S as "Conjecture" in the generated
table. Harmonise.

---

## Questions the authors must answer

1. **Which rate law is fitted?** `params.py` implements both \(\Gamma=\Gamma_0e^{\alpha f+\beta M}S(a)\)
   and \(\Gamma=\xi_0He^{\alpha f+\beta M}S(a)\) (flag `rate_tracks_H`), and Sec. 6 mixes results that
   belong to each. Which family produces Tables 2 and 3? Are \(p>3\) and
   \(\mathcal I_{S}\) applied to the family they were derived for? (See M4.)

2. **How is \(\delta Q_{V,\rm com}=0\) implemented in `growth.py`?** Given M3, is the perturbed rate
   taken from the slaving relation, from the local rate law, or is neither used because the growth
   integration only ever needs the background \(g_c=\omega_V'/\omega_{\rm m}\)? If the last — which
   is what Note 03's (P4) implies — then say so in Sec. 9, because it means the memory sector is
   entirely invisible in the linear observables and Sec. 10's statement that the memory parameters
   are "constrained by the shape of the expansion history" is the only channel there is.

3. **Does the fitted posterior satisfy the hypothesis of the corrected deficit floor** (\(Q_V/H\)
   non-decreasing to today), and does it satisfy \(\Delta\le\Omega_{V0}\) so that the upper member of
   the sandwich is a genuine \(\Lambda\)CDM model? (M2, m3.)

4. **Sec. 8.5:** with the entropy monotonicity corrected, does the reinforcement argument still give
   \(\alpha>0\)? Please display the sign of \(\mathrm d^2S/\mathrm dV^2\) explicitly rather than
   asserting the direction. (M5.)

5. **Is the clock congruence the same congruence as the baryons?** The action of Sec. 8.3 contains
   only \(\lambda\) and \(V\). If baryons are added as a separate dust, what fixes their velocity
   relative to \(u_\mu=-\partial_\mu T\), and does `thm:b-independence` require adiabatic initial
   conditions to be stated as a hypothesis? (m6.)

---

## Note on what was checked by running code

All numerical statements above were obtained with short single-threaded scripts, run without
touching the ongoing chains:

* **M1** — direct integration of the reduced background system in \(N=\ln a\) (DOP853, rtol
  \(10^{-12}\)), with \(s=j'-j(2+3q)\) obtained by cubic-spline differentiation of \(j=1+\varepsilon\)
  and compared against both closed forms. Numbers in the table in M1. The activation term
  \(\varepsilon\,p[1-S_{\rm act}]\) reaches \(+0.601\) at \(z=1\) against a total of \(+0.209\).
* **M2** — closed-form quadrature of \(\Delta=\int q\,e^{3N}\mathrm dN\) for the counterexample
  \(q=e^{-N}\); floor violated at every \(a_e\lesssim0.72\), e.g. \(\varepsilon_0=1.500\) vs
  \(\tfrac92\Delta=2.244\) at \(a_e=0.05\).
* **M4** — cutoff-stability of \(\int_{\rm lo}^1 S(a)a^{-2}\mathrm da\) at
  \(a_{\rm act}=0.5\): convergent for \(p=1.2,2.0\), divergent for \(p=0.5,0.8\).
* `scripts/check_claims.py` was run and passes (47 classified results). I did **not** run the full
  `pytest` suite, to avoid competing with the running MCMC for memory.

The results subsection of Sec. 10 is incomplete by the authors' own note and I have not treated that
as a finding.
