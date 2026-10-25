# AWESOME — the annotated resource index

A map, not a link dump. Every entry below is **registered, dated, and
access-leveled** in the [source register](research/source-register.yaml);
the bracketed ID is your audit trail — click through to see exactly what
was fetched, when, and how far into it this course actually read. The
[evidence ladder](index.html) shows the whole corpus at a glance.

How to read the annotations: each line says what the source is FOR —
the load-bearing idea a chapter or project takes from it — not a
generic summary. Where a source's honest access level matters (vendor
white paper, self-reported program data), the annotation says so.

## The methodological spine

- **Concrete Problems in AI Safety** [SRC-PAPER-001] — the field's
  five-problem decomposition (reward hacking, exploration, robustness,
  oversight, side effects) that Chapter 01's risk models build on.
- **Risks from Learned Optimization** [SRC-PAPER-002] — mesa-optimization
  and the specification–optimization gap; the vocabulary for every
  "the model learned something else" analysis in Ch.03.
- **Defining and Characterizing Reward Hacking** [SRC-PAPER-006] and
  **The Effects of Reward Misspecification** [SRC-PAPER-007] — the
  Goodhart taxonomy and the misalignment-mapping methodology behind
  P02's model organisms.
- **The Benchmark Lottery** [SRC-PAPER-105] —
  why leaderboard claims need their gap×n arithmetic; the chapter's
  flip-probability drill.
- **Position: Embracing Negative Results in ML** [SRC-PAPER-107] — the
  report structure Ch.24 requires of the capstone's honest halves.

## Preference learning and post-training

- **InstructGPT** [SRC-PAPER-009] — the RLHF pipeline (SFT → reward
  model → PPO) Ch.04 dissects, including its own stated limitations.
- **DPO** [SRC-PAPER-010] — the closed-form derivation the chapter
  carries end-to-end and P04 audits at the seam.
- **Constitutional AI** [SRC-PAPER-011] — RLAIF's two-phase recipe and
  the feedback-vs-oversight distinction.
- **PPO** [SRC-PAPER-070] — the surrogate objective mechanics, verified
  at abstract level with the general-RL scope priced honestly.
- **HH-RLHF** [SRC-PAPER-071] + **BeaverTails** [SRC-PAPER-072] — the
  preference datasets P04's label-quality audit leans on (cards in the
  [dataset catalog](datasets/catalog.yaml)).

## Oversight, uncertainty, and truthfulness

- **Weak-to-Strong Generalization** [SRC-PAPER-013] — the oversight gap
  P05 reproduces as a deterministic analogue.
- **Measuring Progress on Scalable Oversight** [SRC-PAPER-014] and
  **AI Safety via Debate** [SRC-PAPER-015] — the two oversight
  paradigms comparison note C03 adjudicates.
- **Language Models (Mostly) Know What They Know** [SRC-PAPER-016] and
  **Teaching Models to Express Uncertainty in Words**
  [SRC-PAPER-017] — the logit vs verbalized confidence channels of
  Ch.06; the second is the spoofable one.
- **Towards Understanding Sycophancy** [SRC-PAPER-018] — preference
  pipelines training in flattery; Ch.06's pressure mechanism.
- **TruthfulQA** [SRC-PAPER-073; dataset card DS-001] — imitative
  falsehoods as a construct-validity worked example.

## Deception evidence (the skeptical canon)

- **Sleeper Agents** [SRC-PAPER-019] — persistence of deceptive
  behavior through safety training; the constructed-organism evidence
  class.
- **Alignment Faking** [SRC-PAPER-020] — conditional compliance
  statistics (the 14%-in-context vs 78%-after-RL pair) and what they
  do and do not show.
- **AI Sandbagging** [SRC-PAPER-021] — strategic underperformance on
  evaluations; the gameability limit of benchmarks.
