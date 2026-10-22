# Note: Wild Patterns: Ten Years After the Rise of Adversarial Machine Learning (2018)

Source: SRC-PAPER-049 · Access: abstract-read · Read: 2026-10-22 ·
Note level: **abstract-level**.

## The actual problem

The authors' framing: adversarial ML had a decade of results before
the deep-learning era noticed — organize it. The operational version:
the field's map — threat models and attacks at training time versus
test time, from the first poisoning and evasion work against
non-deep classifiers through the deep-learning wave, with the
security-evaluation misconceptions called out as first-class content.

## Method

(What the abstract carries:) a survey — the systematic organization
of ten years of work around threat-model distinctions (attacker
knowledge, attack phase), reporting connections between lines of
work and highlighting misconceptions in security evaluation. The
method is the *taxonomy*: the train/test-time and
knowledge/phase/ Specificity axes that chapter 12's grid
operationalizes for the course.

## Central evidence

(For a survey, the evidence is the organization's adequacy — priced
here by what it lets a reader do:) the taxonomy holds: every
subsequent development in chapter 12's canon (evasion, poisoning,
backdoors, extraction, membership inference) slots into the
Biggio–Roli frame without strain — a decade-plus of later results
validating a survey's axes is the strongest evidence a survey can
have.

What the survey does NOT carry (register-level honesty): the
per-attack quantitative details live in the unread full text and are
not cited; the 2018 cutoff means the LLM era (injection, optimized
suffixes, the defense-evaluation failures chapter 12 teaches) is
absent — the frame survives it, the content predates it.

## Assumptions

The survey's premises: that security concepts (attacker models,
phases, objectives) map cleanly onto ML attacks — the transfer that
makes "threat model" the right vocabulary; that organizing by threat
model (rather than by technique or by paper) serves the reader.

Both aged well: the threat-model-first organization is exactly how
the field (and this course) now teaches the material, and the
misconceptions section anticipated the evaluation-discipline
literature (C&W, Croce–Hein) by years.

## Limitations

Authors' (abstract-level): the survey scope itself.
Mine: the deep-learning-era sections were written while that era's
evaluation crisis was still forming — the survey *names* the
misconceptions but could not yet cite their canonical
demonstrations; and the 2018 attacker model (mostly single-shot,
mostly vision) under-weights the query-budget and adaptive-search
structure that later black-box attacks (extraction, optimization-
based injection) made central.

## Nearest alternatives

- **Carlini et al.'s evaluation guidelines (SRC-PAPER-048)**: the
  misconceptions section's future — the same concerns, backed by the
  canonical failure demonstrations, nine authors deep.
- **The OWASP LLM Top 10 (SRC-REPORT-004)**: the taxonomy's
  deployment-vocabulary descendant — threat models translated into
  engineering checklists.
- **Chapter 12 itself**: the course's own synthesis — the grid, the
  feasibility-argument burden, and the audit arithmetic are the
  survey's axes taught as practice.

## Replication feasibility

A survey does not replicate — it *organizes*, and the course-scale
equivalent is the exercise: take any new attack paper and place it
in the grid (phase, knowledge, exploits, feasibility burden). If it
fits, the taxonomy is doing its job; if it strains, the taxonomy
needs a new axis — and the learner has just done survey work.

## Falsifiable extension

Hypothesis (a taxonomy-stress test): the post-2018 attack classes
that strain the Biggio–Roli frame most are the *multi-phase,
multi-agent* ones — prompt injection into an agentic pipeline
(training-time trust + inference-time execution), where the
knowledge/phase grid needs a third axis (whose pipeline stage the
attacker occupies) to classify correctly. Design: collect the
chapter 13–14 attack taxonomy entries; classify each under the
two-axis grid alone, then with the stage axis; count classification
conflicts (entries that fit multiple cells or none). Metric:
conflict rate per scheme with the same entries. What counts
against: if the two-axis grid classifies the agentic entries
without excess conflict, the 2018 frame survived the LLM era
intact — and my third-axis premise fails, which would be a notable
robustness result for the survey.

## My interpretation vs. their claims

Their claims: (1) adversarial ML's first decade organizes around
threat models (attacker knowledge, attack phase); (2) the lines of
work connect across the non-deep and deep eras; (3) security
evaluation of ML carries systematic misconceptions.

My interpretation: (1) is the field's most durable organizational
act — the vocabulary survived its own content (the frame classifies
attacks the authors never saw), which is the only immortality a
survey gets; (2) the continuity claim was quietly corrective: the
deep-learning era's "adversarial examples are new" narrative erased
a decade of poisoning and evasion work, and the survey restored the
pedigree — chapter 12's refusal to teach Szegedy-2013 as year zero
is this correction institutionalized; (3) the misconceptions section
was the survey's most forward-looking part — it priced the
evaluation crisis before the canonical demonstrations existed, and
the field's later fifty-model audit (Croce–Hein) reads as the
empirical confirmation of a warning a survey issued on taxonomy
alone.
