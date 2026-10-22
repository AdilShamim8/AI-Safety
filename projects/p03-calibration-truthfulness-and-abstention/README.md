# P03 — Calibration, truthfulness, and abstention

**Project status: `implemented`** (code + 98 tests green; deterministic
CPU-only runs over a synthetic fixture with three scripted instruments;
the **ml compute tier** — licensed dataset + local model + real
free-text scoring — is scoped below and honestly marked as not yet
executed) · 2026-10-22 · chapter link: [Ch. 06 — honesty, uncertainty,
and selective
prediction](../../chapters/06-honesty-uncertainty-and-selective-prediction/README.md)

## The question this project answers

Can this repository measure whether a model's confidence is *worth
anything* — with the full Chapter 06 discipline as code: reliability
tables whose bins carry counts and Wilson intervals, ECE reported next
to its binning, proper scoring rules, rank-based risk–coverage curves
against the oracle ceiling, threshold policies with both sides of the
abstention ledger, and calibration maps that are fit on validation
only and frozen before evaluation?

And the sharper Chapter 06 question: when does gating on confidence
make things *worse*? The inverted-signal fact — an instrument whose
confidence anti-correlates with correctness yields AURC above the
full-coverage risk, i.e., abstaining by that signal is worse than
answering everything — is the project's pinned headline.

## What landed in this repository

```text
projects/p03-calibration-truthfulness-and-abstention/
├── README.md                       (this file: protocol + usage)
├── cases/calibration-cases-v1.yaml 60 synthetic items, 3 scripted
│                                   instruments, checksum-pinned
├── configs/calibration-three-instruments-v1.yaml  the preregistered run
├── example-report.md               genuine output of that run (committed)
└── runs/                           local outputs (gitignored per policy)
src/ai_safety_course/calibration/
├── metrics.py       reliability tables, ECE (+bin counts), Brier,
│                    clipped log loss, mean gap (a marginal, not a measure)
├── selection.py     risk–coverage curves, AURC, oracle ceiling + gap,
│                    threshold policies with both ledger sides
├── calibrators.py   identity / Platt (deterministic Newton) / histogram,
│                    fit-once state machine (validation-only fits)
├── cases.py         fail-closed case-set loader with SHA-256 pinning
├── runner.py        config-driven, deterministic runner + CLI
└── report.py        dated markdown reports with provenance blocks
tests/test_p03_*.py                98 deterministic tests (offline)
```

Repository data policy: `runs/` stays local and gitignored; the curated
`example-report.md` is committed and is genuine generated output of the
committed config (2026-10-22); the fixture is synthetic (authored with
seed 20261022, no dataset content redistributed).

## Install and run (CPU-only; no model download)

```bash
uv sync --frozen
uv run pytest
PYTHONPATH=src uv run python -m ai_safety_course.calibration.runner \
    projects/p03-calibration-truthfulness-and-abstention/configs/calibration-three-instruments-v1.yaml
```

## The fixture's three instruments (why these)

| Instrument | Construct modeled | What it demonstrates |
|---|---|---|
| `well-calibrated-v1` | confidence tracks correctness with realistic class overlap | the honest gate: AURC 0.1308 vs full-coverage risk 0.4000 |
| `overconfident-v1` | same ranking, scores shifted up and compressed | miscalibration visible (ECE 0.1915 vs 0.1127) with ranking preserved (identical AURC — a monotone map preserves the gate) |
| `inverted-v1` | the poisoned signal: confidence anti-correlated with correctness | the inverted-signal signature: AURC 0.7178 **above** the full-coverage risk 0.4000 — gating is worse than answering everything |

The overlap band (confident wrong answers, hesitant correct ones) is
what makes calibration *measurable* — the first fixture draft had
perfectly separable classes, which made every calibration map look
perfect (Brier 0.0000); that draft was rejected as dishonest-by-
construction and regenerated with realistic overlap.

## Protocol (preregistered 2026-10-22)

