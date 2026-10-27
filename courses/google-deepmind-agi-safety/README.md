# Google DeepMind — the AGI Safety Course

*The frontier lab's own course companion · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW) ·
[channel](https://www.youtube.com/@GDMSafetyResearch) · 16 parts, about 85 minutes total, verified
via YouTube's playlist API on 2026-10-27*

## What this course is

This is Google DeepMind's Safety Research team's own short course on AGI
safety — a compressed, deliberately accessible statement of what one frontier
lab believes the alignment problem is, and what it believes the candidate
answers are. It is not a neutral survey: it is the lab explaining itself. That
is exactly its evidential value here. Read as a **primary source for a
frontier lab's self-understanding**, it answers questions no third-party
summary can: which risks does the lab itself take seriously enough to teach
first, which interventions does it present as its own working program, and
where does its confidence sit?

The course runs about 85 minutes across 16 short videos organized in three
parts, with two pause-and-quiz exercises baked in — the structure of a course
designed for busy practitioners rather than graduate students. No
prerequisites are assumed beyond general AI literacy; every mechanism is
explained from the ground up in a few minutes each. That compression is a
feature to study, not a limitation: each part is a distilled claim about what
matters.

## The three-part structure

- **Part 1 — the risk model (5 videos + 2 exercises).** The course's own case
  that we are on a path toward superhuman capabilities, and that systems which
  plan deliberately toward instrumentally useful subgoals can pursue
  misaligned objectives. The two exercises (instrumental subgoals;
  a classification quiz for alignment failures) are the course checking
  whether the viewer can *apply* the taxonomy, not just recite it.
- **Part 2 — the alignment research program (7 videos).** The lab's candidate
  answers, one mechanism per video: the overall alignment approach, amplified
  oversight, robust training and monitoring, security and control,
  interpretability, safer design patterns, and alignment stress tests.
- **Part 3 — the institutional layer (3 videos).** What no single model or
  lab can solve alone: institutional approaches to AI safety, frontier
  safety practices, and dangerous-capability evaluations.

## The complete video index

| Video | Length | Companion note |
|---|---|---|
| [Part 0: Introduction](https://www.youtube.com/watch?v=F_q9XsN54c4) | 3:40 | [part-00-introduction.md](part-00-introduction.md) |
| [Part 1: 1. We are on a path to superhuman capabilities](https://www.youtube.com/watch?v=EnxCLOoO3XY) | 4:24 | [part-01-01-path-to-superhuman.md](part-01-01-path-to-superhuman.md) |
| [Part 1: 2. Risks from deliberate planning and instrumental subgoals](https://www.youtube.com/watch?v=DKAS2V-kbhI) | 6:41 | [part-01-02-deliberate-planning.md](part-01-02-deliberate-planning.md) |
| [Part 1: 3. Exercise 1: Instrumental subgoals](https://www.youtube.com/watch?v=fynl-QPNAhE) | 2:44 | [part-01-03-exercise-instrumental-subgoals.md](part-01-03-exercise-instrumental-subgoals.md) |
| [Part 1: 4. Where can misaligned goals come from?](https://www.youtube.com/watch?v=KKMETIVEzXA) | 9:00 | [part-01-04-misaligned-goals.md](part-01-04-misaligned-goals.md) |
| [Part 1: 5. Exercise 2: Classification quiz for alignment failures](https://www.youtube.com/watch?v=h95RgGPs-ss) | 2:25 | [part-01-05-exercise-classification.md](part-01-05-exercise-classification.md) |
| [Part 2: 1. Alignment approach](https://www.youtube.com/watch?v=RGh8wP9PjJw) | 3:44 | `part-02-01-alignment-approach.md` |
| [Part 2: 2. Amplified oversight](https://www.youtube.com/watch?v=E9nBGNi6jQA) | 6:18 | `part-02-02-amplified-oversight.md` |
| [Part 2: 3. Robust training & monitoring](https://www.youtube.com/watch?v=xhXYgIWFGkc) | 6:07 | `part-02-03-robust-training-monitoring.md` |
| [Part 2: 4. Security & control](https://www.youtube.com/watch?v=8wmZ0JK8kKM) | 5:11 | `part-02-04-security-and-control.md` |
| [Part 2: 5. Interpretability](https://www.youtube.com/watch?v=G2AenEl9A4Y) | 4:35 | `part-02-05-interpretability.md` |
| [Part 2: 6. Safer design patterns](https://www.youtube.com/watch?v=jWNPqYSH2_o) | 3:47 | `part-02-06-safer-design-patterns.md` |
| [Part 2: 7. Alignment stress tests](https://www.youtube.com/watch?v=vswXc-_Chtg) | 3:44 | `part-02-07-alignment-stress-tests.md` |
| [Part 3: 1. Institutional approaches to AI safety](https://www.youtube.com/watch?v=RsqKKuqgaMA) | 7:01 | `part-03-01-institutional-approaches.md` |
| [Part 3: 2. Frontier safety practices](https://www.youtube.com/watch?v=EtQaN6Shi-E) | 3:51 | `part-03-02-frontier-safety-practices.md` |
| [Part 3: 3. Dangerous capability evaluations](https://www.youtube.com/watch?v=00h9yaN5un4) | 6:26 | `part-03-03-dangerous-capability-evaluations.md` |

## How the course organizes knowledge

The course teaches in **claims, not chapters**. Each video is one named
mechanism or one named risk, stated at whiteboard speed, with the exercises
placed exactly where a misunderstanding would compound (after instrumental
subgoals, after the failure taxonomy). Part 2 is effectively the lab's
research agenda rendered as a curriculum — the same five buckets the repo's
Chapters 03–08 walk in depth (specification and misalignment, oversight,
robustness, control, interpretability), compressed to minutes. The course
prices itself as an on-ramp: nothing in it requires the math the repo's
chapters do, which makes it the natural first watch before starting the
common methodological spine.

## Mapping to this repository's chapters

| Course part | Repository chapters | Why |
|---|---|---|
| P1.1 superhuman path | [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) | the capability trajectory claim and its evidence discipline |
| P1.2–P1.5 planning, subgoals, misaligned goals | [Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md), [Ch. 07](../../chapters/07-deception-scheming-and-evaluation-awareness/README.md) | instrumental convergence, goal misgeneralization, the failure taxonomy |
| P2.1 alignment approach | [Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md) | what "aligned" can operationally mean |
| P2.2 amplified oversight | [Ch. 05](../../chapters/05-scalable-oversight/README.md) | oversight scaling as the core loop |
| P2.3 robust training and monitoring | [Ch. 17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md), [Ch. 18](../../chapters/18-reasoning-faithfulness-and-monitorability/README.md) | training-time robustness, deployment monitoring |
| P2.4 security and control | [Ch. 08](../../chapters/08-ai-control-and-monitoring/README.md) | the control paradigm |
| P2.5 interpretability | [Ch. 09](../../chapters/09-mechanistic-interpretability-foundations/README.md), [Ch. 10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md) | the lab's own interpretability framing |
| P2.6 safer design patterns | [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) | architecture-level safety |
| P2.7 alignment stress tests | [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md) | adversarial evaluation as alignment evidence |
| P3.1–P3.3 institutions, frontier practices, dangerous-capability evals | [Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md), [Ch. 23](../../chapters/23-governance-and-standards/README.md) | the institutional layer |

## Register entries and access levels

- **[SRC-VIDEO-013]** — the [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW) (page-inspected
  via YouTube's playlist API: 16 parts, titles and durations as listed).
- **[SRC-VIDEO-014]** — the [channel](https://www.youtube.com/@GDMSafetyResearch) (metadata-only:
  identified from the playlist's owning channel; channel page not opened).

No video was watched; no spoken content is transcribed or quoted. The
companion notes are original explanations of each part's announced topic,
anchored to the verified playlist structure above and to the literature the
repository already registers.
