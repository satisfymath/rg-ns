#!/usr/bin/env python3
"""Gate: every number in the manuscript must be reachable from `make`.

``gen_numbers.py`` turns a fixed list of results files into LaTeX macros, and
the manuscript quotes those macros. For the manuscript to be reproducible it is
not enough that the files exist: some script must produce each of them, and
that script must be reachable from a documented target, or a reader following
``README_REPRODUCE.md`` ends up with a tree that cannot regenerate what the
paper says.

This is not hypothetical. ``results/growth_comparison.json`` supplied three
numbers to section 10 --- including the Bayes factor with growth data, which is
the manuscript's answer to "your sharpest prediction is untested" --- and had
no producer at all: it had been written by hand during the analysis. Two other
files had producers that no target ran.

The check is deliberately crude. It looks for the file name in the text of each
script and for the script name in the Makefile. A script that writes a file
whose name it never mentions will slip through; nothing here has that shape,
and the alternative is to execute the pipeline, which is what the gate exists
to avoid.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

#: Written by hand and committed, not produced by a script. Each entry needs a
#: reason, and "it is inconvenient to generate" is not one.
BY_HAND = {
    "map_reference.json": "the frozen brute-force maximisation, kept precisely "
                          "so that it is not regenerated",
}


def main() -> int:
    gen = (SCRIPTS / "gen_numbers.py").read_text()
    sources = sorted(set(re.findall(r'"results" / "([a-z_0-9]+\.json)"', gen)))
    makefile = (ROOT / "Makefile").read_text()

    bad = []
    for name in sources:
        if name in BY_HAND:
            print(f"  {name:32s} by hand: {BY_HAND[name]}")
            continue
        producers = []
        for f in sorted(SCRIPTS.glob("*.py")):
            if f.name in ("gen_numbers.py", "check_reproducible.py",
                          "provenance.py"):
                continue                     # read it, do not produce it
            text = f.read_text()
            if f'"{name}"' in text and ("write_text" in text or "json.dump" in text):
                producers.append(f.name)
        reachable = [p for p in producers if p in makefile]
        if not producers:
            bad.append(f"{name}: no script produces it")
        elif not reachable:
            bad.append(f"{name}: produced by {', '.join(producers)}, none of "
                       f"which any Makefile target runs")
        else:
            print(f"  {name:32s} <- {', '.join(reachable)}")

    if bad:
        print("\ncheck_reproducible: FAILED")
        for line in bad:
            print(f"  - {line}")
        print("\nA number the paper quotes cannot be regenerated from a clean "
              "checkout. Add the producing script, and a Makefile target that "
              "runs it.")
        return 1
    print("check_reproducible: every quoted results file has a producer that "
          "`make` runs")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
