# Note: Inverse Scaling — the contest that documented "bigger is worse" (2023)

Source: SRC-PAPER-123 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Scaling laws say loss falls predictably with scale; the field's default
inference — "bigger gets better at everything that matters" — is what
this paper breaks. **Inverse scaling: worse task performance with
increased scale**, with causes in the training objective and data, not
in optimization failure. The evidence engine was a public contest —
the **Inverse Scaling Prize** with a substantial prize pool — yielding
**11 datasets** on which larger models did measurably worse, plus
literature examples analyzed alongside.

The abstract names **four candidate causes** (the fourth truncates in
the API record; three are complete): (i) **preference to repeat
memorized sequences over following in-context instructions** — scale
buys memorization, and memorization *wins* over the instruction;
(ii) **imitation of undesirable patterns in the training data** —
scale amplifies the patterns, it does not launder them; (iii) **tasks
containing an easy distractor task** which [larger models solve at the
expense of the harder real task — the truncation's evident completion,
recorded honestly as inferred-from-structure, not quoted].

## Why this is a safety document, not a benchmark paper

The course reads it as the direct counterweight to every "scale will
fix it" argument:

1. **The alignment-tax debate's mirror.** Note 42's finding was that
   alignment training improved capability evals (scaling looks kind);
   this note documents task families where scale itself degrades
   the *behavior* being measured (scaling looks unkind). Both are
   true; neither generalizes; both are load-bearing for Ch. 04's
   "how much alignment training" governance question.
2. **Memorization-over-instruction (cause i) is an alignment-relevant
   failure family.** The model that repeats memorized sequences over
   in-context instructions is the model whose training prior beats
   its deployment context — the same priority-inversion structure as
   note 44's competing objectives, seen from the training side. When
   safety instructions are the in-context part and the prior encodes
   something else, scale's memorization preference is a *hazard
   gradient*, not a quirk.
3. **U-shaped follow-ups discipline the claim.** The abstract's
   literature-analysis half is where the paper connects to the later
   finding (Wei et al.'s inverse-scaling-can-become-U-shaped result —
   noted in the course's readings as the boundary condition: some
   inverse trends reverse at larger scale). The honest scale-drift
   posture (Ch. 17) is exactly this: today's inverse trend is data,
   not destiny.

## What the abstract establishes

1. The phenomenon's definition and its attribution to
   objective/data flaws.
2. The contest mechanism (public, prize-funded) and the 11-dataset
   yield.
3. Causes (i)–(iii) verbatim; (iv) truncated and marked.
4. The framing that the analysis includes "other examples found in
   the literature."

Body-level, unclaimed: which datasets exhibited which cause, the
per-dataset scaling curves, prize logistics, and the winning-entry
details. The note claims the phenomenon, the mechanism taxonomy (3 of
4), and the contest's existence.

## Why this note exists in the course

Chapter 02 (evaluation science) carries it as the **scale-axis
construct-validity** citation: any eval claiming to measure a safety
property must state its scale dependence, because the sign of the
dependence is an empirical question this paper showed can be negative.
Ch. 17 (distribution shift and deployment reliability) carries it as
the upgrade-drift warning: "the next checkpoint is bigger" is not a
safety monotone — a fleet's failure profile can *worsen* under
uniformly-expected upgrades, which is a release-gate trigger
(behavior-changing release, the glossary term) that Ch. 22's gates
exist to catch.

It also closes a thread from note 41: model-written evaluations
*discovered* new inverse-scaling cases; this paper is the systematic
account of the phenomenon those discoveries pointed at. The two notes
together are why P01's harness pins per-case-family results and
refuses a single headline number.

## The falsifiable extension (deterministic tier)

Cause (iii) — the distractor task — is synthetically implementable:

- Build a two-level task where an easy surface rule predicts labels at
  ~p% and the deeper real rule at ~q% (q > p). Train learners of
  increasing *capacity* (more hidden units / more training passes) on
  the same data; measure which rule each learner's predictions track.
- Prediction worth testing from the paper: low-capacity learners
  lock onto the distractor (it is easier), and — the inverse-scaling
  shape at this tier — *additional capacity does not escape it*
  while the distractor keeps fitting the training data, reproducing
  cause (iii) as a plateau rather than a reversal.
- Falsifier: monotone escape (capacity → real rule) would show this
  synthetic world exhibits only the benign scaling direction —
  bounding the note's transfer, and sharpening that the *data*
  (distractor fit) is the load-bearing variable, exactly the paper's
  attribution to objective-and-data rather than optimizer.
