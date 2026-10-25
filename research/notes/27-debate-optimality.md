# Note: AI Safety via Debate — the optimality claim and its load-bearing assumption (2018)

Source: SRC-PAPER-015 · Access: **abstract-read** (arXiv page,
verified with the chapter-05 build) · Note level: **abstract-level**.

## The actual problem

Scalable oversight's hardest version: humans cannot directly judge
outputs that exceed their own competence. Debate's proposal: have two
AI systems argue opposite sides of a question before a human judge —
and make the ADVERSARY the mechanism that surfaces the flaws the
human could not find alone. The human judges the argument, not the
answer, so oversight strength decouples from oversight expertise.

## Method (as the abstract establishes it)

The debate protocol with the theoretical backbone this course records
in its register entry: under optimal play by both debaters, the
protocol is claimed to converge to true answers for problems in PSPACE
— the optimality argument that makes debate interesting to complexity
theory and not just to product teams. The register's limitations field
carries the honest caveat this note exists to keep visible: "optimal
play" is the load-bearing assumption, and real debaters are trained
models with whatever failure modes their training left in them.

## Results (abstract-level, honestly priced)

A theoretical proposal with toy demonstrations — as the abstract
states it. What the abstract does not give: the honest-judgment
experiments' magnitudes, the debate-protocol variants, and the
known degenerate strategies (collusion between debaters, judged
confusion under simultaneous good arguments). The course's chapter-05
treatment pairs this source with the empirical oversight literature
(weak-to-strong, decomposition) precisely because the optimality claim
is a MODEL of debate, not a measurement of trained debaters.

## What this note does NOT claim

No empirical effectiveness claim for debate in deployed systems; the
PSPACE statement is quoted as the paper's claim under its stated
assumptions, not as a course-verified theorem (the proof lives in the
unread body).

## Falsifiable extension

The assumption "optimal play" is exactly what a deterministic harness
can stress: model two debaters with asymmetric information (one holds
a disqualifying fact) and a judge that sees only the exchanged
arguments; vary the judge's error rate and the honest debater's
rebuttal budget. Stopping rule: if there exists a judge-error band in
which the protocol still converges to truth, debate's robustness margin
is measurable as a function of judge quality — the paper's assumption
becomes a curve; if convergence requires near-zero judge error, the
protocol inherits the judge's competence after all, and the
decoupling claim fails at this scale. Either output upgrades the
chapter's comparison table (C03's alignment-vs-control rows) from
"assumed" to "measured under stated conditions."

## My interpretation vs. their claims

Their claim: debate could exceed human judgment capacity under an
optimality argument. My reading: the paper's real contribution is
making ADVERSARIAL STRUCTURE a legible oversight primitive — the idea
that the safety mechanism can be built out of disagreement rather
than out of verification. That idea survives every caveat: it
reappears in red-team practice (Ch.15), in control's untrusted-
monitor designs (Ch.08), and in the paired ledgers this course runs
on everything (the two-sided ledger IS a one-round debate with a
statistical judge). The PSPACE optimality is the candle to keep lit
carefully: beautiful, load-bearing on "optimal play," and precisely
the kind of claim the audit-only route teaches students to carry
with its assumptions attached.
