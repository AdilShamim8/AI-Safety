# AI Safety

An open-source research curriculum and working project repository for
experienced ML engineers, security engineers, and aspiring technical AI safety
researchers. Free to read, free to run at meaningful small scale: no paid API
or subscription is required for the core path.

**Status (honest, updated 2026-10-28):** the build is complete at its target
scope and deepened — 24 of 24 chapters, 10 of 10 projects implemented
(deterministic, offline, stdlib-first), 47 verified dataset cards, 261
registered sources, 206 registered claims, 74 paper notes + 12 comparisons
+ 14 incident reviews, and a 640-test suite green in CI. Every project marks
its honest not-executed tiers where compute was out of scope. Live counters
and per-unit evidence: [`planning/STATUS.md`](planning/STATUS.md). The whole
build is also navigable as a generated dashboard: **[index.html](index.html)**
(open it in a browser — self-contained, no network needed).

## The 60-second tour

1. **Open [index.html](index.html)** — the whole build as one page:
   what exists, how it was verified (the evidence ladder), the 24
   chapters, the 10 projects, the dataset/source/claims explorers,
   the honesty ledger of what was *not* run, the incident timeline,
   the per-route progress bars, the careers, and the beginner path.
2. **Read [START_HERE.md](START_HERE.md)** and take the
   [diagnostic](prerequisites/diagnostic.md) — five tasks with worked
   answers place your starting point.
3. **Pick a route** — [alignment research](roadmaps/alignment-research.md),
   [AI security engineering](roadmaps/ai-security-engineering.md),
   [evaluations and assurance](roadmaps/evaluations-and-assurance.md),
   or [audit-only](roadmaps/audit-only.md) — then make the first 90
   days concrete: [roadmaps/first-90-days.md](roadmaps/first-90-days.md).
4. **Run it**: `uv sync && uv run pytest` — 640 deterministic tests,
   offline, no GPUs, no API keys.
5. **Wonder about anything**: [FAQ.md](FAQ.md),
   [AWESOME.md](AWESOME.md) (the annotated source map),
   [MAINTENANCE.md](MAINTENANCE.md) (how the truth is kept).
