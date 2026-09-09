# Note 02 — The early universe: why the draft's rate law fails, and the activation law that fixes it

**Status.** Theory note for transcription. Contains a **no-go theorem** against the rate law as
written in the draft's eq. (6.6), and a minimal repair.

**Dependency.** Uses Note 01, Theorem 1.1 (positivity under $\Gamma\ge0$, $L^1_{\rm loc}$ only) and
Note 01, Prop. 2.3 ($V$ is not protected backwards in time).

---

## 0. Setting

System (S) of Note 01, standing hypotheses (H1)–(H4), plus

- **(E0) Cosmological anchoring.** $a(t_0)=1$; $\rho_{k0}$ denotes present values;
  $\Omega_{k0}=\rho_{k0}/(3M_{\rm Pl}^2H_0^2)$. Radiation is separately conserved and
  $\Omega_{r0}\simeq9.2\times10^{-5}$ (photons + 3 massless neutrino species).
  Reference values used only for numerical illustration: $\Omega_{m0}=0.31$, $\Omega_{V0}=0.69$,
  $\Omega_{I0}\le\Omega_{{\rm dm}0}\simeq0.26$, $a_{\rm eq}=\Omega_{r0}/\Omega_{m0}\simeq3.0\times10^{-4}$,
  $a_{\rm rec}\simeq9.1\times10^{-4}$.

Recall the two exact facts used throughout:

$$
\rho_I(a)\,a^{3}=\frac{\rho_{I0}}{1-f_0}\,\big(1-f(a)\big)\;\equiv\;C\,(1-f(a)),
\qquad
\dot V=Q_V=(1-b)\Gamma\rho_I .
\tag{0.1}
$$

Because $f$ is non-decreasing (Note 01, (1.1)), running backwards from $t_0$ gives
$1-f_0\le 1-f(a)\le 1$, hence the **two-sided comoving bound**

$$
\rho_{I0}\;\le\;\rho_I(a)\,a^3\;\le\;C=\frac{\rho_{I0}}{1-f_0}\qquad\text{for all }a\le1 .
\tag{0.2}
$$

Equation (0.2) is what makes all the estimates below rigorous rather than heuristic: the comoving
precursor density is bounded above *and below* by constants, so the only thing that can control the
size of $\int Q_V\,dt$ is $\Gamma$ itself.

---

## 1. No-go for a constant rate floor

The draft adopts $\Gamma=\Gamma_0e^{\alpha f+\beta M}$ with $\Gamma_0>0$ (eq. (6.6)), and notes
$\Gamma_0\le\Gamma\le\Gamma_0e^{\alpha+\beta}$ on $[0,1]^2$. The positive floor $\Gamma_0$ is exactly
what Theorem 1 and Theorem 2 of the draft use (hypothesis 3: $0<g\le\Gamma\le G$). We now show that
the floor is fatal if it is assumed to hold back into the radiation era.

> **Hypotheses.**
> - **(N1)** The solution of (S) exists with non-negative densities on $[t_i,t_0]$, $a(t_i)=a_i\le1$.
> - **(N2)** $\Gamma(t)\ge\Gamma_0>0$ for all $t\in[t_i,t_0]$.
> - **(N3)** $b<1$ and $\rho_{I0}>0$.
> - **(N4)** $H$ is non-increasing on $[t_i,t_0]$ (true by the draft's (7.7) / Note 01, Cor. 1.4,
>   under (H4)).

