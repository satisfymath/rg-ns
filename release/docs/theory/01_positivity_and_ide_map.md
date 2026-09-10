# Note 01 — Positivity, the map to interacting dark energy, and the sandwich theorem

**Status.** Theory note for transcription into the paper. Self-contained: every hypothesis is
stated before it is used and referenced by number in the statement of each result.

**Scope.** Background (homogeneous, spatially flat FLRW) dynamics only. Linear perturbations are
treated in Note 03; cosmography in Note 04; the early-universe closure in Note 02.

---

## 0. Setting, notation, and standing hypotheses

Units: $c=\hbar=k_B=1$, signature $(-+++)$, $M_{\rm Pl}^2=(8\pi G)^{-1}$. Overdots are $d/dt$ with
$t$ cosmic time, $H=\dot a/a$, and $a$ is normalised so that $a(t_0)=1$ today. A prime on a
background quantity denotes $d/dN$ with $N=\ln a$.

### 0.1 The background system (S)

$$
\textbf{(S)}\qquad
\begin{aligned}
\dot\rho_I&=-(3H+\Gamma)\rho_I,\\
\dot\rho_D&=-3H\rho_D+b\,\Gamma\rho_I,\\
\dot V&=(1-b)\,\Gamma\rho_I\;\equiv\;Q_V,\\
\dot\rho_b&=-3H\rho_b,\qquad \dot\rho_r=-4H\rho_r,\\
\dot f&=(1-f)\Gamma,\qquad \tau_M\dot M=f-M,\\
3M_{\rm Pl}^2H^2&=\rho_I+\rho_D+\rho_b+\rho_r+V ,
\end{aligned}
$$

with the positive Friedmann root selected. This is system (7.1) of the draft. The total pressure is
$p=\tfrac13\rho_r-V$; the vacuum component is *exact*, $p_V=-V$, so it carries no independent
equation of state parameter.

We write throughout
$$
\rho_{\rm dm}^{\rm eff}\equiv\rho_I+\rho_D,\qquad
\rho_m\equiv\rho_I+\rho_D+\rho_b,\qquad
s\equiv\frac{\rho_I}{\rho_{\rm dm}^{\rm eff}}\in[0,1] .
$$

### 0.2 Standing hypotheses

- **(H1) Data.** $\rho_{Ii},\rho_{Di},\rho_{bi},\rho_{ri},V_i\ge0$, not all zero, $b\in[0,1]$,
  $\tau_M>0$, $f_i\in[0,1)$, $M_i\in[0,1]$.
- **(H2) Rate regularity.** $\Gamma\ge0$ and, along the solution, $t\mapsto\Gamma(t)$ is
  *locally integrable* ($L^1_{\rm loc}$). No lower bound, no boundedness, and no continuity are
  assumed. Solutions are understood in the Carathéodory sense (absolutely continuous functions
  satisfying the integral form of (S) a.e.).
- **(H3) Local existence.** A solution of (S) exists on a maximal forward interval
  $[t_i,T_{\max})$ with $H$ locally bounded there. (Uniqueness is not needed for the positivity
  statements; it is needed for Corollary 1.4.)
- **(H4) Closure.** No sector other than those listed in (S) is present; in particular no component
  with $\rho+p<0$ beyond the exact vacuum $V$.

Hypothesis (H2) is deliberately weak: the whole point of Theorem 1.1 is that positivity is a
*structural* property of the coupling, not a consequence of smoothness or of any bound on $\Gamma$.

---

## 1. Quasi-positivity

### 1.1 The structural statement

Write the density sector of (S) as $\dot x=F(t,x)$ with $x=(\rho_I,\rho_D,V)\in\mathbb R^3$ and
$$
F(t,x)=\big(-(3H+\Gamma)\rho_I,\;-3H\rho_D+b\Gamma\rho_I,\;(1-b)\Gamma\rho_I\big),
$$
the coefficients $H(t),\Gamma(t)$ being regarded as given measurable functions of $t$ along the
trajectory. Let $K=\mathbb R_{\ge0}^3$ be the closed non-negative orthant.

> **Theorem 1.1 (Quasi-positivity / forward invariance).**
> Assume (H1)–(H3). Then $K$ is forward invariant for (S): if $x(t_i)\in K$ then $x(t)\in K$ for
> every $t\in[t_i,T_{\max})$. Moreover the following *explicit* representations hold for all such
> $t$:
> $$
> \rho_I(t)=\rho_{Ii}\,\exp\!\Big[-\!\int_{t_i}^{t}\!\big(3H+\Gamma\big)ds\Big]\ \ge 0,
> \tag{1.1}
> $$
> $$
> \rho_D(t)\,a^3(t)=\rho_{Di}a_i^3+b\!\int_{t_i}^{t}\!\Gamma\rho_I a^3\,ds\ \ge \rho_{Di}a_i^3\ \ge 0,
> \tag{1.2}
> $$
> $$
> V(t)=V_i+(1-b)\!\int_{t_i}^{t}\!\Gamma\rho_I\,ds\ \ge V_i\ \ge 0 .
> \tag{1.3}
> $$
> In particular $\rho_I$ and $V$ are, respectively, non-increasing and non-decreasing in the
> comoving/absolute senses displayed, and $\rho_I\equiv0$ if $\rho_{Ii}=0$.

**Proof.**

