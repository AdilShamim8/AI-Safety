# Lecture 4 — Model specifications and compliance: lessons from law

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 4: Model Specs](https://www.youtube.com/watch?v=LQ0RRQKKluc) (2:06:04) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The specification lecture: whether model behavior can be governed
by written rules. Announced topics: model specifications and
compliance; lessons from law; value alignment vs. detailed adherence.
The course page links the model specs students produced in class —
the lecture's own artifact layer.

## The announced scope

Model specs as private law: drafting, interpretation, measurement
(SpecEval), and the adjudication gap. The experiment "Can We Prompt
Our Way to Safety?" compares system prompts against safety
post-training on refusal benchmarks.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: the OpenAI Model Spec; Zvi Mowshowitz's review of it;
SpecEval (Ahmed et al. — evaluating adherence to behavior
specifications); "Statutory Construction and Interpretation for
Artificial Intelligence" (He et al.); "How People Use ChatGPT" (NBER,
Chatterji et al.). Optional: OpenAI's Collective Alignment write-up,
Claude's system prompts, RewardBench and RewardBench 2, Governance.ai,
Model Cards, and the Constitutional AI / Deliberative Alignment papers
again. The full list with links lives on the
[course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. Model specs: writing the law the model will be judged by

A model spec is a published document stating how a model should behave —
the operator's constitution, with defaults, chains of command, and
conflict-resolution rules between user, operator, and platform. The
lecture's central question is borrowed from law: can behavior *really*
be specified? The legal-realism answer is that statutes have always
underspecified; what fills the gap is interpretation plus precedent.
Models inherit both: the spec's prose is interpreted by training and by
editors, and SpecEval shows adherence is measurable but partial.

### 2. The compliance problem: specification without adjudication is aspiration

The lecture's "lessons from law" framing: a spec without an
adjudication mechanism (who hears violations, what precedent
accumulates, how rules evolve) is not a legal system, just a values
statement. Model operators are running the world's first legal systems
whose subjects are also their products — with A/B-tested statutes,
silent amendments, and no published case law. The Fall 2025 in-class
artifact (the course page links "model specs produced in class") made
students draft one, and drafting is the fastest way to discover how
underdetermined every clause is.

### 3. Value alignment vs. detailed adherence

The deep question the lecture poses: should alignment target *values*
(few, abstract, delegable) or *behaviors* (many, concrete, brittle)?
Constitutions chose values-plus-institutions; code chose behaviors.
LLMs sit between — abstract enough to interpret, concrete enough to
comply — which is precisely why the spec debate exists. The repo's
[Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md)
carries the failure side (every behavioral spec is gameable); this
lecture is the governance side of the same coin.

### 4. The experiment: prompting your way to safety?

The Fall 2025 experiment compares system-prompt styles against
post-training safety on over-refusal and toxic-refusal benchmarks —
finding prompt effects are highly model-dependent, sometimes reaching
safety-trained refusal rates at lower over-refusal cost. The honest
lesson is double-edged: prompts are a real safety surface, and prompts
are the surface most easily lost in deployment.

## Through-line to this repository's chapters

- [Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md) —
  specification gaming as the failure mode every spec invites.
- [Ch. 23](../../chapters/23-governance-and-standards/README.md) —
  model specs as the industry's private-law layer.
- [Ch. 06](../../chapters/06-honesty-uncertainty-and-selective-prediction/README.md) —
  over-refusal as the honesty-side cost the experiment measured.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
