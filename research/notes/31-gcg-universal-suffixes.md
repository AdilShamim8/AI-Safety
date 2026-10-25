# Note: GCG — optimized suffixes and the end of prompt-level confidence (2023)

Source: SRC-PAPER-004 · Access: **abstract-read** (arXiv page,
verified with the chapter-12/13 builds) · Note level: **abstract-level**.

## The actual problem

Jailbreaks found by humans are idiosyncratic; the question the paper
asks is whether adversarial examples — the Ch.12 phenomenon in vision
— have a direct language-model analogue. If attack suffixes can be
OPTIMIZED against the model's gradients and TRANSFER between models,
then "we patched that jailbreak" is not a defense category, and the
robustness bar for instruction-following resets to where vision
robustness sat after Szegedy: a measured, adversarial, unsolved
problem.

## Method (as the abstract establishes it)

Gradient-guided search over token sequences (GCG — Greedy Coordinate
Gradient) producing adversarial suffixes that induce affirmative
responses to harmful requests; the key empirical property: the suffixes
TRANSFER — optimized against one open model, they jailbreak other
models and commercial APIs, including ones whose gradients are not
accessible. The optimization is discrete (tokens), guided by
continuous gradients over candidate positions.

## Results (abstract-level, honestly priced)

Transferable jailbreaks across model families — as the abstract
states. What it does not give: per-model ASR magnitudes under the
transferred attacks, the suffix-length sensitivity, and the
defense-evaluation results that followed this line. The course cites
it for exactly one load-bearing consequence (below), which the
abstract does establish.

## What this note does NOT claim

No "all defenses are broken" universal claim — the paper demonstrates
a class of optimized, transferable attacks; specific defenses get
their own evaluations (and Ch.13's spotlighting and CaMeL notes carry
those stories with their own numbers).

## Falsifiable extension

The course-scale question is the transfer mechanism itself: is
transfer exploiting shared training data, shared architectures, or
shared INSTRUCTION TUNING? Deterministic probe: three "models" as
differently-seeded logistic policies over the same vocabulary with
(a) shared, (b) disjoint training slices; optimize a discrete suffix
against model A (greedy coordinate search over a small token set),
then measure success against B under each condition. Stopping rule:
transfer under disjoint slices at near the shared-slice rate indicts
the objective family (instruction-following itself is the common
factor); transfer collapsing under disjoint slices indicts data
contamination — and either answer redirects where the defense budget
belongs (architecture-level boundaries vs. data governance).

## My interpretation vs. their claims

Their claim: optimized adversarial suffixes jailbreak aligned models
and transfer. My reading: the durable sentence is the one Ch.13
builds on — prompts-as-defense cannot be a boundary, because the
attack surface is OPTIMIZABLE and the defense is not; every
same-channel defense is a prior about where an adversary has not yet
spent compute. The paper is also why this course's security spine
runs Ch.12 (the vision-era lesson: adversarial pressure is real,
transfer is real, defense evaluation must be adaptive) BEFORE Ch.13's
LLM application security — the suffix result is the bridge between
them, and the Carlini-Wagner lineage (note 05) arrives in language.