*Step 1 (subtangent / Nagumo criterion).* Recall the Nagumo–Brezis subtangent criterion (also
attributed to Kamke and to Bony in the nonsmooth setting): a closed set $K$ is forward invariant for
$\dot x=F(t,x)$ if for a.e.\ $t$ and every $x\in\partial K$ the field is subtangent to $K$ at $x$,
i.e. $\liminf_{h\downarrow0}h^{-1}\operatorname{dist}\!\big(x+hF(t,x),K\big)=0$. For the closed
orthant this reduces to the *Kamke quasi-positivity condition*
$$
x\in K,\ x_k=0\ \Longrightarrow\ F_k(t,x)\ge0 \qquad(k=1,2,3).
\tag{1.4}
$$
Check (1.4) face by face. On $\{\rho_I=0\}\cap K$: $F_1=-(3H+\Gamma)\cdot0=0\ge0$. On
$\{\rho_D=0\}\cap K$: $F_2=b\Gamma\rho_I\ge0$ because $b\ge0$, $\Gamma\ge0$, $\rho_I\ge0$. On
$\{V=0\}\cap K$: $F_3=(1-b)\Gamma\rho_I\ge0$ because $b\le1$. Hence (1.4) holds identically on
$K$ and the orthant is forward invariant.

The structural content of the check is worth isolating, because it is the entire mechanism:

> **Each outflow term in (S) carries the density of its own donor as a factor.**
> The only negative term anywhere in the system is $-\Gamma\rho_I$ in the $\rho_I$ equation
> (and the universal dilution $-3H\rho_k$, which likewise carries $\rho_k$). Therefore *every*
> outflow vanishes identically on the zero set of the component it drains, so no component can be
> pushed through zero.

*Step 2 (a proof that does not need smoothness).* The Nagumo criterion in its classical form
presumes enough regularity for solutions to be well defined; under (H2) $F$ is merely measurable in
$t$, so we give the elementary Carathéodory argument, which also yields (1.1)–(1.3) and is the
version to be transcribed into the paper. The system has a *triangular (cascade) structure*: the
$\rho_I$ equation is autonomous in $\rho_I$ given the coefficients; $\rho_D$ is driven by $\rho_I$;
$V$ is driven by $\rho_I$.

(i) $\rho_I$: the equation $\dot\rho_I=-(3H+\Gamma)\rho_I$ is linear and homogeneous with
$L^1_{\rm loc}$ coefficient, so the integrating factor
$\mu(t)=\exp[\int_{t_i}^t(3H+\Gamma)ds]$ is absolutely continuous and positive, $(\mu\rho_I)^{\textstyle\cdot}=0$
a.e., hence $\mu\rho_I$ is constant and (1.1) follows. The exponential is strictly positive, so
$\operatorname{sign}\rho_I(t)=\operatorname{sign}\rho_{Ii}$ for all $t$; with $\rho_{Ii}\ge0$ we get
$\rho_I\ge0$, and $\rho_{Ii}=0$ gives $\rho_I\equiv0$.

(ii) $\rho_D$: multiply by $a^3$. Then $(\rho_Da^3)^{\textstyle\cdot}=b\Gamma\rho_Ia^3$ a.e.; the
right-hand side is non-negative by (i) and $L^1_{\rm loc}$, so $\rho_Da^3$ is non-decreasing and
(1.2) holds. Since $a^3>0$, $\rho_D\ge0$.

(iii) $V$: directly $\dot V=(1-b)\Gamma\rho_I\ge0$ a.e., giving (1.3).

(iv) $\rho_b,\rho_r$: exact exponentials, positivity immediate.

No step used a lower bound on $\Gamma$, boundedness of $\Gamma$, or continuity. $\square$

**Remark 1.2 (why this is stronger than "the source is positive").** The naive argument
"$Q_V\ge0$ so $V$ grows" is true but does not by itself prevent $\rho_I$ from being driven negative:
that requires the donor's loss term to be *proportional to the donor*. Positivity of the source and
proportionality of the sink are logically independent, and it is the second that does the work.

### 1.3 Correction to the draft

The draft proves positivity inside **Theorem 1** (Sec. 7.4) but under hypothesis 3 of that theorem,
which assumes $0<g\le\Gamma\le G<\infty$ *and* local Lipschitz continuity. Theorem 1.1 above shows
that positivity needs *neither* bound and *no* continuity — only $\Gamma\ge0$ and local
integrability. This matters, because Note 02 will be forced to abandon the lower bound $\Gamma\ge g>0$
(it has no viable early universe), and we must know in advance that positivity survives that
amputation. The Lipschitz hypothesis remains necessary for *uniqueness*, not for positivity.

> **Corollary 1.4 (global forward existence, restated minimally).**
> Assume (H1)–(H4), and in addition that $\Gamma$ is locally Lipschitz in the dynamical variables so
> that solutions are unique. Then $T_{\max}=\infty$. *Proof.* By Theorem 1.1 all densities are
> non-negative, hence $3M_{\rm Pl}^2H^2=\rho_{\rm tot}\ge0$ and $H$ is real. Summing (S),
> $\dot\rho_{\rm tot}=-3H(\rho_m+\tfrac43\rho_r)\le0$ once $H>0$, so $\rho_{\rm tot}\le\rho_{{\rm tot},i}$
> and $0<H\le H_i$; also $a\le e^{H_i(t-t_i)}$ and, by (1.1)–(1.3),
> $\rho_I\le\rho_{Ii}a^{-3}$, $\rho_Da^3\le\rho_{Di}+b\rho_{Ii}$, $V\le V_i+(1-b)\rho_{Ii}$. All
> variables remain in a compact set on any finite interval, so no blow-up occurs and the local
> solution continues. $\square$ (This reproduces the draft's (7.6)–(7.9) with the weakened rate
> hypothesis.)

---

## 2. Why the standard IDE parametrisations fail this test

### 2.1 The two standard families

