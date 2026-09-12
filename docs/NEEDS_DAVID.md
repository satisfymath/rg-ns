# Decisions and details only David can supply

Three things block the deposit and the submission. None of them is hard, none
costs money, and the order matters because of one circularity: the manuscript
must cite the archive's DOI, and the archive is normally created after the
manuscript. Zenodo solves that by letting you *reserve* a DOI before
publishing. Do it in this order and nothing has to be done twice.

---

## Step 1 — a personal email address (5 minutes)

The only requirement is that it is not the Despegar address. A work address on
a paper stops working the day you change jobs, and it implies an institutional
affiliation for work that is not institutional.

If you already have a personal address, use it. If not, any provider is fine;
Gmail, Proton and Fastmail all take about three minutes. Use something you
will still read in ten years, because it goes on the paper permanently and is
how a referee or a reader reaches you.

## Step 2 — an ORCID (5 minutes, free, needs Step 1)

An ORCID is a permanent author identifier — sixteen digits like
`0000-0002-1825-0097`. It exists because names are ambiguous and change;
journals increasingly require one, and arXiv will link your submissions to it.

1. Go to **https://orcid.org/register**
2. Name, the email from Step 1, a password. Confirm the email.
3. That is all. You now have `https://orcid.org/0000-XXXX-XXXX-XXXX`.

Optionally set the visibility of your record to public and add "Independent
researcher" as affiliation; neither is required for the paper.

## Step 3 — a Zenodo DOI for the code (20 minutes, free, needs Step 2)

Zenodo is CERN's open repository. It gives the code a permanent DOI so the
paper's reproducibility claim points at something citable and frozen.

**Sign in with your ORCID** — the button is on the front page — which links
the two accounts automatically.

Then, and this is the part that avoids doing everything twice:

1. **New upload** → do *not* upload anything yet.
2. Click **Reserve DOI**. Zenodo shows you the DOI it will assign, something
   like `10.5281/zenodo.1234567`. Copy it.
3. Fill in the metadata. `/.zenodo.json` in this repository already contains
   the title, description, licence, keywords and author block; you can paste
   from it. Upload type: **Software**. Licence: **MIT**.
4. Come back here and tell me the email, the ORCID and the reserved DOI. I
   replace the three placeholders, rebuild, and run `make release`, which
   produces the archive with the DOI already inside it.
5. Upload that archive to the same Zenodo draft and press **Publish**. The
   reserved DOI becomes live and points at exactly the version the paper
   cites.

There is no GitHub repository here and none is needed: Zenodo takes a direct
upload. If you would rather have the code on GitHub as well, Zenodo can watch
a repository and mint a DOI on every release, but that is a convenience and
can be done later.

### What actually gets deposited

`make_release.py` assembles it: the code, the test suite, the scripts, the
generated results, the figures and the manuscript sources. **No observational
data are redistributed** — a script downloads each public data set and checks
its SHA256 — and the nested-sampling chains are not archived because they are
large and regenerable. Everything the paper quotes a number from is in there.

The script refuses to build while any placeholder remains, in the manuscript
*or* in the deposit metadata. A Zenodo record is permanent and public, so one
with `TODO-ORCID` where an identifier belongs is worse than no record at all.

---

## The title, which is a judgement call and not a blocker

The current title reads

> Self-reinforced geometric absorption: a memory-dependent kinetic framework
> for vacuum, dark matter and localized structure

while the abstract says, in as many words, that we do not claim the defects are
the dark matter. A title offering a framework *for* dark matter beside an
abstract disclaiming exactly that is the kind of mismatch a referee notices on
the first page.

My recommendation is the one-word fix: drop "dark matter" for "the dark
sector". It costs nothing and removes the tension. Say the word and I change
it; say nothing and it stays as it is, which is defensible but spends the
reader's goodwill in the first two lines.

## Later, not now

**arXiv endorsement.** A first-time submitter to astro-ph.CO needs an endorser.
`docs/submission/ENDORSEMENT.md` holds candidates. Worth asking only once the
manuscript is finished, since the request is easier to make with a finished
paper attached.

**Suggested referees**, if JCAP asks for them.
