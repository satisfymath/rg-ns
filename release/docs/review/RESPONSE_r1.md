# Response to referees, round 1

Two independent reports were obtained, from a referee working on interacting
vacuum cosmology (A) and one working on mathematical relativity and mimetic
gravity (C). Both recommended major revision. They agreed on three findings,
which is the strongest signal in the two reports and is reflected in the order
below.

Every point is answered by a change to the manuscript, not by argument. Where a
referee verified a claim numerically we reproduced the check before acting on
it; where a fix required new code, a test now pins the result so the error
cannot return.

## Findings both referees made independently

**The snap formula was wrong (A-M1, C-M1).** The explicit form of
$s-s_{\Lambda\rm CDM}$ was transcribed from the version of the calculation that
predates the activation switch, so the term $p\,[1-S_{\rm act}(a)]$ in
$\mathrm d\ln\Gamma/\mathrm dN$ was missing. This is not a correction to a small
term: at $z=1$ the printed bracket is $-1.94$ where the correct value is
$+1.07$, so the sign was wrong exactly where the effect is largest.

*Changed.* The formula is corrected. `absorb.background` now implements both a
spline-differentiated snap and the closed form, so the two can be compared, and
two tests assert their agreement and assert that the dropped term flips the
sign. The consequence is a weaker theorem and the paper now states it: the
activation term enters the same bracket with the same coefficient as the memory
lag, so the snap constrains their sum. The abstract and conclusions no longer
claim that the $(j_0,s_0)$ plane isolates memory.

**The deficit floor was false as stated (A-M2, C-M2).** The monotonicity
hypothesis was placed on $Q_Va^3/H$; the proof needs it on $Q_V/H$. Both
referees supplied counterexamples satisfying the printed hypothesis and
violating the bound.

*Changed.* The hypothesis is stated on $Q_V/H$, the reason the $a^3$ belongs to
the measure rather than the hypothesis is explained, and the exactness relation
is corrected accordingly.

**The perturbation sector is overdetermined (A-M3, C-M3).** Reading the rate law
as a local law gives three conditions on two unknown kinetic perturbations. Our
own theory note called this an unresolved structural issue and resolved it by
demoting the kinetic variables to diagnostics; none of that reached the
manuscript, which said the perturbations "follow by integration".

*Changed.* The assumption is restated in the note's form, the compatibility
condition is displayed, and the consequence is drawn rather than hidden: at
linear order the kinetic parameters are background bookkeeping, so the locality
claim in the kinetics section is a statement about the homogeneous mode. The
open problem is added to the Outlook, and the hysteresis claim is scoped to the
homogeneous mode accordingly.

## Referee A

**M4, two rate laws in circulation.** The manuscript displayed a constant-rate
law and analysed an expansion-tracking one; $\xi_0$ was never defined and the
convergence exponent $p>3$ belongs to the undisplayed law.

*Changed.* Both laws are named, $\xi_0$ is defined, which one the fits use is
stated, and the convergence condition is derived for each: $p>1$ for the
constant rate and $p>3$ for the expansion-tracking one. Referee C noted a second
consequence we had missed, that the growth signature inherits $p+3/2$ rather
than $p$ for the fitted law; that is now derived, verified against the numerics
(7.50 versus 6.00 at $p=6$) and pinned by a test.

**M5, the de Sitter entropy argument had the sign backwards.** The entropy
$S=24\pi^2M_{\rm Pl}^4/V$ decreases with $V$, so upward nucleation is
suppressed, not favoured.

*Changed.* The corrected argument is displayed: the suppression of a single
upward step falls as flux accumulates, which is the behaviour $\alpha>0$
requires. The bridge is demoted from Proposition to Remark, given the proof it
lacked, and stated to cover $\alpha$ and $b$ but not the memory sector.

**M6, the mimetic objection was conceded, not answered.** The kinetic law is
imposed from outside the action, so the action still does not constrain the
potential.

*Changed.* The claim is withdrawn. The paper now claims only what is true: the
ansatz is a five-parameter monotone bounded family with a specified early-time
cutoff, fixed before any data were examined. The related observation that the
clock action produces the dust/vacuum split but not the precursor/defect
division is added, and the forward reference that implied otherwise is
corrected. The relevant equation is relabelled as an identity.

**M7, the positivity section contradicted itself.** The opening attributed the
catalogued negative densities to the direction of the flow; the correct
diagnostic is donor versus recipient.

*Changed.* The opening is corrected, and the converse half of the dichotomy,
previously one informal sentence, is now a proposition with a proof.

## Referee C

**M5, the hysteresis theorem's final clause was false.** Under the activation
law the integrated rate diverges, so both histories reach $f\to1$: the
asymptotic converted fractions coincide.

*Changed.* The theorem now concludes about the accumulated vacuum, which is
what differs and what the simulation actually reports, and explains why: each
increment of $f$ is weighted by $a^{-3}$ and the two histories convert at
different epochs. The abstract and conclusions follow.

**M6, a restatement was promised and never made.**

*Changed.* The sentence is replaced by what is true: the theorems were already
stated with the weak hypothesis the activation law satisfies, and the condition
that the rate floor used to supply for free appears explicitly where it is
needed. Neither theorem needs its time domain restricted.

**M7, the mimetic pathologies.** The vanishing sound speed was counted twice,
as a conceded pathology and as the basis of a stability claim; the
gradient-stability disclaimer was made for an action that does not produce the
fitted perturbation theory; the caustic caveat was carrying real weight
silently; and the instability result excludes one branch, not all alternatives.

*Changed.* All four. In particular the caustic point is now stated where it
bites: since the constraint guarantees a non-vanishing gradient, a caustic is
the only way the Frobenius step can fail, so caustics are exactly the locus on
which the linear section is undefined. The assumption that the congruence is
caustic-free over the observed range is named as an assumption.

**M8, the Lindblad exponent.** The quoted $-1.19$ came from $N\le8$ and is a
small-$N$ artefact, while a large-$N$ computation was claimed but not reported.

*Changed.* Both are reported. The permutation-symmetric chain, which is exact
for the initial states used, now runs to $N=512$: the fitted exponent is
$-1.011$ and the local slope at the largest $N$ is $-1.001$. The figure shows
the full-Liouvillian points curving away from the $N^{-1}$ line the symmetric
chain follows.

## What the referees checked and found sound

Recorded here because it is as informative as the list of defects: the jerk
identity and bound; the sandwich theorem, in its corrected form, with both
inequalities verified independently; the single-transition corollary; the
quasi-positivity theorem; the four-form stress tensor, confirmed symbolically
including the variation order that usually flips a sign, and the vanishing
polarization count; the clock field equations; the integrability logic; the
whole of the growth, redshift-space and ISW algebra including the non-obvious
$2/(2p_{\rm eff}+5)$; the arithmetic-geometric mean step behind the Bogomolny
bound; the population half of the classical reduction; and every printed number
from the defect solver.

## Round 2

Two changes are substantial enough to warrant re-examination: the corrected
snap and its weakened fingerprint theorem, and the restated geodesic assumption
with its compatibility condition. A second round should be limited to those,
plus the data section once the chains have converged.