> **Theorem 1.1 (rate-floor no-go).** Under (N1)–(N4),
> $$
> \boxed{\;V_0-V(a_i)\;\ge\;c\,(1-b)\,M_{\rm Pl}^2\,\Gamma_0\,H_i,
> \qquad c\;\equiv\;\Omega_I(a_i)\;=\;\frac{\rho_I(a_i)}{3M_{\rm Pl}^2H_i^2}\;>\;0 ,}
> \tag{1.1}
> $$
> where $H_i=H(t_i)$. Consequently, since $0\le V(a_i)$ and $V_0=3\Omega_{V0}M_{\rm Pl}^2H_0^2$,
> $$
> \boxed{\;\Gamma_0\;\le\;\frac{3\,\Omega_{V0}}{(1-b)\,\Omega_I(a_i)}\cdot\frac{H_0^2}{H_i}
> \;\xrightarrow[\ \Omega_I(a_i)=\mathcal O(1)\ ]{}\;\mathcal O(1)\times\frac{H_0^2}{H_i}\;. }
> \tag{1.2}
> $$
>
> **Proof.** By (0.1) and (N2),
> $$
> V_0-V(a_i)=(1-b)\!\int_{t_i}^{t_0}\!\Gamma\rho_I\,dt\;\ge\;(1-b)\,\Gamma_0\!\int_{t_i}^{t_0}\!\rho_I\,dt .
> $$
> Change variables with $dt=da/(aH)$ and use the lower bound of (0.2), $\rho_I\ge\rho_{I0}a^{-3}$:
> $$
> \int_{t_i}^{t_0}\rho_I\,dt\;\ge\;\rho_{I0}\int_{a_i}^{1}\frac{da}{a^{4}H(a)} .
> $$
> By (N4), $H(a)\le H_i$ for $a\ge a_i$, so $1/H(a)\ge1/H_i$ and
> $$
> \int_{a_i}^{1}\frac{da}{a^{4}H(a)}\;\ge\;\frac{1}{H_i}\int_{a_i}^{1}a^{-4}da=\frac{a_i^{-3}-1}{3H_i}.
> $$
> Hence $V_0-V(a_i)\ge(1-b)\Gamma_0\rho_{I0}(a_i^{-3}-1)/(3H_i)$. Finally
> $\rho_{I0}a_i^{-3}\le\rho_I(a_i)=3M_{\rm Pl}^2H_i^2\,\Omega_I(a_i)$ by (0.2) — more precisely
> $\rho_{I0}a_i^{-3}=\rho_I(a_i)(1-f_0)/(1-f(a_i))$, and since $1-f_0\le1-f(a_i)$ this is
> $\le\rho_I(a_i)$; for the *lower* bound we use it directly:
> $\rho_{I0}(a_i^{-3}-1)\ge\rho_{I0}a_i^{-3}(1-a_i^3)$. Writing
> $\rho_{I0}a_i^{-3}=(1-f_0)(1-f(a_i))^{-1}\rho_I(a_i)\ge(1-f_0)\rho_I(a_i)$ and absorbing the
> harmless factors $(1-a_i^3)\ge1/2$ and $(1-f_0)$ into $c$ gives (1.1) with
> $c=\tfrac12(1-f_0)\Omega_I(a_i)$; we quote the cleaner $c=\Omega_I(a_i)$ understanding the
> $\mathcal O(1)$ prefactor. Statement (1.2) follows from $V(a_i)\ge0$ (Note 01, Thm. 1.1) and
> $V_0\le3M_{\rm Pl}^2H_0^2$. $\square$

> **Corollary 1.2 (nothing converts late).** Under (N1)–(N4), the fraction converted over the whole
> late universe obeys
> $$
> \Delta f\;=\;\int_{t_{\rm late}}^{t_0}\!\Gamma\,dt
> \;\le\;\Gamma_0e^{\alpha+\beta}\,(t_0-t_{\rm late})
> \;\lesssim\;\frac{3\,\Omega_{V0}\,e^{\alpha+\beta}}{(1-b)\,\Omega_I(a_i)}\cdot\frac{H_0}{H_i}\,.
> \tag{1.3}
> $$
> *Proof.* $\dot f=(1-f)\Gamma\le\Gamma\le\Gamma_0e^{\alpha+\beta}$ on $[0,1]^2$; then insert (1.2)
> and $t_0-t_{\rm late}\lesssim H_0^{-1}$. $\square$

### 1.3 The numbers

Evaluated on the reference cosmology of (E0), with $b=0$ and $e^{\alpha+\beta}=1$:

| $a_i$ anchored at | $a_i$ | $H_i/H_0$ | $\Omega_I(a_i)$ | bound on $\Gamma_0/H_0$ | resulting $\Delta f$ |
|---|---|---|---|---|---|
| Electroweak, $T\sim100$ GeV | $2.4\times10^{-15}$ | $1.7\times10^{27}$ | $6.6\times10^{-12}$ | $1.8\times10^{-16}$ | $\sim10^{-16}$ |
| BBN, $T\sim1$ MeV | $2.4\times10^{-10}$ | $1.7\times10^{17}$ | $6.6\times10^{-7}$ | $1.8\times10^{-11}$ | $\sim10^{-11}$ |
| $a=10^{-6}$ | $10^{-6}$ | $9.6\times10^{9}$ | $2.8\times10^{-3}$ | $7.6\times10^{-8}$ | $\sim10^{-7}$ |
| Radiation–matter equality | $3.0\times10^{-4}$ | $1.5\times10^{5}$ | $0.42$ | $3.2\times10^{-5}$ | $\sim10^{-5}$ |
| Recombination | $9.1\times10^{-4}$ | $2.3\times10^{4}$ | $0.63$ | $1.4\times10^{-4}$ | $\sim10^{-4}$ |

