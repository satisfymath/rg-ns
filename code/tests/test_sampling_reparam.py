"""The unbounded reparametrisation must not change what is being sampled.

The sampler was moved into a logit coordinate because ensemble moves in the
bounded coordinate were rejected on the prior alone.  That is a legitimate fix
only if the measure on the original parameters is untouched, so it is tested
directly rather than argued: sample the transformed target with a constant
likelihood and check that the parameters come back uniform on their box.
"""
# covers: app:numerics-sampling
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

from __future__ import annotations

import numpy as np
import pytest
from scipy.stats import kstest

from absorb.sampling import LogitMap

LOW = [0.0, 0.019, -3.0]
HIGH = [1.0, 0.026, 1.0]


@pytest.fixture
def lmap() -> LogitMap:
    return LogitMap(LOW, HIGH)


def test_roundtrip_is_exact(lmap: LogitMap) -> None:
    rng = np.random.default_rng(0)
    x = np.array(LOW) + rng.random((200, 3)) * (np.array(HIGH) - np.array(LOW))
    back = np.array([lmap.to_x(lmap.to_z(xi)) for xi in x])
    assert np.abs(back - x).max() < 1e-12


def test_log_jacobian_matches_finite_differences(lmap: LogitMap) -> None:
    z = np.array([0.7, -2.3, 4.1])
    h = 1e-6
    num = sum(
        np.log(abs((lmap.to_x(z + h * e) - lmap.to_x(z - h * e))[i] / (2 * h)))
        for i, e in enumerate(np.eye(3))
    )
    assert abs(lmap.log_jacobian(z) - num) < 1e-8


def test_log_jacobian_does_not_overflow_in_the_tails(lmap: LogitMap) -> None:
    """At |z| = 700 the naive u(1-u) form underflows to zero and gives -inf."""
    z = np.array([700.0, -700.0, 0.0])
    value = lmap.log_jacobian(z)
    assert np.isfinite(value)
    # log|dx/dz| -> log(width) - |z| for large |z|
    expected = sum(np.log(np.array(HIGH) - np.array(LOW))) - 700.0 - 700.0 - 2 * np.log(2.0)
    assert abs(value - expected) < 1e-9


def test_logit_map_preserves_the_prior(lmap: LogitMap) -> None:
    """A flat likelihood in x must stay flat in x after the change of variables.

    Sampled with random-walk Metropolis in z on the target log|dx/dz|, which is
    what the Jacobian correction contributes when the likelihood is constant.
    """
    rng = np.random.default_rng(12345)
    z = np.zeros(3)
    logp = lmap.log_jacobian(z)
    kept = []
    for i in range(400_000):
        prop = z + 0.6 * rng.standard_normal(3)
        lq = lmap.log_jacobian(prop)
        if np.log(rng.random()) < lq - logp:
            z, logp = prop, lq
        if i > 20_000 and i % 20 == 0:
            kept.append(lmap.to_x(z))
    x = np.array(kept)
    lo, hi = np.array(LOW), np.array(HIGH)
    u = (x - lo) / (hi - lo)
    for j in range(3):
        p = kstest(u[:, j], "uniform").pvalue
        assert p > 0.01, f"parameter {j} is not uniform after the transform (p={p:.3g})"
