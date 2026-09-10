"""The prior-narrowing identity used to report the Bayes factor's fragility.

Replacing AIC and BIC with the evidence trades an inapplicable parameter count
for an explicit dependence on the prior volume, and that dependence has to be
reported.  ``scripts/prior_sensitivity.py`` does it without re-sampling, using

    ln Z_B = ln Z_A + ln p_B + ln(|A| / |B|),

where ``p_B`` is the posterior mass inside the narrowed box under the original
prior.  The identity is exact, so it is checked against a case whose evidence
can be written down in closed form rather than against another estimate of
itself.
"""
# covers: tab:comparison
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py. A claim quoted in the abstract or the
#   conclusions with nothing testing it is what the ledger exists to find.

from __future__ import annotations

import numpy as np
from scipy.stats import norm


def _log_evidence(lo, hi, mu, sd):
    """Uniform prior on [lo, hi], Gaussian likelihood: exact log evidence."""
    mass = np.prod([norm.cdf(hi[i], mu[i], sd[i]) - norm.cdf(lo[i], mu[i], sd[i])
                    for i in range(len(mu))])
    return float(np.log(mass) - np.sum(np.log(np.asarray(hi) - np.asarray(lo))))


def test_narrowing_identity_matches_the_closed_form():
    mu = np.array([0.3, -0.2])
    sd = np.array([0.15, 0.4])
    a_lo, a_hi = np.array([-2.0, -3.0]), np.array([2.0, 3.0])
    b_lo, b_hi = np.array([-0.5, -1.0]), np.array([1.0, 1.5])

    ln_za = _log_evidence(a_lo, a_hi, mu, sd)
    ln_zb = _log_evidence(b_lo, b_hi, mu, sd)

    rng = np.random.default_rng(0)
    draws = np.column_stack([rng.normal(mu[i], sd[i], size=2_000_000)
                             for i in range(2)])
    draws = draws[np.all((draws >= a_lo) & (draws <= a_hi), axis=1)]
    p_b = float(np.mean(np.all((draws >= b_lo) & (draws <= b_hi), axis=1)))
    ln_volume = float(np.sum(np.log((a_hi - a_lo) / (b_hi - b_lo))))

    predicted = ln_za + np.log(p_b) + ln_volume
    # Monte Carlo error on p_b at this sample size is a few parts in 1e4
    assert abs(predicted - ln_zb) < 1e-3, (predicted, ln_zb)


def test_narrowing_reduces_the_penalty_when_the_likelihood_is_concentrated():
    """Shrinking a prior around a well-fitting region raises the evidence.

    This is the direction that matters for the paper: the Occam penalty the
    Bayes factor assigns to an extension is the prior volume the extension
    spends away from the null, so a reader who prefers a narrower prior gets a
    smaller penalty. The manuscript therefore reports the span, not a number.
    """
    mu, sd = np.array([0.0]), np.array([0.1])
    wide = _log_evidence(np.array([-5.0]), np.array([5.0]), mu, sd)
    narrow = _log_evidence(np.array([-1.0]), np.array([1.0]), mu, sd)
    assert narrow > wide
    # and by very nearly the log of the volume ratio, since the likelihood is
    # entirely contained in the narrow box
    assert abs((narrow - wide) - np.log(5.0)) < 1e-6