The literature on interacting dark energy overwhelmingly uses one of
$$
\textbf{(A)}\quad
\begin{cases}
\dot\rho_{\rm dm}+3H\rho_{\rm dm}=-\,\xi H\rho_{\rm de},\\[2pt]
\dot\rho_{\rm de}+3H(1+w)\rho_{\rm de}=+\,\xi H\rho_{\rm de},
\end{cases}
\qquad
\textbf{(B)}\quad
\begin{cases}
\dot\rho_{\rm dm}+3H\rho_{\rm dm}=+\,\xi H\rho_{\rm dm},\\[2pt]
\dot\rho_{\rm de}+3H(1+w)\rho_{\rm de}=-\,\xi H\rho_{\rm dm},
\end{cases}
$$
(and sign-flipped variants), i.e. the transfer term is proportional to the density of the
*recipient*, not of the *donor*.

> **Proposition 2.1 (failure of quasi-positivity for (A) and (B)).**
> Fix $\xi>0$, $H>0$.
> (a) In family (A), on the face $\{\rho_{\rm dm}=0,\ \rho_{\rm de}>0\}$ the field component is
> $F_{\rm dm}=-\xi H\rho_{\rm de}<0$: the Kamke condition (1.4) fails, and any trajectory reaching
> $\rho_{\rm dm}=0$ with $\rho_{\rm de}>0$ crosses transversally into $\rho_{\rm dm}<0$.
> (b) In family (B), on the face $\{\rho_{\rm de}=0,\ \rho_{\rm dm}>0\}$ we get
> $F_{\rm de}=-\xi H\rho_{\rm dm}<0$: same conclusion for $\rho_{\rm de}$.
> (c) In both cases the crossing is not a removable artefact of the numerical solver: the exact
> solution of the linear ODE
> $\frac{d}{dN}(\rho_{\rm dm}a^3)=-\xi\rho_{\rm de}a^3$ has $\rho_{\rm dm}a^3$ strictly decreasing
> whenever $\rho_{\rm de}>0$, and the driving term does not switch off as $\rho_{\rm dm}\to0^+$.
>
> **Proof.** (a),(b) are direct evaluations of (1.4). For (c): with $\xi,\rho_{\rm de}>0$ the map
> $N\mapsto\rho_{\rm dm}a^3$ is strictly decreasing with derivative bounded away from $0$ on any
> interval where $\rho_{\rm de}a^3\ge\epsilon>0$; it therefore reaches and passes zero in finite
> $N$ unless $\rho_{\rm de}a^3$ is integrable to the future and small enough, which is a fine-tuned
> condition on the parameters rather than a structural property. $\square$

**Remark 2.2 (relation to the catalogued numerical failures).** This is the mechanism behind the
negative dark-sector densities reported by van der Westhuizen, Abebe & Di Valentino
(arXiv:2509.04494, arXiv:2509.04495, arXiv:2509.04496), who find explicitly negative densities in
7 of the 8 interacting models they survey. Proposition 2.1 says the failures are not accidents of
parameter choice: the coupling structure of families (A) and (B) violates the Kamke condition on a
codimension-one face of the physical region, so the negative-density region is entered through an
open set of initial data and coupling strengths. Conversely, a model in which every outflow is
proportional to its own donor — as in (S) — cannot exhibit the pathology at all, by Theorem 1.1.
We claim no priority for the Nagumo/Kamke criterion, which is classical; the observation is that
it is the correct diagnostic for this class of cosmologies.

### 2.3 Backward invariance fails — the origin of $a_{\min}$

> **Proposition 2.3 (no backward invariance for $V$).**
> Assume (H1)–(H3) and additionally $b<1$, $\rho_{Ii}>0$ and $\Gamma>0$ on a set of positive
> measure. Run (S) backwards from $t_0$. Then $V$ is non-increasing towards the past, and it
> reaches $0$ at a finite $a=a_{\min}>0$ whenever
> $$
> V_0=V(t_0)\;<\;(1-b)\int_{-\infty}^{t_0}\Gamma\rho_I\,dt' ,
> \tag{2.1}
> $$
> the integral being taken along the backward continuation. In that case the physical branch of the
> model is $a\ge a_{\min}$.
>
> **Proof.** Time reversal $t\to-t$ maps (S) to a system in which the $V$ equation reads
> $dV/d(-t)=-(1-b)\Gamma\rho_I$: the loss term is proportional to $\rho_I$, *not* to $V$, so the
> Kamke condition (1.4) fails on the face $\{V=0,\rho_I>0\}$ exactly as in Proposition 2.1(b).
> Integrating (1.3) backwards gives $V(t)=V_0-(1-b)\int_t^{t_0}\Gamma\rho_I dt'$, which is a
> continuous decreasing function of $-t$; under (2.1) it has a zero at finite time, which defines
> $a_{\min}$. $\square$

**Consistency check with the draft.** For the solvable family $\Gamma=\xi H$ (draft Sec. 8.1–8.2)
one has $V=V_i+\frac{(1-b)\xi}{3+\xi}\rho_{Ii}(1-a^{-n})$ with $n=3+\xi$, whose zero is
$$
a_{\min}=\Big[1+\frac{(3+\xi)V_i}{(1-b)\xi\rho_{Ii}}\Big]^{-1/(3+\xi)},
$$
i.e. the draft's (8.6). Proposition 2.3 identifies this as a *structural* fact — the vacuum is a
pure recipient, and recipients are not protected in reverse time — rather than an accident of the
$\Gamma=\xi H$ ansatz. It is also the precise reason that Note 02 must introduce an activation
function: something must switch $\Gamma$ off in the past, or $V$ goes negative.

> **Summary of the asymmetry.** Forward in time the model is protected on all three faces.
> Backwards it is protected on $\{\rho_I=0\}$ (the exponential (1.1) never reaches zero) but
> unprotected on $\{V=0\}$ and, if $\rho_{Di}$ is small, on $\{\rho_D=0\}$. Irreversibility of the
> conversion and one-sided invariance of the orthant are the same statement.

---

## 3. Exact map onto the standard IDE language

