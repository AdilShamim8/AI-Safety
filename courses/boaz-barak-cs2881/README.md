# Harvard CS 2881 — AI Safety (Boaz Barak)

*The graduate-seminar course companion · [playlist](https://www.youtube.com/playlist?list=PL_b4B2IWlal3j01Rbj5ebT663E7x4bl_W) ·
[channel](https://www.youtube.com/@boazbarak2878) · [course page](https://boazbk.github.io/mltheoryseminar)
(read in full 2026-10-27)*

## What this course is

CS 2881 (taught first as CS 2881R in Fall 2025, again as CS 2881 in
Fall 2026) is Harvard's graduate course on the alignment and safety of
artificial intelligence, taught by Boaz Barak — a theoretical computer
scientist at Harvard who is also a member of the technical staff at
OpenAI, a dual role the course page discloses explicitly on its
conflict-of-interest note. The course is a **research seminar, not a
survey**: thirteen in-person lectures (Thursdays, 3:45–6:30pm), each
built around a discussion of required pre-readings, a guest lecture or
Q&A from a working researcher or practitioner, and the live presentation
of a **student experiment** — a small empirical study the students ran
that week and defend in front of the room.

The prerequisites are stated plainly on the course page: mathematical
maturity (proofs, probability, information theory), machine learning at
the level of Harvard CS 181 or MIT 6.036, and enough Python to train a
basic neural network. This is the most technically demanding of the four
courses in this library, and it is priced accordingly in the mapping
below: its lectures are the deep end of the repository's chapter
sequence, not the on-ramp.

The course's own framing — stated in its introduction blog and visible
in every lecture's design — hangs on **two axes: measurement and
scale**. Measurement, because "you can't improve what you don't
measure," and because alignment and safety make measurement harder than
capability work does (worst-case behavior, multi-component interactions,
"cheating" that resists definition). Scale, because current AI systems
are not static: every safety question must be asked twice — does this
problem get better or worse as the system grows, and does this
intervention work better or worse at scale? Those two axes are a
genuinely useful lens, and they recur across the companion notes.

## The two iterations in one playlist

The [playlist](https://www.youtube.com/playlist?list=PL_b4B2IWlal3j01Rbj5ebT663E7x4bl_W) (19 videos, verified via YouTube's
playlist API on 2026-10-27) mixes the completed Fall 2025 course
(12 lecture recordings, plus experiment-only recordings) with the Fall
2026 course as its recordings publish (the Fall 2026 lecture list is on
the course page through December 2026). Where both iterations cover the
same ground — modern LLM training, economics — the companion notes
treat the Fall 2026 version as current and the Fall 2025 version as the
archived prior art, and say so in each note. Guest lectures the course
page records for Fall 2026 but not yet published as recordings are
listed in the schedule below as **announced, not yet in the playlist**
— the honest state of a course that is still being taught.

## The complete video index

### Fall 2025 iteration (complete; 12 lectures)

| Lecture | Video | Length | Companion note |
|---|---|---|---|
| L1 | [Introduction — AI 2027, normal technology, and what this course asks](https://www.youtube.com/watch?v=-NCiWaRS6So) | 2:25:51 | [lecture-01-introduction.md](lecture-01-introduction.md) |
| L2 | [Modern LLM training and safety training](https://www.youtube.com/watch?v=GXggPt_gqiI) | 2:23:02 | [lecture-02-modern-llm-training.md](lecture-02-modern-llm-training.md) |
| L3 | [Robustness — adversarial examples, jailbreaks, prompt injection, weight security](https://www.youtube.com/watch?v=pfKO4MlvM-Y) | 1:36:26 | [lecture-03-adversarial-robustness.md](lecture-03-adversarial-robustness.md) |
| L4 | [Model Specs — specifications and compliance](https://www.youtube.com/watch?v=LQ0RRQKKluc) | 2:06:04 | [lecture-04-model-specifications.md](lecture-04-model-specifications.md) |
| L5 | [Experiment on policy compliance (student experiment session)](https://www.youtube.com/watch?v=HMcA4Gi6HFE) | 17:02 | [lecture-05-experiment-policy-compliance.md](lecture-05-experiment-policy-compliance.md) |
| L6 | [Recursive Self Improvement](https://www.youtube.com/watch?v=wzep3Rnv6iw) | 2:29:33 | [lecture-06-recursive-self-improvement.md](lecture-06-recursive-self-improvement.md) |
| L7 | [Lab vs Field — capabilities vs. safety (Joel Becker, METR)](https://www.youtube.com/watch?v=fuRmxFZ-umE) | 2:01:36 | [lecture-07-lab-vs-field.md](lecture-07-lab-vs-field.md) |
| L8 | [Scheming — reward hacking and deception](https://www.youtube.com/watch?v=8NL1NAMrJxY) | 10:18 | [lecture-08-scheming.md](lecture-08-scheming.md) |
| L8 | [Experiment: Under Pressure — coding agents under impossible tasks](https://www.youtube.com/watch?v=JXvHJheHE10) | 33:52 | [lecture-08-experiment-under-pressure.md](lecture-08-experiment-under-pressure.md) |
| L9 | [Economic Impacts of AI](https://www.youtube.com/watch?v=4vQSMijp_M8) | 2:32:33 | [lecture-09-economic-impacts.md](lecture-09-economic-impacts.md) |
| L10 | [Mechanistic Interpretability](https://www.youtube.com/watch?v=79otWC2FQlE) | 2:30:24 | [lecture-10-mechanistic-interpretability.md](lecture-10-mechanistic-interpretability.md) |
| L11 | [Mental Health and Emotional Attachment](https://www.youtube.com/watch?v=GNvEjP1DfIs) | 1:13:23 | [lecture-11-mental-health.md](lecture-11-mental-health.md) |
| L12 | [AI in 2035 and GDPval](https://www.youtube.com/watch?v=BNSHJLLpsGM) | 1:47:41 | [lecture-12-ai-2035-and-gdpval.md](lecture-12-ai-2035-and-gdpval.md) |

The Fall 2025 archive page also records a short course clip —
["When the earth dies (codex clip)"](https://www.youtube.com/watch?v=4JqWA2sgStc) (3:04)
— used as teaching material; it is indexed here for completeness and
covered inside the notes that use it, not as its own note. The
`note` column fills in link by link as each companion note lands
(plain filename = not yet written — the same in-progress honesty the
library index holds).

### Fall 2026 iteration (recordings publish as the course proceeds)

| Lecture | Video | Length | Companion note |
|---|---|---|---|
| L1 | [Introduction (Fall 2026)](https://www.youtube.com/watch?v=j4WSktB5Ni0) | 2:31:25 | [f26-lecture-01-introduction.md](f26-lecture-01-introduction.md) |
| L3 | [Modern LLM Training and Inference (Fall 2026)](https://www.youtube.com/watch?v=Lp_e8Ts5-nE) | 1:16:37 | [f26-lecture-03-modern-llm-training-inference.md](f26-lecture-03-modern-llm-training-inference.md) |
| L5 | [Economic Impact of AI (Fall 2026)](https://www.youtube.com/watch?v=iezRKFkyjVY) | 2:25:27 | [f26-lecture-05-economic-impact.md](f26-lecture-05-economic-impact.md) |
| L8 | [Open Language Models (Nathan Lambert, Fall 2026)](https://www.youtube.com/watch?v=0L-DGRn52Q0) | 1:31:00 | [f26-lecture-08-open-language-models.md](f26-lecture-08-open-language-models.md) |
| projects | [Oral presentations of student projects (Fall 2026)](https://www.youtube.com/watch?v=Xr9FNl0S66Q) | 1:15:41 | [f26-oral-presentations.md](f26-oral-presentations.md) |

Announced on the Fall 2026 course page but not yet in the playlist:
Cyber Capabilities (Nicholas Carlini, Anthropic); Recursive
Self-Improvement and AI Trajectories (Dwarkesh Patel and Daniel
Kokotajlo); Grading, Reward Hacking and Alignment (John Schulman);
Model Policies (Ziad Reslan); Frontier AI Regulation Under Uncertainty
(Helen Toner); AI Interpretability and Model Welfare (Jack Lindsey and
Jeff Sebo); Alignment in the Age of Recursive Self-Improvement (Jakub
Pachocki); AI Biosecurity and Threat Modeling (Luca Righetti and Brad
Carson); and the December session with Ajeya Cotra and Roy Rinberg.
This list is the course page's own announcement record as read on
2026-10-27 — recordings may follow with delay (the page says
publishing is intended "to the extent technically possible").

## How the course organizes knowledge

Barak's course is organized as a **weekly research seminar with an
evidence discipline**. Each lecture is one topic, prepared by required
readings discussed in advance on Perusall (an annotation forum where
substantive comments are part of the grade), anchored by a guest who
works on that topic, and grounded by a student experiment presented
live. The readings are primary sources — incident reports, technical
reports, preprints — read the way a researcher reads: for what they
establish, what they assume, and what they leave out. The experiments
are small but real: students fine-tune models, run red-team exercises,
measure reward hacking, and present failures as findings. The course
also runs scribe notes and a final project, and it encourages students
to use AI tools throughout — the course's own position is that using
the systems you are studying is part of studying them.

The companion notes in this directory keep that structure: each note
carries the lecture's announced scope, the reading list as published on
the course page, an original explanation of the load-bearing ideas, and
the connections into this repository's chapters and paper spine.

## Mapping to this repository's chapters

| Course lecture | Repository chapters | Why |
|---|---|---|
| L1 Introduction | [Ch. 01](../../chapters/01-risk-models-and-research-epistemics/README.md) | risk models, evidence discipline, forecasting disagreement |
| L2 Modern LLM training | [Ch. 04](../../chapters/04-preference-learning-and-post-training/README.md) | RLHF/RLVR, safety training, distillation |
| L3 Robustness | [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md), [Ch. 13](../../chapters/13-llm-application-security/README.md), [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md) | adversarial examples, jailbreaks, prompt injection, weight security |
| L4 Model Specs | [Ch. 03](../../chapters/03-specification-reward-hacking-and-goal-misgeneralization/README.md) | specification, compliance, interpretive lessons from law |
| L6 Recursive Self-Improvement | [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md), [Ch. 24](../../chapters/24-research-practice-and-capstone-execution/README.md) | takeoff models, AI R&D automation, growth scenarios |
| L7 Lab vs Field | [Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md), [Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md) | METR measurements, RSPs, capabilities evaluations |
| L8 Scheming | [Ch. 07](../../chapters/07-deception-scheming-and-evaluation-awareness/README.md), [Ch. 08](../../chapters/08-ai-control-and-monitoring/README.md) | alignment faking, evaluation awareness, control protocols |
| L9 Economic Impacts | [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) | labor substitution, inequality, productivity evidence |
| L10 Interpretability | [Ch. 09](../../chapters/09-mechanistic-interpretability-foundations/README.md), [Ch. 10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md), [Ch. 11](../../chapters/11-behavioral-steering-and-representation-interventions/README.md) | SAEs, circuits, steering, CoT monitoring |
| L11 Mental Health | [Ch. 21](../../chapters/21-sociotechnical-and-systemic-risk/README.md) | emotional attachment, parasitic AI, clinical evidence |
| L12 AI in 2035 / GDPval | [Ch. 20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md) | GDPval as a real-world economics-of-AI dataset |
| Fall 2026 lectures | same chapters, current readings | the mapping is by topic, not iteration |

## Register entries and access levels

- **[SRC-VIDEO-011]** — the [playlist](https://www.youtube.com/playlist?list=PL_b4B2IWlal3j01Rbj5ebT663E7x4bl_W) (page-inspected
  via YouTube's playlist API: 19 videos, titles and durations as listed).
- **[SRC-VIDEO-012]** — Boaz Barak's [channel](https://www.youtube.com/@boazbarak2878)
  (metadata-only: identified from the videos' owning channel; channel
  page not separately opened).
- **[SRC-CURR-012]** — the [course page](https://boazbk.github.io/mltheoryseminar)
  (full-text-read: the Fall 2026 schedule and the Fall 2025 archive,
  including every lecture's readings and experiments, read on
  2026-10-27).

No video was watched; no spoken content is transcribed or quoted. The
companion notes are original explanations anchored to the verified
structure above.
