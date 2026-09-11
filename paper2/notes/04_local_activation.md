# The activation switch has an exact local form, and it switches off under compression

## The problem

`S_act(a) = a^p / (a^p + a_act^p)` refers to the FLRW scale factor. That is not
a local scalar, so as written the rate law is a statement about the homogeneous
mode and cannot be evaluated in an inhomogeneous region — including the
collapsing regions §11.5 is about.

## An exact rewriting

The survival identity `rho_I a^3 = rho_I,act (1 - f)` is exact, so `a` can be
eliminated with no approximation. Writing `rho_* = rho_I,act / a_act^3` for the
comoving precursor density at activation,

    S_act = [ 1 + ( rho_I / ((1-f) rho_*) )^{p/3} ]^{-1}.

Verified against `S_act(a)` over 2000 random draws of `(p, a_act, a, f,
rho_I,act)`: maximum difference `3.3e-16`. It involves only `rho_I` and `f`,
both local.

It also reads physically: conversion switches on when the precursor has diluted
below a threshold density `rho_*`, rather than at a particular epoch. The
threshold replaces the activation redshift as the parameter.

## What it does at a caustic

Under compression at fixed `f`, the switch closes:

    S_act  ->  ( (1-f) rho_* / rho_I )^{p/3}   as rho_I -> infinity.

Near a fold caustic `rho_I ~ |J|^{-1}`, so

    Gamma = Gamma_0 S_act e^{alpha f + beta M}  ~  |J|^{p/3}  ->  0.

Numerically, with `p = 6` and `f = 0.3`, `S_act` falls from `0.99` at
`rho_I = 0.01 rho_*` to `4.9e-13` at `rho_I = 10^6 rho_*`.

**So the rate does not merely stay bounded on the approach to a caustic; it
vanishes.** In the language of §11.5, where regularity needs `Gamma ~ g/(T-t)`
with `g > c`, this rate behaves as `(T-t)^{+p/3}`: the exponent has the wrong
sign, not merely too small a value. Theorem A says a bounded rate cannot
regularize a caustic. With the activation law written locally, the model's own
rate switches itself off there, which is strictly worse.

## Honest limit of the claim

This is *one* local completion, not *the* local completion. It is distinguished
by using only the survival identity, with no extra assumption, and by reducing
to `S_act(a)` identically on FLRW rather than approximately.

Other completions exist and need not behave the same way. A switch written in
the expansion `Theta` also reduces to a function of `a` on FLRW, but with an
epoch-dependent exponent, and it has the **opposite** behaviour at a caustic:
`Theta -> -infinity` there, and a switch that is decreasing in `Theta` — which
is what matching the FLRW behaviour requires, since `Theta` falls as the
universe ages — would saturate at its maximum rather than close.

So the completions disagree qualitatively exactly where it matters, and the
manuscript cannot claim a definite behaviour at a caustic without choosing one.
What it can say, and what the calculation above establishes, is that the
completion built from the exact identity of the model itself suppresses
conversion under compression.
