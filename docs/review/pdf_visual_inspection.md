# Visual inspection of main.pdf (pre-submission typographic check)

All 60 pages inspected (rendered to PNG at 110 DPI and viewed page by page). 4 defects found: 3 blockers (visible TODO placeholders) and 1 cosmetic/should-fix layout issue, plus one should-fix figure label issue.

| Page | Severity | What is wrong |
|---|---|---|
| 1 | Blocker | Author footnote reads "*Independent researcher. **[TODO: email, ORCID]**" — the bracketed text is rendered in red and is a visible placeholder that must be filled in before submission. |
| 16 | Should-fix | Figure 3, top-left panel: the y-axis label reads "converted fraction, memc" — the label is truncated/cut off (appears to be missing the rest of a word, likely "memory"). |
| 48 | Blocker | "Data and code availability" section: "the results file from which every number and table in this paper is generated are archived at **[TODO: Zenodo DOI]**" — visible red placeholder text, not yet filled in. |
| 52 | Should-fix | Page is almost entirely blank: only the heading "A.2 The claims ladder in full" and one short (6-line) paragraph appear at the top; the remaining ~80% of the page is empty white space because the long table that follows (Table on p. 53) was floated to the next page. |
| 60 | Blocker | Appendix F.9 "Availability": "The code, the data checksums, ... are archived at **[TODO: Zenodo DOI]**" — same visible red placeholder as page 48, appears a second time here. |

## Notes on method
- Pages were rendered with `pdftoppm`/`pdftocairo` at 110 DPI (300 DPI for close-up crops) and read as images.
- `pdftoppm` intermittently threw "Embedded font file is not a stream" / "Embedded font object is wrong type" errors on pages 36–40 that caused those pages to render as blank or truncated in that one run; this was a rendering-tool artifact, not a document defect — re-rendering the same pages with `pdftocairo` (and a repeat `pdftoppm` run) reproduced the full, correct content with no missing text. Pages 36–40 are otherwise clean.
- No other issues found: no tables or equations overflow the text margins, no figure/caption separations, no figures placed far from their first reference, no illegible axis labels elsewhere, no widow/orphan lines, no misformatted bibliography entries, and no footnote/body-text collisions were observed on any other page.
