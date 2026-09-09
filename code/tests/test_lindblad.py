"""Tests for absorb.lindblad.

Three groups:

* *exactness*: the one-unit closed form, trace preservation, and the fact that
  the permutation-symmetric birth chain reproduces the full ``4^N`` Liouvillian;
* *structure*: populations decouple from coherences, so a maximally coherent
  product state and the maximally mixed state absorb identically -- the quantum
  character of the initial state buys nothing here;
* *closure*: the mean-field error decays as ``1/N``, measured first on the full
  Liouvillian (``N = 2..8``) and then, far beyond it, on the birth chain.
"""
from __future__ import annotations

import math

import numpy as np
import pytest

from absorb import lindblad as lb

T_GRID = np.linspace(0.0, 4.0, 81)
ALPHA = 1.0


# ---------------------------------------------------------------------------
# Exactness
# ---------------------------------------------------------------------------
def test_single_unit_closed_form() -> None:
    """One unit: rho_AA(t) = 1 - exp(-Gamma t) exactly."""
    t = np.linspace(0.0, 5.0, 51)
    Gamma0 = 1.7
    run = lb.solve_master(1, t, Gamma0=Gamma0, rtol=1e-13, atol=1e-15)
    exact = lb.single_unit_solution(t, Gamma0)
    assert np.max(np.abs(run.populations[1] - exact)) < 1e-12
    assert np.max(np.abs(run.f - exact)) < 1e-12
    assert np.max(np.abs(run.populations[0] - np.exp(-Gamma0 * t))) < 1e-12


def test_liouvillian_is_trace_preserving() -> None:
    """tr L[rho] = 0 for every rho: the diagonal rows sum to zero column-wise."""
    for N in range(1, 6):
        D = 1 << N
        Lsup = lb.liouvillian(N, 1.0, ALPHA)
        diag_rows = np.arange(D) * D + np.arange(D)
        trace_functional = np.zeros(D * D)
        trace_functional[diag_rows] = 1.0
        assert np.max(np.abs(trace_functional @ Lsup)) < 1e-12


def test_trace_and_positivity_are_preserved_numerically() -> None:
    for N in (2, 4):
        run = lb.solve_master(N, T_GRID, alpha=ALPHA)
        assert np.max(np.abs(run.trace - 1.0)) < 1e-10
        assert np.min(run.populations) > -1e-12
        # occupation numbers are non-decreasing: absorption is irreversible
        assert np.all(np.diff(run.n, axis=1) > -1e-10)
        assert np.all(run.f <= 1.0 + 1e-12)


def test_jump_operator_structure() -> None:
    """L_i maps one basis state to one basis state and L_i^dag L_i is diagonal."""
    N, i = 4, 2
    L = lb.jump_operator(i, N, 1.0, ALPHA)
    dense = L.toarray()
    # exactly one non-zero per non-empty column, and it raises bit i
    for s in range(1 << N):
        col = dense[:, s]
        nz = np.nonzero(col)[0]
        if (s >> i) & 1:
            assert nz.size == 0
        else:
            assert nz.size == 1 and nz[0] == s | (1 << i)
    LdL = (L.T @ L).toarray()
    assert np.count_nonzero(LdL - np.diag(np.diag(LdL))) == 0
    # the rate encodes the environment fraction k/(N-1)
    k = lb.converted_counts(N)
    expected = np.where(
        (np.arange(1 << N) >> i) & 1, 0.0, np.exp(ALPHA * k / (N - 1))
    )
    assert np.allclose(np.diag(LdL), expected)


def test_dicke_chain_reproduces_the_full_liouvillian() -> None:
    """The (N+1)-state birth chain is exact for permutation-symmetric states."""
    for N in range(1, 7):
        full = lb.solve_master(N, T_GRID, alpha=ALPHA)
        red = lb.dicke_master(N, T_GRID, alpha=ALPHA)
        assert np.max(np.abs(full.f - red.f)) < 1e-9, N
        # and the k-resolved distribution matches too
        k = lb.converted_counts(N)
        binned = np.array([full.populations[k == j].sum(axis=0) for j in range(N + 1)])
        assert np.max(np.abs(binned - red.p)) < 1e-9


def test_dicke_conserves_probability() -> None:
    run = lb.dicke_master(200, T_GRID, alpha=ALPHA, method="BDF")
    assert np.max(np.abs(run.p.sum(axis=0) - 1.0)) < 1e-8
    assert np.min(run.p) > -1e-10
    assert np.all(np.diff(run.f) > -1e-12)


# ---------------------------------------------------------------------------
# Structure: populations decouple from coherences
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("N", [1, 2, 3, 4, 5])
def test_populations_decouple_algebraically(N: int) -> None:
    """No matrix element of the Liouvillian sends a coherence to a population."""
    assert lb.populations_decouple(N, alpha=ALPHA) is True


