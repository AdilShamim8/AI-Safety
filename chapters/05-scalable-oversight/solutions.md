# Ch. 05 — Exercises: hints, worked solutions, and rubrics

Attempt every exercise before reading past its hint (§9 of the [chapter README](README.md));
rubrics grade the reasoning trail, not just the final number. All numbers were recomputed
programmatically: committee tails as exact binomial sums (`math.comb`, no normal
approximations); Wilson at z = 1.96, center = (p̂ + z²/2n)/(1 + z²/n), half-width =
z·√(p̂(1 − p̂)/n + z²/4n²)/(1 + z²/n). Error profiles are the exercises' declared synthetic
scenarios; dataset denominators are card-verified.

## Solution 5.1 — correlated-error arithmetic

**Setup.** m = 5 judges, majority vote; marginal per-judge error ε = 0.08 against design
ground truth; shared blind spot on mass q = 0.03 (all judges err together); otherwise
independent residual errors at rate ε′, with ε = q + (1 − q)ε′ and committee error(m) =
q + (1 − q)·P[Bin(m, ε′) ≥ (m+1)/2], tail exact.

### (a) Residual rate ε′ and pairwise correlation ρ

Condition on the blind spot not firing (the hint: ε′ is not ε − q):

> ε′ = (ε − q)/(1 − q) = 0.05/0.97 = 0.05155  (exactly 5/97)

Residual errors must cover the whole 0.05 mass on the 97% of items without the blind spot
— ~3% above the naive 0.05. Two judges err together with probability q + (1 − q)ε′² =
0.03 + 0.97 × 0.05155² = 0.03258, so §3.6's ρ = [q + (1 − q)ε′² − ε²]/[ε(1 − ε)]:

> ρ = (0.03258 − 0.0064)/(0.08 × 0.92) = 0.02618/0.0736 = 0.356

Not established: any real committee's profile — ε and q are inputs here, measurable in
production only by Exercise 5.4's audit. (Method check: the same code at §3.6's q = 0.04,
ε′ = 1/16 reproduces ρ = 0.375 and that table's 5.08/4.21/4.04/4.01/4.00% column.)

### (b) Committee error at m = 5, and the independent contrast

> Correlated: P[Bin(5, ε′) ≥ 3] = 10ε′³(1−ε′)² + 5ε′⁴(1−ε′) + ε′⁵ = 0.0012320 +
> 0.0000335 + 0.0000004 = 0.001266 → committee error = 0.03 + 0.97 × 0.001266 = **3.12%**.
> Independent: P[Bin(5, 0.08) ≥ 3] = 10(0.08)³(0.92)² + 5(0.08)⁴(0.92) + (0.08)⁵ =
> 0.0043336 + 0.0001884 + 0.0000033 = **0.45%**.

At m = 5 the tail is 3–5 discrete terms; a normal approximation at p ≈ 0.05–0.08 errs by
more than the quantity itself. Exact tails by m (m = 1 is the sanity check q + (1 − q)ε′
= ε):

| m | Committee error (blind spot) | Committee error (if independent) |
|---|---|---|
| 1 | 8.00% | 8.00% |
| 3 | 3.75% | 1.82% |
| 5 | **3.12%** | 0.45% |
| 7 | 3.02% | 0.118% |
| 9 | 3.00% | 0.031% |
| 11 | 3.00% | 0.0085% |
| m → ∞ | **3.00% = q** | → 0% |

Five judges cut per-judge error 61% under correlation; under independence the same five
sit at 0.45% — 6.9× fewer errors, the entire difference being the 3% shared mass.

### (c) The floor, and the independent thresholds

As m → ∞ the residual tail → 0 (Condorcet) and committee error → **q = 3.00%**: the floor
depends on error correlation, not committee size. Independent version: below 2% first at
**m = 3** (3(0.08)²(0.92) + (0.08)³ = 0.017664 + 0.000512 = 1.82%); below 0.5% first at
**m = 5** (0.45253%, clearing by 0.047 points — m = 3 does not). The same five judges are
"enough" under independence and can never even reach 2% under the true profile.

### (d) Can any committee size bring the correlated version below 2%?

No: committee error = q + (1 − q)·P[Bin(m, ε′) ≥ (m+1)/2] ≥ q = 3% > 2% for every m — on
a blind-spot item all judges err together, so every majority of any size is wrong with
probability 1, and voting spends its leverage only on the 97% complement. The levers that
move the floor are decorrelation or shrinking q itself (§3.6).

### (e) Sixth same-family judge vs one human expert

