"""Tests for the hedgehog Skyrme sector (absorb.skyrme).

Every reference number is either an exact closed form derived in the module
docstrings (trial energy, Bogomolny bound) or the literature value for the
B = 1 Skyrmion expressed in this module's units.
"""
# covers: eq:defects-solved, prop:derrick
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

from __future__ import annotations

import math

import numpy as np
import pytest

from absorb import skyrme as sk

# Literature value of the classical B = 1 Skyrmion energy, quoted as a ratio to
# the Faddeev-Bogomolny bound (Adkins-Nappi-Witten 1983 and every later
# treatment agree on E / E_bound = 1.232 to four digits).
SKYRME_BOUND_RATIO = 1.232


@pytest.fixture(scope="module")
def hedgehog() -> sk.Hedgehog:
    return sk.solve_hedgehog()


# ---------------------------------------------------------------------------
# Variational (trial) sector
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("R", [0.25, 0.5, 1.0, 1.7, 3.0, 6.0])
def test_trial_energy_closed_form(R: float) -> None:
    """Quadrature of the energy functional reproduces 6 pi^2 (R + 1/R)."""
    numeric = sk.trial_energy(R, quadrature=True)
    closed = 6.0 * math.pi ** 2 * (R + 1.0 / R)
    assert numeric == pytest.approx(closed, rel=1e-8, abs=1e-8)


def test_trial_minimum() -> None:
    """The conformal family is minimised at R = 1 with energy 12 pi^2."""
    grid = np.linspace(0.2, 5.0, 4801)
    energies = np.array([sk.trial_energy(R, quadrature=False) for R in grid])
    i = int(np.argmin(energies))
    assert grid[i] == pytest.approx(1.0, abs=grid[1] - grid[0])
    assert energies[i] == pytest.approx(12.0 * math.pi ** 2, rel=1e-10)
    # and the quadrature agrees with that minimum
    assert sk.trial_energy(1.0) == pytest.approx(12.0 * math.pi ** 2, rel=1e-9)
    assert sk.TRIAL_MIN == pytest.approx(118.4352528, rel=1e-8)


def test_trial_energy_rejects_nonpositive_scale() -> None:
    with pytest.raises(ValueError):
        sk.trial_energy(0.0)


# ---------------------------------------------------------------------------
# Euler-Lagrange derivation
# ---------------------------------------------------------------------------
def test_euler_lagrange_is_variational_derivative() -> None:
    """sympy check that the coded ODE follows from the coded energy density."""
    assert sk.check_euler_lagrange_symbolic() is True


def test_solution_satisfies_euler_lagrange_pointwise(hedgehog: sk.Hedgehog) -> None:
    """The numerical profile annihilates the residual away from the endpoints."""
    x = np.geomspace(1e-2, 10.0, 400)
    F, Fp = hedgehog.sol(x)
    # F'' from the first-order system the solver actually integrated
    Fpp = sk._rhs(x, np.vstack((F, Fp)))[1]
    res = sk.euler_lagrange_residual(x, F, Fp, Fpp)
    scale = np.max(np.abs((x ** 2 + 4.0 * np.sin(F) ** 2) * Fpp))
    assert np.max(np.abs(res)) < 1e-8 * scale


# ---------------------------------------------------------------------------
# The B = 1 solution
# ---------------------------------------------------------------------------
def test_bogomolny_bound_value() -> None:
    assert sk.bogomolny_bound() == pytest.approx(6.0 * math.sqrt(2.0) * math.pi ** 2)


def test_energy_between_bound_and_trial_minimum(hedgehog: sk.Hedgehog) -> None:
    """bound <= Etilde < trial minimum, and Etilde matches the known value."""
    assert sk.bogomolny_bound() <= hedgehog.Etilde < sk.TRIAL_MIN
    expected = SKYRME_BOUND_RATIO * sk.bogomolny_bound()   # ~103.2
    assert hedgehog.Etilde == pytest.approx(expected, rel=1e-2)
    assert hedgehog.bound_ratio == pytest.approx(SKYRME_BOUND_RATIO, rel=1e-2)


def test_virial_identity(hedgehog: sk.Hedgehog) -> None:
    """Derrick scaling x -> lambda x sends (E2, E4) -> (lambda E2, E4/lambda),
    so a stationary point must have E2 = E4."""
    assert hedgehog.E2 == pytest.approx(hedgehog.E4, rel=1e-5)
    assert abs(hedgehog.virial) < 1e-5


def test_degree_is_one(hedgehog: sk.Hedgehog) -> None:
    assert hedgehog.B == pytest.approx(1.0, abs=1e-6)
    assert hedgehog.B_quadrature == pytest.approx(1.0, abs=1e-6)
    assert sk.degree(sk.trial_profile(np.geomspace(1e-6, 1e6, 5))) == pytest.approx(
        1.0, abs=1e-6
    )


def test_profile_shape_and_asymptotics(hedgehog: sk.Hedgehog) -> None:
    """Monotone pi -> 0, with the regular series and the dipole tail."""
    assert np.all(np.diff(hedgehog.F) < 0.0)
    assert hedgehog.F[0] == pytest.approx(np.pi, abs=1e-6)
    assert hedgehog.slope > 0.0
    assert hedgehog.tail > 0.0
    # F ~ pi - s x at small x (the fit window excludes the innermost decade,
    # where pinning F(x_min) = pi injects a little of the x^-2 solution)
    x_small = np.geomspace(2e-3, 2e-2, 20)
    F_small = hedgehog.sol(x_small)[0]
    assert np.allclose(F_small, np.pi - hedgehog.slope * x_small, rtol=0.0, atol=1e-4)
    # and F' is regular (finite, nearly constant) there
    Fp_small = hedgehog.sol(x_small)[1]
    assert np.allclose(Fp_small, -hedgehog.slope, rtol=2e-3)
    # F ~ C/x^2 at large x
    x_big = np.geomspace(20.0, 40.0, 20)
    F_big = hedgehog.sol(x_big)[0]
    assert np.allclose(F_big, hedgehog.tail / x_big ** 2, rtol=2e-2)


def test_solved_energy_beats_every_trial_profile(hedgehog: sk.Hedgehog) -> None:
    """The true minimiser is below the whole one-parameter trial family."""
    for R in (0.5, 0.8, 1.0, 1.25, 2.0):
        assert hedgehog.Etilde < sk.trial_energy(R, quadrature=False)


def test_window_independence() -> None:
    """Doubling the outer radius does not move the energy at the 1e-5 level.

    This is what justifies quoting Etilde to four digits: with the Robin
    condition plus the analytic tail the answer is independent of x_max.
    """
    far = sk.solve_hedgehog(x_max=80.0)
    near = sk.solve_hedgehog(x_max=40.0)
    assert far.Etilde == pytest.approx(near.Etilde, rel=1e-5)


def test_rejects_bad_window() -> None:
    with pytest.raises(ValueError):
        sk.solve_hedgehog(x_min=1.0, x_max=0.5)
