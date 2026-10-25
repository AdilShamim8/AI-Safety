# Note: The Mirage — metric choice manufacturing "emergence" (2023)

Source: SRC-PAPER-095 · Access: **abstract-read** (arXiv page,
verified with the chapter-20 build) · Note level: **abstract-level**.

## The actual problem

The 2023 field narrative: LLMs exhibit "emergent abilities" —
capabilities that appear discontinuously past a scale threshold,
unpredicted by smaller models. If true, that discontinuity is a
safety problem (you cannot extrapolate risk from the model you can
afford to test). The paper's question: is the discontinuity in the
MODELS, or in the METRICS we chose to score them?

## Method (as the abstract establishes it)

The re-analysis: emergent-looking jumps in nonlinear/discontinuous
metrics (exact-match, string equality, multiple-choice all-or-nothing)
dissolve into smooth curves when the same model outputs are scored
with continuous metrics (token-level probability, partial credit).
The claim structure is methodological, not merely empirical: a
discontinuous metric can MANUFACTURE a discontinuity that neither the
underlying model nor the loss landscape contains.

## Results (abstract-level, honestly priced)

Four task families re-analyzed (per the abstract's framing), with the
emergent jumps attributed to metric choice. What the abstract does not
give: the per-task re-plots, the meta-metric arguments, and the
boundary cases where the authors concede discontinuity might survive.
The course's chapter-20 use is the release-evaluation consequence,
below.

## What this note does NOT claim

Not "emergence is disproved" — the paper's claim is attribution for
the audited task families under metric substitution. The capability
safety question stays open exactly as open as the paper leaves it.

## Falsifiable extension

The course-scale version: P03's calibration machinery over a synthetic
capability-growth curve (smooth logistic in model "scale"), scored two
ways — exact-match vs token-probability. Prediction from the paper:
the exact-match curve shows a threshold artifact at the same
underlying smoothness. Stopping rule: if BOTH metrics show a jump, the
organism genuinely has a threshold (constructor knows the truth — that
is the point of an organism) and the paper's attribution logic
validates as a detector; if only exact-match jumps, the mirage
mechanism reproduces deterministically, and every "threshold" claim
in a release memo now carries a required footnote naming its metric.
Either way the instrument (metric-pair comparison) is the durable
output.

## My interpretation vs. their claims

Their claim: emergent abilities in the audited families are metric
artifacts. My reading: the finding generalizes far past emergence —
it is the construct-validity chapter (Ch.02) arriving at scale. EVERY
threshold-flavored safety claim ("capability appears at X parameters",
"the guardrail holds until Y") is a metric-choice statement wearing a
world-statement costume, and chapter 20's release-memo discipline
exists to make the costume visible: name the metric, show the smooth
alternative, let the reviewer decide which curve they believe. The
paper is also the sharpest available answer to "why does your course
obsess over measurement?" — because at frontier scale, measurement
choice IS the capability claim.
