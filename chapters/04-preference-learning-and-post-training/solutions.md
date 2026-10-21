# Ch. 04 — Exercises: hints, worked solutions, and rubrics

Attempt every exercise before reading past its hint. Rubrics grade the reasoning trail, not just the final number — an unsupported right answer scores below a well-argued approximate one. Every figure below was recomputed with the repository Python (σ(z) = 1/(1+e^{−z}); Wilson z = 1.96, z² = 3.8416), inputs shown; where the README rounds, the recomputation says so. Audit outcome counts follow §4.2's convention — illustrative first-run values on card-verified denominators, because the cards publish no agreement statistics [cards/07; cards/08]. Notation is the README's table.

## Solution 4.1 — derivation and counterexample (analysis)

### (a)(i) Step 1 → 2 in full: where the partition function comes from

Per prompt x, both terms of the §3.4 objective are expectations under y ∼ π(·|x), so linearity merges them. Divide by −β (β > 0: maximizing J is minimizing −J/β) and expand the log of a quotient (log a − log b):

```text
−J(π)/β = E_π[ log(π(y|x)/π_ref(y|x)) − r_φ(x,y)/β ]
        = E_π[ log( π(y|x) / (π_ref(y|x) · e^{r_φ(x,y)/β}) ) ]
```

Define Z(x) = Σ_y π_ref(y|x)·e^{r_φ(x,y)/β}. Z(x) is positive, finite, and — the load-bearing fact — **constant in y**: it sums over every response identically, so it does not move with the expectation's variable. Hence π_ref(y|x)·e^{r/β} = Z(x)·π*(y|x), where π*(y|x) := π_ref(y|x)·e^{r/β}/Z(x) is a genuine distribution — non-negative, and summing to 1 *because* Z is its normalizer. Substitute, split the log of a quotient once more, and use the expectation of a constant:

```text
E_π[ log(π/(Z(x)·π*)) ] = E_π[log(π/π*)] − log Z(x) = KL(π‖π*) − log Z(x)
J(π)   = −β · ( KL(π‖π*) + log Z(x) )
```

The middle equality is the hint's point (log Z(x) is constant in y, whatever π is); the last is the definition of KL between conditionals. Full credit also needs both remarks: the identity holds for *every* distribution π (no parametric assumption was made), and the step dies if r stops being exogenous to the policy — then Z stops being constant in y and the closed form collapses.

### (a)(ii) The DPO gradient, derived and interpreted

Per pair, L = −ln σ(ẑ) with ẑ = β·(Δ_w − Δ_l), Δ_w = log π_θ(y_w|x) − log π_ref(y_w|x), Δ_l likewise. Chain rule with σ'(ẑ) = σ(ẑ)(1−σ(ẑ)) = σ(ẑ)·σ(−ẑ) (identity verified numerically), and π_ref frozen — no θ in it, so ∇_θΔ_w = ∇_θ log π_θ(y_w|x):

```text
∇_θ L = −(1/σ(ẑ))·σ(ẑ)σ(−ẑ)·∇_θẑ = −σ(−ẑ)·β·[∇_θ log π_θ(y_w|x) − ∇_θ log π_θ(y_l|x)]
```

**Interpreting each factor.** σ(−ẑ) ∈ (0,1) is the per-pair weight: maximal in the limit ẑ → −∞ — the policy currently prefers the *rejected* response with margin — vanishing as ẑ → +∞ (pair already satisfied), exactly 1/2 at ẑ = 0; it is the logistic analogue of a per-example advantage weight (no error, no update), and it never reaches 0 at finite ẑ. β multiplies twice: inside ẑ it sets how fast the weight saturates as margins grow, outside it scales the update magnitude outright — doubling β does not double the gradient (the same margins give factors 0.045/0.055/0.050 at β = 0.1 but 0.119/0.881/0.500 at β = 1; Solution 4.3(b)). The bracket is the BT gradient with the reward model replaced by the policy's own log-ratios — raise the chosen response's log-probability, lower the rejected one's, per pair [CLM-0027]: "your language model is secretly a reward model" [CLM-0027].

### Recomputation — §3.2 calibration, §4.1 state table, the toy's checks

