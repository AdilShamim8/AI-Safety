# Research-proposal template

Used by chapter 24, the pre-capstone checkpoint, and the P10-alternative
research capstone. One page. If it doesn't fit one page, the problem is not
narrowed yet.

```markdown
# Research proposal: <title>
Author · Date · Route (alignment / security / evaluations)

## Question
One falsifiable question. If it cannot be falsified by an observation, it
is not a research question — it is a topic.

## Nearest prior work
The 1-3 closest published efforts, with what each established and the gap
this proposal addresses. Novelty status: `unverified` or
`related-work-screened` (be honest; "nobody has studied this" is banned
without a screening log).

## Why it matters
What technical or deployment decision changes depending on the answer.
If no decision changes, the question is decorative.

## Method
- Hypothesis and the observation that would count against it.
- Baseline(s) you must beat-or-explain.
- Intervention/comparison and the control that isolates it.
- Metrics with denominators and uncertainty plan (sampling unit stated).

## Data and compute
Dataset or reproducible generation method (with license/access), models,
compute budget by tier (smoke/pilot/full). Anything unavailable becomes a
recorded blocker, not a hope.

## Two-week scoping experiment
The minimum run that de-risks the design. Expected outcome, and what each
possible result implies for the six-week extension.

## Six-week extension
What the full version adds, and the stopping rule (when you stop and
write up regardless).

## Failure conditions
The confounders that could invalidate the study, and the pre-stated
analysis choices that prevent post-hoc rescue.
```
