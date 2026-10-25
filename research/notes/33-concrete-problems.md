# Note: Concrete Problems in AI Safety — the field's founding scope document (2016)

Source: SRC-PAPER-108 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Before this paper, "AI safety" lived mostly in philosophy-of-x-risk essays
on one side and narrow per-system engineering checklists on the other. The
paper's move — visible already in the abstract — is to define **accidents**
as "unintended and harmful behavior that may emerge from poor design of
real-world AI systems" and then to split the accident problem by *where in
the objective-function machinery the failure originates*. That taxonomy is
the reason the course can teach specification (Ch. 03), oversight (Ch. 05),
and exploration (Ch. 04) as one spine rather than three unrelated topics:
they are the three ways the objective can be wrong, expensive, or
under-sampled.

The five problems the abstract names — avoiding side effects, avoiding
reward hacking, scalable supervision, safe exploration, distributional
shift — are not five equal research areas; they are the abstract's own
causal sorting: **wrong objective** (side effects, reward hacking), **too
expensive to evaluate** (scalable supervision), **learning-process
behavior** (safe exploration, distributional shift). Reading them as a
diagnostic tree rather than a list is what makes the document durable ten
years on: every later failure mode in this course's chapters descends from
one of those three branches. Reward misspecification and proxy gaming
(Ch. 03's core) is the wrong-objective branch grown up; weak-to-strong
oversight (note 10) is the expensive-objective branch; distributional shift
(Ch. 17) kept its original name all the way into deployment reliability
engineering.

## What the abstract establishes (and what it does not)

Established at abstract-read level:

1. The field-defining definition of ML accidents quoted above — harm from
   *design*, not malice, which is why the course treats safety failures as
   engineering failures first (Ch. 01's risk-model distinction).
2. The three-origin taxonomy (wrong / expensive / process) with the five
   named problems under it.
3. That the paper reviews prior work *and* proposes research directions
   "with a focus on relevance to cutting-edge AI systems" — i.e., it was
   written as a research agenda, not a survey.

Not established at this access level: the specific prior-work citations,
the concrete research directions proposed per problem, and the closing
"how to think most productively" section's argument. The note prices
accordingly — it leans on the taxonomy, which the abstract carries in
full, and refuses to attribute specific mechanisms (e.g., the side-effects
penalty formulations the body reviews) to a body it has not read.

## Why this note exists in the course

Chapter 01 builds risk models and research epistemics before anything
else; this paper is the historical anchor for why the field's *problem
decomposition* looks the way it does. When a learner meets Ch. 03's
reward-hacking formalism or Ch. 05's oversight protocols and asks "who
decided these were THE problems?", the honest answer routes through this
document: a 2016 taxonomy that the subsequent decade of alignment research
largely filled in rather than overturned. That is also a falsifiable
observation about the field: if the taxonomy were wrong-headed, one would
expect the load-bearing problems of 2025 to sit *outside* its branches —
and the course's chapter map (specification, oversight, shift) is evidence
they mostly do not.

The paper also anchors the course's repeated distinction between
**accidents and adversaries**. The abstract's definition is explicitly
non-adversarial ("unintended and harmful behavior... from poor design");
the adversarial half of the field (Ch. 12's attacker-knowledge grid) was
already mature in 2016 through the security literature. The two halves
share the specification-blindness mechanism — which is exactly the bridge
Ch. 12 builds — but they were founded as separate literatures, and this
paper is the founding document of the accident half.

## The falsifiable extension (deterministic tier)

Take the three-origin taxonomy as a coding scheme and apply it to a
failure corpus:

- Encode the course's incident reviews (Air Canada, DPD, Chevy — and any
  session-2 additions) plus the AIID-style failure pattern list as rows.
- Code each incident on the three origins: wrong objective (the chatbot
  optimized engagement/agreement instead of policy compliance), expensive
  evaluation (no human in the loop could check the claimed policy), or
  learning-process behavior (the post-update regression in DPD).
- Prediction worth testing: production chatbot incidents concentrate in
  the *wrong objective* branch (the deployed objective under-specifies
  the policy constraint), while training-time incidents (sleeper agents,
  sandbagging notes) concentrate in *learning-process behavior*.
- Falsifier: a substantial set of incidents whose mechanism fits none of
  the three origins — e.g., pure infrastructure outages with no objective
  component — would show the taxonomy's coverage is an artifact of which
  literature the field read, not a property of failures.

This runs at the deterministic tier on markdown rows alone; no model
needed. It is the same move the content-matrix makes for chapters, pointed
at the incident record instead.
