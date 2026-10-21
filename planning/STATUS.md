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
| Phase B (part 4): engineering baseline — pyproject + uv.lock (19 pkgs), .python-version, in-repo validator + 7 tests, CI (actions pinned to verified SHAs), issue/PR templates | `66b8574` (pushed; **CI green**: all 8 steps success on run 39557258289) | checks verified via API |
| Phase C (part 1): **chapter 01 complete** — README (ten-element structure: risk decomposition with six primitives, evidence kinds, uncertainty taxonomy, invoice-assistant worked example, approach comparison, failure conditions, verified readings), exercises, full worked solutions + assessor rubrics, GLOSSARY seed (18 entries), chapters index; registers +3 sources (SRC-PAPER-001/002, SRC-REPORT-001) and +3 claims (CLM-0006/0007/0008) | this commit | validator + tests green locally |

## Current phase

**Phase C in progress.** Chapter 01 is complete (ten-element structure met;
readings verified at honest access levels: two arXiv abstracts read, IASR
2026 landing page inspected, owner article full-text-read).

## Curriculum completion counters (truthful)

- Chapters complete: 1 / 24 (Ch. 01 complete; 02–24 planned; see content matrix)
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

Phase C continues with chapter 02 (one coherent commit per unit):

1. Verify chapter 02's readings (construct validity / contamination /
   adaptive overfitting / reproducibility primaries - search, then register
   at achieved access levels; WILDS arXiv:2012.07421 is the brief's seed
   for distribution-shift evaluation material used again in Ch. 17).
2. Write `chapters/02-evaluation-science-and-experimental-design/`
   (README + exercises + solutions + rubric) - deep on: construct validity,
   dataset provenance, grouped splits, contamination, adaptive overfitting,
   statistical power, cluster-aware intervals (Wilson), effect sizes,
   repeated trials, preregistration. Artifact: preregistered evaluation
   plan (a learner's Exercise 1.2 output is its draft).
3. Then P01 (evaluation harness - first code project; the
   src/ai_safety_course package lands there) -> chapter 03 -> P02, same
   discipline.
