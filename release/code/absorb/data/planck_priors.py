"""Compressed CMB likelihood: the Planck 2018 distance priors.

Instead of the full Planck likelihood we use the three-parameter compression
(R, l_A, omega_b) of Chen, Huang & Wang (2019, ApJ 883, 175;
arXiv:1808.05724), derived from the Planck 2018 TT,TE,EE+lowE chains:

    R    = sqrt(Omega_m H_0^2) D_M(z_*) / c    (shift parameter)
    l_A  = pi D_M(z_*) / r_s(z_*)              (acoustic scale)
    omega_b = Omega_b h^2

This compression is lossless for models that share standard pre-recombination
physics and differ only in their late-time expansion history -- exactly the
situation here, where the absorption switch is closed at recombination (see
:mod:`absorb.early`).  It is *not* valid for models that change the early
sound horizon, and we say so in the paper.

Values (their Table I, "Planck 2018 TT,TE,EE+lowE"):

    R       = 1.7502  +/- 0.0046
    l_A     = 301.471 +/- 0.090
    omega_b = 0.02236 +/- 0.00015

with correlation matrix

           R      l_A    omega_b
    R    [ 1.00   0.46   -0.66 ]
    l_A  [ 0.46   1.00   -0.33 ]
    ob   [-0.66  -0.33    1.00 ]
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.linalg import cho_factor

__all__ = ["PlanckPriors", "load_planck_priors"]

#: Order of the compressed data vector.
PARAM_NAMES = ("R", "l_A", "omega_b")

MEAN = np.array([1.7502, 301.471, 0.02236])
SIGMA = np.array([0.0046, 0.090, 0.00015])
CORR = np.array([
    [1.00, 0.46, -0.66],
    [0.46, 1.00, -0.33],
    [-0.66, -0.33, 1.00],
])


@dataclass(frozen=True)
class PlanckPriors:
    """Mean vector, covariance and Cholesky factor of the compressed CMB data."""

    names: tuple[str, ...]
    mean: np.ndarray
    sigma: np.ndarray
    corr: np.ndarray
    cov: np.ndarray
    cho: tuple[np.ndarray, bool]

    @property
    def n(self) -> int:
        return self.mean.size


@lru_cache(maxsize=1)
def load_planck_priors() -> PlanckPriors:
    """Build and cache the compressed Planck 2018 distance-prior likelihood."""
    from .paths import check_covariance

    C = check_covariance(CORR * np.outer(SIGMA, SIGMA), "Planck distance priors")
    return PlanckPriors(names=PARAM_NAMES, mean=MEAN.copy(), sigma=SIGMA.copy(),
                        corr=CORR.copy(), cov=C, cho=cho_factor(C, lower=True))
