"""Symbolic verification of the analytic claims made in the paper.

Every function here re-derives one equation *from its definition* with sympy
and asserts that the result agrees with the form quoted in the text.  Nothing
is copied from the draft: the Christoffel symbols, the stress tensors and the
variational derivatives are all computed on the spot, so a typo in the paper
shows up as a failing test rather than as a plausible-looking formula.

Conventions
-----------
* signature ``(-, +, +, +)``;
* ``eps_{mu nu rho sigma}`` is the Levi-Civita *tensor*, i.e. the permutation
  symbol times ``sqrt(-g)`` (so ``eps^{mu nu rho sigma}`` carries ``-1/sqrt(-g)``);
* ``Mpl`` is the reduced Planck mass, ``8 pi G = 1/Mpl^2``;
* an overdot is ``d/dt`` with ``t`` the cosmic time of the FLRW chart.

Each ``check_*`` returns ``True`` or raises ``AssertionError``.
"""
from __future__ import annotations

from typing import Iterable

import sympy as sp

DIM = 4
IDX = range(DIM)


# ---------------------------------------------------------------------------
# small differential-geometry helpers
# ---------------------------------------------------------------------------
def _christoffel(g: sp.Matrix, coords: Iterable[sp.Symbol]) -> list:
    """Levi-Civita connection ``Gamma^a_{b c}`` of ``g`` as a nested list."""
    coords = list(coords)
    ginv = g.inv()
    return [
        [
            [
                sp.simplify(
                    sp.Rational(1, 2)
                    * sum(
                        ginv[a, d]
                        * (
                            sp.diff(g[d, b], coords[c])
                            + sp.diff(g[d, c], coords[b])
                            - sp.diff(g[b, c], coords[d])
                        )
                        for d in IDX
                    )
                )
                for c in IDX
            ]
            for b in IDX
        ]
        for a in IDX
    ]


def _ricci(gamma: list, coords: Iterable[sp.Symbol]) -> sp.Matrix:
    """Ricci tensor ``R_{b c} = R^a_{b a c}`` from the connection."""
    coords = list(coords)
    R = sp.zeros(DIM, DIM)
    for b in IDX:
        for c in IDX:
            expr = 0
            for a in IDX:
                expr += sp.diff(gamma[a][b][c], coords[a]) - sp.diff(
                    gamma[a][b][a], coords[c]
                )
                for e in IDX:
                    expr += gamma[a][a][e] * gamma[e][b][c]
                    expr -= gamma[a][c][e] * gamma[e][b][a]
            R[b, c] = sp.simplify(expr)
    return R


# ---------------------------------------------------------------------------
# 1. the four-form condensate
# ---------------------------------------------------------------------------
def check_four_form() -> bool:
    """``H_{mu nu rho sigma} = h eps_{mu nu rho sigma}`` behaves as a cosmological
    constant.

    Claims verified, for an arbitrary diagonal metric
    ``g = diag(-A^2, B^2, C^2, D^2)`` with ``A..D`` positive symbols:

        H^2 := H_{mu nu rho sigma} H^{mu nu rho sigma} = -24 h^2 ,
        T_{mu nu} = (1/3!) H_{mu a b c} H_nu^{a b c} - (1/48) g_{mu nu} H^2
                  = -(h^2/2) g_{mu nu} .

    The second line is a perfect fluid with ``p = -rho = -h^2/2``: a
    four-form has no propagating degree of freedom in 4d and its only effect is
    a (quantised) shift of the vacuum energy.  This underlies the "vacuum
    increment" channel of the absorption model.
    """
    A, B, C, D, h = sp.symbols("A B C D h", positive=True)
    g = sp.diag(-A ** 2, B ** 2, C ** 2, D ** 2)
    ginv = g.inv()
    root = sp.sqrt(-g.det())          # = A B C D

    # Levi-Civita tensor (symbol times sqrt(-g)) and the four-form built on it.
    def H(m: int, n: int, r: int, s: int) -> sp.Expr:
        return h * root * sp.LeviCivita(m, n, r, s)

    # H^2
    H2 = 0
    for m in IDX:
        for n in IDX:
            for r in IDX:
                for s in IDX:
                    val = H(m, n, r, s)
                    if val == 0:
                        continue
                    # diagonal metric: raising is a product of diagonal entries
                    H2 += val * H(m, n, r, s) * ginv[m, m] * ginv[n, n] * ginv[r, r] * ginv[s, s]
    H2 = sp.simplify(H2)
    assert sp.simplify(H2 + 24 * h ** 2) == 0, f"H^2 = {H2}, expected -24 h^2"

    # T_{mu nu}
    T = sp.zeros(DIM, DIM)
    for m in IDX:
        for n in IDX:
            expr = 0
            for a in IDX:
                for b in IDX:
                    for c in IDX:
                        first = H(m, a, b, c)
                        if first == 0:
                            continue
                        expr += (
                            first
                            * H(n, a, b, c)
                            * ginv[a, a]
                            * ginv[b, b]
                            * ginv[c, c]
                        )
            T[m, n] = sp.simplify(expr / sp.factorial(3) - g[m, n] * H2 / 48)

    target = -h ** 2 / 2 * g
    diff = sp.simplify(T - target)
    assert diff == sp.zeros(DIM, DIM), f"T_munu - (-h^2/2) g_munu = {diff}"
    return True


