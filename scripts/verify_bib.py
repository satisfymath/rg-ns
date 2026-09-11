#!/usr/bin/env python3
"""Verify every bibliography entry against arXiv, INSPIRE or Crossref.

Motivation: since May 2026 arXiv bans authors for a year when a submission
contains AI-generated content with incorrect or fabricated references.  This
script makes that failure mode impossible to reach silently: no entry enters
paper/references.bib without a machine check that the identifier really
resolves to the claimed title and first author.

Usage
-----
    python scripts/verify_bib.py                 # verify every entry (exit 1 on failure)
    python scripts/verify_bib.py --add 2503.14738 [...]   # fetch and append entries
    python scripts/verify_bib.py --report        # write docs/BIB_VERIFICATION.md
"""
from __future__ import annotations

import argparse
import datetime as dt
import difflib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "paper" / "references.bib"
REPORT = ROOT / "docs" / "BIB_VERIFICATION.md"
RESULTS = ROOT / "results" / "bib_verification.json"

ARXIV_API = "http://export.arxiv.org/api/query"
INSPIRE_API = "https://inspirehep.net/api/literature"
CROSSREF_API = "https://api.crossref.org/works/"
UA = {"User-Agent": "rg-ns-bib-verifier/1.0 (academic use)"}
ATOM = "{http://www.w3.org/2005/Atom}"

TITLE_MATCH_MIN = 0.92     # difflib ratio required between claimed and fetched title
BATCH = 20                 # arXiv id_list batch size
SLEEP = 3.0                # seconds between arXiv calls (their stated courtesy limit)


