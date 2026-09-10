# Decisions and details only David can supply

Everything else in this project is either done or computable. These are not.
They are listed here so they cannot be lost in a commit log, and because two of
them block submission rather than merely improving it.

## Blocking submission

**Author identity.** `paper/main.tex` carries `\TODO{email, ORCID}`. The
decision already taken is: personal email, not the Despegar address, and
affiliation "Independent researcher". What is still needed is the address
itself and an ORCID (free, five minutes, orcid.org). Nothing else in the
manuscript depends on it.

**Zenodo DOI for the code.** `appF_numerics.tex` and
`99_acknowledgments.tex` both carry `\TODO{Zenodo DOI}`. The data-availability
statement is load-bearing for the reproducibility claim in
\cref{sec:observations} and cannot go to a journal as a TODO. The sequence is:
tag the repository, connect it to Zenodo, take the DOI. The chains are not
archived; `results/*.json` are.

## Needed before posting, not before writing

**arXiv endorsement.** A first-time submitter to astro-ph.CO needs an endorser.
`docs/submission/ENDORSEMENT.md` holds candidate names. Worth asking only once
every quality gate passes, since the request is easier to make with a finished
manuscript attached.

**Suggested referees**, if JCAP asks for them.

## Judgement calls where the work is done either way

**The title, and a tension in the current one.** It reads

> Self-reinforced geometric absorption: a memory-dependent kinetic framework
> for vacuum, dark matter and localized structure

while the abstract says, in as many words, "we do not claim that the defects
are the dark matter". A title offering a framework *for* dark matter and an
abstract disclaiming exactly that is the kind of mismatch a referee notices on
the first page, and it is the same failure mode --- summary claiming more than
body --- that referee E found running through the manuscript. No referee raised
it, which is not evidence that no referee will.

Three ways out, in decreasing order of how much they concede:

1. Drop "dark matter" from the title: *...a memory-dependent kinetic framework
   for the dark sector*. One word, no other change, tension gone.
2. Take the narrower phenomenology title recorded in the plan, which fits the
   manuscript as it now stands --- a null result, three obstructions recorded,
   and a cosmographic bound shown not to apply --- better than the omnibus one
   does.
3. Keep it and rely on the abstract's disclaimer. Defensible, but it spends the
   reader's goodwill in the first two lines.

Worth deciding after reading the current abstract rather than before.

**Track A versus Track B as the headline.** The data do not select between
them; LambdaCDM is preferred over both. The paper currently presents the
one-way model first and the reverse channel as its counterpart, which matches
the mathematics. If a future data set leans the other way this is the paragraph
to revisit.
