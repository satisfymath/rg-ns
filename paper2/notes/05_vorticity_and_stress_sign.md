# Two obstructions to the geometric picture, stated exactly

## 1. An exact vacuum that receives energy forbids vorticity

**Hypotheses.** (H1) the vacuum is exact, `T^{mu nu}_V = -V g^{mu nu}`;
(H2) it receives energy with no spatial momentum transfer in the frame `u`,
`nabla_mu T^{mu nu}_V = Q_V u^nu`; (H3) `u` is a unit timelike field.

**Derivation.** From (H1), `nabla_mu T^{mu nu}_V = -nabla^nu V`, so (H2) gives
`nabla_mu V = -Q_V u_mu`. The left side is a gradient, so its curl vanishes
identically, and

    nabla_[mu ( Q_V u_nu] ) = 0.

Expanding with the standard decomposition
`nabla_mu u_nu = -u_mu a_nu + (Theta/3) h_{mu nu} + sigma_{mu nu} + omega_{mu nu}`,
antisymmetrisation kills `h` and `sigma` because they are symmetric, and leaves

    (nabla_[mu Q_V) u_nu]  +  Q_V ( omega_{mu nu} - u_[mu a_nu] )  =  0.

Projecting both indices with `h^mu_alpha h^nu_beta` annihilates every term
carrying a `u`, and the result is

    **Q_V omega_{alpha beta} = 0.**

Checked numerically on explicit `u`, `h`, `sigma`, `omega`, `a` satisfying all
their constraints: the spatial projection of `Q nabla_[mu u_nu]` equals
`Q omega` to `1e-11`.

**Scope.** This is stronger than the clock argument of §8.3, which gets
`omega = 0` from `u = -nabla T` and therefore only covers the clock
realization. The statement above uses no realization: any exact vacuum fed
without momentum transfer forces the feeding congruence to be irrotational
wherever the feeding is on. It is not a novelty claim — the integrability of
`Q u` is standard in the interacting-vacuum literature — but the vorticity
corollary is the form the present question needs.

**Consequence for the programme.** The vortices the geometric picture wants
cannot live in the flow that feeds the vacuum. Exactly one of (H1), (H2), (H3)
must go.

**The minimal modification.** Keep (H1) and (H3), drop (H2): let the vacuum
receive a spatial momentum transfer `q_mu` as well, so the source is
`S_mu = Q_V u_mu + q_mu`. The source must still be a gradient, and the spatial
projection now reads

    Q_V omega_{mu nu}  =  - ( h h nabla_[mu q_nu] ).

Vorticity is then permitted exactly to the extent that the momentum transfer
has a spatial curl. That is a quantitative requirement, not a loophole: it says
how much transverse force the receiver must exert on the flow to sustain a
given vorticity, and it has to come from a mechanism rather than be posited.

## 2. The averaged kinetic stress cannot be negative, and the result is stronger than stated

§13.6 gives `w_eff = 2/3` and qualifies it as holding "for any superposition of
families with vanishing cross terms". Both the value and the positivity are in
fact unconditional.

**The value is an identity.** With `R_ij = <rho dv_i dv_j>`,

    p_R = Tr(R)/3,      eps_kin = (1/2) <rho |dv|^2> = Tr(R)/2,

so `w_eff = p_R / eps_kin = 2/3` for *any* velocity field and *any* non-negative
weight. Transversality and vanishing cross terms play no role: the two
quantities are the same trace with different factors. Verified over strongly
correlated, rank-one, anticorrelated, shear-like and heavy-tailed multi-scale
fields; `w_eff = 0.6667` in every case.

**The positivity needs one hypothesis.** For any direction `n`,

    n^i R_ij n^j = < rho (n . dv)^2 > >= 0   whenever rho >= 0,

so `R` is positive semidefinite and its trace cannot be negative, whatever the
correlations. Replacing `rho` by a signed weight — which `rho >= 0` forbids —
does produce negative eigenvalues, confirming that this is the hypothesis
carrying the result.

**What this rules out.** No averaged quadratic stress built from a non-negative
mass density and any velocity field, at any number of scales, with any
correlations, can have negative pressure. The route "vortices concentrate
energy, therefore negative pressure" is closed at this level, and not by an
approximation that a more careful average could repair.

**A distinction the cosmological reading needs.** The low pressure in a vortex
core is not this quantity. For incompressible Navier-Stokes the pressure is
determined only up to an additive function of time, `p -> p + C(t)`, which
changes no motion; the core depression is a difference within a solution, not
an absolute value. A cosmological interpretation needs the full stress tensor,
where that freedom is fixed by the coupling to gravity, and the fixed value is
the one bounded below by zero above.

**Where the sign could still change.** Not in the kinetic term. The candidates
are interaction stresses, which carry potential energy and are not of the form
`<rho dv dv>`; a receiver with its own dynamics and pressure; and bulk
viscosity, `Pi = -zeta Theta`, which is negative in expansion. Only the last two
survive as routes, and the third is the subject of the separate assessment of
dissipative hydrodynamics.
