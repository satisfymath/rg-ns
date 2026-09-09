"""DESI DR2 baryon-acoustic-oscillation distance measurements.

The release gives 13 numbers: one spherically averaged D_V/r_d (the BGS
tracer at z_eff = 0.295) and six anisotropic (D_M/r_d, D_H/r_d) pairs, with a
13 x 13 covariance in the *same order as the mean file*.  That order is not
sorted -- at z = 2.33 (the Lyman-alpha forest) D_H comes **before** D_M --
so the loader preserves the file order exactly and the likelihood dispatches
on the quantity string rather than on position.

Quantity strings and their meaning (r_d = comoving sound horizon at the drag
epoch, :func:`absorb.early.r_drag`):

    ``DV_over_rs``  D_V/r_d with D_V = [z D_M^2 D_H]^{1/3}
    ``DM_over_rs``  transverse comoving distance / r_d
    ``DH_over_rs``  c/H(z) / r_d
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.linalg import cho_factor

from .paths import check_covariance, raw_path

__all__ = ["BAOData", "load_desi"]

_MEAN = "desi_dr2_bao_mean.txt"
_COV = "desi_dr2_bao_cov.txt"

#: Quantity strings the BAO likelihood knows how to model.
KNOWN_QUANTITIES = ("DV_over_rs", "DM_over_rs", "DH_over_rs")


@dataclass(frozen=True)
class BAOData:
    """A BAO data vector in file order.

    Attributes
    ----------
    z
        Effective redshift of each entry.
    value
        Measured ratio.
    quantity
        One of :data:`KNOWN_QUANTITIES`, per entry.
    cov, cho
        Covariance and its Cholesky factorisation.
    label
        Human-readable name of the compilation.
    """

    z: np.ndarray
    value: np.ndarray
    quantity: np.ndarray
    cov: np.ndarray
    cho: tuple[np.ndarray, bool]
    label: str

    @property
    def n(self) -> int:
        return self.z.size


def read_bao_pair(mean_file: str, cov_file: str, label: str) -> BAOData:
    """Read a ``z value quantity`` table plus its covariance, preserving order."""
    path = raw_path(mean_file)
    z, value, quantity = [], [], []
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            a, b, c = line.split()[:3]
            z.append(float(a))
            value.append(float(b))
            quantity.append(c)
    z = np.asarray(z, dtype=float)
    value = np.asarray(value, dtype=float)
    quantity = np.asarray(quantity, dtype="<U16")

    C = np.loadtxt(raw_path(cov_file), dtype=float)
    C = np.atleast_2d(C)
    if C.shape[0] != z.size:
        raise ValueError(
            f"{label}: covariance is {C.shape} but the mean vector has {z.size} entries"
        )
    C = check_covariance(C, label)
    return BAOData(z=z, value=value, quantity=quantity, cov=C,
                   cho=cho_factor(C, lower=True), label=label)


@lru_cache(maxsize=1)
def load_desi() -> BAOData:
    """Load and cache the 13-point DESI DR2 BAO vector."""
    d = read_bao_pair(_MEAN, _COV, "DESI DR2 BAO")
    unknown = set(d.quantity) - set(KNOWN_QUANTITIES)
    if unknown:
        raise ValueError(f"DESI DR2 BAO: unrecognised quantities {sorted(unknown)}")
    return d
