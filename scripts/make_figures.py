#!/usr/bin/env python3
"""Regenerate every figure in the paper from results/.

Figures that depend on a chain which has not been run are skipped with a
message rather than failing, so the document can be built at any stage of the
analysis; scripts/check_figures.py is what refuses to ship a paper whose
figures are missing.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "code"))

from absorb.plotting import setup_style                        # noqa: E402
from absorb.plotting import fig_cosmo, fig_sims                # noqa: E402


def main() -> int:
    setup_style()
    made, skipped = [], []
    for module in (fig_sims, fig_cosmo):
        for fn in module.ALL:
            try:
                path = fn()
            except FileNotFoundError as exc:
                skipped.append(f"{fn.__name__} (missing input: {exc})")
                continue
            if path is None:
                skipped.append(f"{fn.__name__} (chain not available)")
            else:
                made.append(path.name)
                print(f"  {path.name}")
    print(f"\n{len(made)} figure(s) written, {len(skipped)} skipped")
    for s in skipped:
        print(f"  skipped: {s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