σ(z) = 1/(1+e^{−z}); pair loss = −ln σ(gap). Gap 0.8: σ = 0.6900, loss = **0.3711**; gap 1.6: σ = 0.8320, loss = **0.1839** — the README's 0.371 and 0.184 reproduce exactly. Doubling the gap 0.8 → 1.6 halves the loss; doubling again to 3.2 gives 0.0400 — the tail is asymptotically loss ≈ e^{−gap} (0.4493 / 0.2019 / 0.0408 at the three gaps), so each extra nat of gap still buys ≈ a factor-e reduction. §3.2's "pushes gaps to grow, then saturates" is a pressure that decays exponentially but never switches off — §6.1's silent failure has nonzero gradient at every finite gap.

State table (β = 0.1), every cell reproduced — ẑ = β(Δ_w−Δ_l), σ(ẑ), loss = −ln σ(ẑ), factor = β·σ(−ẑ): rows 1 and 4 → (+0.05, 0.5125, 0.6685, 0.0488); row 2 → (−0.10, 0.4750, 0.7444, 0.0525); row 3 → (+0.30, 0.5744, 0.5544, 0.0426). Row 2 — the only wrong-side state — carries the largest factor, exactly as (a)(ii) predicts.

Toy (π_ref uniform 0.25 over Y = {y1..y4}, r = [1, 0, −1, 2]):

- **β = 1.** e^{r/β} = [2.71828, 1.00000, 0.36788, 7.38906]; Z = 2.86880; π* = [0.23688, 0.08714, 0.03206, 0.64391]; E_π*[r] = 1.49265; KL(π*‖π_ref) = 0.43876 nats. Every §4.1 figure reproduces.
- **Check (a), +5 to every reward.** Numerators and Z all scale by e^5 = 148.413: Z 2.8688 → 425.7683, and π* is identical to five decimals. Offsets never matter; only differences do.
- **Check (b), implicit rewards.** β·[log(π*(y_w)/π_ref) − log(π*(y_l)/π_ref)] = 1.000000 on (y1,y2) and (y4,y1); 3.000000 on (y4,y3); 2.000000 on (y1,y3) — the true reward gaps exactly; the β·log Z(x) term cancels in every difference, as Step 4 claims.
- **Check (c), β = 0.1.** e^{10r} = [22026.47, 1.00000, 0.00005, 4.85×10⁸]; π* = [0.00005, 0.00000, 0.00000, 0.99995]; KL = 1.38579 nats. Honesty note: the point mass on y4 would attain exactly ln 4 = 1.38629, so the README's "1.38579 = ln 4" is exact only in the β → 0 limit (5.0×10⁻⁴ nats short at β = 0.1). The claim it carries is untouched — a nearly collapsed policy sits ~1.39 nats from a uniform reference: the leash reads modest while the behavior change is total (§3.4's ceiling).

### (b) The 3-cycle floor is exactly 3·ln 2

Let ℓ(u) = −ln σ(u) = ln(1+e^{−u}). The cycle A ≻ B, B ≻ C, C ≻ A scores L(r_A, r_B, r_C) = ℓ(r_A−r_B) + ℓ(r_B−r_C) + ℓ(r_C−r_A).

**Convexity.** ℓ''(u) = σ(u)(1−σ(u)) > 0 for all finite u, so ℓ is strictly convex; each term composes ℓ with an affine map of the reward vector, and a sum of convex functions is convex. For a convex differentiable function, every stationary point is a global minimum.

**Stationarity.** With ℓ'(u) = −σ(−u) (finite-difference-verified), the partials are

```text
∂L/∂r_A = σ(r_A−r_C) − σ(r_B−r_A)    ∂L/∂r_B = σ(r_B−r_A) − σ(r_C−r_B)    ∂L/∂r_C = σ(r_C−r_B) − σ(r_A−r_C)
```

Setting all three to zero and using that σ is strictly increasing — hence injective — gives r_A−r_C = r_B−r_A = r_C−r_B =: m. Sum the three equal quantities: (r_A−r_C) + (r_B−r_A) + (r_C−r_B) ≡ 0 (telescoping), so 3m = 0 and m = 0. Every stationary point has all three reward differences zero, where L = 3·ℓ(0) = **3·ln 2 ≈ 2.079442**. By convexity that is the global minimum; the minimizer is the whole line r_A = r_B = r_C (L is shift-invariant), not a single point. ∎