# ---------------------------------------------------------------------------
# 2. the clock field
# ---------------------------------------------------------------------------
def check_clock_action() -> bool:
    """Constrained ("clock") scalar: stress tensor and equation of motion.

    For ``L = -(lambda/2) (g^{mu nu} d_mu T d_nu T + 1) - V(T)`` the claims are

        T_{mu nu} = -2 dL/dg^{mu nu} + g_{mu nu} L
                  = lambda u_mu u_nu - V g_{mu nu}     on  (dT)^2 = -1,

    with ``u_mu = -d_mu T`` the unit timelike velocity, and

        nabla_mu (lambda nabla^mu T) = V_{,T} .

    The first line says the clock is a pressureless dust of density ``lambda``
    on top of a ``V(T)`` vacuum term; the second is what makes ``T`` a genuine
    clock.  The variation with respect to ``g^{mu nu}`` is taken treating the
    sixteen components as independent, which is legitimate because ``L``
    depends on them only through the symmetric combination
    ``sum_{mu nu} G^{mu nu} d_mu T d_nu T``.
    """
    lam = sp.Symbol("lamda", positive=True)
    d = sp.symbols("d0:4")                      # d_mu T
    G = sp.Matrix(DIM, DIM, lambda i, j: sp.Symbol(f"G{i}{j}"))    # g^{mu nu}
    gl = sp.Matrix(DIM, DIM, lambda i, j: sp.Symbol(f"gl{i}{j}"))  # g_{mu nu}
    V = sp.Symbol("V")

    kinetic = sum(G[m, n] * d[m] * d[n] for m in IDX for n in IDX)
    L = -lam / 2 * (kinetic + 1) - V

    T = sp.zeros(DIM, DIM)
    for m in IDX:
        for n in IDX:
            T[m, n] = sp.expand(-2 * sp.diff(L, G[m, n]) + gl[m, n] * L)

    # Impose the constraint (dT)^2 = -1 by eliminating one metric component
    # from it, rather than by pattern-matching the sum inside the expression.
    constraint = sp.solve(sp.Eq(kinetic, -1), G[3, 3], dict=True)[0]
    T_on_shell = sp.Matrix(
        DIM, DIM, lambda i, j: sp.simplify(sp.expand(T[i, j].subs(constraint)))
    )
    # u_mu = -d_mu T  =>  u_mu u_nu = d_mu T d_nu T
    target = sp.Matrix(DIM, DIM, lambda i, j: lam * d[i] * d[j] - V * gl[i, j])
    diff = sp.simplify(T_on_shell - target)
    assert diff == sp.zeros(DIM, DIM), f"clock stress tensor mismatch: {diff}"

    # --- equation of motion, on a general diagonal metric -------------------
    x = sp.symbols("t x y z", real=True)
    fs = [sp.Function(name)(*x) for name in ("A", "B", "C", "D")]
    gmat = sp.diag(-fs[0] ** 2, fs[1] ** 2, fs[2] ** 2, fs[3] ** 2)
    ginv = gmat.inv()
    root = sp.sqrt(-gmat.det())
    Tf = sp.Function("T")(*x)
    Vf = sp.Function("V")

    lag = root * (-lam / 2 * (sum(ginv[m, n] * sp.diff(Tf, x[m]) * sp.diff(Tf, x[n])
                                  for m in IDX for n in IDX) + 1) - Vf(Tf))
    euler = sp.diff(lag, Tf) - sum(
        sp.diff(sp.diff(lag, sp.Derivative(Tf, x[m])), x[m]) for m in IDX
    )

    gamma = _christoffel(gmat, x)
    box = sum(ginv[m, n] * sp.diff(Tf, x[m], x[n]) for m in IDX for n in IDX) - sum(
        ginv[m, n] * gamma[r][m][n] * sp.diff(Tf, x[r])
        for m in IDX
        for n in IDX
        for r in IDX
    )
    # euler / sqrt(-g)  ==  lambda box T - V'(T), i.e. the quoted equation
    residual = sp.simplify(sp.expand(euler / root - (lam * box - sp.diff(Vf(Tf), Tf))))
    assert residual == 0, f"clock equation of motion mismatch: {residual}"
    return True