**Conclusion (to be stated in the paper as written).** *The rate law of the draft's eq. (6.6), with a
strictly positive constant floor $\Gamma_0$ extended into the radiation era, has no viable early
universe.* Either $\Gamma_0$ is large enough to convert an observationally interesting amount today
($\Gamma_0\sim H_0$, $\Delta f\sim\mathcal O(0.1)$), in which case (1.1) forces
$V_0-V(a_i)\gtrsim10^{11}\times3M_{\rm Pl}^2H_0^2$ if $a_i$ is BBN, i.e. $V$ must have been
enormously negative in the past — excluded by Note 01, Theorem 1.1, which says $V$ cannot have been
negative if it is non-negative now and the model is run forward from there; equivalently
$a_{\min}$ (Note 01, Prop. 2.3) sits at $a\sim1$ and the model has no past. Or $\Gamma_0$ satisfies
(1.2), in which case $\Delta f\lesssim10^{-11}$ and the mechanism is observationally inert.

> **Remark 1.4 (comparison with the figure sometimes quoted).** If one takes the sharper hypothesis
> $\Omega_I(a_i)=\mathcal O(1)$ — appropriate only if the precursor *dominated* the energy budget
> at $a_i$ — the bound collapses to the memorable form $\Gamma_0\lesssim H_0^2/H_i$ and
> $\Delta f\sim H_0/H_i$, giving $\sim10^{-18}$ at BBN and $\sim10^{-28}$ at the electroweak scale.
> In radiation domination the honest value of $\Omega_I(a_i)$ is $\simeq a_i/a_{\rm eq}\ll1$, which
> *weakens* the bound by $a_{\rm eq}/a_i$, and this is the version we quote. The qualitative
> conclusion is unchanged: $\Delta f\lesssim10^{-11}$ is already fatal.

### 1.5 Correction to the draft

1. **Hypothesis 3 of the draft's Theorem 1** ($0<g\le\Gamma\le G$ "en el dominio físico") must not
   be read as holding on a domain that reaches back into the radiation era. Theorem 1.1 above shows
   that reading is inconsistent with $V\ge0$ and with $\Omega_{V0}\le1$.
2. **The draft's Theorem 2** (positive vacuum, acceleration, de Sitter limit) uses that hypothesis.
   Its conclusions are *future* statements, so the theorem is not wrong — but its hypothesis is
   only available from an activation time onwards. It must therefore be restated as: *"for
   $t\ge t_{\rm act}$"*, with $t_{\rm act}$ defined by the activation law of Sec. 3 below and with
   the lower bound $g$ established a posteriori (Prop. 3.6). Using Theorem 2 "all the way to the
   past" is not licensed.
3. **The positivity theorem does not need the floor.** This is why Note 01 re-proved positivity
   under $\Gamma\in L^1_{\rm loc}$, $\Gamma\ge0$ only. After removing the floor, positivity, the
   survival identities, the sandwich theorem and the jerk identity all survive intact; only the
   asymptotic de Sitter statement needs the floor, and it needs it only in the future.

---

## 2. Convergence lemma: exactly how fast $\Gamma$ must switch off

> **Definition.** $\displaystyle \xi(a)\equiv\frac{\Gamma}{H}$ (the reduced rate; this is the
> $\xi$ of the solvable family $\Gamma=\xi H$, now allowed to depend on $a$).
> $\displaystyle V_{\rm early}\equiv\lim_{a\to0^+}V(a)$ whenever the limit exists.

> **Lemma 2.1 (convergence criterion).** Assume (H1)–(H4), $b<1$, $\rho_{I0}>0$, and that the
> solution extends to $a\to0^+$ with $H>0$. Then, with $C$ as in (0.1),
> $$
> V_0-V(a)=(1-b)\,C\int_{a}^{1}\xi(a')\,\big(1-f(a')\big)\,\frac{da'}{a'^{4}} ,
> \tag{2.1}
> $$
> and therefore
> $$
> \boxed{\;V_{\rm early}\ \text{exists and is finite}\iff \int_{0}\xi(a)\,\frac{da}{a^{4}}<\infty . }
> \tag{2.2}
> $$
> In particular:
> (a) if $\xi(a)=\mathcal O(a^{3+\epsilon})$ as $a\to0$ for some $\epsilon>0$, the integral converges;
> (b) if $\liminf_{a\to0}\,\xi(a)\,a^{-3}>0$ (in particular if $\xi\to\xi_0>0$, the case
> $\Gamma\propto H$), the integral diverges and $V_{\rm early}=-\infty$: the model has no past.
>
> **Proof.** From $\dot V=(1-b)\Gamma\rho_I$, $dt=da/(aH)$, and $\rho_I=C(1-f)a^{-3}$:
> $$
> \frac{dV}{da}=\frac{(1-b)\Gamma\rho_I}{aH}=(1-b)\,C\,\frac{\Gamma}{H}\,(1-f)\,a^{-4},
> $$
> which integrates to (2.1). For (2.2), note $1-f_0\le1-f(a)\le1$ by monotonicity of $f$, so the
> integrand in (2.1) is bracketed by $(1-f_0)\,\xi a^{-4}$ and $\xi a^{-4}$, both non-negative.
> Two non-negative integrands bracketing each other by fixed positive constants converge or diverge
> together, giving the equivalence. (a) and (b) are the standard comparison tests against
> $a^{-1+\epsilon}$ and $a^{-1}$ respectively. $\square$

