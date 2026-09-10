"""Physical constants and unit conventions.

Densities are expressed as reduced densities ("omegas"),
    omega_X = rho_X / (3 M_Pl^2 H_100^2),   H_100 = 100 km/s/Mpc,
so that the Friedmann equation reads E^2 = sum_X omega_X with E = H/H_100 and
E(a=1) = h.  Time variable is N = ln a with a_0 = 1, hence N <= 0 in the past.
"""
from __future__ import annotations

import numpy as np

# --- exact / defined ---------------------------------------------------------
C_LIGHT_KM_S = 299792.458            # km/s (exact)
MPC_KM = 3.085677581491367e19        # km per Mpc (IAU 2015 definition of pc)
H100_INV_MPC = 100.0 / C_LIGHT_KM_S  # H_100 in 1/Mpc  -> c/H_100 = 2997.92458 Mpc
HUBBLE_DIST_MPC = C_LIGHT_KM_S / 100.0   # c/H_100 [Mpc]

# --- CMB and relativistic species -------------------------------------------
T_CMB_K = 2.7255                     # Fixsen 2009
OMEGA_GAMMA = 2.47282e-5             # omega_gamma = Omega_gamma h^2 at T_CMB_K
N_EFF = 3.044                        # Standard-Model value (Bennett et al. 2021)
N_NU_MASSIVE = 1                     # one massive eigenstate ...
SUM_M_NU_EV = 0.06                   # ... carrying the minimal normal-ordering mass
# Neutrino temperature today, in eV:  k_B T_nu0 = (4/11)^{1/3} k_B T_cmb
KB_TCMB_EV = 8.617333262e-5 * T_CMB_K
KB_TNU0_EV = (4.0 / 11.0) ** (1.0 / 3.0) * KB_TCMB_EV
# Fermion-to-boson energy-density ratio per species, with the standard
# instantaneous-decoupling factor:
NU_PREFACTOR = (7.0 / 8.0) * (4.0 / 11.0) ** (4.0 / 3.0)

# Massive-neutrino interpolation (Komatsu et al. 2011, WMAP7 Eq. 51);
# accurate to ~0.1% across the relativistic/non-relativistic transition.
NU_FIT_A = 180.0 * 1.2020569031595943 / (7.0 * np.pi ** 4)   # 180 zeta(3)/(7 pi^4)
NU_FIT_P = 1.83

# --- reproducibility ---------------------------------------------------------
SEED = 20260909
