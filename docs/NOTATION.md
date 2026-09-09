# Notation

The Spanish draft reuses several symbols for unrelated objects. This table is
the single source of truth for the manuscript; Appendix A of the paper is
generated from it. Clashes inherited from the draft are listed at the end with
their resolution.

## Geometry and gravity

| Symbol | Macro | Meaning | Mass dimension |
|---|---|---|---:|
| $g_{\mu\nu}$ | | metric, signature $(-+++)$ | 0 |
| $M_{\rm Pl}$ | `\Mpl` | reduced Planck mass, $M_{\rm Pl}^2=(8\pi G)^{-1}$ | 1 |
| $G_{\mu\nu}$ | `\Gmn` | Einstein tensor | 2 |
| $T_{\mu\nu}$ | `\Tmn` | total stress-energy tensor | 4 |
| $u^\mu$ | `\umu` | four-velocity of the precursor/clock congruence | 0 |
| $\Theta$ | `\expa` | expansion scalar, $\Theta=\nabla_\mu u^\mu$ | 1 |
| $T$ | `\clock` | constrained clock field | $-1$ |
| $\lambda$ | `\lagm` | Lagrange multiplier of the clock constraint | 4 |
| $\mathcal{H}_{\mu\nu\rho\sigma}$ | `\fourform` | four-form field strength | 2 |
| $h$ | | four-form flux amplitude | 2 |

## Cosmological densities

| Symbol | Macro | Meaning |
|---|---|---|
| $\rho_I$ | `\rhoI` | precursor (pressureless, converted away) |
| $\rho_D$ | `\rhoD` | localized defects (pressureless, produced) |
| $V$ | `\rhoV` | vacuum energy density, $p_V=-V$ |
| $\rho_{\rm b},\rho_{\rm r}$ | `\rhob`,`\rhor` | baryons and radiation, separately conserved |
| $\rho_{\rm m}$ | `\rhom` | total pressureless matter, $\rho_I+\rho_D+\rho_{\rm b}$ |
| $\rho_{\rm dm}^{\rm eff}$ | `\rhodmeff` | effective dark matter, $\rho_I+\rho_D$ |
| $\omega_X$ | | reduced density $\rho_X/(3M_{\rm Pl}^2H_{100}^2)$ |

## Absorption kinetics

| Symbol | Macro | Meaning |
|---|---|---|
| $f$ | `\fconv` | converted fraction, $\dot f=(1-f)\Gamma$ |
| $M$ | `\Mmem` | memory variable, $\tau_M\dot M=f-M$ |
| $\Gamma$ | `\Gam` | conversion rate, $\Gamma_0e^{\alpha f+\beta M}S_{\rm act}$ |
| $\alpha,\beta$ | | instantaneous and memory reinforcement strengths |
| $\tau_M$ | `\tauM` | memory relaxation time |
| $b$ | `\bfrac` | branching ratio of converted energy into defects |
| $\epsilon$ | | convertible fraction, $(1-b)\rho_{I,\rm act}/\omega_c$ |
| $Q_V$ | `\QV` | transfer density-rate, $(1-b)\Gamma\rho_I$ |
| $\Gamma_\downarrow$ | `\Gamdn` | reverse channel rate (Track B) |
| $S_{\rm act}(a)$ | `\actS` | activation switch, $a^p/(a^p+a_{\rm act}^p)$ |

## Expansion and cosmography

| Symbol | Macro | Meaning |
|---|---|---|
| $H$, $E$ | `\Hub` | Hubble rate; $E=H/H_{100}$, so $E(a{=}1)=h$ |
| $N$ | `\efold` | $\ln a$, the time variable used throughout |
| $q$ | `\decel` | deceleration parameter |
| $j$ | `\jerk` | jerk parameter |
| $s$ | `\snap` | snap parameter |
| $\Omega_X$ | `\Om{X}` | density parameter $\omega_X/E^2$ |

## Clashes inherited from the draft, and their resolution

| Draft symbol | Two meanings | Resolution here |
|---|---|---|
| $\Gamma$ | conversion rate; Christoffel symbol | rate keeps $\Gamma$; Christoffels are written $\Gamma^\rho{}_{\mu\nu}$ only inside Sec. 2 and Appendix A, where no rate appears |
| $M$ | memory variable; Planck mass | memory keeps $M$; the mass is always $M_{\rm Pl}$, never $M$ |
| $b$ | branching ratio; baryon subscript | branching keeps $b$; baryons carry the roman subscript $\rm b$ |
| $\lambda$ | clock multiplier; Derrick scaling; double-well coupling | multiplier keeps $\lambda$; Derrick scaling is $\sigma$; the double-well coupling is $\lambda_W$ |
| $T$ | clock field; stress tensor; temperature | clock keeps $T$; the tensor is always indexed $T_{\mu\nu}$; temperature is $\mathcal{T}$ |
| $A$ | $\ddot a/a$; four-acceleration; gauge field | $\ddot a/a$ is written out; acceleration is $A^\mu$; the gauge field is $A_\mu$ |
| $W$ | double-well potential; Skyrme tensor; Schrodinger potential | potential keeps $W$; the Skyrme tensor is $\mathcal{W}_{ij}^{AB}$; the Schrodinger potential is $U$ |
| $\mathcal{H}$ | four-form; history filtration; Hilbert space | four-form keeps $\mathcal{H}$; the filtration is $\mathfrak{F}_t$; the Hilbert space is $\mathscr{H}$ |
| $q$ | deceleration; electric charge; membrane charge | deceleration keeps $q$; electric charge is $q_*$; membrane charge is $\mathsf{q}$ |
