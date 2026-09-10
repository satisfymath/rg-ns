# Note 04 — Cosmography: jerk, snap, and the memory fingerprint

**Status.** Theory note for transcription. Sec. 3 derives the snap parameter from scratch and
confirms (rather than assumes) the form quoted in the project brief.

**Dependencies.** Note 01 (positivity, $Q_V\ge0$, sandwich theorem, matter deficit $\Delta$);
Note 02 (activation law); Note 03 (the identity $\varepsilon=\tfrac32\Omega_mg_c$ linking cosmography
to growth).

---

## 0. Kinematic definitions and standing hypotheses

$$
q\equiv-\frac{\ddot a}{aH^2},\qquad
j\equiv\frac{\dddot a}{aH^{3}},\qquad
s\equiv\frac{\ddddot a}{aH^{4}},\qquad
N=\ln a,\qquad {}'=\frac{d}{dN}.
$$
(The draft writes $q_{\rm dec}$ for $q$; we keep $q$ and never use it for a charge.)

> **Lemma 0.1 (kinematic identities).** For any $a(t)$ with $H=\dot a/a>0$,
> $$
> q=-1-\frac{\dot H}{H^{2}},\qquad
> j=1+3\frac{\dot H}{H^{2}}+\frac{\ddot H}{H^{3}},\qquad
> s=\frac{\dot j}{H}-j\,(2+3q).
> \tag{0.1}
> $$
> **Proof.** $\dot a=aH$; $\ddot a=a(H^2+\dot H)$, giving $q$. $\dddot a=\dot a(H^2+\dot H)+a(2H\dot H+\ddot H)
> =a(H^{3}+3H\dot H+\ddot H)$, giving $j$. For $s$, write $\dddot a=aH^{3}j$ and differentiate:
> $\ddddot a=\dot aH^{3}j+3aH^{2}\dot Hj+aH^{3}\dot j=aH^{4}j+3aH^{2}\dot Hj+aH^{3}\dot j$, so
> $s=j\big(1+3\dot H/H^{2}\big)+\dot j/H$. Finally $1+3\dot H/H^{2}=1-3(1+q)=-(2+3q)$. $\square$

> **Standing hypotheses (C).**
> **(C1)** Spatially flat FLRW; **(C2)** the total matter content is: pressureless components of
> total density $\rho_m$, separately conserved radiation $\rho_r$ with $p_r=\rho_r/3$, and an
> **exact vacuum** $V$ with $p_V=-V$ (no other pressure); **(C3)** the vacuum exchanges energy with
> the pressureless sector only, $\dot V=Q_V$, $\dot\rho_m+3H\rho_m=-Q_V$; **(C4)** Einstein's
> equations hold.
> Note that (C1)–(C4) are satisfied by **this model**, by **running-vacuum models**, and (with
> $Q_V=0$) by **$\Lambda$CDM**; the CPL comparison in Sec. 2.2 replaces (C2)–(C3) by a $w$-fluid and
> is derived separately.

---

## 1. The jerk

> **Theorem 1.1 (jerk identity).** Under (C1)–(C4),
> $$
> \boxed{\;j-1=2\Omega_r+\varepsilon,\qquad
> \varepsilon\equiv\frac{Q_V}{2M_{\rm Pl}^2H^{3}},\qquad
> \Omega_r=\frac{\rho_r}{3M_{\rm Pl}^2H^2}. }
> \tag{1.1}
> $$
> **Proof.** From Einstein: $3M_{\rm Pl}^2H^2=\rho_m+\rho_r+V$ and
> $2M_{\rm Pl}^2\dot H=-(\rho+p)=-\big(\rho_m+\rho_r+V+\tfrac13\rho_r-V\big)=-\big(\rho_m+\tfrac43\rho_r\big)$.
> Differentiating and using (C3), $\dot\rho_m=-3H\rho_m-Q_V$, $\dot\rho_r=-4H\rho_r$:
> $$
> 2M_{\rm Pl}^2\ddot H=3H\rho_m+Q_V+\tfrac{16}{3}H\rho_r .
> $$
> Insert into $j=1+3\dot H/H^2+\ddot H/H^3$ from Lemma 0.1:
> $$
> j=1+\frac{-3\rho_m-4\rho_r}{2M_{\rm Pl}^2H^{2}}+\frac{3\rho_m+\tfrac{16}{3}\rho_r}{2M_{\rm Pl}^2H^{2}}
> +\frac{Q_V}{2M_{\rm Pl}^2H^{3}}
> =1+\frac{\tfrac43\rho_r}{2M_{\rm Pl}^2H^{2}}+\varepsilon .
> $$
> Since $\rho_r/(2M_{\rm Pl}^2H^2)=\tfrac32\Omega_r$, the middle term is $2\Omega_r$. $\square$

