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
# covers: thm:deterministic-limit, prop:memory-origin, eq:process-memory, thm:hysteresis, rem:hysteresis-prescribed, prop:survival, eq:process-survival
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

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


def test_the_finite_size_bias_is_not_order_one_over_sqrt_N() -> None:
    """What this can establish, and what it cannot.

    The test used to be called ``..._is_order_one_over_N`` and asserted that
    ``N * bias`` stays below 12. It cannot support that name. At the largest
    ``N`` the measured ``N * bias`` is of the same size as its own Monte-Carlo
    error, so the data are equally consistent with a bias of exactly zero, and
    a bound of 12 on a quantity whose value is about 2 is not a measurement of
    anything.

    What the same numbers do establish is the alternative that matters: a bias
    of order ``1/sqrt(N)`` would make ``N * bias`` grow by a factor of four
    across this range of ``N``, and it does not grow beyond the Monte-Carlo
    error. That is asserted here, against an error estimated from the ensemble
    rather than assumed.
    """
    t = np.array([0.3, 0.5, 0.7])
    det = st.deterministic(t, REF)
    n_values, R = (500, 2000, 8000), 20000

    scaled, errors = [], []
    for N in n_values:
        ens = st.simulate_thinning(N, t, REF, R=R, seed=SEED)
        scaled.append(np.abs(ens.mean_f - det.f) * N)
        errors.append(N * ens.std_f / np.sqrt(R))
    scaled, errors = np.asarray(scaled), np.asarray(errors)

    # Test at the epoch where the bias is largest at the smallest N, because
    # that is the only one with enough signal to separate the two laws; at the
    # others the bias is small enough that a factor of four is inside the
    # Monte-Carlo error and nothing can be concluded, which is itself the
    # point of the rewrite.
    k = int(np.argmax(scaled[0]))
    predicted_if_sqrt = 4.0 * scaled[0, k]     # sqrt(8000/500) = 4
    gap = (predicted_if_sqrt - scaled[-1, k]) / errors[-1, k]
    assert gap > 3.0, (scaled[:, k], errors[:, k], gap)

    # and the honest statement of what is not established: at the largest N the
    # signal is within its own error, so this cannot separate O(1/N) from zero
    assert scaled[-1, k] < 2.0 * errors[-1, k], (scaled[-1, k], errors[-1, k])


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
    """With beta = 0 the intensity is piecewise constant; both samplers still agree.

    (The two draw different numbers of uniforms per jump -- thinning needs an
    acceptance variate -- so the *paths* differ even at equal seeds; only the
    laws must coincide.)
    """
    p = st.Kinetics(Gamma0=1.3, alpha=1.0, beta=0.0, tau_M=0.5)
    t = np.array([0.2, 0.5, 1.0])
    a = st.simulate_thinning(50, t, p, R=1500, seed=SEED)
    b = st.simulate_inversion(50, t, p, R=1500, seed=SEED + 1)
    for i in range(t.size):
        assert ks_2samp(a.f[:, i], b.f[:, i], method="asymp").pvalue > 0.01


def test_independent_units_are_binomial() -> None:
    """alpha = beta = 0: the units are independent, so k(t) ~ Binomial(N, q).

    This is the one case with a fully closed-form law, and it pins the absolute
    normalisation of both samplers rather than just their mutual agreement.
    """
    N, Gamma0, R = 40, 0.9, 4000
    p = st.Kinetics(Gamma0=Gamma0, alpha=0.0, beta=0.0)
    t = np.array([0.3, 0.8, 1.6])
    q = 1.0 - np.exp(-Gamma0 * t)
    rng = np.random.default_rng(SEED + 7)
    for sampler in (st.simulate_thinning, st.simulate_inversion):
        ens = sampler(N, t, p, R=R, seed=SEED)
        sem = np.sqrt(q * (1.0 - q) / N / R)
        assert np.all(np.abs(ens.mean_f - q) < 4.0 * sem)
        assert np.allclose(ens.f.var(axis=0), q * (1.0 - q) / N, rtol=0.12)
        for i in range(t.size):
            ref = rng.binomial(N, q[i], size=R) / N
            assert ks_2samp(ens.f[:, i], ref, method="asymp").pvalue > 0.01


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
    """The separation is controlled by beta, as the mechanism requires.

    The absolute gap ``|f_A - f_B|`` is not monotone in beta -- at large beta
    both histories run away and saturate, squeezing the gap -- but the ratio of
    surviving unconverted fractions is, and that is the scale-free statement.
    """
    ratios = [
        st.hysteresis_experiment(st.Kinetics(0.15, 2.0, beta, 12.0)).residual_ratio
        for beta in (0.0, 0.5, 1.0, 2.0, 3.0, 4.0)
    ]
    assert ratios[0] == pytest.approx(1.0, abs=1e-8)
    assert np.all(np.diff(ratios) > 0.0), ratios
    assert ratios[-1] > 3.0


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