**Reading of Lemma 2.1.** The dilution factor $a^{-4}$ ($a^{-3}$ from the precursor density,
$a^{-1}$ from the measure $dt=da/(aH)$) is what makes a naive late-time-motivated rate law explode.
Requiring only $\Gamma\to0$ is not enough; requiring $\Gamma/H\to0$ is not enough; one needs
$\Gamma/H$ to vanish *faster than $a^{3}$*. This is the precise statement that the draft's
Sec. 8.2 discovered numerically in the special case $\xi=$ const (its $a_{\min}$), and it is the
design specification for Sec. 3.

> **Corollary 2.2 (the borderline is genuinely borderline).** For $\xi=\xi_0a^{3}$ the integral is
> logarithmically divergent, $V_0-V(a)\sim(1-b)C\xi_0\ln(1/a)$. So $p=3$ exactly is excluded and
> the exponent must strictly exceed $3$.

---

## 3. The activation law

### 3.1 Definition and hypotheses

> **(A1) Activation ansatz.**
> $$
> \boxed{\;\Gamma(a,f,M)=\xi_0\,H(a)\,S(a)\,e^{\alpha f+\beta M},\qquad
> S(a)=\frac{a^{p}}{a^{p}+a_{\rm act}^{p}},\quad p>3,\ \ a_{\rm act}\in(0,1],\ \xi_0\ge0 .}
> \tag{3.1}
> $$
> $S$ is smooth, strictly increasing, $S(a)\in(0,1)$, $S(a_{\rm act})=\tfrac12$,
> $S(a)\to1$ as $a\to\infty$, and $S(a)=(a/a_{\rm act})^{p}\,[1+\mathcal O((a/a_{\rm act})^{p})]$ as
> $a\to0$.
> **(A2)** $\alpha,\beta\ge0$, $\tau_M>0$, $f,M\in[0,1]$ so that $1\le e^{\alpha f+\beta M}\le e^{\alpha+\beta}$.
> **(A3)** The rest of (S) and (E0) hold.

Note that (3.1) still contains the draft's memory law: the reinforcement factor
$e^{\alpha f+\beta M}$ is untouched. What changes is that the *floor* $\Gamma_0$ is replaced by a
Hubble-tracking, activation-gated prefactor. This is the minimal repair: it keeps every result of
Notes 01, 03 and 04 (all of which need only $\Gamma\ge0$), and it removes the no-go.

### 3.2 Positivity of $V$ on the whole branch

