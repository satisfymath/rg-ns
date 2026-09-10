#!/usr/bin/env python3
"""Extract every claim in the manuscript and where it is repeated.

The failure mode this exists to catch is the one four referees found
independently: a summary section asserting more than the body proves. The
ledger pairs each numbered result with its evidential level, its hypotheses,
the tests that cover it, and every place in the abstract, introduction or
conclusions that refers to it, so the three can be compared side by side.

It reads the LaTeX, not the PDF, so labels and levels are exact.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SECTIONS = ROOT / "paper" / "sections"
TESTS = ROOT / "code" / "tests"
OUT_MD = ROOT / "docs" / "CLAIM_LEDGER.md"
OUT_JSON = ROOT / "results" / "claim_ledger.json"

#: Sections whose statements must not exceed what the body proves.
SUMMARY_FILES = {"00_abstract.tex", "01_intro.tex", "14_conclusions.tex"}

ENVS = ("theorem", "proposition", "corollary", "lemma", "assumption",
        "remark", "definition")

ENV_RE = re.compile(
    r"\\begin\{(" + "|".join(ENVS) + r")\}(\[[^\]]*\])?\s*\\label\{([^}]+)\}",
    re.S)
KEYRESULT_RE = re.compile(r"\\begin\{keyresult\}\{(\w+)\}\{([^}]+)\}")
PLAIN_EQ_RE = re.compile(r"\\begin\{equation\}\s*\\label\{([^}]+)\}")
CREF_RE = re.compile(r"\\c?ref\{([^}]+)\}")
LEVEL_NAME = {"A": "postulate", "I": "identity", "C": "theorem of the model",
              "N": "numerical", "P": "fitted to data", "S": "conjecture"}


def body_of(text: str, start: int, env: str) -> str:
    end = text.find(f"\\end{{{env}}}", start)
    return text[start:end if end > 0 else start + 1200]


def collect() -> tuple[dict, set]:
    claims: dict[str, dict] = {}
    unmatched: set[tuple[str, str]] = set()

    for tex in sorted(SECTIONS.glob("*.tex")):
        text = tex.read_text()
        name = tex.name
        for m in ENV_RE.finditer(text):
            env, title, label = m.group(1), (m.group(2) or "").strip("[]"), m.group(3)
            claims[label] = dict(
                claim_id=label, kind=env, title=title, file=name,
                level=None, level_name=None,
                text=" ".join(body_of(text, m.end(), env).split())[:400],
                referenced_in=[], tests=[], status="UNREVIEWED")
        # labelled displayed equations that are not keyresults: they carry no
        # evidential level, but the manuscript still refers to them and a test
        # may still cover them, so they belong in the ledger.
        for m in PLAIN_EQ_RE.finditer(text):
            label = m.group(1)
            claims.setdefault(label, dict(
                claim_id=label, kind="equation", title="", file=name,
                level=None, level_name=None, text="",
                referenced_in=[], tests=[], status="UNREVIEWED"))
        for m in KEYRESULT_RE.finditer(text):
            level, label = m.group(1), m.group(2)
            claims.setdefault(label, dict(
                claim_id=label, kind="keyresult", title="", file=name,
                text="", referenced_in=[], tests=[], status="UNREVIEWED"))
            claims[label]["level"] = level
            claims[label]["level_name"] = LEVEL_NAME.get(level, "?")
            if claims[label]["kind"] != "keyresult":
                claims[label]["kind"] += "+keyresult"

    # where each claim is referred to, with special attention to the summaries
    for tex in sorted(SECTIONS.glob("*.tex")):
        text, name = tex.read_text(), tex.name
        for m in CREF_RE.finditer(text):
            for label in m.group(1).split(","):
                label = label.strip()
                if label in claims and name != claims[label]["file"]:
                    claims[label]["referenced_in"].append(name)

    # which tests cover which claim. Each test module declares this in a
    # "# covers:" marker, because matching on the label text alone missed
    # almost every real case: thm:bounded-rate-obstruction is covered by
    # test_bounded_rate_cannot_regularize, which shares no words with it.
    for path in sorted(TESTS.glob("test_*.py")):
        body = path.read_text()
        for line in body.splitlines():
            if line.startswith("# covers:"):
                payload = line[len("# covers:"):].strip()
                if payload.startswith("("):      # methodology-only marker
                    continue
                for label in payload.split(","):
                    label = label.strip()
                    if label in claims:
                        claims[label]["tests"].append(path.name)
                    elif label:
                        unmatched.add((path.name, label))
        # a label mentioned literally also counts
        for label in claims:
            if label in body:
                claims[label]["tests"].append(path.name)

    for c in claims.values():
        c["referenced_in"] = sorted(set(c["referenced_in"]))
        c["in_summary"] = sorted(set(c["referenced_in"]) & SUMMARY_FILES)
        c["tests"] = sorted(set(c["tests"]))
    return claims, unmatched


def main() -> int:
    claims, unmatched = collect()
    OUT_JSON.write_text(json.dumps(claims, indent=2, sort_keys=True))

    unclassified = [c for c in claims.values()
                    if c["level"] is None and c["kind"] not in
                    ("remark", "definition", "assumption")]
    in_summary_untested = [c for c in claims.values()
                           if c["in_summary"] and not c["tests"]]

    lines = [
        "# Claim ledger",
        "",
        "Generated by `scripts/claim_ledger.py` from the LaTeX sources. One row",
        "per numbered result. `In summary` lists the abstract, introduction or",
        "conclusions that refer to it: those are the places where a claim can",
        "quietly become stronger than its proof, which is what four referees",
        "found independently.",
        "",
        f"- results catalogued: **{len(claims)}**",
        f"- carrying an explicit evidential level: "
        f"**{sum(1 for c in claims.values() if c['level'])}**",
        f"- referred to from a summary section: "
        f"**{sum(1 for c in claims.values() if c['in_summary'])}**",
        f"- referred to from a summary but covered by no test: "
        f"**{len(in_summary_untested)}**",
        "",
        "| claim | kind | level | file | in summary | tests |",
        "|---|---|---|---|---|---|",
    ]
    for label in sorted(claims):
        c = claims[label]
        lvl = f"{c['level']} ({c['level_name']})" if c["level"] else "—"
        lines.append(
            f"| `{label}` | {c['kind']} | {lvl} | {c['file']} | "
            f"{', '.join(c['in_summary']) or '—'} | "
            f"{', '.join(t.replace('test_','').replace('.py','') for t in c['tests']) or '—'} |")

    if unmatched:
        lines += ["", "## Test markers naming a label the manuscript does not define", ""]
        for fname, label in sorted(unmatched):
            lines.append(f"- `{fname}` claims to cover `{label}`, which is not "
                         f"a label in the sources")

    if in_summary_untested:
        lines += ["", "## Referred to from a summary, covered by no test", ""]
        for c in sorted(in_summary_untested, key=lambda x: x["claim_id"]):
            lines.append(f"- `{c['claim_id']}` ({c['kind']}) — cited in "
                         f"{', '.join(c['in_summary'])}")

    OUT_MD.write_text("\n".join(lines) + "\n")
    print(f"catalogued {len(claims)} results -> {OUT_MD.relative_to(ROOT)}")
    print(f"  with a level: {sum(1 for c in claims.values() if c['level'])}")
    print(f"  cited in a summary: {sum(1 for c in claims.values() if c['in_summary'])}")
    print(f"  cited in a summary with no test: {len(in_summary_untested)}")
    if unmatched:
        print("FAILED: a test marker names a label the manuscript does not define:")
        for fname, label in sorted(unmatched):
            print(f"  - {fname}: {label}")
        return 1
    if in_summary_untested:
        print("FAILED: claims quoted in a summary section with nothing testing them:")
        for c in sorted(in_summary_untested, key=lambda x: x["claim_id"]):
            print(f"  - {c['claim_id']} (cited in {', '.join(c['in_summary'])})")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
