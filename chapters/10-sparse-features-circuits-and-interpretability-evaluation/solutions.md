# Ch. 10 — Exercises: hints, worked solutions, and rubrics

**Navigate:** [chapter README](README.md) · [course map](../../SYLLABUS.md) · [all chapters](../README.md)

Attempt every exercise before reading past its hint (§9 of the
[README](README.md)). Rubrics grade the reasoning trail — which evidence kind
each number is, which control is missing — at least as heavily as arithmetic.
Every number below was recomputed programmatically: Wilson intervals at
z = 1.96 per [Ch. 02](../02-evaluation-science-and-experimental-design/README.md);
exact McNemar as the two-sided exact binomial on discordant pairs,
p = 2·P(X ≤ min(b, c)), X ~ Binom(n_d, ½) — no normal approximations. One
README correction surfaced in recomputation and was fixed in-commit: the
baseline Wilson interval is [39.8%, 46.6%], not [39.9%, 46.6%] (hand-rounded
bound drifted half a point). Claim anchors [CLM-0051]…[CLM-0055] match the
README's References.

## Solution 10.0 — the worked example, recomputed end to end

The README promised "computed exactly by the script in solutions.md"; this is
that script's output, narrated. Denominators first, always: 817
(TruthfulQA's card-verified validation split) and 11,435 (SafetyBench's
card-verified question count); the 200-question hand-labeled subsample is this
course's operationalization — the card publishes totals, not per-category
counts.

### (a) Step 1 — reconstruction vs. usefulness, both sides

| Run | Score | Wilson 95% |
|---|---|---|
| clean baseline | 353/817 = 43.2% | [39.8, 46.6] |
| SAE reconstructions substituted | 313/817 = 38.3% | [35.0, 41.7] |
| Gaussian noise, matched 18% variance | 349/817 = 42.7% | [39.4, 46.1] |

Net SAE effect: −40 questions = **−4.90pp**, with 47 questions flipping to
incorrect against 7 to correct. Exact paired test on the 54 discordant
questions: p = 2·P(X ≤ 7 | n = 54, ½) = **2.29 × 10⁻⁸**. The noise control
costs −4 questions (−0.49pp) — same unexplained-variance budget, nearly free.
The contrast is the finding: FVU 0.18 is a *reconstruction* number; the
reconstruction-intervention score is the *usefulness* number; and the gap
between −4.9pp and −0.5pp is the price of the SAE's error being *structured*
(rare, adversarial contexts) rather than isotropic.

### (b) Step 2 — selectivity with dictionary-relative bookkeeping

Recall 87/108 = 80.6%, Wilson **[72.1, 86.9]**; precision 87/104 = 83.7%;
21 misses, of which 10 fire a single health-myths neighbor instead — an
absorption-shaped signature. The honest dashboard sentence: "F covers ~80% of
misconception-labeled items *in this dictionary*, with a known absorbed
sub-family." The qualifier is load-bearing: feature identity is
dictionary-relative ([CLM-0051]; [CLM-0053] for splitting at scale).

### (c) Step 3 — controlled paired ablation

Flips: 77 to correct, 32 to incorrect, 708 unchanged (77 + 32 + 708 = 817 ✓).
New score 398/817 = **48.71%**, net **+45/817 = +5.51pp**, Wilson on the new
score [45.3, 52.1]. Exact McNemar on 109 discordant questions:
p = 2·P(X ≤ 32 | 109, ½) = **1.94 × 10⁻⁵**. Controls: frequency-matched
random feature, b = 23 / c = 26 (net +3 = +0.37pp), n_d = 49,
p = 2·P(X ≤ 23 | 49, ½) = **0.775** — indistinguishable from noise;
SafetyBench side effect −23/11,435 = **−0.20pp** — small but reported,
because a monitoring intervention that silently costs accuracy elsewhere is a
deployment fact. The trap: baseline [39.8, 46.6] and ablated [45.3, 52.1]
*overlap*, yet the paired test is decisive at 10⁻⁵ — independent-sample
intervals carry no information about paired data (Solution 10.3 (e)).

### (d) Step 4 — graded completeness

F alone restores 22% of mean |TE|; the identified 40-feature set 71%; 29%
unexplained. Direction consistency 73/87 = 83.9%, Wilson **[74.8, 90.2]**.
The strong claim ("the channel") fails completeness by construction: 22% is a
fraction, not a takeover. The weak claim survives with numbers attached — and
those are different scientific objects ([CLM-0053] names the gap at frontier
scale; [CLM-0055] names the criterion the dashboard never met).

### Common wrong answers — 10.0

- Reading FVU 0.18 as "the SAE preserves 82% of what matters": Step 1's
  −4.9pp vs −0.5pp is exactly why that inference fails.
