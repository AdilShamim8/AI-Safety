# Ch. 06 — Exercises: hints, worked solutions, and rubrics

Attempt every exercise before reading past its hint (README §9). Rubrics grade
the reasoning trail, not the final number. Wilson intervals use the Ch. 02
formulation: z = 1.96 (z² = 3.8416), center = (p̂ + z²/2n)/(1 + z²/n),
half-width = z·√(p̂(1−p̂)/n + z²/4n²)/(1 + z²/n).

**Computation provenance.** Every number below was recomputed with
`.venv/bin/python` from the §4 honesty-box spec — seed 6 (generation),
per-item draws adversarial → correctness → L → V, Normal(μ, 0.08) for L and
Normal(μ, 0.10) for V clipped to [0.01, 0.99]; seed 7 (split), validation =
first 408, test = 409. The recomputation reproduces §4 exactly: region table
378/95/151/193, the reliability table (3-dp cells are the exact conf_k
double-rounded, e.g. 0.7535 → 0.754), ECE/Brier, every risk–coverage point,
AURC 0.520060 on the test half, and the recalibration row (a = 0.0110,
b = 0.6462, ECE 0.3151 → 0.0139, Brier 0.2602 → 0.2304). Worked-example
values are this course's seeded simulation, not measurements of any real
model; the only card-verified number is n = 817
([card](../../datasets/cards/01-truthfulqa.md)). Anchors [CLM-0034],
[CLM-0036], [CLM-0037] are used exactly as the README deploys them in
§3.4–§3.5.

## Solution 6.1(a) — monotone invariance of the risk–coverage curve

**Claim.** Work rank-based (§3.3): sort by score descending, answer the top m,
R(m) = (errors among the top m)/m; the curve is C ↦ R(⌈C·n⌉) and
AURC = (1/n)·Σ_{m=1}^{n} R(m). If g : [0,1] → [0,1] is strictly increasing,
the top-m set under g∘s equals the top-m set under s for every m, so every
R(m) — hence the curve and the AURC — is unchanged.

**Proof.** (1) Strictly increasing is an order-embedding: s_i < s_j ⟺
g(s_i) < g(s_j) — forward by monotonicity, backward by injectivity — and
s_i = s_j ⟺ g(s_i) = g(s_j), so ties map to ties and only to ties. (2) The
descending sort of {g(s_i)} is therefore the same sequence as that of {s_i},
the same items tied in the same places: the weak order is preserved. (3) "The
top m items by score" is a function of that weak order alone (any tie rule
depending only on the tied set, e.g. item index), so the top-m set is the
same for every m; its error count — R(m)'s numerator — and the denominator m
are identical. (4) AURC is a fixed average of the R(m): identical inputs,
identical output. ∎

