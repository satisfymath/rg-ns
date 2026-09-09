"""Pantheon+ / SH0ES type-Ia supernova compilation (Scolnic et al. 2022;
Brout et al. 2022; Riess et al. 2022).

The release provides 1701 light curves of 1550 distinct supernovae together
with a 1701 x 1701 statistical + systematic covariance of the corrected peak
magnitudes ``m_b_corr``.  Two selections are supported:

``with_shoes=False``
    Hubble-flow sample only, z_HD > 0.01.  The absolute magnitude M_B is a
    free nuisance parameter and is marginalised analytically, so this sample
    constrains the *shape* of the distance-redshift relation but not H_0.

``with_shoes=True``
    The same, plus every light curve flagged ``IS_CALIBRATOR``, whose host
    has a Cepheid distance ``CEPH_DIST``.  Those rows carry an external,
    cosmology-independent distance, which breaks the M_B degeneracy and
    therefore does constrain H_0.  This is the standard SH0ES construction:
    the *same* M_B appears in the calibrator and Hubble-flow residuals.

Redshifts: ``zHD`` is the CMB-frame redshift corrected for peculiar
velocities and is the one entering the comoving distance; ``zHEL`` is
heliocentric and supplies the (1 + z) factor of the luminosity distance
(Calcino & Davis 2017).
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from scipy.linalg import cho_factor

from .paths import check_covariance, raw_path

__all__ = ["PantheonData", "load_pantheon"]

_DAT = "PantheonPlusSH0ES.dat"
_COV = "PantheonPlusSH0ES_STATSYS.cov"

#: Hubble-flow cut of Brout et al. (2022): below this redshift peculiar
#: velocities dominate the distance error budget.
Z_MIN_HUBBLE_FLOW = 0.01


@dataclass(frozen=True)
class PantheonData:
    """Selected Pantheon+ sample.

    Attributes
    ----------
    z_hd, z_hel
        CMB-frame (Hubble-diagram) and heliocentric redshifts.
    m_b_corr
        Corrected apparent peak magnitude; m_b_corr = M_B + mu.
    is_calibrator
        Boolean mask of Cepheid-calibrated hosts.
    use_cepheid
        Rows whose residual must be built from ``ceph_dist`` instead of the
        model distance modulus.  Equal to ``is_calibrator`` when
        ``with_shoes`` and all-False otherwise: ten calibrators sit above the
        Hubble-flow cut and are therefore *in* the SN-only sample, but there
        they must be treated as ordinary supernovae, or the external Cepheid
        calibration would leak into a sample that is meant to be free of it.
    ceph_dist
        Cepheid distance modulus of the host (only meaningful where
        ``is_calibrator``; -9 elsewhere in the release, left untouched).
    cov
        Covariance of ``m_b_corr`` restricted to the selected rows.
    cho
        Cached Cholesky factorisation of ``cov`` for :func:`scipy.linalg.cho_solve`.
    index
        Indices of the selected rows in the original 1701-row table.
    with_shoes
        Whether Cepheid calibrators were included.
    """

    z_hd: np.ndarray
    z_hel: np.ndarray
    m_b_corr: np.ndarray
    is_calibrator: np.ndarray
    use_cepheid: np.ndarray
    ceph_dist: np.ndarray
    cov: np.ndarray
    cho: tuple[np.ndarray, bool]
    index: np.ndarray
    with_shoes: bool

    @property
    def n(self) -> int:
        return self.z_hd.size

    def __repr__(self) -> str:                                # pragma: no cover
        return (f"PantheonData(n={self.n}, with_shoes={self.with_shoes}, "
                f"n_calibrators={int(self.is_calibrator.sum())})")


@lru_cache(maxsize=1)
def _read_table() -> dict[str, np.ndarray]:
    """Parse the whitespace table; returns one float array per needed column."""
    path = raw_path(_DAT)
    with path.open() as fh:
        header = fh.readline().split()
    wanted = ["zHD", "zHEL", "m_b_corr", "m_b_corr_err_DIAG",
              "CEPH_DIST", "IS_CALIBRATOR", "USED_IN_SH0ES_HF"]
    cols = {name: header.index(name) for name in wanted}
    raw = np.loadtxt(path, skiprows=1, usecols=tuple(cols.values()))
    return {name: raw[:, i] for i, name in enumerate(cols)}


@lru_cache(maxsize=1)
def _read_cov() -> np.ndarray:
    """Parse the covariance: first token is the dimension, then n^2 entries
    row-major, one per line."""
    path = raw_path(_COV)
    with path.open() as fh:
        n = int(fh.readline())
        C = np.fromstring(fh.read(), sep=" ")
    if C.size != n * n:
        raise ValueError(f"{path}: expected {n * n} entries, found {C.size}")
    return C.reshape(n, n)


@lru_cache(maxsize=2)
def load_pantheon(with_shoes: bool = False) -> PantheonData:
    """Load and cache the Pantheon+ sample (see the module docstring)."""
    t = _read_table()
    calib = t["IS_CALIBRATOR"] > 0.5
    sel = t["zHD"] > Z_MIN_HUBBLE_FLOW
    if with_shoes:
        # Cepheid hosts are nearby, so most of them fall below the cut; they
        # are added back because their external distance is what anchors M_B.
        sel = sel | calib
    idx = np.flatnonzero(sel)

    C = _read_cov()
    if C.shape[0] != t["zHD"].size:
        raise ValueError("Pantheon+: covariance and table have different lengths")
    C = check_covariance(C[np.ix_(idx, idx)], "Pantheon+")

    return PantheonData(
        z_hd=t["zHD"][idx].copy(),
        z_hel=t["zHEL"][idx].copy(),
        m_b_corr=t["m_b_corr"][idx].copy(),
        is_calibrator=calib[idx].copy(),
        use_cepheid=(calib[idx] & bool(with_shoes)),
        ceph_dist=t["CEPH_DIST"][idx].copy(),
        cov=C,
        cho=cho_factor(C, lower=True),
        index=idx,
        with_shoes=with_shoes,
    )


def n_rows_total() -> int:
    """Number of light curves in the release, before any cut (1701)."""
    return int(_read_table()["zHD"].size)
