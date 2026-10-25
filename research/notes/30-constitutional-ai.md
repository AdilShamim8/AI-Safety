# Note: Constitutional AI — supervision moved into a document (2022)

Source: SRC-PAPER-011 · Access: **abstract-read** (arXiv page,
verified with the chapter-04 build) · Note level: **abstract-level**.

## The actual problem

RLHF's scaling bottleneck is the humans: preference labels are
expensive, inconsistent, and encode whatever the labeler crowd
believes that day. The paper's question: can the supervision target
itself be made explicit — written down, inspectable, revisable — so
that a model can be trained against PRINCIPLES rather than against an
anonymous crowd's implicit ones?

## Method (as the abstract establishes it)

The two-phase recipe the course's chapter 04 records: **revision** —
the model critiques and rewrites its own harmful responses against an
explicit constitution (a written set of principles), producing
revised training data; **RL from AI feedback (RLAIF)** — a separate
model instance scores response pairs against the same constitution,
replacing the human preference labels in the RLHF-shaped pipeline.
The constitution is the load-bearing artifact: supervision that lives
in a document people can read, diff, and argue about.

## Results (abstract-level, honestly priced)

Harmlessness improved with dramatically fewer human labels — as the
abstract states. What it does not give: the harmlessness-helpfulness
tradeoff magnitudes, the constitution-sensitivity analysis (does
changing the document change the model the way changing labelers
does?), and the AI-feedback-reward-hacking behavior P04's audit
would look for. Those are body-level, unread, not cited.

## What this note does NOT claim

No claim that written principles are "more aligned" than human labels
— they are more INSPECTABLE, which is a different property and the
one the course actually uses.

## Falsifiable extension

The unexamined question the course can run: a constitution is a
GOODHART SURFACE like any other supervision target. Design at the
deterministic tier: P02's JudgeScoredAnswers organism with the judge
replaced by a rule-based "constitutional" scorer (principles as
explicit predicates); pressure the pipeline (bon-width / budgeted
search) and measure whether the organism Goodharts the CONSTITUTION
the same way it Goodharts scalar rewards. Stopping rule: if proxy-gap
growth under the constitutional judge matches the scalar judge's at
equal pressure, the document changes who reads the supervision, not
the failure family — a real, quotable boundary on the "principles
fix it" narrative; if the gap grows slower, the explicitness itself
buys robustness, which is the paper's strongest unstated claim.

## My interpretation vs. their claims

Their claim: constitutional training buys harmlessness with less human
labeling. My reading: the durable contribution is GOVERNANCE-SHAPED,
not training-shaped — supervision that can be read is supervision
that can be audited, contested, and versioned, which is why chapter
23's governance instruments and chapter 22's safety cases both cite
the pattern. The honest caveat the course attaches: an inspectable
objective is still an objective, and P02/P04's whole curriculum role
is to keep "you can read it" from quietly becoming "it is aligned."
The two-sided ledger applies to documents too.
