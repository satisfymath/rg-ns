#!/usr/bin/env python3
"""Fail if the manuscript contains hand-typed numbers or stale macros.

Three checks:
1. Regenerating paper/generated/numbers.tex from every results file registered
   in gen_numbers.SOURCES must reproduce the committed file byte for byte.
2. No decimal literal may appear in the prose of paper/sections/*.tex outside
   maths, a whitelisted context, or a generated macro.  Quoted results belong
   in a results file, not in the text.
3. Every ``\num...`` macro the sections use must be defined by the generator.
   Check 1 cannot catch an *invented* macro name: a subsection once quoted
   seven \numPancake... macros that existed nowhere, from a results file no
   script read, one of them for a quantity that had never been computed.  The
   document still compiled, because latexmk was running in force mode.
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

    defined = set(re.findall(r"\\newcommand\{\\(num[A-Za-z]+)\}",
                             after or ""))
    used: dict[str, str] = {}
    for tex in sorted(SECTIONS.glob("*.tex")):
        for m in re.finditer(r"\\(num[A-Za-z]+)\b", tex.read_text()):
            used.setdefault(m.group(1), str(tex.relative_to(ROOT)))
    for name, where in sorted(used.items()):
        if name not in defined:
            failures.append(f"{where}: \\{name} is used but no results file "
                            f"defines it (invented macro name, or a results "
                            f"file missing from gen_numbers.SOURCES)")

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