This is the draft's Theorem 3, eq. (9.3), re-derived; it is the one cosmographic statement of the
draft that survives unchanged.

> **Corollary 1.2 (Track A inequality).** In the one-way model, $Q_V=(1-b)\Gamma\rho_I\ge0$
> (Note 01, Thm. 1.1), hence
> $$
> \boxed{\;j\ \ge\ 1+2\Omega_r\ >\ 1\qquad\text{at every epoch.}}
> \tag{1.2}
> $$
> In the reverse-channel model (Track B of Note 01, Sec. 6), $Q_V\to Q_V^{\rm net}$ and the
> inequality reverses once $\Gamma_\downarrow V>(1-b)\Gamma\rho_I$.

### 1.3 $\varepsilon$ in terms of the model parameters

> **Proposition 1.3.** For system (S) with $\Omega_I=\rho_I/(3M_{\rm Pl}^2H^2)$,
> $$
> \boxed{\;\varepsilon=\frac32\,(1-b)\,\frac{\Gamma}{H}\,\Omega_I
> \;=\;\frac32\,\Omega_m\,g_c ,}
> \tag{1.3}
> $$
> where $g_c=\bar Q_V/(H\bar\rho_m)$ is the growth-coupling function of Note 03, eq. (7.0).
> With the activation law of Note 02, $\Gamma/H=\xi_0S(a)e^{\alpha f+\beta M}$, so today
> $$
> \boxed{\;\varepsilon_0=\frac32\,(1-b)\,\xi_0\,S(1)\,e^{\alpha f_0+\beta M_0}\,\Omega_{I0},
> \qquad S(1)=\frac{1}{1+a_{\rm act}^{\,p}} . }
> \tag{1.4}
> $$
> **Proof.** $\varepsilon=(1-b)\Gamma\rho_I/(2M_{\rm Pl}^2H^3)$ and
> $\rho_I=3M_{\rm Pl}^2H^2\Omega_I$ give the first equality; the second follows from
> $\varepsilon=\big[Q_V/(H\rho_m)\big]\cdot\rho_m/(2M_{\rm Pl}^2H^2)=g_c\cdot\tfrac32\Omega_m$. $\square$

**Order of magnitude.** For $a_{\rm act}=0.3$, $p=6$ ($S(1)=0.9993$), $\Omega_{I0}=0.26$, $b=0$, and
$\xi_0e^{\alpha f_0+\beta M_0}=0.1$: $\varepsilon_0\simeq0.039$, i.e. $j_0\simeq1.04$. This is the
honest expected size of the signal and it is *far* below current sensitivity (Sec. 2.4).

### 1.4 What the sandwich theorem does and does not bound

> **Proposition 1.4 (the sandwich alone gives only the trivial bound).** Let $L,U$ be the two
> $\Lambda$CDM brackets of Note 01, Theorem 5.1, and $\Delta$ the matter deficit. Then
> $E^2$, $E^2_{\rm low}$ and $E^2_{\rm high}$ all have the *same* first $N$-derivative at $a=1$,
> $$
> \big(E^2\big)'=-3\omega_m-4\omega_r\quad\text{exactly, at every }a,
> $$
> so the sandwich is tangent at $a=1$ to first order and constrains $q_0$ trivially and $j_0$ not
> at all. Only the second derivative of $E^2$ sees $Q_V$: $\big(E^2\big)''=9\omega_m+16\omega_r+3q$
> with $q\equiv Q_V/(3M_{\rm Pl}^2H_0^2H)=\tfrac23\varepsilon E^2$.
> **Proof.** $\omega_m'=-3\omega_m-q$ and $\omega_V'=+q$ cancel in $\big(E^2\big)'=\omega_m'+\omega_r'+\omega_V'$;
> differentiate once more. $\square$

