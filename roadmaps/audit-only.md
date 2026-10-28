# Route: audit-only — the spine without a specialization

**Navigate:** [← the learner's map](../ROADMAP.md) · [study schedules](study-schedules.md) · [progress tracker](progress/audit-only.md)

**Primary purpose:** learn to READ and JUDGE AI-safety evidence —
evaluation designs, red-team reports, interpretability claims, safety
cases — without producing research artifacts of your own. This is the
reviewer's route: for managers, policy analysts, journalists,
investors, and engineers who need to tell a strong claim from a
dressed-up one, at reading pace.

**You:** anyone who can pass diagnostic task R1-light (read a
probability statement without flinching). No PyTorch required; the
route never builds anything, it audits everything. Expect to run the
projects' committed example reports, not the code.

**Session-2 readings now in the route's spine:** the [judge's
audit](../planning/SESSION2_JUDGE_AUDIT.md) as a worked example of the
auditor's own method; [the accountability-era incidents](../research/notes/incidents/README.md)
(Galactica, EEOC-iTutorGroup, Amazon) with [the response-posture
comparison](../research/notes/comparison-10-incident-response-postures.md);
[the supply-strategy comparison](../research/notes/comparison-12-evaluation-supply-strategies.md)
for reading benchmark claims critically; and the
[verification re-check](../planning/STATUS.md) as the one-fetch drill
done at repo scale.

## The sequence (≈120 h)

[**Track your progress:**](progress/audit-only.md) the auditor route's milestone checklist (M0–M4, written challenges as the artifacts).

| Step | Unit | ≈ hours | What you can judge afterward |
|---|---|---|---|
| 1 | Ch.01 risk models & epistemics | 6 | whether a safety claim is even structured as a claim |
| 2 | [Verifying sources](../prerequisites/verifying-sources.md) | 2 | whether the citation trail behind a number is real |
| 3 | Ch.02 evaluation science | 10 | construct validity, splits, power — the three ways reports fool you |
| 4 | P01 example report (read-only) | 3 | a harness report's provenance and paired ledger |
| 5 | Ch.03 specification & reward hacking | 8 | Goodhart claims and proxy gaps |
| 6 | Ch.06 truthfulness & calibration | 8 | calibration tables, abstention ledgers |
| 7 | Ch.07 deception evidence | 8 | the evidence ladder (constructed < conditioned < deployment) |
| 8 | Ch.15 red teaming | 8 | denominators, over-refusal, the two-sided ledger |
| 9 | The [incident reviews](../research/notes/incidents/README.md) | 3 | what production records establish vs imply |
| 10 | Ch.12-13 (readings only) | 12 | adversarial-ML and injection claims at reading level |
| 11 | Ch.20 release evaluation + Ch.22 safety cases | 14 | a release memo and a safety case, line by line |
| 12 | P10 dossier (read-only) | 4 | a deployability verdict and its improvement actions |
| 13 | Ch.23 governance & standards | 8 | "NIST-aligned" as genre laundering or as real evidence |
| 14 | Ch.24 research practice | 6 | negative results and the benchmark lottery |

## Exit criteria (what you can do at the end)

1. **Read any safety report in this field and name its weakest link**
   — the missing denominator, the unevaluated defense, the
   post-hoc gate, the vendor-mapped certification.
2. **Audit a citation** — one fetch away from any claimed number's
   primary source, and able to say what access level you achieved.
3. **Write the review** — a one-page structured critique of a safety
   claim: what it establishes, what it assumes, what would falsify it,
   and what the source register says about its provenance.

## How this route relates to the other three

The specialized routes ([alignment research](alignment-research.md),
[AI security engineering](ai-security-engineering.md),
[evaluations and assurance](evaluations-and-assurance.md)) exist to
PRODUCE the artifacts this route exists to JUDGE. The market wants
both: every safety case needs a reader who can attack it (Ch.22's
defeater discipline), and every hiring loop for safety-adjacent roles
is, at its core, an audit of claims. See
[careers-index.md](careers-index.md) for where the reviewer's skill
lands professionally — governance and policy roles filter strongly on
exactly this reading competence.

### The lecture-library pairing

This route's chapters pair with the video layer as follows (full
mapping in [courses/study-plans.md](../courses/study-plans.md) and
each chapter's watching-companions block):
- The Safeshield series as a second spine: modules 1–2 with Ch. 01,
  module 8 with the risk chapters, modules 9–11 with Ch. 23, and
  modules 12–14 with Ch. 22 and the audit practice.
- The CAIS course (Lectures 1, 4, 7, 8) for the society-scale
  framing regulators actually use.
- The DeepMind Part 3 videos for the frontier-evaluation connection
  auditors will increasingly be asked to check.

## Pitfalls this route is designed to prevent

1. **Credential worship.** The route never asks whether the author is
   famous; it asks whether the number traces. By step 14 this is a
   reflex.
2. **Premature skepticism.** The audit route is not "doubt
   everything" — every critique must name what WOULD count as
   evidence, or it is vibes wearing a reviewer's badge.
3. **Reading without running anything.** Steps 4, 9, and 12 pin the
   reading to real committed artifacts — the example reports, the
   incident notes, the dossier — because auditing a rendering of an
   artifact you never opened is how review theater starts.
