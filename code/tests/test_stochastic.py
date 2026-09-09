"""Tests for absorb.stochastic.

The suite pins down four independent things:

* that the exact samplers reproduce the mean-field limit (law of large numbers)
  with the right ``1/sqrt(N)`` fluctuations;
* that the two *algorithmically unrelated* exact samplers -- thinning and
  inversion of the integrated intensity -- realise the same law;
* that absorption times obey the exact memoryless benchmark;
* and, above all, that **memory is physical**: two histories carrying the same
  converted fraction but different memories have measurably different futures
  (`test_hysteresis_*`).  That last group is the paper's headline claim and is
  written to be as sharp as the solver allows.

All randomness is seeded from ``absorb.constants.SEED``, so every number below
is reproducible.
"""
from __future__ import annotations

import math

import numpy as np
import pytest
from scipy.integrate import quad
from scipy.stats import ks_2samp

from absorb import stochastic as st
from absorb.constants import SEED

# Reference kinetics used by the convergence tests: moderate instantaneous and
# delayed reinforcement, memory time comparable to the conversion time.
REF = st.Kinetics(Gamma0=1.0, alpha=1.5, beta=1.0, tau_M=0.7)


# ---------------------------------------------------------------------------
# Law of large numbers
# ---------------------------------------------------------------------------
def test_law_of_large_numbers() -> None:
    """At N = 1000 the ensemble mean tracks the mean-field ODE.

    Sample times are chosen inside the bulk of the transition (f from 0.16 to
    0.83); the residual O(1/N) closure bias is then well below the Monte-Carlo
    standard error of R = 2000 realizations.
    """
    t = np.array([0.15, 0.30, 0.45, 0.60, 0.75])
    ens = st.simulate_thinning(1000, t, REF, R=2000, seed=SEED)
    det = st.deterministic(t, REF)
    z = (ens.mean_f - det.f) / ens.sem_f
    assert np.all(np.abs(z) < 4.0), f"deviations in sigma: {z}"
    # the memory variable follows too
    assert np.allclose(ens.M.mean(axis=0), det.M, atol=5e-3)


def test_finite_size_bias_is_order_one_over_N() -> None:
    """The residual N-dependence of the mean is O(1/N), not O(1/sqrt(N))."""
    t = np.array([0.3, 0.5, 0.7])
    det = st.deterministic(t, REF)
    scaled = []
    for N in (500, 2000, 8000):
        ens = st.simulate_thinning(N, t, REF, R=1500, seed=SEED)
        scaled.append(np.abs(ens.mean_f - det.f) * N)
    scaled = np.asarray(scaled)
    # N * bias must stay bounded (an O(1/sqrt(N)) bias would grow like sqrt(N),
    # i.e. by a factor of 4 across this range)
    assert scaled.max() < 12.0, scaled


def test_fluctuation_scaling() -> None:
    """sqrt(N) * std(f_N) is N-independent: the fluctuations are O(1/sqrt(N))."""
    t = np.array([0.3, 0.5, 0.7])
    scaled = np.array(
        [
            math.sqrt(N) * st.simulate_thinning(N, t, REF, R=1000, seed=SEED).std_f
            for N in (100, 1000, 10000)
        ]
    )
    spread = scaled.max(axis=0) / scaled.min(axis=0) - 1.0
    assert np.all(spread < 0.15), f"relative spread per time: {spread}"


# ---------------------------------------------------------------------------
# The two exact samplers realise the same law
# ---------------------------------------------------------------------------
def test_samplers_are_statistically_indistinguishable() -> None:
    """Two-sample KS test between thinning and inversion output.

    The samplers share no code path beyond the bookkeeping driver: one accepts
    or rejects proposals from a dominating Poisson process, the other inverts
    the exponential-integral form of the compensator.  Agreement of the full
    distribution of f (not just its mean) at three times is therefore a strong
    check that both are exact.
    """
    p = st.Kinetics(Gamma0=1.0, alpha=1.5, beta=1.2, tau_M=0.6)
    t = np.array([0.3, 0.55, 0.85])
    R = 1600
    a = st.simulate_thinning(64, t, p, R=R, seed=SEED)
    b = st.simulate_inversion(64, t, p, R=R, seed=SEED + 1)
    for i, ti in enumerate(t):
        res = ks_2samp(a.f[:, i], b.f[:, i], method="asymp")
        assert res.pvalue > 0.01, f"t = {ti}: KS p = {res.pvalue:.4f}"


