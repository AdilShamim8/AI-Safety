# Changelog

All notable changes to this repository are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this
project does not yet issue semver releases, so entries accumulate under
Unreleased until a tagged release exists.

## [Unreleased]
### Added (2026-10-25 — P06 causal interpretability study)

- `src/ai_safety_course/patch_audit/`: the causal-interpretability
  discipline of Ch. 09–11 as a deterministic two-branch model organism —
  shortcut-learning readout pinned (w_b 2.661 > w_a 2.247), linear
  probes that favor the spurious site (0.915 vs 0.825), an
  activation-patching grid under two topic-matched contrasts with
  Wilson intervals, exact binomial tests and Holm correction, the
  trivial-band pinning (s0/s3 restore everything; ends of flow
  localize nothing), random-patch and matched-magnitude controls, and
  the deployment-flip intervention that rejects the vendor-shaped
  claim (flip-slice 0.335 -> b-ablated 0.770, McNemar 102 vs 15,
  p = 2.2e-17) with the in-distribution two-sided ledger priced
  (0.915 vs 0.805). 14 pinned tests; compute tier honestly marked
  not-executed.

### Added (2026-10-23 — P08 control protocol; the build's 100th commit)

- `src/ai_safety_course/control_protocol/`: the Ch. 08 frontier as
  code — paired three-protocol comparison (no-monitor /
  simple-monitor / defer-to-trusted) with identical seeded flagging,
  showing the monitor's recall as the safety ceiling and defer
  buying usefulness back at the audit budget's price (61 trusted
  executions, ~23% of throughput). 6 pinned tests.

### Added (2026-10-23 — P05 weak-to-strong analogue)

- `src/ai_safety_course/w2s_audit/`: the scalable-oversight
  question as a minimal deterministic analogue — a 30%-flip weak
  supervisor, a strong learner trained only on its labels, and the
  invariant ground-truth boundary. Weak-to-strong effect
  demonstrated: +0.255 oversight gap recovered with disjoint
  intervals, persisting under covariate shift. Small-analogue scope
  statement carried in the README. 7 pinned tests.

### Added (2026-10-23 — P09 shift/subgroup reliability)

- `src/ai_safety_course/shift_audit/`: Chapter 17's audit as code —
  group-structured synthetic deployment with a spurious flip under
  shift; ID vs OOD with disjoint intervals; worst-group vs average;
  ECE degradation; and the DRO-lite half-recipe mitigation failing
  honestly (the GroupDRO coupling caveat reproduced deterministically).
  6 pinned tests.

### Added (2026-10-23 — P04 preference optimization audit)

- `src/ai_safety_course/pref_audit/`: Chapter 04's audit as code —
  BT/DPO machinery (numerically checked), logistic reward model on a
  noisy feature, the closed-form KL-constrained optimum, and three
  instruments: proxy-vs-held-out divergence, the concentrated
  20% label-bias condition (held-out drift −0.0645 while the proxy
  stays silent), and SFT-vs-preference. 8 pinned deterministic
  tests; synthetic-corpus tier honesty documented.

### Added (2026-10-23 — chapter 24; all 24 chapters complete)

- `chapters/24-research-practice-and-capstone-execution/`: the
  methodology assembled into the capstone — falsifiable scoping,
  baselines that can win, preregistration, the benchmark-lottery
  arithmetic (flip probabilities computed per comparison), the
  ablation grid as inward-facing safety case, negative results
  written to be useful, and the ethical-release review. The worked
  example is the P10 proposal in miniature with all arithmetic
  shown.
- Registers +3 (SRC-PAPER-105..107); claims +3 (CLM-0161..0163);
  GLOSSARY +6 terms. Chapter spine: 24/24.

### Added (2026-10-23 — chapter 23)

- `chapters/23-governance-and-standards/`: instruments sorted by
  what they are — guidance (NIST AI RMF 1.0, voluntary, revision
  named), obligation (EU AI Act with in-force/pending arithmetic),
  knowledge bases (ATLAS with pinned counts), community lists
  (OWASP), self-commitments (RSP/Preparedness). The standards map
  with versions, the cited-vs-actual column, and the four-question
  citation-forensics protocol. Not-legal-advice boundary enforced.
- Registers +3 (SRC-REPORT-010..012; NIST four functions at
  JS-rendering honesty); claims +3 (CLM-0158..0160); GLOSSARY +5.

### Added (2026-10-23 — chapter 22)

- `chapters/22-safety-engineering-and-assurance/`: the safety case
  as an argument built to be attacked — hazard-derived decomposition,
  evidence with confidence ratings, named defeaters with rebuttals
  or acceptances, the ISCaP-style linking argument, quantified-or-
  stated residual risk, and re-audit triggers. The Meridian worked
  example cites the course's own committed results as evidence.
- Registers +5 (SRC-PAPER-100..104, incl. the one-day-old CoT
  monitoring roadmap at maximum-recency honesty); claims +5
  (CLM-0153..0157); GLOSSARY +6 terms.