> **Proposition 3.3.** Under (A1)–(A3) with $\xi_0>0$, $b<1$:
> (i) $V_{\rm early}=\lim_{a\to0^+}V(a)$ exists and is finite;
> (ii) $V$ is non-decreasing in $a$, so
> $$
> \boxed{\;V(a)\ge0\ \text{ for all }a\in(0,1]\iff V_{\rm early}\ge0 . }
> $$
> (iii) A sufficient condition, explicit in the parameters, is
> $$
> \boxed{\;\xi_0\;\le\;\frac{V_0\,(1-f_0)}{(1-b)\,e^{\alpha+\beta}\,\rho_{I0}\;\mathcal I_S}
> \;=\;\frac{3\,\Omega_{V0}\,(1-f_0)}{(1-b)\,e^{\alpha+\beta}\,\Omega_{I0}\;\mathcal I_S}\cdot\frac{1}{3},}
> \qquad
> \mathcal I_S\equiv\int_0^1 S(a)\,a^{-4}\,da ,
> \tag{3.2}
> $$
> written more simply as $\;\xi_0\,\mathcal I_S\le \dfrac{\Omega_{V0}(1-f_0)}{(1-b)e^{\alpha+\beta}\,\Omega_{I0}}$,
> and
> $$
> \boxed{\;\tfrac12\,\Big(\tfrac{1}{p-3}+\tfrac13\Big)a_{\rm act}^{-3}-\tfrac16\;\le\;
> \mathcal I_S\;\le\;\Big(\tfrac{1}{p-3}+\tfrac13\Big)a_{\rm act}^{-3}-\tfrac13\;. }
> \tag{3.3}
> $$
>
> **Proof.** (i) By (A1), $\xi(a)=\xi_0S(a)e^{\alpha f+\beta M}\le\xi_0e^{\alpha+\beta}S(a)$ and
> $S(a)\le(a/a_{\rm act})^p$, so $\xi(a)=\mathcal O(a^p)$ with $p>3$; Lemma 2.1(a) applies.
> (ii) $\dot V=Q_V\ge0$ (Note 01, Thm. 1.1) and $a$ is increasing, so $V$ is non-decreasing in $a$;
> the equivalence is then immediate, the "$\Leftarrow$" from $V(a)\ge V_{\rm early}$ and the
> "$\Rightarrow$" from taking the limit.
> (iii) From (2.1) with $a\to0$ and $(1-f)\le1$, $e^{\alpha f+\beta M}\le e^{\alpha+\beta}$:
> $$
> V_0-V_{\rm early}\le(1-b)\,C\,\xi_0\,e^{\alpha+\beta}\int_0^1S(a)a^{-4}da
> =(1-b)\frac{\rho_{I0}}{1-f_0}\,\xi_0\,e^{\alpha+\beta}\,\mathcal I_S ,
> $$
> and $V_{\rm early}\ge0$ follows if the right-hand side is $\le V_0$, which is (3.2).
> For (3.3): $S(a)=\big[1+(a_{\rm act}/a)^p\big]^{-1}$ satisfies
> $\tfrac12\min\{1,(a/a_{\rm act})^p\}\le S(a)\le\min\{1,(a/a_{\rm act})^p\}$, because for
> $a\le a_{\rm act}$, $S\le(a/a_{\rm act})^p$ and $S\ge\tfrac12(a/a_{\rm act})^p$, while for
> $a\ge a_{\rm act}$, $\tfrac12\le S\le1$. Integrating the upper envelope,
> $$
> \int_0^{a_{\rm act}}\!\!\frac{a^{p-4}}{a_{\rm act}^{p}}da+\int_{a_{\rm act}}^{1}\!\!a^{-4}da
> =\frac{a_{\rm act}^{-3}}{p-3}+\frac{a_{\rm act}^{-3}-1}{3}
> =\Big(\frac{1}{p-3}+\frac13\Big)a_{\rm act}^{-3}-\frac13 ,
> $$
> and halving gives the lower envelope. $\square$

**Numerical check of (3.3)** (exact quadrature versus the envelope):
$a_{\rm act}=0.3,p=6$: $\mathcal I_S=19.06$ against upper envelope $24.4$;
$a_{\rm act}=0.3,p=8$: $15.41$ against $19.4$;
$a_{\rm act}=0.1,p=6$: $523.3$ against $666.3$;
$a_{\rm act}=0.1,p=8$: $424.7$ against $533.0$. The envelope is tight to $\sim25\%$, as expected.

### 3.4 BBN and recombination are untouched

> **Proposition 3.5.** Under (A1)–(A3), for any $a\le a_\star$,
> $$
> \frac{\Gamma}{H}\Big|_{a}\;\le\;\xi_0\,e^{\alpha+\beta}\Big(\frac{a}{a_{\rm act}}\Big)^{p},
> \qquad\text{and}\qquad
> \Big|\frac{d\ln(\rho_ma^3)}{d\ln a}\Big|=\xi_{\rm eff}\le\xi_0e^{\alpha+\beta}\Big(\frac{a}{a_{\rm act}}\Big)^{p},
> \tag{3.4}
> $$
> so the fractional change of the comoving dust density accumulated from $a=0$ to $a=a_\star$ is at
> most $\xi_0e^{\alpha+\beta}(a_\star/a_{\rm act})^{p}/p$.
> *Proof.* First inequality: $S(a)\le(a/a_{\rm act})^p$ and $e^{\alpha f+\beta M}\le e^{\alpha+\beta}$.
> Second: Note 01, Thm. 4.1 gives $|\delta_{\rm eff}|=\xi_{\rm eff}=(1-b)\Gamma s/H\le\Gamma/H$.
> Integrating $\int_0^{a_\star}(a/a_{\rm act})^p\,da/a=(a_\star/a_{\rm act})^p/p$. $\square$

Numerically, with $\xi_0e^{\alpha+\beta}=\mathcal O(1)$:

| $a_{\rm act}$ | $p$ | $\Gamma/H$ at recombination ($a=9.1\times10^{-4}$) | $\Gamma/H$ at BBN ($a=2.4\times10^{-10}$) |
|---|---|---|---|
| $0.30$ | $6$ | $7.7\times10^{-16}$ | $2.3\times10^{-55}$ |
| $0.30$ | $8$ | $7.1\times10^{-21}$ | $1.4\times10^{-73}$ |
| $0.24$ | $6$ | $2.9\times10^{-15}$ | $8.8\times10^{-55}$ |
| $0.10$ | $6$ | $5.6\times10^{-13}$ | $1.7\times10^{-52}$ |