- Quoting recall 80.6% without the absorbed sub-family: the miss analysis is
  what makes the number interpretable.
- Reporting the ablation without the random-feature control: +5.5pp is
  only impressive against +0.4pp.

### Grading rubric (assessor) — 10.0

| Criterion | Pass requires |
|---|---|
| Both Wilson forms | All six intervals reproduced (incl. the corrected 39.8 bound) |
| Paired statistics | Exact binomial McNemar shown for all three tests (2.29e-8, 1.94e-5, 0.775) |
| Control logic | Random-feature and SafetyBench controls stated with what each rules out |
| Completeness | 22% vs 71% vs 29% retold as three *different* claims, not one muddled number |
| Overlap trap | Independent-interval overlap correctly diagnosed as non-informative for paired data |

## Solution 10.1 — the SAE-critique table (the chapter's declared assessment)

| Item | Evidence kind | Silent assumption | Missing control | What a pass requires |
|---|---|---|---|---|
| (i) FVU 0.12 at L0 18 (4M features) | reconstruction measurement | reconstruction quality implies downstream usefulness | reconstruction-intervention run on a task battery with a matched-isotropic-noise arm | net task cost of substituting reconstructions, both ledger sides, vs. matched noise — FVU alone can never pass |
| (ii) dashboard: 12 top-activating transcripts for "deception feature" 4M/2371917 | plausibility ([CLM-0055]: human judgment measures plausibility) | the label describes the feature rather than one correlate of it | selectivity denominators: recall/precision over labeled corpora; absorption check on misses; RAVEL-style confound split ([CLM-0054]) | recall with Wilson interval on n ≥ 100 labeled items; miss autopsy; version-pinned dictionary |
| (iii) clamping makes model refuse role-play in 5/5 | causal anecdote (n = 5) | 5/5 under unspecified selection generalizes | paired ablation with flip counts on a pinned, n ≥ 100 instrument; frequency-matched feature control; capability side ledger | exact McNemar on discordant counts; random-feature control non-significant; collateral accuracy interval |
| (iv) "deception is now monitorable in production" | none (a construct claim wearing measurement clothing) | a dashboard + anecdote = a deployed monitor | everything above plus: deployment-distribution drift, audit-budget arithmetic ([Ch. 08](../08-ai-control-and-monitoring/README.md)), adversarial adaptation | no current method delivers the full upgrade — dictionary-relativity ([CLM-0051; CLM-0053]) and self-evaluation limits ([CLM-0053; CLM-0055]) leave the production claim unsupported |