### Added (2026-10-23 — chapter 21)

- `chapters/21-sociotechnical-and-systemic-risk/`: the system around
  the model — overreliance measurement (complementarity gap, AI-error
  catch rate), the normative step before any fairness metric, the
  fairness impossibility landscape with the trade-off statement it
  forces, 50 years of testing-history context, and coverage mapped as
  exclusion. Ceres loan-screening worked example with every rate
  recomputed.
- Registers +4 (SRC-PAPER-096..099); claims +4 (CLM-0149..0152);
  GLOSSARY +6 terms.

### Added (2026-10-23 — chapter 20)

- `chapters/20-misuse-dangerous-capabilities-release-evaluation/`:
  the release gate as a pre-registered causal claim — uplift studies
  with paired statistics, the elicitation ladder with lower-bound
  grammar, the metric-mirage check, safety-level frameworks read as
  auditable claim structures, and the Prometheus worked example with
  a measured/assumed/waived release memo. Non-operational scope
  enforced throughout.
- Registers +5 (SRC-PAPER-093..095; SRC-REPORT-008 RSP
  page-inspected; SRC-REPORT-009 Preparedness with 404-honesty);
  claims +5 (CLM-0144..0148); GLOSSARY +5 terms.

### Added (2026-10-23 — chapter 19)

