# Where the reinforcement coefficient comes from, and what Paper I's argument missed

## The gap in the published argument

Paper I, §8.5, argues for `alpha > 0` like this: the upward and downward
nucleation rates satisfy `Gamma_up / Gamma_down = exp(-Delta S)` with
`Delta S = S(V) - S(V + q h) ~ 24 pi^2 Mpl^4 q h / V^2 > 0`, and `Delta S`
"itself decreases as V grows, so the upward rate rises with accumulated flux".

That does not follow. `Delta S` controls the **ratio**. Writing
`Gamma_up = Gamma_down exp(-Delta S)`,

    d ln Gamma_up / dh = d ln Gamma_down / dh - d Delta S / dh,

and the first term is never computed. If the downward rate fell faster than the
suppression relaxed, the upward rate would fall too. The conclusion needs the
other term.

## The calculation

**Hypotheses, all stated.**

- **(H1)** The downward nucleation is described by the thin-wall bounce in the
  weak-gravity limit, `B_down = 27 pi^2 sigma^4 / (2 (q h)^3)` (Coleman 1977),
  with `sigma` the membrane tension. Validity requires the critical bubble to
  be small against the de Sitter horizon, which works out to
  `sigma < (sqrt 6 / 3) Mpl q ~ 0.816 Mpl q`.
- **(H2)** Detailed balance between de Sitter vacua,
  `Gamma_up / Gamma_down = exp(-Delta S)`, with `S = 24 pi^2 Mpl^4 / V`.
- **(H3)** `V = h^2/2` and one membrane shifts the flux by `q`.

**Result.** Both contributions scale the same way in the flux:

    ln Gamma_up = -K / h^3,    K = pi^2 (96 Mpl^4 q^4 + 27 sigma^4 / 2) / q^3 > 0.

The bounce action and the entropy penalty are *both* proportional to `h^-3`, so
they push in the same direction, and

    d ln Gamma_up / dh = 3K / h^4 > 0.

The conclusion of Paper I survives. Its argument does not: it establishes the
weaker half and omits the half that could have cancelled it.

**Which term dominates.** In the regime where (H1) holds,

    K_bounce / K_entropy = 9 sigma^4 / (64 Mpl^4 q^4) < 1/16,

so the reinforcement is driven by the entropy penalty rather than by the
bounce. That is a statement about the mechanism, not a technicality: what makes
each successive nucleation easier is that the horizon entropy cost of a step
falls as the vacuum grows.

## What the exponential law actually requires

The kinetic law of Paper I needs `log Gamma` linear in `h` across the swept
range `Delta h = N q`. From `ln Gamma = -K h^-3`:

    d^2 ln Gamma / dh^2  =  -12 K / h^5,

so the relative curvature across the range is `4 N q / h`, and the relative
error of truncating at the linear term, evaluated at the end of conversion, is

    2 N q / h.

The exponential form is therefore an approximation valid when the total flux
converted is small against the flux already present, `N q << h`, with a
quantitative error. Paper I states the linearity as a modelling choice; it is
derivable, with a range.

## The coefficient, and a relation between it and the entropy

    alpha = N q d ln Gamma / dh = 3 (N q / h) Delta S [1 + O((sigma / Mpl q)^4)],

with `Delta S = 96 pi^2 Mpl^4 q / h^3` the entropy change per step. So the
reinforcement coefficient is three times the product of the fractional flux
swept and the entropy cost of a single step. Combined with the linearity
condition `N q / h < 1/4`,

    alpha < (3/4) Delta S.

That is a consistency relation, not a fit: a model with `alpha` of order unity
requires an entropy change per step of at least order unity, and the two cannot
be chosen independently.

## What this does not do

It does not produce `beta` or `tau_M`. Nothing in the bridge generates the
memory sector, as Paper I already says. It does not address whether the
nucleation is thermal or driven, which is the caveat Paper I attaches and which
this calculation inherits: `alpha` derived here is the *structure* of the rate's
dependence on flux, under detailed balance, and detailed balance is an
equilibrium statement applied to a process Paper I assumes to be driven.

It also does not establish that the wall remnant is the Skyrme defect of §11.
That identification is asserted in §8.5 and is examined separately.
