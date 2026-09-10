#!/usr/bin/env python3
"""Report chain progress without taking a lock on the files.

Opening an HDF5 file while the sampler is writing to it takes a lock and can
kill the run.  Reading with locking disabled is safe here because we only ever
read attributes, and a torn read costs nothing worse than a stale number.
"""
from __future__ import annotations

import glob
import os
import sys
from pathlib import Path

os.environ["HDF5_USE_FILE_LOCKING"] = "FALSE"

import h5py                                                    # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    for path in sorted(glob.glob(str(ROOT / "results" / "chains" / "*.h5"))):
        name = Path(path).name
        try:
            with h5py.File(path, "r", locking=False) as fh:
                g = fh["mcmc"]
                print(f"  {name:26s} {int(g.attrs['iteration']):7d} steps, "
                      f"{g['chain'].shape[1]} walkers")
        except Exception as exc:                               # noqa: BLE001
            print(f"  {name:26s} unreadable ({type(exc).__name__})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
