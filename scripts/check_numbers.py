#!/usr/bin/env python3
"""Fail if the manuscript contains hand-typed numbers or stale macros.

Two checks:
1. Regenerating paper/generated/numbers.tex from results/results.json must
   reproduce the committed file byte for byte.
2. No decimal literal may appear in the prose of paper/sections/*.tex outside
   maths, a whitelisted context, or a generated macro.  Quoted results belong
   in results.json, not in the text.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "paper" / "sections"
NUMBERS = ROOT / "paper" / "generated" / "numbers.tex"
WHITELIST = ROOT / "docs" / "NUMBERS_WHITELIST.txt"

# strip maths, comments and verbatim before looking for literals
MATH = re.compile(r"\$[^$]*\$|\\\[.*?\\\]|\\begin\{(equation|align|aligned|gather|keyresult|array|cases|pmatrix|bmatrix)\*?\}.*?\\end\{\1\*?\}", re.S)
COMMENT = re.compile(r"(?<!\\)%.*")
COMMANDS = re.compile(r"\\(?:label|ref|cref|Cref|cite\w*|includegraphics|input|eqref|url|href)\s*(\[[^\]]*\])?\{[^}]*\}")
OPTS = re.compile(r"\[[^\]]*\]")
DECIMAL = re.compile(r"(?<![\w.])\d+\.\d+(?![\w.])")


def load_whitelist() -> set[str]:
    if not WHITELIST.exists():
        return set()
    return {ln.split("#")[0].strip() for ln in WHITELIST.read_text().splitlines()
            if ln.split("#")[0].strip()}


def main() -> int:
    failures: list[str] = []

    before = NUMBERS.read_text() if NUMBERS.exists() else None
    subprocess.run([sys.executable, str(ROOT / "scripts" / "gen_numbers.py")],
                   check=True, capture_output=True)
    after = NUMBERS.read_text() if NUMBERS.exists() else None
    if before is not None and before != after:
        failures.append(
            "paper/generated/numbers.tex is out of date with results/results.json "
            "(run `make tables` and commit the result)")

    allowed = load_whitelist()
    for tex in sorted(SECTIONS.glob("*.tex")):
        text = tex.read_text()
        text = COMMENT.sub("", text)
        text = MATH.sub(" ", text)
        text = COMMANDS.sub(" ", text)
        text = OPTS.sub(" ", text)
        for m in DECIMAL.finditer(text):
            if m.group() in allowed:
                continue
            line = text[:m.start()].count("\n") + 1
            failures.append(f"{tex.relative_to(ROOT)}: hand-typed number "
                            f"{m.group()!r} in prose (near line {line})")

    if failures:
        print("check_numbers FAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    print("check_numbers: no hand-typed numbers, generated macros up to date")
    return 0


if __name__ == "__main__":
    sys.exit(main())