# ---------------------------------------------------------------------------
# 3. FLRW curvature
# ---------------------------------------------------------------------------
def check_flrw() -> bool:
    """Einstein tensor and Ricci scalar of ``ds^2 = -dt^2 + a(t)^2 dx^2``.

    Verified:  ``G_00 = 3 H^2``,  ``G_ij = -(2 Hdot + 3 H^2) g_ij``,
    ``R = 6 (Hdot + 2 H^2)``, with ``H = adot/a``.
    """
    t, x, y, z = sp.symbols("t x y z", real=True)
    coords = (t, x, y, z)
    a = sp.Function("a", positive=True)(t)
    g = sp.diag(-1, a ** 2, a ** 2, a ** 2)
    ginv = g.inv()

    gamma = _christoffel(g, coords)
    Ric = _ricci(gamma, coords)
    R = sp.simplify(sum(ginv[m, n] * Ric[m, n] for m in IDX for n in IDX))
    G = sp.Matrix(DIM, DIM, lambda i, j: sp.simplify(Ric[i, j] - R * g[i, j] / 2))

    H = sp.diff(a, t) / a
    Hdot = sp.diff(H, t)

    assert sp.simplify(R - 6 * (Hdot + 2 * H ** 2)) == 0, f"R = {R}"
    assert sp.simplify(G[0, 0] - 3 * H ** 2) == 0, f"G_00 = {G[0, 0]}"
    for i in (1, 2, 3):
        resid = sp.simplify(G[i, i] + (2 * Hdot + 3 * H ** 2) * g[i, i])
        assert resid == 0, f"G_{i}{i} mismatch: {resid}"
    for m in IDX:
        for n in IDX:
            if m != n:
                assert sp.simplify(G[m, n]) == 0, f"G_{m}{n} should vanish"
    return True


# ---------------------------------------------------------------------------
# 4. cosmography
# ---------------------------------------------------------------------------
def check_jerk_identity() -> bool:
    """``j = 1 - pdot / (2 Mpl^2 H^3)`` in any single-fluid FLRW background.

    Two steps, both symbolic:

    (i)  from ``j := adddot / (a H^3)`` and ``H = adot/a``,
         ``j = 1 + 3 Hdot/H^2 + Hddot/H^3``;
    (ii) eliminating ``rho`` and ``p`` with the Friedmann pair
         ``3 Mpl^2 H^2 = rho`` and ``Mpl^2 (2 Hdot + 3 H^2) = -p`` turns the
         right-hand side into ``1 - pdot/(2 Mpl^2 H^3)``.

    The continuity equation ``rhodot = -3H(rho+p)`` is then checked to hold
    identically, which is the Bianchi identity for this background.
    """
    t = sp.Symbol("t", real=True)
    Mpl = sp.Symbol("M_Pl", positive=True)
    a = sp.Function("a", positive=True)(t)
    H = sp.diff(a, t) / a

    # (i) kinematic identity
    j_kin = sp.diff(a, t, 3) / (a * H ** 3)
    j_H = 1 + 3 * sp.diff(H, t) / H ** 2 + sp.diff(H, t, 2) / H ** 3
    assert sp.simplify(j_kin - j_H) == 0, "j is not 1 + 3 Hdot/H^2 + Hddot/H^3"

    # (ii) dynamics
    rho = 3 * Mpl ** 2 * H ** 2
    p = -Mpl ** 2 * (2 * sp.diff(H, t) + 3 * H ** 2)
    j_dyn = 1 - sp.diff(p, t) / (2 * Mpl ** 2 * H ** 3)
    assert sp.simplify(j_H - j_dyn) == 0, "jerk identity fails"

    cont = sp.simplify(sp.diff(rho, t) + 3 * H * (rho + p))
    assert cont == 0, f"continuity residual {cont}"
    return True


