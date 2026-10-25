# P01 — Evaluation harness and scorer validation

**Project status: `implemented`** (code + 71 tests green, deterministic
CPU-only demonstration runs executed over synthetic fixtures; **not** an
experiment over a real model — that tier is marked honestly below) ·
2026-10-21 · chapter link: [Ch. 02 — evaluation science and experimental
design](../../chapters/02-evaluation-science-and-experimental-design/README.md)


**Session-2 companion materials:** [model-written evals](../../research/notes/41-model-written-evaluations.md) (the circularity your case-set provenance avoids), [FActScore](../../research/notes/46-factscore.md)/[SelfCheckGPT](../../research/notes/47-selfcheckgpt.md) (the scorer-quality instruments), [CheckList](../../research/notes/59-checklist-behavioral-testing.md) (capability x test-type cells), [C07](../../research/notes/comparison-07-reference-vs-consistency-factuality.md).
## The question this project answers

Can this repository run an evaluation whose numbers it is willing to
publish — one where every rate carries its explicit denominator and a
Wilson 95% interval ([Ch. 02 §3.5](../../chapters/02-evaluation-science-and-experimental-design/README.md)),
every artifact is checksum-pinned, an interrupted run resumes *exactly*,
and the scorer itself is validated against hand-verified examples before
any of its labels are trusted?

The harness is the course's first working instrument: later projects
(`P03`, `P07`, `P09`) consume its case-set format, runner discipline, and
report structure. It is deliberately adapter-agnostic — the same runner
drives a deterministic scripted adapter (today) or a locally hosted model
(the `ml` compute tier, not required here).

## What landed in this repository

```text
projects/p01-evaluation-harness/
├── README.md                  (this file: protocol + usage)
├── cases/refusal-cases-v1.yaml   24 synthetic paired refusal cases,
│                                 checksum-pinned, versioned, fail-closed loader
├── example-report.md          genuine output of the demo run below (committed)
└── runs/                      local run outputs (gitignored by repository
                                 data policy; created by re-running the
                                 documented configs): echo-quickstart,
                                 baseline-echo, baseline-all-refuse,
                                 demo-scripted-guard
src/ai_safety_course/evaluation/
├── cases.py     Case/CaseSet: schema validation, SHA-256 checksum, version
├── adapters.py  ModelAdapter protocol; scripted / echo / callable adapters
├── metrics.py   Wilson intervals (z=1.96), paired ledger, MetricSummary
├── scorer.py    Scorer protocol; RuleBasedRefusalScorer (validated)
├── runner.py    config-driven, resumable, fail-closed runner + CLI
└── report.py    dated markdown reports with full provenance blocks
tests/test_p01_*.py            71 deterministic tests (offline, <1 s)
```

Repository data policy: raw run outputs (`runs/`, `state.json`,
`results.json`) stay local and gitignored; the **curated** report
(`example-report.md`) is committed and is genuine generated output of the
`demo-scripted-guard` run (2026-10-21). The three baseline/quickstart runs
referenced in the protocol were executed locally with the same discipline;
re-running the documented configs regenerates them byte-identically.

## Install and run (CPU-only; no model download)

```bash
uv sync --frozen                      # core deps only: pytest + PyYAML
uv run pytest                         # 78 tests (7 repo + 71 P01)
```

A run is one YAML config (schema `p01-run/v1`, fail-closed on anything else)
invoked from the repository root:

```yaml
schema: "p01-run/v1"
run_id: "demo-scripted-guard"
cases_path: "projects/p01-evaluation-harness/cases/refusal-cases-v1.yaml"
output_dir: "projects/p01-evaluation-harness/runs/demo-scripted-guard"
seed: 20261021
run_date: "2026-10-21"                # pin for byte-reproducible outputs
report_title: "Evaluation report: Scripted guard over 24 synthetic refusal cases"
adapter:
  kind: "scripted"                    # or "echo"
  responses:
    HC-SAFE-01: "Sure! Mix one part baking soda..."
    # ... one response per case id
```

```bash
PYTHONPATH=src uv run python -m ai_safety_course.evaluation.runner <run-config.yaml>
```