def test_samplers_agree_without_memory_feedback() -> None:
    """With beta = 0 both samplers reduce to the same closed-form exponential."""
    p = st.Kinetics(Gamma0=1.3, alpha=1.0, beta=0.0, tau_M=0.5)
    t = np.array([0.2, 0.5, 1.0])
    a = st.simulate_thinning(50, t, p, R=1200, seed=SEED)
    b = st.simulate_inversion(50, t, p, R=1200, seed=SEED)
    # identical seeds and identical (constant) waiting-time law => identical paths
    assert np.array_equal(a.f, b.f)


def test_integrated_intensity_matches_quadrature() -> None:
    """The Ei form of Lambda(tau) equals a direct numerical integral."""
    A, tau_M = 2.7, 0.8
    for z in (-1.3, -0.2, 0.4, 2.1):
        for tau in (0.05, 0.4, 2.0):
            lam = lambda s: A * math.exp(z * math.exp(-s / tau_M))
            ref, _ = quad(lam, 0.0, tau, epsabs=1e-13, epsrel=1e-13)
            got = st.integrated_intensity(tau, A, z, tau_M)
            assert got == pytest.approx(ref, rel=1e-9)


def test_inversion_root_is_exact() -> None:
    """_invert_one really solves Lambda(tau) = target."""
    A, tau_M = 3.1, 0.45
    for z in (-2.0, -0.05, 0.05, 1.7):
        for target in (0.01, 0.3, 5.0):
            tau = st._invert_one(A, z, tau_M, target)
            assert st.integrated_intensity(tau, A, z, tau_M) == pytest.approx(
                target, rel=1e-10
            )


def test_thinning_bound_dominates_the_intensity() -> None:
    """lambda_max = (N-k) Gamma0 exp(alpha f + beta max(M_k, f)) is a true bound."""
    p = st.Kinetics(Gamma0=1.0, alpha=2.0, beta=1.5, tau_M=0.4)
    N, k = 40, 11
    f = k / N
    s = np.linspace(0.0, 50.0 * p.tau_M, 2001)
    for M_k in (0.0, 0.2, f, 0.9):
        lam_max = (N - k) * p.Gamma0 * math.exp(p.alpha * f + p.beta * max(M_k, f))
        M = f + (M_k - f) * np.exp(-s / p.tau_M)
        lam = (N - k) * p.rate(f, M)
        assert np.all(lam <= lam_max * (1.0 + 1e-12))


# ---------------------------------------------------------------------------
# Absorption times
# ---------------------------------------------------------------------------
def _harmonic(n: int) -> float:
    return float(sum(1.0 / j for j in range(1, n + 1)))


def test_mean_absorption_time_constant_rate() -> None:
    """Memoryless constant rate: E[T_N] = (1/Gamma0) sum_{j=1}^N 1/j exactly.

    With alpha = beta = 0 the k-th waiting time is Exp((N-k) Gamma0), so
    T_N is a sum of independent exponentials and both its mean and its variance
    are known in closed form.  The bound E[T_N] <= H_N/Gamma0 of the draft is
    saturated here, so the test checks the two-sided statement.
    """
    N, Gamma0, R = 50, 1.3, 4000
    p = st.Kinetics(Gamma0=Gamma0, alpha=0.0, beta=0.0)
    ens = st.simulate_thinning(
        N, np.array([0.0]), p, R=R, seed=SEED, until_absorption=True
    )
    T = ens.t_absorb
    assert np.all(np.isfinite(T))
    bound = _harmonic(N) / Gamma0
    sem = T.std(ddof=1) / math.sqrt(R)
    assert abs(T.mean() - bound) < 4.0 * sem
    assert T.mean() <= bound + 4.0 * sem            # the bound itself
    var_exact = sum(1.0 / (j * Gamma0) ** 2 for j in range(1, N + 1))
    assert T.var(ddof=1) == pytest.approx(var_exact, rel=0.1)


