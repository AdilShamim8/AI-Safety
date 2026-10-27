# SYLLABUS — the 24-unit course catalog

One row per chapter unit: what it teaches, what it requires, what it produces.
Depth is not uniform by design: difficult concepts get more space, and
cross-links replace repetition. Chapter directories carry the full treatment
(each with exercises, readings with reasons, and completion criteria); this
page is the map. Completion state lives truthfully in
[planning/STATUS.md](planning/STATUS.md) and `planning/content-matrix.yaml`.
Companion pages: the whole build as a generated dashboard
([index.html](index.html)), the annotated resource index
([AWESOME.md](AWESOME.md)), the route pages
([roadmaps/](roadmaps/) — including [audit-only](roadmaps/audit-only.md)),
the careers mapping ([roadmaps/careers-index.md](roadmaps/careers-index.md)
with [first-90-days.md](roadmaps/first-90-days.md)), and the
verification discipline every reading assumes
([prerequisites/verifying-sources.md](prerequisites/verifying-sources.md)).

| ID | Chapter | Hard prerequisites | Core artifact | Projects |
|---|---|---|---|---|
| 01 | Risk models and research epistemics — hazard/capability/propensity/exposure/severity, causal pathways, operationalization, evidence hierarchies, uncertainty | — | threat hypothesis with weakening observations | — |
| 02 | Evaluation science and experimental design — construct validity, provenance, grouped splits, contamination, adaptive overfitting, power, cluster-aware intervals, effect sizes, reproducibility | 01 | preregistered evaluation plan | P01 |
| 03 | Specification, reward hacking, goal misgeneralization — proxy vs capability vs learned-goal failure, Goodhart, distribution shift | 01 | counterexample analysis + bounded experiment | P02 |
| 04 | Preference learning and post-training — reward modeling, KL regularization, SFT, PPO-style RLHF, DPO, RLAIF, Constitutional AI; what objectives do and don't imply | 03 | one derived objective + label-quality audit | P04 |
| 05 | Scalable oversight — weak-to-strong, debate, decomposition, process vs outcome supervision, correlated errors | 02 | bounded comparison with checkable ground truth | P05 |
| 06 | Honesty, uncertainty, selective prediction — calibration, abstention, risk–coverage, sycophancy; why verbal confidence ≠ truth probability | 02 | calibration analysis | P03 |
| 07 | Deception, scheming, evaluation awareness — model organisms, alignment faking, sandbagging; evidence vs extrapolation | 03 | skeptical evidence table | — |
| 08 | AI control and monitoring — trusted/untrusted assumptions, audit budgets, deferral, adaptive red teams, collusion, safety–usefulness | 05 | control protocol with failure conditions | P08 |
| 09 | Mechanistic interpretability foundations — residual streams, attention/MLP contributions, causal interventions, patching with controls | 02 | causal claim with controls | P06 |
| 10 | Sparse features, circuits, interpretability evaluation — superposition, SAE reconstruction vs usefulness, faithfulness, completeness | 09 | SAE/circuit critique | — |
| 11 | Behavioral steering and representation interventions — probes, steering, linear assumptions, confounds, side effects | 09 | held-out intervention evaluation | — |
| 12 | Adversarial ML and robustness — evasion, poisoning, backdoors, extraction, membership inference; attacker knowledge; adaptive evaluation | 02 | threat-model comparison | — |
| 13 | LLM application security — direct/indirect injection, trust boundaries, output handling, retrieval risks; why prompts-as-defense fails | 12 | injection-to-framework mapping | P07 |
| 14 | Agent, tool, memory, MCP security — capability-based access, least privilege, delegation, authorization, isolation, dependency compromise | 13 | privilege & trust-boundary matrix | P07 |
| 15 | Red teaming and adversarial evaluation — coverage, adaptive attacks, benign controls, scoring with denominators, over-refusal, responsible reporting | 02, 13 | attack/defense report | P07, P10 |
| 16 | Privacy, provenance, supply chains — memorization, privacy accounting concepts, model artifacts, licenses, dependency integrity | 02 | provenance audit | — |
| 17 | Distribution shift and deployment reliability — OOD, worst-group, drift, uncertainty under shift; covariate vs label vs concept change | 02 | shift-taxonomy analysis | P09 |
| 18 | Reasoning faithfulness and monitorability — CoT faithfulness, hidden actions, monitor evasion; action/outcome evidence | 08 | faithfulness critique | — |
| 19 | Multimodal and embodied safety — cross-modal injection, perceptual failure, sensor shift, sim-to-real limits | 13 | worked multimodal case | — |
| 20 | Misuse, dangerous capabilities, release evaluation — elicitation, access conditions, safeguards, dual-use, release decisions (non-operational) | 15 | release-evaluation design | — |
| 21 | Sociotechnical and systemic risk — automation bias, disparate impact, incentives, power, stakeholders, linguistic coverage | 01 | stakeholder & failure-pathway analysis | — |
| 22 | Safety engineering and assurance — hazard analysis (FMEA/STPA-style), assurance claims, evidence, rebuttals, residual risk | 01, 08 | safety-case draft | P10 |
| 23 | Governance and standards — NIST AI RMF, NIST AML taxonomy, MITRE ATLAS, OWASP GenAI, GPAI guidance, responsible scaling; guidance vs obligation vs proposal | 22 | standards mapping with versions | — |
| 24 | Research practice and capstone execution — scoping, baselines, falsifiability, preregistration, ablations, negative results, ethical release | 02, 22 | research proposal + capstone report | P10 |

## The watching track (2026-10-27)

The [lecture library](courses/README.md) adds a video layer to this
syllabus: four external courses — Harvard CS 2881, the Google
DeepMind AGI Safety Course, the CAIS Ethics & Society course, and the
Safeshield governance series — each with a course page, verified
video index, and one companion note per lecture. The library does not
change the chapter sequence; it schedules watching against it (see
[courses/study-plans.md](courses/study-plans.md)): the DeepMind
course as the 90-minute primer before Chapter 01, the alongside pass
paired chapter-cluster by chapter-cluster, and the Safeshield series
as the operator spine for the assurance-oriented routes. Each
chapter's README carries its own "watching companions" block with the
specific pairings and the reason for each.

## How chapters are assessed

Each chapter carries: two demanding exercises (one analysis/derivation, one
empirical/design/critical), hints and worked solutions or an assessor rubric
published separately from the prompts, and a concrete completion artifact
(the "core artifact" column above) with explicit completion criteria. Rubrics
live in `assessment/` as chapters land. Reading lists are 2–4 essential
primary sources with reasons and section pointers, verified in the
[source register](research/source-register.yaml) at the stated access level.

## Where the projects attach

P01 evaluation harness (Ch.02) · P02 reward misspecification (Ch.03) ·
P03 calibration/abstention (Ch.06) · P04 preference optimization audit
(Ch.04) · P05 weak-to-strong analogue (Ch.05) · P06 causal interpretability
(Ch.09–11) · P07 injection defense (Ch.13–15) · P08 control protocol (Ch.08) ·
P09 shift/subgroup reliability (Ch.17) · P10 capstone assurance dossier
(Ch.22+24). Full specifications land with each project's directory;
requirements are tracked in `planning/content-matrix.yaml`.

## Scope boundaries (course-level)

The course covers present-day demonstrated harms and uncertain frontier
risks, keeping them separate: malicious use, unintended failures,
loss-of-control hypotheses, and systemic effects are treated with different
evidence standards, not as one undifferentiated "risk." High-consequence
misuse domains stay non-operational (evaluation and governance level only).
No chapter promises a safety proof; every chapter includes where its methods
fail.
