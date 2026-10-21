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
| **Chapter 03 complete** — ten-element structure: three-way failure taxonomy (proxy/capability/learned-goal) with formal grounding (Skalse et al. hackability conditions; Pan et al. capability thresholds; Shah et al. goal misgeneralization; mesa-optimization re-anchored to SRC-PAPER-002), Goodhart gap G and proxy validity region V(R-hat) defined with notation, truthfulness-judge worked example swept over BoN pressure with real AdvBench/TruthfulQA card numbers and preregistered gates G1/G2 (Wilson intervals recomputed in solutions), approach comparison (5 rows), where-the-methods-fail section, 2 demanding exercises + full solutions with rubrics (509-line solutions file with programmatic arithmetic); GLOSSARY +10 terms; readings = 4 verified sources (1 re-verified) | this commit | validator + tests green | |

## Current phase

Phase C in progress: chapter 03 complete (3/24); chapters 04–05 written and verified, landing next; P01 code green in its worktree.

## Curriculum completion counters (truthful)

- Chapters complete: 3 / 24
- Dataset cards complete: 13 verified cards in the catalog
- Projects complete: 0 / 10
- Paper notes complete: 0 / 20 required minimum
- Comparison notes: 0 / 5 planned
- Incident analyses: 0 (verified set, grows with the build)
- Real local-model experiments executed: 0 / 3 required (recorded honestly;
  compute-tier projects mark their own execution status truthfully)

## Blockers

None. (Environment note: token `GH_TOKEN` was exposed in chat before this
build and must be rotated by the owner when convenient; pushes currently
depend on it — flagged here so it is not forgotten.)

## Next exact action

Next exact action: chapter 04 (preference learning and post-training) — its README and solutions are written and its sources verified (InstructGPT, DPO, Constitutional AI, Ziegler); merge its fragment and commit, then chapter 05, then the P01 evaluation-harness project pair (spec + implementation) from worktrees/p01.
