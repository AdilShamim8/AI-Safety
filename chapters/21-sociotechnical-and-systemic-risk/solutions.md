# Chapter 21 — Solutions and rubrics

## Exercise 21.1 — the normative step, first

**Full-credit solution.**

*Population-at-risk and harm:* Applicants whose qualifications are
systematically mis-scored, with the harm being *screened out of
consideration* (denied the job) at a rate their qualifications do
not justify; the secondary harmed population is the employer, whose
candidate pool is distorted (a validity harm, not a moral one —
naming both keeps the analysis honest).

*Construct:* the decision rule (score threshold + human review
protocol) applied to the model's calibrated score; the harm
construct is *false negative decisions concentrated in a group* —
not "the model's bias," which is a mechanism hypothesis, not the
harm.

*Whose fairness definition:* the deployment is in a regulated
context where the four-fifths-style screen carries legal weight
(the *regulator's* definition), while the employer's stated value is
*equal opportunity conditional on qualification* (an error-rate
view) — these are not the same construct and the memo must say
which governs.

*Silently sacrificed conditions:* if the governing metric is
calibration (score means what it says per group), then with unequal
base rates the deployment *cannot* also hold error rates equal
across groups [SRC-PAPER-098] — it sacrifices the equalized FPR/FNR
condition; if instead error-rate balance governs, calibration per
group is sacrificed for at least one group. The memo must state:
"we choose [calibration], which means accepting [unequal FPR across
groups at 14/120 vs 31/110-style rates], chosen because [the
regulator's construct governs], visible to [stakeholders]."

**Rubric.** Three normative statements with the harmed population
concrete (3); the sacrifice pair correctly derived from the
impossibility result (3); the memo sentence in the stakeholder-
visible form (4).

## Exercise 21.2 — complementarity arithmetic

**Full-credit solution.**

(a) Complementarity gap = 104/120 − 102/120 = +1.7 points. The
honest uncertainty: the comparison is *paired* (same 120 decisions),
so the discordant pairs carry the information: 14 (combined right,
AI wrong) vs 12 (combined wrong, AI right) of 26 discordant — exact
two-sided p = 0.845. The gap is indistinguishable from zero: the
honest statement is "the human contribution is not statistically
detectable at this n," not "+1.7% improvement."

(b) Catch rate 5/18 = 27.8%, Wilson **[12.5%, 50.9%]**. It
establishes: under this interface, the human+AI system resolves
fewer than a third of the AI's errors — consistent with automation
bias (the mechanism [SRC-PAPER-096] predicts exactly this). It does
*not* establish: that the *specific* humans are negligent (the
interface design is the confound), nor the longitudinal deskilling
claim (needs cohorts), nor the counterfactual under a different
interface (that is what (c) measures).

(c) Forced-independence re-measurement: randomly sample k = 20% of
AI-recommended decisions per period to route to *independent* human
review (no AI recommendation shown, reviewer blind to arm); catch
rate measured on the AI-wrong items in the sampled set with
denominator ≥ 30 for an interpretable interval; pre-stated
threshold: oversight counts as restored only if the forced-
independence catch rate's *lower* bound exceeds 50% — rubber-
stamping restored if it collapses toward the advisory-interface
27.8%. Report both rates side by side, per period, with the
sampling rate fixed in advance (so the monitor cannot be quietly
turned down under pressure — the incentive station).

**Rubric.** Paired-test insight with the "not detectable" phrasing
(3); the interval plus the two does/does-not lists (3); the blind
sampling design with pre-stated threshold and fixed rate (4).

## Exercise 21.3 — impossibility, concretely

**Full-credit explanation (≤ 200 words).**

"Both fairness conditions can hold together only when the two
groups have equal base rates — the same true qualification
frequency. Concretely: if 60% of group A applicants are truly
qualified and 40% of group B applicants are, then any *calibrated*
score (an 0.7 means 70% qualified, in both groups) *must* produce
different error rates per group at any threshold — because the
score distributions sit on different true rates. To equalize the
error rates, you must shift one group's threshold off calibration —
so an 0.7 means 70% for A but something else for B. You have not
found a bug to fix; you have found a *choice* to make — the
mathematics guarantees the choice exists [SRC-PAPER-098]."

*Trade-off statement:* "Ceres screens under calibration with
per-group thresholds fixed jointly across groups; this choice
accepts unequal false-positive rates (A 11.7% [7.1, 18.6]% vs B
28.2% [20.6, 37.2]%), chosen because [stakeholder reason], with
equalized-error-rate operation available at the cost of group
miscalibration."

**Rubric.** Equal-base-rate special case used as the pivot (3);
concrete unequal-rate example showing the forced choice (3); the
memo sentence with both sacrificed quantities named (4).

## Exercise 21.4 — stakeholder and failure-pathway analysis

**Full-credit design (skeleton).**

*Stakeholder map.* Quadrants: high-power/high-interest (the lender's
risk office, the regulator); high-power/low-interest (the platform
vendor, the integration partner); low-power/high-interest
(applicants — both screened-in and screened-out populations, the
fifth-language cohort); low-power/low-interest (the general public
via precedent). The map's job is to show *who must see the
trade-off choice* (§ the fairness statement) — power over the
decision, interest in the outcome.

*Five stations located.* (1) Model: the score's measured per-group
reliability (Ch. 17's worst-group discipline re-applied). (2)
Decision rule: the threshold and its group-differential error
structure — where the disparate impact actually lives. (3)
Deployment context: the advisory interface whose catch rate is
27.8% — the human oversight is a *deployment* property. (4)
Incentive structure: the volume targets that push cycle time — the
friction list (forced-independence sampling at fixed 20%, quarterly
re-audit) is what these incentives erode; name who wants each
friction gone. (5) Coverage boundary: the four measured languages +
the 9% fifth-language cohort on the fallback path (3.2x cycle) —
exclusion as design.

*Measured rates.* Per-group pass rates and FPRs with intervals
(Ceres instrument 1); complementarity and catch rate (instrument
2); per-language quality arms (instrument 3).

*The fairness statement.* The impossibility-forced choice, stated
with the sacrificed quantity, the reason, and the stakeholders who
saw it [SRC-PAPER-097, 098].

*The honesty check:* no finding is attributed to "the model" alone —
each is located at a station, because that is what the artifact is
for.

**Rubric.** Stakeholder quadrants with the trade-off audience
identified (2); all five stations populated with located findings
(4); measured rates with intervals present (2); the fairness
statement complete (2).

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **CAIS course**, [lecture-05-complex-systems](../../courses/cais-ethics-society/lecture-05-complex-systems.md) — watch before working the cascade exercises.
- **CAIS course**, [lecture-07-collective-action-problems](../../courses/cais-ethics-society/lecture-07-collective-action-problems.md) — watch before working the coordination exercises.