- **AI Control** [SRC-PAPER-022] + **Evaluating Control Protocols**
  [SRC-PAPER-023] + **Adaptive Attacks on Trusted Monitors**
  [SRC-PAPER-024] — the control paradigm Ch.08 teaches and P08
  implements (the monitor's recall is the safety ceiling).

## Interpretability

- **A Mathematical Framework for Transformer Circuits**
  [SRC-PAPER-025] — the residual stream / QK-OV / MLP decomposition
  Ch.09 is built on.
- **Causal Mediation Analysis** [SRC-PAPER-027] — the TE/IE/DE
  formalism behind activation patching.
- **Towards Monosemanticity** [SRC-PAPER-030] and **Scaling
  Monosemanticity** [SRC-PAPER-032] — dictionary learning and the
  feature-splitting story (the San Francisco 1→2→11 example, verified
  verbatim).
- **Refusal Is Mediated by a Single Direction** [SRC-PAPER-037] — the
  refusal direction Ch.11's steering audit re-prices with full
  intervals.
- **Probing Classifiers: Promises, Shortcomings, Advances**
  [SRC-PAPER-039] — why readout ≠ causation (P06's opening move).
- **Faithfully Interpretable NLP Systems** [SRC-PAPER-034] —
  faithfulness vs plausibility, the Ch.10 evidence standard.

## Adversarial ML and defense evaluation

- **Intriguing Properties** [SRC-PAPER-040] + **Explaining and
  Harnessing** [SRC-PAPER-046] — the founding transfer and
  linear-explanation results.
- **BadNets** [SRC-PAPER-042] — supply-chain poisoning with the
  25%-accuracy-drop trigger; the backdoor archetype.
- **Membership Inference** [SRC-PAPER-041] + **Stealing Models via
  Prediction APIs** [SRC-PAPER-043] — the privacy/extraction pair
  Ch.12 and Ch.16 use.
- **Carlini-Wagner** [SRC-PAPER-044] — the 100%-vs-claimed-0.5%
  distillation autopsy; defense evaluation's founding failure.
- **Reliable Evaluation of Adversarial Robustness** [SRC-PAPER-047]
  and **On Evaluating Adversarial Robustness** [SRC-PAPER-048] — the
  ensemble/50+-model audits that make "our defense works" a testable
  claim.

## LLM application and agent security

- **Not What You've Signed Up For** [SRC-PAPER-050] — Greshake's
  indirect injection taxonomy; the Ch.13 backbone.
- **Ignore Previous Prompt** [SRC-PAPER-051] — goal hijacking and
  prompt leaking as named classes.
- **The Instruction Hierarchy** [SRC-PAPER-052] — privileged-instruction
  training, honestly priced (same-channel defense).
- **Spotlighting** [SRC-PAPER-053] — delimiter defenses with measured
  ASR (the >50%→<2% pricing Ch.13 carries).
- **Defeating Prompt Injections by Design** [SRC-PAPER-054] — Dual LLM
  and CaMeL; the architecture-level boundary family.
- **AgentDojo** [SRC-PAPER-055] + **LM Agents with an LM-Emulated
  Sandbox** [SRC-PAPER-056] — agent attack surfaces and the
  ToolEmu-style evaluation topology behind P07/P10 fixtures.
- **Programming Semantics for Multiprogrammed Computations**
  [SRC-PAPER-057] — Dennis & Van Horn 1966: capabilities as the
  still-correct vocabulary for tool calls.
- **OWASP LLM Top 10 (2025)** [SRC-REPORT-004] — the industry risk
  index Ch.13 maps onto (page-verified at the listed version).

## Red teaming

- **Red Teaming Language Models to Reduce Harms** [SRC-PAPER-058] —
  38,961 released attacks and the human-scaling trend.
- **Red Teaming with Language Models** [SRC-PAPER-059] — LM-vs-LM
  attack generation.
- **Explore, Establish, Exploit** [SRC-PAPER-060] — from-scratch red
  teaming and the marginal-value inversion.
- **XSTest** [SRC-PAPER-003; dataset DS-006] — over-refusal as a
  safety failure of the second kind; the 250/200 structure the
  chapter's benign controls mirror.

## Reasoning, release, and governance

- The CoT-faithfulness set Ch.18 uses: [SRC-PAPER-083..087] —
  plausibility-vs-faithfulness, the monitorability tax, the oversight
  flip, self-instructed evasion; two at high-recency honesty.
- **Evaluating Frontier Models for Dangerous Capabilities**
  [SRC-PAPER-094] — the evaluation-suite approach to release gates
  Ch.20 builds its release discipline on.
- **Are Emergent Abilities a Mirage?** [SRC-PAPER-095] — why
  emergent-capability claims need the scaling curves under them; the
  metric-choice lesson of Ch.20.
- **Anthropic RSP** [SRC-REPORT-005] and **OpenAI Preparedness**
  [SRC-REPORT-006, with its 404 recorded] — the labs' own frameworks,
  fetched at page level where they were reachable.
- **NIST AI RMF 1.0** [SRC-REPORT-010] — the four functions Ch.23
  maps with citation forensics (JS-rendering honesty noted).
- **MITRE ATLAS** [SRC-REPORT-011] — the adversarial knowledge base,
  pinned at fetch (16/208/40/73 counts, living-database caveat).
- EU AI Act [SRC-REPORT-012] — the timeline arithmetic (Annex III 405
  days, Annex I 649 days out at verification date) Ch.23 teaches as
  phase-in discipline.

## The dataset catalog (22 verified cards)

Not repeated here — the cards ARE the annotation:
[datasets/catalog.yaml](datasets/catalog.yaml). Each card traces every
composition number to the URL it was collected from, with license and
contamination status. Start with TruthfulQA [DS-001], AdvBench
[DS-009], and XSTest [DS-006] — the three the projects use most.

## Courses, fellowships, and the from-scratch track

- **ARENA curriculum** [SRC-CURR-001] — the ML-engineer-side safety
  curriculum this course's prerequisites are calibrated against.
- **The from-scratch video course** [SRC-VIDEO-001] + its MIT companion
  repo [SRC-REPO-001] — the owner-selected mechanics track
  (research/ai-researcher-from-scratch/), distilled into 7 module
  notes with runnable stdlib code.
- **MATS** [SRC-CURR-006] — the alignment fellowship (12 weeks,
  Berkeley/London; self-reported outcomes priced as such in the
  register).
- **80,000 Hours AI hub** [SRC-CURR-005] — entry paths, advising, the
  900+-role board; the careers index's structure source.
- **BlueDot Impact** (named on the 80k hub [SRC-CURR-005]) — free
  entry-level courses; the community on-ramp.

## The note companions (start from the map, land in the notebook)

The research notebook now carries 32 paper notes and 6 comparison
notes — each anchored to a register source at the level the access
supports, each ending in a falsifiable extension runnable at course
scale. The fastest way in: the chapter you are reading names its
note companions in the readings section; the full index is
[research/notes/README.md](research/notes/README.md). The notes added
in the 2026-10-25 session alone: CaMeL (21 — the boundary that moved
out of the model), AgentDojo (22 — the environment as the
instrument), Sandbagging (23 — the evaluation channel's gameability),
Explore-Establish-Exploit (24 — red teaming as method), DPO (25 — the
reparameterization), InstructGPT (26 — the pipeline), Debate (27 —
the optimality assumption), Sycophancy (28 — the preference pipeline),
Mirage (29 — metric choice manufactures thresholds), Constitutional
AI (30 — supervision in a document), GCG (31 — the optimized attack),
Verbalized confidence (32 — the trained channel), plus comparison C06
(safety cases vs red-team reports — assurance's two documents).

## The incident record

Three production incidents reviewed under the strict template
([notes/incidents/](research/notes/incidents/README.md)): Air Canada
liability [SRC-REPORT-013], DPD release regression [SRC-REPORT-014],
Chevy commitment authority [SRC-REPORT-015/016]. The AI Incident
Database [SRC-REPORT-015's host] is the field-wide record this
collection grows from — cite entries by ID with fetch dates.

## Career market data (perishable — re-verify before deciding)

- **AISafety.com jobs board** [SRC-CURR-007] — 553 roles at fetch
  (2026-10-25), employer-disclosed salary examples included.
- **SANS AI cybersecurity careers white paper** [SRC-CURR-008] — the
  four titles hiring today, from 10,643 postings; vendor-mapped to its
  own curriculum (the caveat is the lesson).
- Both live in [roadmaps/careers-index.md](roadmaps/careers-index.md)
  with per-claim provenance and the five-rung progress ladder.
