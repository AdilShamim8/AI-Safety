# ROADMAP — the learner's map

The dependency-aware path through the course. Three specializations share a
common methodological spine; three schedules fit different lives; exit
criteria are artifacts you can show, not weeks elapsed or pages read.

Companion pages: route details in [roadmaps/](roadmaps/) (including the
[audit-only](roadmaps/audit-only.md) reviewer's route) · the three role
families mapped to the job market in
[roadmaps/careers-index.md](roadmaps/careers-index.md) · the 24-unit course
catalog in [SYLLABUS.md](SYLLABUS.md) · what exists today in
[planning/STATUS.md](planning/STATUS.md).

## The shape of the course

```text
 COMMON SPINE (everyone)                weeks 1–2 of any plan
 ├─ Ch.01  Risk models & research epistemics
 └─ Ch.02  Evaluation science & experimental design  ── P01 harness
                    │
    ┌───────────────┼────────────────────┐
 ALIGNMENT       AI SECURITY          EVALUATIONS &
 RESEARCH        ENGINEERING          ASSURANCE
 Ch.03→04→05     Ch.12→13→14→15       Ch.05→08→17
 Ch.07, 09–11    Ch.16, 19            Ch.22→23
 P04,P05,P06     P07 (+P08 shared)    P03,P08,P09
    └───────────────┼────────────────────┘
        Ch.20 misuse & release · Ch.21 sociotechnical risk
        Ch.24 research practice ── P10 CAPSTONE (or research capstone)
```

Hard prerequisites are listed per chapter in [SYLLABUS.md](SYLLABUS.md) and
enforced by the route pages. The two most common mistakes this diagram
prevents: starting interpretability (Ch.09) before evaluation science
(Ch.02), and starting LLM application security (Ch.13) before adversarial ML
basics (Ch.12).

## Prerequisites (compact)

| Skill | Assumed at | Check via | Refresh via |
|---|---|---|---|
| Python + scientific stack | spine | diagnostic task A | refresher R1 |
| Probability, linear algebra | spine | diagnostic task A | R1 |
| Gradient optimization, PyTorch | Ch.03 onward | task A | R2 |
| Transformers (mechanics) | Ch.04, Ch.09 | task A | R2 |
| Experiment hygiene | Ch.02 | task B | R3 |
| Basic RL / MDPs | Ch.03, Ch.04 | task C | R4 |
| Threat modeling basics | Ch.12–15 | task D | R5 |
| Causal-claims literacy | Ch.17, Ch.21 | task E | R6 |

Full tasks with worked answers: [prerequisites/diagnostic.md](prerequisites/diagnostic.md).
Targeted refreshers: [prerequisites/targeted-refreshers.md](prerequisites/targeted-refreshers.md).

## The three schedules

### A. Focused 12 weeks (~10 h/week, ~120 h total) — a deliberate selection

Completes the spine, **4–5 chapters of one specialization, 2 projects, and a
mini-capstone artifact** — 7–8 of 24 chapters. It does not pretend to cover
the course. Example for the security route:

| Weeks | Units (≈ hours) |
|---|---|
| 1–2 | Ch.01 (8) + Ch.02 (12) |
| 3–4 | P01 evaluation harness, smoke tier (20) |
| 5–6 | Ch.12 adversarial ML (10) + Ch.13 LLM app security (10) |
| 7–9 | Ch.14 agent/MCP security (10) + P07 injection defense (20) |
| 10–11 | Ch.15 red teaming (10) + benign/attack report (10) |
| 12 | mini-capstone: threat model + regression suite (10) |

Other routes substitute their chapters per the route page (alignment: Ch.03,
04, 05, 07 + P04; evaluations: Ch.05, 06, 08, 17 + P03). ~120 h total.

### B. Part-time ~24 weeks (~7 h/week, ~170 h total) — one full specialization

Spine (Ch.01–02, P01) → 8–9 specialization chapters with 3 projects →
comparison notes → a full capstone-equivalent artifact set. You finish with
all portfolio evidence for one route; the other routes' chapters remain
available later.

### C. Open-ended research route — full curriculum + capstone

All 24 chapters, all 10 projects at their full tiers, 20+ paper notes, and
the P10 capstone (or the alternative research capstone: nearest-baseline
replication plus one controlled extension). No fixed weekly load; exit is the
artifact set. Realistic total effort: 350–500 focused hours; plan accordingly
or explicitly switch to schedule A/B.

## Exit criteria (artifacts, per route)

| Route | You are done when you can show |
|---|---|
| Alignment research | a replication with ablation, a critical research memo, and a falsifiable extension proposal (P04–P06 + capstone variant) |
| AI security engineering | a threat model, an isolated attack/defense evaluation with a regression suite, and a remediation report (P07 + Ch.14/15 artifacts) |
| Evaluations and assurance | a dataset card, validated scorers with uncertainty analysis, a monitoring study, and an evidence-backed safety case (P03/P09 + Ch.22 artifacts) |

Each chapter's own completion criteria (listed in the chapter) are the
intermediate gates; these are the route-level exits.

## Checkpoints (narrow the problem before the capstone)

1. **After the spine:** your preregistered evaluation plan from Ch.02 is
   reviewed against its rubric — if the plan cannot name its denominator,
   stop and fix it before specialization.
2. **Mid-route:** one project report passes self-review against the
   experiment-report template (hypotheses, stopping rules, error analysis).
3. **Pre-capstone:** a one-page research proposal with the nearest baseline
   named and a falsifiable question — the capstone builds only after this
   narrows.

## What you will NOT get

No certification, no expertise guarantee, no career promise. The course
builds demonstrable skills and evidence; what that becomes is up to you and
your reviewers.
