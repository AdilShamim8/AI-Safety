# STATUS — durable progress record

Single source of truth for where the build stands. Updated in the same commit
as the work it describes. On session start, read this file, then
`git log --oneline -10`, then continue from "Next exact action".

## Repository facts

- Target: `https://github.com/AdilShamim8/AI-Safety` (owner: AdilShamim8)
- Working branch: `main` (push verified after each unit)
- Research baseline: 2026-10-20 (build execution began 2026-10-21)
- Licensing: MIT for original code, CC BY 4.0 for original prose (ADR-0001)
- Tooling: uv + pyproject.toml + uv.lock, Python 3.12 floor (ADR-0002)

## Completed units (with evidence)

| Unit | Commit | Evidence |
|---|---|---|
| Fresh start: repository reset to owner's initial commit `7fe58ec` (all prior agent work removed per owner instruction, 2026-10-21) | `7fe58ec` (remote verified) | remote tree = `README.md` only; issues/labels/Actions artifacts cleaned |
| Phase A (part 1): research provenance — research method, article map (full-text fetch 2026-10-21), source register (5 entries), claims register (5 claims), AGENTS.md, .gitignore | `4ebb954` (pushed, remote head verified) | `research/*`; validator passed |
| Phase A (part 2): planning package — BUILD_PLAN, STATUS, content-matrix skeleton, dependency map, ADR-0001/0002 | this commit | `planning/*` |

## Current phase

**Phase A → B transition.** Phase A exit gate is met with this commit: target,
provenance, licensing, and build plan are explicit; the reference-article map
makes no unsupported claims (access record and non-validation note included).

## Curriculum completion counters (truthful)

- Chapters complete: 0 / 24 (all `planned`; see content matrix)
- Projects complete: 0 / 10 (all `planned`)
- Paper notes complete: 0 / 20 required minimum
- Comparison notes: 0 / 5 planned
- Incident analyses: 0 / small verified set planned
- Real local-model experiments executed: 0 / 3 required (blocked on
  environment check at first model-dependent project; will be recorded
  honestly either way)

## Blockers

None. (Environment note: token `GH_TOKEN` was exposed in chat before this
build and must be rotated by the owner when convenient; pushes currently
depend on it — flagged here so it is not forgotten.)

## Next exact action

1. Phase B commit 1 — governance and licensing baseline: `LICENSE` (MIT),
   `LICENSE-DOCS` (CC BY 4.0), `THIRD_PARTY_NOTICES.md`, `CITATION.cff`,
   `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`,
   `RESPONSIBLE_RESEARCH.md`, `CHANGELOG.md` (real content, no stubs).
2. Phase B commit 2 — entry layer: `README.md` (accurate current status),
   `START_HERE.md`, `ROADMAP.md` (common spine + 3 specializations + 3
   schedules with honest hours), `SYLLABUS.md`, `prerequisites/diagnostic.md`
   (5 diagnostic tasks + worked answers), `prerequisites/targeted-refreshers.md`,
   `roadmaps/*.md`, `templates/*`.
3. Phase B commit 3 — engineering baseline: `pyproject.toml`, `uv.lock`,
   minimal real CI (markdown links + YAML schema + python import smoke),
   `scripts/` check tooling ported into the repository.
4. Then Phase C: chapter 01 → chapter 02 → chapter 03 → P01 → P02, one
   coherent commit each, readings verified in the source register as they
   are assigned.