> **Proposition 1.5 (a real bound, under monotonicity).** Assume (C1)–(C4), $Q_V\ge0$, and that
> $q(N)=Q_V/(3M_{\rm Pl}^2H_0^2H)$ is **non-decreasing in $N$** up to today (true under the
> activation law of Note 02 while $S$ is switching on). Then
> $$
> \Delta=\int_{-\infty}^{0}q(N)\,e^{3N}\,dN\;\le\;q_0\int_{-\infty}^{0}e^{3N}dN=\frac{q_0}{3},
> $$
> hence
> $$
> \boxed{\;j_0-1\;=\;2\Omega_{r0}+\varepsilon_0\;\ge\;2\Omega_{r0}+\frac92\,\Delta . }
> \tag{1.5}
> $$
> If in addition $q\propto a^{p_{\rm eff}}$ near $a=1$, the relation is exact:
> $\Delta=q_0/(p_{\rm eff}+3)$ and
> $$
> \boxed{\;\varepsilon_0=\frac32\big(p_{\rm eff}+3\big)\,\Delta ,}
> \tag{1.6}
> $$
> so a joint measurement of $j_0$ and $\Delta$ determines the effective activation slope
> $p_{\rm eff}$.
> **Proof.** $\Delta=\int Q_Va^3dt/(3M_{\rm Pl}^2H_0^2)=\int q\,e^{3N}dN$ (Note 01, eq. (5.1), with
> $dt=dN/H$). Monotonicity gives $q\le q_0$ on $N\le0$. Then $\varepsilon_0=\tfrac32q_0\ge\tfrac92\Delta$
> by (1.3). For (1.6), $\int_{-\infty}^0 e^{(p_{\rm eff}+3)N}dN=1/(p_{\rm eff}+3)$. $\square$

**Reading.** The two anchor-free observables of Note 01 — $\{H(z),j(z),\Delta\}$ — are not
independent: under a mild monotonicity assumption, a measured matter deficit sets a *floor* on the
jerk excess, and under a local power-law they determine each other through the activation slope.
This is the model's tightest internal consistency test.

---

## 2. Sign proposition: the jerk separates the competing late-time models

### 2.1 Running vacuum

> **Proposition 2.1.** Consider the running-vacuum model $V=V_0+3\nu M_{\rm Pl}^2\big(H^2-H_0^2\big)$
> with $\nu$ constant, pressureless matter and (C1)–(C4). Then
> $$
> \boxed{\;j-1=2\Omega_r-3\nu\,(1+q)\;\xrightarrow[\ \Omega_r\to0\ ]{}\;-3\nu\,(1+q)\;<\;0
> \quad\text{for }\nu>0 . }
> \tag{2.1}
> $$
> **Proof.** $Q_V=\dot V=6\nu M_{\rm Pl}^2H\dot H$, so
> $\varepsilon=Q_V/(2M_{\rm Pl}^2H^3)=3\nu\dot H/H^2=-3\nu(1+q)$ by Lemma 0.1. Insert into
> Theorem 1.1. Since $\dot H\le0$ under (C2) (all sectors have $\rho+p\ge0$), $1+q\ge0$, so
> $\nu>0\Rightarrow j<1+2\Omega_r$. $\square$

Note the structural contrast: running vacuum has $Q_V\propto H\dot H<0$ — **the vacuum loses energy
to matter** for $\nu>0$ — which is why the sign is opposite. The two models are not variants of one
another; they transfer energy in opposite directions, and the jerk records that.

### 2.2 CPL dark energy

