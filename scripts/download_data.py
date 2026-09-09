#!/usr/bin/env python3
"""Download the public datasets used in the analysis and record checksums.

Every file is fetched from its canonical public location, hashed, and compared
against data/SHA256SUMS.  Run with --record on a clean checkout to (re)write the
checksum file.  No data are redistributed with this repository.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
SUMS = ROOT / "data" / "SHA256SUMS"

PANTHEON = ("https://raw.githubusercontent.com/PantheonPlusSH0ES/DataRelease/"
            "main/Pantheon%2B_Data/4_DISTANCES_AND_COVAR/")
DESI = ("https://raw.githubusercontent.com/CobayaSampler/bao_data/master/"
        "desi_bao_dr2/")
SDSS = "https://raw.githubusercontent.com/CobayaSampler/bao_data/master/"
CC = "https://gitlab.com/mmoresco/CCcovariance/-/raw/master/"

FILES = {
    # Type Ia supernovae -- Brout et al. 2022 (Pantheon+SH0ES)
    "PantheonPlusSH0ES.dat":        PANTHEON + "Pantheon%2BSH0ES.dat",
    "PantheonPlusSH0ES_STATSYS.cov": PANTHEON + "Pantheon%2BSH0ES_STAT%2BSYS.cov",
    # BAO -- DESI DR2 (arXiv:2503.14738), Cobaya-packaged Gaussian likelihood
    "desi_dr2_bao_mean.txt":        DESI + "desi_gaussian_bao_ALL_GCcomb_mean.txt",
    "desi_dr2_bao_cov.txt":         DESI + "desi_gaussian_bao_ALL_GCcomb_cov.txt",
    # RSD -- eBOSS DR16 full-shape (fsigma8 sub-blocks only)
    "sdss_DR16_LRG_FSBAO.dat":      SDSS + "sdss_DR16_BAOplus_LRG_FSBAO_DMDHfs8.dat",
    "sdss_DR16_LRG_FSBAO_cov.txt":  SDSS + "sdss_DR16_BAOplus_LRG_FSBAO_DMDHfs8_covtot.txt",
    "sdss_DR16_QSO_FSBAO.dat":      SDSS + "sdss_DR16_BAOplus_QSO_FSBAO_DMDHfs8.dat",
    "sdss_DR16_QSO_FSBAO_cov.txt":  SDSS + "sdss_DR16_BAOplus_QSO_FSBAO_DMDHfs8_covtot.txt",
    # Cosmic chronometers -- Moresco et al. compilation + systematics
    "HzTable_MM_BC03.dat":          CC + "data/HzTable_MM_BC03.dat",
    "data_MM20.dat":                CC + "data/data_MM20.dat",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(name: str, url: str, force: bool = False) -> Path:
    dest = RAW / name
    if dest.exists() and not force:
        print(f"  have  {name} ({dest.stat().st_size:,} B)")
        return dest
    print(f"  get   {name} ...", end="", flush=True)
    req = urllib.request.Request(url, headers={"User-Agent": "rg-ns/1.0"})
    with urllib.request.urlopen(req, timeout=120) as resp, dest.open("wb") as out:
        out.write(resp.read())
    print(f" {dest.stat().st_size:,} B")
    return dest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--record", action="store_true",
                    help="write data/SHA256SUMS instead of verifying")
    ap.add_argument("--force", action="store_true", help="re-download")
    args = ap.parse_args()

    RAW.mkdir(parents=True, exist_ok=True)
    print(f"data directory: {RAW}")
    digests = {}
    for name, url in FILES.items():
        try:
            path = fetch(name, url, force=args.force)
        except Exception as exc:                              # noqa: BLE001
            print(f"\n  FAIL  {name}: {exc}")
            return 1
        digests[name] = sha256(path)

    if args.record:
        SUMS.write_text("".join(f"{d}  {n}\n" for n, d in sorted(digests.items())))
        print(f"\nwrote {SUMS}")
        return 0

    if not SUMS.exists():
        print(f"\n{SUMS} missing; rerun with --record")
        return 1
    expected = {}
    for line in SUMS.read_text().splitlines():
        if line.strip():
            d, n = line.split(maxsplit=1)
            expected[n.strip()] = d
    bad = [n for n, d in digests.items() if expected.get(n) != d]
    if bad:
        print("\nCHECKSUM MISMATCH: " + ", ".join(bad))
        return 1
    print(f"\nall {len(digests)} files verified against SHA256SUMS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
