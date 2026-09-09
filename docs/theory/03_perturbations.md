# Note 03 — Linear scalar perturbations in the geodesic realization

**Status.** Theory note for transcription. Contains a **correction to Proposition 7 of the draft**,
which is stated for a single dust component and is wrong as written for $b>0$.

**Dependencies.** Note 01 (positivity, $Q_V\ge0$, the identity $d\ln(\rho_ma^3)/d\ln a=-Q_V/(H\rho_m)$);
Note 02 (the activation law, which controls the size and epoch dependence of $g_c$ below).

---

## 0. Setting, gauge, and variables

### 0.1 Matter content and frames

We work with the background system (S) of Note 01. All three pressureless components
$k\in\{I,D,{\rm b}\}$ (precursor, defects, baryons) are assumed to share a single four-velocity
$u^\mu$ — a *single-flow* assumption, legitimate at linear order and for the modes considered
here, and stated explicitly as hypothesis (P2) below. Radiation is dropped throughout Secs. 1–5
(the results are for $z\lesssim100$); it is restored only in the numerical form of Sec. 7 through
$E(N)$ and $\Omega_m(N)$.

Kinematic decomposition:
$$
\Theta=\nabla_\mu u^\mu,\qquad A^\mu=u^\nu\nabla_\nu u^\mu,\qquad
D=u^\mu\nabla_\mu,\qquad \Delta^{\mu\nu}=g^{\mu\nu}+u^\mu u^\nu .
$$

### 0.2 Gauge

**Synchronous comoving gauge.** $u^\mu=(1,0,0,0)$, $ds^2=-dt^2+a^2(\gamma_{ij}+h_{ij})dx^idx^j$.
Perturbation variables:
$$
\delta_k=\frac{\delta\rho_k}{\bar\rho_k},\qquad
\vartheta=\delta\Theta,\qquad
\delta_m=\frac{\sum_k\bar\rho_k\delta_k}{\bar\rho_m},\quad \bar\rho_m=\sum_k\bar\rho_k .
$$
Note the sign convention: for conserved dust, $\dot\delta=-\vartheta$, so $\vartheta<0$ in a
collapsing overdensity and $f_g=-\vartheta/(H\delta)$ is positive for a growing mode.
Because $u^\mu$ is geodesic in Realization G (Sec. 1) the synchronous gauge is comoving and the
residual gauge freedom is the usual constant-in-time mode, removed by the growing-mode initial
conditions of Sec. 7.3.

### 0.3 Standing hypotheses for this note

- **(P1)** The background solves (S) with $\Gamma\ge0$; $H>0$; all densities non-negative
  (Note 01, Thm. 1.1).
- **(P2) Single flow.** $\rho_I,\rho_D,\rho_b$ share one four-velocity $u^\mu$; the internal transfer
  $I\to D$ carries no momentum relative to that frame.
- **(P3) Exact vacuum.** $T^{\mu\nu}_V=-Vg^{\mu\nu}$, so $p_V=-V$ identically and there is no
  independent vacuum sound speed, no vacuum four-velocity and no vacuum anisotropic stress.
- **(P4) Realization G.** Stated and discussed in Sec. 1.
- **(P5)** No anisotropic stress from any sector, so the two Bardeen potentials coincide,
  $\Phi=\Psi$.

---

## 1. Realization G, stated as an explicit assumption

### 1.1 The integrability obstruction

The transfer to an exact vacuum with no spatial force in the frame $u^\mu$ is
$$
-\nabla^\mu V=Q_V\,u^\mu .
\tag{1.1}
$$
Lowering the index, the left-hand side is an exact one-form, so $d(Q_V u)=0$ where
$u\equiv u_\mu dx^\mu$; equivalently
$$
\nabla_{[\mu}\big(Q_Vu_{\nu]}\big)=0 .
\tag{1.2}
$$
This is the draft's (10.2). It is a genuine additional condition: specifying $Q_V$ as a scalar
function of the local matter state does **not** in general satisfy it.

> **Lemma 1.1 (geodesic clock $\Rightarrow$ $Q_V$ and $V$ are functions of $T$).**
> Suppose $u_\mu=-\partial_\mu T$ with $dT\ne0$ on an open set $U$ (so $u$ is hypersurface
> orthogonal and, since $u^\mu u_\mu=-1$ fixes $g^{\mu\nu}\partial_\mu T\partial_\nu T=-1$,
> the flow is geodesic: $A_\mu=u^\nu\nabla_\nu u_\mu=-u^\nu\nabla_\nu\partial_\mu T
> =-u^\nu\nabla_\mu\partial_\nu T=-\tfrac12\partial_\mu(u^\nu u_\nu)=0$).
> Then (1.2) is equivalent on $U$ to
> $$
> dQ_V\wedge dT=0 ,
> \tag{1.3}
> $$
> hence $Q_V=Q_V(T)$ locally; and (1.1) then gives $dV=Q_V(T)\,dT$, so $V=V(T)$ with
> $V'(T)=Q_V(T)$.
>
> **Proof.** $Q_Vu=-Q_V\,dT$, so $d(Q_Vu)=-dQ_V\wedge dT$, and (1.2) is $d(Q_Vu)=0$. Equation (1.3)
> says the one-forms $dQ_V$ and $dT$ are proportional, i.e. $Q_V$ is constant on level sets of $T$
> (Frobenius, using $dT\neq0$). Then (1.1) reads $\nabla_\mu V=Q_V\partial_\mu T$, whose
> integrability $d(Q_V\,dT)=0$ is (1.3) again; integrating along the flow gives $V=V(T)$. $\square$

> **Corollary 1.2.** On comoving hypersurfaces ($T=\text{const}$, which coincide with the
> constant-time slices of the synchronous comoving gauge),
> $$
> \boxed{\;\delta V_{\rm com}=0,\qquad \delta Q_{V,\rm com}=0 .}
> \tag{1.4}
> $$

### 1.3 What (1.4) does to the kinetic sector