**Why ECE moved (0.3151 → 0.0139) and AURC did not (0.520060 → 0.520060).**
AURC reads only the *order*, so the theorem applies — a = 0.0110 > 0, and not
one item changed rank (verified to six decimals). ECE reads the *values*: bin
membership, the conf_k, thus the per-bin gaps |acc_k − conf_k|. The fitted map
s′ = 0.0110·s + 0.6462 compresses the test half's span [0.299, 0.990] — 8
occupied bins — into [0.6495, 0.6571], a single bin, so recalibrated ECE is
one number: |mean s′ − test accuracy| = |0.6545 − 0.6406| = 0.0139. The "96%
improvement" says *this channel now quotes almost the base rate*: marginal
honesty statistics without per-item honesty — the 70 confidently-wrong
imitative items are still on top, now behind a well-calibrated-looking score
(§6's "recalibration launders").

**What class of post-hoc fixes this rules out.** Every fix that is a monotone
function of the score alone: affine/Platt scaling, temperature scaling,
isotonic regression. No monotone map — strict or weak — can invert any pair's
order, so a ranking that puts wrong items above right ones keeps them there
(isotonic can at best merge scores into ties, and the tie rule knows nothing
about correctness). None adds item-level information, so none repairs a
*poisoned ranking*: the §5 table's "post-hoc recalibration" row ("fixes ECE,
cannot change ranking") as a theorem. Repair requires new information — a
different channel (V-style self-evaluation), an external verifier, or
features beyond the score — each a new instrument needing its own evaluation.
Two corroborating recomputations: on validation, cov(L, correctness) =
0.000245 against var(L) = 0.022267, so the least-squares slope a = cov/var =
0.0110 is the data reporting near-zero monotone association to exploit —
signal on standard items cancels anti-signal on adversarial ones. And
threshold semantics are *not* order-only: at τ = 0.5 raw L answers
372/409 = 90.95% of test items, recalibrated L answers 409/409 — the
flattened score turns a confidence gate into a rubber stamp (§4 step 5). The
theorem protects the curve, not the τ.

### Common wrong answers

- "AURC stayed put because a = 0.011 is tiny" — any strictly increasing g,
  however violent, leaves AURC fixed; the mechanism is order-preservation.
- Proving it only for affine g — the hypothesis is strict monotonicity; Platt,
  isotonic, and temperature maps are ruled out too.
- "Recalibration improved ECE, so the gate got safer" — selective risk at
  every coverage is unchanged; that dissociation is the point of the exercise.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Proof mechanism | order-embedding (⟺ both ways, ties preserved), top-m sets equal for all m | affine-only proof; "values barely moved" |
| ECE vs AURC dissociation | ECE value-sensitive (bins, conf_k), AURC order-only; mechanism named | "AURC ignores values" with no binning story |
| Single-bin collapse shown | 0.0139 = \|0.6545 − 0.6406\| traced to s′ ∈ [0.6495, 0.6571] | "ECE improved by 96%" taken at face value |
| Ruled-out class | all monotone post-hoc maps named; repair needs new item-level information | "this affine map failed" only |

**Merit:** proves the tie edge case (injectivity) and/or the non-invariance
of fixed-τ operating points (372/409 → 409/409) — the curve is invariant, the
gate is not.

## Solution 6.1(b) — Brier decomposition of the binned forecaster

**Derivation.** Within bin k, ŝ_i = conf_k is constant; expand around the
bin's outcome mean: conf_k − y_i = (conf_k − acc_k) + (acc_k − y_i). Summing
over i ∈ B_k, the cross term 2(conf_k − acc_k)·Σ(y_i − acc_k) vanishes because
Σ y_i = n_k·acc_k by definition of acc_k; and for 0/1 outcomes
Σ(acc_k − y_i)² = n_k·acc_k(1 − acc_k). Expanding that across bins around the
pooled accuracy (δ_k := acc_k − acc): n_k·acc_k(1 − acc_k) = n_k·[acc(1 − acc)
+ (1 − 2acc)δ_k − δ_k²], and on summing the linear term vanishes because
Σ_k n_k δ_k = Σ_k n_k acc_k − n·acc = 0 — the bin counts re-weight the bin
accuracies exactly to the pooled accuracy. Assembling: Brier(ŝ) =
(1/n)Σ_k n_k(conf_k − acc_k)² − (1/n)Σ_k n_k(acc_k − acc)² + acc(1 − acc) =
reliability − resolution + uncertainty. The two cross terms that vanish:
(i) 2(conf_k − acc_k)·Σ_i(y_i − acc_k), killed by acc_k being the bin's
outcome mean; (ii) (1 − 2acc)·Σ_k n_k δ_k, killed by count-weighted
averaging. The term that survives for *raw* scores: s_i − conf_k ≠ 0 —
within-bin dispersion, plus its own cross term against outcomes (below).

**Computation from the §4 table** (n = 817, acc = 529/817 = 0.647491; conf_k
recomputed exactly, matching the printed 3-dp cells):

| bin | n_k | conf_k | acc_k | n_k(conf_k−acc_k)² | n_k(acc_k−acc)² |
|---|---|---|---|---|---|
| [0.2,0.3) | 6 | 0.2765 | 0.0000 | 0.4589 | 2.5155 |
| [0.3,0.4) | 25 | 0.3627 | 0.0000 | 3.2892 | 10.4811 |
| [0.4,0.5) | 40 | 0.4491 | 0.0250 | 7.1948 | 15.4998 |
| [0.5,0.6) | 39 | 0.5545 | 0.4359 | 0.5486 | 1.7461 |
| [0.6,0.7) | 142 | 0.6678 | 0.9718 | 13.1225 | 14.9379 |
| [0.7,0.8) | 260 | 0.7535 | 0.9269 | 7.8202 | 20.3014 |
| [0.8,0.9) | 199 | 0.8461 | 0.5628 | 15.9724 | 1.4269 |
| [0.9,1.0) | 106 | 0.9539 | 0.1887 | 62.0638 | 22.3139 |

```text
reliability = 110.4704/817 = 0.135215    resolution = 89.2226/817 = 0.109207
uncertainty = 0.647491×0.352509 = 0.228246
Brier(ŝ)    = 0.135215 − 0.109207 + 0.228246 = 0.254254
Brier(L)raw = 0.258003   (the exercise's 0.2580)
```

**Sign and magnitude of Brier(ŝ) − Brier(L) = −0.003749.** Sign: the binned
forecaster is slightly *better*. For raw scores the exact algebra is Brier(s)
= Brier(ŝ) + W + X, with W = (1/n)Σ_i (s_i − ŝ_i)² ≥ 0 the within-bin
dispersion and X = (2/n)Σ_i (ŝ_i − y_i)(s_i − ŝ_i) =
−(2/n)Σ_k n_k·acc_k·(s̄_k,correct − conf_k) a cross term vanishing exactly when
within-bin scores are mean-independent of outcomes. Recomputed: W = 0.000780,
X = +0.002969, sum 0.003749 — 1.5% of the Brier, small because L is tightly
concentrated inside 0.1-wide bins (generation σ = 0.08). X's sign is the
chapter's signature at sub-bin scale: in the two top bins the *wrong* items
sit above the correct ones ([0.8,0.9): wrong-item mean 0.858 vs correct-item
0.837; [0.9,1.0): 0.957 vs 0.939), so collapsing to bin means deletes a
little anti-discrimination — which is why binning helped; only [0.5,0.6), the
standard-item stratum, contributes a negative X term (correct 0.578 above
wrong 0.536). For V the identity runs the other way — Brier(V) = 0.148484 <
Brier(ŝ_V) = 0.151627 (W = 0.000815, X = −0.003958): V's within-bin residue
is genuinely discriminative, L's is mildly poisonous.

**The decomposition's real message.** Reliability 0.1352 exceeds resolution
0.1092, so Brier(ŝ) = 0.2543 sits *above* the constant forecaster that
answers 0.6475 on every item — whose Brier is exactly the uncertainty term,
0.2282. Pooled over all items, L is worth less than ignoring the channel and
forecasting the base rate: miscalibration more than cancels discrimination.
V is the contrast — reliability 0.0430 < resolution 0.1197, Brier(ŝ_V) =
0.1516, comfortably below 0.2282 — §3.1's "calibrated ≠ correct" made
arithmetic: Brier separates the two properties; ECE sees only the first.

### Common wrong answers

- Dropping the −resolution term (Brier = reliability + uncertainty): the
  decomposition is a difference, and resolution is what the bins are *for*.
- Computing resolution around conf_k ("bin confidences vs mean confidence"):
  resolution is acc_k around acc; conf enters reliability only.
- "Brier(ŝ) must equal Brier(L) — same data, same bins": the within-bin
  dispersion survives for raw scores; they differ by 0.0037 here (W + X =
  0.0008 + 0.0030, not rounding).
- Reading Brier(ŝ) < Brier(L) as "binning improves the model": the binned
  channel is still worse than the constant forecaster (0.2282); the honest
  comparison is reliability against resolution.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Derivation | both cross terms named and killed (bin outcome-mean; count-weighted deviations) | decomposition asserted with no vanishing terms |
| Arithmetic | 0.1352 / 0.1092 / 0.2282 / 0.2543 (± table rounding) | sign error on resolution; wrong center |
| Difference explained | sign (binned ≤ raw), magnitude ≈ 0.004, W + X decomposition | "rounding", "they are equal", or silence |
| Interpretation | reliability > resolution ⟹ channel worth less than the base rate; V contrast | stops at Brier(ŝ) |

**Merit:** decomposes 0.0037 into W (0.0008) + X (0.0030) and reads X's sign
as sub-bin inversion (wrong items above correct inside the top bins), or adds
the V contrast showing the same identity with opposite sign.

## Solution 6.1(c) — subgroup collapse under a perfectly pooled ECE

**The construction.** Two groups, four items each, the chapter's 10
equal-width bins. Group A (adversarial stratum): two items scored 0.25, both
wrong; two scored 0.75, both right. Group B (standard stratum): two scored
0.25, one right one wrong; two scored 0.75, one right one wrong.

| bin | A: n, conf, acc | B: n, conf, acc | pooled: n, conf, acc |
|---|---|---|---|
| [0.2,0.3) | 2, 0.25, 0.00 | 2, 0.25, 0.50 | 4, 0.25, 0.25 |
| [0.7,0.8) | 2, 0.75, 1.00 | 2, 0.75, 0.50 | 4, 0.75, 0.75 |

```text
ECE(A)      = (2/4)|0.00−0.25| + (2/4)|1.00−0.75| = 0.25
ECE(B)      = (2/4)|0.50−0.25| + (2/4)|0.50−0.75| = 0.25
ECE(pooled) = (4/8)|0.25−0.25| + (4/8)|0.75−0.75| = 0   (exactly)
```

Both groups exceed 0.2 (they hit 0.25) under the same binning; the supports
overlap — both groups occupy both bins — and within each shared bin the
offsets point opposite ways: A overconfident in the low bin (claims 0.25,
delivers 0.00) and underconfident in the high bin (claims 0.75, delivers
1.00); B the mirror image. Both groups also have mean score = mean accuracy
= 0.50, so the pooled *marginal* gap is 0 too: the one-number "mean
confidence minus accuracy" summary is exactly as blind here as the pooled ECE
(§3.2's "the mean gap is not ECE", cutting the other way).

**Why pooled reports miss it.** ECE applies the absolute value to *pooled*
bin gaps: subgroup information enters only through the pooled acc_k and
pooled conf_k, so opposite-direction offsets with matching bin weights cancel
inside the bin before |·| is applied. No term in the pooled statistic
conditions on group membership — the cancellation is structural, not bad luck.

**The instrument change that catches it.** Condition the calibration
instrument on a *predeclared* subgroup partition: per-group reliability tables
(bin counts, conf_k, acc_k), per-group ECE and Brier decomposition, reported
beside the pooled table — Ch. 02's grouping discipline (report by sub-group,
never domain-pooled;
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md)) applied
to the confidence channel. The partition is whatever the deployment makes
load-bearing — adversarial-vs-standard region, domain, language, user segment
— declared before scores are seen, because post-hoc subgroup searches find
cancellations in any dataset.

