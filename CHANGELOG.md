# Changelog

All notable changes to this repository are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this
project does not yet issue semver releases, so entries accumulate under
Unreleased until a tagged release exists.

## [Unreleased]
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