> **Hypotheses (H1)–(H4) as above. Definitions:**
> $\rho_{\rm dm}^{\rm eff}=\rho_I+\rho_D$, $s=\rho_I/\rho_{\rm dm}^{\rm eff}$ (set $s=0$ when
> $\rho_{\rm dm}^{\rm eff}=0$), $Q_V=(1-b)\Gamma\rho_I$.

> **Proposition 3.1 (the model is an IDE model of type "$Q\propto\rho_{\rm dm}$", with a
> state-dependent coupling).**
> Under (H1)–(H4),
> $$
> \dot\rho_{\rm dm}^{\rm eff}+3H\rho_{\rm dm}^{\rm eff}=-Q_V,\qquad \dot V=+Q_V,
> \tag{3.1}
> $$
> and
> $$
> \boxed{\;Q_V=\xi_{\rm eff}\,H\,\rho_{\rm dm}^{\rm eff},\qquad
> \xi_{\rm eff}=\frac{(1-b)\,\Gamma\,s}{H}\;\ge\;0 .}
> \tag{3.2}
> $$
> Furthermore $0\le\xi_{\rm eff}\le(1-b)\Gamma/H$, with the upper bound attained iff $\rho_D=0$.
>
> **Proof.** Add the first two equations of (S):
> $\dot\rho_I+\dot\rho_D+3H(\rho_I+\rho_D)=-\Gamma\rho_I+b\Gamma\rho_I=-(1-b)\Gamma\rho_I=-Q_V$,
> which is (3.1); the second half of (3.1) is the third line of (S). For (3.2) write
> $\rho_I=s\rho_{\rm dm}^{\rm eff}$ and divide by $H\rho_{\rm dm}^{\rm eff}$, legitimate since
> $H>0$ by Corollary 1.4. Non-negativity of $\xi_{\rm eff}$ follows from $\Gamma\ge0$, $b\le1$,
> $s\ge0$, $H>0$. The bound follows from $s\le1$. $\square$

> **Corollary 3.2 (exact coincidence with $Q=\xi H\rho_{\rm dm}$).**
> The background of (S) coincides with the constant-coupling model
> $\dot\rho_{\rm dm}+3H\rho_{\rm dm}=-\xi H\rho_{\rm dm}$, $\dot\rho_{\rm de}=+\xi H\rho_{\rm dm}$,
> $w_{\rm de}=-1$, for a *constant* $\xi>0$ **iff**
> $$
> (1-b)\,\Gamma(t)\,s(t)=\xi H(t)\quad\text{for all }t .
> $$
> If in addition $\rho_{Di}=0$, this forces $b=0$ (hence $s\equiv1$ by (1.2)) and $\Gamma=\xi H$ —
> precisely the solvable family of the draft's Sec. 8.1.
>
> **Proof.** The "iff" is (3.2). For the second statement: if $b>0$ and $\rho_{Ii}>0$ then by (1.2)
> $\rho_Da^3$ is strictly increasing as soon as $\Gamma>0$, so $s<1$ and $s$ is a non-constant
> function of time. Then $(1-b)\Gamma s=\xi H$ can still be solved for $\Gamma$, but $\Gamma$ is no
> longer of the postulated exponential-memory form (6.6) of the draft; if one insists on
> $\Gamma=\Gamma_0e^{\alpha f+\beta M}$ *and* $\Gamma\propto H$ with constant proportionality, then
> $s$ must be constant, which by (1.2)–(1.3) requires $b\Gamma\rho_I\equiv0$, i.e. $b=0$. $\square$

> **Proposition 3.3 (the model can never take the form $Q\propto\rho_{\rm de}$).**
> There is no function $\chi$ with $\chi(V)>0$ for $V>0$ such that $Q_V=\chi(V)$ identically along
> all solutions of (S).
>
> **Proof.** Consider two solutions with the same $V(t_1)=V_\star>0$ at some time $t_1$ but with
> $\rho_I(t_1)=0$ in the first (take $\rho_{Ii}=0$, $V_i=V_\star$, allowed by (H1)) and
> $\rho_I(t_1)>0$, $\Gamma(t_1)>0$ in the second. By (1.1) the first has $\rho_I\equiv0$, hence
> $Q_V(t_1)=0$; the second has $Q_V(t_1)=(1-b)\Gamma\rho_I>0$ whenever $b<1$. A function of $V$
> alone cannot take two values at $V=V_\star$. $\square$

**Interpretation.** Equation (3.2) is the honest translation dictionary: *whatever* an IDE
pipeline reports as $\xi$, the model predicts that quantity to be non-negative, time-dependent, and
suppressed at early times by both $S(a)$ (Note 02) and $s(a)$. In particular the model does not live
in the $Q\propto\rho_{\rm de}$ half of the standard model space at all, and Proposition 2.1 says
that is exactly the half where negative densities occur.

---

## 4. The no-sign-flip theorem

The single most compact falsifiable statement of the background model.

> **Definition.** $\displaystyle \delta_{\rm eff}(a)\equiv\frac{d\ln\!\big(\rho_{\rm dm}^{\rm eff}a^3\big)}{d\ln a}$.
> $\delta_{\rm eff}=0$ is exactly conserved (non-interacting) dark matter; $\delta_{\rm eff}<0$
> means dark matter is losing energy; $\delta_{\rm eff}>0$ means it is gaining.

