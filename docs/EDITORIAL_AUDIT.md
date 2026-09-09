# Editorial audit

Run after the referee rounds, before packaging. The format follows the
contradiction-table method: fix a canonical answer for every disputed fact,
then check every occurrence against it.

## 1. Executive summary

[Core contribution in two sentences. The two weakest points. Whether the
manuscript is ready to submit.]

## 2. Canonical narrative decisions

Where the manuscript could say two different things, this table fixes which one
it says. Every occurrence must match.

| Question | Canonical answer | Enforced in |
|---|---|---|
| Is this a unified theory? | No. It is an effective framework with an explicit claims ladder. The words "unified" and "unification" appear only qualified by "effective framework" or in the negative. | title, abstract, Sec. 1, Sec. 14 |
| Is the clock action new? | No. It is the Lim-Sawicki-Vikman construction; what is new is that its potential is determined by the kinetics rather than chosen. | Sec. 8 |
| Is the interacting vacuum new? | No. Wands, De-Santiago and Wang. | Sec. 1, Sec. 5 |
| What is new? | The absorbing-state kinetics with self-reinforcement, and the memory law with its hysteresis consequence. | Sec. 1, Sec. 3, Sec. 4 |
| Does the data favour this model? | [to be filled from results/results.json; state it the same way everywhere] | abstract, Sec. 10, Sec. 14 |
| What is the status of the defect-as-dark-matter identification? | Conjecture. | Sec. 11, Sec. 13 |
| Is the jerk bound confirmed by data? | No. It is a falsifiable prediction; current constraints do not decide it. | Sec. 7, Sec. 10 |

## 3. Contradiction table

| ID | Location A | Location B | Type | Resolution | Confidence |
|---|---|---|---|---|---|
| C-01 | | | | | |

Types: numerical (two values disagree), logical (two statements cannot both
hold), scope (a claim is broader in one place than another), attribution (prior
work credited inconsistently).

## 4. Placeholder and reference audit

- [ ] No `\TODO` or `\CITE` remains
- [ ] No `[to be filled]`, `XXX`, or `TBD`
- [ ] Every `\cref` resolves
- [ ] Every figure referenced in the text before it appears
- [ ] `docs/BIB_VERIFICATION.md` shows every entry OK

## 5. Claims audit

- [ ] Every displayed result appears in `docs/CLAIMS_LADDER.md`
- [ ] No level-S claim outside the Outlook
- [ ] No claim in the abstract stronger than its section states
- [ ] Every theorem names the assumptions it uses

## 6. Numerical consistency

- [ ] Every number in the abstract, introduction and conclusions matches
      `results/results.json`
- [ ] `make check` green

## 7. Action plan

**Critical** (blocks submission):

**Important** (should fix):

**Nice to have**:
