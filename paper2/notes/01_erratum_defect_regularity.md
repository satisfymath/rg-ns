# Erratum to Paper I: the regularity condition at a caustic is incomplete

**Status: demonstrated error in a boxed level-C result. Minimal correction
given below.**

## The affected equation

`paper/sections/11_defects.tex`, `eq:defects-regularity`:

> T_{mu nu} finite at the caustic  <=>  g > c  and  b = 0

and the sentence supporting it (same file, ~line 195):

> "the defect density obeys d rho_D/dt = -Theta rho_D + b Gamma rho_I, whose
> homogeneous part alone gives rho_D ~ (T-t)^{-c}: ... so its density diverges
> for every g **whenever b > 0**."

## What is wrong

The sentence correctly identifies that the *homogeneous* part of the defect
equation behaves as `(T-t)^{-c}`, and then attributes the divergence to
`b > 0`. Those are different statements. The homogeneous solution is

    rho_D^hom(t) = rho_D(t_0) exp(-int Theta dt) = rho_D(t_0) |J_0 / J|,

which diverges as `|J| -> 0` for **any** non-zero initial defect density,
whatever `b` is. Setting `b = 0` removes the *source* — the particular
solution — and leaves the homogeneous one untouched.

So `b = 0` is necessary but not sufficient. The condition is

    T_{mu nu} finite  <=>  g > c  and  b = 0  and  rho_D(t_0) = 0,

that is: no localized product may be present on the collapsing sheet at all,
not merely none produced during the collapse.

## Verification

Integrating the exact local system (`absorb.collapse.LocalSector`) with
`c = 1`, `g = 1.5` — so that the precursor and the vacuum are both regular —
and reading the exponent of `rho_D` from three distances to the caustic:

| b | rho_D(t_0) | rho_D at s = 1e-6 | measured exponent |
|---|---|---|---|
| 0.00 | 0.0 | 0 | — |
| **0.00** | **0.1** | **1.0e5** | **-1.0000** |
| 0.00 | 1.0 | 1.0e6 | -1.0000 |
| 0.25 | 0.0 | 2.5e5 | -1.0000 |

The second and third rows are the counterexample: `b = 0`, and the density
still diverges with exponent exactly `-c`.

## Why it matters, beyond the erratum

This closes a route that looked open. The obstruction as stated in Paper I is
that regularity wants `b = 0` while a relic abundance wants `b > 0`, which
invites the repair: *form the defects through a different channel, before the
collapse, and let the compression-driven channel feed only the vacuum*. The
corrected condition rules that out. Defects formed earlier are pressureless
dust on the collapsing sheet; they compress as `|J|^{-1}` like anything else,
and the stress tensor diverges regardless of how they were made.

So the obstruction is **stronger** than Paper I claims, not weaker: pointwise
regularity of `T_{mu nu}` at a fold caustic is incompatible with the presence
of any localized product there, by any mechanism.

The caveat Paper I already attaches survives unchanged and is worth repeating:
pointwise finiteness of `T_{mu nu}` is not a criterion for the absence of a
spacetime singularity, and a generic fold caustic of a dust congruence is
Tipler-weak and expected to be extendible. What diverges is the source in the
field equations, not necessarily the geometry.

## Minimal correction to the manuscript

Two changes, both local:

1. In `eq:defects-regularity`, add the third condition.
2. In the supporting sentence, replace "whenever `b > 0`" with a statement that
   the homogeneous part diverges for any non-zero initial defect density, and
   that `b = 0` removes only the source.

A regression test is added at `code/tests/test_collapse.py`
(`test_zero_branching_does_not_make_the_defect_density_finite`), which fails if
the weaker condition is reinstated.