**Numeric verification.** Gradient descent from 10 random starts converges to loss 2.079442 with max pairwise gap ≤ 9×10⁻¹⁶; a 0.5-step grid over [−2, 2]³ bottoms at 2.079442 at equal rewards. The best *transitive* attempt — r = (1, 0, −1), which gets two of the three pairs right with gap 1 — pays 2.753451, and every translate (2,1,0), (5,4,3) pays identically (shift-invariance again): 0.674 nats above the floor, at any offset. At the minimum the model assigns σ(0) = 0.5 to every pair — a coin flip each time. More data shrinks sampling error around this statement; it cannot move the floor, because no scalar ordering satisfies a cycle (§6.3). The failure is representational, not statistical.

### (c) Row 1 vs row 4, in five sentences

Rows 1 and 4 share (Δ_w − Δ_l) = +0.5, and every DPO quantity is a function of that difference alone — ẑ = +0.05, σ(ẑ) = 0.5125, loss 0.6685, gradient factor 0.0488, identical in both rows — so neither loss nor gradient sees the levels Δ_w and Δ_l at all. In row 1 the preferred response sits above π_ref's probability; in row 4 it sits below, and the objective cannot tell them apart. A falling DPO loss therefore certifies exactly one thing: the margins β(Δ_w−Δ_l) are growing on the training pairs. A safety reviewer must not conclude from it that preferred responses became more likely in absolute terms, that the policy stayed near π_ref, or that typical-text likelihood was preserved — row 4 shows all three can be false while the loss falls (§6.4). Those conclusions need their own measurement: per-response log-probabilities under the trained policy, reported next to the loss.

### Common wrong answers

- "Z cancels because it is small" (or "because β is small"): Z cancels because it is constant in y — the +5 check grows Z by 148× with zero effect on π*.
- Writing the gradient weight as σ(ẑ) instead of σ(−ẑ): this inverts the objective's attention — satisfied pairs get the largest updates and wrong-side pairs the smallest. Likewise differentiating through π_ref: it is frozen; ∇_θΔ_w is ∇_θ log π_θ(y_w|x) and nothing more.
- (b) by grid search alone: numerics suggest, convexity + stationarity prove — and only the proof yields "attained when all differences are zero," which is the actual claim.
- Reading (b) as a data problem ("collect more labels"), or (c) as "falling DPO loss means the good behavior got more likely": the cycle is representational (§6.3), and row 4 has margin up while the preferred response fell below reference probability.

### Grading rubric (assessor)

| Criterion | Pass | Merit | Fail signatures |
|---|---|---|---|
| Step 1→2 algebra | quotient expanded; Z's y-invariance named | both remarks: holds for every π; dies if r depends on π | "Z is small so it cancels"; no expansion shown |
| Gradient derivation | σ′ = σσ(−ẑ) shown; π_ref frozen used | β's double role articulated | weight σ(ẑ); π_ref differentiated |
| Interpretation | weight maximal as ẑ→−∞; bracket = BT shape | factor-e saturation arithmetic cited | "β is the learning rate" only |
| (b) route and result | convexity + stationarity; 3·ln 2 = 2.079442 at zero gaps | telescoping closure, shift-invariance, numeric verification, transitive-try comparison | grid search only; 2.079 without proof or meaning |
| (c) | margin-only claim + one named non-conclusion | ≥ 3 non-conclusions + the supporting measurement named | "falling loss = safer model" |
| Recomputations | state table + toy checks reproduced | 1.38579-vs-ln 4 honesty note included | numbers copied unread from README |

## Solution 4.2 — preregistered label-quality audit (worked skeleton)

A passing plan for **HH-RLHF** [cards/08], in the required sections; a second team can execute it unchanged. (A BeaverTails variant swaps in the four-configuration denominators and the CC BY-NC 4.0 line [cards/07]; the skeleton is what is graded.)

**Claim (context form).** On a pinned revision (HF snapshot hash recorded at load time [cards/08]) of the HH-RLHF train split — 161k of 169k rows; the 8.55k test split is never sampled by the audit [cards/08] — three label-quality statements, each gated by Wilson 95% bounds: (i) the order-swap inconsistency rate's upper bound is below 10%; (ii) the chosen-strictly-longer share's interval lies inside [45%, 55%]; (iii) double-annotation agreement under our written instructions has lower bound above 80%. Together these support: "single-order labels at a declared noise floor are adequate for reward-model training on this corpus." Any failure fires its pre-stated remedy, not a corpus-wide verdict.

