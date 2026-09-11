# Auditing the bridge of §8.5: what is connected and what is only adjacent

Paper I opens §8.5 with "the three constructions above are related by more than
analogy, and this subsection states the connection precisely enough to be
attacked". Attacking it, the claim splits into two halves that fare very
differently.

## What does hold: the event sequence

The identification of the nucleation sequence with the reinforced birth process
is sound and is now more than sound, because the rate's dependence on flux is
derivable rather than asserted (see `02_reinforcement_from_the_bridge.md`). That
half of the bridge survives.

## What does not: the remnant is not the Skyrme object

§8.5 says the wall energy that does not disperse "is the localized remnant" and
that such remnants "are candidates for the defect sector of §11". No map is
given, and the two constructions do not share the ingredients a map would need.

| | four-form sector (§8.1, §8.5) | localized defect (§11) |
|---|---|---|
| field | 3-form potential `A_{mu nu rho}`, no propagating modes in 4D | `n^A(x)`, `A = 1..4`, `n·n = 1`, i.e. an SU(2)-valued scalar |
| object | membrane (2-brane), a domain wall | texture, a map `S^3 -> S^3` |
| charge | membrane charge `q`, a gauge charge | degree in `pi_3(S^3) = Z` |
| what sets the size | nothing in the action | the quartic Skyrme term, against Derrick |
| boundary condition | flux `h` at infinity | `n ->` const at infinity |

These are independent constructions that happen to appear in the same paper.
Nothing in the four-form action contains an SU(2)-valued scalar, and nothing in
the Skyrme energy contains a 3-form gauge field or a membrane charge. The
homotopy groups are not the same group, and neither is a relabelling of the
other.

**The minimal honest statement** is therefore that §8.5 connects the *kinetics*
to the four-form sector and says nothing about the defect sector; the defect of
§11 remains a calculable representative of a localized product, which is what
§11 itself already calls it, and not the remnant of a membrane.

## And the remnant is not stable anyway

Independently of whether it is a Skyrmion, the thin-wall membrane leaves no
localized object in the theory as written. For a closed wall of radius `R`
enclosing a region lower in vacuum energy by `Delta V`,

    E(R) = 4 pi R^2 sigma - (4/3) pi R^3 Delta V,
    dE/dR = -4 pi R (R Delta V - 2 sigma),

whose only non-zero critical point is `R_c = 2 sigma / Delta V` with

    E''(R_c) = -8 pi sigma < 0.

That is a **maximum**, the familiar critical bubble: the wall either collapses
or runs away, and there is no radius at which it sits. `E(R_c) =
16 pi sigma^3 / 3 (Delta V)^2` is the barrier, not a rest mass.

So "the wall energy that does not disperse is the localized remnant" assumes a
stabilisation mechanism that the four-form-plus-membrane action does not
contain. Producing one requires an extra ingredient — angular momentum, a
conserved charge on the wall, a repulsive core, or a different action — and
whichever is chosen has to be declared, because it changes the theory.

## Consequence for the branching ratio

`b = E_wall / epsilon` is presented in §8.5 as making the branching ratio "not a
free parameter but a ratio of energies". With no stable remnant, `E_wall` is not
the energy of an object; it is the energy that fails to reach the vacuum and
must go somewhere else — radiation, gravitational waves, or a black hole. The
identification of `b` with a defect fraction therefore does not follow from this
bridge either.

That does not make `b` meaningless: it remains the fraction of transferred
energy that does not end as vacuum, which is what the cosmological sections
actually use. What it is not is a fraction that ends as defects.