def test_the_survival_identity_holds_for_a_state_dependent_rate():
    """``prop:survival``: 1 - f = (1 - f_i) exp(-int Gamma), Gamma along the path.

    The identity is the integrating factor of ``f' = (1 - f) Gamma`` and so
    holds for any locally integrable rate, including one that depends on the
    state it is driving. That last clause is the part worth checking: the rate
    used here is ``Gamma_0 exp(alpha f + beta M)`` with a relaxing memory, so
    it is neither prescribed in advance nor monotone in time, and the integral
    in the exponent is of the realized rate rather than of a given function.

    The integral is accumulated as a state variable of the same solver, so
    that the comparison is not between an ODE solution and a separate
    quadrature with its own error.
    """
    from scipy.integrate import solve_ivp

    g0, alpha, beta, tau = 0.7, 3.0, 2.0, 0.35
    f_i = 0.05

    def rhs(t, y):
        f, M, S = y                       # S = int_0^t Gamma ds
        rate = g0 * np.exp(alpha * f + beta * M) * (1.0 + 0.5 * np.sin(3.0 * t))
        return [(1.0 - f) * rate, (f - M) / tau, rate]

    sol = solve_ivp(rhs, (0.0, 6.0), [f_i, 0.0, 0.0], rtol=1e-12, atol=1e-14,
                    dense_output=True)
    assert sol.success

    t = np.linspace(0.0, 6.0, 400)
    f, _, S = sol.sol(t)
    residual = np.abs((1.0 - f) - (1.0 - f_i) * np.exp(-S))
    assert residual.max() < 1e-10, residual.max()

    # the test would be vacuous if nothing happened: the rate must vary and
    # the conversion must actually run to near completion
    assert f[-1] > 0.99 and f[0] == pytest.approx(f_i)
    assert S[-1] > 5.0


def test_a_flat_background_cannot_exhibit_hysteresis_in_the_vacuum():
    """Why the demonstration needs an expanding background, asserted not claimed.

    With ``a = 1`` the vacuum increment is ``dV = (1-f) Gamma dt = df``, so
    ``V`` is the converted fraction up to a constant and any difference in
    ``V`` between two histories equals their difference in ``f`` exactly. A
    run on a flat background therefore *cannot* show what
    ``thm:hysteresis`` says -- histories that agree in the converted fraction
    and differ in the accumulated vacuum -- and the manuscript described such a
    run in those terms for a while, quoting one difference for both.

    The two assertions below are the whole argument: degenerate when flat, not
    degenerate when expanding, with both histories run to completion so that
    the fractions genuinely agree rather than merely being close.
    """
    from absorb import stochastic as st

    flat = st.hysteresis_experiment()
    assert abs(flat.delta_V - flat.delta_f_final) < 1e-9 * max(
        abs(flat.delta_V), 1e-30), (
        f"on a flat background dV should equal df exactly; got "
        f"{flat.delta_V:.6e} and {flat.delta_f_final:.6e}")

    grown = st.hysteresis_experiment(a=lambda t: (1.0 + t) ** (2.0 / 3.0),
                                     t_final=20.0)
    # both histories have run to completion: the fractions agree to solver
    # tolerance, so nothing about the kinetics distinguishes their endpoints
    assert abs(grown.delta_f_final) < 1e-9, grown.delta_f_final
    assert abs(1.0 - grown.f_final_A) < 1e-9
    assert abs(1.0 - grown.f_final_B) < 1e-9
    # and the accumulated vacua nonetheless differ, by far more than that
    assert grown.relative_delta_V > 0.05, grown.relative_delta_V
    assert abs(grown.delta_V) > 1e6 * abs(grown.delta_f_final)