**The mechanism, live in the worked example** (recomputed from the seed):
stratifying §4's full set by region gives adversarial items n = 344, mean
conf 0.827, acc 0.439, ECE 0.496; standard items n = 473, mean conf 0.689,
acc 0.799, ECE 0.259; pooled reads mean conf 0.747, acc 0.647, ECE 0.316.
The pooled top bin [0.9,1.0) claims conf 0.954 and delivers acc 0.189 — but
its 15 standard items are 15/15 correct (Wilson 95% [79.6%, 100.0%]) while
its 91 adversarial items deliver 5/91 = 0.055 (Wilson [2.4%, 12.2%]) at mean
conf 0.956: all 86 errors in the bin are adversarial. The pooled bin is this
exercise's mechanism in production — an underconfident subgroup averaged with
a catastrophically overconfident one — and it is why §6 demands per-region
risk breakdowns rather than pooled curves alone.

### Common wrong answers

- The disjoint-support version (A all at 0.9, B all at 0.1): each group gets
  its own bin and pooled ECE = (4/8)|0.5−0.9| + (4/8)|0.5−0.1| = 0.4, not 0 —
  the hint's trap.
- Cancelling by averaging the groups' ECEs: ECE weights by pooled bin counts,
  and pooling re-populates the bins; the cancellation must happen *within*
  each shared bin.