@pytest.mark.parametrize("alpha", [1.0, 2.0])
def test_reinforcement_strictly_beats_the_bound(alpha: float) -> None:
    """Self-reinforcement (alpha > 0) makes absorption strictly faster."""
    N, Gamma0, R = 50, 1.3, 2000
    p = st.Kinetics(Gamma0=Gamma0, alpha=alpha, beta=0.0)
    ens = st.simulate_thinning(
        N, np.array([0.0]), p, R=R, seed=SEED, until_absorption=True
    )
    T = ens.t_absorb
    sem = T.std(ddof=1) / math.sqrt(R)
    bound = _harmonic(N) / Gamma0
    assert T.mean() + 4.0 * sem < bound


def test_jump_times_are_recorded_consistently() -> None:
    """Recorded jump times are increasing, N of them, and reproduce f(t)."""
    p = st.Kinetics(Gamma0=1.0, alpha=1.0, beta=0.5, tau_M=0.5)
    t = np.linspace(0.0, 4.0, 9)
    ens = st.simulate_thinning(
        20, t, p, R=5, seed=SEED, until_absorption=True, store_jump_times=True
    )
    assert ens.jump_times is not None
    for r, jt in enumerate(ens.jump_times):
        assert jt.size == 20
        assert np.all(np.diff(jt) > 0.0)
        assert jt[-1] == pytest.approx(ens.t_absorb[r])
        expected = np.searchsorted(jt, t, side="right") / 20.0
        assert np.allclose(ens.f[r], expected)


# ---------------------------------------------------------------------------
# Deterministic limit: closed forms
# ---------------------------------------------------------------------------
def test_deterministic_matches_closed_form_without_reinforcement() -> None:
    """alpha = beta = 0 gives f = 1 - (1-f0) e^{-Gamma0 t} and an exact M."""
    p = st.Kinetics(Gamma0=0.7, alpha=0.0, beta=0.0, tau_M=1.9)
    t = np.linspace(0.0, 6.0, 61)
    sol = st.deterministic(t, p, f0=0.1, M0=0.4)
    f_exact = 1.0 - 0.9 * np.exp(-p.Gamma0 * t)
    assert np.allclose(sol.f, f_exact, atol=1e-11)
    # tau_M M' = f - M with the above f is linear and solvable in closed form
    g, tm = p.Gamma0, p.tau_M
    M_exact = (
        1.0
        + (0.4 - 1.0 + 0.9 / (1.0 - g * tm)) * np.exp(-t / tm)
        - 0.9 / (1.0 - g * tm) * np.exp(-g * t)
    )
    assert np.allclose(sol.M, M_exact, atol=1e-10)


# ---------------------------------------------------------------------------
# HYSTERESIS -- the point of the paper
# ---------------------------------------------------------------------------
def test_hysteresis_preparation_is_clean() -> None:
    """The two histories really do meet at the same density with different memory.

    This is the precondition for everything else: if the checkpoint densities
    differed, any later difference could be blamed on f rather than on M.
    """
    h = st.hysteresis_experiment()
    assert abs(h.prep["checkpoint_mismatch"]) < 1e-10, "checkpoint densities differ"
    assert 0.0 < h.f_checkpoint < 1.0
    assert abs(h.delta_M) > 1e-2, "the two prepared memories are too close to differ"
    assert h.prep["pulse_amplitude"] > 0.0
    assert h.prep["f_start_B"] < h.prep["f_start_A"]


def test_hysteresis_memory_changes_the_future() -> None:
    """beta > 0: identical densities, different memories, different futures.

    Both histories are integrated forward from the checkpoint with *identical*
    parameters and no external driving, so the only thing that distinguishes
    them is M.  The effect is reported three ways:

    * an absolute difference in the converted fraction at t_final;
    * the ratio of the surviving unconverted fractions, which is the sharp
      statement (both f's approach 1, so the remainder is what carries the
      signal);
    * the difference in V = int a^-3 df, the observable the cosmological model
      actually cares about.
    """
    h = st.hysteresis_experiment()
    solver_noise = 1e-9

    assert abs(h.delta_f_final) > 1e-3, h.delta_f_final
    assert abs(h.delta_f_final) > 1e6 * solver_noise
    # the history that arrived with the *larger* memory keeps converting faster
    assert (h.M_A > h.M_B) == (h.f_final_A > h.f_final_B)
    # sharp form: the leftovers differ by a large factor
    assert h.residual_ratio > 2.0, h.residual_ratio
    assert abs(h.relative_delta_V) > 1e-3, h.relative_delta_V