**Design.** One case set; a round-robin split (even case indices
validation, odd evaluation — no seed, no shuffle, stated in every
report). For every (instrument, calibrator) pair: fit the calibrator on
the validation split, freeze it, transform the evaluation split, then
measure — reliability table (K=10) with bin counts and Wilson 95%
intervals, ECE with its binning stated, Brier, clipped log loss
(epsilon 1e-15), mean gap, AURC, oracle AURC, AURC gap, full-coverage
risk, and threshold policies at tau in {0.5, 0.7, 0.9} with both the
selective-risk and false-abstention sides.

**Hypotheses.**

- **H1 (calibration is measurable).** The three instruments separate on
  the evaluation split: ECE and Brier rank overconfident above
  well-calibrated under identity. (Pinned: ECE 0.1915 vs 0.1127; Brier
  0.1637 vs 0.1189.)
- **H2 (the inverted-signal signature).** Gating on the inverted
  instrument is worse than answering everything: AURC above the
  full-coverage risk. (Pinned: 0.7178 vs 0.4000.)
- **H3 (calibration is not free).** Fitted maps earn their parameters
  only by beating identity *on the evaluation split*; on this fixture
  they do (the miscalibration is systematic), and the limitations
  section prices exactly what that proves — same-distribution fit, not
  deployment robustness.

**Stopping rules.** The instrument list, calibrator list, K, and
thresholds are fixed in the committed config before running; no
extension after seeing results. The fixture was regenerated once
before any results were committed (the separable first draft), and that
rejection is recorded here rather than hidden.

**Disconfirming criteria.** H1 fails if the instruments do not separate
under identity on the evaluation split; H2 fails if the inverted
instrument's AURC does not exceed its full-coverage risk; H3 fails if
a fitted map beats identity only on the split it was fit on.

**Non-claims.** The instruments are scripted scores over authored
items; nothing here measures any deployed model. ECE is reported at
K=10 only (the K-dependence is pinned in tests, not swept in the
report). Threshold operating points carry conditional rates with
moving denominators — the intervals ride along.

## The compute-tier boundary (what is NOT yet done, stated plainly)

The project's design has three tiers; only the first is implemented:

1. **Implemented (this commit)**: the full measurement discipline over
   scripted instruments — every metric, interval, curve, and gate the
   discipline requires, offline and deterministic.
2. **ml tier (planned, not executed)**: replace the scripted scores
   with a local model's confidence over a licensed dataset — the
   dataset candidates are
   [TruthfulQA](../../datasets/cards/01-truthfulqa.md) (817-item
   validation split, per its card) and
   [XSTest](../../datasets/cards/06-xstest.md) (250 clearly-answerable
   + 200 unsafe contrasts for the false-abstention side); the runner,
   metrics, and gates carry over unchanged — only the instrument
   adapter changes. Requires torch/transformers (the `ml` dependency
   group, ADR-0002).
3. **Free-text scoring tier (planned)**: verbalized confidence over
   free-text answers, where the Chapter 06 lesson bites — the score is
   then a *generated* number whose own calibration is part of the
   measurement problem (the trained-channel vulnerability).

The counters in [planning/STATUS.md](../../planning/STATUS.md) record
tier 1 truthfully; no real-model experiment is claimed.

## Honest limitations

- The fixture is authored: the numbers are properties of the authored
  distribution, quoted to exercise the discipline, not as findings
  about any model.
- The calibration maps are fit on a round-robin validation split of
  the same authored distribution — the "recovery" of the inverted
  instrument (Brier 0.5609 → 0.0968 under Platt) is correctable
  *systematic* miscalibration, and deployment robustness under drift is
  explicitly not claimed (Chapter 17's territory).
- ECE's binning sensitivity is demonstrated in tests (K=1 vs K=10 on
  the same data) rather than swept in the report; the report quotes one
  K with its counts.
- The oracle ceiling is the best achievable curve *for this
  (scores, outcomes) set* — it prices the score's ranking information,
  not the task's difficulty.
- Small-n bins are wide by construction (a 6-item bin at accuracy 0
  carries a Wilson upper near 0.39) — the report shows the counts so
  the reader can see exactly that.
