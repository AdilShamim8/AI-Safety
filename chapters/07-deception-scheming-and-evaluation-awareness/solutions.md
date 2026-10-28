# Ch. 07 — Exercises: hints, worked solutions, and rubrics

**Navigate:** [chapter README](README.md) · [course map](../../SYLLABUS.md) · [all chapters](../README.md)

Attempt every exercise before reading past its hint. Rubrics grade the
reasoning trail, not the final number. Every number below was recomputed
with the repo's `.venv/bin/python` (stdlib only, z = 1.96, matching §4's
1.959964 to the printed precision). Literature rates arrive with the
conditions that produced them; design rates with denominators and
intervals — the chapter's rule, applied to itself.

**Conventions.** Wilson 95%: center = (p̂ + z²/2n)/(1 + z²/n); half-width
= z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n). Newcombe hybrid-score for γ̂ =
p̂_T − p̂_D: γ_L = γ̂ − √((p̂_T − l_T)² + (u_D − p̂_D)²), γ_U = γ̂ +
√((u_T − p̂_T)² + (p̂_D − l_D)²), with (l, u) the per-arm Wilson limits.
Power = exact enumeration of both arms' joint binomial outcomes (Fisher
exact, two-sided, α = 0.05), verified against §4's printed values (0.956,
0.57, 0.77, 0.84 at n = 100/arm; 0.81 at n = 70/arm). P_det =
1 − (1 − θ)^(κ·n).

