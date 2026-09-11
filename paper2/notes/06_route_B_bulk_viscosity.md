# Route B assessed: what the conversion can and cannot do to the pressure

## The question

Can the model's own dynamics generate a bulk viscous stress `Pi = -zeta Theta`
with `zeta > 0`, which is negative in expansion and could drive acceleration
without postulating an exact vacuum?

## Reading the conversion as a bulk pressure

Each sector obeys `d rho/dt + 3H(rho + p + Pi) = 0`. Solving for the `Pi` that
reproduces the model's own equations, with the precursor losing energy at rate
`Gamma rho_I` and a fraction `b` reaching the defects:

    Pi_I = + Gamma rho_I / 3H        (donor: positive)
    Pi_D = - b Gamma rho_I / 3H      (recipient: negative)

The recipient does acquire a negative effective pressure, which is the result
from particle-creation cosmology and is not an artefact. But the donor acquires
an equal and opposite one, and

    Pi_I + Pi_D = (1 - b) Gamma rho_I / 3H,

which vanishes identically when `b = 1`, that is when the conversion is
entirely between the two pressureless sectors.

As a viscosity the donor's coefficient is `zeta_I = -Gamma rho_I / 9H^2 < 0`,
which the second law forbids. That negative sign is the tell: the precursor is
not dissipating, it is handing energy to something else, and calling that
viscosity misreads it.

## The general statement

**Proposition.** Let the dark sector consist of components exchanging energy
with no momentum transfer, each a perfect fluid with its own density `rho_i`
and pressure `p_i`. Then the total pressure is the sum of the `p_i`,
independent of every transfer rate. In particular, if every component is
pressureless the total is pressureless, and the expansion never accelerates,
whatever the rate, the reinforcement, or the memory.

**Corollary.** Acceleration requires `sum_i (rho_i + 3 p_i) < 0`, which is a
statement about the components' own equations of state. The kinetics decides
how much energy each component holds. It cannot manufacture an equation of
state.

**Verification.** Integrating the two-sector system with all conversion going
to the defects, over eight random draws of `(Gamma_0, alpha, beta, tau_M)`
spanning two decades in rate and the full prior ranges of reinforcement and
memory: `(rho + 3p)/rho = 1.000000` in every case, and the total density obeys
`d rho / dN = -3 rho` to `6e-13`. The conversion is invisible in the total
pressure.

## What this means for Paper I, and for Route B

It is the honest statement of where the acceleration in Paper I comes from. The
exact vacuum's `p = -V` does all of the work; the kinetics, the reinforcement
and the memory decide only how much vacuum there is by today. No amount of
conversion between pressureless sectors substitutes for that equation of state.

For Route B it means the bulk-viscous route is not a reinterpretation of the
existing model but a different theory. Genuine bulk viscosity with `zeta > 0`
requires dissipation -- entropy production -- and an internal variable whose
relaxation lags the expansion. The memory variable `M` is such a variable, and
that is suggestive, but a pressureless fluid has no pressure for the lag to act
on: the standard result `zeta ~ tau (dp/dxi)(dxi_eq/drho)(rho + p)` vanishes
identically when `p = 0` and `rho + p = rho` multiplies a zero derivative. A
bulk viscosity therefore requires the matter sector to have pressure in the
first place, which the model does not give it.

## The minimal modification, and its cost

Give the recipient its own pressure. That is the one route the proposition
leaves open, and it is the same conclusion the covariant dichotomy of §11.5
reached from a different direction: a recipient with dynamics and pressure,
rather than an exact vacuum, is what both obstructions point at.

The cost is that `p = -V` exactly is what makes the vacuum *silent* --- no rest
frame, no perturbations, no sound speed. A recipient with pressure has all
three, and the perturbation results of §9 would have to be redone rather than
inherited. That is a substantial change, not a reinterpretation, and it belongs
in a separate development rather than in this manuscript.
