"""Cosmic chronometers: H(z) from the differential age of passively evolving
early-type galaxies (Jimenez & Loeb 2002).

Data: the 15 BC03-calibrated measurements of Moresco et al. (2012, 2015,
2016) collected in ``HzTable_MM_BC03.dat``.  These are the only H(z) points
that are genuinely independent of a cosmological model -- they measure
H = -(1/(1+z)) dz/dt directly -- which is why they are kept as a separate
probe from BAO.

Covariance
----------
The diagonal errors quoted with the data are *statistical plus a partial
systematic*; the full error budget of Moresco et al. (2020, ApJ 898, 82,
"MM20") is correlated across redshift because it comes from the choice of
stellar population model.  Following their prescription, the covariance is

    C = diag(sigma_i^2) + C_IMF + C_SPS,
    C_X[i,j] = (H_i sigma_X(z_i)/100) (H_j sigma_X(z_j)/100),

where sigma_X(z) is the *percentage* systematic of contribution X tabulated
in ``data_MM20.dat`` (hence the factor 1/100) and interpolated linearly in z,
clamped to the end values outside the tabulated range 0.075 <= z <= 1.475.
Each contribution is fully correlated across redshift, which is what makes
these terms rank-one outer products rather than diagonal additions.

Two variants are provided:

``variant="default"``
    IMF + ``mod_ooo``: the initial mass function plus the "odd" stellar
    population model contribution, i.e. the spread among the models that
    survive the MM20 selection.  This is the combination used in the Moresco
    et al. (2020) baseline and in most subsequent analyses.

``variant="conservative"``
    Adds the stellar library (``stlib``) and the full model spread (``mod``),
    which roughly doubles the error bars.  Used as a robustness check.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

import numpy as np
from scipy.linalg import cho_factor

from .paths import check_covariance, raw_path

__all__ = ["CosmicChronometers", "load_cc"]

_HZ = "HzTable_MM_BC03.dat"
_MM20 = "data_MM20.dat"

#: Systematic contributions entering each variant, by column name in data_MM20.dat.
VARIANTS: dict[str, tuple[str, ...]] = {
    "default": ("IMF", "mod_ooo"),
    "conservative": ("IMF", "stlib", "mod", "mod_ooo"),
}
_MM20_COLUMNS = ("IMF", "stlib", "mod", "mod_ooo")


@dataclass(frozen=True)
class CosmicChronometers:
    """H(z) measurements with the Moresco systematic covariance.

    ``H`` and ``err_H`` are in km/s/Mpc; ``cov`` is the full covariance of
    ``H`` including the correlated systematics.
    """

    z: np.ndarray
    H: np.ndarray
    err_H: np.ndarray
    cov: np.ndarray
    cho: tuple[np.ndarray, bool]
    variant: str

    @property
    def n(self) -> int:
        return self.z.size


@lru_cache(maxsize=1)
def _read_hz() -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Comma-separated ``z, Hz, errHz, stat, met, reference``."""
    z, H, err = [], [], []
    with raw_path(_HZ).open() as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",")
            z.append(float(parts[0]))
            H.append(float(parts[1]))
            err.append(float(parts[2]))
    return (np.asarray(z, dtype=float), np.asarray(H, dtype=float),
            np.asarray(err, dtype=float))


@lru_cache(maxsize=1)
def _read_mm20() -> dict[str, np.ndarray]:
    """Percentage systematics table; column 0 is z."""
    raw = np.loadtxt(raw_path(_MM20))
    out = {"z": raw[:, 0]}
    for i, name in enumerate(_MM20_COLUMNS, start=1):
        out[name] = raw[:, i]
    return out


def _sigma_percent(name: str, z: np.ndarray) -> np.ndarray:
    """Percentage systematic of contribution ``name`` at redshifts ``z``.

    ``np.interp`` clamps to the end values outside the tabulated range, which
    is the intended behaviour: the tabulation covers 0.075-1.475 while the
    highest chronometer sits at z = 1.965.
    """
    t = _read_mm20()
    return np.interp(z, t["z"], t[name])


@lru_cache(maxsize=2)
def load_cc(variant: Literal["default", "conservative"] = "default") -> CosmicChronometers:
    """Load and cache the cosmic-chronometer sample (see the module docstring)."""
    if variant not in VARIANTS:
        raise ValueError(f"load_cc: unknown variant {variant!r}, "
                         f"expected one of {sorted(VARIANTS)}")
    z, H, err = _read_hz()
    C = np.diag(err ** 2)
    for name in VARIANTS[variant]:
        s = H * _sigma_percent(name, z) / 100.0     # absolute systematic, km/s/Mpc
        C = C + np.outer(s, s)                      # fully correlated -> rank one
    C = check_covariance(C, f"cosmic chronometers ({variant})")
    return CosmicChronometers(z=z, H=H, err_H=err, cov=C,
                              cho=cho_factor(C, lower=True), variant=variant)
