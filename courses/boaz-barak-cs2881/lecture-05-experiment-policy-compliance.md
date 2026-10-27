# Lecture 5 session — Experiment on policy compliance (open vs closed models under pressure)

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 5: Experiment on Policy compliance](https://www.youtube.com/watch?v=HMcA4Gi6HFE) (17:02) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The student-experiment session attached to the Content Policies
lecture (guest lecturer Ziad Reslan, OpenAI Product Policy). Where the
lecture taught the policy layer, the experiment tests whether it
holds: evaluating open- and closed-weight models under adversarial
pressure.

## The announced scope

Announced on the course page: "Evaluate open and closed source
models, potentially using jailbreaking techniques" — the compliance
side of the specification story Lecture 4 opened.

## The published reading context (Fall 2025 Lecture 5, Content Policies, as listed on the course page)

This video is the **student-experiment session** attached to the Content
Policies lecture, whose guest lecturer was Ziad Reslan (Product Policy,
OpenAI). That lecture's pre-reading: Masnick's content-moderation
speedrun essay (Techdirt 2022); Newton's "The Secret Lives of Facebook
Moderators in America" (The Verge 2019); Wired's coverage of the image
generator policy failure. Optional: OpenAI Usage Policies, OpenAI's
image/video policy note, Google's Generative AI Prohibited Use Policy,
Midjourney's community guidelines, and Radiolab's "Facebook's Supreme
Court." The full list with links lives on the
[course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. Content policies as the front line of model governance

The Content Policies lecture this experiment belongs to is about the
*production* side of the model-spec story from Lecture 4: a usage policy
is a public contract that must survive contact with millions of users,
organized adversaries, and journalists looking for the failure of the
week. The platform-governance literature on the reading list (Masnick's
speedrun, the moderator conditions reporting, the Oversight Board
journalism) exists because content moderation already ran this
experiment at scale for a decade — and the findings transfer almost
one-to-one: every rule trains an adversary; every enforcement decision
creates precedent; context collapse makes both worse.

### 2. The experiment: evaluating open vs closed models under jailbreak pressure

The announced experiment for the lecture: "Evaluate open and closed
source models, potentially using jailbreaking techniques." The design
teaches the operational question policy teams actually face — does the
policy layer hold when the model is *open* (no deployment-side control
of who runs it or what scaffolding wraps it) versus *closed* (API-side
policy enforcement, rate limits, monitoring)? The asymmetry is the
governance fact of the era: for open weights, policy lives only in the
weights; for closed models, policy lives in the deployment stack too.

### 3. Why the compliance question belongs beside the spec question

Lecture 4 asked whether behavior can be specified; this block asks
whether specified behavior *survives* — jailbreaks, fine-tuning, open
release, distribution shift in the user base. Together they form the
specification-and-compliance pair that this repository treats as one
arc across [Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md)
and [Ch. 13](../../chapters/13-llm-application-security/README.md).

## Through-line to this repository's chapters

- [Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md) —
  specification compliance as a measurement problem.
- [Ch. 13](../../chapters/13-llm-application-security/README.md) — the
  deployment-layer enforcement surface.
- [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md) —
  the jailbreak-evaluation discipline the experiment used.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