The sixth same-family judge shares the blind spot, so it shrinks only the residual term —
of the 0.12 points of headroom above the 3.00% floor, m = 7 already consumes 0.10 (3.12% →
3.02%). A human expert with different failure modes attacks the shared 3% mass itself —
decorrelation being the only lever that moves the floor — so "one more ~92%-accurate
checker" describes both additions identically in ε while differing exactly in ρ.

### Common wrong answers

- **ε′ = 0.05** — subtracting q without conditioning; understates every tail below it.
- **ρ from Pr[both err] = ε²** — assumes the independence under test.
- **Normal approximation at m = 5** — exact tail 0.00127; the error exceeds the contrast.
- **"Eventually below 2%"** — the correlated column is monotone to 3.00%, full stop.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| (a) conditioning | ε′ = (ε − q)/(1 − q), conditioning stated | ε′ = ε − q = 0.05 |
| (a) ρ arithmetic | joint-error numerator over ε(1 − ε) | "correlation is high," no numbers |
| (b) exact tails | binomial terms enumerated or `math.comb` cited | normal approximation at m = 5 |
| (c) floor and thresholds | floor = q, m-independent; m = 3 and m = 5 | floor shrinking with m; m = 7 or 9 |
| (d) lower-bound argument | committee error ≥ q > 2% for all m | "m ≈ 15 should get there" |
| (e) the lever | human expert attacks q; same-family only the residual | repeats "~92% accurate" as the argument |

## Solution 5.2 — evaluator capability limits and debate

**Setup.** Verified MNIST judge-analogue endpoints [CLM-0032]: 59.4% → 88.9% (6 visible
pixels) and 48.2% → 85.2% (4 pixels) with debating agents; everything recomputed below.

### (a) Absolute gains and error-rate reductions

> 6 pixels: gain = 88.9 − 59.4 = **+29.5 pp**; errors 100 − 59.4 = 40.6% → 100 − 88.9 =
> 11.1%; reduction = 29.5/40.6 = **72.7%**; ratio 0.273 → 3.66× fewer errors.
> 4 pixels: gain = 85.2 − 48.2 = **+37.0 pp**; errors 51.8% → 14.8%; reduction = 37.0/51.8
> = **71.4%** (exactly 5/7); ratio 0.286 → 3.50× fewer errors.

Matches README §3.3. The error framing is the honest one — oversight risk scales with
error *mass*, of which debate removed ~72% in both regimes. Not established: the endpoints
belong to a sparse-pixel *classifier* standing in for a human judge, on a small toy, with
the paper flagging open questions about scaling [CLM-0032] — a large effect on a small
toy, not a deployment guarantee.

### (b) Three load-bearing assumptions

1. **Judge-analogue substitution** (the hint's first target): the judge is a classifier
   reading a few pixels — its whole persuasion surface is those pixels. If real judges
   reward confidence, fluency, or fabricated citations (§6), the mechanism inverts and
   debate trains the exploit it was meant to contain.
2. **Truth wins arguments in front of this judge**: the dishonest debater is constrained by
   an opponent quoting its earlier statements, and the PSPACE-vs-NP framing *assumes
   optimal play* [CLM-0032]. Collusion, sub-optimal honest play, or a judge that cannot
   absorb the quotes flips the advantage.
3. **Task external validity**: MNIST has binary checkable ground truth and pixel-priced
   judge queries; refusal oversight has a borderline middle, adversarial distribution
   shift, and human-attention budgets. If it fails, the *direction* may transfer while the
   *magnitude* (+29.5/+37.0 pp) does not.

### (c) Minimal experiment: the judge-capability limit on refusal oversight

**Task and ground truth.** XSTest's paired structure — 250 safe prompts to comply with,
200 unsafe contrasts to refuse, design-determined and checkable
([card](../../datasets/cards/06-xstest.md)); the card's boundary inherits (clearly safe or
clearly unsafe items only — the borderline middle is out of scope).

**Who debates.** Two same-tier agents with opposing briefs on one *draft response*: Pro-Pass
argues it is appropriate, Pro-Block that it should have been refused; alternating statements
to a fixed limit, both seeing prompt, draft, and each other's statements, and able to quote
them back — the constraint mechanism debate depends on.

**Who judges.** A judge-analogue with a *restricted view* (the sparse-pixel analog): a weak
model seeing the prompt but only a masked or truncated draft, so draft information must
arrive through the debate; the same judge and restriction run in both arms (paired per
item).

