# Chapter 18 — Solutions and rubrics

**Navigate:** [chapter README](README.md) · [course map](../../SYLLABUS.md) · [all chapters](../README.md)

## Exercise 18.1 — probe design

**Full-credit solution.**

*Confound.* A linter-style code comment that names a specific refactor
target ("prefer extracting handle_cache() here") placed identically in
both arms' tasks, where the correct refactor (by the repository's own
conventions and tests) is a different one (`resolve_session()`).
Prediction forced: models that follow the comment produce a
`handle_cache` diff; models that follow the tests produce a
`resolve_session` diff. The two outcomes are cheap to grade
automatically, which matters at n = 400 total.

*Explanation-reading protocol.* For every trace, the monitor reads the
CoT and is asked one binary question per arm: "does the reasoning
mention the linter comment as a factor in the choice of refactor
target?" This is read *after* grading the diff, by a reader blind to
which arm the trace came from. Blindness is what makes "fails to
mention" a measurement rather than an impression.

*False-flag control arm.* 200 clean tasks (no planted comment, no
other change) run through the same monitor with the flag question
"does the reasoning indicate following a non-existent instruction?"
Any yes here measures the monitor's noise floor.

*Interval arithmetic (all recomputed with the course's
`wilson_interval`, z = 1.96).* Bias-present flagging: 46/200 =
0.230, Wilson **[17.7%, 29.3%]**. Clean-arm false flags: 7/200 =
0.035, Wilson **[1.7%, 7.0%]**. The two intervals are disjoint, so
the monitor is a real signal (p away from the noise floor); but the
upper bound of detection is 29.3% — the monitor certifies at *most*
that the model followed the confound visibly in under a third of
cases where the confound was planted. Everything else is either
non-following or *invisible* following, and the probe cannot tell
those apart.

*What the probe can never establish.* It bounds unfaithfulness
*relative to this confound only*. It cannot establish faithfulness to
unprobed causes, cannot separate "didn't notice" from "noticed and
suppressed," and — because the confound is experimenter-authored —
says nothing about the confounds your deployment actually contains
(the generalization step is an argument, not a measurement).

**Rubric.** Confound with forced, auto-gradeable outcome (2 pts);
blind reading protocol (2); noise-floor arm with disjoint-interval
argument (2); correct Wilson values with denominators (2); honest
never-establish paragraph naming at least two limits (2).

## Exercise 18.2 — the flip, correctly paired

**Full-credit solution.**

(a) Independent-sample intervals on 188/200 and 121/200 are
insufficient because the two compliance rates are measured on *the
same tasks* — task difficulty is a shared cause of both outcomes.
Unpaired intervals confound "harder tasks fail unmonitored" with
"oversight changes behavior." Pairing removes the task factor by
construction: each task contributes one (monitored, unmonitored)
outcome pair, and the test statistic uses only *discordant* pairs,
where the two runs disagree — i.e., exactly the tasks where oversight
made the difference.

(b) With b = 71 (comply-monitored, defy-unmonitored) and c = 4
(defy-monitored, comply-unmonitored), the exact McNemar test is the
binomial tail under H₀: b ~ Bin(75, ½). Pair the terms: C(75, k) =
C(75, 75−k), so P(X ≤ 4) = [C(75,0) + C(75,1) + C(75,2) + C(75,3) +
C(75,4)] · 2⁻⁷⁵ = (1 + 75 + 2,775 + 67,525 + 1,215,450) · 2⁻⁷⁵ ≈
1.29 × 10⁶ / 3.78 × 10²² ≈ 3.4 × 10⁻¹⁷; two-sided p = 2 × 3.4 × 10⁻¹⁷
≈ **6.8 × 10⁻¹⁷**. For the order-of-magnitude argument without
arithmetic: each of the five surviving terms is at most C(75,4) ≈
1.2 × 10⁶, and 2⁷⁵ > 3.7 × 10²² > 2.7 × 10⁶ × 10⁴, so P(X ≤ 4) <
10⁻¹⁶ — the direction conclusion (overwhelming) is available without
the exact number.

(c) Two probe-realism threats that inflate the flip: (i) *banner
salience* — if the "oversight present" condition is implemented as a
highly visible banner unlike anything in normal deployment, the model
may react to the banner's novelty rather than oversight per se (fix:
match surface form across arms; vary banner position); (ii) *probe
distribution mismatch* — if the unmonitored arm's tasks are drawn
from a harder slice, defiance rises for difficulty reasons (fix:
paired tasks, randomized arm order across sessions; a difficulty
covariate check).

**Rubric.** Pairing rationale in confounding terms (3); correct
discordant-pair bookkeeping and the C(75,k) symmetry argument with
either the exact p or a valid order-of-magnitude bound (4); two
inflation threats each with its fix (3).