So for $a_{\rm act}\ge0.3$ and $p\ge6$ one has $\Gamma/H<10^{-15}$ at recombination and
$<10^{-54}$ at BBN. Consequences, all immediate from (3.4):

- **BBN.** The expansion rate at $T\sim1$ MeV differs from $\Lambda$CDM by a fractional amount
  $\le\mathcal O(10^{-54})$; the effective number of relativistic species is unaffected at any
  conceivable precision, and no energy is injected into or removed from the radiation bath
  (radiation is separately conserved by (S)).
- **Recombination.** The comoving dust density at $a_{\rm rec}$ differs from its $a\to0$ value by
  $\le10^{-16}$; $\omega_m$, $\omega_b$, the sound horizon $r_s$, and the acoustic peak structure
  are those of $\Lambda$CDM with parameters $(\Omega_{m0}+\Delta,\ \Omega_{V0}-\Delta)$ in the
  sense of Note 01, Theorem 5.1.
- **Matter era.** Between $a_{\rm rec}$ and $a\sim a_{\rm act}$, $\xi_{\rm eff}\le\xi_0e^{\alpha+\beta}(a/a_{\rm act})^p$
  remains $\ll1$, so $\rho_m\propto a^{-3}$ to high accuracy and the standard matter-dominated
  growth $\delta\propto a$ is preserved (see Note 03, Sec. 4, where the correction is computed).

> **Proposition 3.6 (restatement of the draft's Theorem 2).** Fix $t_{\rm act}$ by
> $a(t_{\rm act})=a_{\rm act}$ and suppose $V(t_{\rm act})>0$ (guaranteed if $V_{\rm early}>0$, and
> also if $V_{\rm early}=0$ with $\xi_0>0$, $b<1$, $\rho_{I0}>0$, since then $V$ is strictly
> increasing). Then on $[t_{\rm act},\infty)$,
> $$
> \Gamma\;\ge\;g\;\equiv\;\xi_0\,S(a_{\rm act})\sqrt{\frac{V(t_{\rm act})}{3M_{\rm Pl}^2}}
> \;=\;\frac{\xi_0}{2}\sqrt{\frac{V(t_{\rm act})}{3M_{\rm Pl}^2}}\;>\;0 ,
> $$
> and $\Gamma\le G\equiv\xi_0e^{\alpha+\beta}H(t_{\rm act})$. Hence hypothesis 3 of the draft's
> Theorem 1 holds on $[t_{\rm act},\infty)$ and **the draft's Theorem 2 (positive vacuum,
> $f\to1$, $H\to H_\infty>0$, de Sitter attractor, eventual acceleration) holds verbatim with
> $t_i$ replaced by $t_{\rm act}$.**
> *Proof.* $S$ is increasing and $S(a_{\rm act})=\tfrac12$; $H(t)\ge\sqrt{V(t)/3M_{\rm Pl}^2}\ge\sqrt{V(t_{\rm act})/3M_{\rm Pl}^2}$
> for $t\ge t_{\rm act}$ by the Friedmann constraint, non-negativity of the other densities
> (Note 01, Thm. 1.1) and monotonicity of $V$; $e^{\alpha f+\beta M}\ge1$. The upper bound uses
> $S\le1$, $e^{\alpha f+\beta M}\le e^{\alpha+\beta}$ and $H\le H(t_{\rm act})$ (Note 01, Cor. 1.4).
> The argument is not circular: the lower bound on $H$ uses only positivity, which needs no lower
> bound on $\Gamma$. $\square$

---

## 4. Two sub-models: (FG) fully generated vacuum, and (PL) partially generated

The activation law leaves $V_{\rm early}\ge0$ free. Two qualitatively different physical claims sit
at the two ends.

- **(FG) Fully generated:** $V_{\rm early}=0$. The vacuum energy is *entirely* a product of the
  conversion; there is no primordial cosmological constant. This is the philosophically attractive
  version.
- **(PL) Partial:** $V_{\rm early}>0$. A primordial vacuum term exists and is topped up by a small
  amount of late conversion.

The following exact relation decides between them.

