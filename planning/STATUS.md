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
| Phase A (part 2): planning package — BUILD_PLAN, STATUS, content-matrix skeleton, dependency map, ADR-0001/0002 | `38011a4` (pushed) | `planning/*` |
| Phase B (part 1): governance and licensing baseline — MIT, CC BY 4.0, notices, citation, contributing, conduct, security (verified: private-vuln-reporting disabled), responsible research, changelog | `6f0ab31` (pushed) | 9 root governance files |
| Phase B (part 2): learner entry layer — README/START_HERE/ROADMAP/SYLLABUS, diagnostic with worked answers, refreshers, 3 route pages, study schedules | `c123179` (pushed) | validator passed (13 dead links caught and fixed by completing the unit) |
| Phase B (part 3): eight content templates (chapter, paper-note, experiment-report, threat-model, dataset-card, safety-case, research-proposal, incident-review) | `08c24bc` (pushed) | `templates/*` |
| Phase B (part 4): engineering baseline — pyproject + uv.lock (19 pkgs), .python-version, in-repo validator + 7 tests, CI (actions pinned to verified SHAs), issue/PR templates | this commit | `uv run pytest` 7/7; ruff + black clean; validator OK |

## Current phase

**Phase B complete.** Exit gate met: a learner can understand scope
(README/START_HERE), select a route and schedule (ROADMAP + route pages),
and see truthful completion status (STATUS + content matrix); all published
links resolve (validator-enforced); a real CI workflow runs the same checks
that gate commits locally.

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

Phase C begins with chapter 01 (one coherent commit per unit):

1. Verify chapter 01's core readings at the stated access level (add
   source-register entries first): Concrete Problems in AI Safety
   (arXiv:1606.06565), Risks from Learned Optimization (arXiv:1906.01820),
   plus the International AI Safety Report 2026 landing page for edition
   metadata.
2. Write `chapters/01-risk-models-and-research-epistemics/`: README.md
   (ten-element structure), exercises.md, solutions.md; add initial
   GLOSSARY.md entries for the chapter's terms; update content matrix
   (01 → drafting → complete) in the same commit.
3. Then chapter 02 → P01 → chapter 03 → P02, same discipline.
