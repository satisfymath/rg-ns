#!/usr/bin/env python3
"""Fail on LaTeX warnings that indicate a real defect in the manuscript."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "paper" / "build" / "main.log"
BLG = ROOT / "paper" / "build" / "main.blg"

FATAL = [
    (re.compile(r"LaTeX Warning: (Reference|Citation) `([^']+)' on page .* undefined"),
     "undefined reference or citation"),
    (re.compile(r"LaTeX Warning: Label `([^']+)' multiply defined"),
     "duplicate label"),
    (re.compile(r"Package biblatex Warning: The following entry could not be found"),
     "missing bibliography entry"),
    # pdflatex reports errors two ways.  Without -file-line-error they begin
    # with "! "; with it (which this build uses) they are "file:line: message"
    # and carry no exclamation mark at all.  Missing the second form let ten
    # undefined control sequences through a "clean" report once.
    (re.compile(r"^! ", re.M), "LaTeX error"),
    (re.compile(r"^[^\s:]+\.\w+:\d+: (?!LaTeX Warning)(.+)$", re.M),
     "LaTeX error (file:line form)"),
    (re.compile(r"Undefined control sequence", re.M), "undefined control sequence"),
    (re.compile(r"Missing \\?\$ inserted", re.M), "math-mode error"),
]
OVERFULL = re.compile(r"Overfull \\hbox \(([\d.]+)pt too wide\)")
MAX_BAD_BOXES = 5
BAD_BOX_PT = 10.0


def main() -> int:
    if not LOG.exists():
        print(f"{LOG} not found; run `make pdf` first")
        return 1
    text = LOG.read_text(errors="replace")
    failures: list[str] = []

    for pattern, label in FATAL:
        for m in pattern.finditer(text):
            failures.append(f"{label}: {m.group(0).strip()[:120]}")

    bad = [float(m.group(1)) for m in OVERFULL.finditer(text)
           if float(m.group(1)) > BAD_BOX_PT]
    if len(bad) > MAX_BAD_BOXES:
        failures.append(f"{len(bad)} overfull hboxes wider than {BAD_BOX_PT}pt "
                        f"(limit {MAX_BAD_BOXES})")

    if BLG.exists():
        blg = BLG.read_text(errors="replace")
        for m in re.finditer(r"^WARN - (.*)$", blg, re.M):
            failures.append("biber: " + m.group(1).strip())

    if failures:
        print("check_log FAILED:")
        for f in dict.fromkeys(failures):
            print("  - " + f)
        return 1
    print(f"check_log: clean ({len(bad)} tolerated overfull boxes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