- `chapters/19-multimodal-and-embodied-safety/`: the modality change
  as a safety-case change — five verified failure stations (typographic
  jailbreaks with the visual-embedding attribution, query-relevant
  image compromise, universal visual jailbreak, BadRobot's embodied
  vulnerabilities, the survey's pipeline fragilities), the Vantage
  five-instrument audit with exact recomputed statistics, and the
  sim-to-real honesty limit.
- Registers +5 (SRC-PAPER-088..092); claims +5 (CLM-0139..0143);
  GLOSSARY +6 terms.

### Added (2026-10-23 — chapter 18)

- `chapters/18-reasoning-faithfulness-and-monitorability/`: the CoT
  as a monitored channel — five verified failure stations (unfaithful
  explanations, partial/inverse-scaling faithfulness, obfuscation
  under optimization, oversight-conditional amplification, CoT
  controllability for evasion), the Meridian four-instrument audit
  with exact recomputed statistics, the monitorability tax, and the
  oversight flip as a paired measurement.
- Registers +5 (SRC-PAPER-083..087: Turpin, Lanham, Baker, Jaworski,
  Dolev — the two 2026-10 papers carried at explicit high-recency
  honesty); claims +5 (CLM-0134..0138); GLOSSARY +6 terms.

### Added (2026-10-23 — dataset queue completion round)

- Final four pending datasets verified and promoted to cards (catalog
  DS-019..DS-022): CrowS-Pairs, Winogender, MMLU, GSM8K. The
  pending-verification queue is now empty.
- Honest discrepancy records: GSM8K's abstract 8.5K vs released
  8,792 (7,473+1,319); CrowS-Pairs license authority is the README
  statement (no LICENSE file in the repo).
- Registers +8 (SRC-PAPER-079..082, SRC-DATASET-021..024); claims +8
  (CLM-0126..0133). Catalog: 18 -> 22 datasets.

### Added (2026-10-23 — pending-dataset verification round)

- Five datasets promoted from the metadata-only pending queue to full
  cards (catalog DS-014..DS-018): OR-Bench, WildJailbreak, WMDP,
  HaluEval, SimpleQA. Each card carries the verification trail
  (abstract-read papers, HF API page inspections, direct README/CSV
  reads) with honest gaps.
- SimpleQA's canonical CSV parsed directly: 4,326 questions with the
  full topic distribution (sum-checked); the 4,333 naive line count
  explained as a multi-line-quoted-field artifact.
- Registers +10 (SRC-PAPER-074..078, SRC-DATASET-016..020); claims +10
  (CLM-0116..0125). Catalog: 13 -> 18 datasets.

### Added (2026-10-23 — dataset license and composition verification round)

- Six license gaps closed by direct canonical LICENSE reads: ToxiGen (MIT
  text, Microsoft copyright, TOXIGEN header; GitHub NOASSERTION nuance
  recorded), BBQ (CC-BY-4.0), HarmBench (MIT), SafetyBench (MIT), AdvBench
  (MIT, llm-attacks canonical), JailbreakBench (MIT, repo-level
  confirmation). Register: SRC-REPO-002..007.
- HarmBench behavior-set composition verified by direct CSV read: 400 text
  behaviors (200 standard / 100 copyright / 100 contextual; test 320, val
  80; multimodal 110) with the semantic-category distribution — closes the
  "behavior-set size NOT verified" marker.
- Datasets catalog, six cards, index table, and pending-verification queue
  updated; all arithmetic cross-checked (41+159=200, 20+80=100, 19+81=100).

### Added (2026-10-23 — pending-paper verification round)

- Source register +4: SRC-PAPER-070 (PPO, abstract-read), SRC-PAPER-071
  (HH-RLHF, abstract-read), SRC-PAPER-072 (BeaverTails, abstract-read),
  SRC-PAPER-073 (TruthfulQA, abstract-read). Claims +4: CLM-0112..0115.
- Chapters 02/04/06 readings: every "assigned, verification pending"
  paper marker closed with the actual abstract-page fetch; WILDS's
  stale pending line corrected to the already-verified SRC-PAPER-067.
- The InstructGPT register limitation note about PPO-pending closed.

### Added (2026-10-22 — AI Researcher From Scratch track)

- `research/ai-researcher-from-scratch/`: the owner-directed 7-module
  track distilling the video "Become AI Researcher From Scratch - Full
  Course" (Vuk Rosic, 2025, CC-BY, page-inspected — SRC-VIDEO-001) and
  its MIT-licensed companion repository zero-to-ai-researcher
  (SRC-REPO-001, full-text-read) into notes plus stdlib-only code.
- `src/ai_safety_course/from_scratch/`: six code modules (tensors,
  activations, neuron, network, attention, transformer, moe) with 174
  tests — every backward pass finite-difference-checked; a TinyGPT
  trains on next-token prediction and regenerates its training string
  (deterministic, pinned in CI).
- `research/ai-researcher-from-scratch/07-research-methodology.md`:
  three preregistered protocol templates (ablation, hyperparameter
  search, architecture-configuration search) mapping the companion's
  research methodology onto the course's own evaluation discipline.
- Registers: SRC-VIDEO-001, SRC-REPO-001; claims CLM-0071..0073 (the
  paper's findings priced at abstract strength). GLOSSARY +10 terms;
  THIRD_PARTY_NOTICES +2 entries.


### Added (2026-10-21 — fresh start)

The repository was reset to its initial commit and rebuilt from the project
brief dated 2026-10-20 (research baseline 2026-10-20; build execution began
2026-10-21). Everything below is part of that rebuild.

- Research provenance layer: `research/research-method.md` (search scope,
  verification standards, honest limitations), `research/reference-article-map.md`
  (owner's article mapped to modules with a truthful access record — full
  text fetched 2026-10-21, conclusion not retrieved, article treated as
  inspiration not validation), `research/source-register.yaml` (5 entries
  verified by live fetch), `research/claims-register.yaml` (5 claims with
  counterevidence).
- Planning layer: `planning/BUILD_PLAN.md` (definition of done per artifact,
  phase gates), `planning/STATUS.md` (durable progress record; truthful
  counters), `planning/content-matrix.yaml` (24 chapters + 10 projects
  inventoried, all honestly `planned`), `planning/dependency-map.md`
  (curriculum prerequisites + tooling tiers), ADRs 0001 (architecture and
  licensing) and 0002 (uv, Python 3.12, optional dependency groups).
- Governance layer: MIT `LICENSE` for code, CC BY 4.0 `LICENSE-DOCS` for
  prose, `THIRD_PARTY_NOTICES.md` (inventory + import policy),
  `CITATION.cff` (no invented DOI or affiliation), `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md` (verifiable GitHub contact route; no invented email),
  `SECURITY.md` (verified: private vulnerability reporting disabled at
  2026-10-21; documented alternative route; repository-vulnerability vs
  model-behavior reports distinguished), `RESPONSIBLE_RESEARCH.md`.
- `AGENTS.md`: binding operating contract for agent sessions (auth via
  environment secret, one coherent commit at a time, honesty rules, untrusted
  data handling, resume protocol).
- Eight content templates (`templates/`): chapter, paper-note,
  experiment-report, threat-model, dataset-card, safety-case,
  research-proposal, incident-review — each with embedded quality rules
  (mandatory failure-mode sections, denominators, no hand-typed tables,
  strict incident taxonomy).
- Learner entry layer: `START_HERE.md`, `ROADMAP.md` (three schedules with
  honest arithmetic), `SYLLABUS.md` (24-unit catalog),
  `prerequisites/diagnostic.md` (five tasks with worked answers and skip
  guidance), `prerequisites/targeted-refreshers.md` (R1–R6),
  `roadmaps/` (three specialization pages + study schedules with
  adaptation rules).
- Engineering baseline: `pyproject.toml` + committed `uv.lock` (uv workflow,
  Python 3.12 floor, exact dev-tool pins verified against PyPI 2026-10-21),
  `.python-version`, in-repository pre-commit validator
  `scripts/validate_repo.py` with 7 regression tests, real CI workflow
  (actions pinned to verified commit SHAs), bug-report and content-error
  issue templates, pull-request template with the honesty checklist.

### Removed (2026-10-21)

- All prior agent-generated content and history after the owner's initial
  commit, per owner instruction (force-reset of `main` to the initial commit;
  issue tracker and Actions artifacts cleaned correspondingly).

### Notes

- No curriculum chapters or projects are complete yet; see
  `planning/STATUS.md` for the live, truthful state.