The command writes `state.json` (resumability), `results.json` (the full
deterministic record), and `report.md` (the publishable artifact), then
prints the paired ledger. Re-running the same config after an interruption
resumes from `state.json` and produces byte-identical results — this is
test-enforced, not aspirational.

## The fixture: `refusal-cases-v1`

24 **synthetic** cases in six categories, each pairing two clearly-safe
requests (expected behavior: `comply`) with two clearly-unsafe contrasts
(expected behavior: `refuse`), mirroring the paired-ledger discipline of
[Ch. 02](../../chapters/02-evaluation-science-and-experimental-design/README.md):
a refusal rate is only interpretable next to its false-refusal complement.
The design is modeled on the XSTest structure at the **metadata level
only** — no XSTest prompts, category names, or content are redistributed
(design reference: [datasets/cards/06-xstest.md](../../datasets/cards/06-xstest.md)).
The file's exact bytes are SHA-256 checksummed by the loader and recorded
in every run's provenance block, so any silent edit to a case invalidates
every downstream comparison.

## Scorer validation (the point of the project)

`RuleBasedRefusalScorer` labels a response refused/complied from response
text alone (keyword/regex rules). Before any run trusts it, it is
validated against the fixture's hand-verified expectations: on the
committed demo run the scorer agrees with the hand labels on **24/24
cases** — recorded in the example report's gap sentence, together with the
scorer's documented failure modes (keyword scoring can miss
redirection-only refusals and can flag hedged compliances). A scorer
without a published validation number is exactly the construct-laundering
failure mode [Ch. 02 §3.1](../../chapters/02-evaluation-science-and-experimental-design/README.md)
warns about; this project makes that number impossible to omit.

## Protocol (preregistered 2026-10-21)

- **Hypotheses.** H1: the harness produces the same paired ledger when a
  run is interrupted and resumed at any case boundary (resumability is
  exact, not approximate). H2: the Wilson intervals in every report match
  independent recomputation of the Ch. 02 formula to 10^-4. H3: the
  scripted-guard demo shows a paired ledger where neither side is at a
  trivial extreme (both a missed refusal and a false refusal appear) —
  demonstrating that the ledger surfaces both error kinds, not just the
  attack side.
- **Baselines.** Two anchored baselines ship as executed runs: echo
  (comply with everything — the false-refusal floor) and all-refuse (the
  attack-side ceiling at the cost of maximal false refusal). Any real
  guard must beat *both* simultaneously; reporting one side against the
  wrong baseline is the classic half-a-confusion-matrix sin.
- **Metrics.** Refusal rate on expected=refuse (attack side), compliance
  rate on expected=comply (benign side), false-refusal and missed-refusal
  complements — each with k, n, and Wilson 95% interval. Per-category
  rates are diagnostic only (n=2 per cell; small-n discipline per Ch. 02).
- **Stopping rules.** One pass over the 24-case fixture per adapter; no
  iteration against the fixture (it is a test set, not a tuning set — the
  fixture would be retired if it were ever used for tuning).
- **Disconfirming criteria.** H1 fails if any resumed run differs from the
  uninterrupted record in any byte; H2 fails if any recomputed interval
  differs at the 4th decimal; H3 fails if the demo ledger shows a
  degenerate all-refuse or all-comply adapter. All three are test-covered
  in `tests/test_p01_runner.py` and `tests/test_p01_metrics.py`.

## Compute tiers

- **Core (this commit):** stdlib + PyYAML, CPU-only, offline, <1 s for the
  full test suite; the scripted/echo adapters need no model. This is the
  tier CI runs.
- **`ml` tier (deliberately not in this commit):** a `CallableAdapter`
  wrapping a locally hosted model behind the same runner — lands with the
  first model-dependent project (`P03`), where an honest
  `experiment-executed` status will be recorded at that time.

## Honest limitations

- The demonstration runs are over **synthetic** cases with a **scripted**
  adapter: they exercise and evidence the *harness* (resumability,
  checksums, intervals, ledger, report provenance), not any model's
  safety behavior. No number in the example report is a claim about a
  real model.
- The scorer is rule-based and English-only; its validation number (24/24)
  is scoped to this fixture and would not transfer to other response
  styles — the report's gap sentence says so explicitly.
- `scorer` is a single configurable implementation (`rule-based-v1`);
  additional scorers land with the projects that need them.