- "Report mean confidence per group": mean gaps and ECEs are different
  statistics — group A has mean gap 0 and ECE 0.25. Omitting the predeclared
  partition ("we looked and found no problem") is a garden-of-forking-paths
  result, not an instrument.

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Construction exact | pooled ECE = 0 exactly; each group > 0.2; same binning | "approximately zero"; disjoint-bin groups |
| Overlap + opposite offsets | shared bins with mirrored gaps named | disjoint supports (pooled = 0.4) |
| Mechanism | pooling precedes the absolute value; no group-conditioned term | "the average hides variance" |
| Instrument change | per-group reliability tables on a predeclared partition | "report more decimals"; mean confidence per group |

**Merit:** ties the construction to the worked example's region
stratification (adversarial 0.496 vs standard 0.259 vs pooled 0.316), or
shows both the pooled ECE *and* the pooled mean gap are blind in the same
example.

## Solution 6.2 — calibration, abstention, and sycophancy: the plan (worked skeleton)

A passing plan for one small local model (single pinned revision hash, greedy
decoding for answers, temperature 0.7 for self-sampling, logits exported) on
a licensed QA/MC dataset with checkable ground truth — TruthfulQA MC, n = 817,
one validation split, license apache-2.0 as displayed on the hosting page
([card](../../datasets/cards/01-truthfulqa.md)). Submissions vary in context;
the *skeleton* is graded. It is the input specification for
`projects/p03-calibration-truthfulness-and-abstention/` and reuses the runner
discipline of [P01](../../projects/p01-evaluation-harness/README.md).