> **Theorem 4.1 (no sign flip, with or without memory).**
> Assume (H1)–(H4) and $\rho_{\rm dm}^{\rm eff}>0$. Then for every admissible rate law $\Gamma\ge0$
> — in particular for every $\Gamma_0\ge0$, $\alpha\ge0$, $\beta\ge0$, $\tau_M>0$ in
> $\Gamma=\Gamma_0e^{\alpha f+\beta M}$, and for every activation profile $S(a)\in[0,1]$ of Note 02 —
> $$
> \boxed{\;\delta_{\rm eff}(a)=-\frac{Q_V}{H\rho_{\rm dm}^{\rm eff}}=-\,\xi_{\rm eff}(a)\;\le\;0
> \quad\text{for all }a,\;}
> \tag{4.1}
> $$
> with equality at a given $a$ iff $\Gamma(a)\rho_I(a)=0$ or $b=1$. The same statement holds for the
> total dust, $d\ln(\rho_ma^3)/d\ln a=-Q_V/(H\rho_m)\le0$.
>
> **Proof.** From (3.1), $\frac{d}{dt}(\rho_{\rm dm}^{\rm eff}a^3)=-Q_Va^3$. Divide by
> $\rho_{\rm dm}^{\rm eff}a^3>0$ and by $H>0$:
> $\delta_{\rm eff}=\frac{1}{H}\frac{d}{dt}\ln(\rho_{\rm dm}^{\rm eff}a^3)=-Q_V/(H\rho_{\rm dm}^{\rm eff})$.
> By Theorem 1.1, $\Gamma\ge0$ and $\rho_I\ge0$, so $Q_V=(1-b)\Gamma\rho_I\ge0$; with $H>0$ the
> sign follows. Baryons contribute $\dot\rho_ba^3=0$, so adding them changes the denominator only. $\square$

