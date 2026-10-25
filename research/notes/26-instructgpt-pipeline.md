# Note: InstructGPT — the paper that made "helpful" a training target (2022)

Source: SRC-PAPER-009 · Access: **abstract-read** (arXiv v1 page,
verified with the chapter-04 build) · Note level: **abstract-level**.

## The actual problem

The alignment-before-InstructGPT state: base models follow the
*distribution* of human text, which is not the same as following
*instructions* — ask a base model a question and it may answer three
more questions to itself. The paper's question: can modest-scale
human feedback make models that follow instructions, and what does
that pipeline cost and buy?

## Method (as the abstract establishes it)

The three-stage pipeline the field inherited: supervised fine-tuning
on demonstrations → reward-model training from pairwise human
preferences → reinforcement learning (PPO) against the reward model,
with the KL-to-reference constraint. The abstract's headline
capability result: 1.3B-parameter InstructGPT outputs are preferred to
GPT-3 175B outputs — a 100x parameter efficiency gain for
instruction-following, which is why the pipeline became the industry
default rather than a footnote.

## Results (abstract-level, with the honest caveats the register carries)

What the course takes: the pipeline structure and its OWN stated
limitations — the register entry records the paper's honest admission
that the model can still give wrong answers with confidence and that
the alignment is narrow (to labelers' notion of "good"), which
chapter 04 prices as the first appearance of the sycophancy and
proxy-validity threads the course develops later. What the abstract
does not give: labeler-agreement statistics, the
distributional-sensitivity of the preference data, and the RL
stability details — body-level, unread, not cited.

## What this note does NOT claim

No claim that the pipeline "solved" alignment (the paper does not
claim it either — the limitations paragraph is the part to quote); no
modern-model comparisons (the 2022 model set is historical context,
not a current measurement).

## Falsifiable extension

The pipeline's unexamined number is labeler disagreement: with k
labelers per pair and disagreement rate d, the reward model learns the
MAJORITY preference — and every minority preference becomes training
noise indistinguishable from label error. At course scale, P04's
harness already implements biased label streams; the extension is a
two-population labeler model (deterministic, seeded) where the
disagreement is CORRELATED (two coherent preference profiles) rather
than random, measuring whether the tuned policy interpolates the
profiles or collapses to one. Stopping rule: collapse to one profile
at every mixture weight means the pipeline cannot represent
plural preferences — a construct-validity finding about RLHF-style
tuning that no amount of scale fixes; interpolation means the
preference geometry is richer than the majority-vote objective
assumes.

## My interpretation vs. their claims

Their claims: (1) human feedback at modest scale buys large
instruction-following gains; (2) the three-stage pipeline works.
My reading: (1) is one of the field's most consequential results and
the 100x efficiency framing deserves its fame; (2) is true and is the
course's caution — the pipeline WORKS, which is why its failure
surfaces (reward hacking on learned proxies, sycophancy from
preference pressure, the narrow-alignment limitation the authors
themselves flag) became the DEFAULT risks of every deployed assistant.
Chapter 03's Goodhart chain, chapter 04's label audit, chapter 06's
sycophancy analysis, and P04's seam are the curriculum-shaped answer
to this one paper's success.
