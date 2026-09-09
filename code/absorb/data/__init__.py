"""Observational data sets used in the cosmological fits.

Each submodule owns one probe, exposes a frozen dataclass holding plain NumPy
arrays, and caches the parsed product at module level so that repeated
likelihood calls never touch the disk.  Raw files live outside the package
(``<repo>/data/raw``) and are never modified; the location can be overridden
with the ``ABSORB_DATA_DIR`` environment variable.
"""
from __future__ import annotations

from .cc import CosmicChronometers, load_cc
from .desi import BAOData, load_desi
from .pantheon import PantheonData, load_pantheon
from .paths import RAW_DIR, raw_path
from .planck_priors import PlanckPriors, load_planck_priors
from .rsd import FSBAOData, load_rsd

__all__ = [
    "RAW_DIR",
    "raw_path",
    "PantheonData",
    "load_pantheon",
    "BAOData",
    "load_desi",
    "CosmicChronometers",
    "load_cc",
    "FSBAOData",
    "load_rsd",
    "PlanckPriors",
    "load_planck_priors",
]