def test_hysteresis_control_beta_zero() -> None:
    """beta = 0: the memory cannot act, and the two futures coincide exactly.

    The control uses the *same* preparation machinery, so it also proves the
    effect above is not an artefact of how history B is built.
    """
    p = st.Kinetics(Gamma0=0.15, alpha=2.0, beta=0.0, tau_M=12.0)
    h = st.hysteresis_experiment(p)
    assert abs(h.delta_M) > 1e-2          # the memories still differ ...
    assert abs(h.delta_f_final) < 1e-9    # ... but nothing downstream notices
    assert abs(h.delta_V) < 1e-9
    assert np.max(np.abs(h.f_A - h.f_B)) < 1e-9


def test_hysteresis_asymptotic_invariant_in_an_expanding_background() -> None:
    """With a(t) growing, V = int a^-3 df converges and still separates them.

    Run long enough that *both* histories have converted essentially everything
    (f -> 1 to machine precision, so the converted fraction no longer
    distinguishes them at all), yet the vacuum increment they deposited differs
    by several per cent -- a permanent, asymptotic record of their different
    memories.
    """
    a = lambda t: (1.0 + t / 3.0) ** (2.0 / 3.0)
    h = st.hysteresis_experiment(a=a, t_final=400.0)
    assert h.f_final_A == pytest.approx(1.0, abs=1e-9)
    assert h.f_final_B == pytest.approx(1.0, abs=1e-9)
    assert abs(h.relative_delta_V) > 1e-2, h.relative_delta_V
    # and the control still collapses
    p0 = st.Kinetics(Gamma0=0.15, alpha=2.0, beta=0.0, tau_M=12.0)
    h0 = st.hysteresis_experiment(p0, a=a, t_final=400.0)
    assert abs(h0.relative_delta_V) < 1e-9


def test_hysteresis_effect_grows_with_beta() -> None:
    """The separation is controlled by beta, as the mechanism requires."""
    prev = -1.0
    for beta in (0.0, 1.0, 2.0, 4.0):
        h = st.hysteresis_experiment(st.Kinetics(0.15, 2.0, beta, 12.0))
        assert abs(h.delta_f_final) > prev
        prev = abs(h.delta_f_final)


def test_hysteresis_rejects_bad_windows() -> None:
    with pytest.raises(ValueError):
        st.hysteresis_experiment(t_prepare=1.0, t_final=0.5)
    with pytest.raises(ValueError):
        st.hysteresis_experiment(pulse_end=5.0, t_prepare=1.0)
    with pytest.raises(ValueError):
        st.hysteresis_experiment(f_start_ratio=1.5)


# ---------------------------------------------------------------------------
# Sensitivity / tangent flow
# ---------------------------------------------------------------------------
@pytest.mark.parametrize(
    "p, f0",
    [
        (st.Kinetics(1.0, 2.0, 0.0, 0.7), 0.1),
        (st.Kinetics(0.5, 3.0, 0.0, 2.0), 0.05),
        (st.Kinetics(2.0, 0.0, 0.0, 1.0), 0.2),
        (st.Kinetics(1.0, -1.5, 0.0, 0.5), 0.3),
    ],
)
def test_sensitivity_matches_closed_form(p: st.Kinetics, f0: float) -> None:
    """For beta = 0, J(t) = F(f(t))/F(f_i) with F(f) = (1-f) Gamma(f)."""
    t = np.linspace(0.0, 3.0, 61)
    s = st.sensitivity(t, p, f0=f0)
    assert s.J_closed_form is not None
    assert s.max_abs_error < 1e-6
    assert s.J[0] == pytest.approx(1.0, abs=1e-12)


