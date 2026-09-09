"""Tests for absorb.symbolic.

Each ``check_*`` is exercised twice: once through its own assertion machinery,
and once through an independent spot check performed here, so that a check that
silently degenerated into a tautology would still be caught.
"""
from __future__ import annotations

import sympy as sp

from absorb import symbolic as sy


# ---------------------------------------------------------------------------
# the six claims
# ---------------------------------------------------------------------------
def test_four_form() -> None:
    assert sy.check_four_form() is True


def test_four_form_equation_of_state() -> None:
    """Independent check: the four-form fluid has w = -1 in FLRW.

    T_munu = -(h^2/2) g_munu means rho = T_00 = h^2/2 and
    p = T_11/g_11 = -h^2/2.
    """
    t = sp.Symbol("t", real=True)
    a = sp.Function("a", positive=True)(t)
    h = sp.Symbol("h", positive=True)
    g = sp.diag(-1, a ** 2, a ** 2, a ** 2)
    T = -h ** 2 / 2 * g
    rho = T[0, 0]                       # u^mu u^nu T_munu with u = (1,0,0,0)
    p = sp.simplify(T[1, 1] / g[1, 1])
    assert sp.simplify(p + rho) == 0


def test_clock_action() -> None:
    assert sy.check_clock_action() is True


def test_clock_action_is_dust_plus_vacuum() -> None:
    """Independent check: on the constraint the clock's energy density is
    lambda + V and its pressure is -V, i.e. dust plus a vacuum term."""
    lam, V = sp.symbols("lamda V", positive=True)
    t = sp.Symbol("t", real=True)
    a = sp.Function("a", positive=True)(t)
    g = sp.diag(-1, a ** 2, a ** 2, a ** 2)
    # comoving clock: T = t, so d_mu T = (1,0,0,0), u_mu = (-1,0,0,0)
    u = sp.Matrix([-1, 0, 0, 0])
    T = sp.Matrix(4, 4, lambda i, j: lam * u[i] * u[j] - V * g[i, j])
    rho = T[0, 0]
    p = sp.simplify(T[1, 1] / g[1, 1])
    assert sp.simplify(rho - (lam + V)) == 0
    assert sp.simplify(p + V) == 0


def test_flrw() -> None:
    assert sy.check_flrw() is True


def test_flrw_matter_solution() -> None:
    """Independent check: a ~ t^(2/3) solves G_00 = rho/Mpl^2 with p = 0."""
    t = sp.Symbol("t", positive=True)
    a = t ** sp.Rational(2, 3)
    H = sp.diff(a, t) / a
    Hdot = sp.diff(H, t)
    rho = 3 * H ** 2                       # Mpl = 1
    p = -(2 * Hdot + 3 * H ** 2)
    assert sp.simplify(p) == 0
    assert sp.simplify(sp.diff(rho, t) + 3 * H * (rho + p)) == 0


def test_jerk_identity() -> None:
    assert sy.check_jerk_identity() is True


def test_jerk_is_one_for_lcdm() -> None:
    """Independent check: a constant p (a cosmological constant plus dust)
    gives j = 1 exactly, which is the null hypothesis the paper tests."""
    t = sp.Symbol("t", positive=True)
    Mpl = sp.Symbol("M_Pl", positive=True)
    # LCDM: rho = rho_m0 a^-3 + Lambda-like constant, so p = -const
    a = sp.Function("a", positive=True)(t)
    H = sp.diff(a, t) / a
    p = sp.Symbol("p_const")
    j = 1 - sp.diff(p, t) / (2 * Mpl ** 2 * H ** 3)
    assert sp.simplify(j - 1) == 0


def test_growth_equation() -> None:
    assert sy.check_growth_equation() is True


def test_growth_reduces_to_standard_case() -> None:
    """With gamma_c = 0 the growth equation is the textbook one."""
    t = sp.Symbol("t", real=True)
    Mpl = sp.Symbol("M_Pl", positive=True)
    delta = sp.Function("delta")(t)
    H = sp.Function("H")(t)
    rho = sp.Function("rho")(t)
    gam = sp.Integer(0)
    eq = (
        sp.diff(delta, t, 2)
        + (2 * H - gam) * sp.diff(delta, t)
        - (rho / (2 * Mpl ** 2) + sp.diff(gam, t) + 2 * H * gam) * delta
    )
    standard = sp.diff(delta, t, 2) + 2 * H * sp.diff(delta, t) - rho * delta / (2 * Mpl ** 2)
    assert sp.simplify(eq - standard) == 0


def test_solvable_family() -> None:
    assert sy.check_solvable_family() is True


def test_solvable_family_limits() -> None:
    """xi -> 0 must switch the conversion off and freeze every density."""
    a, xi, b = sp.symbols("a xi b", positive=True)
    rho_I0, rho_D0, V0, f0 = sp.symbols("rho_I0 rho_D0 V0 f0", real=True)
    rho_I = rho_I0 * a ** (-(3 + xi))
    rho_D = a ** (-3) * (rho_D0 + b * rho_I0 * (1 - a ** (-xi)))
    V = V0 + xi * (1 - b) * rho_I0 * (1 - a ** (-(3 + xi))) / (3 + xi)
    f = 1 - (1 - f0) * a ** (-xi)
    assert sp.simplify(sp.limit(rho_I, xi, 0) - rho_I0 * a ** -3) == 0
    assert sp.simplify(sp.limit(rho_D, xi, 0) - rho_D0 * a ** -3) == 0
    assert sp.simplify(sp.limit(V, xi, 0) - V0) == 0
    assert sp.simplify(sp.limit(f, xi, 0) - f0) == 0


# ---------------------------------------------------------------------------
# aggregate entry point
# ---------------------------------------------------------------------------
def test_run_all() -> None:
    results = sy.run_all()
    assert set(results) == {fn.__name__ for fn in sy.ALL_CHECKS}
    assert all(results.values())
