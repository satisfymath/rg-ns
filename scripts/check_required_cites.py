#!/usr/bin/env python3
"""Refuse to ship without the references a referee will look for.

These are the works whose scope overlaps this manuscript most directly: the
interacting-vacuum lineage, the mimetic/constrained-clock lineage and its known
pathologies, the interacting-dark-energy pathology catalogue, the DESI-era
constraints on the sign of the dark-sector coupling, and the data sets used.
Omitting any of them would read as an incomplete literature search.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "paper" / "references.bib"
SECTIONS = ROOT / "paper" / "sections"
GENERATED = ROOT / "paper" / "generated"


def tex_sources():
    """Every file whose citations reach the document, including the tables
    generated from results/results.json and included by the sections."""
    return sorted(SECTIONS.glob("*.tex")) + sorted(GENERATED.glob("*.tex"))

REQUIRED = {
    "1203.6776":  "Wands, De-Santiago & Wang: inhomogeneous vacuum energy",
    "1003.5751":  "Lim, Sawicki & Vikman: dust of dark energy (our clock action)",
    "1403.3961":  "Chamseddine, Mukhanov & Vikman: mimetic matter with a potential",
    "1612.08661": "Sebastiani, Vagnozzi & Myrzakulov: mimetic gravity review",
    "2602.14082": "Malaeb: mimetic gravity review (current)",
    "2607.19494": "The silent dark sector: closest published construction",
    "2603.12321": "Open effective field theory of dark energy",
    "2607.20348": "Beyond j=1: constraints on almost-LambdaCDM",
    "2509.04494": "Interacting dark energy pathologies II",
    "2509.04495": "Interacting dark energy pathologies I",
    "2509.04496": "Interacting dark energy pathologies III",
    "2607.12283": "Direction of the dark-sector interaction",
    "2608.21938": "Dark-sector interactions after DESI DR2",
    "0804.0232":  "Vaeliviita et al.: large-scale instability of IDE",
    "2312.14123": "Interacting vacuum perturbation formalism",
    "astro-ph/0502034": "Szydlowski: energy transfer and the third derivative",
    "hep-th/0004134": "Bousso & Polchinski: four-form fluxes",
    "2305.02349": "Kaloper: unimodular gravity with charged membranes",
    "2604.03363": "Topolons: three-form remnants",
    "gr-qc/9904062": "Rideout & Sorkin: sequential growth dynamics",
    "cond-mat/0001070": "Hinrichsen: absorbing-state phase transitions",
    "2503.14738": "DESI DR2 BAO",
    "1807.06209": "Planck 2018 parameters",
    "2202.04077": "Pantheon+ cosmological constraints",
    "1808.05724": "Planck distance priors",
    "1704.03367": "Babichev & Ramazanov: caustic-free completion",
    "1604.08586": "Ijjas, Ripley & Steinhardt: mimetic gradient instabilities",
}
# these must be cited in the introduction, where the relation to prior art is set
EARLY = ["1203.6776", "1003.5751", "1403.3961", "2607.19494"]


def main() -> int:
    if not BIB.exists():
        print("references.bib not found")
        return 1
    bib = BIB.read_text()
    keys_by_eprint = {}
    for m in re.finditer(r"@\w+\{([^,]+),(.*?)\n\}", bib, re.S):
        key, body = m.group(1).strip(), m.group(2)
        ep = re.search(r"eprint\s*=\s*\{([^}]+)\}", body)
        if ep:
            keys_by_eprint[ep.group(1).strip()] = key

    failures = []
    for eprint, why in REQUIRED.items():
        if eprint not in keys_by_eprint:
            failures.append(f"missing from references.bib: {eprint} ({why})")

    all_text = "\n".join(p.read_text() for p in tex_sources())
    cited = set(re.findall(r"\\[a-zA-Z]*cite[a-zA-Z]*\s*(?:\[[^\]]*\])*\{([^}]+)\}",
                           all_text))
    cited = {k.strip() for group in cited for k in group.split(",")}

    intro = SECTIONS / "01_intro.tex"
    intro_cited = set()
    if intro.exists():
        for group in re.findall(
                r"\\[a-zA-Z]*cite[a-zA-Z]*\s*(?:\[[^\]]*\])*\{([^}]+)\}",
                intro.read_text()):
            intro_cited |= {k.strip() for k in group.split(",")}

    # only enforce citation coverage once the sections have real content
    written = any(len(p.read_text()) > 400 for p in SECTIONS.glob("*.tex"))
    if written:
        for eprint, why in REQUIRED.items():
            key = keys_by_eprint.get(eprint)
            if key and key not in cited:
                failures.append(f"in the bibliography but never cited: {eprint} ({why})")
        for eprint in EARLY:
            key = keys_by_eprint.get(eprint)
            if key and key not in intro_cited:
                failures.append(f"must be cited in the introduction: {eprint}")

    if failures:
        print("check_required_cites FAILED:")
        for f in failures:
            print("  - " + f)
        return 1
    state = "citation coverage enforced" if written else "bibliography complete (sections still drafts)"
    print(f"check_required_cites: {len(REQUIRED)} required works present, {state}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
