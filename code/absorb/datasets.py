"""Named data-set combinations used in the paper.

`baseline` is the headline combination.  The others exist to answer specific
questions a referee will ask: what the late-time data say on their own
(`nocmb`), what happens when the SH0ES calibration is included (`shoes`), and
whether growth is consistent with the geometry (`rsd`).
"""
from __future__ import annotations

from typing import Callable

from .growth import Growth
from .likelihoods import (ChronometerLikelihood, DesiBAOLikelihood,
                          JointLikelihood, PantheonLikelihood,
                          PlanckPriorLikelihood, RSDLikelihood)

SIGMA8_FIDUCIAL = 0.8111     # Planck 2018 TT,TE,EE+lowE+lensing


def _fs8(sigma8: float = SIGMA8_FIDUCIAL) -> Callable:
    """f sigma_8 predictor wired to the linear growth solver.

    sigma_8 is held at its Planck value rather than marginalised: the point of
    including growth here is to test whether the geometry-preferred parameters
    are compatible with structure formation, and letting sigma_8 float would
    absorb precisely the effect being tested.  The consequence -- that the
    evidence for the "+growth" combination is conditional on this value -- is
    stated in the numerics appendix. The marginalised variant has not been
    run; an earlier version of this docstring said Section 10 reported both,
    and it did not.
    """
    return lambda bg, z: Growth(bg).f_sigma8(z, sigma8)


def build(name: str) -> JointLikelihood:
    """Return the named likelihood combination."""
    sn = PantheonLikelihood()
    sn_shoes = PantheonLikelihood(with_shoes=True)
    bao = DesiBAOLikelihood()
    cc = ChronometerLikelihood()
    # The cosmic-chronometer covariance has two published variants. The one
    # used by default adds the IMF and the "model, odd one out" terms to the
    # statistical errors; the conservative one adds the stellar library and the
    # full model term as well, which doubles the effective error on a coherent
    # offset in H(z), from 5.7% to 11.6%. Carrying both lets the dependence on
    # that choice be measured rather than assumed away.
    cc_cons = ChronometerLikelihood(variant="conservative")
    cmb = PlanckPriorLikelihood()

    combos = {
        "baseline": [sn, bao, cc, cmb],
        "shoes":    [sn_shoes, bao, cc, cmb],
        "nocmb":    [sn, bao, cc],
        "rsd":      [sn, bao, cc, cmb, RSDLikelihood(fs8_model=_fs8())],
        "bao_only": [bao, cmb],
        "baseline_cc_cons": [sn, bao, cc_cons, cmb],
    }
    if name not in combos:
        raise KeyError(f"unknown dataset {name!r}; have {sorted(combos)}")
    return JointLikelihood(combos[name], name=name)


DATASETS = ("baseline", "shoes", "nocmb", "rsd", "bao_only",
            "baseline_cc_cons")