> **Proposition 1.3 (slaving of the rate perturbation).** Assume (P1)–(P4) and $b<1$,
> $\bar\rho_I>0$, $\bar\Gamma>0$. Since $Q_V=(1-b)\Gamma\rho_I$ with $b$ constant, (1.4) gives
> $\delta(\Gamma\rho_I)=0$, i.e.
> $$
> \boxed{\;\frac{\delta\Gamma}{\bar\Gamma}=-\,\delta_I\;}
> \tag{1.5}
> $$
> on comoving slices. With the rate law $\Gamma=\xi_0H\,S(a)\,e^{\alpha f+\beta M}$ of Note 02
> (in which $H$, $S(a)$ and $a$ are unperturbed on these slices), (1.5) becomes the algebraic
> constraint
> $$
> \alpha\,\delta f+\beta\,\delta M=-\delta_I .
> \tag{1.6}
> $$
> The perturbed kinetic equations then read
> $$
> \delta\dot f=-\bar\Gamma\,\delta f+(1-\bar f)\,\delta\Gamma
> =-\bar\Gamma\,\delta f-(1-\bar f)\bar\Gamma\,\delta_I ,
> \qquad
> \tau_M\,\delta\dot M=\delta f-\delta M ,
> \tag{1.7}
> $$
> which determine $(\delta f,\delta M)$ by quadrature once $\delta_I(t,\mathbf x)$ is known, from
> initial data $\delta f(t_i)=\delta M(t_i)=0$.

**Honest statement of the structural cost.** Equations (1.6) and (1.7) are *three* conditions on
*two* unknowns $(\delta f,\delta M)$: the system is overdetermined by one. Differentiating (1.6)
and substituting (1.7) yields a compatibility condition,
$$
\alpha\Big[-\bar\Gamma\delta f-(1-\bar f)\bar\Gamma\delta_I\Big]
+\frac{\beta}{\tau_M}\big(\delta f-\delta M\big)=-\delta\dot_I ,
$$
which is not identically satisfied by the dust dynamics of Sec. 3. We therefore state Realization G
in the following precise, self-consistent form, and record the residual issue as open:

> **(P4) Realization G — the defining assumption.**
> *The theory is defined by imposing (1.1) with a geodesic clock, i.e. by (1.4). The volumetric
> transfer $Q_V$ is spatially uniform on comoving hypersurfaces; the local conversion rate
> anti-correlates exactly with the local precursor density, eq. (1.5). The kinetic variables
> $(f,M)$ are then diagnostic: their perturbations are reconstructed from (1.5) plus whichever of
> the equations (1.7) one retains, and this choice does not enter any linear observable, because —
> as Theorem 3.1 below shows — the entire linear dust sector closes on $\delta_m$ and $\vartheta$
> and sees the kinetic sector only through the background quantity $\bar Q_V$.*

**Correction to the draft.** Sec. 10.1 of the draft lists four ways to extend the transfer to
inhomogeneities (constrain the rate so that it is compatible with (1.2); allow momentum transfer and
a donor acceleration; give the vacuum its own dynamics and pressure; build a full open action) and
*chooses none of them*. This note chooses the first and states it as an assumption with a name,
because every subsequent perturbation result depends on it, and because the second option is shown
in Sec. 2 to be unstable.

---

## 2. Why not the alternative: gradient instability of a clumping vacuum

> **Hypotheses.** (P1)–(P3), (P5), and instead of (P4):
> **(P4$'$)** $\delta V_{\rm com}=\zeta\,\delta_I$ for some $\zeta>0$ (the vacuum tracks the
> precursor overdensities), with $\zeta$ slowly varying.
> For simplicity take a single dust component $\rho_I$; the argument is unchanged with several.

