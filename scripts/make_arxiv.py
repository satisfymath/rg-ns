#!/usr/bin/env python3
"""Build the arXiv submission bundle.

arXiv does not run biber, so the bundle ships a pre-built .bbl.  The sources
are flattened into one main.tex because a submission with \\input from
subdirectories is fragile, and the result is test-compiled in a clean
directory with pdflatex alone before being archived.
"""
from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / "paper"
OUT = ROOT / "build" / "arxiv"

INPUT_RE = re.compile(r"^\s*\\input\{([^}]+)\}\s*$", re.M)


def flatten(text: str, base: Path, depth: int = 0) -> str:
    """Recursively inline \\input directives."""
    if depth > 6:                                              # pragma: no cover
        raise RuntimeError("\\input nesting too deep")

    def repl(m: re.Match) -> str:
        name = m.group(1)
        path = base / (name if name.endswith(".tex") else name + ".tex")
        if not path.exists():
            raise FileNotFoundError(path)
        body = path.read_text()
        return (f"% ==== begin {name} ====\n"
                + flatten(body, base, depth + 1)
                + f"\n% ==== end {name} ====")

    return INPUT_RE.sub(repl, text)


def main() -> int:
    build = PAPER / "build"
    bbl = build / "main.bbl"
    if not bbl.exists():
        print("build/main.bbl not found; run `make pdf` first")
        return 1

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    main_tex = flatten((PAPER / "main.tex").read_text(), PAPER)
    # arXiv compiles with the bbl in place; drop the biber resource line
    main_tex = main_tex.replace(r"\addbibresource{references.bib}",
                                "% bibliography is shipped as main.bbl")
    (OUT / "main.tex").write_text(main_tex)
    shutil.copy(bbl, OUT / "main.bbl")

    figs = OUT / "figures"
    figs.mkdir()
    n_fig = 0
    for pdf in sorted((PAPER / "figures").glob("*.pdf")):
        shutil.copy(pdf, figs / pdf.name)
        n_fig += 1

    # test-compile in a scratch directory with pdflatex alone
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        shutil.copytree(OUT, tmp / "src")
        for _ in range(2):
            r = subprocess.run(
                ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                 "main.tex"],
                cwd=tmp / "src", capture_output=True, text=True)
        if not (tmp / "src" / "main.pdf").exists():
            tail = "\n".join(r.stdout.splitlines()[-25:])
            print("arXiv bundle failed to compile:\n" + tail)
            return 1
        pages = subprocess.run(["pdfinfo", "main.pdf"], cwd=tmp / "src",
                               capture_output=True, text=True).stdout
        pages = next((l.split()[-1] for l in pages.splitlines()
                      if l.startswith("Pages")), "?")

    archive = ROOT / "build" / "arxiv_submission.zip"
    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(OUT.rglob("*")):
            if path.is_file():
                zf.write(path, path.relative_to(OUT))

    size = archive.stat().st_size / 1024
    print(f"arXiv bundle: {archive.relative_to(ROOT)} "
          f"({size:.0f} kB, {n_fig} figures, compiles to {pages} pages)")
    print("Checklist before uploading:")
    print("  - set \\draftfigsfalse in preamble.tex")
    print("  - remove every \\TODO (author email, ORCID, Zenodo DOI)")
    print("  - primary category astro-ph.CO, cross-list gr-qc")
    return 0


if __name__ == "__main__":
    sys.exit(main())
