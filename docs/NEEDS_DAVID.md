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

**The title.** Two options are recorded in the plan: the omnibus one and the
narrower phenomenology one. The narrower one is more defensible and the
manuscript as it now stands --- a null result, three obstructions recorded, and
a cosmographic bound shown not to apply --- fits it better. Worth deciding
after reading the current abstract rather than before.

**Track A versus Track B as the headline.** The data do not select between
them; LambdaCDM is preferred over both. The paper currently presents the
one-way model first and the reverse channel as its counterpart, which matches
the mathematics. If a future data set leans the other way this is the paragraph
to revisit.