> **Proposition 2.1 (negative effective sound speed).** Under (P1)–(P3), (P4$'$), (P5), the dust is
> no longer geodesic:
> $$
> \bar\rho_I A_i=\partial_i\,\delta V=\zeta\,\partial_i\delta_I ,
> \tag{2.1}
> $$
> and the linear growth equation acquires, in Fourier space, the term
> $$
> \ddot\delta_I+2H\dot\delta_I+\Big(\underbrace{-\frac{\zeta}{\bar\rho_I}}_{\;\equiv\,c_{\rm eff}^2}\frac{k^2}{a^2}
> -\frac{\bar\rho_I}{2M_{\rm Pl}^2}-\frac{\zeta}{M_{\rm Pl}^2}\Big)\delta_I=\ldots ,
> \tag{2.2}
> $$
> i.e. an effective squared sound speed $c_{\rm eff}^2=-\zeta/\bar\rho_I<0$. The mode with
> wavenumber $k$ grows as $\exp\big[\,k\sqrt{\zeta/\bar\rho_I}\,\int dt/a\,\big]$, with a rate that
> diverges linearly in $k$: the initial-value problem is Hadamard ill-posed.
>
> **Proof.** Total conservation $\nabla_\mu(T^{\mu\nu}_{\rm dust}+T^{\mu\nu}_V)=0$ with
> $T^{\mu\nu}_V=-Vg^{\mu\nu}$ gives $\nabla_\mu T^{\mu\nu}_{\rm dust}=\nabla^\nu V$. Projecting with
> $\Delta^\alpha{}_\nu$ and using $T^{\mu\nu}_{\rm dust}=\rho_Iu^\mu u^\nu$:
> $\rho_IA^\alpha=\Delta^{\alpha\nu}\nabla_\nu V$, whose spatial part at linear order is (2.1).
> The Raychaudhuri equation is
> $$
> D\Theta=-\tfrac13\Theta^2-\sigma^2+\omega^2+\nabla_\mu A^\mu-\tfrac{1}{2M_{\rm Pl}^2}(\rho+3p).
> $$
> Linearising with $\Theta=3H+\vartheta$, and using $\delta\rho+3\delta p=\bar\rho_I\delta_I+\delta V-3\delta V
> =(\bar\rho_I-2\zeta)\delta_I$ for a dust-plus-exact-vacuum mixture:
> $$
> \dot\vartheta+2H\vartheta=-\frac{(\bar\rho_I-2\zeta)}{2M_{\rm Pl}^2}\delta_I+\nabla_\mu A^\mu ,
> \qquad
> \nabla_\mu A^\mu=\frac{1}{a^2}\nabla^2\!\Big(\frac{\zeta\delta_I}{\bar\rho_I}\Big)
> \xrightarrow{\ \rm Fourier\ }-\frac{k^2\zeta}{a^2\bar\rho_I}\delta_I .
> \tag{2.3}
> $$
> Eliminating $\vartheta$ with $\dot\delta_I=-\vartheta+(\text{transfer terms})$ gives (2.2); the
> $k^2$ term enters the growth equation with the sign displayed, i.e. exactly as
> $-k^2\zeta\delta_I/(a^2\bar\rho_I)$ appearing as a *source* rather than a restoring force.
> Setting $\delta_I\propto e^{\lambda\int dt}$ in the large-$k$ limit gives
> $\lambda^2\simeq k^2\zeta/(a^2\bar\rho_I)$, hence $\lambda\propto k$. $\square$

> **Corollary 2.2 (stability selects the geodesic realization).** Realization G is the $\zeta=0$
> member of the family (P4$'$), and it is the boundary of stability: any $\zeta>0$ gives a gradient
> instability with unbounded growth rate, while $\zeta<0$ ($\delta V$ anticorrelated with $\delta_I$)
> gives $c_{\rm eff}^2>0$ but requires the vacuum to be *underdense* where matter is overdense, which
> contradicts the transfer direction $Q_V\ge0$ concentrated in overdense regions. We therefore adopt
> (P4) on stability grounds, not merely on grounds of covariance.

**Caveat.** Proposition 2.1 assumes the vacuum retains $p_V=-V$ exactly (P3) while acquiring
$\delta V\ne0$. If instead one replaces the exact vacuum by a genuine scalar-field or fluid dark
energy with its own $c_s^2\ge0$, the instability disappears — but so does the model: that is the
draft's third option in Sec. 10.1, and it is a different theory.

---

## 3. The $b$-independence theorem

### 3.1 Statement

> **Hypotheses.** (P1)–(P5), with $k$ ranging over $\{I,D,{\rm b}\}$ and
> $\bar\rho_m=\bar\rho_I+\bar\rho_D+\bar\rho_b>0$. Define
> $$
> \delta_m=\frac{\bar\rho_I\delta_I+\bar\rho_D\delta_D+\bar\rho_b\delta_b}{\bar\rho_m},
> \qquad
> \gamma_c\equiv\frac{\bar Q_V}{\bar\rho_m}\;\ge0 .
> $$

> **Theorem 3.1 ($b$-independence of linear growth).** Under (P1)–(P5), for every $b\in[0,1]$,
> $$
> \boxed{\;\dot\delta_m=-\vartheta+\gamma_c\,\delta_m,
> \qquad
> \dot\vartheta+2H\vartheta=-\frac{\bar\rho_m}{2M_{\rm Pl}^2}\,\delta_m\;}
> \tag{3.1}
> $$
> and hence
> $$
> \boxed{\;\ddot\delta_m+(2H-\gamma_c)\dot\delta_m
> -\Big(\frac{\bar\rho_m}{2M_{\rm Pl}^2}+\dot\gamma_c+2H\gamma_c\Big)\delta_m=0 .}
> \tag{3.2}
> $$
> The branching ratio $b$ enters (3.1)–(3.2) **only** through the background quantity
> $\bar Q_V=(1-b)\bar\Gamma\bar\rho_I$ inside $\gamma_c$; the split of $\bar\rho_m$ between
> precursor and defects, and the individual contrasts $\delta_I,\delta_D$, drop out.
>
> **Proof.** *(a) The individual equations.* Local energy conservation for each dust species, with
> (P2) (common $u^\mu$) and (P3), reads
> $$
> D\rho_I+\Theta\rho_I=-\Gamma\rho_I,\qquad
> D\rho_D+\Theta\rho_D=+b\,\Gamma\rho_I,\qquad
> D\rho_b+\Theta\rho_b=0 .
> $$
> Write $\rho_k=\bar\rho_k(1+\delta_k)$, $\Theta=3H+\vartheta$, and subtract the background.
> Using $\delta(\Gamma\rho_I)=0$ from (1.4)/(1.5) — so that also $\delta(b\Gamma\rho_I)=0$ — and
> $\dot{\bar\rho}_I=-(3H+\bar\Gamma)\bar\rho_I$, $\dot{\bar\rho}_D=-3H\bar\rho_D+b\bar\Gamma\bar\rho_I$:
> $$
> \dot\delta_I=-\vartheta+\bar\Gamma\,\delta_I,\qquad
> \dot\delta_D=-\vartheta-\frac{b\bar\Gamma\bar\rho_I}{\bar\rho_D}\,\delta_D,\qquad
> \dot\delta_b=-\vartheta .
> \tag{3.3}
> $$
> *(b) The sum.* Multiply each by $\bar\rho_k$ and add, using
> $(\bar\rho_k\delta_k)^{\textstyle\cdot}=\dot{\bar\rho}_k\delta_k+\bar\rho_k\dot\delta_k$:
> $$
> (\bar\rho_I\delta_I)^{\textstyle\cdot}=(-3H-\bar\Gamma)\bar\rho_I\delta_I+\bar\rho_I(-\vartheta+\bar\Gamma\delta_I)
> =-3H\bar\rho_I\delta_I-\bar\rho_I\vartheta,
> $$
> $$
> (\bar\rho_D\delta_D)^{\textstyle\cdot}=(-3H\bar\rho_D+b\bar\Gamma\bar\rho_I)\delta_D
> +\bar\rho_D\Big(-\vartheta-\frac{b\bar\Gamma\bar\rho_I}{\bar\rho_D}\delta_D\Big)
> =-3H\bar\rho_D\delta_D-\bar\rho_D\vartheta,
> $$
> $$
> (\bar\rho_b\delta_b)^{\textstyle\cdot}=-3H\bar\rho_b\delta_b-\bar\rho_b\vartheta .
> $$
> **The $\pm b\bar\Gamma\bar\rho_I\,\delta$ terms have cancelled in each line and, a fortiori, in
> the sum.** Adding, $(\bar\rho_m\delta_m)^{\textstyle\cdot}=-3H\bar\rho_m\delta_m-\bar\rho_m\vartheta$.
> Subtracting $\dot{\bar\rho}_m\delta_m=(-3H\bar\rho_m-\bar Q_V)\delta_m$ gives
> $\bar\rho_m\dot\delta_m=\bar Q_V\delta_m-\bar\rho_m\vartheta$, i.e. the first of (3.1).
> *(c) Raychaudhuri.* With $A^\mu=0$ (geodesic, Lemma 1.1), $\sigma^2,\omega^2$ quadratic, and
> $\delta\rho+3\delta p=\bar\rho_m\delta_m+\delta V-3\delta V=\bar\rho_m\delta_m$ by (1.4),
> the linearised Raychaudhuri equation gives the second of (3.1) directly. Note that the vacuum
> contributes nothing: $\delta V=0$ and $\delta p_V=-\delta V=0$.
> *(d)* Solve the first of (3.1) for $\vartheta=-\dot\delta_m+\gamma_c\delta_m$, differentiate and
> substitute into the second; collecting terms gives (3.2). $\square$

### 3.2 Correction to the draft: Proposition 7 is wrong for $b>0$

The draft's Proposition 7 (Sec. 10.2) states (10.4)–(10.5) with
$$
\delta=\delta\rho_I/\bar\rho_I,\qquad \gamma_c=\bar Q_V/\bar\rho_I,\qquad
\dot\vartheta+2H\vartheta=-\frac{\bar\rho_I}{2M_{\rm Pl}^2}\delta ,
$$
and prefaces it with "for a single interacting dust and vacuum $V(T)$, without radiation or separate
baryons". Read as a statement about the full model of Sec. 7 of the draft it is **incorrect for
$b>0$**, in two independent ways, both visible by comparing with (3.1) and (3.3):

1. **Wrong friction coefficient.** From (3.3), the correct coefficient in the $\delta_I$ equation is
   $\bar\Gamma$, not $\bar Q_V/\bar\rho_I=(1-b)\bar\Gamma$. These agree only at $b=0$. The draft's
   $\gamma_c$ is therefore too small by the factor $(1-b)$ when applied to $\delta_I$.
2. **Wrong Poisson source.** The gravitational source in the Raychaudhuri equation is the *total*
   dust, $\bar\rho_m\delta_m$, not $\bar\rho_I\delta_I$. For $b>0$ the defects carry a finite share
   $\bar\rho_D$ of the dust and must appear; so must baryons. Using $\bar\rho_I$ underestimates the
   source by the factor $\bar\rho_I/\bar\rho_m$, which by the survival identities (7.2)–(7.3) of the
   draft tends to zero as $f\to1$.

Both defects are repaired by Theorem 3.1, which is the statement to be transcribed: the *correct*
variable is $\delta_m$, the *correct* coefficient is $\gamma_c=\bar Q_V/\bar\rho_m$, and the
resulting equation has exactly the form the draft wrote — but for the total dust. We record this
plainly because the $b=0$ restriction is not stated in the draft's Proposition 7 and a reader would
apply it to the two-product model.

> **Corollary 3.3 ($b$ and the dark-sector split are invisible in linear cosmology).**
> (i) All linear observables built from $\delta_m$, $\vartheta$ and the metric potentials
> (matter power spectrum shape, $f\sigma_8$, ISW, CMB lensing) depend on the model only through
> $H(a)$ and $\gamma_c(a)$. (ii) $\delta_I$ and $\delta_D$ separately are not observables: the
> defects are by hypothesis pressureless and interact only gravitationally, so no linear probe
> distinguishes them from the precursor. (iii) At background level $b$ survives only as the
> amplitude factor $(1-b)$ multiplying $\bar\Gamma\bar\rho_I$ in $\bar Q_V$; since $\bar\rho_I$ and
> $\bar f$ obey equations independent of $b$, the map $b\mapsto\bar Q_V$ is a pure rescaling at
> fixed $\Gamma$-history, and $b$ is therefore degenerate with the normalisation $\xi_0$ of the rate
> up to the mild nonlinearity introduced by the reinforcement factor $e^{\alpha f}$.
> *Proof.* (i) is Theorem 3.1 plus (P5) and the Poisson relation of Sec. 5. (ii) follows because
> $b$ enters (3.3) only through $\bar\rho_D/\bar\rho_m$, which is not separately measurable, and
> because $\delta_I,\delta_D$ appear in no source term other than through $\delta_m$. (iii) is
> read off from (S): $\dot\rho_I=-(3H+\Gamma)\rho_I$ and $\dot f=(1-f)\Gamma$ contain no $b$. $\square$

**This is good news and should be presented as such:** the model's most speculative ingredient — the
existence and abundance of localised defects — is *not* required to be tuned to match structure
formation. It is also bad news for identifying the defects: linear cosmology cannot see them.

---

## 4. Growth, redshift-space distortions and the growth index

### 4.1 The two growth rates

> **Definitions.** With $N=\ln a$ and a growing solution $\delta_m(N)>0$,
> $$
> f_g\equiv\frac{d\ln\delta_m}{d\ln a},\qquad
> f_{\rm RSD}\equiv-\frac{\vartheta}{H\delta_m},\qquad
> g_c\equiv\frac{\gamma_c}{H}=\frac{\bar Q_V}{H\bar\rho_m}\;\ge0 .
> $$
> $f_g$ is the growth rate of the *density* contrast; $f_{\rm RSD}$ is the *velocity* growth rate,
> which is what redshift-space distortions actually measure, because the RSD signal is generated by
> peculiar velocities and the Kaiser factor is built from $\nabla\!\cdot\!\mathbf v$.

> **Proposition 4.1 (RSD is not the density growth rate here).** Under (P1)–(P5),
> $$
> \boxed{\;f_{\rm RSD}=f_g-g_c=f_g-\frac{\bar Q_V}{H\bar\rho_m}\;\le\;f_g .}
> \tag{4.1}
> $$
> Consequently the RSD observable is
> $$
> \boxed{\;\big[f\sigma_8\big]_{\rm RSD}(z)=\big[f_g(z)-g_c(z)\big]\,\sigma_{8,0}\,
> \frac{\delta_m(z)}{\delta_m(0)} . }
> \tag{4.2}
> $$
> **Proof.** From the first of (3.1), $\vartheta=-\dot\delta_m+\gamma_c\delta_m$. Divide by
> $-H\delta_m$: $f_{\rm RSD}=\dot\delta_m/(H\delta_m)-\gamma_c/H=f_g-g_c$. Non-negativity of $g_c$ is
> Note 01, Thm. 1.1. Equation (4.2) is the definition of $f\sigma_8$ with
> $\sigma_8(z)=\sigma_{8,0}\,\delta_m(z)/\delta_m(0)$ (linear, scale-independent growth, guaranteed
> by the $k$-independence of (3.2)). $\square$

**Why this matters.** In $\Lambda$CDM and in any model with conserved dust, $f_{\rm RSD}=f_g$ and
the distinction is empty. Here it is a genuine, one-signed offset: the model predicts that the
velocity field lags the density field by exactly $g_c$. Any analysis that infers $f_g$ from RSD and
then compares it to the density growth predicted by this model will find a spurious mismatch of
size $g_c$; equations (4.1)–(4.2) are the correct comparison.

### 4.2 Perturbative solution in the matter era and the growth index

> **Hypotheses (extra).** **(P6)** Matter domination: $\Omega_m\to1$, $E'/E\to-\tfrac32$,
> $\Omega_r$ negligible. **(P7)** $g_c\ll1$ with local logarithmic slope
> $p\equiv d\ln g_c/dN$ approximately constant over the interval considered. (For the activation
> law of Note 02, $g_c\propto S(a)\,\bar\Gamma\bar\rho_I/(H\bar\rho_m)$, and deep in the matter era
> $S\propto a^{p_{\rm act}}$ dominates the variation, so $p\simeq p_{\rm act}\ge6$; at
> $a\gtrsim a_{\rm act}$, $p$ drops towards $\mathcal O(1)$ or below.)

> **Theorem 4.2 (leading correction to the growth rates).** Under (P1)–(P7), to first order in
> $g_c$ the growing mode of (3.2) satisfies
> $$
> \boxed{\;f_g=1+\frac{2p+3}{2p+5}\,g_c+\mathcal O(g_c^2),\qquad
> f_{\rm RSD}=1-\frac{2}{2p+5}\,g_c+\mathcal O(g_c^2). }
> \tag{4.3}
> $$
> In particular $f_g>1$ (growth is *enhanced*) and $f_{\rm RSD}<1$ (the velocity field is
> *suppressed*), for every $p\ge0$.
>
> **Proof.** In matter domination the system (3.1) in $N$, with $u\equiv-\vartheta/H$ so that
> $f_{\rm RSD}=u/\delta_m$, reads
> $$
> \delta_m'=u+g_c\delta_m,\qquad u'+\tfrac12u=\tfrac32\delta_m ,
> $$
> the second following from $\dot\vartheta+2H\vartheta=-\tfrac32H^2\Omega_m\delta_m$ with
> $\Omega_m=1$, $\dot H/H^2=-\tfrac32$. Eliminating $u$:
> $$
> \delta_m''+\tfrac12\delta_m'-\tfrac32\delta_m=\big(g_c\delta_m\big)'+\tfrac12 g_c\delta_m .
> \tag{4.4}
> $$
> At zeroth order the growing mode is $\delta_m^{(0)}=e^{N}$ (and the decaying one $e^{-3N/2}$),
> giving $u^{(0)}=e^N$, $f_g=f_{\rm RSD}=1$. Writing $g_c=Ge^{pN}$ and
> $\delta_m=e^N+\delta_1$ with $\delta_1=Ae^{(p+1)N}$, the left side of (4.4) evaluated on
> $\delta_1$ is $A\,p(p+\tfrac52)\,e^{(p+1)N}$ and the right side is
> $G\,(p+\tfrac32)\,e^{(p+1)N}$, so
> $$
> A=\frac{G\,(2p+3)}{p\,(2p+5)} .
> $$
> Then $f_g=\delta_m'/\delta_m=1+(p+1-1)Ae^{pN}+\mathcal O(G^2)=1+pA\,e^{pN}
> =1+\frac{2p+3}{2p+5}g_c$, and $f_{\rm RSD}=f_g-g_c$ gives the second of (4.3). (Verified
> independently by symbolic algebra.) $\square$

**Checks and readings.**
- $p=0$ (constant $g_c$): $f_g=1+\tfrac35g_c$, $f_{\rm RSD}=1-\tfrac25g_c$. The naive "adiabatic"
  estimate obtained by dropping $f_1'$ in the Riccati form reproduces exactly this, as it must.
- $p\to\infty$ (very sharp activation): $f_g\to1+g_c$, $f_{\rm RSD}\to1$. The density contrast picks
  up the full $g_c$ while the velocity field is unaffected — as expected, since a sudden uniform
  energy removal changes $\bar\rho_m$ and hence $\delta_m$ without touching $\vartheta$.
- The signs are opposite. **This is the sharpest linear signature of the model**: a simultaneous
  *enhancement* of the density growth rate and *suppression* of $f\sigma_8$. A model that removed
  energy from clustered matter in proportion to the local density would suppress both.

> **Corollary 4.3 (shift of the growth index).** Parametrise $f_g=\Omega_m^{\gamma}$ with
> $\gamma=\gamma_0+\delta\gamma$, $\gamma_0=6/11$ for $\Lambda$CDM. Then, at any epoch where
> $\Omega_m$ is appreciably below unity,
> $$
> \boxed{\;\delta\gamma\simeq\frac{1}{\ln\Omega_m}\cdot\frac{2p+3}{2p+5}\,\frac{g_c}{\Omega_m^{\gamma_0}}
> \;<\;0 ,}
> \tag{4.5}
> $$
> while the index inferred from RSD data (which measures $f_{\rm RSD}$) shifts the other way,
> $$
> \delta\gamma_{\rm RSD}\simeq-\frac{1}{\ln\Omega_m}\cdot\frac{2}{2p+5}\,\frac{g_c}{\Omega_m^{\gamma_0}}\;>\;0 .
> \tag{4.6}
> $$
> *Proof.* $\delta f_g=\Omega_m^{\gamma_0}\ln\Omega_m\,\delta\gamma$; solve for $\delta\gamma$ and
> insert (4.3). Signs follow from $\ln\Omega_m<0$. $\square$
>
> **Caveat, to be stated in the paper.** The $\gamma$-parametrisation degenerates in matter
> domination ($\ln\Omega_m\to0$), which is exactly where Theorem 4.2 is derived. Equations
> (4.5)–(4.6) should be used only as an order-of-magnitude translation at $z\lesssim1$, and the
> honest comparison with data is (4.2) evaluated by numerical integration of (7.1) below.
> Note also that $\Omega_m(z)$ itself differs between this model and $\Lambda$CDM at fixed $H_0$
> (Note 01, Thm. 5.1), so (4.5) mixes a genuine growth effect with a background effect; only the
> full $[f\sigma_8](z)$ curve is unambiguous.

---

## 5. The gravitational potential and the ISW effect

> **Hypotheses.** (P1)–(P5); sub-horizon modes so the Poisson equation in the form below applies;
> $\Phi=\Psi$ by (P5).

> **Proposition 5.1 (decay law of $\Phi$).** With the relativistic Poisson equation
> $-\dfrac{k^2}{a^2}\Phi=\dfrac{\bar\rho_m\,\delta_m}{2M_{\rm Pl}^2}$ ($\delta_m$ the
> comoving-gauge contrast),
> $$
> \boxed{\;\frac{d\ln\Phi}{d\ln a}=f_{\rm RSD}-1=f_g-g_c-1 . }
> \tag{5.1}
> $$
> **Proof.** $\Phi\propto a^{2}\bar\rho_m\delta_m/k^{2}=a^{-1}\big(a^{3}\bar\rho_m\big)\delta_m/k^2$.
> By Note 01, Thm. 4.1, $d\ln(a^3\bar\rho_m)/dN=-g_c$. Hence
> $d\ln\Phi/dN=-1-g_c+f_g=f_{\rm RSD}-1$ using (4.1).
> *Equivalent derivation avoiding the split:* from the proof of Theorem 3.1(b),
> $(\bar\rho_m\delta_m)^{\textstyle\cdot}=-3H\bar\rho_m\delta_m-\bar\rho_m\vartheta$, so
> $d\ln(a^3\bar\rho_m\delta_m)/dt=-\vartheta/\delta_m=Hf_{\rm RSD}$, and
> $\Phi\propto a^{-1}\cdot a^3\bar\rho_m\delta_m$ gives (5.1) at once. $\square$

> **Corollary 5.2 ($\Phi$ decays already in matter domination).** Under (P6)–(P7),
> $$
> \boxed{\;\frac{d\ln\Phi}{d\ln a}\Big|_{\rm MD}=-\frac{2}{2p+5}\,g_c
> \;=\;-\frac{2}{2p+5}\,\frac{\bar Q_V}{H\bar\rho_m}\;<\;0 ,}
> \tag{5.2}
> $$
> whereas in $\Lambda$CDM $d\ln\Phi/d\ln a=0$ exactly during matter domination.
> **The sign is the same as the late-time $\Lambda$CDM ISW effect (decaying potentials), the effect
> starts earlier, and the two contributions add rather than cancel.**
> *Proof.* Insert (4.3) into (5.1). $\square$

**Physical reading, and an honest correction of a tempting shortcut.** One is tempted to say that
$\Phi$ decays at the rate $g_c=\bar Q_V/(H\bar\rho_m)$, on the grounds that $\bar\rho_m$ is being
drained at that rate. That is the answer *only if one freezes $\delta_m$*. The correct calculation
must include the back-reaction of the drain on the growth of $\delta_m$: because
$\delta Q_{V,\rm com}=0$ (Realization G), overdense and underdense regions lose the *same absolute*
energy density, so overdense regions lose a *smaller fraction*, and $\delta_m$ is boosted by
$+\gamma_c\delta_m$. That boost partially cancels the background drain, and the net decay rate is
$2g_c/(2p+5)$ — smaller than $g_c$ by a factor between $2/5$ (slow activation) and $\sim1/p$ (sharp
activation). The statement "$\Phi$ decays at rate $Q_V/(H\rho_m)$" should not be transcribed; (5.2)
should.

**Observational hooks.** (i) A positive cross-correlation between the CMB temperature and
low-redshift tracers extending to *higher* redshift than $\Lambda$CDM predicts. (ii) Because
$\Phi=\Psi$ and the lensing potential is $\Phi+\Psi=2\Phi$, CMB lensing and galaxy lensing amplitudes
are reduced by the same factor as $\Phi$, i.e. $S_8$ is lowered relative to a $\Lambda$CDM model with
the same early-time normalisation — the direction favoured by lensing-versus-CMB tensions, though we
make no claim about the magnitude here.

---

## 6. Absence of a Väliviita-type large-scale instability

> **Theorem 6.1 (no independent dark-energy degree of freedom, hence no instability).**
> Under (P1)–(P5), the linear scalar sector of the model reduces to the **two-dimensional,
> $k$-independent** system
> $$
> \frac{d}{dN}\begin{pmatrix}\delta_m\\ \tilde\vartheta\end{pmatrix}
> =\mathcal M(N)\begin{pmatrix}\delta_m\\ \tilde\vartheta\end{pmatrix},
> \qquad
> \mathcal M(N)=\begin{pmatrix} g_c & -1\\[2pt] -\tfrac32\Omega_m & -\big(2+\tfrac{E'}{E}\big)\end{pmatrix},
> \qquad \tilde\vartheta\equiv\frac{\vartheta}{H},
> \tag{6.1}
> $$
> whose coefficients depend on $N$ only. Consequently:
> (i) there is no vacuum density perturbation ($\delta V_{\rm com}=0$) and no vacuum pressure
> perturbation ($\delta p_V=-\delta V=0$), so no non-adiabatic pressure mode exists;
> (ii) the characteristic exponents of (6.1) are independent of $k$, so no mode's growth rate
> diverges as $k\to0$;
> (iii) the growth is scale-independent, $\delta_m(N,\mathbf k)=D(N)\,\delta_m(N_i,\mathbf k)$ for a
> single transfer function $D$.
> Therefore the early-time large-scale instability of Väliviita, Majerotto & Maartens
> (arXiv:0804.0232) has no analogue in this model.
>
> **Proof.** *Row 1.* Divide $\dot\delta_m=-\vartheta+\gamma_c\delta_m$ (Thm. 3.1) by $H$ and use
> $\dot{}=H\,{}'$: $\delta_m'=-\tilde\vartheta+g_c\delta_m$.
> *Row 2.* With $\vartheta=H\tilde\vartheta$,
> $\dot\vartheta=H\frac{d}{dN}(H\tilde\vartheta)=H^2\tilde\vartheta'+H\dot H\,\tilde\vartheta$.
> Insert into $\dot\vartheta+2H\vartheta=-\bar\rho_m\delta_m/(2M_{\rm Pl}^2)=-\tfrac32H^2\Omega_m\delta_m$
> and divide by $H^2$, using $\dot H/H^2=E'/E$:
> $\tilde\vartheta'+\big(2+E'/E\big)\tilde\vartheta=-\tfrac32\Omega_m\delta_m$, i.e. row 2 of
> $\mathcal M$.
> *No $k$ anywhere.* $\delta_m$ and $\vartheta$ are sourced only by $\bar\rho_m\delta_m$ (from
> Raychaudhuri, which contains no gradients once $A^\mu=0$ by Lemma 1.1) and by $\gamma_c\delta_m$.
> The vacuum enters the perturbed Einstein equations only through $\delta\rho_V=\delta V=0$ and
> $\delta p_V=-\delta V=0$, so it adds neither a variable nor a constraint.
> *Why the Väliviita et al. mechanism is absent.* That instability arises in the coupled system
> $(\delta_{\rm dm},\theta_{\rm dm},\delta_{\rm de},\theta_{\rm de})$, in which $\delta\rho_{\rm de}$ is an
> independent dynamical variable carrying a non-adiabatic pressure perturbation
> $\delta p_{\rm de}=c_{s,\rm de}^2\delta\rho_{\rm de}+\big(c_{s,\rm de}^2-c_a^2\big)\,3H(1+w)\rho_{\rm de}\,\theta_{\rm de}/k^2$,
> whose $k^{-2}$ piece — fed by the interaction term — dominates at small $k$ and produces
> super-horizon blow-up for $1+w$ of the wrong sign. Here $\delta\rho_{\rm de}\equiv\delta V=0$ and
> $1+w\equiv0$ identically, so every factor in that expression vanishes. $\square$

> **Component form of (6.1), for reference:**
> $$
> \boxed{\;
> \delta_m'=g_c\,\delta_m-\tilde\vartheta,
> \qquad
> \tilde\vartheta'=-\Big(2+\frac{E'}{E}\Big)\tilde\vartheta-\frac32\Omega_m\,\delta_m .}
> \tag{6.2}
> $$

**What this does *not* rule out — a distinction that must be drawn explicitly.** The clock/dust
sector has $c_s^2=0$ identically. Vanishing sound speed means there is no pressure support at *any*
scale, so the pressureless flow generically develops **caustics** (shell crossings) at the nonlinear
level, where $\Theta\to-\infty$ and the single-flow assumption (P2) and the clock foliation
$u_\mu=-\partial_\mu T$ both break down. This is the well-known pathology of mimetic/dust-like
constructions analysed in arXiv:1704.03367. It is a **nonlinear** problem and is logically
independent of Theorem 6.1, which is a statement about the linear system. We claim linear stability,
not global regularity; the draft's Sec. 10.2 already flags caustics and we repeat the flag rather
than weaken it.

---

## 7. Equations in the form needed for numerical integration

### 7.1 Reduced variables

$$
N=\ln a,\qquad E=\frac{H}{H_0},\qquad
\omega_k=\frac{\rho_k}{3M_{\rm Pl}^2H_0^2}\ \ (k=I,D,{\rm b},r,V),\qquad
\Omega_k=\frac{\omega_k}{E^2},
$$
$$
\omega_m=\omega_I+\omega_D+\omega_b,\qquad E^2=\omega_m+\omega_r+\omega_V,\qquad
\frac{E'}{E}=-\frac32\Omega_m-2\Omega_r .
$$
The background is integrated as
$$
\omega_I'=-\big(3+\tfrac{\Gamma}{H}\big)\omega_I,\quad
\omega_D'=-3\omega_D+b\tfrac{\Gamma}{H}\omega_I,\quad
\omega_V'=(1-b)\tfrac{\Gamma}{H}\omega_I,\quad
\omega_b'=-3\omega_b,\quad \omega_r'=-4\omega_r,
$$
$$
f'=(1-f)\frac{\Gamma}{H},\qquad M'=\frac{f-M}{\tau_MH},\qquad
\frac{\Gamma}{H}=\xi_0\,\frac{a^{p_{\rm act}}}{a^{p_{\rm act}}+a_{\rm act}^{p_{\rm act}}}\,e^{\alpha f+\beta M}.
$$

> **Definition of the coupling function.**
> $$
> \boxed{\;g_c\equiv\frac{\gamma_c}{H}=\frac{\bar Q_V}{H\bar\rho_m}=\frac{\omega_V'}{\omega_m}\;\ge0 . }
> \tag{7.0}
> $$
> *Proof of the last equality:* $\omega_V'=\dot V/(3M_{\rm Pl}^2H_0^2H)=Q_V/(3M_{\rm Pl}^2H_0^2H)$ and
> $\omega_m=\bar\rho_m/(3M_{\rm Pl}^2H_0^2)$; the ratio is $Q_V/(H\bar\rho_m)$. $\square$

### 7.2 The growth equation in $N$

> **Theorem 7.1.** Under (P1)–(P5), $\delta_m(N)$ obeys
> $$
> \boxed{\;\delta_m''+\Big(2+\frac{E'}{E}-g_c\Big)\delta_m'
> -\Big[\frac32\Omega_m+g_c'+\Big(2+\frac{E'}{E}\Big)g_c\Big]\delta_m=0 ,
> \qquad g_c=\frac{\omega_V'}{\omega_m}. }
> \tag{7.1}
> $$
> **Proof (derivation, not a quotation).** Start from (3.2). Convert derivatives with
> $\frac{d}{dt}=H\frac{d}{dN}$:
> $$
> \dot\delta_m=H\delta_m',\qquad
> \ddot\delta_m=H\frac{d}{dN}\big(H\delta_m'\big)=H^2\delta_m''+HH'\delta_m' .
> $$
> Substituting into $\ddot\delta_m+(2H-\gamma_c)\dot\delta_m-\big[\bar\rho_m/(2M_{\rm Pl}^2)+\dot\gamma_c+2H\gamma_c\big]\delta_m=0$
> and dividing by $H^2$:
> $$
> \delta_m''+\frac{H'}{H}\delta_m'+\Big(2-\frac{\gamma_c}{H}\Big)\delta_m'
> -\Big[\frac{\bar\rho_m}{2M_{\rm Pl}^2H^2}+\frac{\dot\gamma_c}{H^2}+\frac{2\gamma_c}{H}\Big]\delta_m=0 .
> $$
> Now use, term by term:
> $H'/H=E'/E$; $\gamma_c/H=g_c$;
> $\dfrac{\bar\rho_m}{2M_{\rm Pl}^2H^2}=\dfrac32\cdot\dfrac{\bar\rho_m}{3M_{\rm Pl}^2H^2}=\dfrac32\Omega_m$;
> and, writing $\gamma_c=g_cH$,
> $$
> \frac{\dot\gamma_c}{H^2}=\frac{H(g_cH)'}{H^2}=\frac{g_c'H+g_cH'}{H}=g_c'+g_c\frac{E'}{E}.
> $$
> Collecting the $\delta_m$ coefficient:
> $\tfrac32\Omega_m+g_c'+g_cE'/E+2g_c=\tfrac32\Omega_m+g_c'+\big(2+E'/E\big)g_c$, which is (7.1).
> $\square$

Equivalently, integrate the first-order system (6.2), which is numerically better conditioned:
$$
\delta_m'=g_c\delta_m-\tilde\vartheta,\qquad
\tilde\vartheta'=-\Big(2+\frac{E'}{E}\Big)\tilde\vartheta-\frac32\Omega_m\delta_m,
\qquad
f_{\rm RSD}=-\frac{\tilde\vartheta}{\delta_m},\qquad
f_g=g_c-\frac{\tilde\vartheta}{\delta_m}=g_c+f_{\rm RSD}.
$$
(The last two are $f_{\rm RSD}\equiv-\vartheta/(H\delta_m)=-\tilde\vartheta/\delta_m$ and
Prop. 4.1. Check against the $\Lambda$CDM matter-domination limit $\tilde\vartheta=-\delta_m$,
$f_{\rm RSD}=f_g=1$.)

### 7.3 Growing-mode initial conditions

Start at $N_i=\ln a_i$ with $a_i$ chosen so that (a) $a_i\gg a_{\rm eq}$ (matter domination) and
(b) $a_i\ll a_{\rm act}$, so that by Note 02, Prop. 3.5, $g_c(a_i)\le\xi_0e^{\alpha+\beta}(a_i/a_{\rm act})^{p_{\rm act}}$
is negligible. A convenient choice is $a_i=10^{-2}$ ($z_i=99$), for which
$g_c\lesssim10^{-9}$ with $a_{\rm act}=0.3$, $p_{\rm act}=6$, $\xi_0e^{\alpha+\beta}=1$.

> **Growing mode.** In the limit $g_c\to0$, $\Omega_m\to1$, $E'/E\to-\tfrac32$, (7.1) becomes
> $\delta_m''+\tfrac12\delta_m'-\tfrac32\delta_m=0$ with roots $r=1$ (growing) and $r=-\tfrac32$
> (decaying). Hence
> $$
> \boxed{\;\delta_m(N_i)=1\ \text{(arbitrary normalisation)},\qquad
> \delta_m'(N_i)=1+\frac{2p+3}{2p+5}\,g_c(N_i),\qquad
> \tilde\vartheta(N_i)=-\Big[1-\frac{2}{2p+5}g_c(N_i)\Big],}
> $$
> with $p=d\ln g_c/dN$ evaluated at $N_i$ (equal to $p_{\rm act}$ there), using Theorem 4.2 to
> include the leading correction. Setting the correction to zero, $\delta_m'(N_i)=1$, changes the
> answer only at $\mathcal O(g_c(N_i))\lesssim10^{-9}$ and is acceptable in practice; it is quoted
> here so that convergence with respect to $a_i$ can be verified.
> Finally, $\sigma_8(z)=\sigma_{8,0}\,\delta_m(z)/\delta_m(0)$ removes the normalisation, and (4.2)
> gives the observable.

**Numerical sanity checks to run.** (i) Setting $\xi_0=0$ must reproduce $\Lambda$CDM growth to
machine precision. (ii) $f_g-f_{\rm RSD}$ must equal $g_c=\omega_V'/\omega_m$ at every step (this is
an exact identity, Prop. 4.1, and is a good integrator diagnostic). (iii) $d\ln(\omega_ma^3\ldots)$:
in reduced variables the identity of Note 01, Thm. 4.1 reads $(\ln\omega_m)'+3=-g_c$, which must hold
to integrator tolerance. (iv) Changing $b$ at fixed $\omega_V'(N)$ must leave $\delta_m(N)$ exactly
unchanged (Theorem 3.1).

---

## What this does not establish

1. **Realization G is assumed, not derived.** Lemma 1.1 shows what the integrability condition
   *implies* given a geodesic clock; it does not show that a fundamental theory produces such a
   clock, nor that the microscopic rate law can actually satisfy the constraint (1.5). The
   overdetermination noted after Proposition 1.3 (three conditions, two unknowns $\delta f,\delta M$)
   is an unresolved structural issue. All that is established is that the *dust sector* closes
   consistently and that the closure is unique given (1.4).
2. **Sec. 2 is a stability argument, not a no-go.** Proposition 2.1 shows that a clumping exact
   vacuum with $\zeta>0$ is ill-posed. It does not exclude the other two options of the draft's
   Sec. 10.1 (momentum transfer with a compensating force; a genuine dark-energy sector with
   $c_s^2>0$). Those are different theories with different, possibly viable, perturbations.
3. **No Boltzmann-code output.** Equations (7.1)/(6.2) are the sub-horizon, late-time, matter-only
   system. The CMB requires the full Einstein–Boltzmann hierarchy with radiation, neutrinos,
   super-horizon modes and the correct initial adiabatic conditions. Nothing here substitutes for
   that computation, and the claims about ISW and $S_8$ in Sec. 5 are directional only.
4. **Single-flow (P2) is an assumption.** If the defects $D$ were to acquire even a small velocity
   dispersion, or if the $I\to D$ conversion transferred momentum, (3.3) would acquire relative
   velocity terms and Theorem 3.1 would hold only up to those corrections.
5. **Linear only.** Theorem 6.1 asserts the absence of a *linear* large-scale instability. Caustics
   of the $c_s^2=0$ flow (arXiv:1704.03367), nonlinear structure formation, halo response to a
   time-varying $\bar\rho_m$, and the validity of the halo model in this background are all
   untouched.
6. **Theorem 4.2 is perturbative in $g_c$ and assumes matter domination.** At $z\lesssim1$, where
   $g_c$ peaks and $\Omega_m<1$, the coefficients $(2p+3)/(2p+5)$ and $2/(2p+5)$ are only
   indicative; the numerical integration of Sec. 7 is the statement to be compared with data.
7. **$\Phi=\Psi$ is assumed (P5).** No anisotropic stress is generated at linear order in this
   closure, but this has not been checked against the four-form realization of the draft's Sec. 3.2.
8. **$b$-invisibility is a linear statement.** Corollary 3.3 does not exclude that nonlinear
   dynamics, or the internal structure and small-scale clustering of the defects, distinguishes $b$.
   Indeed, if the defects are localised objects the model *should* be tested by small-scale probes;
   that lies outside linear theory.