def check_growth_equation() -> bool:
    """Second-order growth equation with a source/absorption term ``gamma_c``.

    From the first-order pair

        deltadot = -theta + gamma_c delta ,
        thetadot + 2 H theta = -rho delta / (2 Mpl^2) ,

    eliminating ``theta`` gives

        deltaddot + (2H - gamma_c) deltadot
            - (rho/(2 Mpl^2) + gamma_cdot + 2 H gamma_c) delta = 0 .

    Note the *sign*: a positive absorption rate both anti-damps the mode and
    adds to the effective source, which is the signature the paper looks for in
    growth data.
    """
    t = sp.Symbol("t", real=True)
    Mpl = sp.Symbol("M_Pl", positive=True)
    delta = sp.Function("delta")(t)
    gam = sp.Function("gamma_c")(t)
    H = sp.Function("H")(t)
    rho = sp.Function("rho")(t)

    theta = -sp.diff(delta, t) + gam * delta            # first equation
    residual = sp.diff(theta, t) + 2 * H * theta + rho * delta / (2 * Mpl ** 2)

    target = (
        sp.diff(delta, t, 2)
        + (2 * H - gam) * sp.diff(delta, t)
        - (rho / (2 * Mpl ** 2) + sp.diff(gam, t) + 2 * H * gam) * delta
    )
    # residual = 0 and target = 0 must be the same equation (here: target = -residual)
    diff = sp.simplify(sp.expand(target + residual))
    assert diff == 0, f"growth equation mismatch: {diff}"
    return True


# ---------------------------------------------------------------------------
# 5. the exactly solvable family Gamma = xi H
# ---------------------------------------------------------------------------
def check_solvable_family() -> bool:
    """Closed-form background for a rate locked to the expansion, ``Gamma = xi H``.

    With ``N = ln a`` the kinetic equations lose all reference to ``H``:
    ``d/dN`` of every density is algebraic in ``xi``.  The solutions, normalised
    at ``a = 1``, are

        rho_I = rho_I0 a^-(3+xi) ,
        rho_D = a^-3 [ rho_D0 + b rho_I0 (1 - a^-xi) ] ,
        V     = V0 + xi (1-b) rho_I0 (1 - a^-(3+xi)) / (3+xi) ,
        f     = 1 - (1 - f0) a^-xi ,

    and they are checked here against the defining ODEs

        rhodot_I + 3 H rho_I = -Gamma rho_I ,
        rhodot_D + 3 H rho_D = +b Gamma rho_I ,
        Vdot                 = (1-b) Gamma rho_I ,
        fdot                 = (1-f) Gamma ,

    for a completely arbitrary ``a(t)``: the family is a solution whatever the
    expansion history does, which is exactly why it is used as the analytic
    benchmark for the numerical background integrator.
    """
    t = sp.Symbol("t", real=True)
    a = sp.Function("a", positive=True)(t)
    xi, b = sp.symbols("xi b", positive=True)
    rho_I0, rho_D0, V0, f0 = sp.symbols("rho_I0 rho_D0 V0 f0", real=True)

    H = sp.diff(a, t) / a
    Gamma = xi * H

    rho_I = rho_I0 * a ** (-(3 + xi))
    rho_D = a ** (-3) * (rho_D0 + b * rho_I0 * (1 - a ** (-xi)))
    V = V0 + xi * (1 - b) * rho_I0 * (1 - a ** (-(3 + xi))) / (3 + xi)
    f = 1 - (1 - f0) * a ** (-xi)

    checks = {
        "rho_I": sp.diff(rho_I, t) + 3 * H * rho_I + Gamma * rho_I,
        "rho_D": sp.diff(rho_D, t) + 3 * H * rho_D - b * Gamma * rho_I,
        "V": sp.diff(V, t) - (1 - b) * Gamma * rho_I,
        "f": sp.diff(f, t) - (1 - f) * Gamma,
    }
    for name, residual in checks.items():
        r = sp.simplify(sp.powsimp(sp.expand(residual), force=True))
        assert r == 0, f"{name} equation not satisfied: {r}"

    # consistency: the total converted comoving density is conserved
    total = sp.simplify(
        sp.powsimp(
            sp.expand(
                sp.diff(rho_I + rho_D, t)
                + 3 * H * (rho_I + rho_D)
                + (1 - b) * Gamma * rho_I
            ),
            force=True,
        )
    )
    assert total == 0, f"I + D budget not closed: {total}"
    return True


ALL_CHECKS = (
    check_four_form,
    check_clock_action,
    check_flrw,
    check_jerk_identity,
    check_growth_equation,
    check_solvable_family,
)


def run_all() -> dict[str, bool]:
    """Run every check; returns ``{name: True}`` or raises on the first failure."""
    return {fn.__name__: fn() for fn in ALL_CHECKS}