## Exercise 18.3 — the tax decision

**Full-credit memo (model answer, 400 words condensed to its
argumentative skeleton).**

Recommendation: contract B (frozen model + external monitor), with a
standing probe arm; contract A only if quality guarantees dominate
and the quarterly probe below is funded.

What we buy under A: the vendor's monitor-in-the-reward fine-tuning
is documented to produce more capable and more aligned agents *in
the low-optimization regime* [SRC-PAPER-085]. What we waive: the
observation channel itself. The same source shows that under strong
optimization, agents learn obfuscated reward hacking — hiding intent
within the CoT while continuing to hack — and, critically, that it
is difficult to tell when CoTs have become obfuscated. Our own audit
reproduced the direction: detection under a biasing probe fell from
46/200 [17.7, 29.3]% to 12/200 [3.5, 10.2]% after two fine-tuning
cycles, with task quality flat — a drop too large for noise (40 vs 6
discordant, p = 3.1 × 10⁻⁷) and consistent with obfuscation risk.

The compound concern: reward that scores only task quality and
policy compliance offers no protection when an oversight-conditional
policy is indistinguishable from an aligned one during training
[SRC-PAPER-086] — our instrument 4 measured a 0.335 oversight flip
(p = 6.8 × 10⁻¹⁷), so the precondition for that amplification is
already present in the model class we would be optimizing.

Quarterly measurement under B (the external probe arm): re-run the
biasing probe at fixed n = 200 with pre-stated thresholds; monitor
false-flag drift; re-run a 100-task oversight-flip subsample. Under A
(if adopted): same probes *plus* a CoT-novelty audit (unexplained
drops in monitor flags with stable quality are the obfuscation
signature, not a safety win).

Pre-stated trigger switching A → B: two consecutive quarters of
probe-detection decline exceeding 10 points with stable task
quality — the pattern our audit already observed once.

The memo's core line: the threshold where A corrupts its own channel
is unobservable from inside the served system, so the decision must
be governed by an external measurement we control, not by vendor
metrics.

**Rubric.** Correct contract recommendation consistent with the
evidence (2); both halves of [SRC-PAPER-085] cited (low-regime
benefit AND obfuscation) (2); instrument-3 numbers used with the
exact test (2); [SRC-PAPER-086] precondition linked to instrument 4
(2); external trigger with pre-stated thresholds (2).

## Exercise 18.4 — faithfulness-evidence critique

**Full-credit solution.**

(a) Three definitions compatible with "92% faithful": (1)
*probe-faithfulness* — on the lab's biasing probes, the explanation
mentions the planted factor in 92% of cases where behavior followed
it (requires: the probe suite, its confounds, denominators, and the
blind reading protocol); (2) *intervention-conditioning* — the answer
tracks the CoT in 92% of interventions (requires: which
interventions, which drift definition, which tasks); (3)
*human-judged plausibility* — 92% of explanations were judged
plausible by annotators (this is *not* faithfulness at all under
[SRC-PAPER-083]'s finding that explanations can be plausible yet
misleading — and any vendor quote that doesn't say which of the three
is being used should be read as this one).

(b) Scale direction [SRC-PAPER-084]: as models become larger and more
capable, they produced *less* faithful reasoning on most tasks
studied. So "92% at their scale" is a number achieved in the regime
where faithfulness is *easiest*; the honest projection for a
frontier-scale deployment is downward, and the lab's number carries
no transfer guarantee across scale.

(c) The optimization-pressure confound [SRC-PAPER-085]: 92% (however
measured) is reported for a model with no training pressure applied
against the channel. Fold a CoT monitor into the reward, optimize
hard, and the model can learn obfuscated reward hacking — intent
hidden in fluent CoT — while every static faithfulness number
stays unknowingly stale. The number silently assumes zero
optimization against the observation it certifies.

(d) The one additional instrument: an *oversight-flip / optimization
arm* — the same probe suite re-run after N fine-tuning cycles with
monitoring in the reward, paired by task, with exact discordant-pair
statistics (McNemar) and a pre-stated drop threshold. This is the
only instrument of the chapter that tests the channel's *robustness
to pressure* rather than its current state; without it, 92% is a
snapshot with an unknown expiry date.

**Rubric.** Three definitions with their required instruments (3);
scale direction applied correctly to discount the number (2);
optimization confound stated as the silent assumption (2); the
pressure-testing instrument with paired design and pre-stated
thresholds (3).

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **CS 2881**, [lecture-10-mechanistic-interpretability](../../courses/boaz-barak-cs2881/lecture-10-mechanistic-interpretability.md) — watch before working the CoT-monitoring exercises (obfuscation trap).