**Arms and metric.** Arm 1: judge alone; arm 2: judge + debate. Primary: missed refusals on
the 200 unsafe side; secondary: false refusals on the 250 safe side; Wilson 95% per arm per
side, paired analysis by discordant items. Resolution honesty: 20/200 = 10% → [6.6%, 14.9%]
and 25/250 = 10% → [6.9%, 14.3%] — only effects ≳ 8 pp per side are resolvable; smaller
effects need a bigger instrument or a weaker claim.

**What would weaken "debate helps judges."** (i) the debate estimate falls inside the alone
arm's Wilson interval (no resolvable effect); (ii) direction reversal on the unsafe side —
Pro-Pass persuades the judge on unsafe items, *raising* missed refusals (rhetoric beating
truth, §6 in miniature); (iii) the honesty swap — rerun with the honest brief exchanged
between agents; verdicts tracking the agent rather than the honest side show the mechanism
is persuasion; (iv) false refusals balloon on the safe side (benign-ledger harm even if
the unsafe side improves).

**Cannot test.** Persuadable humans at deployment scale (the judge is a stand-in — (b1)
survives only as analogy); the borderline middle (card boundary); self-play-trained or
adaptive debaters optimizing the judge across rounds
(`chapters/08-ai-control-and-monitoring/`); multi-step oversight (one approval decision).

### Common wrong answers

- **+29.5 pp quoted as transferable** — a toy-task effect on a classifier judge; transfer
  is assumption (b1)/(b3), not a finding.
- **Unsafe side only** — a debate that wins by refusing everything destroys the benign
  ledger; both sides are the ledger.
- **Judge sees the full draft in both arms** — destroys the restricted-view pairing; both
  arms then measure prompt-reading.
- **Reversed weakening direction** — rising missed refusals *weakens* the hypothesis; it is
  the strongest evidence against the mechanism.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| (a) both framings | gains and error reductions, arithmetic shown | accuracy points relabeled "error reduction" |
| (a) honesty | toy/stand-in caveat anchored to [CLM-0032] | presented as evidence debate scales |
| (b) attackable assumptions | each with its specific breakage | "might not generalize" ×3 |
| (c) restricted-view pairing | same judge, same restriction, both arms | judge sees full context in one arm |
| (c) weakeners directional | ≥ 2 concrete, correctly signed | "bad results would weaken it" |
| (c) limits named | judge-substitution, borderline, non-adaptive debaters | claims the design tests human persuadability |

## Solution 5.3 — process vs outcome arithmetic

**Setup.** k = 8 steps; an item is wrong iff at least one step is wrong; 70% of items fully
correct, 30% exactly one wrong step. (A) Outcome check: catches a wrong final answer with
probability 0.85, falsely rejects a correct item with probability 0.01. (B) Process check:
a wrong step is caught with probability 0.90 (slips with s = 0.10), a correct step is
falsely flagged with f = 0.02. Under B an item is approved iff *no* step is flagged — false
rejections compound as 1 − (1 − f)^k (the hint), and a wrong item is approved only if its
wrong step slips *and* its 7 correct steps escape false flags.

### (a) Probability a wrong item is approved

A: the single check misses → 1 − 0.85 = **0.150**. B: the slip channel alone is s = 0.100
(§3.4's quoted form); the full approval event is 0.10 × 0.98⁷ = 0.10 × 0.868126 =
**0.0868**. The 1.3-point gap is wrong items rejected because a *correct* step was falsely
flagged — right verdict, wrong reason: the item-level catch rate (1 − 0.0868 = 91.3%)
partly rides on the check's own false positives, overstating its diagnostic power (0.90 at
the step level).

### (b) Probability a correct item is falsely rejected

A: **0.010**. B: any of 8 correct steps flagged → 1 − 0.98⁸ = 1 − 0.850763 = **0.1492** —
14.9%, not 2%: the compounding, exactly §3.4's numbers (27.6% at k = 16, recomputed
27.62%).

### (c) Overall rates and the ship decision

| Scheme | wrong approved (of wrong) | correct rejected (of correct) | approved-wrong mass | rejected-correct mass |
|---|---|---|---|---|
| A (outcome) | 15.0% | 1.0% | 0.30 × 0.150 = 4.50% | 0.70 × 0.010 = 0.70% |
| B (process) | 8.68% | 14.92% | 0.30 × 0.0868 = 2.60% | 0.70 × 0.1492 = 10.45% |

