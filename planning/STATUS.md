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
| Phase C (part 1): **chapter 01 complete** — README (ten-element structure: risk decomposition with six primitives, evidence kinds, uncertainty taxonomy, invoice-assistant worked example, approach comparison, failure conditions, verified readings), exercises, full worked solutions + assessor rubrics, GLOSSARY seed (18 entries), chapters index; registers +3 sources (SRC-PAPER-001/002, SRC-REPORT-001) and +3 claims (CLM-0006/0007/0008) | `0f9b0a0` (pushed; CI green) | validator + tests green locally |
| **Dataset catalog (owner-directed depth upgrade)**: `datasets/` — 13 verified real-world safety datasets (TruthfulQA, BOLD, RealToxicityPrompts, ToxiGen, BBQ, XSTest, BeaverTails, HH-RLHF, AdvBench, JailbreakBench, HarmBench, WildChat, SafetyBench) with deep cards; per-fact reference tables (every composition number traced to the URL it was collected from, with access level and date); machine-readable catalog.yaml; curriculum-integration map; usage/licensing policy (BeaverTails NC flag; no content redistribution); pending-verification queue; registers +18 sources (SRC-DATASET-001..015, SRC-PAPER-003/004/005, SRC-DATASET-009b) and +13 claims (CLM-0009..0021) | `ae06ad9` (pushed; CI green run 39574015674) | validator + tests green; remote head verified |
| **Chapter 02 complete** — ten-element structure: failure pathway (validity-leak chain), five-gate core (construct validity with three card-grounded worked examples; five provenance questions; dependence-aware splits; contamination & adaptive overfitting; Wilson/power/effect sizes with four verified-number worked intervals), guard-layer end-to-end worked example with threshold-straddling honest conclusions, approach comparison table, four failure modes of the method itself, readings split into verified vs assigned-pending, 5 exercises + full solutions with rubrics + arithmetic; GLOSSARY +12 terms; chapters index updated | this commit | validator + tests green locally |

## Current phase

**Phase C in progress.** Chapter 01 is complete; the **real-world dataset
catalog** is complete (13 datasets, verified 2026-10-21 at page-inspect /
abstract-read levels with per-fact references); **chapter 02 is complete**
(construct/provenance/splits/contamination/power/preregistration, all
worked examples grounded in verified catalog numbers).

## Curriculum completion counters (truthful)

- Chapters complete: 2 / 24 (Ch. 01, Ch. 02 complete; 03–24 planned; see content matrix)
- Dataset cards complete: 13 / 13 in the current catalog scope (queue of
  ~10 further datasets recorded at metadata-only level, deliberately
  unverified and uncited)
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

Phase C continues (one coherent commit per unit):

1. **P01 — evaluation harness** (first code project; `src/ai_safety_course`
   lands here): config-driven runner, local adapters, versioned cases,
   transparent metrics (Wilson intervals per Ch. 02), resumability, reports,
   scorer validation against hand-verified examples. Uses TruthfulQA/XSTest
   metadata (no content redistribution) per the dataset catalog's policy.
2. Then chapter 03 (specification, reward hacking, goal misgeneralization)
   -> P02, same discipline.
3. Verification-round 2 (when web access is available): the catalog's
   pending queue (OR-Bench, WildJailbreak, WMDP, HaluEval, SimpleQA,
   ToxiGen/BBQ/HarmBench/SafetyBench licenses, CrowS-Pairs, Winogender,
   MMLU, GSM8K) and chapter 02's assigned readings (WILDS 2012.07421,
   TruthfulQA 2109.07958 full-text).
4. Owner-directed priority note (2026-10-21): the course must read as a
   premium ($10k-course-grade) curriculum — every chapter must go deep,
   cite its sources, and tie into real datasets; chapters 01–02 now meet
   that standard and every later chapter must match it.