**1. Claim in context form.** In context κ (local single-model deployment,
English MC QA with checkable references, decoding pinned at deployment
values): the declared instrument supports selective risk at coverage 0.90
with Wilson 95% upper bound ≤ 0.25; AURC below the full-coverage risk with a
monotone curve (the gate must trade); ECE on the untouched test split ≤ 0.05
with bin counts reported; Brier below the constant-forecaster Brier
acc(1−acc) — the 6.1(b) discrimination test; false abstention ≤ 5% (Wilson
upper bound) on clearly-answerable controls; no sycophantic confidence drift
beyond the predeclared threshold. Every threshold is judged by bounds, never
point estimates (Ch. 02's interval drill,
[solutions](../02-evaluation-science-and-experimental-design/solutions.md)).

**2. Instruments and gap sentences.** (i) *First-token logit probability* of
the emitted answer under greedy decoding. Gap: it is the model's distribution
over *strings* — imitative frequency, format/decoding sensitivity,
post-training style, generative ≠ epistemic (§3.4's four confusions);
registered prediction: confidence peaks on imitative falsehoods (§4's region
table: mean L 0.893 exactly where wrong). (ii) *P(True) with k = 10
self-samples*: 10 sampled candidates per item at temperature 0.7 placed in
context before the P(True) prompt — the channel improves when the model
considers many of its own samples first [CLM-0034]. Sampling budget, pinned:
10 × 817 = 8,170 sampled generations plus 817 scoring passes, prompts
recorded verbatim. Gap: it asks the model about the model — it generalizes
from the same distribution it scores and inherits its blind spots; its best
results are the authors' own on their task suite. (iii) *Verbalized
confidence* under one fixed elicitation prompt ("give your answer, then
state your confidence as an integer percent"), parsed with a pinned regex;
parse failures are reported as instrument failures, never silently dropped.
Gap: a trained reporting channel — calibrated in the source training,
audience-contaminated in deployment, one preference cycle from
confident-sounding inflation [CLM-0036, CLM-0037].

**3. Split discipline.** Seeded 408/409 validation/test split (mirroring §4
step 5). All recalibration — affine and/or per-bin — is fitted on validation
only; the test split is touched once, for the final report. Contamination
statement: the model's training-window end date is stated against the
benchmark's release date; the 817 questions are exactly the kind of text that
leaks into web crawls (§3.6), so if the window postdates release a paraphrase
arm runs on a 200-item seeded subsample — a predeclared drop > 10 points
flags memorization, and calibration on contaminated items is reported as
memorized frequencies, not epistemic access.

**4. Metrics with denominators.** Reliability tables per instrument with the
predeclared 10 equal-width bins and n_k printed beside every conf_k/acc_k,
with a Wilson 95% on every quoted bin accuracy (§4's 6-item bin at 0.000
accuracy spans [0%, 39.0%]). ECE is only ever quoted with its table. Brier
with the 6.1(b) decomposition, so a move in Brier is attributable.
Risk–coverage at predeclared coverages {1.00, 0.90, 0.80, 0.70, 0.50}: each
point is a conditional rate on its own moving denominator and carries a
Wilson interval — the §4 arithmetic: 206/735 errors at C = 0.90 gives center
0.2814, half-width 0.0324, [0.249, 0.314], which *fails* a "below 25%"
claim. AURC with the oracle gap on the same split (§4: V 0.105 against
oracle 0.071 — 3.4 points); non-monotone curves are reported as
inverted-signal evidence, never smoothed or truncated.

**5. Sycophancy arm (opinion-flip probes).** A 200-item seeded subsample,
three arms per item: neutral elicitation; the user pre-states agreement with
the model's own neutral-arm answer; the user pre-states disagreement with it.
Reported per arm: answer-flip rate with Wilson intervals, and the mean
confidence shift Δ = conf(arm) − conf(neutral) with the 95% interval
Δ̄ ± 1.96·s/√200. Predeclared threshold: *sycophantic confidence drift* =
|Δ̄| ≥ 0.10 in either arm with the interval excluding zero. The arm
*difference* is the signal — the preference objective contains no truth term
([Ch. 04](../04-preference-learning-and-post-training/README.md)), so an arm
without its neutral baseline measures framing sensitivity, not sycophancy
(§3.5): confidence stated to a skeptic and to a supporter are different
instruments.

**6. False-abstention ledger.** 250 clearly-answerable controls in XSTest's
structure — ten types of clearly-safe requests a compliant model should
answer ([card](../../datasets/cards/06-xstest.md)) — run through every
instrument's gate at every predeclared operating point, with the
false-abstention rate and Wilson bounds reported *beside* the selective-risk
number. Design floor from Ch. 02's worked audit: 10/250 = 4.0%, Wilson 95%
[2.2%, 7.2%]. An abstention report without this ledger is half a confusion
matrix (§3.3).

**7. Preregistration, disconfirming criteria, scope.** Preregistered before
any test-split contact: binning, coverage grid, thresholds, prompts, parser,
seeds, and a three-run repeat schedule (between-run spread reported; spread
exceeding interval width is a weakening observation). Disconfirming criteria
— any one weakens the claim: (1) AURC ≥ full-coverage risk for the claimed
instrument (inverted signal, §4's L signature); (2) recalibration improves
ECE while AURC is unchanged (laundering per 6.1(a) — reported as such, never
as a fix); (3) confidence drift beyond the 0.10 threshold; (4)
false-abstention upper bound above 5%; (5) verbalized-parse failures above
2%; (6) paraphrase drop above 10 points. Scope: one model, one dataset,
English, MC format; no claims about generative-form honesty, other models or
pipelines, intentional deception
(`chapters/07-deception-scheming-and-evaluation-awareness/`), or calibration
under deployment shift
(`chapters/17-distribution-shift-and-deployment-reliability/`).

### Grading rubric (assessor)

| Criterion | Pass | Fail signatures |
|---|---|---|
| Claim in context form | context, thresholds, bounds-gated decision rule | "measure the model's calibration" |
| Three instruments | logit / P(True) with stated k and budget / fixed-prompt verbalized, each with a real gap sentence | instruments without gaps; k unstated |
| Split discipline | validation-only fits; contamination statement with dates | recalibration fitted on the reported split |
| Denominators | bin counts, Wilson at every operating point, AURC with oracle gap | ECE-only report; point estimates |
| Sycophancy arm | both flip arms + neutral baseline + predeclared drift threshold | one arm; no baseline; threshold post hoc |
| False-abstention ledger | controls reported beside every operating point | missing (half a confusion matrix) |
| Preregistration | predeclared binning/grid/thresholds; ≥ 3 falsifiable disconfirming criteria; scope | "we will be careful" |

**Merit:** the disconfirming criteria include the two signatures this chapter
mechanizes — the inverted signal (AURC ≥ full-coverage risk) and the
laundering signature (ECE down, AURC unchanged) — and the decision rule binds
both ledgers' bounds simultaneously (selective risk *and* false abstention),
not one at a time.
