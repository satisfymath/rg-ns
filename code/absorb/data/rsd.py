"""SDSS-IV/eBOSS DR16 full-shape + BAO consensus measurements.

Two catalogues are provided by the collaboration in the "FS+BAO" (full shape
plus BAO) consensus form (Alam et al. 2021, PRD 103, 083533):

* LRG, three effective redshifts z = 0.38, 0.51, 0.698, three quantities each
  (D_M/r_d, D_H/r_d, f sigma_8) -- 9 numbers with a block 9 x 9 covariance;
* QSO, one effective redshift z = 1.48, the same three quantities -- 3 numbers.

Only the ``f_sigma8`` entries are used by
:class:`~absorb.likelihoods.RSDLikelihood`; the geometric entries of these
same catalogues overlap in volume with DESI DR2 and are therefore *not*
combined with it, to avoid double counting.  Because the three quantities at
one redshift are strongly correlated, the RSD likelihood must extract the
f sigma_8 rows *and columns* of the covariance -- taking only the diagonal
would misstate the errors.  :attr:`FSBAOData.fs8_index` provides those
indices and :meth:`FSBAOData.fs8_block` the sub-covariance.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.linalg import cho_factor

from .paths import check_covariance, raw_path

__all__ = ["FSBAOData", "load_rsd"]

_FILES = {
    "LRG": ("sdss_DR16_LRG_FSBAO.dat", "sdss_DR16_LRG_FSBAO_cov.txt"),
    "QSO": ("sdss_DR16_QSO_FSBAO.dat", "sdss_DR16_QSO_FSBAO_cov.txt"),
}


@dataclass(frozen=True)
class FSBAOData:
    """Concatenated DR16 full-shape + BAO vector, in file order.

    ``tracer`` labels each entry with the catalogue it came from; the
    covariance is block diagonal between catalogues (they are disjoint
    samples) and dense within each block.
    """

    z: np.ndarray
    value: np.ndarray
    quantity: np.ndarray
    tracer: np.ndarray
    cov: np.ndarray
    cho: tuple[np.ndarray, bool]

    @property
    def n(self) -> int:
        return self.z.size

    @property
    def fs8_index(self) -> np.ndarray:
        """Indices of the ``f_sigma8`` entries in the full vector."""
        return np.flatnonzero(self.quantity == "f_sigma8")

    def fs8_block(self) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Return ``(z, f sigma_8, covariance)`` of the f sigma_8 sub-vector."""
        i = self.fs8_index
        return self.z[i], self.value[i], self.cov[np.ix_(i, i)]


def _read_one(tag: str) -> tuple[np.ndarray, ...]:
    mean_file, cov_file = _FILES[tag]
    z, value, quantity = [], [], []
    with raw_path(mean_file).open() as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            a, b, c = line.split()[:3]
            z.append(float(a))
            value.append(float(b))
            quantity.append(c)
    C = np.atleast_2d(np.loadtxt(raw_path(cov_file), dtype=float))
    if C.shape[0] != len(z):
        raise ValueError(f"DR16 {tag}: covariance {C.shape} vs {len(z)} data points")
    return (np.asarray(z, dtype=float), np.asarray(value, dtype=float),
            np.asarray(quantity, dtype="<U16"), C)


@lru_cache(maxsize=1)
def load_rsd() -> FSBAOData:
    """Load and cache the concatenated LRG + QSO DR16 FS+BAO vector."""
    blocks = [_read_one(tag) for tag in ("LRG", "QSO")]
    z = np.concatenate([b[0] for b in blocks])
    value = np.concatenate([b[1] for b in blocks])
    quantity = np.concatenate([b[2] for b in blocks])
    tracer = np.concatenate([
        np.full(b[0].size, tag, dtype="<U8")
        for tag, b in zip(("LRG", "QSO"), blocks)
    ])
    n = z.size
    C = np.zeros((n, n))
    off = 0
    for b in blocks:
        m = b[0].size
        C[off:off + m, off:off + m] = b[3]
        off += m
    C = check_covariance(C, "SDSS DR16 FS+BAO")
    return FSBAOData(z=z, value=value, quantity=quantity, tracer=tracer,
                     cov=C, cho=cho_factor(C, lower=True))
