"""Location of the raw data files and small shared parsing helpers."""
from __future__ import annotations

import os
from pathlib import Path

import numpy as np

#: ``<repo>/data/raw``.  This file is ``<repo>/code/absorb/data/paths.py``,
#: hence three levels up.  Overridable with ``ABSORB_DATA_DIR`` so that the
#: package can be installed elsewhere or pointed at a mirror.
RAW_DIR = Path(
    os.environ.get("ABSORB_DATA_DIR", Path(__file__).resolve().parents[3] / "data" / "raw")
)


def raw_path(name: str) -> Path:
    """Absolute path of a raw data file, with an explicit error if missing."""
    p = RAW_DIR / name
    if not p.exists():
        raise FileNotFoundError(
            f"missing raw data file {p}.  Set ABSORB_DATA_DIR or re-run the "
            f"download script."
        )
    return p


def check_covariance(C: np.ndarray, name: str, sym_tol: float = 1e-8) -> np.ndarray:
    """Validate a covariance matrix and return it symmetrised.

    Raises if it is not square, not symmetric to ``sym_tol`` (relative to its
    diagonal), or not positive definite.  Symmetrising afterwards removes the
    last-bit asymmetry of the published ASCII files, which would otherwise
    make ``cholesky`` non-deterministic.
    """
    C = np.asarray(C, dtype=float)
    if C.ndim != 2 or C.shape[0] != C.shape[1]:
        raise ValueError(f"{name}: covariance is not square, shape {C.shape}")
    scale = np.sqrt(np.outer(np.diag(C), np.diag(C)))
    if np.max(np.abs(C - C.T) / scale) > sym_tol:
        raise ValueError(f"{name}: covariance is not symmetric")
    C = 0.5 * (C + C.T)
    try:
        np.linalg.cholesky(C)          # cheapest exact test of positive definiteness
    except np.linalg.LinAlgError as exc:
        raise ValueError(f"{name}: covariance is not positive definite") from exc
    return C
