#!/usr/bin/env python3
"""Record exactly what produced the results, so a reader can tell.

Versions, seeds, checksums, commit and platform, written to
``results/provenance.json``. The point is not ceremony: three of the numbers in
this manuscript changed during review because a protocol changed underneath
them, and without a record of which artifact came from which code there is no
way to notice that from the outside.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "provenance.json"

PACKAGES = ("numpy", "scipy", "matplotlib", "sympy", "emcee", "dynesty",
            "h5py", "pandas", "astropy")
DATA_DIR = ROOT / "data" / "raw"
RESULT_FILES = ("results.json", "evidence.json", "profile.json",
                "pancake.json", "theory_checks.json", "map.json",
                "chain_diagnostics.json", "prior_sensitivity.json",
                "evidence_repeatability.json", "prior_width_evidence.json")


def sha256(path: Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(chunk), b""):
            h.update(block)
    return h.hexdigest()


def git(*args: str) -> str:
    try:
        return subprocess.run(("git", *args), cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:                                           # noqa: BLE001
        return "unavailable"


def versions() -> dict[str, str]:
    out = {}
    for name in PACKAGES:
        try:
            mod = __import__(name)
            out[name] = getattr(mod, "__version__", "unknown")
        except ImportError:
            out[name] = "not installed"
    return out


def main() -> int:
    from absorb.constants import SEED                          # noqa: E402

    record = {
        "git_commit": git("rev-parse", "HEAD"),
        "git_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "python": sys.version.split()[0],
        "platform": platform.platform(),
        "packages": versions(),
        "master_seed": SEED,
        "data_checksums": {p.name: sha256(p)
                           for p in sorted(DATA_DIR.glob("*"))
                           if p.is_file()} if DATA_DIR.exists() else {},
        "result_checksums": {
            name: sha256(ROOT / "results" / name)
            for name in RESULT_FILES
            if (ROOT / "results" / name).exists()},
    }
    OUT.write_text(json.dumps(record, indent=2, sort_keys=True))
    print(f"provenance: commit {record['git_commit'][:8]}"
          f"{' (dirty)' if record['git_dirty'] else ''}, "
          f"python {record['python']}, "
          f"{len(record['data_checksums'])} data files, "
          f"{len(record['result_checksums'])} result files")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT / "code"))
    sys.exit(main())
