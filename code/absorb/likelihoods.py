"""Gaussian likelihoods for the background probes.

Every likelihood exposes the same minimal interface,

    chi2(bg, nuisance) -> float

where ``bg`` is a solved :class:`~absorb.background.Background` and
``nuisance`` is an optional mapping of nuisance parameters (only the
supernova and RSD likelihoods use one, and the supernova absolute magnitude
is marginalised analytically rather than sampled).  The log-likelihood is
``logL = -chi2/2`` throughout: all normalisation constants that do not depend
on the model are dropped, with the single exception of the ``log(E0/2 pi)``
term produced by the analytic marginalisation over M_B, which *does* depend
on the data selection and is kept so that different SN samples can be
compared.

Numerics
--------
No covariance is ever inverted explicitly.  Each data set caches a Cholesky
factorisation at load time and every chi^2 is evaluated with
:func:`scipy.linalg.cho_solve`, which is both faster and numerically far
better conditioned -- the 1701 x 1701 Pantheon+ matrix has a condition
number of ~10^6.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Mapping, Protocol, Sequence

import numpy as np
from scipy.linalg import cho_factor, cho_solve, solve_triangular

from . import early
from .background import Background
from .data import cc as cc_data
from .data import desi as desi_data
from .data import pantheon as pantheon_data
from .data import planck_priors as planck_data
from .data import rsd as rsd_data
from .data.paths import check_covariance

__all__ = [
    "Likelihood",
    "PantheonLikelihood",
    "DesiBAOLikelihood",
    "ChronometerLikelihood",
    "PlanckPriorLikelihood",
    "RSDLikelihood",
    "JointLikelihood",
]

Nuisance = Mapping[str, float] | None


class Likelihood(Protocol):
    """Anything that can score a background against data."""

    name: str

    def chi2(self, bg: Background, nuisance: Nuisance = None) -> float:
        """chi^2 = -2 log L up to a model-independent constant."""
        ...

    def n_data(self) -> int:
        """Number of data points entering :meth:`chi2`."""
        ...


def _chi2_cho(residual: np.ndarray, cho: tuple[np.ndarray, bool]) -> float:
    """r^T C^-1 r via the cached Cholesky factor."""
    return float(residual @ cho_solve(cho, residual))


# ---------------------------------------------------------------------------
# Type Ia supernovae
# ---------------------------------------------------------------------------
@dataclass
class PantheonLikelihood:
    """Pantheon+ (optionally + SH0ES Cepheid calibrators).

    The model prediction for a Hubble-flow supernova is

        m_B,i = M_B + mu(z_i),   mu = 5 log10(D_L/Mpc) + 25,

    with D_L = (1 + z_hel) D_M(z_hd).  For a Cepheid-calibrated host the
    distance modulus is supplied externally by ``CEPH_DIST``, so the residual
    is m_B,i - CEPH_DIST_i and involves *the same* M_B.  Defining

        Delta_i = m_B,i - mu_i            (Hubble flow)
        Delta_i = m_B,i - CEPH_DIST_i     (calibrators)

    the chi^2 at fixed M_B is (Delta - M_B 1)^T C^-1 (Delta - M_B 1).  With a
    flat prior on M_B the marginal likelihood is a Gaussian integral,

        chi^2_marg = A - B^2/E0 + log(E0 / 2 pi),
        A = Delta^T C^-1 Delta,  B = Delta^T C^-1 1,  E0 = 1^T C^-1 1,

    (Goliath et al. 2001; Conley et al. 2011, Appendix C).  The log term is
    the Jacobian of the marginalisation; it is constant for a fixed data
    selection but is kept explicit so that the returned number is a genuine
    -2 log L.

    Setting ``marginalize_MB=False`` instead uses ``nuisance["M_B"]``.

    Note that with ``with_shoes=False`` the marginalisation removes *all*
    sensitivity to H_0: only the shape of the distance-redshift relation is
    constrained.  With ``with_shoes=True`` the calibrator rows pin M_B and
    the sample does constrain H_0.
    """

    with_shoes: bool = False
    marginalize_MB: bool = True
    name: str = field(default="", init=False)

    def __post_init__(self) -> None:
        self.name = "SN(Pantheon+SH0ES)" if self.with_shoes else "SN(Pantheon+)"
        self._d = pantheon_data.load_pantheon(with_shoes=self.with_shoes)
        self._real_mb = None
        self._marg_cache = None

    @property
    def data(self) -> pantheon_data.PantheonData:
        return self._d

    def n_data(self) -> int:
        return self._d.n

    def dof(self) -> int:
        """Data points minus the one marginalised nuisance parameter."""
        return self._d.n - (1 if self.marginalize_MB else 0)

    def residual(self, bg: Background) -> np.ndarray:
        """Delta_i, i.e. the residual *before* subtracting M_B."""
        d = self._d
        mu = bg.distance_modulus(d.z_hd, d.z_hel)
        model = np.where(d.use_cepheid, d.ceph_dist, mu)
        return d.m_b_corr - model

    def chi2(self, bg: Background, nuisance: Nuisance = None) -> float:
        d = self._d
        delta = self.residual(bg)
        if not self.marginalize_MB:
            M_B = float((nuisance or {}).get("M_B", 0.0))
            return _chi2_cho(delta - M_B, d.cho)
        # C^-1 1 and 1^T C^-1 1 do not depend on the cosmology, so they are
        # cached on first use.  The remaining quadratic form is evaluated as
        # ||L^-1 Delta||^2 with a single triangular solve, which is half the
        # work of cho_solve and makes the supernova term cheap enough that the
        # sampler is dominated by the background integration rather than by
        # linear algebra.
        cache = self._marg_cache
        if cache is None:
            ones = np.ones_like(delta)
            Cinv_one = cho_solve(d.cho, ones)
            cache = (Cinv_one, float(ones @ Cinv_one))
            self._marg_cache = cache
        Cinv_one, E0 = cache
        L, lower = d.cho
        y = solve_triangular(L, delta, lower=lower, check_finite=False)
        A = float(y @ y)
        B = float(delta @ Cinv_one)
        return A - B * B / E0 + float(np.log(E0 / (2.0 * np.pi)))

    def simulate(self, bg: Background, rng) -> None:
        """Replace the data with a draw from the model at ``bg``.

        Used only by the threshold calibration, which needs the null
        distribution of a likelihood-ratio statistic that regular asymptotics
        do not supply. The draw is ``model + L z`` with ``L`` the Cholesky
        factor already held for the chi-square, so the synthetic data carry
        exactly the covariance the fit assumes. ``restore`` puts the real data
        back, and every simulate/restore pair is balanced by the caller.
        """
        d = self._d
        if self._real_mb is None:
            self._real_mb = d.m_b_corr.copy()
        mu = bg.distance_modulus(d.z_hd, d.z_hel)
        model = np.where(d.use_cepheid, d.ceph_dist, mu)
        d.m_b_corr[:] = model + _draw(d.cho, rng, d.n)

    def restore(self) -> None:
        if self._real_mb is not None:
            self._d.m_b_corr[:] = self._real_mb

    def best_fit_MB(self, bg: Background) -> float:
        """The profiled absolute magnitude, M_B = B/E0."""
        d = self._d
        delta = self.residual(bg)
        ones = np.ones_like(delta)
        return float(delta @ cho_solve(d.cho, ones)) / float(ones @ cho_solve(d.cho, ones))


# ---------------------------------------------------------------------------
# BAO
# ---------------------------------------------------------------------------
def _draw(cho, rng, n) -> np.ndarray:
    """A correlated Gaussian draw with covariance ``C``, given ``cho_factor``.

    ``cho_factor`` returns the factor in one triangle and *arbitrary values in
    the other*, so the raw array must not be multiplied as if it were
    triangular. Extracting the triangle is the whole content of this helper,
    and getting it wrong would silently inflate the simulated covariance --
    which is why the test asserts the empirical covariance of many draws
    against the stated one.
    """
    c, lower = cho
    L = np.tril(c) if lower else np.triu(c).T
    return L @ rng.standard_normal(n)


def _bao_model(bg: Background, z: np.ndarray, quantity: np.ndarray,
               r_d: float) -> np.ndarray:
    """Model vector for a list of (z, quantity) BAO observables."""
    getters = {"DV_over_rs": bg.D_V, "DM_over_rs": bg.D_M, "DH_over_rs": bg.D_H}
    out = np.empty(z.size, dtype=float)
    seen = np.zeros(z.size, dtype=bool)
    for name, getter in getters.items():          # one vectorised call per kind
        m = quantity == name
        if m.any():
            out[m] = np.asarray(getter(z[m]), dtype=float) / r_d
            seen |= m
    if not seen.all():
        raise ValueError(f"BAO: unknown quantities {sorted(set(quantity[~seen]))}")
    return out


@dataclass
class DesiBAOLikelihood:
    """DESI DR2 BAO distances.

    The sound horizon at the drag epoch is evaluated from the fitting formula
    :func:`absorb.early.r_drag` with the **pre-activation** densities
    ``omega_b`` and ``omega_b + omega_c`` taken from the background
    parameters.  This is the physically correct choice, and it matters: in
    the absorption model part of ``omega_c`` is converted into vacuum energy
    after activation, so today's matter density is lower than ``omega_c`` by
    eps omega_c f_0.  The BAO ruler, however, is imprinted at z ~ 1060, long
    before the switch opens (S_act ~ (a/a_act)^p with p >~ 6 gives a
    suppression of >10^20 there), when the convertible sector is still
    entirely pressureless matter.  Using the *present-day* matter density
    here would shift r_d by several percent and fake a BAO signal of the
    conversion.
    """

    method: str = "aubourg"
    name: str = "BAO(DESI DR2)"

    def __post_init__(self) -> None:
        self._d = desi_data.load_desi()
        self._real = None

    @property
    def data(self) -> desi_data.BAOData:
        return self._d

    def n_data(self) -> int:
        return self._d.n

    def r_drag(self, bg: Background) -> float:
        """Drag-epoch sound horizon in Mpc for this background."""
        p = bg.p
        return early.r_drag(p.omega_b, p.omega_b + p.omega_c, method=self.method)

    def model(self, bg: Background) -> np.ndarray:
        d = self._d
        return _bao_model(bg, d.z, d.quantity, self.r_drag(bg))

    def chi2(self, bg: Background, nuisance: Nuisance = None) -> float:
        d = self._d
        return _chi2_cho(d.value - self.model(bg), d.cho)

    def simulate(self, bg: Background, rng) -> None:
        d = self._d
        if self._real is None:
            self._real = d.value.copy()
        d.value[:] = self.model(bg) + _draw(d.cho, rng, d.n)

    def restore(self) -> None:
        if self._real is not None:
            self._d.value[:] = self._real


# ---------------------------------------------------------------------------
# Cosmic chronometers
# ---------------------------------------------------------------------------
@dataclass
class ChronometerLikelihood:
    """H(z) from cosmic chronometers, with the Moresco systematic covariance.

    A pure expansion-rate probe: no sound horizon, no standard candle, hence
    no nuisance parameter.  ``H_model = 100 E(z)`` in km/s/Mpc.
    """

    variant: str = "default"
    name: str = "CC"

    def __post_init__(self) -> None:
        self._d = cc_data.load_cc(self.variant)
        self._real = None
        self.name = f"CC({self.variant})"

    @property
    def data(self) -> cc_data.CosmicChronometers:
        return self._d

    def n_data(self) -> int:
        return self._d.n

    def chi2(self, bg: Background, nuisance: Nuisance = None) -> float:
        d = self._d
        return _chi2_cho(d.H - 100.0 * bg.E(d.z), d.cho)

    def simulate(self, bg: Background, rng) -> None:
        d = self._d
        if self._real is None:
            self._real = d.H.copy()
        d.H[:] = 100.0 * bg.E(d.z) + _draw(d.cho, rng, d.n)

    def restore(self) -> None:
        if self._real is not None:
            self._d.H[:] = self._real


# ---------------------------------------------------------------------------
# Compressed CMB
# ---------------------------------------------------------------------------
@dataclass
class PlanckPriorLikelihood:
    """Planck 2018 compressed distance priors (R, l_A, omega_b).

    Both geometric entries are computed with the *pre-activation* densities,
    for the reason spelled out in :class:`DesiBAOLikelihood`: R and l_A
    describe the angular size of a ruler laid down at recombination, and the
    matter density that sets both the ruler and the expansion rate there is
    omega_b + omega_c before any conversion has taken place.  The late-time
    conversion enters only through D_M(z_*), which is an integral over the
    full history and is therefore sensitive to the model exactly as intended.
    """

    name: str = "CMB(compressed)"

    def __post_init__(self) -> None:
        self._d = planck_data.load_planck_priors()
        self._real = None

    @property
    def data(self) -> planck_data.PlanckPriors:
        return self._d

    def n_data(self) -> int:
        return self._d.n

    def model(self, bg: Background) -> np.ndarray:
        p = bg.p
        omega_m = p.omega_b + p.omega_c + early.OMEGA_NU0
        R, l_A = early.cmb_distance_priors(bg, p.omega_b, omega_m)
        return np.array([R, l_A, p.omega_b])

    def chi2(self, bg: Background, nuisance: Nuisance = None) -> float:
        d = self._d
        return _chi2_cho(d.mean - self.model(bg), d.cho)

    def simulate(self, bg: Background, rng) -> None:
        d = self._d
        if self._real is None:
            self._real = d.mean.copy()
        d.mean[:] = self.model(bg) + _draw(d.cho, rng, d.n)

    def restore(self) -> None:
        if self._real is not None:
            self._d.mean[:] = self._real


# ---------------------------------------------------------------------------
# Redshift-space distortions
# ---------------------------------------------------------------------------
FS8Model = Callable[[Background, np.ndarray], np.ndarray]


@dataclass
class RSDLikelihood:
    """f sigma_8 from the SDSS DR16 full-shape + BAO consensus.

    Only the ``f_sigma8`` entries are used, together with the corresponding
    rows *and columns* of the covariance: at each effective redshift the
    growth measurement is strongly correlated with the two geometric ones
    (|rho| ~ 0.4), which are dropped here because they overlap in volume with
    the DESI sample and would otherwise be counted twice.

    Growth is not part of the background module, so the model must be
    supplied as a callable ``fs8_model(bg, z) -> array``; sigma_8 (or the
    combination A_s-sigma_8) is then a nuisance parameter of that callable,
    not of this class.  With :mod:`absorb.growth` the wiring is::

        from absorb.growth import Growth
        RSDLikelihood(fs8_model=lambda bg, z: Growth(bg).f_sigma8(z, sigma8_0))

    Until a model is supplied the likelihood raises rather than silently
    returning a wrong number.
    """

    fs8_model: FS8Model | None = None
    name: str = "RSD(DR16 fsigma8)"

    def __post_init__(self) -> None:
        d = rsd_data.load_rsd()
        self._full = d
        z, value, cov = d.fs8_block()
        cov = check_covariance(cov, "DR16 f sigma_8 block")
        self._z = z
        self._value = value
        self._cov = cov
        self._cho = cho_factor(cov, lower=True)

    @property
    def z(self) -> np.ndarray:
        return self._z

    @property
    def value(self) -> np.ndarray:
        return self._value

    @property
    def cov(self) -> np.ndarray:
        return self._cov

    def n_data(self) -> int:
        return self._z.size

    def chi2(self, bg: Background, nuisance: Nuisance = None) -> float:
        model = self.fs8_model
        if nuisance is not None and "fs8_model" in nuisance:
            model = nuisance["fs8_model"]
        if model is None:
            raise NotImplementedError(
                "RSDLikelihood needs an f sigma_8 model.  Pass "
                "fs8_model=callable(bg, z) -> array (e.g. from absorb.growth) "
                "when constructing the likelihood."
            )
        pred = np.asarray(model(bg, self._z), dtype=float)
        if pred.shape != self._z.shape:
            raise ValueError(
                f"fs8_model returned shape {pred.shape}, expected {self._z.shape}"
            )
        return _chi2_cho(self._value - pred, self._cho)


# ---------------------------------------------------------------------------
# Combination
# ---------------------------------------------------------------------------
@dataclass
class JointLikelihood:
    """Sum of independent likelihoods.

    The data sets combined here are taken to be statistically independent:
    they come from different instruments and (with the exception noted in
    :class:`RSDLikelihood`) non-overlapping volumes, so their covariances are
    block diagonal and the chi^2 values simply add.
    """

    parts: Sequence[Likelihood]
    name: str = "joint"

    def __post_init__(self) -> None:
        self.parts = list(self.parts)
        if not self.parts:
            raise ValueError("JointLikelihood: at least one component required")

    def n_data(self) -> int:
        return sum(p.n_data() for p in self.parts)

    def chi2(self, bg: Background, nuisance: Nuisance = None) -> float:
        return float(sum(p.chi2(bg, nuisance) for p in self.parts))

    def breakdown(self, bg: Background, nuisance: Nuisance = None) -> dict[str, float]:
        """chi^2 of each component, for the tables in the paper."""
        return {p.name: p.chi2(bg, nuisance) for p in self.parts}

    def logL(self, bg: Background, nuisance: Nuisance = None) -> float:
        return -0.5 * self.chi2(bg, nuisance)

    def can_simulate(self) -> bool:
        return all(hasattr(p, "simulate") for p in self.parts)

    def simulate(self, bg: Background, rng) -> None:
        """Replace every component's data with a draw from the model at ``bg``.

        The components are independent by construction -- that is the premise
        of adding their chi-squares -- so drawing each separately is the
        correct joint draw. A component that cannot simulate makes the whole
        joint refuse, rather than silently leaving real data in place beside
        synthetic data, which would produce a statistic with no null
        distribution at all.
        """
        if not self.can_simulate():
            missing = [p.name for p in self.parts if not hasattr(p, "simulate")]
            raise NotImplementedError(
                f"these components cannot generate synthetic data: {missing}")
        for p in self.parts:
            p.simulate(bg, rng)

    def restore(self) -> None:
        for p in self.parts:
            if hasattr(p, "restore"):
                p.restore()