> **Corollary 4.2 (memory is invisible in the sign).**
> The memory parameters $(\beta,\tau_M)$ enter (4.1) only through the scalar $\Gamma\ge0$. They can
> change the *magnitude* of $\delta_{\rm eff}$ by the bounded factor $e^{\beta M}\in[1,e^{\beta}]$
> and can shift the *epoch* at which $|\delta_{\rm eff}|$ peaks (through $M$'s lag $\tau_M$), but
> they cannot change $\operatorname{sign}\delta_{\rm eff}$. In this precise sense memory is a
> second-order observable at background level; Note 04 shows where it *does* appear (the snap).

### 4.3 Honest confrontation with data

DESI DR2-era interacting-dark-energy fits weakly prefer the *opposite* sign, i.e. energy flowing
from dark energy into dark matter, equivalently $\delta_{\rm eff}>0$ / $\xi_{\rm eff}<0$
(arXiv:2607.12283, arXiv:2608.21938). We state this plainly:

- Theorem 4.1 is not a fitted feature and cannot be fitted away. It follows from the single
  postulate that the conversion is one-way, $\Gamma\ge0$.
- Therefore **a robust detection of $\delta_{\rm eff}>0$ falsifies the one-way model (Track A)**,
  independently of $b$, $\alpha$, $\beta$, $\tau_M$, and of the activation profile.
- The current preference is weak and is entangled with the choice of $Q$ parametrisation — and,
  by Proposition 2.1, some of the parametrisations carrying that preference are the ones that admit
  negative densities. That is an argument for re-running such analyses with a
  quasi-positive coupling, not an argument for dismissing the data.
- The disciplined response, if the preference strengthens, is Track B (Sec. 6 below), which is a
  *different physical model*, not a reparametrisation of this one.

---

## 5. The sandwich theorem and the death of the "phantom appearance" argument

### 5.1 Statement

> **Hypotheses.** (H1)–(H4), plus:
> **(H5)** the solution is defined and non-negative on $[t_e,t_0]$ with $a(t_e)=a_e>0$ and
> $a(t_0)=1$; **(H6)** radiation is exactly conserved, $\rho_r=\rho_{r0}a^{-4}$.
>
> **Definitions.** $m(t)\equiv\rho_m(t)a^3(t)$ (comoving total dust), $\rho_{m0}\equiv m(t_0)$,
> $\rho_m^{\rm early}\equiv m(t_e)$, $V_0\equiv V(t_0)$, $\rho_{{\rm crit},0}\equiv3M_{\rm Pl}^2H_0^2$,
> and the **matter deficit**
> $$
> \boxed{\;\Delta\;\equiv\;\frac{\rho_m^{\rm early}-\rho_{m0}}{\rho_{{\rm crit},0}}
> \;=\;\frac{1}{3M_{\rm Pl}^2H_0^2}\int_{t_e}^{t_0}Q_V\,a^3\,dt\;\ge\;0 .}
> \tag{5.1}
> $$

> **Theorem 5.1 (Sandwich).** Under (H1)–(H6), define two spatially flat $\Lambda$CDM comparison
> models by
> $$
> 3M_{\rm Pl}^2H_{\rm low}^2(a)=\rho_{m0}a^{-3}+\rho_{r0}a^{-4}+V_0 ,
> $$
> $$
> 3M_{\rm Pl}^2H_{\rm high}^2(a)=\rho_m^{\rm early}a^{-3}+\rho_{r0}a^{-4}+\Lambda_{\rm high},
> \qquad \Lambda_{\rm high}\equiv V_0-\big(\rho_m^{\rm early}-\rho_{m0}\big).
> $$
> Then **both comparison models have exactly the observed $H_0$**,
> $H_{\rm low}(1)=H_{\rm high}(1)=H_0$, and for all $a\in[a_e,1]$
> $$
> \boxed{\;3M_{\rm Pl}^2H_{\rm low}^2(a)\;\le\;3M_{\rm Pl}^2H^2(a)\;\le\;3M_{\rm Pl}^2H_{\rm high}^2(a)\;}
> \tag{5.2}
> $$
> with equality on both sides at $a=1$. In reduced variables the sandwich reads
> $$
> E^2_{\Lambda{\rm CDM}}\big(\Omega_{m0},\,\Omega_{V0}\big)\;\le\;E^2(a)\;\le\;
> E^2_{\Lambda{\rm CDM}}\big(\Omega_{m0}+\Delta,\,\Omega_{V0}-\Delta\big),
> \tag{5.3}
> $$
> i.e. *the expansion history is bracketed by two flat $\Lambda$CDM models with the same $H_0$ that
> differ only by moving the amount $\Delta$ from $\Lambda$ to matter.*

**Proof.** Write $3M_{\rm Pl}^2H^2(a)=m(t)a^{-3}+\rho_{r0}a^{-4}+V(t)$, exact by the Friedmann
constraint in (S) and (H6). From (3.1) and (1.3),
$$
\dot m=-Q_Va^3,\qquad \dot V=+Q_V .
\tag{5.4}
$$

*Lower bound.* For $t\le t_0$,
$m(t)-m(t_0)=\int_t^{t_0}Q_Va'^3dt'$ and $V(t)-V(t_0)=-\int_t^{t_0}Q_Vdt'$, whence
$$
3M_{\rm Pl}^2\big[H^2(a)-H_{\rm low}^2(a)\big]
=\big[m(t)-\rho_{m0}\big]a^{-3}+\big[V(t)-V_0\big]
=\int_t^{t_0}Q_V\Big[\Big(\frac{a'}{a}\Big)^{3}-1\Big]dt' .
\tag{5.5}
$$
Since $a$ is non-decreasing (H>0) and $t'\ge t$, we have $a'\ge a$, so the bracket is $\ge0$; and
$Q_V\ge0$ by Theorem 1.1. Hence the integral is $\ge0$, which is the left inequality, with equality
at $t=t_0$ (empty integration range).

*Upper bound.* Using $\Lambda_{\rm high}=V_0-\rho_m^{\rm early}+\rho_{m0}$,
$$
3M_{\rm Pl}^2\big[H^2(a)-H_{\rm high}^2(a)\big]
=\big[m(t)-\rho_m^{\rm early}\big]a^{-3}+V(t)-V_0+\rho_m^{\rm early}-\rho_{m0}.
$$
Insert $m(t)-\rho_m^{\rm early}=-\int_{t_e}^{t}Q_Va'^3dt'$, $V(t)-V_0=-\int_{t}^{t_0}Q_Vdt'$, and
$\rho_m^{\rm early}-\rho_{m0}=\int_{t_e}^{t_0}Q_Va'^3dt'$. Splitting the last integral at $t$ and
cancelling,
$$
3M_{\rm Pl}^2\big[H^2(a)-H_{\rm high}^2(a)\big]
=\int_{t_e}^{t}Q_V\,a'^3\Big[1-\frac{1}{a^{3}}\Big]dt'
\;+\;\int_{t}^{t_0}Q_V\big[a'^3-1\big]dt' .
\tag{5.6}
$$
In the first integral $a\le1$ gives $1-a^{-3}\le0$; in the second $a'\le1$ gives $a'^3-1\le0$.
Both integrands are therefore $\le0$, proving the right inequality; at $a=1$ the first bracket
vanishes and the second integration range is empty, so equality holds. Finally
$H_{\rm low}(1)^2=(\rho_{m0}+\rho_{r0}+V_0)/(3M_{\rm Pl}^2)=H_0^2$ by the Friedmann constraint at
$t_0$, and $H_{\rm high}(1)^2=(\rho_m^{\rm early}+\rho_{r0}+\Lambda_{\rm high})/(3M_{\rm Pl}^2)=H_0^2$
by the definition of $\Lambda_{\rm high}$. Equation (5.3) follows on dividing by
$3M_{\rm Pl}^2H_0^2$ and using (5.1). $\square$

> **Remark 5.2 (a bound that looks right and is not).** The pair
> $\big(\rho_m^{\rm early},V_{\rm early}\big)$ does **not** bound $H$ from above. Repeating the
> computation with $3M_{\rm Pl}^2H_e^2(a)=\rho_m^{\rm early}a^{-3}+\rho_{r0}a^{-4}+V(t_e)$ gives
> $$
> 3M_{\rm Pl}^2\big[H^2(a)-H_e^2(a)\big]=\int_{t_e}^{t}Q_V\Big[1-\Big(\frac{a'}{a}\Big)^{3}\Big]dt'\;\ge\;0 ,
> $$
> because $a'\le a$ on $[t_e,t]$. So the early-anchored model is a *lower* bound, not an upper one,
> and it has $H_e(1)>H_0$, i.e. it does not share $H_0$. The correct upper member of the sandwich
> must renormalise $\Lambda$ by exactly the deficit, as in Theorem 5.1. We record this because the
> naive version is easy to write down and is wrong.

> **Corollary 5.3 (bounds on derived quantities).** On $a\in[a_e,1]$,
> $$
> 0\;\le\;E^2(a)-\big[\Omega_{m0}a^{-3}+\Omega_{r0}a^{-4}+\Omega_{V0}\big]\;\le\;\Delta\,(a^{-3}-1),
> $$
> so the fractional deviation from today-anchored $\Lambda$CDM is at most
> $\Delta(a^{-3}-1)/E^2$, which vanishes at $a=1$ and, for $a\ll1$, tends to
> $\Delta/\Omega_{m0}$. *Proof.* Subtract $E^2_{\rm low}$ from (5.3) and use
> $E^2_{\rm high}-E^2_{\rm low}=\Delta(a^{-3}-1)$. $\square$
> Thus $\Delta$ is a *sufficient* statistic for how far the background can wander from $\Lambda$CDM,
> and it is bounded above by $\Omega_{V0}$ if $\Lambda_{\rm high}\ge0$ is required.

### 5.4 Correction to the draft: the "phantom appearance" of Sec. 7.7 is an anchoring artefact

The draft (Sec. 7.7, eq. (7.13)) introduces a bookkeeping parameter through
$\dot V+3H(1+w_{V,\rm eff})V=0$, obtaining $w_{V,\rm eff}=-1-Q_V/(3HV)\le-1$, and comments that this
"is not automatically the $w(z)$ an observational fit would infer". That caveat is correct but far
too weak: the sign itself is not an invariant. We replace the discussion with the following
proposition, which should be transcribed in place of Sec. 7.7.

> **Proposition 5.5 (three legitimate $w$'s for one $H(a)$).**
> Fix a solution of (S) with $\rho_r$ negligible. Suppose an analyst assumes conserved dust of
> present density $\rho_m^{\rm fit}$ and attributes the remainder to a dark-energy fluid,
> $$
> \rho_{\rm DE}^{\rm fit}(a)\equiv3M_{\rm Pl}^2H^2(a)-\rho_m^{\rm fit}a^{-3},
> \qquad
> 1+w_{\rm fit}=-\frac{1}{3H}\frac{\dot\rho_{\rm DE}^{\rm fit}}{\rho_{\rm DE}^{\rm fit}} .
> $$
> Then, wherever $\rho_{\rm DE}^{\rm fit}>0$,
> $$
> \boxed{\;1+w_{\rm fit}(a)=\frac{\big[m(t)-\rho_m^{\rm fit}\big]a^{-3}}{\rho_{\rm DE}^{\rm fit}(a)}\;}
> \tag{5.7}
> $$
> and consequently
> $$
> \rho_m^{\rm fit}=\rho_{m0}\ \Rightarrow\ w_{\rm fit}\ge-1\ \text{(quintessence-like)},\qquad
> \rho_m^{\rm fit}=\rho_m^{\rm early}\ \Rightarrow\ w_{\rm fit}\le-1\ \text{(phantom-like)},
> $$
> while the *physical* vacuum has $p_V=-V$, i.e. $w_V=-1$ exactly, and the draft's (7.13) gives yet
> a third value $w_{V,\rm eff}\le-1$. All four statements describe the *same* $H(a)$.
>
> **Proof.** Differentiate $\rho_{\rm DE}^{\rm fit}=[m(t)-\rho_m^{\rm fit}]a^{-3}+V(t)$ using (5.4):
> $$
> \dot\rho_{\rm DE}^{\rm fit}=-Q_Va^3\cdot a^{-3}-3H\big[m-\rho_m^{\rm fit}\big]a^{-3}+Q_V
> =-3H\big[m-\rho_m^{\rm fit}\big]a^{-3}.
> $$
> Dividing by $-3H\rho_{\rm DE}^{\rm fit}$ gives (5.7). Since $m$ is non-increasing in $t$ (by
> (5.4) and $Q_V\ge0$), $m(t)\ge m(t_0)=\rho_{m0}$ and $m(t)\le m(t_e)=\rho_m^{\rm early}$ for
> $t\in[t_e,t_0]$, which fixes the two signs. $\square$

**Consequences to be stated in the paper.**

1. Reporting "this model looks phantom" or "this model looks quintessence-like" is meaningless
   without stating the anchor. A CPL fit anchored by CMB-calibrated $\omega_m$ at recombination
   sits near the phantom branch of (5.7); a fit that lets $\Omega_m$ float and is dominated by
   low-$z$ distances sits near the quintessence branch. A referee will notice this immediately if
   we do not say it first.
2. The anchoring-independent content of the background model is precisely the triple
   $$
   \boxed{\;\big\{\,H(z),\ j(z),\ \Delta\,\big\}\;}
   $$
   — the expansion history itself, the jerk (Note 04, which is a local functional of $H$ and its
   derivatives and therefore anchor-free), and the matter deficit $\Delta$ of (5.1), which is by
   construction the difference between two *physically defined* comoving dust densities and does
   not require a dark-energy parametrisation at all.
3. $\Delta$ is directly the quantity a joint CMB+BAO+SNe analysis measures as a mismatch between
   $\omega_m$ inferred at recombination and $\Omega_m h^2$ inferred at $z\lesssim2$, at fixed $H_0$.
   Theorem 5.1 guarantees that mismatch is one-signed: $\Delta\ge0$, early matter is always
   *larger*.

---

## 6. Track B: adding a reverse channel

### 6.1 The modified system

> **System (S$_\downarrow$).** Replace the $V$ and $\rho_D$ equations of (S) by
> $$
> \dot V=(1-b)\Gamma\rho_I-\Gamma_\downarrow V,\qquad
> \dot\rho_D=-3H\rho_D+b\Gamma\rho_I+\Gamma_\downarrow V ,
> $$
> keeping everything else, with **(H2$'$)** $\Gamma\ge0$, $\Gamma_\downarrow\ge0$, both
> $L^1_{\rm loc}$ along the solution. Define the *net* transfer
> $$
> Q_V^{\rm net}\equiv(1-b)\Gamma\rho_I-\Gamma_\downarrow V .
> $$

> **Proposition 6.1 (positivity survives).** Under (H1), (H2$'$), (H3), the orthant
> $\{\rho_I,\rho_D,V\ge0\}$ is forward invariant for (S$_\downarrow$).
>
> **Proof.** Kamke condition (1.4) again. On $\{\rho_I=0\}$: $F_1=0$. On $\{\rho_D=0\}$:
> $F_2=b\Gamma\rho_I+\Gamma_\downarrow V\ge0$. On $\{V=0\}$:
> $F_3=(1-b)\Gamma\rho_I-\Gamma_\downarrow\cdot0=(1-b)\Gamma\rho_I\ge0$. The new outflow
> $-\Gamma_\downarrow V$ is proportional to *its own* donor $V$ and therefore vanishes on the face
> it could have violated — the same structural mechanism as Theorem 1.1. Carathéodory version: the
> pair $(\rho_I,V)$ is no longer triangular, but the system is *cooperative off-diagonal*
> (all off-diagonal coefficients of the linear-in-$x$ field are $\ge0$), so the Kamke theorem for
> quasi-monotone systems applies; alternatively, apply the integrating factor
> $\exp[\int\Gamma_\downarrow]$ to $V$ and $\exp[\int3H]$ to $\rho_D$ and iterate the Picard scheme,
> which preserves the orthant at every step and converges. $\square$

> **Proposition 6.2 (sign flip of $\delta_{\rm eff}$).** For (S$_\downarrow$),
> $\dot\rho_{\rm dm}^{\rm eff}+3H\rho_{\rm dm}^{\rm eff}=-Q_V^{\rm net}$ and
> $$
> \delta_{\rm eff}=-\frac{Q_V^{\rm net}}{H\rho_{\rm dm}^{\rm eff}}
> =-\frac{(1-b)\Gamma\rho_I-\Gamma_\downarrow V}{H\rho_{\rm dm}^{\rm eff}},
> $$
> so $\delta_{\rm eff}>0$ **iff** $\Gamma_\downarrow V>(1-b)\Gamma\rho_I$. If $\Gamma_\downarrow$ is
> bounded below by a positive constant at late times and $\Gamma$ carries an activation profile that
> saturates while $\rho_I\propto a^{-3}\!\!\cdot\!(1-f)$ decays, then $\rho_I/V\to0$ and the
> inequality holds for all sufficiently late times: **the flip is generic, not tuned.**
>
> **Proof.** The first display repeats the proof of Proposition 3.1 with the extra term; note that
> $\Gamma_\downarrow V$ enters $\rho_D$ with a $+$ and $V$ with a $-$, so it survives the sum with a
> $+$ into $\rho_{\rm dm}^{\rm eff}$. The sign statement is immediate. For genericity: by (1.1)
> $\rho_I a^3\le\rho_{Ii}$ so $\rho_I\to0$, while by Theorem 1.1 applied to the forward $V$ equation
> with source $\ge0$, $V$ is bounded below by $V_\star e^{-\int\Gamma_\downarrow}$ from any time at
> which $V=V_\star>0$; if $\int^\infty\Gamma_\downarrow dt$ converges (e.g. $\Gamma_\downarrow$
> decaying no slower than $H$ with $H\to H_\infty>0$ excluded, or simply $\Gamma_\downarrow$
> constant with a de Sitter attractor rebalancing), $V$ stays bounded away from $0$ and
> $\Gamma_\downarrow V/[(1-b)\Gamma\rho_I]\to\infty$. $\square$

> **Corollary 6.3 (the discriminator).** By Note 04, $j-1=2\Omega_r+Q_V^{\rm net}/(2M_{\rm Pl}^2H^3)$
> in both tracks, with $Q_V\to Q_V^{\rm net}$. Hence
> $$
> \boxed{\;\text{Track A}\Rightarrow j>1+2\Omega_r\ \text{always};\qquad
> \text{Track B}\Rightarrow j<1+2\Omega_r\ \text{once the reverse channel dominates.}}
> $$
> $\operatorname{sign}(j-1)$ at low redshift is therefore the observational discriminator between
> the two tracks, and it is *the same* quantity that discriminates the model from running-vacuum and
> CPL alternatives (Note 04, Prop. 2).

**Note on the cost of Track B.** The reverse channel destroys the interpretation of the conversion
as a genuine absorbing-state process: with $\Gamma_\downarrow>0$ the "absorbed" state is no longer
absorbing at the level of energy, and the survival identity (1.1) for $\rho_I$ survives but the
identities (7.3)–(7.4) of the draft relating $\rho_D$ to $f$ do not. Track B should be presented as
a distinct model with a distinct microphysical story (vacuum decaying into defects), not as a
parameter extension of Track A.

---

## What this does not establish

1. **Nothing about inhomogeneous general relativity.** Theorem 1.1 and Corollary 1.4 concern an ODE
   system obtained by imposing exact FLRW symmetry. They say nothing about global existence for the
   Einstein equations with generic data, about shell crossing, caustics of the pressureless flow, or
   gravitational singularities. In particular the $c_s^2=0$ dust sector is expected to develop
   caustics at the nonlinear level (see Note 03, Sec. 6).
2. **No derivation of the rate law.** $\Gamma\ge0$ is a postulate. Theorem 1.1 holds for *every*
   non-negative $\Gamma$, which is a strength for robustness and a weakness for predictivity: the
   theorem cannot be used as evidence for the specific memory law $\Gamma_0e^{\alpha f+\beta M}$.
3. **No claim of novelty for Nagumo/Kamke.** The subtangent criterion is classical. What is (as far
   as we are aware) not standard in the cosmological IDE literature is its systematic use as an
   admissibility filter on couplings $Q$; we have not performed a bibliographic search sufficient to
   claim priority for that use either.
4. **The sandwich theorem does not bound observables directly.** Theorem 5.1 bounds $H^2(a)$ pointwise
   in $a$. Distance moduli, BAO ratios and CMB acoustic scales are integrals and ratios of $H$ and
   are only bounded by (5.2) after propagating the inequality through those functionals, which
   requires $a_e$ to be pushed back to recombination — legitimate only under the activation law of
   Note 02.
5. **$\Delta$ is not yet shown to be measurable at useful precision.** Corollary 5.3 says $\Delta$
   controls the deviation; it does not show that current data constrain $\Delta$ at the level where
   the model is distinguishable from $\Lambda$CDM. No fit has been performed here.
6. **Proposition 2.1 does not refute the DESI-era IDE preference.** It shows that a class of models
   carrying that preference is dynamically ill-posed on part of its parameter space. It does not
   show that the preference disappears when the class is replaced by a quasi-positive one; that is
   an open computation.
7. **Track B is not developed.** Proposition 6.2 gives a sufficient condition for the sign flip
   under stated asymptotic assumptions on $\Gamma_\downarrow$; no solution, no attractor analysis,
   and no perturbation theory for (S$_\downarrow$) is provided.
8. **No microphysical justification of $b$.** The branching ratio is a free constant here; the
   claim that the defect product is exactly pressureless is an assumption (H4), not a result.
