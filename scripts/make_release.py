#!/usr/bin/env python3
"""Assemble the deposit archive, and refuse to build a broken one.

What goes in is what a reader needs to check the paper: sources, figures,
generated macros and tables, the machine-readable results, the referee reports,
the claim ledger and the reproduction instructions. What stays out is anything
large, machine-specific or private.

The refusals matter more than the copying. The archive will not be built while
the manuscript carries a placeholder for the author's metadata or the Zenodo
DOI, nor while a generated table is missing its input, because an archive is
the one artifact that cannot be quietly corrected after the fact.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release"

INCLUDE_FILES = [
    "Makefile", "requirements.txt", "README.md", "README_REPRODUCE.md",
    # The licence and the citation metadata belong in the deposit itself. A
    # record that declares MIT while the archive contains no licence text
    # leaves a user with no grant, and one with no CITATION.cff makes the
    # reader reconstruct by hand how to cite it.
    "LICENSE", "CITATION.cff", ".zenodo.json",
    "docs/CLAIM_LEDGER.md", "docs/FINAL_READINESS.md",
    "docs/NEEDS_DAVID.md", "docs/BIB_VERIFICATION.md",
    "data/SHA256SUMS",
    # The built manuscript. It lives under paper/build/, which the tree walk
    # skips as a build directory, so it has to be named. A deposit that backs
    # a paper's reproducibility claim should contain the paper.
    "paper/build/main.pdf",
]
INCLUDE_TREES = [
    ("paper", {".tex", ".bib", ".pdf"}),
    ("paper/figures", {".pdf", ".png"}),
    ("paper/generated", {".tex"}),
    ("code", {".py", ".toml"}),
    ("scripts", {".py"}),
    ("results", {".json"}),
    ("docs/review", {".md"}),
    ("docs/theory", {".md"}),
]
EXCLUDE_DIRS = {"build", "__pycache__", ".git", "chains", "posteriors",
                "sims", "raw", ".pytest_cache"}
#: Strings that must not appear in any shipped .tex file.
FORBIDDEN = (r"\TODO{", r"\CITE", "[TODO:", "FIXME", "XXX", "[missing:")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def blockers() -> list[str]:
    out: list[str] = []
    for tex in sorted((ROOT / "paper").rglob("*.tex")):
        if any(part in EXCLUDE_DIRS for part in tex.parts):
            continue
        # Checked line by line, skipping the line that *defines* the \TODO
        # macro: the definition is fine, every use of it is a blocker.
        for lineno, line in enumerate(tex.read_text().splitlines(), 1):
            if "newcommand" in line or line.lstrip().startswith("%"):
                continue
            for token in FORBIDDEN:
                if token in line:
                    out.append(f"{tex.relative_to(ROOT)}:{lineno} contains "
                               f"{token!r}")
                    break
    for gen in sorted((ROOT / "paper" / "generated").glob("*.tex")):
        if "[missing:" in gen.read_text():
            out.append(f"{gen.relative_to(ROOT)} is missing its results input")
    if not (ROOT / "results" / "provenance.json").exists():
        out.append("results/provenance.json absent (run `make provenance`)")
    return out


def copy_into(dest: Path) -> int:
    n = 0
    for rel in INCLUDE_FILES:
        src = ROOT / rel
        if src.exists():
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest / rel)
            n += 1
    for tree, suffixes in INCLUDE_TREES:
        base = ROOT / tree
        if not base.exists():
            continue
        for src in sorted(base.rglob("*")):
            if not src.is_file() or src.suffix not in suffixes:
                continue
            if any(part in EXCLUDE_DIRS for part in src.relative_to(ROOT).parts):
                continue
            target = dest / src.relative_to(ROOT)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, target)
            n += 1
    return n


METADATA_FILES = (".zenodo.json", "CITATION.cff")


def metadata_placeholders(root) -> list[str]:
    """Placeholders in the deposit metadata, not just in the manuscript.

    The manuscript's TODOs are checked because they would be printed. These
    are checked because they would be *deposited*: a Zenodo record whose
    creator has "TODO-ORCID" where an identifier belongs is worse than no
    record, since it is permanent and public.
    """
    out = []
    for name in METADATA_FILES:
        path = root / name
        if not path.exists():
            out.append(f"{name} is missing")
            continue
        for i, line in enumerate(path.read_text().splitlines(), 1):
            if "TODO" in line:
                out.append(f"{name}:{i} contains a placeholder: {line.strip()}")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--force", action="store_true",
                    help="assemble even with blockers, for inspection only; "
                         "the archive is then marked DRAFT and not checksummed")
    args = ap.parse_args()

    found = blockers() + metadata_placeholders(ROOT)
    if found and not args.force:
        print("make_release refuses to build: the manuscript is not shippable")
        for b in found:
            print("  - " + b)
        print("\nRun with --force to assemble a DRAFT copy for inspection.")
        return 1

    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    n = copy_into(OUT)

    digests = {str(p.relative_to(OUT)): sha256(p)
               for p in sorted(OUT.rglob("*")) if p.is_file()}
    if found:
        (OUT / "DRAFT_NOT_FOR_DEPOSIT.txt").write_text(
            "This archive was assembled with --force and is not shippable.\n\n"
            + "\n".join(f"- {b}" for b in found) + "\n")
        print(f"assembled DRAFT with {n} files and {len(found)} blocker(s)")
    else:
        (OUT / "SHA256SUMS").write_text(
            "".join(f"{d}  {p}\n" for p, d in sorted(digests.items())))
        print(f"assembled {n} files, {len(digests)} checksummed -> "
              f"{OUT.relative_to(ROOT)}")
        # Zenodo takes one file. Building the archive here, rather than
        # leaving it to be zipped by hand, keeps the deposited bytes identical
        # to the ones whose checksums are recorded inside it.
        archive = Path(shutil.make_archive(str(ROOT / "release_bundle"), "zip",
                                           root_dir=str(OUT.parent),
                                           base_dir=OUT.name))
        print(f"archive:   {archive.relative_to(ROOT)}  "
              f"({archive.stat().st_size / 1e6:.1f} MB)")
    return 0 if not found else 1


if __name__ == "__main__":
    sys.exit(main())