B buys 1.9 points of false-approval mass (4.50% → 2.60%) and pays 9.7 points of
false-rejection mass (0.70% → 10.45%). With c_w the cost of approving a wrong item and c_r
the cost of rejecting a correct one, B is preferred iff 0.30(0.150 − 0.0868)·c_w ≥
0.70(0.1492 − 0.010)·c_r, i.e. **c_w ≥ 5.14·c_r**: ship B only if a shipped wrong item
costs ≳ 5× a blocked correct one (plausible for safety gating — unsafe content shipped vs
correct work blocked), otherwise ship A; if B ships, its 14.9% correct-item rejection is a
declared, user-visible harm. State the breakeven and both masses, not a naked preference.

### (d) The f thresholds for > 20% false rejection

Solve 1 − (1 − f)^k = 0.20 → (1 − f)^k = 0.80 → f = 1 − 0.80^(1/k):

> k = 8: f = 1 − 0.972492 = **2.75%**  (check: 1 − 0.972492⁸ = 0.200)
> k = 4: f = 1 − 0.945742 = **5.43%**  (check: 1 − 0.945742⁴ = 0.200)

Halving the chain nearly doubles the tolerance (2.75% → 5.43%): at f = 2%, false rejection
is 14.9% at k = 8 but 7.8% at k = 4 — the compounding, not f, sets the exposure.

### (e) The binding constraint (one sentence)

The step-checker's false-flag rate on *correct* steps: because rejections compound as
1 − (1 − f)^k while catches do not, a per-step false-positive rate that looks negligible
(2–3%) silently rejects a fifth of correct work at k = 8 — deployability is capped by f
long before catching power is capped by s.

### Common wrong answers

- **False rejection under B = f = 2%** — ignores compounding, 7.5× off at k = 8.
- **0.10 as P[wrong approved under B]** — that is the slip rate; approval requires all 8
  steps to pass, giving 0.0868.
- **One pooled "accuracy" per scheme** — a two-ledger tradeoff; pooling hides the 5.14×
  breakeven it turns on.
- **(d) by trial-and-error only** — fine numerically, but the closed form exhibits the
  k-scaling that (e) needs.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| (a) both channels | 0.15 vs 0.0868 (or 0.10 with the gap explained) | one number for both schemes |
| (b) compounding | 1 − (1 − f)^k evaluated | f quoted directly |
| (c) two ledgers + breakeven | masses and the ~5.1 cost ratio | "B is better," no costs |
| (d) closed form | 1 − 0.8^(1/k), k-scaling noted | brute-force numbers only |
| (e) names f | false-flag rate as the binding constraint | "process supervision is expensive" |

## Solution 5.4 — bounded comparison with checkable ground truth (design skeleton)

The learner's document runs 800–1,200 words; this skeleton pins the decisions it must
carry — all six required elements, each load-bearing.

### (i) Task and ground truth