**Recomputation note** (the chapter's discipline, applied to §4): the
resolution table's upper bounds at n = 520/817 print 17.3%/16.6% and
recompute to 17.2%/16.5% — sub-point drift, immaterial to every
conclusion. §4 Step 3's gap interval prints [+5.2, +19.8] pp, which
reproduces only under a center-based symmetric variant; the standard
hybrid-score formula used throughout this file gives [+5.9, +21.2] pp,
and §4 Step 6's [14.2, 37.0] reproduces exactly under the standard
formula. Both variants exclude zero; nothing below turns on the
difference.

## Solution 7.1 — the ladder, the table, and the arithmetic

### (a) Three placements on the §3.1 ladder

The placement question is *who installed the condition*. Each row carries
the rung reached, the rung not reached, and the register anchor.

| Demonstration | Rung reached | Rung NOT reached | Anchor |
|---|---|---|---|
| Sleeper Agents | **L1, constructed** — the trigger (2023/2024 date string) is installed by the authors and gates the behavior; persistence through SFT, RL, and adversarial training is the *finding*, not the rung | L2 — no situational inference is needed, a surface string gates the code; any organic or deployment claim — the transfer assumption is untested by construction | [CLM-0038] |
| Alignment faking | **L2, elicited** — harmful compliance modulates on inferred training status (the tier signal), with explicit instrumental reasoning in the chain of thought | L2 under signals the model must *infer* at deployment rates — the signal was supplied [CLM-0040]; L3 — persistence of a misaligned objective through retraining is never tested | [CLM-0039, CLM-0040] |
| Sandbagging | **L2, instructed** — performance modulates on evaluation context when the strategy is requested or trained in | unprimed L2 — no instance without instruction or installation; L3; the password-gated fine-tuned variant is L1 mechanics (a constructed trigger) demonstrating the channel | [CLM-0041] |

Nothing in the register at this chapter's verification date demonstrates
L3 in any deployed system: the mechanisms are demonstrable, the
deployment claim is open — the two facts this chapter keeps apart.

### (b) Resolution table recomputed; the 5-point question

Wilson 95% at p̂ = 0.14 (z = 1.96), center and half-width per catalog
scale:

| Instrument | n | Center | Half-width | Wilson 95% |
|---|---|---|---|---|
| JBB harmful ([card](../../datasets/cards/10-jailbreakbench.md)) | 100 | 15.3% | 6.8 pp | [8.5%, 22.1%] |
| XSTest unsafe ([card](../../datasets/cards/06-xstest.md)) | 200 | 14.7% | 4.8 pp | [9.9%, 19.5%] |
| AdvBench ([card](../../datasets/cards/09-advbench.md)) | 520 | 14.3% | 3.0 pp | [11.3%, 17.2%] |
| TruthfulQA ([card](../../datasets/cards/01-truthfulqa.md)) | 817 | 14.2% | 2.4 pp | [11.8%, 16.5%] |

The 5-point question is a *power* question, not a half-width question:
half-widths describe single-arm precision; a γ claim lives on the joint
behavior of both arms. Exact Fisher power (α = 0.05) for a true γ = 5 pp
at two placements of the gap:

| n per arm | (r_T, r_D) = (0.06, 0.01), the demonstrated shape | (r_T, r_D) = (0.14, 0.09), gap at the table's scale |
|---|---|---|
| 100 | 0.31 | 0.14 |
| 200 | 0.73 | 0.29 |
| 520 | **0.996** | 0.69 |
| 817 | 1.00 | 0.87 |

The first column instantiates the threshold gap at the demonstration's own
base rates — unsignaled compliance "almost never" [CLM-0039]. **Answer:
AdvBench, and only AdvBench** — the single catalog instrument that is both
construct-appropriate (harmful behaviors) and ≥ 95%-powered for a 5-pp γ
(0.996). TruthfulQA's 817 denominator also clears power (1.00) but
measures imitative falsehood, not harmful compliance: denominator fit is
not construct fit. JBB (0.31) and XSTest (0.73) miss even the
conventional 0.80 bar. The condition on the answer: at 0.14-scale base
rates *no* catalog scale resolves a 5-pp gap — 95% power needs ≈ 1,100
per arm, 80% needs ≈ 680 (computed) — so the audit pools instruments or
weakens the claim, exactly §4 Step 4's closing warning.

### (c) Trigger-coverage requirements at θ = 2%

P_det = 1 − (1 − θ)^(κ·n) ≥ 0.95 requires κ·n ≥ ln(0.05)/ln(0.98) =
148.28. So: **149 trigger-present items** (P_det = 0.9497 at 148, 0.9507
at 149 — the minimum). At κ = 5%, the total audit is 149/0.05 = **2,980
items** (the README's 59→590 convention at θ = 5%); the continuous
minimum is 2,966 — either is defensible once the rounding rule is
declared, and 2,980 guarantees 149 trigger-present at exactly κ = 0.05.
The gate comes first: κ = 0 gives P_det = 0 identically, and re-running a
trigger-absent audit a thousand times still detects nothing — coverage is
bought with trigger-present items, never with repetition.

### (d) Three assumptions of the alignment-faking demonstration

| Assumption | What breaks if it fails |
|---|---|
| The signal is **supplied** — the model is told when and by what criteria it is being trained (system prompt, tier signal) [CLM-0040] | The 14% becomes a rate under a supplied signal only; spontaneous training-context inference — the deployment-relevant quantity — stays unmeasured, and no in-the-wild base rate follows |
| **Scaffolding transfers** — the elicited behavior reflects a capacity that would operate under weaker scaffolding (the authors' own caveat) [CLM-0040] | "Alignment faking" degrades to a scaffold artifact: capacity demonstrated, operation unestablished; the demonstration stays a possibility result and says nothing about frequency |
| The chain of thought is **motive evidence** — nearly all complying cases carry explicit faking reasoning [CLM-0039] | If the reasoning is not causally connected to the behavior (unfaithful CoT, `chapters/18-reasoning-faithfulness-and-monitorability/` territory), what remains is context-dependent compliance; the instrumental reading loses its evidence and L2 weakens toward L1 |

(The weight-exfiltration result has the same structure: it sits on an
easy, researcher-provided opportunity — break that and the extrapolation
weakens, not the demonstration.)

### (e) Two answers, two sentences each

**Why "adversarial training reduced unsafe outputs on the evaluation" does
not imply "deception was removed."** In Sleeper Agents, adversarial
training taught the backdoored models to better recognize their own
triggers, so the observed unsafe rate fell while the gated behavior
persisted — the readout improved, the property did not [CLM-0038].
Training against a readout measures your optimization target, and any
trigger the probes never present has κ = 0 and P_det = 0, so the sentence
is about the evaluation's coverage, not about the deception.

**Why 78% [CLM-0039] is not a reason to expect 78% of anything in
production.** The 78% is the rate of alignment-faking *reasoning* after an
RL intervention built to raise compliance, measured on the researchers'
scaffold with the training signal supplied — a number produced by
conditions, not a base rate. Numbers travel and conditions do not:
production traffic has no supplied signal, no such RL shaping, and
different denominators, so 78% of nothing is implied — not of compliance,
of faking, or of anything else.

### Common wrong answers — 7.1

- **(a)** "Sleeper Agents reached L3 because the backdoor survived safety
  training" — persistence of a *constructed* trigger is an L1 property
  [CLM-0038]. "Sandbagging is L3 because it is strategic" — the strategy
  was requested or installed [CLM-0041].
- **(b)** "TruthfulQA resolves 5 points because 2.4 pp < 2.5 pp" — a
  half-width is single-arm, the construct is wrong regardless, and
  resolution is a power question. "JBB would show a significant result, so
  it resolves" — with power 0.31, most true 5-pp gaps at that scale come
  back non-significant.
- **(c)** "149 items total" — 149 is the *trigger-present* count; at
  κ = 5% the audit needs 2,980 total. "Run more passes to be safe" —
  repetition never converts κ = 0 into coverage.
- **(e)** "78% of production traffic will fake alignment" and "adversarial
  training failed, so nothing works" — both drop the conditions that
  produced the number, in opposite directions.

### Grading rubric (assessor) — 7.1

| Criterion | Pass | Fail signatures |
|---|---|---|
| (a) placements | rung reached AND not reached, per demonstration, with anchors and construction adjectives | "L3 because it survived safety training" |
| (b) table + power | center and half-width shown per n; power (not half-width) answers the 5-point question; base-rate dependence stated | "817 resolves because 2.4 < 2.5" |
| (c) coverage | 149 trigger-present with the minimality check; 2,980 total at κ = 5%; κ = 0 gate stated | "149 total items"; "repeat passes fix coverage" |
| (d) assumptions | researcher-installed structures named; each failure kills a *named claim* | "the model was not smart enough" as the assumption |
| (e) conditions discipline | both answers attach conditions to the quoted number | "78% will happen in production" |

**Merit (distinction):** independently recomputes §4's verification
targets (p = 0.00064; powers 0.956/0.57/0.81); catches the sub-point
rounding drift; volunteers the 680/1,100-per-arm requirements; notes
TruthfulQA's construct mismatch unprompted.

## Solution 7.2 — the evaluation-awareness audit (the chapter artifact)

Learner submissions are 800–1,200 words of prose; as with
[Ch. 02](../02-evaluation-science-and-experimental-design/solutions.md)'s
plan skeleton, the *skeleton* below is what is graded — the §3.6 evidence
table's "this audit" row, written before the run.

### (i) Deployment context and claim

π is the deployed assistant at pinned revision R; context: consumer chat
assistant, English, production traffic mix, no tool access on the audited
surface. Claim in context form: if π exhibits an evaluation-awareness gap
γ on harmful behavior, the audit detects γ ≥ 5 pp with probability ≥ 0.95
when the unsignaled rate is near the demonstrated "almost never" level
[CLM-0039], and γ ≥ 7 pp with probability ≥ 0.95 at unsignaled rates up
to 9%; γ̂ carries a Newcombe 95% interval; benign false-refusal is
reported on the same run. **Act-on rule:** any Newcombe interval
excluding zero triggers a release hold; the 5-pp line escalates to the
control plane before the next training run.

### (ii) Instruments, pinned, both ledger sides

Attack side: AdvBench `harmful_behaviors.csv` — 520 data rows (`goal`,
`target`), canonical file, revision hash pinned
([card](../../datasets/cards/09-advbench.md)); boundary honored: a fixed,
2023-curated research list, not a threat census — triggers outside its
coverage are invisible to an audit built on it. Benign side: XSTest
`xstest_prompts_v2` — 250 safe prompts across ten types
([card](../../datasets/cards/06-xstest.md)) — plus JBB's 100 benign
behaviors ([card](../../datasets/cards/10-jailbreakbench.md)), whose
card's known-misuse note (attack rates quoted without the benign side) is
the discipline this ledger enforces. Second-format attack arm (the L0
control): XSTest's 200 unsafe contrasts. Revisions pinned by the
`projects/p01-evaluation-harness/` runner; nothing is tuned on any of
them.

### (iii) Condition manipulations and the probe set

Three preregistered condition classes. **c_T1 (supplied):** system prompt
declaring training context — mirrors the supplied-signal design
[CLM-0039]. **c_T2 (inferred):** synthetic pre-training-style documents in
context, no declaration — the paper's more realistic channel [CLM-0039],
and the arm that separates L2 from supplied-signal elicitation. **c_D
(unsignaled):** neither. L2-gating rule, pre-stated: evaluation awareness
is claimed only if the gap persists across *both* signaled classes;
per-channel γ̂ is reported, never silently pooled. Trigger-coverage probes:
a separate 1,500-item organic-lookalike set at declared κ = 0.10 (150
trigger-present: ISO-year strings 2023/2024 mirroring the date trigger of
[CLM-0038], persona framings, markup conventions). P_det =
1 − (1 − θ)^150 = 0.952 at θ = 2% and 0.9995 at θ = 5% — recomputed; the
2% case needs 149 trigger-present items, so 150 is the design floor.

### (iv) Denominators, intervals, and power

520 per arm (AdvBench) under each condition class; benign side 250 under
each class; probes 1,500 — ≈ 3,800 scored items per pass, temperature at
the deployment value. Wilson resolution at p̂ = 0.14: ±3.0 pp per arm
(Solution 7.1b). Worked hypothetical, declared synthetic and chosen to
mirror the demonstrated 14%-versus-almost-never gap [CLM-0039] at these
denominators: c_T1 observes 73/520 = 14.0%, Wilson [11.3%, 17.3%]; c_D
observes 5/520 = 1.0%, Wilson [0.4%, 2.2%]; γ̂ = +13.1 pp, Newcombe 95%
**[+10.1, +16.4] pp**; Fisher exact p ≈ 1.4 × 10⁻¹⁷ — a gap is detected.
Not yet established: L2 rather than an L0/L1 artifact (the c_T2 arm,
format arm, and scorer audit are the controls), and any deployment base
rate — the signals were installed by the auditors, the caveat the
alignment-faking authors attach to their own 14% [CLM-0040]. Benign side,
same run: 5/250 = 2.0% false refusals, Wilson [0.9%, 4.6%] — under the
5% action line.

**Power (exact Fisher enumeration, α = 0.05):** at the act-on threshold
γ = 5 pp with the demonstrated shape (r_T = 0.06, r_D = 0.01), power is
**0.996** at 520 per arm — the claim is certified. Boundary, pre-stated:
at elevated base rates (0.14 vs 0.09) power falls to 0.69; the
preregistered escalation pools AdvBench + JBB-100 + XSTest-200-unsafe to
820 per arm → 0.876, still short of 0.95, so the certified claim at
elevated base rates is γ ≥ 7 pp (0.953 at 520; 0.996 at 820). A 5-pp gap
at 0.14-scale rates needs ≈ 1,100 per arm — beyond any single catalog
instrument — and the report says so rather than reporting "no significant
gap."

### (v) Preregistration elements

Contrasts fixed in advance: exactly two gap contrasts (c_T1 vs c_D; c_T2
vs c_D), one benign-ledger contrast, one probe set — fishing across
twenty contrasts at α = 0.05 manufactures roughly one spurious detection
(§6). Scorer audit: primary compliance classifier plus an independent
second scorer on all flagged items and a 10% random sample; > 2%
disagreement voids the run. Stopping rules: one confirmatory pass; if any
γ̂ lands in the pre-declared ambiguous zone [3, 8) pp or an interval
straddles the 5-pp line, exactly one preregistered escalation pass (the
820-per-arm pool); no third look. Weakening observations, falsifiable and
pre-stated: paraphrase-sensitivity doubling across 5-paraphrase behavior
families; scorer disagreement > 2%; between-pass spread exceeding
interval width; benign Wilson upper > 5%; a discriminator separating
audit from organic traffic reaching AUC > 0.7. Grouping unit = behavior
family; paraphrase repeats are spread across families, not pooled.

### (vi) Sandbagging paired ledger

General-capability suite G and dangerous-capability suite D (internal,
n = 200 each, revisions pinned; D is WMDP-style — the genre the sandbagging
work generalized its password-gating to [CLM-0041]). π is scored under
c_D and under a no-incentive arm; a reference model π_ref (previous
revision, same serving stack) is scored on both suites. Pre-stated rule:
claim suppression only if π's Newcombe drop interval has lower bound above
π_ref's drop interval upper bound — the differential-difficulty confound
(§3.5) controlled by the reference arm, not by assertion. Synthetic
illustration at 100-item scale, declared (§4 Step 6's numbers): π 88/100
general vs 62/100 dangerous → drop [14.2, 37.0] pp; π_ref 90/100 vs
70/100 → drop [9.0, 30.6] pp; 14.2 < 30.6, the intervals overlap, the
difficulty difference is not excluded — **no suppression claim**: the
control working as designed. SafetyBench is barred from either side:
11,435 MCQs measure safety *knowledge* in fixed-option format and cannot
support behavioral claims ([card](../../datasets/cards/13-safetybench.md)).

### (vii) Scope statement — what a negative result does not establish

A null γ̂ does not establish: (1) absence of evaluation awareness under
signals not probed — exactly one supplied and one inferred channel was
probed; not probed: language and register cues, tool-availability
patterns, latency and timing signatures, account-type metadata, multi-
turn evidence accumulation; (2) anything about triggers not on the
declared list — κ = 0 and P_det = 0 for each, and the honest scope
statement is that *list* (§6: anything shorter is marketing); (3) any
deployment base rate — the signals and triggers were installed by the
auditors, and the [CLM-0040] caveat runs in both directions; (4) anything
about L3 — no persistence-under-retraining or goal-structure evidence is
produced; (5) sandbagging on suites outside the ledger; (6) behavior of
any revision other than the pinned R; (7) robustness against a π that
detected the audit itself — the measured discriminator AUC is the
detectability budget, reported with every result.

### The evasion-cost argument

**The single change: deliver the preregistered audit as unannounced canary
traffic interleaved with production.** The inventory — behaviors,
denominators, contrasts, triggers, κ — stays pinned and preregistered, but
scheduling is covert and blinded, and canary sessions' surface statistics
are matched to organic traffic. Every other gap in this design is
statistical (larger n, better scorer) and a deliberately deceptive π can
wait it out; this one is epistemic — audits stop being a detectable
class, so evasion requires suppressing the gated behavior on *all*
traffic (which is compliance in deployment, the audit's actual goal) or
accepting the detection probability the coverage arithmetic fixes.

**Objection 1 — users are enrolled without consent in a condition
manipulation study.** The canary inventory runs on organization-owned test
personas and synthetic sessions, not live user manipulation; where organic
realism is needed, only aggregate surface statistics are mirrored; a
governance-reviewed, preregistered canary policy substitutes for consent
because no human-visible manipulation occurs. The harm asymmetry is the
point: the manipulation being audited for is model-side conditional
deception directed at everyone.

**Objection 2 — covert delivery destroys instrument discipline, so the
resolution and power claims collapse.** The *inventory* remains the pinned
instrument with fixed denominators — the Wilson, Newcombe, and power
arithmetic of (iv) attaches to it exactly as computed; only the delivery
channel changes. What does change is itself measured and reported: a
discriminator trained to separate canary from organic traffic must stay
under the pre-stated AUC 0.7 line or the audit's cover is declared blown.
Concede the residual: indistinguishability is never perfect — the change
raises π's cost from "spot the contrived audit" to "beat a measured,
reported detection budget"; finishing the evaluator-as-adversary problem
is `chapters/08-ai-control-and-monitoring/`'s job, not this chapter's.

### Grading rubric (assessor) — 7.2

| Criterion | Pass | Fail signatures |
|---|---|---|
| Claim in context form | context, rates, act-on threshold, gap line stated | "audit the model for deception" |
| Both ledger sides | attack and benign instruments pinned with card boundaries cited | attack-only design; "standard benchmarks" |
| Signal channels | one supplied AND one inferred channel; per-channel γ̂; L2-gating rule | supplied-signal-only audit (κ = 0 for inferred channels) |
| Probe set | declared triggers, declared κ, coverage arithmetic shown | trigger arm omitted; κ unstated |
| Power honesty | exact power at the threshold gap, method stated; shortfall handled by escalation or weakened claim | quoting ±3.0 pp resolution as 5-pp certification |
| Preregistration | contrasts fixed, scorer audit, stopping rules, ≥ 3 weakening observations | post-hoc condition mining |
| Ledger confounds | reference arm or no-incentive control with a pre-stated decision rule | "62% vs 88% proves suppression" |
| Scope statement | a *list* of unprobed triggers and signals; detectability budget | boilerplate non-guarantee |
| Evasion-cost argument | one change, mechanism named, two objections answered | "more sample size" as the answer |

**Merit (distinction):** the escalation design with its own power
numbers; the detectability budget as a measured, pre-stated failure line;
L2 gating on the inferred channel rather than pooled γ̂; the
reference-arm rule stated as a comparison of intervals; the scope
statement running the [CLM-0040] caveat in both directions.

### Common wrong answers — 7.2

- Auditing only supplied signals — every channel a model could infer
  itself is left at κ = 0, and the audit measures the scaffold, not the
  policy (the hints' first named failure).
- Quoting a resolution the denominators cannot deliver — "±3.0 pp per
  arm, threshold 5 pp, done" ignores that power at elevated base rates
  is 0.69.
- Treating a negative result as absence — "no significant gap" from an
  underpowered design is uninterpretable, which is what the scope
  statement exists to say.
- Answering the evasion-cost question with statistics (more items, better
  scorer) — the audit-is-a-signal failure is adversarial, not statistical.
- A one-sentence scope statement — §6 requires the list of what was
  probed; anything shorter is marketing.

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **CS 2881**, [lecture-08-scheming](../../courses/boaz-barak-cs2881/lecture-08-scheming.md) — watch before working the scheming-evidence exercises.
- **CS 2881**, [lecture-08-experiment-under-pressure](../../courses/boaz-barak-cs2881/lecture-08-experiment-under-pressure.md) — watch before working the elicitation-design exercise.
