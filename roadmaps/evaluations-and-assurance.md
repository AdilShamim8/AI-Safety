# Route: evaluations and assurance

**Primary purpose:** design credible tests and contextual safety arguments —
evaluation methodology, calibration and abstention, distribution shift,
control protocols, and evidence-backed safety cases for real deployment
decisions.

**You:** an ML engineer, evaluation engineer, or reliability/quality engineer
who passed diagnostic task B (experiment hygiene) or is willing to run
refresher R3 first — this route is where R3's habits become professional
practice.

## Sequence
[**Track your progress:**](progress/evaluations-and-assurance.md) the engineer route's expanded milestone checklist (M0–M5, price tags on every control).



| Step | Unit | ≈ hours | Evidence produced |
|---|---|---|---|
| 1 | Ch.01 risk models & epistemics | 8 | threat hypothesis |
| 2 | Ch.02 evaluation science | 12 | preregistered evaluation plan |
| 3 | P01 evaluation harness (full) | 25 | harness + scorer validation + report |
| 4 | Ch.06 honesty, uncertainty, selective prediction | 10 | calibration analysis |
| 5 | P03 calibration, truthfulness & abstention | 20 | validation-only calibration, Brier/log loss, risk–coverage curves |
| 6 | Ch.05 scalable oversight | 10 | oversight-failure analysis |
| 7 | Ch.08 AI control & monitoring | 10 | control protocol + failure conditions |
| 8 | P08 control & monitoring protocol | 20 | usefulness–failure tradeoff under audit budget |
| 9 | Ch.17 distribution shift & deployment reliability | 10 | shift-taxonomy analysis |
| 10 | P09 distribution shift & subgroup reliability | 20 | ID vs. shifted vs. subgroup outcomes + one mitigation |
| 11 | Ch.15 red teaming (shared with security route) | 10 | evaluation design with benign controls |
| 12 | Ch.20 misuse & release evaluation | 8 | release-evaluation design (non-operational) |
| 13 | Ch.22 safety engineering & assurance | 12 | safety-case draft |
| 14 | Ch.23 governance & standards | 8 | standards mapping with versions |
| 15 | paper notes (≥8 on this route) | 16 | notes/papers/* |
| 16 | Ch.24 research practice | 8 | evaluation-research proposal |
| 17 | capstone P10: agent evaluation & assurance dossier | 40 | claim–evidence–assumption–rebuttal safety case + documented deployment-decision impact |

Core sequence ≈ 247 h; the 24-week part-time schedule covers steps 1–14;
schedule A covers steps 1–10. P01 is the spine artifact of this route: the
harness you validate in step 3 is the instrument every later evaluation runs
on.

## Exit criteria (portfolio evidence)

1. **A dataset card** (P03/P09): provenance, license, splits, known biases,
   and — the part most cards omit — what the dataset cannot support.
2. **Validated scorers with uncertainty analysis:** scorer agreement against
   hand-verified examples, cluster-aware intervals, denominators reported.
3. **A monitoring study:** drift/shift behavior with selective prediction,
   from P09.
4. **An evidence-backed safety case:** P10's dossier — explicit claims,
   evidence, assumptions, rebuttals, and residual risk, tied to one
   deployment decision.

## Pitfalls this route is designed to prevent

- Single-number "safety scores" merging unrelated dimensions (Ch.02/22 keep
  capability, behavior, and deployment constraints separate).
- Zero-failure theater: "we tested N prompts and saw nothing" presented as
  assurance (Ch.15/22 state what such evidence can and cannot support).
- LLM-judge-as-ground-truth (the judge-validation rules in Ch.02 and P01's
  scorer validation exist precisely for this).
- Calibration fit on test data (P03's split discipline is enforced, not
  advised).
