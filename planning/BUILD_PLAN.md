# BUILD_PLAN — maintainer build plan

This is the **maintainer's** task-level plan. It is deliberately separate from
`ROADMAP.md`, which is the **learner's** roadmap. Nothing here assigns learner
work; it defines what must be built, in what order, and what "done" means.

Last updated: 2026-10-21. Live status: `planning/STATUS.md`. Coverage detail:
`planning/content-matrix.yaml`.

## Mission recap

Build the repository as all six things at once: (1) an advanced,
dependency-aware learning roadmap; (2) a coherent course with substantive
original explanations and assessments; (3) a research notebook with critical
paper analyses and uncertainty tracking; (4) reproducible, bounded experiments
and capstones; (5) an annotated `AWESOME.md` index; (6) a maintained open-source
project. The organizing chain for all technical content:

**risk or failure hypothesis → assumptions and threat model → observable
evidence → intervention → evaluation → limitations → revised claim.**

## Definition of done

**A chapter is done when** its directory contains a substantive `README.md`
plus separate exercise and reading/assessment files; it covers all ten
required elements from the project brief (research question tied to a failure
pathway; prerequisites, outcomes, scope exclusions; original explanation with
notation; a worked example/derivation/case; comparison of approaches with
assumptions and failure modes; a counterexample or failure condition; 2–4
essential primary readings with reasons and sections; two demanding exercises
—one analysis, one empirical/design/critical; hints and worked solutions or a
rubric in a separate file; a concrete artifact, completion criteria, references,
and prev/next/cross links). Required readings must be verified in the source
register at the stated access level before the chapter is marked complete.

**A project is done when** it has a README (question, chapter links, exact
install/run commands, expected output structure, compute tiers), a dated
protocol (hypotheses, baselines, metrics, stopping rules, disconfirming
criteria), real code + configuration + small fixtures + tests + a data card +
an experiment report, appropriate split discipline, a baseline and one
meaningful ablation or stress test, benign controls, error analysis, per-case
outputs plus a script that computes the published summary (no hand-typed
tables), provenance fields (dataset/model versions, license, seed, environment,
timestamps, code revision, known nondeterminism), a fresh-environment CPU
smoke check, and an honest report status (`protocol-only`, `implemented`,
`smoke-tested`, `experiment-executed`; `independently-reproduced` only with
external evidence).

**A paper note is done when** it covers the actual problem, method, central
evidence, assumptions, limitations, nearest alternatives, replication
feasibility, and a falsifiable extension, distinguishing the note author's
interpretation from the authors' claims.

## Phase plan

Phases are implemented through multiple coherent commits, never one giant
commit. Each phase's exit gate must hold before the next begins (blockers are
recorded in `planning/STATUS.md`, not silently skipped).

| Phase | Work | Exit gate |
|---|---|---|
| A | Provenance: repo inspection, article access verification, research method, source + claims registers, ADRs, build plan, content matrix skeleton | Target, provenance, licensing, and build plan explicit; no unsupported article claims |
| B | README, START_HERE, ROADMAP, SYLLABUS, diagnostic, refreshers, study schedules, templates, governance files (LICENSE, LICENSE-DOCS, CONTRIBUTING, CoC, SECURITY, RESPONSIBLE_RESEARCH, CHANGELOG, CITATION), initial CI, glossary seed | A learner can understand scope, pick a route, and see truthful completion status; all published links resolve |
| C | Chapters 01–03 and projects P01–P02 | Methodology and first experiments substantive, runnable, assessed |
| D | Chapters 04–08 and P03–P05/P08 | Alignment, oversight, and control coverage with baselines, critiques, honest execution status |
| E | Chapters 09–11 and P06 | Interpretability explanations and intervention evidence with causal controls and held-out tests |
| F | Chapters 12–16 and P07 | Security coverage with enforceable boundaries and measured benign/attack tradeoffs |
| G | Chapters 17–23 and P09 | Deployment, multimodal, systemic, assurance coverage with artifacts and dated guidance |
| H | Chapter 24, P10, ≥20 paper notes, comparison notes, incident analyses, glossary completion, annotated AWESOME index, RESEARCH_QUESTIONS cards, frontier snapshot | All required units meet their acceptance criteria |
| I | Fresh-environment checks, three labeled self-review passes, cross-file review, final documentation, remote verification | Acceptance checklist satisfied or blockers explicitly reported |

## Commit and push conventions

- One coherent, defensible purpose per commit (a complete chapter, a runnable
  experiment improvement, a verified reading list). Never a single giant final
  commit; never cosmetic-commit noise.
- Before every commit: run the repository validator (YAML schema, local link,
  size checks) and the checks appropriate to the change; repair failures first.
- `planning/STATUS.md` and `planning/content-matrix.yaml` update **in the same
  commit** as the unit they describe.
- Push to `main` after verification; confirm the remote head hash before
  starting a dependent unit. Experiment results may follow the implementation
  commit that produced them; never record a future commit hash.
- Conventional-commit-style prefixes (`research:`, `docs:`, `feat:`, `fix:`,
  `ci:`, `test:`, `planning:`) with a body explaining the defensible purpose.

## Build sequence notes (from the project brief, binding)

- Chapters get their paper notes and glossary entries **with** the chapters
  that need them, not in one final batch.
- A documentation site is optional and only after the repository is complete;
  no badges unless they represent a real workflow or fact.
- Model downloads and GPU runs stay outside normal PR CI; CPU smoke runs are
  the default tier.
- External link checks are rate-limited and scheduled separately from PR CI;
  dead links are distinguished from 429s/auth walls/crawler blocks, and
  exceptions carry reasons and review dates.
- If interrupted: checkpoint the last complete unit, leave a precise
  continuation instruction in `planning/STATUS.md`, never mark unfinished
  files complete.
