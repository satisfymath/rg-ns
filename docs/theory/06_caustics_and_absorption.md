# Note 06 — Does conversion regularize a caustic?

**Status.** Theory note. Every statement below is either proved here or marked
as open. The numerical checks are in `code/tests/test_collapse.py` and
`code/tests/test_pancake.py`; the exact solutions are in
`code/absorb/collapse.py`.

**Scope.** Local analysis along a single flow line, plus a one-dimensional
Zel'dovich pancake. Nothing here concerns the homogeneous cosmology of the main
paper, which is untouched.

---

## 0. The question, and what the manuscript claimed

Section 13 of the manuscript recorded, as a conjecture at level S:

> $Q_V \propto \rho_I$ diverges at shell crossing $\Longrightarrow$ $\rho_I$
> remains finite.

The intuition was that conversion runs away where the density runs away, and
therefore removes the divergence. **This note shows the implication is false**,
identifies exactly what would have to be true instead, and finds that each
repair moves the divergence rather than removing it.

---

## 1. The exact local solution

Along a flow line with proper time $\tau$ and expansion $\Theta=\nabla_\mu
u^\mu$, the precursor obeys

$$
\frac{D\rho_I}{D\tau}+\Theta\rho_I=-\Gamma\rho_I
\qquad\Longleftrightarrow\qquad
\frac{d\ln\rho_I}{d\tau}=-(\Theta+\Gamma) ,
$$

so that, exactly and with no approximation,

$$
\boxed{\;\rho_I(\tau)=\rho_I(\tau_0)\,
\exp\Big[-\int_{\tau_0}^{\tau}\big(\Theta+\Gamma\big)\,ds\Big] . }
\tag{1.1}
$$

Everything follows from the divergence structure of that single integral.

> **Lemma 1.1 (trichotomy).** As $\tau\to T$,
> $\rho_I\to\infty$ iff $\int^{T}(\Theta+\Gamma)\to-\infty$;
> $\rho_I$ tends to a finite non-zero limit iff the integral converges;
> $\rho_I\to0$ iff it tends to $+\infty$.
> *Proof.* Immediate from (1.1) and continuity of $\exp$. $\square$

> **Theorem A (bounded-rate obstruction).** Suppose $0\le\Gamma\le G<\infty$ on
> $[\tau_0,T)$ with $T-\tau_0<\infty$, and suppose the compression is
> non-integrable, $\int^{T}\Theta\,ds=-\infty$. Then $\rho_I\to\infty$.
>
> *Proof.* $\int_{\tau_0}^{\tau}\Gamma\,ds\le G(T-\tau_0)<\infty$ for every
> $\tau<T$, so the conversion contributes a factor
> $\exp[-\int\Gamma]\in[e^{-G(T-\tau_0)},1]$, bounded below by a positive
> constant. The compression contributes $\exp[-\int\Theta]\to+\infty$. A
> divergent factor times a factor bounded below by a positive constant
> diverges. $\square$

**This applies to the model as published.** Under the activation law of the
manuscript, $\Gamma=\Gamma_0 S_{\rm act}(a)e^{\alpha f+\beta M}$ with
$\alpha,\beta\ge0$ and $f,M\in[0,1]$, so $\Gamma\le\Gamma_0e^{\alpha+\beta}$:
the rate is bounded, Theorem A applies, and the conjecture is false.

**Where the intuition went wrong.** $Q_V=(1-b)\Gamma\rho_I$ does diverge,
because $\rho_I$ does. But $Q_V$ is a transfer *per unit volume*; what appears
in the exponent of (1.1) is the *fractional* loss rate $\Gamma$, and that stays
bounded. A diverging absolute transfer with a bounded fractional rate removes a
fixed proportion of an ever-larger density, which is not regularization.

---

## 2. What a compression-driven rate would have to do

Take the self-similar model
$$
\Theta=-\frac{c}{T-t},\qquad
\Gamma=\frac{g}{T-t}+\Gamma_{\rm b}(t),\qquad c,g>0,
$$
with $\Gamma_{\rm b}$ bounded. Writing $s=T-t$, (1.1) gives

