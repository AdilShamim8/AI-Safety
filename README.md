# AI Safety

An open-source research curriculum and working project repository for
experienced ML engineers, security engineers, and aspiring technical AI safety
researchers. Free to read, free to run at meaningful small scale: no paid API
or subscription is required for the core path.

**Status (honest):** this repository is an active build. 0 of 24 chapters and
0 of 10 projects are complete. The provenance, planning, and governance layers
exist and are verified; curriculum units land chapter by chapter with their
readings, exercises, and projects. Live counters: [`planning/STATUS.md`](planning/STATUS.md).

## What this repository is

1. An advanced, dependency-aware **learning roadmap** (three specializations
   over a common methodological spine).
2. A coherent **course**: 24 chapter units with original explanations,
   worked examples, critique, and assessments.
3. A **research notebook**: paper notes with real methodological analysis,
   comparison notes, and uncertainty tracking.
4. A collection of **reproducible, bounded experiments** and capstones
   (10 projects, each with a CPU smoke mode and an honest execution status).
5. An annotated **resource index** (`AWESOME.md`, planned) — a map, not a
   link dump.
6. A maintained **open-source project** you can navigate, run, cite, and
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

All routes share the methodological spine (chapters 01–02) and end in a
capstone (P10 or the alternative research capstone). Schedules and hour
arithmetic: [ROADMAP.md](ROADMAP.md).

## Repository structure

| Path | Purpose | State |
|---|---|---|
| `prerequisites/` | Diagnostic, targeted refreshers, skip guidance | planned (Phase B) |
| `roadmaps/` | Route pages and study schedules | planned (Phase B) |
| `chapters/` | 24 chapter units (the course itself) | planned (Phases C–H) |
| `projects/` | 10 runnable research learning units | planned (Phases C–H) |
| `notes/` | Paper notes, comparisons, incident analyses | planned (with chapters) |
| `research/` | Method, article map, source + claims registers, frontier snapshot | **exists** — verified |
| `planning/` | Build plan, status, content matrix, ADRs | **exists** — verified |
| `assessment/` | Rubrics and worked solutions | planned |
| `templates/` | Chapter, paper-note, experiment-report, threat-model, dataset-card, safety-case, research-proposal, incident-review templates | planned |
| `src/ai_safety_course/` | Shared course utilities | planned (with P01) |

## Getting started

1. Read [START_HERE.md](START_HERE.md).
2. Take the [diagnostic](prerequisites/diagnostic.md) honestly — worked
   answers are included.
3. Pick a route and a schedule in [ROADMAP.md](ROADMAP.md).
4. Check [planning/STATUS.md](planning/STATUS.md) to see which units exist
   today; the build proceeds in phases, and every published unit is complete
   when it appears.

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