> **Proposition 2.2.** Consider pressureless matter plus a single dark-energy fluid with
> $p_{\rm DE}=w(a)\rho_{\rm DE}$, each separately conserved, no radiation. Then
> $$
> \boxed{\;j-1=\frac92\,\Omega_{\rm DE}\,w\,(1+w)-\frac32\,\Omega_{\rm DE}\,\frac{dw}{d\ln a}\;. }
> \tag{2.2}
> $$
> **Proof.** $2M_{\rm Pl}^2\dot H=-\big[\rho_m+(1+w)\rho_{\rm DE}\big]$, so
> $3\dot H/H^2=-\tfrac92\big[\Omega_m+(1+w)\Omega_{\rm DE}\big]$. Differentiating, with
> $\dot\rho_m=-3H\rho_m$ and $\dot\rho_{\rm DE}=-3H(1+w)\rho_{\rm DE}$:
> $$
> 2M_{\rm Pl}^2\ddot H=3H\rho_m+3H(1+w)^2\rho_{\rm DE}-\dot w\,\rho_{\rm DE},
> $$
> hence $\ddot H/H^3=\tfrac92\Omega_m+\tfrac92(1+w)^2\Omega_{\rm DE}-\tfrac32\Omega_{\rm DE}\,dw/dN$.
> Adding, the $\Omega_m$ terms cancel and
> $j-1=\tfrac92\Omega_{\rm DE}(1+w)\big[(1+w)-1\big]-\tfrac32\Omega_{\rm DE}dw/dN$, which is (2.2). $\square$

> **Corollary 2.3 (sign in the DESI-preferred quadrant).** For CPL, $w(a)=w_0+w_a(1-a)$, one has
> $dw/dN|_{a=1}=-w_a$, so
> $$
> j_0-1=\Omega_{\rm DE,0}\Big[\tfrac92w_0(1+w_0)+\tfrac32w_a\Big].
> $$
> The DESI-preferred region has $w_0>-1$ and $w_a<0$ (a quintessence-like value today, phantom in the
> past). Both terms are then negative: $w_0(1+w_0)<0$ because $-1<w_0<0$, and $w_a<0$.
> **Numerical example:** $\Omega_{\rm DE,0}=0.7$, $w_0=-0.9$, $w_a=-0.8$ give
> $j_0-1=0.7\,[4.5(-0.9)(0.1)+1.5(-0.8)]=0.7\,[-0.405-1.2]=-1.12$.

### 2.3 The discriminator

> **Theorem 2.4 (sign table).** Under the stated hypotheses of each model,
>
> | model | $j-1$ (radiation dropped) | sign |
> |---|---|---|
> | $\Lambda$CDM | $0$ | zero |
> | this model, Track A | $\varepsilon=\tfrac32(1-b)(\Gamma/H)\Omega_I$ | $>0$ |
> | this model, Track B (once reverse channel dominates) | $\tfrac32(1-b)(\Gamma/H)\Omega_I-\tfrac{\Gamma_\downarrow V}{2M_{\rm Pl}^2H^3}$ | $<0$ |
> | running vacuum, $\nu>0$ | $-3\nu(1+q)$ | $<0$ |
> | CPL in the DESI-preferred quadrant | $\Omega_{\rm DE}\big[\tfrac92w_0(1+w_0)+\tfrac32w_a\big]$ | $<0$ |
>
> Consequently **a robust measurement of $j_0<1$ falsifies Track A** — it cannot be accommodated by
> any choice of $b,\alpha,\beta,\tau_M,\xi_0,a_{\rm act},p$ — and selects, among the constructions
> considered here, either the reverse channel of Note 01, Sec. 6, or a genuinely different dark-energy
> sector.
> **Proof.** Row by row: $\Lambda$CDM has $Q_V=0$ in Theorem 1.1; Track A is Corollary 1.2; Track B
> is Note 01, Cor. 6.3 combined with Theorem 1.1 applied to $Q_V^{\rm net}$; running vacuum is
> Proposition 2.1; CPL is Corollary 2.3. $\square$

