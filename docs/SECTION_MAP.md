# Section map: Spanish draft v0.2 to the manuscript

Source: `docs/source_draft_es_v0.2.md` (2705 lines). The manuscript is a
rewrite in English, not a translation: statements are recast with explicit
hypotheses, and the corrections listed below are applied.

| New section | Title | Draft source (lines) | Target pages |
|---|---|---|---:|
| 1 | Problem, hypotheses, and what is claimed | 45-87 | 3 |
| 2 | Covariant setup | 89-261 | 3 |
| 3 | Absorbing process with reinforcement and memory | 443-733 | 4 |
| 4 | Homogeneous cosmology with two products | 735-967 | 5.5 |
| 5 | Positivity, and the map to interacting dark energy | NEW (`docs/theory/01`) | 3 |
| 6 | Solvable family and the early-universe branch | 969-1103 + NEW (`docs/theory/02`) | 4 |
| 7 | Cosmographic bounds: jerk and snap | 1105-1202 + NEW (`docs/theory/04`) | 3 |
| 8 | Covariant realizations of a silent vacuum | 263-441 + NEW (four-form bridge) | 4.5 |
| 9 | Linear perturbations | 1204-1330 + NEW (`docs/theory/03`) | 4 |
| 10 | Observational constraints | NEW (MCMC against DESI DR2, Pantheon+, CC, Planck priors) | 5.5 |
| 11 | Localized defects | 1773-1935 + NEW (solved hedgehog profile) | 3.5 |
| 12 | Quantum absorption and irreversibility | 1946-2051 | 2.5 |
| 13 | Outlook | 2054-2184, 1662-1770, 1936-1943, 1646-1659, 2298-2333 | 2 |
| 14 | Conclusions | 2335-2344 | 1 |
| App. A | Conventions and notation | 2347-2370 + `docs/NOTATION.md` | 1.5 |
| App. B | Deferred proofs | 489-536, 855-880 | 3.5 |
| App. C | Quantum-hydrodynamic identities | 1514-1645 | 2 |
| App. D | Hydrodynamics and causality | 1332-1512 | 2 |
| App. E | Skyrme integrals | 2373-2416 | 1.5 |
| App. F | Numerical methods and reproducibility | 2187-2270 | 2 |

Draft Appendix C (audit of v0.1) does not appear in the paper; it seeds
`docs/EDITORIAL_AUDIT.md`. Draft Sec. 13.5 becomes a remark in Sec. 8.

## Corrections applied to the draft

| Draft location | Problem | Correction |
|---|---|---|
| Prop. 7, Eq. (10.4) | assumes $b=0$ silently; wrong for $b>0$ | replaced by the total-matter growth equation, in which $b$ cancels identically (`docs/theory/03`) |
| Sec. 7.7 | "phantom appearance" depends on what the fit anchors | replaced by the sandwich theorem plus the matter deficit (`docs/theory/01`) |
| Eq. (6.6) | a constant rate floor has no viable early universe | replaced by the activation law with $p>3$ (`docs/theory/02`) |
| Theorem 2 | assumes $\Gamma\ge g>0$, violated in the past by activation | restated for $t\ge t_{\rm act}$ |
| Eq. (10.2) | integrability stated, consequence never drawn | the geodesic realization is adopted as an explicit assumption and the alternative is shown to be gradient-unstable |
| Eq. (5.7) | mixes rates with and without memory | restricted to the memoryless pure-birth chain |
| Sec. 16 | OpenAI Navier-Stokes discussion, with web-page citations | compressed to one Outlook paragraph; no non-archival citations |
| throughout | notation clashes | resolved in `docs/NOTATION.md` |
