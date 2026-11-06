# The honesty round — what was not run, and why

**Navigate:** [← questions](README.md) · [behavioral](behavioral.md)

**What this round is.** The newest round in the field's loops, and the
one this entire corpus was built to train: the interviewer probes the
boundary of your claims. "You said it works — under what conditions
did you verify that, and where does the verification stop?"

## Why it exists

Because the field's incidents taught it: evaluations that claimed
more than they tested (the [incidents](../../research/notes/incidents/)
layer reviews fourteen of them), and honesty failures that were only
caught in deployment. The corpus's answer is structural — every
project report ends with its not-executed tiers, and the
[honesty ledger](../../courses/honesty-ledger.md) records the
repository's own corrections the same way.

## The rehearsed answers

**"What did you not test?"** — Always answer with the list, never
with a hedge. "The suite covers direct injection and the spotlighting
family; it does not cover indirect vectors via retrieved content —
the Greshake note defines that gap." A named gap is a credential; a
fog is a rejection.

**"What would falsify your conclusion?"** — Every project carries a
preregistration or an explicit expectation; quote yours. "If the
subgroup gap vanished under decomposition, P09's claim would be
wrong. It didn't; the paired ledger is the evidence."

**"How confident are you, numerically?"** — The Wilson interval
answer, with the interval, from the [example report
format](../../projects/p01-evaluation-harness/example-report.md).
"About" is a hedge; an interval is an answer.

**"Have you ever shipped something you weren't sure about?"** — The
only acceptable shape: what was uncertain, what was done to bound it,
what monitoring watched for the failure. That is the
[safety-engineer](../roles/safety-engineer.md) job description in
miniature.

## The meta-answer

If asked "why do you answer this way": because in this field the
honest boundary IS the product — the [workforce
gap](../market/workforce-gap.md) is a demand signal for exactly this
discipline, and the [skills outlook](../market/skills-outlook.md)
says the durable skill is the method. This round is where that claim
gets tested first.
