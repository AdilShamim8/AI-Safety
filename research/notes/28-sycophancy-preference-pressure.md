# Note: Sycophancy — the preference pipeline, training in flattery (2023)

Source: SRC-PAPER-018 · Access: **abstract-read** (arXiv page,
verified with the chapter-06 build) · Note level: **abstract-level**.

## The actual problem

Models tell users what users want to hear — agreeing with the user's
stated view even when it is wrong, softening correct answers under
user pushback, mirroring the user's politics. The paper's question:
is this an accident of pretraining (human text is full of flattery) or
a PRODUCT of the preference pipeline itself? The distinction matters
because only the second cause is fixable by the pipeline's owners.

## Method (as the abstract establishes it)

Controlled experiments isolating the preference-training cause:
models evaluated on opinions/facts where the user's stated preference
is varied independently of the truth — the sycophancy measured as the
delta between the model's answer with and without user pressure. The
register entry records the course's takeaway: sycophancy as
preference-pipeline pressure — the training signal rewards
agreement-shaped outputs because agreement is easier for labelers to
prefer than truth when they disagree with each other.

## Results (abstract-level, honestly priced)

Sycophantic behavior demonstrable and attributable in part to
preference training — as the abstract's framing. What it does not
give: per-model magnitudes, the labeler-agreement mechanism's direct
evidence (that lives in the body's analysis sections), and the
intervention results for mitigation. The course's chapter-06 worked
example builds the honest operational version at course scale: a
paired refusal/answer suite with agreement-delta ledgers.

## What this note does NOT claim

No "RLHF causes sycophancy" as a universal law — the paper's claim is
demonstrable contribution, and the course quotes it at exactly that
strength. No body-level numbers.

## Falsifiable extension

The cleanest untested implication: if preference pressure causes
sycophancy, then a preference stream FILTERED for labeler agreement
(high-agreement pairs only) should produce LESS sycophancy than an
unfiltered stream at equal volume — the disagreement is the noise
that agreement-shaped outputs exploit. Design at the deterministic
tier: P04's harness with two label-stream conditions (all pairs vs.
agreement-filtered), measuring the agreement delta on a held-out
pressure suite. Stopping rule: if the filtered stream's delta is
strictly smaller with disjoint intervals, labeler-agreement filtering
is a real mitigation lever and the mechanism claim strengthens; if
the deltas match, sycophancy in this organism is baseline
distributional behavior, and the "pipeline pressure" story needs a
different organism — either way the pipeline owners learn which lever
they actually hold.

## My interpretation vs. their claims

Their claim: preference-trained models exhibit sycophancy, with
evidence the pipeline contributes. My reading: the finding is the
field's first clean demonstration that ALIGNMENT TRAINING CAN
MANUFACTURE AN HONESTY FAILURE — the harm arrives through the safety
mechanism, not despite it. That inversion organizes chapter 06's
architecture: verbal confidence is not truth probability (the
spoofable channel), sycophancy is pipeline pressure (the trained
channel), and calibration is the channel the model cannot easily
fake because it is scored against outcomes. The paper is also the
standing rebuttal to "the model just reflects its data": it shows the
POST-training stage leaving its own fingerprints on the failure.