@pytest.mark.parametrize("N", [2, 3, 4, 5])
def test_coherent_and_mixed_initial_states_absorb_identically(N: int) -> None:
    """A maximally coherent product state and the mixed state agree to 1e-10.

    ``((|I> + |A>)/sqrt2)^{tensor N}`` has every coherence at its maximum value
    ``2^-N`` while the maximally mixed state has none, yet the two share the same
    populations.  Since the Liouvillian never feeds a coherence into a
    population, ``<n_i>(t)`` must be the same function of time for both -- the
    absorption dynamics is effectively classical.
    """
    kw = dict(alpha=ALPHA, rtol=1e-12, atol=1e-14)
    coh = lb.solve_master(N, T_GRID, initial="coherent", **kw)
    mix = lb.solve_master(N, T_GRID, initial="mixed", **kw)
    assert coh.coherence[0] > 0.5           # the coherent state really is coherent
    assert mix.coherence[0] < 1e-12         # the mixed state really is not
    assert np.max(np.abs(coh.n - mix.n)) < 1e-10
    assert np.max(np.abs(coh.f - mix.f)) < 1e-10


def test_coherences_only_decay() -> None:
    """The coherences of the product state are damped, never amplified."""
    run = lb.solve_master(3, T_GRID, alpha=ALPHA, initial="coherent")
    assert run.coherence[-1] < run.coherence[0]


# ---------------------------------------------------------------------------
# Mean-field closure
# ---------------------------------------------------------------------------
def test_mean_field_closed_form_without_reinforcement() -> None:
    t = np.linspace(0.0, 5.0, 51)
    f = lb.mean_field(t, Gamma0=0.8, alpha=0.0)
    assert np.allclose(f, 1.0 - np.exp(-0.8 * t), atol=1e-12)


def test_closure_error_is_order_one_over_N_full_liouvillian() -> None:
    """max_t |<fhat> - f_MF| ~ N^-1 across the whole reachable Hilbert space.

    N = 2..8 is a short lever arm and the sub-leading 1/N^2 term is still
    visible, so the fitted exponent is allowed a 0.25 window around -1; the
    ``dicke`` version of the same test below tightens it to 0.05.
    """
    cs = lb.closure_error_scaling(range(2, 9), T_GRID, alpha=ALPHA)
    assert cs.engine == "master"
    assert np.all(np.diff(cs.error) < 0.0)          # monotonically shrinking
    assert abs(cs.slope + 1.0) < 0.25, f"fitted slope {cs.slope:.4f}"
    # N * error must approach a constant
    scaled = cs.error * cs.N
    assert scaled.max() / scaled.min() < 1.5


def test_closure_error_is_order_one_over_N_large_N() -> None:
    """Same measurement on the birth chain, over three decades of N.

    The full Liouvillian stops at N = 8 (a 65536-dimensional ODE); the
    permutation-symmetric reduction reaches N = 4096 in a fraction of the time
    and pins the exponent to -1 within a few per cent.
    """
    Ns = [16, 64, 256, 1024, 4096]
    cs = lb.closure_error_scaling(
        Ns, T_GRID, alpha=ALPHA, engine="dicke", method="BDF"
    )
    assert abs(cs.slope + 1.0) < 0.05, f"fitted slope {cs.slope:.4f}"
    scaled = cs.error * cs.N
    assert scaled.max() / scaled.min() < 1.05
    assert cs.prefactor > 0.0


def test_dicke_variance_is_the_dropped_term() -> None:
    """Var(fhat) ~ 1/N: this is exactly what the mean-field closure throws away."""
    scaled = []
    for N in (64, 256, 1024):
        run = lb.dicke_master(N, T_GRID, alpha=ALPHA, method="BDF")
        scaled.append(np.max(run.var_f) * N)
    assert max(scaled) / min(scaled) < 1.15, scaled


# ---------------------------------------------------------------------------
# Guards
# ---------------------------------------------------------------------------
def test_full_liouvillian_size_guard() -> None:
    with pytest.raises(ValueError):
        lb.solve_master(9, T_GRID)


def test_unknown_initial_state() -> None:
    with pytest.raises(ValueError):
        lb.initial_density_matrix(2, "bogus")     # type: ignore[arg-type]
    with pytest.raises(ValueError):
        lb.solve_master(2, T_GRID, initial=np.eye(3))


def test_single_unit_has_no_environment() -> None:
    """N = 1: the empty average is zero, so the rate is the bare Gamma_0."""
    assert lb.dicke_rates(1, 2.5, 99.0)[0] == pytest.approx(2.5)
    assert lb.jump_operator(0, 1, 2.5, 99.0).toarray()[1, 0] == pytest.approx(
        math.sqrt(2.5)
    )