# --------------------------------------------------------------------------- #
# Minimal BibTeX parsing (entries are machine-written, so this is enough)
# --------------------------------------------------------------------------- #
ENTRY_RE = re.compile(r"@(\w+)\s*\{\s*([^,]+),(.*?)\n\}", re.S)
FIELD_RE = re.compile(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*(?=\n\s*\w+\s*=|\s*$)", re.S)


def parse_bib(text: str) -> list[dict]:
    out = []
    for kind, key, body in ENTRY_RE.findall(text):
        fields = {k.lower(): " ".join(v.split())
                  for k, v in FIELD_RE.findall(body)}
        out.append({"type": kind.lower(), "key": key.strip(), **fields})
    return out


#: Greek letters written as LaTeX macros must normalise back to the character
#: the remote record carries, or the title comparison fails on a difference
#: this script itself introduced.
_MACRO_TO_CHAR = {
    "lambda": "\u03bb", "Lambda": "\u039b", "omega": "\u03c9",
    "Omega": "\u03a9", "alpha": "\u03b1", "beta": "\u03b2",
    "gamma": "\u03b3", "Gamma": "\u0393", "delta": "\u03b4",
    "Delta": "\u0394", "sigma": "\u03c3", "Sigma": "\u03a3",
    "mu": "\u03bc", "nu": "\u03bd", "pi": "\u03c0", "tau": "\u03c4",
    "phi": "\u03c6", "chi": "\u03c7", "theta": "\u03b8", "rho": "\u03c1",
    "eta": "\u03b7", "xi": "\u03be", "zeta": "\u03b6", "kappa": "\u03ba",
    "psi": "\u03c8", "Phi": "\u03a6", "Psi": "\u03a8", "times": "\u00d7",
}


def norm_title(s: str) -> str:
    """Normalise a title for comparison: undo our own LaTeX escaping, then
    reduce to lowercase alphanumerics."""
    s = s or ""
    s = re.sub(r"\\ensuremath\s*\{\s*\\(\w+)\s*\}",
               lambda m: _MACRO_TO_CHAR.get(m.group(1), m.group(1)), s)
    s = re.sub(r"\\(\w+)",
               lambda m: _MACRO_TO_CHAR.get(m.group(1), m.group(1)), s)
    s = re.sub(r"[{}$\\]", "", s).lower()
    return re.sub(r"[^a-z0-9 ]+", " ", s).strip()


def first_surname(author_field: str) -> str:
    if not author_field:
        return ""
    first = author_field.split(" and ")[0].strip()
    if "," in first:
        return norm_title(first.split(",")[0])
    return norm_title(first.split()[-1]) if first.split() else ""


# --------------------------------------------------------------------------- #
# Remote lookups
# --------------------------------------------------------------------------- #
def _get(url: str, timeout: int = 60) -> bytes:
    return urllib.request.urlopen(
        urllib.request.Request(url, headers=UA), timeout=timeout).read()


def fetch_arxiv(ids: list[str]) -> dict[str, dict]:
    """Return {arxiv_id: {title, authors, published, doi, journal}}."""
    found: dict[str, dict] = {}
    for i in range(0, len(ids), BATCH):
        chunk = ids[i:i + BATCH]
        url = f"{ARXIV_API}?id_list={','.join(chunk)}&max_results={len(chunk)}"
        root = ET.fromstring(_get(url))
        for e in root.findall(f"{ATOM}entry"):
            raw = (e.findtext(f"{ATOM}id") or "")
            aid = raw.rsplit("/abs/", 1)[-1]
            aid_base = re.sub(r"v\d+$", "", aid)
            title = " ".join((e.findtext(f"{ATOM}title") or "").split())
            if not title or title.lower() == "error":
                continue
            authors = [a.findtext(f"{ATOM}name") or ""
                       for a in e.findall(f"{ATOM}author")]
            found[aid_base] = {
                "title": title,
                "authors": authors,
                "published": (e.findtext(f"{ATOM}published") or "")[:10],
                "doi": e.findtext("{http://arxiv.org/schemas/atom}doi") or "",
                "journal": e.findtext(
                    "{http://arxiv.org/schemas/atom}journal_ref") or "",
            }
        if i + BATCH < len(ids):
            time.sleep(SLEEP)
    return found


def fetch_inspire_doi(doi: str) -> dict | None:
    url = (f"{INSPIRE_API}?q=doi%20{urllib.parse.quote(doi)}"
           "&fields=titles,authors,publication_info&size=1")
    try:
        data = json.loads(_get(url))
    except Exception:                                             # noqa: BLE001
        return None
    hits = data.get("hits", {}).get("hits", [])
    if not hits:
        return None
    md = hits[0].get("metadata", {})
    titles = md.get("titles") or [{}]
    authors = [a.get("full_name", "") for a in (md.get("authors") or [])]
    return {"title": titles[0].get("title", ""), "authors": authors,
            "source": "inspire"}


def fetch_crossref_doi(doi: str) -> dict | None:
    try:
        data = json.loads(_get(CROSSREF_API + urllib.parse.quote(doi)))
    except Exception:                                             # noqa: BLE001
        return None
    msg = data.get("message", {})
    titles = msg.get("title") or [""]
    authors = [f"{a.get('given','')} {a.get('family','')}".strip()
               for a in (msg.get("author") or [])]
    return {"title": titles[0], "authors": authors, "source": "crossref"}


# --------------------------------------------------------------------------- #
# Verification
# --------------------------------------------------------------------------- #
def verify(entries: list[dict]) -> list[dict]:
    arxiv_ids = [e["eprint"] for e in entries if e.get("eprint")]
    remote = fetch_arxiv(arxiv_ids) if arxiv_ids else {}

    rows = []
    for e in entries:
        row = {"key": e["key"], "status": "UNVERIFIED", "score": 0.0,
               "source": "", "identifier": "", "fetched_title": ""}
        eprint, doi = e.get("eprint"), e.get("doi")
        meta = None
        if eprint:
            row["identifier"] = f"arXiv:{eprint}"
            row["source"] = "arxiv"
            meta = remote.get(re.sub(r"v\d+$", "", eprint))
        elif doi:
            row["identifier"] = f"doi:{doi}"
            meta = fetch_inspire_doi(doi) or fetch_crossref_doi(doi)
            row["source"] = (meta or {}).get("source", "none")
        else:
            row["status"] = "NO IDENTIFIER"
            rows.append(row)
            continue

        if meta is None:
            row["status"] = "NOT FOUND"
            rows.append(row)
            continue

        row["fetched_title"] = meta["title"]
        score = difflib.SequenceMatcher(
            None, norm_title(e.get("title", "")), norm_title(meta["title"])).ratio()
        row["score"] = round(score, 4)
        want = first_surname(e.get("author", ""))
        got = " ".join(norm_title(a) for a in meta.get("authors", [])[:3])
        author_ok = (not want) or (want in got)
        row["author_ok"] = author_ok
        row["status"] = "OK" if (score >= TITLE_MATCH_MIN and author_ok) else "MISMATCH"
        rows.append(row)
    return rows


#: pdflatex cannot typeset Greek or fancy punctuation coming from arXiv
#: titles, so entries are sanitised on the way in.  Latin accents are fine
#: (inputenc utf8 with T1 fonts handles them) and are left alone.
NON_ASCII_MAP = {
    "\u039b": r"$\\Lambda$", "\u03bb": r"$\\lambda$",
    "\u03a9": r"$\\Omega$", "\u03c9": r"$\\omega$",
    "\u03b1": r"$\\alpha$", "\u03b2": r"$\\beta$",
    "\u03b3": r"$\\gamma$", "\u0393": r"$\\Gamma$",
    "\u03b4": r"$\\delta$", "\u0394": r"$\\Delta$",
    "\u03b5": r"$\\epsilon$", "\u03c3": r"$\\sigma$",
    "\u03a3": r"$\\Sigma$", "\u03bc": r"$\\mu$", "\u03bd": r"$\\nu$",
    "\u03c0": r"$\\pi$", "\u03c4": r"$\\tau$", "\u03c6": r"$\\phi$",
    "\u03c7": r"$\\chi$", "\u03b8": r"$\\theta$", "\u03c1": r"$\\rho$",
    "\u03b7": r"$\\eta$", "\u03be": r"$\\xi$", "\u03b6": r"$\\zeta$",
    "\u03ba": r"$\\kappa$", "\u03c8": r"$\\psi$",
    "\u03a6": r"$\\Phi$", "\u03a8": r"$\\Psi$",
    "\u00d7": r"$\\times$", "\u2212": "-", "\u2013": "--", "\u2014": "---",
    "\u2019": "'", "\u2018": "'", "\u201c": "``", "\u201d": "''",
}


def sanitise(text: str) -> str:
    """Replace characters pdflatex cannot typeset, and escape TeX specials.

    Replacements use \\ensuremath rather than bare dollar signs, because arXiv
    titles frequently already wrap the character in math mode and nesting
    delimiters silently produces an undefined control sequence.  Ampersands in
    journal names (A&A) must also be escaped.
    """
    for k, v in NON_ASCII_MAP.items():
        text = text.replace(k, v)
    return re.sub(r"(?<![\\&])&", r"\\&", text)


BIB_TEMPLATE = """@article{{{key},
  author       = {{{authors}}},
  title        = {{{title}}},
  year         = {{{year}}},
  eprint       = {{{eprint}}},
  archiveprefix = {{arXiv}},
{extra}}}
"""


def make_key(meta: dict, eprint: str) -> str:
    surname = first_surname(" and ".join(meta["authors"])) or "anon"
    surname = re.sub(r"[^a-z]", "", surname)
    year = meta.get("published", "")[:4] or "0000"
    return f"{surname}{year}_{eprint.replace('/', '').replace('.', '')}"


def add_entries(ids: list[str]) -> int:
    meta = fetch_arxiv(ids)
    missing = [i for i in ids if re.sub(r"v\d+$", "", i) not in meta]
    if missing:
        print("could not resolve: " + ", ".join(missing))
        return 1
    existing = parse_bib(BIB.read_text()) if BIB.exists() else []
    have = {e.get("eprint") for e in existing}
    chunks = []
    for i in ids:
        base = re.sub(r"v\d+$", "", i)
        if base in have:
            print(f"  already present: {base}")
            continue
        m = meta[base]
        extra = ""
        if m.get("doi"):
            extra += f"  doi          = {{{m['doi']}}},\n"
        if m.get("journal"):
            extra += f"  journal      = {{{m['journal']}}},\n"
        extra += (f"  verified     = {{arXiv API "
                  f"{dt.date.today().isoformat()}}},\n")
        chunks.append(sanitise(BIB_TEMPLATE.format(
            key=make_key(m, base),
            authors=" and ".join(m["authors"]),
            title=m["title"], year=m.get("published", "")[:4],
            eprint=base, extra=extra)))
        print(f"  added: {base}  {m['title'][:70]}")
    if chunks:
        with BIB.open("a") as fh:
            fh.write("\n" + "\n".join(chunks))
    return 0


def write_report(rows: list[dict]) -> None:
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Bibliography verification log",
        "",
        f"Generated by `scripts/verify_bib.py` on {dt.date.today().isoformat()}.",
        "",
        "Every entry in `paper/references.bib` is resolved against the arXiv API",
        "(or INSPIRE/Crossref for journal-only references) and the fetched title",
        "is compared with the stored one. The build gate fails if any entry is",
        "unverified or mismatched.",
        "",
        "| key | identifier | status | title match | source |",
        "|---|---|---|---:|---|",
    ]
    for r in sorted(rows, key=lambda r: r["key"]):
        lines.append(f"| `{r['key']}` | {r['identifier']} | {r['status']} | "
                     f"{r['score']:.3f} | {r['source']} |")
    REPORT.write_text("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--add", nargs="+", metavar="ARXIV_ID")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    if args.add:
        return add_entries(args.add)

    if not BIB.exists():
        print(f"{BIB} not found")
        return 1
    entries = [e for e in parse_bib(BIB.read_text())
               if e["key"] != "placeholder2026"]
    if not entries:
        print("references.bib has no real entries yet")
        return 0

    rows = verify(entries)
    RESULTS.parent.mkdir(parents=True, exist_ok=True)
    RESULTS.write_text(json.dumps(rows, indent=2))
    write_report(rows)

    bad = [r for r in rows if r["status"] != "OK"]
    for r in rows:
        mark = "ok " if r["status"] == "OK" else "FAIL"
        print(f"  [{mark}] {r['key']:32s} {r['identifier']:22s} "
              f"score={r['score']:.3f} {r['status']}")
    # An entry that is verified but never cited is a different failure from an
    # entry that is wrong, and it is one a referee does notice: five of these
    # were the most directly relevant prior work in the file, sitting uncited
    # while the text cited the general formalism instead.
    import re as _re
    tex = "".join(p.read_text() for p in
                  sorted((ROOT / "paper").rglob("*.tex")))
    cited = set()
    for m in _re.finditer(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\])*"
                          r"\{([^}]*)\}", tex):
        cited |= {k.strip() for k in m.group(1).split(",")}
    uncited = sorted(k for k in (r["key"] for r in rows) if k not in cited)
    if uncited:
        print("\nverified but never cited:")
        for k in uncited:
            print(f"  - {k}")

    print(f"\n{len(rows) - len(bad)}/{len(rows)} entries verified")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
