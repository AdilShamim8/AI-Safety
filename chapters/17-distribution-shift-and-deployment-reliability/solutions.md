# Chapter 17 — Solutions and assessor rubrics

Worked solutions for the two exercises in
[README.md](README.md). Every rate carries its explicit denominator;
every interval is a Wilson 95% at z = 1.95996 (recomputed with the
course's metric module).

---

## Exercise 17.1 — the triage assistant's taxonomy audit

### (a) The shift-taxonomy analysis

| Shift class | Instance in this deployment | Detection signal | Evaluation instrument |
|---|---|---|---|
| Covariate | twelve sites incl. two rural clinics with different patient mixes, devices, and note styles than the three urban training sites | input-distribution indicators (feature drift, note-style statistics) | held-out-site evaluation: per-site rates with intervals (the WILDS pattern [SRC-PAPER-067]) |
| Label | flu season moves the severity base rate | outcome-rate surveillance (case-mix monitoring) | per-season re-computation of precision/recall at the operating threshold; label-shift correction |
| Concept | clinician presentations adapt to the assistant's known behavior | outcome-only: referral outcomes vs. downstream ground truth | outcome-monitoring cohort study — input-side signals are blind here |
| Group | site type (urban vs rural) — pre-declarable now | worst-group tracking with alert threshold | worst-site rate as first-class metric; group-DRO retraining available [SRC-PAPER-068] |
| Temporal | all of the above over months | drift indicators wired to re-evaluation triggers | rolling per-month windows; validity-window dating on every published number |

### (b) The two-sentence response to "96% average accuracy"

> "Average accuracy is a deployment claim only when the deployment
> is homogeneous — and overparameterized models are documented to
> fit the aggregate while consistently failing atypical groups
> [SRC-PAPER-068]. Report per-site rates with intervals; if the
> worst site's interval does not overlap the average's, the 96% is
> describing a patient population we are not serving."

### (c) What drift does to the referral policy

The threshold was tuned on deployment-day calibration. Under shift,
accuracy and calibration degrade together [SRC-PAPER-069] — so the
threshold's *operating point* silently moves even if the number
stays: overconfident errors cross the referral gate as if
calibrated. The surveillance: per-window reliability tables and ECE
(P03's machinery), recomputed on a rolling window, with the
threshold re-tuned only on per-window validation data (Ch. 06's
validation-only discipline plus the window discipline — a map fit on
last quarter anti-calibrates this quarter), and every published
policy number stamped with its validity window.

### (d) The class input-side monitoring cannot catch

**Concept shift.** When P(y|x) itself moves — clinician
presentations adapting to the assistant — the input distribution can
be statistically identical while the input-outcome relation has
changed. Input-side indicators (however good) measure P(x); the
failure lives in the conditional. Only labeled outcomes catch it,
which is why the audit's instrument column for concept shift reads
"outcome-monitoring cohort study" and nothing cheaper.

Assessor rubric: full credit requires all five rows with matched
signals and instruments (outcome-only for concept); the two-sentence
response carrying the overparameterized-group finding; the
threshold-operating-point argument with [SRC-PAPER-069]; and the
concept-shift answer with the P(x) vs P(y|x) distinction explicit.
Deduct for any input-side method proposed for concept shift.

---

## Exercise 17.2 — pricing the Halcyon numbers

### (a) Five intervals

| Quantity | Rate | Wilson 95% |
|---|---|---|
| ID accuracy | 481/500 = 96.2% | [94.1%, 97.6%] |
| OOD accuracy | 421/500 = 84.2% | [80.7%, 87.1%] |
| Worst-group (region E) | 61/100 = 61.0% | [51.2%, 70.0%] |
| Average-group | 92/100 = 92.0% | [85.0%, 95.9%] |
| False escalations, month 12 | 37/200 = 18.5% | [13.7%, 24.5%] |

The ID and OOD intervals do not overlap — the 12-point snapshot
drop is resolved, of the Recht kind [SRC-PAPER-066]. The worst-group
and average-group intervals do not overlap — the 31-point group gap
is real, not noise [SRC-PAPER-068's shape].

### (b) Which metric the tolerance should be written on

The vendor's tolerance is written on model accuracy (4-point drop,
arguably tolerable). The deployment broke at the *policy* layer:
false escalations grew from 2% to 18.5% — a 9-fold error-growth on
the quantity the business actually experiences, driven by
calibration degradation [SRC-PAPER-069], not by the accuracy drop.
Tolerances for gated systems belong on the gate's error rates at the
operating point, priced per window; accuracy tolerances are a
model-facing proxy that this example shows can stay green while the
system fails.

### (c) Pricing the group-DRO retraining

Worst-group after retraining: 78/100 → Wilson 95% [68.9%, 85.0%].
What improved: the worst-group rate (61.0% → 78.0%, intervals
[51.2%, 70.0%] vs [68.9%, 85.0%] — non-overlapping, the improvement
is resolved). What did not: nothing measured — average accuracy was
held, per the ledger. The coupling caveat [SRC-PAPER-068]: the gain
came from group DRO *plus* stronger-than-typical regularization
(doubled L2 / early stopping) — in the overparameterized regime,
DRO alone fails because training loss vanishes everywhere; the
worst-group problem is a *generalization* problem. The recipe that
ships must name both ingredients, or the next team reproduces half
of it and concludes the method is hype.

### (d) The validity-window statement

> "All rates in this report are measured on the month-12 audit
> window (2024-data-trained model, regions A-D + E post-retraining),
> carry Wilson 95% intervals at the stated denominators, and expire
> 90 days from issuance. Re-evaluation triggers: (i) input-drift
> indicator breaching its control band; (ii) any new region or
> client class exceeding 5% of traffic; (iii) calendar expiry.
> Unwatched by this report: sources not in the enumerated set,
> adversarial adaptation of content to the classifier (induced
> concept shift — outcome monitoring required), and label drift
> between policy updates. The escalation threshold's calibration is
> window-local and must be re-fit on window validation data before
> reuse."

Assessor rubric: full credit requires all five intervals correct;
the tolerance argument naming policy-error vs model-accuracy as the
metric distinction (with the 9-fold growth as the evidence); the
DRO pricing with both intervals, the coupling caveat in the recipe,
and the "reproduces half of it" consequence; and the validity-window
statement with dated numbers, named triggers, and an explicit
unwatched list. Deduct for presenting the retrained worst-group as
a bare point estimate, or for any undated published number.

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **DeepMind course**, [part-02-03-robust-training-monitoring](../../courses/google-deepmind-agi-safety/part-02-03-robust-training-monitoring.md) — watch before working the drift exercises.
