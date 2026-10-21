# Changelog

All notable changes to this repository are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this
project does not yet issue semver releases, so entries accumulate under
Unreleased until a tagged release exists.

## [Unreleased]

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

### Removed (2026-10-21)

- All prior agent-generated content and history after the owner's initial
  commit, per owner instruction (force-reset of `main` to the initial commit;
  issue tracker and Actions artifacts cleaned correspondingly).

### Notes

- No curriculum chapters or projects are complete yet; see
  `planning/STATUS.md` for the live, truthful state.
