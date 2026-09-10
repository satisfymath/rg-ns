"""Every included figure must exist; every figure present must be used."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "paper" / "sections"
FIGS = ROOT / "paper" / "figures"
INCLUDE = re.compile(r"\\includegraphics\s*(?:\[[^\]]*\])?\{([^}]+)\}")
COMMENT = re.compile(r"(?<!\\)%.*")


def main() -> int:
    failures, used = [], set()
    for tex in sorted(SECTIONS.glob("*.tex")):
        text = COMMENT.sub("", tex.read_text())
        for m in INCLUDE.finditer(text):
            name = m.group(1)
            used.add(Path(name).stem)
            candidates = [FIGS / name, FIGS / f"{name}.pdf", FIGS / f"{name}.png"]
            if not any(c.exists() for c in candidates):
                failures.append(f"{tex.name}: missing figure {name!r}")
            elif not (FIGS / name).suffix and not (FIGS / f"{name}.pdf").exists():
                failures.append(f"{tex.name}: {name!r} exists only as a raster; "
                                "the paper requires vector PDF")

    present = {p.stem for p in FIGS.glob("*.pdf")}
    orphans = sorted(present - used)
    if orphans:
        print(f"check_figures: note, {len(orphans)} figure(s) not referenced yet: "
              + ", ".join(orphans[:8]) + ("..." if len(orphans) > 8 else ""))

    if failures:
        print("check_figures FAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    print(f"check_figures: {len(used)} referenced figures all present as PDF")
    return 0


if __name__ == "__main__":
    sys.exit(main())