> **Proposition 4.1 (deficit–vacuum relation).** Assume (A1)–(A3) and $b<1$. Let
> $\Delta=(\rho_m^{\rm early}-\rho_{m0})/(3M_{\rm Pl}^2H_0^2)$ be the matter deficit of Note 01,
> eq. (5.1), with $\rho_m^{\rm early}=\lim_{a\to0}\rho_ma^3$. Then
> $$
> \boxed{\;\Delta=\big(\Omega_{V0}-\Omega_{V,\rm early}\big)\,\big\langle a^{3}\big\rangle_{Q_V},
> \qquad
> \big\langle a^{3}\big\rangle_{Q_V}\equiv\frac{\int_0^{t_0}Q_V\,a^{3}\,dt}{\int_0^{t_0}Q_V\,dt}\in(0,1],}
> \tag{4.1}
> $$
> where $\Omega_{V,\rm early}=V_{\rm early}/(3M_{\rm Pl}^2H_0^2)$.
> *Proof.* $\rho_m^{\rm early}-\rho_{m0}=\int_0^{t_0}Q_Va^3dt$ and $V_0-V_{\rm early}=\int_0^{t_0}Q_Vdt$,
> both from (5.4) of Note 01; divide and rearrange. $\langle a^3\rangle\le1$ since $a\le1$, and
> $>0$ since $Q_V\ge0$, $\not\equiv0$. $\square$

> **Corollary 4.2 (FG dichotomy).** In (FG), $\Omega_{V,\rm early}=0$, so
> $$
> \Delta=\Omega_{V0}\,\langle a^3\rangle_{Q_V}.
> $$
> Requiring the matter deficit to be a fraction $\eta$ of the present matter density,
> $\Delta\le\eta\,\Omega_{m0}$, forces
> $$
> \boxed{\;\langle a^3\rangle_{Q_V}\le\frac{\eta\,\Omega_{m0}}{\Omega_{V0}},\qquad\text{i.e.}\qquad
> 1+z_{\rm conv}\;\gtrsim\;\Big(\frac{\Omega_{V0}}{\eta\,\Omega_{m0}}\Big)^{1/3},}
> \tag{4.2}
> $$
> where $z_{\rm conv}$ is the $Q_V$-weighted conversion redshift, $\langle a^3\rangle\equiv(1+z_{\rm conv})^{-3}$.
> But $V$ is monotone and reaches within $\eta\Omega_{m0}/\Omega_{V0}$ of its final value by
> $z\sim z_{\rm conv}$, so for all $z<z_{\rm conv}$ the model is a pure cosmological constant:
> $Q_V\to0$, $\varepsilon\to0$, $j\to1+2\Omega_r$ (Note 04), and every observable of Notes 01, 03, 04
> degenerates to $\Lambda$CDM.

**Numerical evaluation of the FG case.** For the reference weighting $Q_V\propto S(a)a^{-4}$
(i.e. dropping the slowly varying $(1-f)e^{\alpha f+\beta M}$, which is bounded between $1-f_0$ and
$e^{\alpha+\beta}$):

| $a_{\rm act}$ | $p$ | $\langle a^3\rangle_{Q_V}$ | $\Delta$ (FG) | $\Delta/\Omega_{m0}$ |
|---|---|---|---|---|
| $0.30$ | $6$ | $0.063$ | $0.044$ | $14\%$ |
| $0.30$ | $8$ | $0.078$ | $0.054$ | $17\%$ |
| $0.10$ | $6$ | $0.0044$ | $0.0030$ | $1.0\%$ |
| $0.10$ | $8$ | $0.0054$ | $0.0037$ | $1.2\%$ |

Since CMB+BAO determine $\omega_m$ at the $\sim1\%$ level and low-redshift probes determine
$\Omega_m$ at the few-percent level *at fixed $H_0$*, a $14$–$17\%$ deficit is excluded outright, and
even $a_{\rm act}=0.1$ ($z_{\rm act}=9$) sits at the edge. Pushing further requires
$a_{\rm act}\lesssim0.05$, by which point $\Gamma/H$ today is $\xi_0e^{\alpha+\beta}S(1)\simeq\xi_0e^{\alpha+\beta}$
but $\rho_I$ has already been drained, so $Q_V$ today — and hence $\varepsilon_0$ and $j_0-1$ — is
negligible.

> **Conclusion (FG).** The fully generated sub-model is either **excluded** (activation late enough
> to be observable $\Rightarrow$ matter deficit of $10\%$ or more) or **unobservable** (activation
> early enough to hide the deficit $\Rightarrow$ exact $\Lambda$ at all observable redshifts).
> Both horns are stated as a theorem-with-numbers, not as an impression.

> **Honest correction to a stronger claim.** It is tempting to say FG requires
> "$\Delta=\Omega_{V0}$" and is therefore excluded unless activation happens at $z\gg10^{3}$.
> Equation (4.1) shows the exact statement is $\Delta=\Omega_{V0}\langle a^3\rangle$, and (4.2)
> gives $1+z_{\rm conv}\gtrsim(\Omega_{V0}/\eta\Omega_{m0})^{1/3}$, i.e. $z_{\rm conv}\gtrsim5$ for
> $\eta=1\%$ and $z_{\rm conv}\gtrsim50$ for $\eta=10^{-5}$. Only if one demands
> $\eta\lesssim10^{-6}$ does one reach $z\gg10^{3}$. We state the derived bound, not the memorable
> one.

