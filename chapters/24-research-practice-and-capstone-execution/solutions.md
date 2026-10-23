# Chapter 24 — Solutions and rubrics

## Exercise 24.1 — scoping drill

**Full-credit solution.**

*"Is my model safe?"* → Scoped: "On the 200-item XSTest-modeled
over-refusal suite and the 300-item HarmBench-modeled refusal suite,
at base prompting, does the deployed model achieve non-refusal ≥
92% and refusal ≥ 90% respectively [Wilson intervals reported]?"
Decision rule: both point estimates clear thresholds AND both
intervals' lower bounds clear the deployment floor (92−2, 90−2).
Embarrassing result: any interval straddling the floor. *What the
unscoped version protects:* the refusal to name a construct —
"safety" averaged over incompatible constructs can never fail.

*"Does CoT help?"* → Scoped: "On the course's 100-item probe set,
does emitting CoT before the answer improve first-attempt accuracy
by ≥ 5 points over answer-only, with the CoT-conditioning check
(paraphrase-drift) reported alongside?" Rule: paired interval on
the difference excludes 0 and point estimate ≥ 5. Embarrassing:
conditioning near zero — the CoT is theater (Ch. 18's station 2).
*Unscoped protection:* "help" without a task, a denominator, or the
faithfulness confound.

*"Is X better than Y?"* → Scoped: "At true-rate gap g and n per
system, does X's measured rate exceed Y's with flip probability ≤
5% — and is the instrument's validity audit clean?" Rule: the
comparison is only claimable if gap × n × audit all pass.
Embarrassing: the flip probability at the achieved n exceeds the
claim's stakes. *Unscoped protection:* hiding the lottery ticket
inside "better" [SRC-PAPER-105].

**Rubric.** Each question scoped with context form + numeric rule +
embarrassment case (2 pts each, 6); the protection diagnosis naming
what vaguenness hides (4).

## Exercise 24.2 — the lottery, computed

**Full-credit solution.**

(a) Two-proportion power: for p₁ = 0.30, p₂ = 0.20, α = 0.05
two-sided (z = 1.96), power 80% (z_β = 0.84): n = (z_{α/2} +
z_β)² · [p₁(1−p₁) + p₂(1−p₂)] / (p₁−p₂)² = 7.84 × (0.21 +
0.16) / 0.01 = 7.84 × 0.37 / 0.01 = **290** — the chapter's 295
rounds conservatively (and any honest answer in 285-300 passes);
pooling at p̄ = 0.25 gives 7.84 × 0.375 / 0.01 = 294 — either
arithmetic shown with its assumption named.

(b) Flip probability, 3-point gap (0.70 vs 0.73), n = 400 per
system: μ = 400(0.70 − 0.73) = −12; σ = √(400·0.7·0.3 +
400·0.73·0.27) = √(84 + 78.84) = √162.84 ≈ 12.76. P(X_worse >
X_better) ≈ P(D > −0.5) for D ~ N(−12, 12.76) = 1 − Φ((−0.5 +
12)/12.76) = 1 − Φ(0.901) ≈ **0.184** — the worse system ranks
first roughly once in five comparisons at this "respectable" n.

(c) Six systems pairwise = 15 comparisons. If each is run at a
5% false-positive rate, the family-wise expectation is ~0.54
false "winners" even with *zero* true differences; and each
individual comparison carries its own flip probability (b's 18.4%
at small gaps). The demanded corrections: (i) pre-declare the
*one* primary comparison (the preregistration's job), (ii) report
every pairwise claim with its own flip probability, and (iii)
family-wise correction (e.g., Bonferroni-exact for the primary) or
refuse sub-5-point conclusions outright — in the chapter's
language, the multiplicity is the unstated lottery multiplier.

**Rubric.** Power arithmetic with assumptions (3); flip probability
with both variances and the continuity correction (3); the
multiplicity argument with a concrete correction demand (4).

## Exercise 24.3 — negative-result writing

**Full-credit results section (model answer).**

> We preregistered H1: a ≥ 10-point ASR reduction from
> provenance-spotlighting, supported only if the paired interval on
> the difference excluded zero with a point estimate ≥ 10 points.
> The study was powered (n = 300/arm) to detect a 10-point
> difference at 80% power, α = 0.05; smaller effects were not the
> design's target. Observed: ASR 22.4% treatment [18.0%, 27.5%] vs
> 24.1% control [19.5%, 29.4%]; paired difference −1.7 points, 95%
> interval including zero. H1 is **not supported**. The design could
> not have detected effects smaller than ~7 points at this n;
> effects of that size or smaller remain possible and unmeasured
> here. The ablation grid ran as preregistered: removing the
> provenance-marking step alone shifted ASR by −0.4 points
> (interval including zero), consistent with the mechanism not
> carrying the load the hypothesis assigned it. The trivial
> (keyword-refusal) baseline lost on quality as expected; the
> delimiter-convention baseline matched full spotlighting within
> intervals — the prior method remains the simpler default. We
> report this as a negative result because the power statement,
> the preregistered rule, and the ablation ledger all say the same
> thing: at deployable configurations, this mechanism did not earn
> its complexity.

**Rubric.** The power statement preventing the "no effect" misread
(3); point estimates with intervals and the preregistered rule's
verdict (3); the ablation ledger's honest fate (2); the
"effects smaller than X remain possible" sentence verbatim or
equivalent (2).

## Exercise 24.4 — the capstone proposal

**Full-credit proposal (skeleton; full submission 800-1,200 words).**

All eight components of §4's worked example, at the student's own
scale: scoped question in context form; preregistered H1/H2 with
*numeric* thresholds and the paired-interval rule; the power
arithmetic shown (with the formula and its assumption, not just the
n); the three baseline classes with the ablated-self named; the
lottery statement computed at the planned n (the flip probability
for the smallest gap the hypotheses care about); the ablation grid
listing each removed component; the negative-result commitment
(pre-stated shipping behavior); and the ethical-release review in
safety-case form (claims/evidence/defeaters/residual for the data,
the probes, any weights, and the people).

*The embarrassment requirement:* at least one statement that could
fail — e.g., "if the ablated-self baseline matches full-self within
intervals, the mechanism's contribution is unsupported and the
report ships as a negative result." A proposal with no such
statement is a plan, not a study, and loses the assessment's core
points.

**Rubric.** Eight components present and numeric where required (6);
the arithmetic correct (2); the embarrassment statement explicit (2).