6. **Watch alongside**: the [lecture library](courses/README.md) —
   four courses (Harvard CS 2881, DeepMind's AGI Safety Course, the
   CAIS Ethics & Society course, Safeshield's governance series),
   57 verified videos with 61 companion notes, scheduled against the
   chapters in [courses/study-plans.md](courses/study-plans.md).

## What this repository is

1. An advanced, dependency-aware **learning roadmap** (three specializations
   over a common methodological spine).
2. A coherent **course**: 24 chapter units with original explanations,
   worked examples, critique, and assessments.
3. A **research notebook**: paper notes with real methodological analysis,
   comparison notes, and uncertainty tracking.
4. A collection of **reproducible, bounded experiments** and capstones
   (10 projects, each with a CPU smoke mode and an honest execution status).
5. An annotated **resource index** ([AWESOME.md](AWESOME.md)) — a map, not a
   link dump: every entry registered, dated, and access-leveled.
6. A generated **dashboard website** ([index.html](index.html)) — the whole
   build as one self-contained page: progress counters, the verification
   evidence ladder, chapter map, project cards, dataset/source/claims
   explorers, career tracks, and a beginner quickstart.
7. A maintained **open-source project** you can navigate, run, cite, and
   contribute to.

The organizing chain used throughout:

**risk or failure hypothesis → assumptions and threat model → observable
evidence → intervention → evaluation → limitations → revised claim.**

## Who it is for

You should be comfortable with Python, linear algebra, probability,
gradient-based optimization, PyTorch, transformers, and basic RL before the
advanced chapters — or be willing to close specific gaps first. The
[diagnostic](prerequisites/diagnostic.md) tells you which gaps matter.
Security specialists get an ML refresher path; ML specialists get a
threat-modeling refresher path. This is not a beginner Python or generic AI
course.

## The three routes

| Route | Primary purpose | Portfolio evidence |
|---|---|---|
| [Alignment research](roadmaps/alignment-research.md) | Investigate alignment interventions and their failure modes | Replication, ablation, critical research memo, falsifiable extension |
| [AI security engineering](roadmaps/ai-security-engineering.md) | Secure AI applications and agent workflows | Threat model, isolated attack/defense evaluation, regression suite, remediation report |
| [Evaluations and assurance](roadmaps/evaluations-and-assurance.md) | Design credible tests and contextual safety arguments | Dataset card, validated scorers, uncertainty analysis, monitoring study, evidence-backed safety case |

Where the routes lead: the three role families — AI safety researcher,
AI security specialist, AI (safety) engineer — are mapped to the live job
market (dated demand signal, entry mechanisms, and a five-rung progress
ladder) in [roadmaps/careers-index.md](roadmaps/careers-index.md).

All routes share the methodological spine (chapters 01–02) and end in a
capstone (P10 or the alternative research capstone). Schedules and hour
arithmetic: [ROADMAP.md](ROADMAP.md).

## Repository structure

| Path | Purpose | State |
|---|---|---|
| `index.html` | The generated dashboard website (regenerate: `uv run python scripts/build_dashboard.py`) | **exists** — generated from the repo's own data |
| `prerequisites/` | Diagnostic, targeted refreshers, skip guidance | **complete** — with worked answers |
| `roadmaps/` | Route pages, study schedules, careers index with the progress ladder | **complete** |
| `chapters/` | 24 chapter units (the course itself) | **complete** (24/24) — readings verified, solutions with rubrics |
| `projects/` | 10 runnable research learning units | **implemented** (10/10) — deterministic, pinned numbers, honest tiers |
| `research/` | Method, article map, source + claims registers, notes (74 paper + 12 comparison + 14 incident reviews) | **complete** — 261 sources / 206 claims, audit-clean |
| `research/ai-researcher-from-scratch/` | The from-scratch researcher track (stdlib-only modules) | **complete** (7/7) — 174 tests |
| `datasets/` | 47 verified real-world dataset cards + machine-readable catalog | **complete** — queue empty |
| `planning/` | Build plan, status, content matrix, ADRs | **exists** — the build's durable record |
| `templates/` | Chapter, paper-note, experiment-report, threat-model, dataset-card, safety-case, research-proposal, incident-review templates | **complete** (8) |
| `src/ai_safety_course/` | Project packages (evaluation, reward_spec, calibration, pref_audit, w2s_audit, patch_audit, agent_guard, control_protocol, shift_audit, assurance) + from_scratch | **implemented** — 640-test suite (401 package + 174 from-scratch + 65 repo-instrument) |
| `scripts/` | Validator, missing-values audit, link verifier, dashboard generator | **exists** — all run in CI |

## Getting started

1. Open **[index.html](index.html)** — the dashboard gives you the whole
   build in one page: what exists, how it was verified, where to start.
2. Read [START_HERE.md](START_HERE.md).
3. Take the [diagnostic](prerequisites/diagnostic.md) honestly — worked
   answers are included.
4. Pick a route and a schedule in [ROADMAP.md](ROADMAP.md); see where the
   routes lead in [roadmaps/careers-index.md](roadmaps/careers-index.md).
5. Clone and run: `uv sync` then `uv run pytest` — the deterministic suite
   must pass on your machine before anything else (no GPUs, no API keys).
6. Track what exists in [planning/STATUS.md](planning/STATUS.md); every
   published unit is complete when it appears.

## Provenance and honesty rules

Every substantive claim traces to the [source register](research/source-register.yaml)
with the access level actually achieved; claims live in the
[claims register](research/claims-register.yaml) with counterevidence. The
owner's reference article is mapped in
[research/reference-article-map.md](research/reference-article-map.md) and is
treated as inspiration, not validation. Project reports carry statuses
(`protocol-only`, `implemented`, `smoke-tested`, `experiment-executed`) that
match reality. These rules are binding on contributions (`CONTRIBUTING.md`).

## License, citation, conduct

- Original code: MIT ([LICENSE](LICENSE)). Original prose: CC BY 4.0
  ([LICENSE-DOCS](LICENSE-DOCS)). Third-party material: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
- Citation: [CITATION.cff](CITATION.cff).
- Contributing: [CONTRIBUTING.md](CONTRIBUTING.md). Conduct:
  [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md). Security:
  [SECURITY.md](SECURITY.md). Research ethics: [RESPONSIBLE_RESEARCH.md](RESPONSIBLE_RESEARCH.md).
