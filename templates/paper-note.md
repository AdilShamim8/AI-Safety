# Paper-note template

A paper note is a methodological analysis, not an abstract paraphrase. If
your note could be written from the abstract alone, it is not done. Read the
method, evaluation, and limitations sections first; if only the abstract is
accessible, write an abstract-level entry and **say so** — the register's
access level must match.

```markdown
# Note: <Paper title> (<year>)
Source: <SRC-ID from research/source-register.yaml> · Access: <level> · Read: <date>

## The actual problem
What the authors set out to solve, in their framing — and the operational
version of that problem (what would count as solved in deployment).

## Method
What they actually did: setup, key moves, and the clever/fragile parts.
Define the objective or algorithm precisely enough to reimplement.

## Central evidence
The experiments/results that carry the paper's weight. Report the numbers
with their n's and conditions; note which claims the evidence does NOT
carry. Cite figures/tables/sections by number.

## Assumptions
What the method needs to be true (about data, models, evaluators, scale).
Mark which assumptions are tested in-paper and which are inherited.

## Limitations
The authors' stated limitations (fairly represented) plus the ones you see
that they don't state.

## Nearest alternatives
The 1-3 closest methods and what different evidence they provide. If you
cannot name one, you have not read the field around the paper yet.

## Replication feasibility
Could this repo's learners reproduce the core result at small scale? What
compute/data would it take? What would break first?

## Falsifiable extension
One concrete experiment that would extend or contradict the paper's claim —
hypothesis, baseline, metric, stopping rule, and what result counts against.

## My interpretation vs. their claims
Two labeled lists. Keep them separate; conflating them is the note-author's
most common sin.
```

Rules: quote sparingly (short fragments only, with section pointers);
distinguish "the authors claim X" from "I assess X"; never manufacture
benchmark numbers or author lists; record the source-register ID and actual
access level in the header line.