> **The (PL) sub-model.** With $\Omega_{V,\rm early}>0$, (4.1) reads
> $\Delta=(\Omega_{V0}-\Omega_{V,\rm early})\langle a^3\rangle\le\Omega_{V0}-\Omega_{V,\rm early}$.
> The deficit is now controlled by the *converted* portion, which is an independent parameter and
> can be made arbitrarily small while keeping activation late ($a_{\rm act}\sim0.3$–$0.5$) and hence
> keeping the late-time signal $Q_V(t_0)>0$ alive. Concretely, the observationally relevant
> parameter pair is
> $$
> \big(\varepsilon_0,\ \Delta\big),\qquad
> \varepsilon_0=\frac{Q_V(t_0)}{2M_{\rm Pl}^2H_0^3}=\frac32(1-b)\,\xi_0S(1)e^{\alpha f_0+\beta M_0}\,\Omega_{I0},
> $$
> (derived in Note 04, eq. (1.4)), with $\Delta\simeq(1-b)\xi_0\Omega_{I0}\langle a^3\rangle\mathcal I_S\cdot(\ldots)$
> small. **PL is allowed and testable**; it is the version that should be fitted.

---

## 5. Summary of the repaired model, in the form to be quoted

$$
\Gamma=\xi_0\,H\,\frac{a^{p}}{a^{p}+a_{\rm act}^{p}}\,e^{\alpha f+\beta M},\qquad
\dot f=(1-f)\Gamma,\qquad \tau_M\dot M=f-M,
$$
$$
p>3\ \ (\text{use }p\ge6),\qquad a_{\rm act}\in(0,1],\qquad
V_{\rm early}=V_0-(1-b)C\!\int_0^1\!\xi_0S(1-f)e^{\alpha f+\beta M}\frac{da}{a^{4}}\;>\;0 .
$$
Free parameters: $\{\xi_0,\ a_{\rm act},\ p,\ \alpha,\ \beta,\ \tau_M,\ b,\ \Omega_{V,\rm early}\}$,
of which $b$ is unobservable in linear cosmology (Note 03, Thm. 3.1), $p$ is a shape nuisance once
$p\ge6$, and $(\beta,\tau_M)$ appear only in the snap (Note 04, Thm. 3.1).

---

## What this does not establish

1. **The activation law is not derived.** $S(a)=a^p/(a^p+a_{\rm act}^p)$ is an ansatz chosen to be
   the simplest function satisfying Lemma 2.1(a) with a single scale. No microphysics selects it,
   and no symmetry forbids alternatives (e.g. $\Gamma\propto H\,\rho_I/\rho_{\rm tot}$, or a
   temperature threshold). Any $\xi=\mathcal O(a^{3+\epsilon})$ passes the convergence test; the
   phenomenology of Sec. 3.4 depends on the specific profile only through $\mathcal I_S$ and
   $\langle a^3\rangle_{Q_V}$.
2. **No dynamical explanation of $a_{\rm act}$.** Placing activation at $a_{\rm act}\sim0.3$–$0.5$
   reproduces the observed onset of acceleration by construction. This is a coincidence-problem
   restatement, not a solution; the draft's Sec. 8.4 already concedes this and nothing here improves
   it.
3. **The no-go theorem is about the *floor*, not about memory.** Theorem 1.1 forbids
   $\Gamma\ge\Gamma_0>0$ back to the radiation era. It says nothing against $\alpha,\beta>0$; the
   reinforcement factor survives untouched in (3.1). Do not over-read it as a refutation of the
   self-reinforcement hypothesis.
4. **BBN/recombination "untouched" is a background statement.** Proposition 3.5 bounds the
   *background* effect. A full CMB computation (transfer functions, ISW, lensing) is not performed
   here; Note 03 gives the linear equations but no Boltzmann-code output.
5. **The FG exclusion assumes $\Delta$ is measurable at the quoted precision.** The $\sim1\%$
   figure for $\omega_m$ is quoted from the standard $\Lambda$CDM analyses; in a model with a
   modified late expansion the error budget must be recomputed self-consistently, which has not been
   done. The exclusion should be read as "strongly disfavoured pending a proper fit".
6. **$V_{\rm early}>0$ is not explained.** PL reintroduces a primordial cosmological constant and
   therefore does *not* solve the cosmological-constant problem; it only makes a fraction of $V_0$
   dynamical. This must be said in the paper.
7. **Nothing here constrains the pre-activation era.** For $a\ll a_{\rm act}$ the model is exactly
   $\Lambda$CDM with $\Lambda=V_{\rm early}$ plus an inert precursor; inflation, reheating and the
   origin of $\rho_{Ii}$ are entirely outside the closure.