**Prior art, explicitly acknowledged.** The link between $j>1$ and a transfer of energy from matter
to the vacuum is not new to this work: it was already made by Szydłowski (astro-ph/0502034) in the
context of decaying-vacuum cosmologies, and the jerk as a diagnostic of interaction in the dark
sector has been revisited recently by Worsley, Chakraborty & Dunsby (arXiv:2607.20348). Our
contribution here is (i) the *inequality* form (1.2), which holds for every admissible $\Gamma\ge0$
and is therefore parameter-free, and (ii) the sign table of Theorem 2.4, which turns the diagnostic
into a discriminator between named alternatives.

### 2.4 Honest assessment of current sensitivity

- Late-time-only cosmographic reconstructions (SNe + cosmic chronometers + BAO, expanded about
  $z=0$ or in a $y$-redshift variable) currently give $\sigma(j_0)\approx0.4$. With
  $\varepsilon_0\sim0.04$ predicted (Sec. 1.3), the model's signal is a factor $\sim10$ below the
  present error bar. **The bound (1.2) is not yet decisive, and we must say so.**
- Quoted values of $j_0$ obtained by combining CMB with low-redshift data are **model-dependent**:
  they are derived within a parametrisation (usually $\Lambda$CDM or CPL) and then reported as if
  they were kinematic. Such values must not be used to test (1.2). The test requires a
  reconstruction in which $j$ is obtained from $H(z)$ and its derivatives with a stated smoothing
  prior and a propagated covariance — as the draft's Sec. 9.3 already warns, and as has not been
  done in this work.
- Because $j$ involves the third derivative of $a(t)$, the practical route is not a direct
  measurement but a consistency test: fit the model's $H(z)$, then verify that the recovered
  $Q_V(z)$ from eq. (9.2) of the draft, $Q_V=2M_{\rm Pl}^2(\ddot H+3H\dot H)-\tfrac43H\rho_r$, is
  non-negative within errors.

---

## 3. The snap, and the cosmographic fingerprint of memory

### 3.1 Derivation

> **Hypotheses.** (C1)–(C4) and the model system (S), with a rate law $\Gamma$ that is
> differentiable along the trajectory. Define the $\Lambda$CDM reference snap **at the same $q$ and
> $\Omega_r$**, i.e. the snap of a model with the same $q$ but $Q_V=0$:
> $$
> s_{\Lambda{\rm CDM}}(q)\equiv 4\Omega_r(q-1)-\big(1+2\Omega_r\big)\big(2+3q\big)
> \;\xrightarrow[\ \Omega_r\to0\ ]{}\;-(2+3q).
> \tag{3.1}
> $$

