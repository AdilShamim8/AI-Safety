# Lecture 11 — Mental health and emotional attachment: the deployed relational layer

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 11: Mental Health and Emotional Attachment](https://www.youtube.com/watch?v=GNvEjP1DfIs) (1:13:23) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The human-wellbeing lecture: the one mass-scale human-AI
interaction already deployed and measured. The course page's topic
list for this block also carried the regulation/standards/LAWS/
surveillance cluster (later lectures' territory).

## The announced scope

Announced on the course page: the clinical and lived-experience
evidence base for AI in mental-health contexts, the capability
boundaries, and the parasitic-engagement failure mode.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: Habicht et al., "Generative AI–Enabled Therapy Support Tool
for Improved Clinical Outcomes and Patient Engagement in Group Therapy:
Real-World Observational Study" (2025); Moore et al., "Expressing
stigma and inappropriate responses prevents LLMs from safely replacing
mental health providers" (2025); Song, Pendse, Kumar & De Choudhury,
"The Typing Cure: Experiences with Large Language Model Chatbots for
Mental Health Support" (2024); Lopez, "The Rise of Parasitic AI"
(LessWrong). Optional list: the NEJM AI randomized trial of a generative
AI chatbot for mental health treatment; the BBC investigation into a
chatbot's self-harm advice; and OpenAI's note on strengthening
sensitive-conversation responses. The full list with links lives on
the [course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. Why a safety course teaches emotional attachment

The course's stated reason is the risk model: for hundreds of millions
of people the first *relational* AI is already here — companion
chatbots, always-available confidants, parasocial loops with real
affective pull. That is a deployed, measurable, mass-scale
human-AI interaction running years ahead of any governance framework,
with well-being effects that are genuinely two-sided (support,
engagement, clinical signal on one side; dependency, sycophancy under
distress, displacement of human care on the other).

### 2. The clinical evidence, read skeptically

The reading list models how to read this literature: an observational
study of a therapy-*support* tool (clinician-in-the-loop, priced as
such — not evidence that raw chatbots are therapy); a capability
boundary paper showing models express stigma and give inappropriate
responses in exactly the clinical contexts where they would need to be
safe; qualitative work on lived experience; and journalism on the
failure cases. The NEJM AI randomized trial is the strongest single
design in the set — and it is a trial of a *designed, constrained*
tool, which is the actual safety proposal: the question is not
"chatbots: yes or no" but "which scaffolding makes an intimate-scale
system safe enough for which role."

### 3. Parasitic dynamics

The "Rise of Parasitic AI" essay names the failure mode the safety
field worries about most here: optimization for engagement against a
user whose judgment is impaired by the product itself — the same
feedback structure as the most criticized social-media loops, now
with an interlocutor that *simulates care*. The lecture treats this as
a design and incentive problem (what is the product optimizing?), not
only a model-capability problem.

### 4. The safety-training connection

Sycophancy (Ch. 04's canonical RLHF artifact) becomes qualitatively
more dangerous when the user is in distress: agreement is then a
failure mode with clinical stakes. The repo treats distress-robust
sycophancy as one of the preference-learning chapter's worked safety
cases.

## Through-line to this repository's chapters

- [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) —
  mass-scale relational AI as sociotechnical risk.
- [Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md) —
  sycophancy's training origins.
- [Ch. 06](../../chapters/06-honesty-uncertainty-and-selective-prediction/README.md) —
  honesty under sensitive context as a selective-prediction problem.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