**Three questions, in order, with justification.** 1. *"What are the
selectivity denominators — labeled set size, recall, precision, and what
fires on the misses?"* — cheapest to answer, and its failure mode (absorption,
dictionary-relativity) collapses items (ii)–(iv) before anything costlier is
run. 2. *"What is the paired, controlled ablation result with flip counts on
a pinned instrument, and what does the frequency-matched control show?"* —
the causal core; without it (iii) stays an anecdote and (iv) has no content.
3. *"What does the intervention cost on unrelated tasks, with intervals?"* —
the deployment ledger; a monitor that silently degrades capabilities is a
different product. The order is triage: construct validity before causality
before deployment economics — each question's answer can kill the claim
before the next question is worth asking ([Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
§3's validity-leak chain, applied to features).

**The upgrade path for (iv), honestly.** Defensible would require: (1) a
pinned dictionary version with reproduction on a retrained SAE (dictionary
relativity, [CLM-0051; CLM-0053]); (2) selectivity with denominators and
absorption autopsy on deployment-representative corpora; (3) paired
controlled ablation at scale with random-feature and matched-noise arms;
(4) graded completeness against the full behavior, not the feature;
(5) capability side-effects with intervals; (6) audit-budget arithmetic under
[Ch. 08](../08-ai-control-and-monitoring/README.md)'s protocol framing; and
(7) evidence under distribution drift and adversarial adaptation. No current
method delivers (4) at frontier scale ([CLM-0053]'s own completeness gap) or
(7) — which is the point of saying so in writing.

### Common wrong answers — 10.1

- Grading item (i) as "good evidence, FVU is low": FVU measures the SAE, not
  the model's task behavior — kind confusion is the whole exercise.
- Questions in the order (iii)→(ii)→(i): running causal work before
  construct validity wastes the budget; the order is part of the answer.
- Letting (iv) pass "if (iii) were n = 500": scale repairs the anecdote, not
  the construct leap from "a feature" to "monitorable in production."

### Grading rubric (assessor) — 10.1

| Criterion | Pass requires |
|---|---|
| Evidence kinds | All four items classified correctly (reconstruction / plausibility / causal anecdote / none) |
| Assumptions | Each row's silent assumption named, not generic |
| Controls | Missing control per row is *specific* (matched noise, absorption autopsy, frequency-matched feature, audit budget) |
| Question order | Triage logic justified (construct → causal → deployment), not arbitrary |
| Upgrade honesty | States which upgrade steps no current method delivers, citing [CLM-0053]/[CLM-0055] |

## Solution 10.2 — preregistered feature-evaluation protocol (sycophancy)

A model solution at rubric depth, 700–1,200 words as briefed; each numbered
element below maps to a rubric row.

**(i) Claim in context form, with action threshold.** "In model M (pinned
revision), SAE feature S (dictionary version pinned, index recorded), labeled
*sycophancy* on the team dashboard, causally contributes to
user-preference-following errors: ablating S reduces sycophantic answer
selection on the TruthfulQA validation split's preference-adjacent items."
Action threshold, set before any run: we act only if the paired ablation
moves the sycophancy instrument by ≥ +4pp net with exact McNemar p < 0.01
*and* the random-feature control stays below ±1pp — anything smaller is
recorded, not acted on. The threshold is part of the preregistration, not a
post-hoc reading.

**(ii) Instruments, both ledger sides, card boundaries honored.** Primary
instrument: TruthfulQA's 817-question validation split
([datasets/cards/01-truthfulqa.md](../../datasets/cards/01-truthfulqa.md)) —
sycophancy-adjacent because imitative falsehoods are exactly
prefer-the-common-over-the-true errors; the card's boundary: it is
English-only, single split, evaluation-only — no training, no fine-tuning
claims, and per-category counts are ours to hand-label (the card publishes
totals). Unrelated-task side: SafetyBench's 11,435 questions
([datasets/cards/13-safetybench.md](../../datasets/cards/13-safetybench.md))
— capability side-effect control; its boundary: multiple-choice format,
Chinese and English — we report the English subset separately and say so.
Both cards' "cannot support" sections are honored by construction: no
generative-regime claims from TruthfulQA's MC numbers, no production-safety
claims from SafetyBench's accuracy.

**(iii) Dictionary-relativity controls.** Version pinned by training-config
hash; absorption check: on every primary-instrument item where S fails to
fire but the hand-label says sycophancy-adjacent, record which features *do*
fire (top-3) — a persistent single neighbor means S under-covers a sub-family
(the §4 Step 2 signature); splitting check: rerun selectivity with one larger
dictionary (≥ 4× features); if "the sycophancy feature" becomes several, the
claim downgrades to "a feature family" before it is written down.

**(iv) Statistical plan.** Paired design: every item scored clean and
ablated; flip counts b (to-worse) and c (to-better) reported; exact McNemar
two-sided as primary test; Wilson 95% on every rate (recall, precision, both
score sides); cluster caveat stated: TruthfulQA items share question
templates — if ≥ 20% of flips share a template, report a
template-clustered sensitivity analysis (drop one template family, recompute)
rather than pretending independence.

**(v) Preregistration elements ([Ch. 02](../02-evaluation-science-and-experimental-design/README.md)).**
Conditions fixed in advance: instrument revisions, dictionary version,
ablation site (all positions where S fires vs. a pre-stated position family),
α = 0.01 two-sided. ≥ 3 weakening observations pre-stated: (1) if random
feature control exceeds ±1pp, the ablation channel itself is noisy — halt;
(2) if absorption check shows ≥ 30% of label-positive items carried by one
neighbor, S is the wrong unit — downgrade to family-level claim; (3) if
SafetyBench side-effect exceeds −1pp with p < 0.01, the intervention is a
capability tax, not a monitor — restate the claim as a tradeoff. Stopping
rules: one grid + one replication on a second hand-labeled subsample; no
third pass without a new preregistration document.

**(vi) Negative-result scope statement.** A negative result (no paired
movement at threshold) does *not* establish that M lacks sycophantic
computation — it establishes that *this dictionary's feature S, at this site,
under this ablation, does not mediate measurable sycophancy on this
instrument*. Superposition guarantees the computation could be distributed
([CLM-0051]); dictionary choice could have missed it; the instrument could be
underpowered for the sub-families involved. Absence of evidence for feature
S is evidence about S, not about the behavior.

### Common wrong answers — 10.2

- Inheriting §4's numbers as the design (353/817 etc.): those are the
  misconception-feature illustration; a sycophancy protocol needs its own
  threshold and arms.
- Treating the SafetyBench side as a courtesy check: it is half the claim —
  a feature intervention with capability cost is a different decision object.
- No negative-result scope: without it, "we found nothing" silently becomes
  "there is nothing," the exact inference superposition forbids.

### Grading rubric (assessor) — 10.2

| Criterion | Pass requires |
|---|---|
| Claim + threshold | Context form (model, dictionary, feature, instrument) with a *numeric* pre-set action threshold |
| Instruments | Both cards pinned with revisions; each card's "cannot support" honored explicitly |
| Dictionary controls | Version pin + absorption autopsy + one larger-dictionary splitting check |
| Statistics | Paired McNemar primary; Wilson on all rates; template-cluster caveat addressed |
| Preregistration | ≥ 3 weakening observations with numeric triggers; stopping rule |
| Scope | Negative-result statement distinguishes feature-level from behavior-level absence |

## Solution 10.3 — empirical drill (recomputation on designed numbers)

Given: b = 21 (to incorrect), c = 55 (to correct) on the 817-question
instrument; feature fires on 96 of 124 hand-labeled concept-positive items;
patching feature alone restores 31% of the clean-vs-corrupted logit gap, the
35-feature circuit 64%; SafetyBench moves −41/11,435.

**(a)** New score: 353 + (55 − 21) = **387/817 = 47.37%**; net **+34/817 =
+4.16pp**; discordant count n_d = 21 + 55 = **76**. Exact McNemar:
p = 2·P(X ≤ 21 | 76, ½) = **1.21 × 10⁻⁴** (the binomial sum
Σ_{k=0}^{21} C(76,k)/2⁷⁶, doubled; the code in the build tree computes it
directly). Significant, but two orders weaker than §4's 1.94 × 10⁻⁵ — fewer
discordant pairs buy less certainty at similar effect size.

**(b)** Firing recall: 96/124 = 0.7742. Wilson: denominator
1 + z²/124 = 1.03097; center = (0.7742 + z²/248)/1.03097 = **0.7660**;
half-width = z·√(0.7742·0.2258/124 + z²/(4·124²))/1.03097 = **0.0730**;
interval **[69.3%, 83.9%]**. Note the trap the hint flagged: n = 124 (the
hand-labeled positives), not 817 — the denominator is the labeled set,
and the interval is honest about the labeling budget's cost.

**(c)** Completeness: the single feature restores 31% of mean |TE| against
the circuit's 64% — a shortfall of **33 points of mean |TE|**, and 36% of
the total effect remains unexplained even with the circuit. The feature
carries 31/64 = **48.4%** of the circuit's restored effect — roughly half:
"a major channel, jointly with others," never "the channel."

**(d)** SafetyBench side effect: −41/11,435 = **−0.359pp**. Materiality has
two honest readings, and the report must carry both: (1) by magnitude, the
collateral is an order of magnitude smaller than the +4.16pp target effect
(ratio 1:11.6); (2) by signal, at n = 11,435 the sampling yardstick
(√(0.25/11,435) ≈ 0.47pp) is the same order as 0.36pp — whether −41 is
noise depends on the *discordant split*, which the drill (correctly) does not
give you. The disciplined sentence: "−0.36pp net; significance undecidable
without flip counts; treated as material until the paired counts say
otherwise" — the conservative reading a capability ledger demands.

**(e)** Two sentences, verbatim gradeable: "The before/after Wilson intervals
are computed on independent-sample assumptions — their overlap says nothing
about the *paired* differences, which are the actual data." "The discordant
pairs concentrate the evidence: 55 vs 21 is a 2.6:1 imbalance impossible
under the null at these counts (p = 1.2 × 10⁻⁴), even though the marginal
intervals overlap by 6+ points."

### Common wrong answers — 10.3

- (a) with b and c swapped (21 to correct): the net flips sign; reading the
  drill's own sentence ("flips 55 to correct") is the test.
- (b) with n = 817: the recall denominator is the labeled set (124), the
  hint's entire point.
- (d) declared "immaterial" by magnitude alone: the paired counts are
  missing on purpose — noticing that is the answer.

### Grading rubric (assessor) — 10.3

| Criterion | Pass requires |
|---|---|
| (a) | 387/817, +4.16pp, n_d = 76, p = 1.21 × 10⁻⁴ (binomial sum shown or coded) |
| (b) | [69.3, 83.9] with center 0.766 and half-width 0.073 shown, n = 124 |
| (c) | 33-point shortfall; 48.4% of circuit's effect; 36% unexplained |
| (d) | −0.359pp; both readings (magnitude vs. paired-count dependence) present |
| (e) | Independent-vs-paired distinction in ≤ 2 sentences, both technically correct |

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **CS 2881**, [lecture-10-mechanistic-interpretability](../../courses/boaz-barak-cs2881/lecture-10-mechanistic-interpretability.md) — watch before working the SAE evaluation exercises.
