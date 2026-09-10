#!/usr/bin/env python3
"""Editorial artefacts that survive a compile: duplicated lines and words.

A line-level edit that inserts without deleting leaves an exact duplicate line,
which LaTeX sets happily as a repeated sentence. One reached the manuscript
this way. A duplicated word ("the the") does the same at smaller scale. Neither
is caught by any other gate, because both are perfectly valid LaTeX.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "paper" / "sections"

#: Short or structural lines repeat legitimately.
MIN_LEN = 25
STRUCTURAL = re.compile(r"^\s*(\\(begin|end|item|midrule|toprule|bottomrule|"
                        r"hline|\\)|%|\$\$|&)")
DUP_WORD = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
#: Words that legitimately repeat in mathematics or prose.
DUP_OK = {"that", "had", "has", "very"}


def main() -> int:
    failures: list[str] = []
    for tex in sorted(SECTIONS.glob("*.tex")):
        lines = tex.read_text().split("\n")
        rel = tex.relative_to(ROOT)
        for i in range(1, len(lines)):
            a, b = lines[i - 1].strip(), lines[i].strip()
            if (a == b and len(a) >= MIN_LEN and not STRUCTURAL.match(a)):
                failures.append(f"{rel}:{i + 1}: line duplicated verbatim: "
                                f"{a[:60]!r}")
        text = "\n".join(lines)
        # Replace maths with a token rather than a space: blanking it makes
        # "X and Y and using" read as "and and", which is not a repeat.
        text = re.sub(r"\$[^$]*\$", " MATH ", text)
        text = re.sub(r"(?<!\\)%.*", " ", text)         # and comments
        for m in DUP_WORD.finditer(text):
            word = m.group(1).lower()
            if word in DUP_OK or len(word) < 3 or word.isdigit():
                continue
            line = text[:m.start()].count("\n") + 1
            failures.append(f"{rel}:{line}: word repeated: {m.group(0)!r}")

    if failures:
        print("check_prose FAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    print("check_prose: no duplicated lines or words")
    return 0


if __name__ == "__main__":
    sys.exit(main())