$$
\boxed{\;\rho_I\sim s^{-(c-g)}\times[\text{factor bounded above and below}] . }
\tag{2.1}
$$

> **Theorem B (collapse/absorption balance).** With the above,
> $\rho_I$ diverges for $g<c$, tends to a finite non-zero limit for $g=c$, and
> vanishes for $g>c$. The bounded part of the rate cannot change which case
> occurs.

**But $\rho_I$ is not the only thing that has to stay finite.** Three further
quantities must be checked, and they do not all give the same condition.

**(a) The vacuum.** $\dot V=(1-b)\Gamma\rho_I\sim s^{g-c-1}$, so
$$
\int^{T}\dot V\,dt<\infty
\iff g-c-1>-1
\iff \boxed{g>c\ \text{strictly}.}
\tag{2.2}
$$
At $g=c$ exactly the precursor is finite but the vacuum still diverges,
logarithmically. Numerically the vacuum increases by exactly $\ln 100$ per two
decades of $s$ there, which is asserted in the test suite.

**(b) The defects.** $\dot\rho_D=-\Theta\rho_D+b\Gamma\rho_I$. The homogeneous
part alone gives $\rho_D\sim s^{-c}$: **the defect density diverges for every
$g$ whenever $b>0$**, because the localized product is itself pressureless dust
being compressed by the same $\Theta$, and nothing removes it. Its *column*
density $\rho_D\times(\text{proper width})\sim s^{-c}\cdot s^{c}$ tends to a
finite constant: the mass is finite, the density is not.

**(c) The total stress tensor.** Combining,
$$
\boxed{\;T_{\mu\nu}\ \text{remains finite at the caustic}
\iff g>c\ \ \text{and}\ \ b=0 . }
\tag{2.3}
$$

> **Corollary (the $\kappa>1$ threshold).** For
> $\Gamma_{\rm collapse}=\kappa\,[-\Theta]_+$ one has $g=\kappa c$, so
> $g>c\iff\kappa>1$, independently of $c$. For a generic Zel'dovich pancake
> $c=1$: the Jacobian $J=1+D\psi'$ crosses zero linearly, so
> $\Theta=d\ln J/dt\sim-1/(T-t)$.

The threshold is dimensionless and sharp. It says the conversion must remove a
larger fraction of the precursor per unit time than the compression adds.

---

## 3. Covariance: the dichotomy

Before any of this can be adopted, the transfer must be covariantly consistent.
With $T_V^{\mu\nu}=-Vg^{\mu\nu}$ so that $\nabla_\mu T_V^{\mu\nu}=-\nabla^\nu
V$, total conservation requires $\nabla^\nu V=-Q^\nu$, where $Q^\nu$ is the
transfer four-vector. The left side is a gradient, so $Q^\nu$ must be closed.

> **Theorem C (transfer dichotomy).** Let the conversion act at a caustic.
>
> **(i) Dust to dust is free but useless.** If the product is a second
> pressureless sector sharing the congruence, the two continuity equations sum
> to $D(\rho_I+\rho_D)+\Theta(\rho_I+\rho_D)=0$ identically: no integrability
> condition arises, and the *total* dust density is exactly what it would be
> with no conversion at all. The divergence is relocated, not weakened.
>
> **(ii) Dust to vacuum can regularize but is constrained.** Writing
> $Q^\nu=Qu^\nu+q^\nu$ with $q\cdot u=0$:
> - $q^\nu=0$ forces $d(Q\,u)=0$, hence $Q=Q(T)$ for a geodesic clock: the
>   transfer must be constant on each comoving slice. A rate depending on
>   $\Theta$ is not, precisely at a caustic, so the geodesic-vacuum realization
>   of the manuscript is **incompatible** with a compression-driven rate.
> - $q^\nu\ne0$ is always available: for any smooth $V$, $Q^\nu=-\nabla^\nu V$
>   is closed, its timelike part reproduces $DV=Q$ automatically, and the whole
>   content is the spatial part $q^\nu=-D^\nu V$, which the dust must absorb as
>   a force, $\rho_I A^\nu=D^\nu V$. The dust is then no longer geodesic, and
>   the force *density* $D^\nu V$ scales as $V/w$ with $w$ the caustic width,
>   which diverges.

