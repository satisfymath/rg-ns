"""The two limits the manuscript quotes must remain the kind of thing a limit is.

# covers: eq:observations-deficit-limit, eq:observations-jerk-limit
#   Machine-readable link from tests to the claims they cover, read by
#   scripts/claim_ledger.py.

These are pipeline outputs rather than analytic results, so what a test can do
is guard the properties that make them meaningful. Both were, at one point, not
meaningful: the deficit limit was read off a profile whose grid points missed
their targets by up to a factor of three and whose Delta chi-square ran 0.09,
298, 22, 127, and the jerk limit was a NaN that LaTeX typeset as the word.

The checks below are exactly the conditions that failure violated.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

RESULTS = Path(__file__).resolve().parents[2] / "results" / "profile.json"
THRESHOLD = 2.71          # one-sided 95% for one parameter of interest


def _profile(key: str) -> dict:
    if not RESULTS.exists():
        pytest.skip("results/profile.json not present")
    data = json.loads(RESULTS.read_text())
    if key not in data:
        pytest.skip(f"{key} not in profile.json")
    return data[key]


@pytest.mark.parametrize("key", ["xi_h__baseline__matter_deficit",
                                 "xi_h__baseline__jerk_excess"])
def test_profile_actually_imposed_its_constraint(key):
    """Every grid point must have reached the value it was profiling at."""
    p = _profile(key)
    assert p["max_target_miss_rel"] < 1e-6, (
        f"{key}: worst grid point missed its target by "
        f"{p['max_target_miss_rel']:.3g} relative; the constraint is not being "
        f"imposed and the curve is not a profile")


@pytest.mark.parametrize("key", ["xi_h__baseline__matter_deficit",
                                 "xi_h__baseline__jerk_excess"])
def test_profile_is_monotone_above_its_minimum(key):
    """A profile that goes down after going up means the optimiser failed."""
    p = _profile(key)
    assert p["n_non_monotone_steps"] == 0, (
        f"{key}: {p['n_non_monotone_steps']} decreasing steps above the "
        f"minimum; each grid point is maximising a different function")


@pytest.mark.parametrize("key", ["xi_h__baseline__matter_deficit",
                                 "xi_h__baseline__jerk_excess"])
def test_quoted_limit_is_a_real_crossing_not_a_grid_endpoint(key):
    """The limit must be interior, and the profile must actually cross 2.71."""
    p = _profile(key)
    assert not p["unbounded"], f"{key}: no crossing, so no limit exists to quote"
    limit = p["limit_95"]
    assert np.isfinite(limit), f"{key}: limit is {limit}"
    targets = np.asarray(p["targets"])
    assert targets[0] < limit < targets[-1], (
        f"{key}: limit {limit} is not interior to the grid "
        f"[{targets[0]}, {targets[-1]}] -- an endpoint is not a limit")
    assert p["max_delta_chi2"] > THRESHOLD, (
        f"{key}: profile only reaches {p['max_delta_chi2']:.3f}, below the "
        f"{THRESHOLD} threshold it is supposed to cross")


def test_the_deficit_limit_is_the_value_the_manuscript_quotes():
    """Regression on the published number itself.

    Loose enough to survive a re-run of the optimiser, tight enough to fail if
    the profile changes character.
    """
    p = _profile("xi_h__baseline__matter_deficit")
    assert p["limit_95"] == pytest.approx(0.0101, rel=0.10)


def test_the_jerk_limit_is_the_value_the_manuscript_quotes():
    """Regression on the published number, with its one deliberate change.

    The pin was 0.0306 and this test caught its change, which is the test
    working rather than failing. The grid it came from ran from 1e-4 to 0.16
    while the unconstrained maximum sits at a jerk excess of 1.4e-8, so the
    profile never sampled the region containing its own minimum and measured
    every Delta chi-square from a floor 0.93 too high. Widening the grid to
    nine decades moves the limit to 0.0273 -- tighter, because the rise is now
    measured from the true floor.

    The pin is updated, not loosened: the tolerance is the same ten per cent.
    """
    p = _profile("xi_h__baseline__jerk_excess")
    assert p["limit_95"] == pytest.approx(0.0273, rel=0.10)


def test_no_number_is_quoted_for_a_parameter_the_data_do_not_constrain():
    """A prior-dominated parameter must not appear in the table as a number.

    The manuscript says in as many words that the upper limit on the
    convertible fraction is withdrawn, because the rate can always be sent to
    zero and Lambda-CDM recovered at any value of it. The generated table went
    on printing ``< 0.83 (95%)`` beside that paragraph, which is the 95th
    percentile of the prior and not a measurement. Four of the nine sampled
    parameters were in the same position.

    The criterion is the chain-stability gate's: the 5--95 span as a fraction
    of the prior width. This test reads the published table and checks that
    every parameter above that threshold carries the word "unconstrained"
    rather than digits.
    """
    import importlib.util
    import re

    root = Path(__file__).resolve().parents[2]
    table = root / "paper" / "generated" / "tab_parameters.tex"
    results = root / "results" / "results.json"
    if not table.exists() or not results.exists():
        pytest.skip("generated table or results.json not present")

    spec = importlib.util.spec_from_file_location(
        "_gt", root / "scripts" / "gen_tables.py")
    gt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gt)

    chains = json.loads(results.read_text()).get("chains", {})
    key = "memory__baseline"
    if key not in chains:
        pytest.skip("the full model's posterior is not present")

    text = table.read_text()
    rows = {}
    for line in text.splitlines():
        if "&" in line and line.rstrip().endswith(r"\\"):
            label, _, rest = line.partition("&")
            rows[label.strip()] = rest

    threshold = gt._prior_fill_max()
    checked = 0
    for name, entry in chains[key]["parameters"].items():
        fill = gt.prior_fill("memory", name, entry)
        if fill is None or fill <= threshold:
            continue
        checked += 1
        label = gt.PARAM_LABEL.get(name, name)
        row = rows.get(label)
        assert row is not None, f"{name}: no row for {label} in the table"
        assert "unconstrained" in row, (
            f"{name} fills {fill:.0%} of its prior, above the {threshold:.0%} "
            f"threshold the chain-stability gate uses, yet the table quotes "
            f"{row.strip()}. A number there is the prior's, not the data's.")
        assert not re.search(r"\d+\.\d", row.split("&")[0]), (
            f"{name}: the posterior cell still carries digits: {row}")
    assert checked >= 1, (
        "no prior-dominated parameter was found to check; either the "
        "posterior changed or the fill computation is not working")
