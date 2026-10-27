# Chapter 20 — Solutions and rubrics

## Exercise 20.1 — lower-bound grammar

**Full-credit solution.**

(a) Original: "no evidence of self-proliferation capability."
Unsupportable as stated because it drops both the elicitation scope
and the denominator — it reads as a claim about the model when it is
a claim about *the test*. Honest: "Under the tested elicitation (base
prompting, single-turn, no tools), the self-proliferation battery
produced 0 successes in 150 trials — a 95% upper bound of 2.5% under
that elicitation [0.0%, 2.5%] — with scaffolded and fine-tuned rungs
untested for this battery." Supported by exactly that measurement;
strengthened by each additional rung.

(b) Original: "the model passes 92% of our safety evals." Three
faults: no construct (which safety — refusal? toxicity? — mixed
constructs average away failures); no denominator; no elicitation
(safety evals at base prompting say nothing about the fine-tuned
arm). Honest: "On the 250-item XSTest-modeled over-refusal suite at
base prompting, appropriate non-refusal on 230/250 = 92.0% [88.0%,
94.9%]; on the HarmBench-modeled refusal suite, refusal on 4,326 →
[state]; the fine-tuned arm was not evaluated." The blended claim
hides exactly the trade Ch. 19 instrument 4 costed.

(c) Original: "the fine-tuned arm's autonomy rate is 31%."
Unsupportable because the bare number hides that 31% is one rung of
a ladder, on one probe set, with an interval that does not exclude
20%. Honest: "On the 100-item dangerous-capability probe's autonomy
subscale, the attacker-fine-tuned arm (refusal-suppressed
open-weight twin) completed 31/100 [22.8%, 40.6%], versus 24/100
[16.7%, 33.2%] scaffolded and 11/100 [6.3%, 18.6%] base — a ladder,
not a ceiling; the pre-stated escalation rule (lower bound > 20%)
fires."

**Rubric.** Each rewrite carrying elicitation + denominator +
interval (2 pts each, 6); the diagnosis naming what the original hid
(2); the measurement that would support each (2).

## Exercise 20.2 — the uplift study, correctly powered

**Full-credit solution.**

(a) With b = 17 (treatment completes, control fails) and c = 6
(reverse), the exact paired test is the binomial tail: under H₀,
b ~ Bin(23, ½). P(X ≤ 6) = Σ_{k=0}^{6} C(23,k)·2⁻²³. Compute the
ratio structure: C(23,6)/C(23,0) alone is 100,947, so the lower tail
is dominated by its last terms; summing exactly gives P(X ≤ 6) ≈
0.0174, two-sided p = 2 × 0.0174 ≈ **0.0347**. Order-of-magnitude
argument: the middle term C(23,11)/2²³ ≈ 0.168 is ~9.6× the k = 6
term, and the tail has ≤ 7 terms each below the k = 6 term, so
P(X ≤ 6) < 7 × 0.0174/1.15… — the honest version: the tail is small
because 6 is well below the mean 11.5, and the exact value is 0.0347
two-sided.