So the sector that can absorb the divergence is the one that does not dilute,
and that is exactly the sector whose transfer is constrained.

## 4. The one good news: the new channel is invisible where the paper lives

> **Theorem D (FLRW and its perturbations are untouched).** Let
> $\Gamma_{\rm collapse}=\kappa[-\Theta]_+$. On the open set $\{\Theta>0\}$
> this vanishes identically. An expanding FLRW background has $\Theta=3H>0$,
> and a neighbourhood of it in any reasonable perturbative topology still has
> $\Theta>0$. Hence every term of the perturbative expansion about such a
> background vanishes: the background, the linear theory, and every higher
> order are exactly unchanged.

This is stronger than "the correction is nonlinear". The correction is
identically zero on an open set containing the background, so no order of
perturbation theory sees it. What switches it on is not a large perturbation
but a change of sign of the local expansion.

---

## 4b. Self-similar scaling: which quantities may diverge

Posit $\rho\sim s^{-p}$ and $\ell_i\sim s^{q_i}$ for the three principal
directions, $s=T-t$. The proper volume of the core is $s^{Q}$ with
$Q=\sum_i q_i$, so

$$
E_{\rm core}=\int\rho\sqrt{\gamma}\,d^3x\ \sim\ s^{Q-p},
\qquad\text{finite}\iff Q\ge p,\qquad\text{vanishing}\iff Q>p .
$$

This is the entire content of "a divergent density can carry a finite mass". It
is dimensional bookkeeping, and any mass-conserving collapse satisfies it with
$p=Q$ exactly. It is not a mechanism, and nothing is gained by dressing it up
as one. For a planar caustic one direction contracts, $q_1=c$, and the other
two do not, so $Q=c$.

The point of the table below is that quantities usually spoken of together do
not stand or fall together.

| Quantity | Exponent in $s$ | Finite? |
|---|---|---|
| precursor density | $\kappa-1$ | iff $\kappa\ge1$ |
| precursor column density | $\kappa$ | always, and $\to0$ |
| defect density ($b>0$) | $-1$ | never |
| defect column density ($b>0$) | $0$ | always |
| vacuum increment | $\kappa-1$ | iff $\kappa>1$ |
| expansion $\Theta$ | $-1$ | **never** |
| velocity | bounded | always |
| core width | $+1$ | always |
| curvature invariant | $\min$ of the density exponents | iff $\kappa>1$ and $b=0$ |

Two entries deserve emphasis. The **expansion scalar diverges in every case**,
including those where the stress tensor is finite: what conversion can remove is
the gravitational effect of the caustic, not the caustic of the congruence. A
congruence singularity is not a spacetime singularity, and the two must not be
conflated. And the **defect channel never helps**: with $b>0$ the curvature
diverges however strong the conversion, because the product is dust and is
compressed by the same $\Theta$.

## 5. Summary table

| Quantity | Bounded rate | $g<c$ | $g=c$ | $g>c$, $b>0$ | $g>c$, $b=0$ |
|---|---|---|---|---|---|
| $\rho_I$ | diverges | diverges | finite | $\to0$ | $\to0$ |
| $V$ | finite | diverges | diverges (log) | finite | finite |
| $\rho_D$ | diverges | diverges | diverges | diverges | absent |
| column densities | finite | finite | finite | finite | finite |
| $T_{\mu\nu}$ | diverges | diverges | diverges | diverges | **finite** |
| covariance | consistent | \multicolumn{4}{c}{needs momentum transfer or a non-vacuum receiver} |

---

## What this does not establish

The analysis above prescribes $\Theta$; it does not solve for it. Once the dust
is accelerated by $D^\nu V$, or once the converted vacuum back-reacts
gravitationally, $\Theta$ is no longer the Zel'dovich value and the exponents
must be recomputed self-consistently. Nothing here shows that a self-consistent
solution with $\kappa>1$ and $b=0$ exists, only what such a solution would have
to satisfy. Nor does anything here bear on the homogeneous cosmology of the
main paper: $[-\Theta]_+$ vanishes there identically, which is the content of
Theorem D and also the reason none of this changes any published number.
