# Note: Language Models (Mostly) Know What They Know (2022)

Source: SRC-PAPER-016 · Access: abstract-read · Read: 2026-10-21 ·
Note level: **abstract-level**.

## The actual problem

The authors' framing: do language models have a usable signal about
the correctness of their own outputs — and can that signal be
*elicited* by simply asking? The operational version: the P(True)
self-evaluation channel (ask the model to rate its own answer's
truth) and the P(IK) knowledge-state channel (ask whether the model
*knows* an answer to the question at all), as groundwork for training
more honest models.

## Method

(What the abstract carries:) self-evaluation — the model grades its
own proposed answers through prompted channels — framed explicitly as
groundwork for honesty training rather than as a finished calibration
instrument.

The design logic: instead of extracting confidence from the token
distribution (the logit channel, which measures the model's next-token
distribution, not its belief about truth), *generate* the confidence
as text and read it out. This makes confidence a trained behavior —
with everything that implies (trainable, and trainable-on).

## Central evidence

The abstract-level claim the chapter carries at exactly its strength:
self-evaluation channels carry real signal — models "mostly" know
what they know, the title's hedge being the paper's own honesty
device (the register's limitations entry carries this verbatim). The
P(True) and P(IK) channels are the named instruments; the quantitative
calibration figures and prompt formats live in the unread full text
and are not cited.

What the evidence does NOT carry: no claim that self-reported
confidence is calibrated (signal is not calibration — chapter 06's
whole measurement apparatus exists because "the model says 0.8" is a
score, not a probability); nothing about the trained-channel
vulnerability (a model trained to *look* confident on its own outputs
satisfies the channel without the state — the spoofing condition
chapter 06 §3.4 marks); nothing about free-text answers (the channels
are evaluated in their own format).

## Assumptions

Tested in-paper: the channels carry signal on the authors' task suite
(their own evaluation — the register's self-evaluation caveat).

Inherited: that elicited self-reports track an internal state (rather
than correlating with surface features of the question — the
correlate-vs-state question the probing literature prices); that the
signal survives distribution shift (the channels are prompted
behaviors, as drift-sensitive as any other); that "knows what it
knows" generalizes from the suite to deployment queries.

## Limitations

Authors' (abstract-level): the "mostly" hedge — the paper's own scope
statement. Mine: all results are the authors' self-evaluation on
their own suite (no external benchmark existed for self-knowledge —
still largely true); the P(True) channel's readout inherits the
sycophancy pressure of the preference pipeline (a model tuned to
please raters has a conflict of interest in grading itself); and the
paper predates the free-text-scoring problem — deployment honesty is
about answers the model writes, not labels it assigns to its own
multiple-choice.

## Nearest alternatives

- **Logit-based confidence (chapter 06 §3.4's other channels)**:
  cheaper, always available, but measures the next-token distribution
  — the paper's channels measure (or at least elicit) something
  closer to belief; the two are compared, not identified.
- **Lin et al. verbalized confidence (chapter 06's third channel)**:
  the free-text form of the same idea — numbers the model *says*,
  with the same trained-channel caveat arriving one step later.
- **Calibration-metric literature (P03's canon)**: the measurement
  side — the chapter-06 discipline that turns any of these channels
  into a priced instrument (Brier/ECE/AURC on a held-out split).

## Replication feasibility

High at course scale — this is P03's tier-3 design: a local model,
authored question sets with known outcomes, P(True)/P(IK)-style
prompted readouts, and the calibration machinery the repo already
ships. What breaks first: the free-text side (grading open answers
needs a grader — whose own calibration becomes part of the
measurement, the recursion chapter 06 flags); the suite-to-deployment
shift (the authored set answers questions the deployment has not
asked yet).

## Falsifiable extension

Hypothesis: P(True) signal is preference-pressure-sensitive — a model
fine-tuned for rater-pleasing (the standard RLHF step) shows degraded
self-evaluation calibration relative to its base model, with the
degradation concentrated on items where honesty and rater-pleasing
diverge (the sycophancy stratum). Design: base vs post-preference
model; authored items stratified into aligned/divergent (where the
truth is unpleasant vs pleasant to claim); measure P(True) channel
calibration (Brier, ECE) per stratum with the P03 machinery.
Baseline: the base model's calibration. Stopping rule: two strata,
one model pair. What counts against: if post-preference calibration
is unchanged across strata, self-evaluation survives the preference
pipeline and my pressure premise fails — a useful negative for the
sycophancy-uncertainty link the chapter asserts.

## My interpretation vs. their claims

Their claims: (1) models mostly know what they know; (2) P(True)/
P(IK)-style channels elicit that signal; (3) this is groundwork for
training more honest models.

My interpretation: (1) survives as one of the field's most-quoted and
least-troublesome results — the hedge in the title is the reason it
aged well; (2) the channels are best read as *instruments under
training pressure* rather than properties — their value is that they
make honesty a measurable, trainable target, and their vulnerability
is that the same trainability serves spoofing; (3) the groundwork
framing was honest and prescient: the follow-up literature (verbalized
confidence, calibrated fine-tuning) is exactly the program the paper
proposed — with chapter 06's lesson attached: every elicited channel
is a behavior, and behaviors are optimization targets for whoever
controls the training signal.
