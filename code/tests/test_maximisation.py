"""The fast maximisation protocol must not lose ground against the slow one.

# covers: (methodology only; supports the chi-square column of tab:comparison)

History, because it is the reason this file exists. Three protocols have been
used. A small per-dimension budget from a few random starts returned 1435.807
where the maximum is near 1434.88. Forty full Nelder-Mead runs from uniform
prior draws found it but took 8.4 hours for five models. A screened protocol
now does it in minutes.

The first attempt to validate the screened protocol against the slow one
compared the slow answer with itself: the validation run crashed in a print
statement placed *before* the results were written, so the previous value
survived in the JSON and the comparison was vacuous. The reference values are
therefore frozen in ``results/map_reference.json`` and compared here, which is
a comparison that cannot silently degenerate in the same way.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
REFERENCE = ROOT / "results" / "map_reference.json"
CURRENT = ROOT / "results" / "map.json"

#: How much worse than the brute-force maximum the fast protocol may be.
#: The chi-square difference the model comparison turns on is about 1.6, so a
#: tolerance of 0.05 keeps the optimiser's error at a few per cent of it.
TOLERANCE = 0.05


def _load(path: Path) -> dict:
    if not path.exists():
        pytest.skip(f"{path.name} not present")
    return json.loads(path.read_text())


@pytest.mark.parametrize("key", ["lcdm__baseline", "xi_h__baseline",
                                 "reinforce__baseline"])
def test_fast_protocol_matches_the_brute_force_reference(key):
    ref, cur = _load(REFERENCE), _load(CURRENT)
    if key not in ref or key not in cur:
        pytest.skip(f"{key} absent from one of the files")
    gap = cur[key]["chi2_min"] - ref[key]["chi2_min"]
    assert gap < TOLERANCE, (
        f"{key}: the screened protocol found {cur[key]['chi2_min']:.4f}, "
        f"which is {gap:+.4f} worse than the brute-force reference "
        f"{ref[key]['chi2_min']:.4f}. Either raise --restarts/--screen or "
        f"report the maximisation error alongside the chi-square difference.")


def test_reference_is_not_the_same_file_as_the_current_results():
    """Guard against the comparison degenerating into self-comparison again."""
    assert REFERENCE.name != CURRENT.name
    ref = _load(REFERENCE)
    assert all(v.get("protocol", "").startswith("brute force") for v in ref.values())


@pytest.mark.parametrize("larger,smaller", [
    ("xi_h", "lcdm"),
    ("reinforce", "lcdm"),
    ("memory", "reinforce"),
    ("track_b", "memory"),
])
def test_a_model_never_fits_worse_than_one_it_contains(larger, smaller):
    """Nesting is exact, so the chi-square column must be monotone in it.

    It was not. The nine-parameter model's search returned a chi-square 1.55
    *worse* than the seven-parameter model it contains, which is impossible:
    evaluating the larger model at the smaller one's best fit reproduces the
    smaller one's value exactly. The larger search had simply failed to find
    it, and the number was on its way into the comparison table.

    The maximiser now seeds each search with every submodel's answer embedded,
    which makes this property hold by construction rather than by luck. This
    test is what notices if that stops working.
    """
    cur = _load(CURRENT)
    a, b = f"{larger}__baseline", f"{smaller}__baseline"
    if a not in cur or b not in cur:
        pytest.skip("one of the models has not been run")
    assert cur[a]["chi2_min"] <= cur[b]["chi2_min"] + 1e-6, (
        f"{larger} ({cur[a]['chi2_min']:.4f}) fits worse than {smaller} "
        f"({cur[b]['chi2_min']:.4f}), which it contains as a submodel; the "
        f"larger maximisation has failed")