(b) Two-proportion power: detecting p₁ − p₂ = 0.15 with control
rate near p₂ = 0.13 (instrument 1's), p₁ = 0.28; variance per arm
p(1−p) ≈ 0.25 worst case; n per arm ≈ (z_{α/2} + z_{β})² · (p₁(1−p₁) +
p₂(1−p₂)) / (0.15)² ≈ (1.96 + 0.84)² · (0.2016 + 0.1131) / 0.0225 ≈
7.84 × 0.3147 / 0.0225 ≈ **110 per arm** (round up; with pairing and
expected discordance the paired test needs fewer — but only if the
correlation is real, which is a design bet, not a fact).

(c) Two threats: (i) *actor scarcity and heterogeneity* — experts
  are few and variable, widening intervals and inviting
  uncontrolled skill covariates (fix: paired designs within actor,
  stratified randomization); (ii) *grading validity* — "task
  complete" for real hazardous outcomes is contested and often
  ungradeable without domain experts who are themselves scarce and
  dual-use-constrained (fix: pre-registered grading rubric, blinded
  dual-grading with disagreement rates reported).

**Rubric.** Exact tail argument with the value 0.0347 or a valid
bound (3); power arithmetic with stated variance assumption (3);
both threats with fixes (4).

## Exercise 20.3 — gate audit

**Full-credit audit finding (skeleton).**

*Finding: threshold-definition / measurement mismatch (audit
question (ii)).* The framework's ASL-3 trigger is operationalized as
a *misuse-risk increase over non-AI baselines* — a two-arm uplift
construct [SRC-REPORT-008's own definition]. The release memo
supplies QA-probe scores: single-arm ability measurements with no
control arm, no randomization, no causal claim. The substitution
hides three things: (1) whether the model changes *outcomes* rather
  than answering questions — the entire distinction the definition
  encodes; (2) the elicitation ladder — QA probes sit at the base
  rung while the definition's risk actor climbs scaffolded and
  fine-tuned rungs; and (3) the baseline's strength — "over non-AI
  baselines" requires naming and dating the baseline, which the memo
  omits.

*Remediation demanded before signature:* an uplift study per the
framework's own definition — treatment/control arms with the
strongest dated non-AI baseline, paired by task, at the two highest
elicitation rungs, with pre-registered grading — or an explicit memo
paragraph downgrading the claim from "below ASL-3" to "not assessed
against the ASL-3 construct," with the gate decision re-made under
the weaker statement.

**Rubric.** Correct failing audit question identified (2); the
definition-vs-instrument mismatch stated in uplift terms (3); three
named hidden items (3); the remediation or the honest downgrade (2).

## Exercise 20.4 — release-evaluation design

**Full-credit design (skeleton; the full submission is 800-1,000
words).**

*Scope statement.* Covers malicious use [SRC-PAPER-093]; race,
organizational, and rogue-AI categories waived to the risk register.

*Persuasion and deception.* Construct: measurable attitude or belief
shift in recruited participants vs a baseline message arm. Arms:
model-crafted vs human-crafted vs control; n ≥ 200 per arm with
pre-registered instruments and deception debriefing; elicitation:
base + few-shot persuasion scaffolds (fine-tuning adds little here —
the capability is generative).

*Cyber-security.* Construct: task completion on sanctioned
CTF-style environments. Arms: model-assisted vs
search/baseline-assisted, expert and novice strata; ladder base →
agentic (tool loop) → fine-tuned (open weights make this the shipped
arm, not an attack — §3.5's point); denominators per stratum.

*Self-proliferation.* Construct: multi-step acquisition/replication
subtasks in sandboxed environments; zero-numerator reporting
mandatory with the elicitation qualifier; any success triggers the
escalation rule.

*Self-reasoning.* Construct: self-modification and self-analysis
subtasks; paired with the Ch. 18 monitorability instruments (a model
that reasons about its own oversight is a Ch. 18 concern re-indexed).

*Metric-mirage check:* every trended capability reported under one
thresholded and one continuous metric [SRC-PAPER-095]; discontinuity
claims require both metrics to jump.

*Pre-stated gate rules:* fine-tuned-arm lower bound > X% on autonomy
→ escalate; any uplift p < 0.05 with lower bound > Y points → ASL-3
assessment; zero-numerator bounds reported with rung scoping.

*Access conditions:* open weights ⇒ refusal-suppression is a base
property; API ⇒ the fine-tuning rung becomes prompt-optimization
plus any future LoRA-style endpoints — thresholds restated per
condition, not held fixed.

**Rubric.** All four areas with constructs/instruments/arms (4);
open-weights ladder logic correct (2); mirage check included (1);
gate rules pre-stated with numbers (2); waived categories stated (1).

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **DeepMind course**, [part-03-03-dangerous-capability-evaluations](../../courses/google-deepmind-agi-safety/part-03-03-dangerous-capability-evaluations.md) — watch before working the uplift-framing exercises.
