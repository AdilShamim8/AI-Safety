# START HERE

Five minutes from zero to a study plan. This page assumes nothing except that
you can read Markdown and run Python.

## Step 1 — Diagnose honestly (60–90 minutes)

Work the five tasks in [prerequisites/diagnostic.md](prerequisites/diagnostic.md)
**before** looking at the worked answers. They cover the five capabilities the
course assumes: a cross-entropy gradient and a transformer activation
inspection, experiment hygiene, an MDP with a proxy reward, a trust boundary,
and a causal-claims critique. Each task maps to skip guidance: pass it and you
skip a refresher; fail it and [prerequisites/targeted-refreshers.md](prerequisites/targeted-refreshers.md)
tells you exactly what to study and which chapters will hurt without it.

The point is calibration, not gatekeeping: nobody checks your answers, but
the advanced chapters will be unpleasant if the gaps stay open.

## Step 2 — Pick a route and a schedule (10 minutes)

- Routes: [alignment research](roadmaps/alignment-research.md),
  [AI security engineering](roadmaps/ai-security-engineering.md),
  [evaluations and assurance](roadmaps/evaluations-and-assurance.md) — or
  audit-only if you want the spine without a specialization.
- Schedules: 12-week focused (~10 h/week, a **selection**, not the whole
  course), ~24-week part-time (~6–8 h/week, one full specialization), or
  open-ended research (full curriculum + capstone). The arithmetic is in
  [ROADMAP.md](ROADMAP.md) — the focused route does not pretend 24 advanced
  chapters and 10 projects fit into 12 weeks.

Exit criteria are **artifacts**, not reading completion: each route ends with
portfolio evidence you can show (a replication, a threat model, a safety
case). Elapsed weeks are an estimate, not a completion criterion.

## Step 3 — Start the spine

Everyone starts with the methodological spine:

1. **Chapter 01 — Risk models and research epistemics** (how safety claims
   are structured, what evidence supports them).
2. **Chapter 02 — Evaluation science and experimental design** (how claims
   are tested; your preregistered evaluation plan is the first artifact).

Then your route's next chapter. Each chapter states its own prerequisites,
outcomes, scope exclusions, and completion criteria; each is tied to a paper
critique, a project, or a specific research deliverable.

## Compute expectations (set them now)

- The **core path is free and CPU-only**. Every project has a CPU smoke mode
  that runs on a laptop with the `core` dependency tier.
- **Local-model experiments** (projects P03, P04, P06, and model paths of
  P01/P08) use small open models on the optional `ml` dependency tier; a
  normal laptop CPU runs them at reduced scale, a GPU makes them pleasant.
  Model downloads are never required for the prose path.
- Nothing in the course requires a paid API. Where a commercial model would
  be interesting, the course instead designs the evaluation so a small local
  model demonstrates the same methodology.

## Current build state (read this once)

This is an honest work-in-progress build: units appear when they are complete,
and [planning/STATUS.md](planning/STATUS.md) tracks exactly what exists. If a
chapter you need is not there yet, the roadmap still tells you what it will
cover and which readings it will require; the source register already records
the verified sources behind the plan.

## Asking questions and reporting problems

- Content errors or citation problems: open an issue (see
  [CONTRIBUTING.md](CONTRIBUTING.md) for what to include).
- Security issues: [SECURITY.md](SECURITY.md) — not public issues.
- Conduct: [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