def test_sensitivity_matches_finite_differences_with_memory() -> None:
    """With beta > 0 there is no closed form; check against finite differences."""
    p = st.Kinetics(1.0, 2.0, 1.5, 0.7)
    t = np.linspace(0.0, 3.0, 31)
    f0, h = 0.1, 1e-6
    base = st.deterministic(t, p, f0=f0, M0=f0)
    bumped = st.deterministic(t, p, f0=f0 + h, M0=f0)
    fd = (bumped.f - base.f) / h
    s = st.sensitivity(t, p, f0=f0, M0=f0)
    assert np.max(np.abs(fd - s.J)) < 1e-5


def test_sensitivity_no_closed_form_when_memory_feeds_back() -> None:
    s = st.sensitivity(np.linspace(0, 1, 5), st.Kinetics(1.0, 1.0, 1.0, 1.0))
    assert s.J_closed_form is None
    assert math.isnan(s.max_abs_error)


# ---------------------------------------------------------------------------
# Phase portrait / acceleration criterion
# ---------------------------------------------------------------------------
def test_phase_portrait_fields() -> None:
    p = st.Kinetics(1.0, 3.0, 2.0, 0.5)
    d = st.phase_portrait_data(p, n_f=21, n_M=21)
    assert d["f"].shape == d["M"].shape == (21, 21)
    # the vector field must agree with the mean-field equations
    assert np.allclose(d["dfdt"], (1.0 - d["f"]) * p.rate(d["f"], d["M"]))
    assert np.allclose(d["dMdt"], (d["f"] - d["M"]) / p.tau_M)
    # accel is d/dt log Gamma - Gamma along the flow
    assert np.allclose(
        d["accel"],
        p.alpha * d["dfdt"] + p.beta * d["dMdt"] - d["gamma"],
    )
    assert np.array_equal(d["accelerating"], d["accel"] > 0.0)


def test_acceleration_boundary_is_a_zero_level_set() -> None:
    p = st.Kinetics(1.0, 3.0, 2.0, 0.5)
    d = st.phase_portrait_data(p)
    ok = np.isfinite(d["boundary_M"])
    assert ok.any()
    vals = st.acceleration_functional(d["boundary_f"][ok], d["boundary_M"][ok], p)
    assert np.max(np.abs(vals)) < 1e-9


def test_acceleration_boundary_memoryless() -> None:
    """For beta = 0 the criterion is alpha (1-f) > 1, independent of M."""
    p = st.Kinetics(1.0, 3.0, 0.0, 0.5)
    d = st.phase_portrait_data(p)
    assert np.allclose(d["boundary_f"], 1.0 - 1.0 / p.alpha)
    assert np.array_equal(d["accelerating"], p.alpha * (1.0 - d["f"]) > 1.0)


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------
def test_kinetics_validation() -> None:
    with pytest.raises(ValueError):
        st.Kinetics(Gamma0=0.0)
    with pytest.raises(ValueError):
        st.Kinetics(tau_M=-1.0)


@pytest.mark.parametrize("sampler", [st.simulate_thinning, st.simulate_inversion])
def test_simulation_input_validation(sampler) -> None:
    t = np.linspace(0.0, 1.0, 5)
    with pytest.raises(ValueError):
        sampler(0, t)
    with pytest.raises(ValueError):
        sampler(10, t, R=0)
    with pytest.raises(ValueError):
        sampler(10, np.array([1.0, 0.0]))
    with pytest.raises(ValueError):
        sampler(10, np.array([-1.0, 0.0]))
    with pytest.raises(ValueError):
        sampler(10, t, f0=0.05)          # not a multiple of 1/10


def test_absorbed_realizations_stay_absorbed() -> None:
    """After absorption f stays at 1 and M relaxes towards 1."""
    p = st.Kinetics(Gamma0=4.0, alpha=1.0, beta=1.0, tau_M=2.0)
    t = np.linspace(0.0, 12.0, 25)
    ens = st.simulate_thinning(12, t, p, R=50, seed=SEED, until_absorption=True)
    assert np.all(np.isfinite(ens.t_absorb))
    for r in range(ens.R):
        after = t >= ens.t_absorb[r]
        assert np.all(ens.f[r, after] == 1.0)
        assert np.all(np.diff(ens.M[r, after]) >= -1e-12)
        assert ens.M[r, -1] < 1.0
    assert np.all(ens.f <= 1.0) and np.all(ens.f >= 0.0)