def test_the_memory_law_is_the_exact_average_of_per_unit_relaxations():
    """``prop:memory-origin`` and ``eq:process-memory``, with stochastic input.

    The claim is that the population law tau dM/dt = f - M is not an extra
    non-local assumption but the exact average of per-unit laws
    tau dm_i/dt = s_i - m_i with a *common* tau, where s_i is the indicator
    that unit i has converted. It is exact by linearity, which is the point:
    the assumption it replaces is local and of equal or greater strength, not
    weaker.

    This was among the claims whose coverage the ledger asserted and no test
    supplied. The check drives the per-unit equations with conversion times
    drawn at random rather than with a smooth prescribed f, so that the two
    sides are compared on a realization and not on the idealisation the
    proposition is stated over.
    """
    from scipy.integrate import solve_ivp

    rng = np.random.default_rng(11)
    n_units, tau = 400, 0.7
    t_conv = np.sort(rng.exponential(1.0, size=n_units))   # conversion times
    t_end = float(t_conv.max()) + 3.0 * tau

    def f_of(t):
        """Realized converted fraction: a staircase with n_units steps."""
        return float(np.searchsorted(t_conv, t, side="right")) / n_units

    # per-unit: tau m_i' = s_i - m_i, integrated for every unit at once
    def per_unit(t, m):
        s = (t >= t_conv).astype(float)
        return (s - m) / tau

    sol_units = solve_ivp(per_unit, (0.0, t_end), np.zeros(n_units),
                          rtol=1e-11, atol=1e-13, dense_output=True,
                          max_step=0.01)
    assert sol_units.success

    # population: tau M' = f - M, driven by the same realization
    def population(t, y):
        return [(f_of(t) - y[0]) / tau]

    sol_pop = solve_ivp(population, (0.0, t_end), [0.0], rtol=1e-11,
                        atol=1e-13, dense_output=True, max_step=0.01)
    assert sol_pop.success

    t = np.linspace(0.0, t_end, 500)
    mean_of_units = sol_units.sol(t).mean(axis=0)
    population_M = sol_pop.sol(t)[0]
    assert np.max(np.abs(mean_of_units - population_M)) < 1e-6, (
        np.max(np.abs(mean_of_units - population_M)))

    # the test would pass trivially if nothing moved
    assert population_M[-1] > 0.9
    assert np.ptp(population_M) > 0.9

    # and the identification fails if the relaxation times are not common,
    # which is what makes "a common tau" a hypothesis rather than a convention
    taus = tau * rng.uniform(0.5, 2.0, size=n_units)

    def per_unit_mixed(t, m):
        return ((t >= t_conv).astype(float) - m) / taus

    mixed = solve_ivp(per_unit_mixed, (0.0, t_end), np.zeros(n_units),
                      rtol=1e-11, atol=1e-13, dense_output=True,
                      max_step=0.01)
    assert np.max(np.abs(mixed.sol(t).mean(axis=0) - population_M)) > 1e-3


def test_the_prescribed_history_hypothesis_cannot_be_dropped():
    """``rem:hysteresis-prescribed``: the coupled version contradicts itself.

    The theorem compares two solutions of one system, so both must be driven
    by the same a(t); its conclusion is that they accumulate different vacuum,
    which through the Friedmann constraint gives them different a(t). Stated
    for the coupled system it would contradict its own hypothesis.

    That is checked here rather than argued. The same two histories are
    evolved twice: once against a prescribed expansion, where the comparison
    is available and the vacua separate, and once with the expansion solved
    for from the densities, where the two expansion histories separate too --
    so the premise "the same a(t)" is false and the comparison the theorem
    makes does not exist.
    """
    from scipy.integrate import solve_ivp

    from absorb import stochastic as st

    h = st.hysteresis_experiment(a=lambda t: (1.0 + t) ** (2.0 / 3.0),
                                 t_final=20.0)
    # prescribed: the vacua separate, which is the theorem
    assert h.relative_delta_V > 0.05

    # coupled: integrate (f, M, V) together with a Friedmann-like closure in
    # which the expansion is set by the densities the kinetics produces
    p = st.Kinetics(Gamma0=0.15, alpha=2.0, beta=4.0, tau_M=12.0)

    def coupled(t, y):
        f, M, V, lna = y
        rate = p.Gamma0 * np.exp(p.alpha * f + p.beta * M)
        rho_I = (1.0 - f) * np.exp(-3.0 * lna)
        H = np.sqrt(max(rho_I + V, 1e-300) / 3.0)
        return [(1.0 - f) * rate, (f - M) / p.tau_M,
                (1.0 - f) * rate * np.exp(-3.0 * lna), H]

    out = []
    for M0 in (h.M_A, h.M_B):
        sol = solve_ivp(coupled, (0.0, 12.0), [h.f_checkpoint, M0, 0.30, 0.0],
                        rtol=1e-11, atol=1e-13)
        assert sol.success
        out.append(sol.y[:, -1])

    (fa, _, va, lna_a), (fb, _, vb, lna_b) = out
    # the vacua still separate
    assert abs(va - vb) / max(va, vb) > 1e-3, (va, vb)
    # and so do the expansion histories, by a comparable amount: the premise
    # of the prescribed-history theorem is not available here
    assert abs(lna_a - lna_b) > 1e-3, (lna_a, lna_b)