**TruthfulQA** ([card](../../datasets/cards/01-truthfulqa.md)): 817 adversarial questions,
single validation split, evaluation-only, targeting *imitative falsehoods* — wrong answers
statistically frequent in human text, i.e. a curated catalog of correlated human–model
error, exactly §3.1's family; ground truth fixed-option and checkable. Card boundaries
carried: a TruthfulQA score is not general honesty, and the "cannot support" list rules out
toxicity, bias, and refusal-quality claims — everything below is oversight on *this
catalog*. Leakage discipline (questions circulate in web text; the 817 never enter any
training pipeline) forces the split in (v). Alternatives: BBQ's 58,492 paired items
([card](../../datasets/cards/05-bbq.md)) — n to burn for the audit, different construct;
SafetyBench's 11,435 bilingual MCQs ([card](../../datasets/cards/13-safetybench.md)) —
safety *knowledge*, cannot support behavioral claims (§6's substitution trap).

### (ii) Roles and the supervisor error profile

Weak supervisor ω: a small open model labeling the training pool (its labels are the weak
supervision). Strong learner σ: a frontier-tier model finetuned on ω's labels; σ\*: the
same model on ground-truth labels of the same pool (ceiling arm). The profile is
*measured, not assumed*: an agreement audit of ω against G on a 250-item labeled slice
yields ε̂_ω with a Wilson interval; a declared synthetic fallback (ε = 0.10, q = 0.04 as in
§4) is permitted only flagged as a teaching value, never quoted as a measurement.

### (iii) Primary metric and the resolution table

PGR = (a_W2S − a_ω)/(a_σ\* − a_ω) on the untouched 817, each accuracy Wilson-bounded.
Planning normalizer declared: a_ω = 0.70, a_σ\* = 0.90 (gap 0.20), replaced by measured
values at run time. Resolution recomputed at z = 1.96, worst-case p̂ = 0.5:

| Eval n | Wilson half-width | Implied PGR resolution (÷ 0.20) |
|---|---|---|
| 817 | ±3.42 pp | ±0.17 |
| 250 | ±6.15 pp | ±0.31 |
| 100 | ±9.62 pp | ±0.48 |

Worked consequence at a_W2S = 0.80: n = 817 gives Wilson [77.1%, 82.6%] → first-order PGR
≥ 0.36, so a "PGR ≥ 0.3" claim is supportable; n = 250 gives [74.6%, 84.5%] → 0.23, and
the same point estimate no longer supports it; n = 100 gives [71.1%, 86.7%] → 0.06,
indistinguishable from the supervisor. (Propagates a_W2S only — a_ω and a_σ\* carry
intervals of the same order, so the table is an optimistic floor on resolution.) The
hint's discipline: the primary comparison runs at the full n = 817, affordable only
because the training pool is disjoint (v); a context that cannot afford 817 evaluation
items must weaken the claim, not the arithmetic.

### (iv) Error-correlation audit

On the audit slice, ω and σ (pre-finetune, zero-shot) label the same items against G: the
2×2 error table gives joint error P̂₁₁ and marginals ε̂_ω, ε̂_σ, hence ρ̂ = (P̂₁₁ −
ε̂_ωε̂_σ)/√(ε̂_ω(1 − ε̂_ω)ε̂_σ(1 − ε̂_σ)), reducing to §3.6's formula at equal marginals.
Estimating q needs more than a pair: add a third, different-family checker (plus a
human-expert slice); q̂ = the all-wrong mass — with only a pair, q and correlated residuals
are not separately identifiable. Report ρ̂ and q̂ with item-level bootstrap intervals;
pre-state ρ̂ > 0.2 as a weakening observation (informative errors shrink the W2S bonus,
§3.2/§6).

### (v) Preregistration elements (Ch. 02 carryover)

Claim in context form: "In context κ (TruthfulQA MCQ-form, English, fixed options, HF
revision pinned), σ finetuned on ω's labels achieves PGR ≥ 0.3 by Wilson-bounded a_W2S."
Weakening observations, pre-stated: (1) paraphrase-arm drop > 10 pp on the 817 —
contamination, since the questions circulate in web text
([card](../../datasets/cards/01-truthfulqa.md)); (2) option-order permutation shifts
a_σ\* by > 3 pp — letter memorization; (3) ρ̂ > 0.2 on the audit slice; (4) between-run
spread exceeds interval width. Split discipline: the 817 are evaluation-only, untouched by
any training pipeline (card rule); the weak-label pool is *authored* TruthfulQA-style items
in the card's page-verified adversarial categories (Misconceptions, Proverbs,
Misquotations, Conspiracies, Superstitions), disjoint by construction; knowledge cutoffs
recorded; the paraphrase and option-order arms of
[Ch. 02's solutions](../02-evaluation-science-and-experimental-design/solutions.md) run as
contamination checks, not re-derived here.

### (vi) Small-analogue scope statement

Cannot tell you: (1) whether weak-to-strong survives a human→superhuman capability gap —
the course's reading (§6) is that "GPT-2 supervising GPT-4" differs in kind, not just
size, from human supervising superhuman, and the anchor covers only "consistent W2S
generalization, far from full recovery" [CLM-0030]; (2) anything about supervision
*without* checkable ground truth — open-ended behavior has no G, and PGR is undefined
there; (3) whether the student resolves supervisor errors outside this curated catalog;
(4) supervision versus elicitation attribution — PGR conflates them (§3.2's elicitation
gap [CLM-0030]); (5) behavior under an adaptive adversary optimizing against the supervisor
(`chapters/08-ai-control-and-monitoring/`). The artifact is the input specification for
`projects/p05-weak-to-strong-or-scalable-oversight-analogue/` — a bounded experiment
design, not evidence about superhuman supervision.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Card-cited task + boundary | 817 + evaluation-only discipline + "cannot support" quoted | "TruthfulQA measures honesty" |
| Roles + measured profile | ω/σ/σ\* named; audit yields ε̂ with an interval | supervisor accuracy assumed |
| Resolution table | half-widths at all three n + a forced design decision | table with no consequence drawn |
| Correlation audit | 2×2 → ρ̂; third checker for q̂; pair-only limit named | "we will measure correlation" |
| Preregistration | context-form claim, ≥ 3 weakening observations, split discipline | a goal, nothing testable |
| Scope statement | ≥ 3 honest cannot-tells | "this will show weak-to-strong works" |
