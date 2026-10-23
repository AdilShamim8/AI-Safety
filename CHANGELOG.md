# Changelog

All notable changes to this repository are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this
project does not yet issue semver releases, so entries accumulate under
Unreleased until a tagged release exists.

## [Unreleased]
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
