# Paper II — assessment before starting

## What the central result of Paper I actually is

Stripped of everything it does not claim, Paper I establishes one thing: **that
a dark-sector transfer whose rate carries an internal memory variable is a
structurally different object from any transfer written as a function of the
densities and the expansion rate, and that the difference is the dimension of
the state space rather than the shape of a coupling.** Everything else is
either a consequence of that (the positivity theorem, whose real content is the
donor-proportional criterion; the jerk inequality and its sign; the
b-independence of linear growth) or a boundary marker on it (the caustic
obstruction, the covariant dichotomy, the observational null). The memory law
and its hysteresis are the load-bearing novelty; the dark-sector interpretation
is scaffolding around it.

That reading matters for Paper II, because it says the productive direction is
whatever sharpens or breaks the state-space claim, not whatever makes the dark
matter identification more plausible.

## Discrepancies between the PDF, the working summaries and the repository

Checked directly against `paper/build/main.pdf`, `results/*.json` and the code.

1. **Lindblad, N = 8 vs N = 512.** Working summaries said the open-system sector
   was exact only to N = 8. Wrong, and it mattered: N = 8 is the limit of the
   *full Liouvillian*. Because the jump operators preserve permutation symmetry,
   the same observable comes from the (N+1)-state symmetric chain, which the
   repository runs to **N = 512** (`results.json: lindblad.closure_N_max`),
   giving a fitted exponent of -1.011 and a local slope at the largest N of
   -1.001. Extending N is not a pending task. Justifying the scaling
   analytically, and bounding where the symmetric reduction is faithful, is.

2. **Between-seed reproducibility of ln Z.** A referee reported that an
   independent seed moved `ln Z(xi_h)` by 0.944, some 4.5 times its quoted
   error, and that finding was carried into the working notes. A controlled
   three-seed measurement with the same script and settings
   (`results/evidence_repeatability.json`) gives values -733.935, -734.088,
   -733.796: a standard deviation of **0.146** against a reported error of
   0.208, a ratio of 0.70. The scatter is *consistent* with the quoted error.
   The referee's replicate is an outlier relative to this sample, or was run
   with different settings. Three seeds is a small sample and this should be
   said, but the claim that the evidence is irreproducible is not supported by
   the controlled measurement. Paper I's comparison stands at the level of
   sampler noise.

3. **Maximisation protocol.** The chi-square column is produced by a screened
   protocol validated against a frozen brute-force reference
   (`results/map_reference.json`); it lands 0.015 above it for the
   six-parameter model, which is 0.9 per cent of the chi-square difference the
   comparison turns on. Working summaries at one point reported agreement to
   4e-5; that comparison was invalid (the reference file had not been
   rewritten) and has been corrected.

4. **Pancake scope.** The runs approach but never cross the caustic: with the
   fiducial profile J = 1 - D cos(kq) > 0 for D < 1. Any statement about the
   multi-stream regime is outside what has been computed. This is stated
   correctly in the PDF; it is worth repeating here because Front 2 exists
   precisely to lift it.

## What is frozen

`paper/` is the release candidate and is not touched by this work. Paper II
lives in `paper2/`, on branch `paper2`.