**Instruments (pinned).** (1) *Order-swap consistency*: n = 1,000 pairs, sampled without replacement at row level; re-present each pair reversed to a different annotator in a separate session; inconsistency = the two judgments disagree (HH-RLHF is pairwise by construction, so the instrument fits natively [cards/08]). (2) *Length stratification*: the same 1,000 pairs; chosen strictly longer by character count; no new annotation. (3) *Double-annotation agreement*: n = 200 pairs re-annotated under written dimension-level instructions by annotators blind to the original label; raw agreement. Honesty boundary: the card is metadata-only on the original worker protocol [cards/08], so instrument (3) measures *our* instructions' reproducibility on this material — not the 2022 protocol's — which is why its threshold is a screening gate.

**Split/grouping.** The audit draws from the train split only, without replacement, one row per pair; the reversed presentation is a within-pair repeat *by design* — contrasted with the forward judgment, never pooled into a single rate. Overlap between instruments 1 and 3 is flagged when a pair appears in both. Declared caveat: the card records that multi-turn session structure was not verified at page level [cards/08] — if session identifiers become available, re-draw session-disjoint and say so; until then, row-level sampling is an assumption the report carries.

**Intervals and pre-stated thresholds.** Wilson 95% (z = 1.96), center and half-width reported per rate. (i) upper bound > 10% → collect both orders for all future labels and average or drop conflicted pairs, then re-audit; (ii) lower bound > 55% (or upper < 45%) → length-balance the training mix or debias the reward before RM training; (iii) upper bound < 80% → adjudication protocol and written instructions before any classifier claim.

