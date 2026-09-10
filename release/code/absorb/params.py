"""Model registry: sampled parameters, priors and nested-model definitions.

Every model shares the same core reduced densities (omega_b, omega_c,
omega_V_act) so that priors are commensurate across the nested comparison.
The Hubble constant is *derived*, h^2 = E^2(N=0), which removes the need for a
shooting step: one background solve per likelihood call.

Nesting structure (each row adds parameters to the row above):

    lcdm      omega_b, omega_c, omega_V                            3
    wcdm      + w                                                  4
    w0wa      + w_a                                                5
    xi_h      + eps, log10_xi, z_act        (Gamma = xi H)         6
    reinforce + alpha_tot                   (beta = 0)             7
    memory    + r_beta, log10_tau                                  9
    track_b   + log10_gamma_down                                  10

`eps = 0` collapses every absorption model to LambdaCDM exactly, which is the
nested point used for the Savage-Dickey density ratio.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Sequence

import numpy as np

from .background import Background, BackgroundParams


@dataclass(frozen=True)
class Prior:
    """A uniform prior on one sampled parameter."""

    name: str
    low: float
    high: float
    latex: str

    def sample(self, rng: np.random.Generator, size: int | None = None):
        return rng.uniform(self.low, self.high, size)

    def contains(self, x: float) -> bool:
        return self.low <= x <= self.high

    def unit_to_value(self, u: float) -> float:
        """Map [0,1] -> prior range (for nested sampling)."""
        return self.low + u * (self.high - self.low)


# --- the full prior catalogue ------------------------------------------------
PRIORS: dict[str, Prior] = {
    "omega_b":          Prior("omega_b", 0.019, 0.026, r"\omega_b"),
    "omega_c":          Prior("omega_c", 0.05, 0.25, r"\omega_c"),
    "omega_V_act":      Prior("omega_V_act", 0.0, 1.5, r"\omega_{V,\rm act}"),
    "eps":              Prior("eps", 0.0, 1.0, r"\epsilon"),
    "log10_gamma0":     Prior("log10_gamma0", -2.0, 2.0, r"\log_{10}(\Gamma_0/H_{100})"),
    "log10_xi":         Prior("log10_xi", -3.0, 1.0, r"\log_{10}\xi"),
    "alpha_tot":        Prior("alpha_tot", 0.0, 8.0, r"\alpha+\beta"),
    "r_beta":           Prior("r_beta", 0.0, 1.0, r"\beta/(\alpha+\beta)"),
    "log10_tau":        Prior("log10_tau", -2.0, 1.0, r"\log_{10}(\tau_M H_{100})"),
    "z_act":            Prior("z_act", 0.3, 30.0, r"z_{\rm act}"),
    "log10_gamma_down": Prior("log10_gamma_down", -3.0, 1.0,
                              r"\log_{10}(\Gamma_\downarrow/H_{100})"),
    # dark-energy parametrizations used for comparison only
    "w0":               Prior("w0", -2.0, -0.3, r"w_0"),
    "wa":               Prior("wa", -3.0, 2.0, r"w_a"),
    # nuisance
    "sigma8":           Prior("sigma8", 0.5, 1.2, r"\sigma_8"),
}


@dataclass(frozen=True)
class Model:
    """A named model: its sampled parameters and how they build a background."""

    name: str
    params: tuple[str, ...]
    builder: Callable[[dict[str, float]], Background]
    description: str

    @property
    def ndim(self) -> int:
        return len(self.params)

    def priors(self) -> list[Prior]:
        return [PRIORS[p] for p in self.params]

    def labels(self) -> list[str]:
        return [PRIORS[p].latex for p in self.params]

    def to_dict(self, theta: Sequence[float]) -> dict[str, float]:
        return dict(zip(self.params, np.asarray(theta, dtype=float)))

    def log_prior(self, theta: Sequence[float]) -> float:
        for p, v in zip(self.priors(), theta):
            if not p.contains(v):
                return -np.inf
        return 0.0

    def prior_transform(self, u: np.ndarray) -> np.ndarray:
        """Unit hypercube -> parameter values, for nested sampling."""
        return np.array([p.unit_to_value(ui) for p, ui in zip(self.priors(), u)])


# --- builders ----------------------------------------------------------------
def _build_lcdm(d: dict[str, float]) -> Background:
    return Background(BackgroundParams(
        omega_b=d["omega_b"], omega_c=d["omega_c"],
        omega_V_act=d["omega_V_act"], eps=0.0))


def _build_absorption(d: dict[str, float], *, memory: bool, track_b: bool) -> Background:
    return Background(BackgroundParams(
        omega_b=d["omega_b"], omega_c=d["omega_c"],
        omega_V_act=d["omega_V_act"], eps=d["eps"],
        log10_gamma0=d["log10_gamma0"],
        alpha_tot=d.get("alpha_tot", 0.0),
        r_beta=d.get("r_beta", 0.0) if memory else 0.0,
        log10_tau=d.get("log10_tau", -0.5),
        z_act=d["z_act"], p_act=6.0,
        log10_gamma_down=d.get("log10_gamma_down") if track_b else None,
        switch="smooth"))


def _build_xi_h(d: dict[str, float]) -> Background:
    """Gamma = xi H family.  Implemented by noting that Gamma/H = xi is a
    constant multiple of the expansion rate, which the general solver
    reproduces when Gamma_0 is scaled by the instantaneous E; here we integrate
    it directly through a dedicated parameter mapping."""
    return Background(BackgroundParams(
        omega_b=d["omega_b"], omega_c=d["omega_c"],
        omega_V_act=d["omega_V_act"], eps=d["eps"],
        log10_gamma0=d["log10_xi"], alpha_tot=0.0, r_beta=0.0,
        z_act=d["z_act"], p_act=6.0, switch="smooth", rate_tracks_H=True))


MODELS: dict[str, Model] = {
    "xi_h": Model(
        "xi_h",
        ("omega_b", "omega_c", "omega_V_act", "eps", "log10_xi", "z_act"),
        _build_xi_h,
        "Analytically solvable benchmark with Gamma = xi H (draft Sec. 8)."),
    "lcdm": Model(
        "lcdm", ("omega_b", "omega_c", "omega_V_act"), _build_lcdm,
        "Flat LambdaCDM: the eps -> 0 limit of every absorption model."),
    "reinforce": Model(
        "reinforce",
        ("omega_b", "omega_c", "omega_V_act", "eps", "log10_gamma0",
         "alpha_tot", "z_act"),
        lambda d: _build_absorption(d, memory=False, track_b=False),
        "Self-reinforced absorption without memory (beta = 0)."),
    "memory": Model(
        "memory",
        ("omega_b", "omega_c", "omega_V_act", "eps", "log10_gamma0",
         "alpha_tot", "r_beta", "log10_tau", "z_act"),
        lambda d: _build_absorption(d, memory=True, track_b=False),
        "Full model: self-reinforcement with a causal memory variable."),
    "track_b": Model(
        "track_b",
        ("omega_b", "omega_c", "omega_V_act", "eps", "log10_gamma0",
         "alpha_tot", "r_beta", "log10_tau", "z_act", "log10_gamma_down"),
        lambda d: _build_absorption(d, memory=True, track_b=True),
        "As `memory`, plus the reverse vacuum -> defect channel."),
}


def build(model: str, theta: Sequence[float]) -> Background:
    m = MODELS[model]
    return m.builder(m.to_dict(theta))
