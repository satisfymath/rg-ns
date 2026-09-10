"""Integrity checks on the raw data products.

These are deliberately paranoid: a silently mis-parsed covariance or a
reordered BAO vector would bias every result in the paper without producing
any visible failure elsewhere.
"""
from __future__ import annotations

import numpy as np
import pytest

from absorb.data import (
    load_cc,
    load_desi,
    load_pantheon,
    load_planck_priors,
    load_rsd,
)
from absorb.data.cc import _read_hz, _read_mm20
from absorb.data.pantheon import _read_cov, _read_table, n_rows_total


def _assert_valid_covariance(C: np.ndarray, name: str, sym_tol: float = 1e-5) -> None:
    assert C.ndim == 2 and C.shape[0] == C.shape[1], f"{name}: not square"
    scale = np.sqrt(np.outer(np.diag(C), np.diag(C)))
    assert np.max(np.abs(C - C.T) / scale) < sym_tol, f"{name}: not symmetric"
    # positive definiteness, both ways round
    np.linalg.cholesky(C)
    assert np.all(np.linalg.eigvalsh(C) > 0.0), f"{name}: non-positive eigenvalue"


# ---------------------------------------------------------------------------
# Pantheon+
# ---------------------------------------------------------------------------
def test_pantheon_row_counts():
    assert n_rows_total() == 1701
    t = _read_table()
    assert t["zHD"].size == 1701
    assert int((t["IS_CALIBRATOR"] > 0.5).sum()) == 77
    assert int((t["zHD"] > 0.01).sum()) == 1590


def test_pantheon_covariance_shape():
    C = _read_cov()
    assert C.shape == (1701, 1701)


@pytest.mark.parametrize("with_shoes", [False, True])
def test_pantheon_selection_and_covariance(with_shoes):
    d = load_pantheon(with_shoes=with_shoes)
    assert d.n == (1657 if with_shoes else 1590)
    assert d.cov.shape == (d.n, d.n)
    assert d.z_hd.shape == d.z_hel.shape == d.m_b_corr.shape == (d.n,)
    _assert_valid_covariance(d.cov, "Pantheon+")
    # The Cepheid distances are only *used* when the SH0ES anchors are in.
    assert d.use_cepheid.any() == with_shoes
    assert np.all(d.ceph_dist[d.use_cepheid] > 25.0)
    if not with_shoes:
        assert np.all(d.z_hd > 0.01)


def test_pantheon_covariance_matches_selected_rows():
    """The sub-covariance must be the one belonging to the selected rows."""
    d = load_pantheon(with_shoes=False)
    C = _read_cov()
    k = d.index[[0, 5, 100, -1]]
    sub = C[np.ix_(k, k)]
    got = d.cov[np.ix_([0, 5, 100, d.n - 1], [0, 5, 100, d.n - 1])]
    assert np.allclose(got, 0.5 * (sub + sub.T), rtol=0, atol=1e-7)


def test_pantheon_is_cached():
    assert load_pantheon(with_shoes=False) is load_pantheon(with_shoes=False)


# ---------------------------------------------------------------------------
# DESI DR2 BAO
# ---------------------------------------------------------------------------
def test_desi_row_count_and_covariance():
    d = load_desi()
    assert d.n == 13
    assert d.cov.shape == (13, 13)
    _assert_valid_covariance(d.cov, "DESI DR2")


def test_desi_file_order_is_preserved():
    """At z = 2.33 the release lists D_H/r_d *before* D_M/r_d.  The covariance
    follows the file, so any sorting of the data vector would silently pair
    each measurement with the wrong variance."""
    d = load_desi()
    assert d.quantity[0] == "DV_over_rs" and d.z[0] == pytest.approx(0.295)
    assert d.quantity[11] == "DH_over_rs" and d.z[11] == pytest.approx(2.33)
    assert d.quantity[12] == "DM_over_rs" and d.z[12] == pytest.approx(2.33)
    assert d.value[11] == pytest.approx(8.6315, abs=1e-3)
    assert d.value[12] == pytest.approx(38.9890, abs=1e-3)


def test_desi_quantities_are_known():
    d = load_desi()
    assert set(d.quantity) <= {"DV_over_rs", "DM_over_rs", "DH_over_rs"}


# ---------------------------------------------------------------------------
# Cosmic chronometers
# ---------------------------------------------------------------------------
def test_cc_row_counts():
    z, H, err = _read_hz()
    assert z.size == H.size == err.size == 15
    assert _read_mm20()["z"].size == 29


def test_cc_covariance_structure():
    d = load_cc()
    assert d.n == 15
    _assert_valid_covariance(d.cov, "CC")
    # The systematic terms only add: every diagonal element must grow.
    assert np.all(np.diag(d.cov) > d.err_H ** 2)
    # ... and they are correlated, so the matrix is not diagonal.
    off = d.cov - np.diag(np.diag(d.cov))
    assert np.max(np.abs(off)) > 0.0


def test_cc_conservative_variant_is_wider():
    d, dc = load_cc("default"), load_cc("conservative")
    assert np.all(np.diag(dc.cov) > np.diag(d.cov))
    with pytest.raises(ValueError):
        load_cc("nonsense")


def test_cc_systematics_are_clamped_outside_the_table():
    """The MM20 table stops at z = 1.475 but a chronometer sits at z = 1.965."""
    from absorb.data.cc import _sigma_percent

    t = _read_mm20()
    assert _sigma_percent("IMF", np.array([5.0]))[0] == pytest.approx(t["IMF"][-1])
    assert _sigma_percent("IMF", np.array([0.0]))[0] == pytest.approx(t["IMF"][0])


# ---------------------------------------------------------------------------
# RSD / DR16
# ---------------------------------------------------------------------------
def test_rsd_rows_and_block_structure():
    d = load_rsd()
    assert d.n == 12
    assert int((d.tracer == "LRG").sum()) == 9
    assert int((d.tracer == "QSO").sum()) == 3
    _assert_valid_covariance(d.cov, "DR16 FS+BAO")
    # LRG and QSO are disjoint samples: no cross-covariance.
    assert np.all(d.cov[:9, 9:] == 0.0)


def test_rsd_fs8_extraction():
    d = load_rsd()
    i = d.fs8_index
    assert i.tolist() == [2, 5, 8, 11]
    z, v, C = d.fs8_block()
    assert C.shape == (4, 4)
    assert z == pytest.approx([0.38, 0.51, 0.698, 1.48])
    # taking the sub-block, not the diagonal: the two LRG redshifts correlate
    assert C[0, 1] != 0.0
    assert np.allclose(np.diag(C), [d.cov[j, j] for j in i])


# ---------------------------------------------------------------------------
# Planck compressed priors
# ---------------------------------------------------------------------------
def test_planck_priors():
    p = load_planck_priors()
    assert p.n == 3
    assert p.mean == pytest.approx([1.7502, 301.471, 0.02236])
    assert p.sigma == pytest.approx([0.0046, 0.090, 0.00015])
    _assert_valid_covariance(p.cov, "Planck priors")
    assert np.allclose(np.sqrt(np.diag(p.cov)), p.sigma)
    assert p.cov[0, 2] < 0.0            # R and omega_b anti-correlate