> **Theorem 3.1 (snap of the model).** Under the above hypotheses,
> $$
> \boxed{\;s-s_{\Lambda{\rm CDM}}(q)=\varepsilon\left[\frac{d\ln\Gamma}{dN}-\frac{\Gamma}{H}-2\right] . }
> \tag{3.2}
> $$
> For the draft's rate law $\Gamma=\Gamma_0e^{\alpha f+\beta M}$ (no explicit $a$-dependence),
> $d\ln\Gamma/dN=\alpha(1-f)\Gamma/H+\beta(f-M)/(\tau_MH)$ and (3.2) becomes
> $$
> \boxed{\;s-s_{\Lambda{\rm CDM}}(q)=-\varepsilon\left[2+\frac{\Gamma}{H}
> -\alpha(1-f)\frac{\Gamma}{H}-\frac{\beta\,(f-M)}{\tau_M H}\right] ,}
> \tag{3.3}
> $$
> confirming the form quoted in the project brief. For the activation law of Note 02,
> $\Gamma=\xi_0HS(a)e^{\alpha f+\beta M}$, one has additionally
> $d\ln\Gamma/dN\to d\ln\Gamma/dN-(1+q)+p\,[1-S(a)]$, so
> $$
> s-s_{\Lambda{\rm CDM}}(q)=\varepsilon\left[\alpha(1-f)\frac{\Gamma}{H}+\frac{\beta(f-M)}{\tau_MH}
> +p\big(1-S\big)-(1+q)-\frac{\Gamma}{H}-2\right].
> \tag{3.4}
> $$
>
> **Proof.** From Lemma 0.1, $s=j'-j(2+3q)$ with $j'=dj/dN=\dot j/H$. By Theorem 1.1,
> $j=1+2\Omega_r+\varepsilon$, so
> $$
> s=2\Omega_r'+\varepsilon'-\big(1+2\Omega_r+\varepsilon\big)(2+3q).
> $$
> *Radiation piece.* $\Omega_r=\rho_r/(3M_{\rm Pl}^2H^2)$ gives
> $\Omega_r'=-4\Omega_r-2\Omega_r H'/H=-4\Omega_r+2\Omega_r(1+q)=2\Omega_r(q-1)$, using
> $H'/H=\dot H/H^2=-(1+q)$. Therefore
> $$
> 2\Omega_r'-\big(1+2\Omega_r\big)(2+3q)=4\Omega_r(q-1)-\big(1+2\Omega_r\big)(2+3q)=s_{\Lambda{\rm CDM}}(q),
> $$
> which is (3.1), and
> $$
> s-s_{\Lambda{\rm CDM}}(q)=\varepsilon'-\varepsilon\,(2+3q)=\varepsilon\left[\frac{\varepsilon'}{\varepsilon}-(2+3q)\right].
> \tag{3.5}
> $$
> *The logarithmic derivative of $\varepsilon$.* From (1.3),
> $\ln\varepsilon=\ln\tfrac{(1-b)}{2M_{\rm Pl}^2}+\ln\Gamma+\ln\rho_I-3\ln H$, so
> $$
> \frac{\varepsilon'}{\varepsilon}=\frac{d\ln\Gamma}{dN}+\frac{d\ln\rho_I}{dN}-3\frac{d\ln H}{dN}
> =\frac{d\ln\Gamma}{dN}-\Big(3+\frac{\Gamma}{H}\Big)+3(1+q)
> =\frac{d\ln\Gamma}{dN}-\frac{\Gamma}{H}+3q ,
> \tag{3.6}
> $$
> using $\dot\rho_I=-(3H+\Gamma)\rho_I$ from (S) and $H'/H=-(1+q)$. Substituting (3.6) into (3.5),
> the $3q$ cancels against the $3q$ in $(2+3q)$ and (3.2) follows.
> *The two rate laws.* For $\Gamma=\Gamma_0e^{\alpha f+\beta M}$,
> $d\ln\Gamma/dN=\alpha f'+\beta M'$ with $f'=\dot f/H=(1-f)\Gamma/H$ and
> $M'=\dot M/H=(f-M)/(\tau_MH)$, giving (3.3) after factoring out $-1$. For
> $\Gamma=\xi_0HS(a)e^{\alpha f+\beta M}$, $d\ln\Gamma/dN$ acquires
> $d\ln H/dN=-(1+q)$ and $d\ln S/dN=p\,a_{\rm act}^{p}/(a^{p}+a_{\rm act}^{p})=p\,[1-S(a)]$,
> giving (3.4). $\square$

**Independent check of (3.3) against the draft.** The draft's Proposition 5 gives the criterion for
accelerating conversion, $\ddot f>0\iff d\log\Gamma/dt>\Gamma$, i.e. $d\ln\Gamma/dN>\Gamma/H$.
Equation (3.2) can therefore be written
$$
s-s_{\Lambda{\rm CDM}}(q)=\varepsilon\Big[\underbrace{\Big(\frac{d\ln\Gamma}{dN}-\frac{\Gamma}{H}\Big)}_{>0\ \iff\ \ddot f>0}-2\Big],
$$
so $s>s_{\Lambda{\rm CDM}}$ requires not merely accelerating conversion but *strongly* accelerating
conversion, with margin greater than $2$. This is a nontrivial consistency link between two
independently derived results of the manuscript and is worth stating in the paper.

### 3.2 The key point: memory cancels from $j$ and survives in $s$

> **Theorem 3.2 (memory fingerprint).** Under the hypotheses of Theorem 3.1:
> (i) The jerk depends on the memory sector **only through the instantaneous scalar value of
> $\Gamma$**, namely through $\varepsilon=\tfrac32(1-b)(\Gamma/H)\Omega_I$. The parameters
> $(\beta,\tau_M)$ enter $j$ solely inside the bounded factor $e^{\beta M}\in[1,e^{\beta}]$, which is
> exactly degenerate with the rate normalisation $\Gamma_0$ (or $\xi_0$). Hence, at fixed
> $(H_0,q_0,j_0)$, $(\beta,\tau_M)$ are **unconstrained** by the jerk.
> (ii) The snap depends on $(\beta,\tau_M)$ through the *independent* combination
> $$
> \mathcal B\equiv\frac{\beta\,(f-M)}{\tau_M H},
> $$
> which is the memory *lag* term and cannot be absorbed into $\Gamma_0$ because $f-M$ is a dynamical
> quantity vanishing in the memoryless limit $\tau_M\to0$ and in the saturated limit $f,M\to1$.
> Hence
> $$
> \boxed{\;\frac{\partial s_0}{\partial\mathcal B}=+\varepsilon_0\neq0,\qquad
> \frac{\partial j_0}{\partial\mathcal B}=0 . }
> $$
> **The $(j_0,s_0)$ plane is therefore the cosmographic fingerprint of memory:** $j_0$ measures the
> instantaneous transfer, $s_0$ measures whether that transfer is being driven by a lagged history.
>
> **Proof.** (i) is Proposition 1.3: $j-1-2\Omega_r=\varepsilon$ and $\varepsilon$ is a function of
> the state $(\Gamma,\rho_I,H)$ at one instant; the map $(\Gamma_0,\beta,M)\mapsto\Gamma$ is
> $\Gamma_0e^{\alpha f}\cdot e^{\beta M}$, so a shift in $e^{\beta M}$ is compensated exactly by a
> rescaling of $\Gamma_0$ at that instant. (ii) is read off from (3.3): $\mathcal B$ appears with
> coefficient $+\varepsilon$ and appears nowhere in (1.1). That $\mathcal B$ is not degenerate with
> $\Gamma_0$ follows because $\Gamma_0$ also multiplies $\Gamma/H$ inside the same bracket with the
> *opposite* sign and with a different dependence on $f$: the bracket of (3.3) is
> $2+(1-\alpha(1-f))\Gamma/H-\mathcal B$, in which the coefficient of $\Gamma/H$ is
> $1-\alpha(1-f)$ and that of $\mathcal B$ is $-1$; these are independent directions in parameter
> space unless $f$ is fixed. $\square$

> **Corollary 3.3 (limits, as sanity checks).**
> - **No memory** ($\beta=0$, or $\tau_M\to0$ so $M\to f$ and $f-M\to0$): $\mathcal B=0$ and
>   $s-s_{\Lambda{\rm CDM}}=-\varepsilon[2+(1-\alpha(1-f))\Gamma/H]$, which is strictly negative for
>   $\alpha(1-f)\le1$.
> - **Saturation** ($f,M\to1$): $\mathcal B\to0$ and $\varepsilon\to0$ (since $\rho_I\to0$), so
>   both $j\to1+2\Omega_r$ and $s\to s_{\Lambda{\rm CDM}}$: the de Sitter attractor of the draft's
>   Theorem 2 is cosmographically indistinguishable from $\Lambda$CDM, as it must be.
> - **Strong lag** ($\tau_MH\ll1$ with $f-M>0$): $\mathcal B$ can dominate the bracket and flip the
>   sign of $s-s_{\Lambda{\rm CDM}}$ while leaving $j-1>0$ untouched. This is the observationally
>   distinctive corner.

### 3.4 Practical form for the $(j_0,s_0)$ plane

Collecting, with radiation dropped at $z\simeq0$ and writing $x\equiv\Gamma_0/H_0$ for the reduced
rate today (or $\xi_0S(1)e^{\alpha f_0+\beta M_0}$ under the activation law):
$$
\boxed{
\begin{aligned}
j_0&=1+\varepsilon_0, &&\varepsilon_0=\tfrac32(1-b)\,x\,\Omega_{I0},\\[3pt]
s_0&=-(2+3q_0)+\varepsilon_0\Big[\alpha(1-f_0)\,x+\mathcal B_0-x-2\Big],
&&\mathcal B_0=\frac{\beta(f_0-M_0)}{\tau_MH_0}.
\end{aligned}}
\tag{3.7}
$$
Two consequences for a fit: (a) the locus of $\Lambda$CDM in this plane is the single point
$\big(1,\,-(2+3q_0)\big)$; (b) at fixed $j_0$, varying $\mathcal B_0$ moves $s_0$ along a straight
line of slope $\varepsilon_0=j_0-1$, so **the vertical spread of the model's predictions in the
$(j_0,s_0)$ plane is directly proportional to its horizontal offset from $\Lambda$CDM**. Any model
that sits at $j_0=1$ has no memory signal either; the two must be detected together or not at all.

---

## What this does not establish

1. **No measurement.** Every statement here is a model prediction or a kinematic identity. No
   reconstruction of $H(z)$, $j(z)$ or $s(z)$ from data has been performed in this work, and the
   quoted $\sigma(j_0)\approx0.4$ is a literature-level order of magnitude, not a result of ours.
2. **$s_0$ is currently unmeasurable.** The snap involves the fourth derivative of $a(t)$. Existing
   constraints on $s_0$ from low-redshift data are consistent with essentially any value and are
   dominated by the choice of expansion variable and truncation order. Theorem 3.2 is therefore a
   statement about *where the information lives*, not about a test that can be run today. It
   motivates high-precision $H(z)$ reconstruction (e.g. from redshift drift or a large sample of
   cosmic chronometers), not a present-day likelihood.
3. **Cosmographic expansions are fragile.** Taylor series in $z$ diverge for $z>1$; series in
   $y=z/(1+z)$ converge but bias the coefficients; derivative reconstruction from noisy data
   amplifies errors and requires a stated smoothing prior with a propagated covariance. The draft's
   Sec. 9.3 says this and it remains true.
4. **The sign table assumes each model's own hypotheses.** Proposition 2.1 assumes the specific
   running-vacuum law $V\propto H^2$ with constant $\nu$; other running laws ($V\propto H$,
   $V\propto\dot H$, $V\propto H^{2n}$) give other signs. Proposition 2.2 assumes a single
   non-interacting $w$-fluid; an interacting CPL model changes the result. Theorem 2.4 discriminates
   *these* alternatives, not "all dark energy".
5. **The $\Lambda$CDM reference in (3.1) is a definition.** $s_{\Lambda{\rm CDM}}(q)$ means "the
   snap a $\Lambda$CDM model would have at the same $q$ and $\Omega_r$". It is not the snap of the
   best-fit $\Lambda$CDM model to any dataset, and the two differ because $q_0$ itself differs
   between the models.
6. **The degeneracy argument in Theorem 3.2(ii) is local.** It shows $\mathcal B$ and $x$ enter the
   snap bracket with different coefficients at a given $f$. It does not prove global identifiability
   of $(\beta,\tau_M)$ from $(j_0,s_0)$: those two parameters enter only through the single
   combination $\mathcal B_0$, so at most one number about the memory sector is measurable from
   cosmography at $z=0$. Separating $\beta$ from $\tau_M$ requires the redshift dependence
   $\mathcal B(z)$, i.e. $s(z)$, which is far beyond reach.
7. **Radiation was dropped in the comparison table.** Restoring it shifts every entry by
   $+2\Omega_r$, which is $\sim2\times10^{-4}$ today and irrelevant, but not at $z\gtrsim100$.
8. **No claim of novelty for the identities.** Lemma 0.1, Theorem 1.1 and Proposition 2.2 are
   standard cosmography; Proposition 2.1 restates a known property of running-vacuum models; the
   $j>1\Leftrightarrow$ matter-to-vacuum link is Szydłowski's (astro-ph/0502034). The new content is
   Theorem 3.1's explicit snap for this rate law and Theorem 3.2's separation of memory between $j$
   and $s$.