**Power.** Wilson half-width ≤ 3pp needs n = 490 at p̂ ≈ 0.132 and n = 1,064 at worst-case p̂ = 0.5 (recomputed; §4.2's 1,068 is the Wald round-up z²·0.25/ε² = 1,067.1 — the more conservative figure, and both are stated). n = 1,000 sits at the honest edge for mid-range rates; the 200-row instrument carries ±6.2pp near p̂ = 0.71 — a screening tool only, and the claim above is worded (bounds, thresholds) to survive that width.

**Weakening observations (falsifiable, pre-stated).** (1) A fresh 1,000-pair order-swap sample returns an upper bound above 10%. (2) The length-share lower bound exceeds 55%. (3) Double-annotation upper bound falls below 80%. (4) Splitting the audit sample by corpus order (first vs second 500) yields non-overlapping intervals on any instrument — annotator-population drift between collection waves (§6.6). Each names its statistic and its trigger.

**Scope exclusions and license.** MIT license [cards/08] permits commercial downstream use — had the corpus been BeaverTails, CC BY-NC 4.0 would bar it [cards/07]. English-only; single-corpus claim with no transfer statement to other preference corpora; the unaudited ~160k rows are covered by extrapolation, reported as such; biases without instruments here (style, sycophancy toward the prompter, topic-dependent severity) are out of scope by construction — and the audit says so rather than implying cleanliness (§6.6).

**Arithmetic a second team can check against §4.2's illustrative run.** 132/1,000 → center 0.1334, half 0.0210, [11.2%, 15.4%]; 614/1,000 → center 0.6136, half 0.0301, [58.3%, 64.4%], exact binomial tail P(X ≥ 614 | n = 1,000, p = 0.5) = 2.8×10⁻¹³ (z = 7.21); 142/200 → center 0.7060, half 0.0624, [64.4%, 76.8%]. All reproduce §4.2; the counts themselves are illustrative first-run values — the cards publish no agreement statistics [cards/07; cards/08].

### Common wrong answers

- Power reported only at p̂ = 0.5 (the worst case, not the operating point); re-annotation framed as reproducing the *original* protocol (the card is metadata-only on it [cards/08] — you cannot re-run what was never published).
- Thresholds applied to point estimates ("13.2% > 10%, trigger") instead of interval bounds; the audit presented as certifying all 161k rows (it certifies the sample; extrapolation is declared).
- A BeaverTails plan without the CC BY-NC 4.0 exclusion, or one that mixes the 330k and 30k split families [cards/07].

### Grading rubric (assessor)

| Criterion | Pass | Merit | Fail signatures |
|---|---|---|---|
| Claim in context form | corpus, pinned revision, three rates with bound-based thresholds | remedy per failure stated, not just pass/fail | "check that the labels are good" |
| Instruments pinned | card denominators (161k/8.55k), n per instrument | instrument-3 boundary (our instructions) named | denominators from memory; "a sample" |
| Split/grouping | within-pair repeat by design; test split untouched | session-structure caveat declared | forward+reversed pooled into one rate |
| Thresholds and power | bound-triggered remedies; operating-point and worst-case n | Wald-vs-Wilson n difference noted | post-hoc thresholds; single n with no p̂ |
| Weakening observations | ≥ 3, named statistics, falsifiable | each paired with its trigger | vague "if results look bad" |
| License and scope | MIT vs CC BY-NC 4.0 named; extrapolation declared | uninstrumented biases listed as out of scope | license ignored |

## Solution 4.3 — numeric drill (full arithmetic)

Method throughout: σ(z) = 1/(1+e^{−z}); BT loss = −ln σ(gap); DPO loss = −ln σ(ẑ), ẑ = β(Δ_w−Δ_l), gradient factor β·σ(−ẑ); Wilson center = (p̂+z²/2n)/(1+z²/n), half-width = z·√(p̂(1−p̂)/n + z²/4n²)/(1+z²/n).

### (a) BT loss at gap 1.2, and at a tie

- Gap 1.2: σ(1.2) = 0.768525 → loss = −ln(0.768525) = **0.263282**.
- Tie (gap 0): σ(0) = 0.5 → loss = ln 2 = **0.693147**. A tie is not free — it is the coin-flip point, the same per-pair value the 3-cycle of Solution 4.1(b) is stuck at on every pair.

### (b) DPO loss and gradient factor, β = 0.1

| (Δ_w, Δ_l) | ẑ = β(Δ_w−Δ_l) | σ(ẑ) | loss −ln σ(ẑ) | factor β·σ(−ẑ) |
|---|---|---|---|---|
| (3.0, 1.0) | +0.20 | 0.5498 | 0.5981 | 0.0450 |
| (−0.5, 1.5) | −0.20 | 0.4502 | 0.7981 | 0.0550 |
| (0, 0) | 0 | 0.5000 | 0.6931 | 0.0500 |

The wrong-side state (−0.5, 1.5) — the model prefers the rejected response — carries both the largest loss and the largest gradient factor; the well-separated state carries the smallest: the objective's attention concentrates on its current errors. All three factors sit in the narrow band [0.045, 0.055] because β = 0.1 compresses ẑ — small β ⇒ slow saturation ⇒ near-uniform weighting. At β = 1 the same margins give factors 0.119 / 0.881 / 0.500: β sets both the scale and the discriminativeness of the weight (the double role of 4.1(a)(ii)).

### (c) Wilson 95% intervals, center and half-width visible

**87/1,000 inconsistent under order swap** (p̂ = 0.087): z²/2n = 0.0019208; z²/n = 0.0038416; center = (0.087 + 0.0019208)/1.0038416 = **0.0886**; p̂(1−p̂)/n = 0.087·0.913/1000 = 7.9431×10⁻⁵; z²/4n² = 9.604×10⁻⁷; √(8.0391×10⁻⁵) = 0.008966; ×1.96 = 0.017574; ÷1.0038416 → half = **0.0175**. **Wilson 95% = [7.1%, 10.6%].**

**165/200 re-annotation agreement** (p̂ = 0.825): z²/2n = 0.009604; z²/n = 0.019208; center = (0.825 + 0.009604)/1.019208 = **0.8189**; p̂(1−p̂)/n = 0.144375/200 = 7.21875×10⁻⁴; z²/4n² = 2.401×10⁻⁵; √(7.45885×10⁻⁴) = 0.027311; ×1.96 = 0.053529; ÷1.019208 → half = **0.0525**. **Wilson 95% = [76.6%, 87.1%].**

### (d) Do the intervals support the claims?

- **"Inconsistency below 10%": not supported.** The point estimate 8.7% is below 10%, but the upper bound is 10.6% — the data are consistent with a true rate above 10%. Bound-gated claims fail on bounds (Ch. 02's discipline); under Solution 4.2's pre-stated rule (upper bound > 10% → collect both orders), the remedy fires. Resolving the claim needs the upper bound below 10% — first reached around n ≈ 2,050–3,000 at this rate (recomputed: n = 2,050 → [7.5%, 10.0%]; n = 3,000 → [7.7%, 9.8%]).
- **"Agreement at least 80%": not supported.** The lower bound is 76.6% < 80%; 165/200 is consistent with true agreement anywhere in [76.6%, 87.1%]. The screening gate (upper bound < 80% → adjudication) does *not* fire — the interval straddles 80% — so the honest verdict is "unresolved," not "passed." Both verdicts share one lesson: *not supported is not false* — each interval also contains rates that would satisfy its claim; the sample simply cannot decide.

### (e) The §4.1 toy at β = 0.5

e^{r/β} = e^{2r} = [7.38906, 1.00000, 0.13534, 54.59815]; Z = 0.25 × 63.12254 = 15.78064; **π* = [0.11706, 0.01584, 0.00214, 0.86495]**; **E_π*[r] = 1.84482**; **KL(π*‖π_ref) = 0.93087 nats**. Against β = 1 (π* = [0.23688, 0.08714, 0.03206, 0.64391]; E[r] = 1.49265; KL = 0.43876): halving β doubles the exponent, so the same rewards buy a visibly sharper policy — y4's mass 0.644 → 0.865, E[r] 1.493 → 1.845 (rising toward its supremum 2; at β = 0.1 it is 1.99995), and KL more than doubles, 0.439 → 0.931, still under the ln 4 ceiling. Unchanged: the response ordering (β is a temperature on e^{r/β} — it sharpens, never re-ranks), offset-invariance, and the exactness of implicit reward differences (still 1.000000 on (y1,y2) at β = 0.5). β is a sharpness dial on one ordering, not a preference editor.

### Common wrong answers

- (a) tie reported as loss 0 ("no preference, no penalty"): the tie is the coin-flip point — ln 2, the per-pair floor the 3-cycle pays everywhere.
- (b) factor computed with σ(ẑ) — the satisfied state would get the *largest* factor, the objective's attention inverted; or β forgotten inside ẑ (ẑ = 2.0 → loss 0.127), which changes every downstream number.
- (c) silently substituting Wald: at p̂ = 0.087 it is passable, but the drill specifies Wilson, and Wald collapses near p̂ = 0 or 1 (Ch. 02 Solution 1.3(e)).
- (d) "8.7% < 10%, so supported": point-estimate gating — the exact failure mode Ch. 02's rubrics flag.
- (e) reporting π* at β = 0.5 with the β = 1 KL, or claiming β re-orders the policy.

### Grading rubric (assessor)

| Criterion | Pass | Merit | Fail signatures |
|---|---|---|---|
| Arithmetic visible | σ, ẑ, center, half-width all shown | intermediate radicals carried | end-points only, unverifiable |
| (a) tie | ln 2 with the coin-flip reading | tied back to the 3-cycle floor | 0 |
| (b) factor | β·σ(−ẑ); wrong-side state largest | β's double role shown via β = 1 | σ(ẑ); satisfied state largest |
| (c) Wilson mechanics | center + half-width to 4 dp | inputs listed before the arithmetic | Wald silently substituted |
| (d) verdicts | bound-gated, both directions | "not supported ≠ false" nuance; resolution n estimated | point-estimate gating |
| (e) comparison | three changes named (π*, E[r], KL) | two invariances named (ordering, implicit gaps) | π* only, no contrast |

## Solution 4.4 — RLAIF evidence critique (critical)

### (a) What [CLM-0028] establishes — and what deployment still needs

**Established** (abstract-level, per the register): the two-phase CAI pipeline runs — supervised training on model-generated self-critiques and revisions against a principles list, then RL from AI Feedback (a preference model trained on the model's own judgments of its sampled pairs) — and it produced an assistant that engages harmful queries by explaining its objections rather than evading them, with *no human labels identifying harmful outputs*: the only human oversight is the principles list [CLM-0028]. That establishes **possibility** — a lab demonstrated the loop; in this course's taxonomy it is a lab self-evaluation by the authors [CLM-0028].

**A deployment decision still needs:** (i) independent evaluation — the verified record contains no non-author numbers, and the judge–human agreement figures live in the full text, unread this round; (ii) quantified judge–human agreement with intervals *on the deployer's prompt distribution*, not the lab's; (iii) a provenance story for the constitution — whose values the principles encode and by what process they were chosen, since the list is itself a proxy for intended values (§3.6); (iv) drift monitoring — the judge is "this model, under this prompt, at this date," a moving target across versions (§6.5); (v) harm-category construction validated for the deployment context. None is supplied by the abstract-level evidence; all five separate "possible" from "deployable."

### (b) Three judge biases a naïve RLAIF pipeline would optimize

The mechanism is identical for all three: the BT loss fits whatever correlates with the judge's choices, at full strength — there is no other target in the objective (§3.6, §6.2).

1. **Length/verbosity.** If the judge prefers longer responses even a few points above chance, the preference model learns it and the optimized policy is long. The human-side analogue ran at 61.4% chosen-strictly-longer in §4.2's illustrative audit; for a judge there is no published magnitude at all — which is the problem.
2. **Style / self-preference.** Judges favor responses in their own model family's idiom, or matching the judging prompt's framing; the construct silently becomes "sounds like the judge," and the policy drifts toward judge-idiomatic text (§3.6).
3. **Sycophantic agreement.** Preference for responses that agree with the prompter or the judge's framing; the policy is optimized to please — a safety-relevant failure (telling users what they want to hear) that preference-accuracy numbers do not display (§6.2's invisible symptoms).

Biases 1–2 are the ones §3.6 names; 3 is §6.2's. No verified magnitude exists for any of them in an AI judge at this build's access level — the honest phrasing is "named, mechanistically plausible, unmeasured here."

### (c) The validation study that upgrades the evidence class

**Design.** From the live RLAIF labeling stream — pinning the judge model, judging prompt, and date (the construct is all three, §6.5) — sample n = 1,000 AI-labeled pairs, stratified by harm category and deployment prompt mix. Two independent human annotators (not project authors; blind to the AI's label and to response provenance) judge each pair under written instructions. Primary statistic: AI–human agreement — the share of pairs where the human majority matches the AI label — with a Wilson 95% interval. Control arm: 500 pairs double-annotated by humans, giving the human–human ceiling the judge is measured against.

**Denominators and widths (recomputed).** n = 1,000 at p̂ = 0.80 gives center 0.7989, half-width 0.0248 → [77.4%, 82.4%]; the 500-row control at p̂ = 0.75 gives center 0.7481, half-width 0.0379 → [71.0%, 78.6%]. The primary arm resolves ±2.5pp — adequate for the thresholds below; the control arm is a ceiling estimate, not a precision instrument.

**Pre-stated weakening numbers.** The RLAIF-alignment hypothesis is weakened if: (1) the AI–human Wilson *lower* bound falls below **0.75**; or (2) AI–human agreement sits **> 10pp below** the human–human control (bound-based comparison); or (3) any harm-category stratum's lower bound falls below **0.60** — a construct change in that category, reported per stratum, never pooled away.

**What a pass establishes — and does not.** A pass upgrades the evidence from possibility to *measured agreement on the sampled distribution*: the judge tracks the human construct at a declared floor there. It does not establish deployment-range validity (§6.1), nor that the optimized policy stays where the judge was validated.

**The study's own limits.** Humans are the gold standard by fiat — their own heuristics are the documented failure [CLM-0029], so the validators import §6.2's problem with them; blinding is incomplete (annotators may recognize AI style); the sample covers the sampled distribution only — judge behavior under distribution shift or across versions remains unmeasured; label agreement is not policy behavior — a high-agreement judge can still be optimized into corners by RL (§6.1); and the study is one snapshot of a moving target (§6.5).

### Common wrong answers

- Reading [CLM-0028] as "CAI validated RLAIF": the verified record is the authors' internal evaluation — possibility, not deployment validity.
- Judge biases listed without mechanism (no link to BT fitting them at full strength): a vocabulary quiz, not an analysis. A validation study with no human–human control is equally uninterpretable — "82% AI–human agreement" means nothing without the ceiling it is measured against.
- Thresholds on point estimates, or no pre-stated weakening number at all; claiming the study validates the *policy* — it validates the *labeler*, on a sample, at one date.

### Grading rubric (assessor)

| Criterion | Pass | Merit | Fail signatures |
|---|---|---|---|
| Established/needed split | possibility vs deployment needs, internal-evidence caveat | all five needs enumerated with reasons | "CAI proved RLAIF works" |
| Biases with mechanism | each tied to BT fitting at full strength | magnitudes honestly labeled unmeasured | buzzword list |
| Study design | denominators, Wilson, control arm, blinding | stratification + pinned judge/prompt/date | "ask some humans to check" |
| Weakening numbers | concrete bounds that fire | stratum-level rule included | "if agreement is low" |
| Limits | gold-standard-by-fiat + sampling named | policy-vs-labeler distinction drawn | absent |
