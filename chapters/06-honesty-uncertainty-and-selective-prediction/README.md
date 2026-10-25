# Ch. 06 — Honesty, uncertainty, and selective prediction

> Every earlier chapter measured what a system *does*. This one asks whether
> the system can report what it *knows* — and what breaks when the confidence
> signal you build abstention on was never a truth probability at all.

## 1. Research question and failure pathway

**The question this chapter answers:** *how do you measure whether a model
knows what it knows, turn that measurement into an abstention policy that
actually reduces error, and avoid the three lookalikes — fluency, token
probability, and user-pleasing agreement — that get mistaken for knowledge?*

**The failure pathway it prevents:**

```text
fluent, assertive answers ──► no legible uncertainty signal ──►
users and pipelines treat every answer as knowledge ──►
token probability mistaken for truth probability ──►
confidence peaks exactly on imitative falsehoods ──►
the system is most certain where it is most wrong
```

The middle arrows are the core. A model's probability for a string is a
statement about *text statistics* — how likely humans were to write
something like it — not about the world; where the popular answer is the
false one, imitation points the confidence signal the wrong way (§3.4, §4).
The last arrow makes this a deployment problem: automation bias means users
anchor on confident answers, and a selective-prediction layer driven by a
poisoned signal *concentrates* harm — in the worked example, gating on the
raw token probability raises the error rate among answered items from 35.3%
to 46.1% at half coverage. The chapter sits on the spine of
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md);
what is new is the *epistemic channel* — scores that claim to describe the
model's own uncertainty — and the abstention machinery built on it.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.**
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
(construct validity, paired ledgers, Wilson intervals, preregistration);
diagnostic task B
([diagnostic](../../prerequisites/diagnostic.md)); refresher R3
([targeted refreshers](../../prerequisites/targeted-refreshers.md)).

**Outcomes.** After this chapter you can:

1. Distinguish **truthfulness**, **honesty**, and **calibration**, and name
   the confusion committed when any two are collapsed.
2. Compute reliability tables, expected calibration error (ECE), Brier
   scores, risk–coverage curves, and area under the risk–coverage curve
   (AURC) — and state what each metric does not measure.
3. Explain **sycophancy**: its mechanism under preference training, its
   measurement, and why it contaminates factuality scores and confidence
   elicitation alike.
4. Explain why token probabilities and verbalized confidence are **not
   automatic truth probabilities**, and design instruments and abstention
   policies that survive that fact.

**Scope exclusions.** Intentional deception and evaluation awareness are
`chapters/07-deception-scheming-and-evaluation-awareness/` — here "honesty"
means self-report correspondence, not intent. Internal representations of
truth are `chapters/09-mechanistic-interpretability-foundations/` through
`chapters/11-behavioral-steering-and-representation-interventions/`;
calibration decay under deployment shift is
`chapters/17-distribution-shift-and-deployment-reliability/`. Running a
live calibration experiment is
`projects/p03-calibration-truthfulness-and-abstention/`'s job; this chapter
supplies the design, arithmetic, and failure conditions that project must
survive. Whether models "really" have beliefs is noted where it bites (§6)
and otherwise set aside.

## 3. Core explanation

### 3.1 Three constructs that keep getting collapsed

Fix an evaluation of n items. The model produces answer a_i for item i;
y_i ∈ {0,1} is its correctness against a reference; s_i ∈ [0,1] is a
confidence score some instrument attaches to item i.

- **Truthfulness** is an *output-level* property: does a_i correspond to
  verifiable reference facts. TruthfulQA operationalizes the adversarial
  corner: 817 questions in one validation split, built to trigger
  *imitative falsehoods* — false statements humans commonly repeat — with
  page-verified categories such as Misconceptions, Proverbs, Misquotations,
  Conspiracies, and Superstitions
  ([card](../../datasets/cards/01-truthfulqa.md); SRC-DATASET-001). The
  mechanism matters more than the name: the wrong answer is the
  *statistically frequent* answer in pretraining text, so an imitatively
  trained model fails for a reason baked into its objective.
- **Honesty** is a *self-report-level* property. This course's
  operationalization: the model's statements about its own knowledge track
  its actual epistemic state — when it signals doubt it is unreliable; when
  it claims to know it is right. Kadavath et al. frame their self-evaluation
  work explicitly as groundwork "for training more honest models" [CLM-0034].
  Honesty is not directly measurable without a truth proxy: every honesty
  metric in practice is the *calibration of some self-report channel*
  against realized outcomes.
- **Calibration** is a *statistical* property of the pair (score, outcome):
  among items scored s, the realized correctness frequency is s — a matching
  property, not a competence property.

Each pairwise collapse has a name. **Calibrated ≠ correct:** a model scoring
everything 0.4 and right 40% of the time is perfectly calibrated and useless;
the Brier decomposition (Exercise 6.1) separates calibration from
discrimination exactly. **Truthful ≠ honest:** a true answer whose confidence
bears no relation to its grounds is luck, not self-report — and an honest
model at full coverage produces *more visible errors than a bluffer*;
honesty makes the score interpretable, it does not raise it. **Honest ≠
calibrated:** a model can faithfully report a miscalibrated internal state;
this chapter's target is the conjunction — a calibrated channel that reports
something about the *item*, not just the marginal.

### 3.2 Measuring calibration: reliability table, ECE, Brier

Partition [0,1] into K equal-width bins B_1..B_K, with n_k items, mean score
conf_k, and realized accuracy acc_k in bin k:

```text
ECE   =  Σ_k (n_k / n) · |acc_k − conf_k|           (expected calibration error)
Brier =  (1/n) Σ_i (s_i − y_i)^2                    (mean squared score vs outcome)
```

Three disciplines. **ECE is a binning artifact:** it depends on K and on bin
populations — with n = 817 and K = 10, the worked example's bins hold between
6 and 260 items, and a 6-item bin reading 0.000 accuracy carries a Wilson 95%
upper bound near 0.39; report bin counts with every ECE. **The mean gap is
not ECE:** mean confidence minus accuracy is a one-number marginal, while ECE
sees the shape — in §4, instrument V has a mean gap of −0.6 points yet
ECE = 0.187, because off-middle bins cancel in the average. **Brier is a
proper scoring rule:** minimized in expectation only by true probabilities,
it punishes miscalibration *and* rewards discrimination, while ECE measures
only the first (Exercise 6.1(b) decomposes it).

### 3.3 Selective prediction: coverage, selective risk, risk–coverage curves

An abstention policy answers item i only when its score clears a threshold:
answer iff s_i ≥ τ, with coverage C(τ) = (1/n)·#{i : s_i ≥ τ} and selective
risk R(τ) = (errors among answered)/(answered). It is cleaner to work
rank-based: sort items by score descending and answer the top m; the
**risk–coverage curve** is R as a function of C = m/n, and the **AURC** is
the mean of R(m) over m = 1..n — the average selective risk if every
coverage level were equally likely. The **oracle** curve ranks by y_i itself
(all correct items first); it is the best achievable curve for this (s, y)
set, and the gap to it measures the ranking information the score fails to
extract.

Three facts deployers get wrong. **Abstention only trades if the signal
separates correct from wrong:** a poisoned signal inverts the trade — in §4,
gating on token probability yields AURC 0.520 against a full-coverage risk
of 0.353, so averaged over coverage levels the gate was *worse* than
answering everything. **Selective risk is a conditional rate:** its
denominator is the answered count, which moves with τ, so Ch. 02's interval
discipline applies at every quoted operating point (§4, step 4).
**Abstention has a false-abstention side, the same ledger as over-refusal:**
XSTest measures exactly that complement — 250 clearly-safe prompts a
well-calibrated model should comply with, plus 200 unsafe contrasts it should
refuse ([card](../../datasets/cards/06-xstest.md); SRC-PAPER-003). An
abstention report without a false-abstention rate on clearly-answerable
items is half a confusion matrix.

### 3.4 Where confidence comes from — and why token probability is not a truth probability

The model's output distribution p(x) is a distribution over *strings*.
Reading p(answer) as "the probability the answer is true" silently
identifies four different objects:

1. **Imitation.** Pretraining maximized the likelihood of human text, so
   frequently-made claims get high probability regardless of truth; on
   imitative falsehoods the wrong answer is the *typical* answer
   ([card](../../datasets/cards/01-truthfulqa.md)). The bias is directional
   and points at the hazard.
2. **Format and decoding.** Tokenization, prompt template, and sampling
   parameters move token probabilities with no epistemic change — Ch. 02's
   format-sensitivity discipline, applied to the confidence channel.
3. **Post-training.** Preference optimization reshapes marginals (hedging
   phrases, assertiveness) as *style*, independently of knowledge — the
   pressure §3.5 documents as sycophancy.
4. **Generative ≠ epistemic.** The distribution answers are sampled from and
   the distribution that would describe the model's knowledge are different
   objects, however correlated.

The research program built on here adds self-evaluation channels that
partially escape imitation, and that §6 treats as *generated text shaped by
an objective* — trainable in, trainable out. **P(True):** sample an answer,
then ask the model to evaluate the probability that this specific answer is
correct; Kadavath et al. report encouraging performance, calibration, and
scaling across a diverse task suite, improving further when the model
considers many of its own samples first [CLM-0034]. **P(IK):** predict the
probability that "I know" the answer *before* proposing one — an
abstention-native signal that performs well, partially generalizes across
tasks, but struggles with calibration on *new* tasks, and rises
appropriately when relevant source material enters the context [CLM-0035].
**Verbalized confidence:** train the model to *say* "90% confidence" without
logits; Lin et al. show a GPT-3 model whose verbalized levels map to
well-calibrated probabilities, remain moderately calibrated under
distribution shift, and track uncertainty in its own answers rather than
imitating human examples [CLM-0036].

### 3.5 Sycophancy: the preference pressure against honesty

**Sycophancy** — responses that match user beliefs over truthful ones — is a
property of the training pipeline, not a bug in individual models. Sharma et
al. document it on both sides of the preference loop: five state-of-the-art
assistants exhibit sycophancy consistently across four varied free-form
tasks; in human preference data, responses matching the user's views are
more likely to be preferred; humans and preference models prefer
convincingly-written sycophantic responses over correct ones a non-negligible
fraction of the time; and optimizing outputs against preference models
sometimes sacrifices truthfulness in favor of sycophancy [CLM-0037].

The mechanism is structural and connects to
[Ch. 04](../04-preference-learning-and-post-training/README.md): the
preference objective contains no truth term, so truth enters only insofar as
raters reward it — and they measurably reward *agreement* more often. Three
consequences for measurement. **Factuality scores need flip arms:** a
neutrally-asked question measures agreement under neutral framing; the same
question with the user's contrary opinion stated is a different measurement,
and the *difference* between arms is the sycophancy signal (Exercise 6.2
requires this design). **Confidence elicitation is contaminated by
audience:** "90% sure" to a skeptic and to a supporter are not the same
quantity; the elicitation prompt is part of the instrument. **Sycophancy is
a moving target:** it is a trained disposition measured against whatever the
current pipeline rewards, so an honesty claim dated t is about the pipeline
as of t.

### 3.6 Measuring factuality: TruthfulQA used honestly

TruthfulQA is the course's canonical factuality instrument, and its card
states exactly how far it reaches: 817 questions, one validation split,
multiple-choice and generative scoring regimes, the adversarial categories
of §3.1, license apache-2.0 as displayed on the hosting page
([card](../../datasets/cards/01-truthfulqa.md); SRC-DATASET-001). The
card's negative scope is load-bearing: it cannot support honesty or
calibration claims, cannot rank models without prompt format and decoding
parameters stated, and cannot speak to long-horizon consistency;
paper-level details remain pending the assigned full-text read and are not
cited here as fact.

Two Ch. 02 disciplines become concrete on this dataset. **Contamination:**
the 817 questions are exactly the kind of text that leaks into web crawls, so
a model whose training window postdates the benchmark may have memorized
question–answer structure — a calibration curve on contaminated items
measures memorized frequencies, not epistemic access; report knowledge
cutoffs against benchmark release dates. **The honesty gap:** TruthfulQA
measures an output-level construct, the §3.4 channels a self-report
construct, and a deployer building selective prediction needs *both* plus
the abstention ledger of §3.3 — the shape of the artifact in §8 and of
`projects/p03-calibration-truthfulness-and-abstention/`.

## 4. Worked example: calibrating and gating an 817-question evaluation, end to end

**Honesty box.** The only real-world number here is n = 817, the TruthfulQA
validation split's verified row count
([card](../../datasets/cards/01-truthfulqa.md)). Every per-item score and
label is a *seeded simulation* — this course's own operationalization, so
that every §3 formula is computable by a checkable script; these are not
measurements of any real model, and real-model verification is
`projects/p03-calibration-truthfulness-and-abstention/`'s job. Spec: each
item is adversarial with probability 0.40 (course-chosen; the card publishes
no category proportions); the model is correct with probability 0.80 on
standard items, 0.45 on adversarial ones; L is Normal(μ_L, 0.08) clipped to
[0.01, 0.99] with μ_L = 0.75 / 0.90 / 0.45 for correct / adversarial-wrong
(the imitative pull) / standard-wrong; V is Normal(μ_V, 0.10) clipped with
μ_V = 0.72 / 0.55 / 0.40 (the self-evaluation partially escapes the pull).
Seeds 6 (generation) and 7 (split); every number was recomputed with
`.venv/bin/python` at the repo root; the script lands with the solutions
pass. **Instruments:** L is the *logit-style* channel — the probability
assigned, at generation time, to the emitted answer string; V is the §3.4
*self-evaluation* channel.

**Step 1 — where the errors live.** Simulated outcome: 529/817 correct
(64.75%), 344 adversarial items. The region table is the diagnosis before
any calibration math:

| Region | n | mean L | mean V | accuracy |
|---|---|---|---|---|
| standard, correct | 378 | 0.752 | 0.723 | 1.000 |
| standard, wrong | 95 | 0.442 | 0.395 | 0.000 |
| adversarial, correct | 151 | 0.743 | 0.716 | 1.000 |
| adversarial, wrong | 193 | **0.893** | **0.543** | 0.000 |

The fourth row is the chapter in one line: token probability is *highest*
exactly where the model is wrong, because the wrong answer is the frequent
one. V does not fully escape (0.543, above its standard-wrong 0.395) —
consistent with self-evaluation inheriting the model's blind spots
[CLM-0034, CLM-0035] — but it is 35 points lower than L in the region that
matters.

**Step 2 — calibration.** Mean confidence: L = 0.747, V = 0.641, against
accuracy 0.648 — L overconfident by 10 points, V by −0.6. Reliability table
for L (10 equal-width bins; empty bins omitted):

| bin | n | mean conf | accuracy |
|---|---|---|---|
| [0.2, 0.3) | 6 | 0.277 | 0.000 |
| [0.3, 0.4) | 25 | 0.363 | 0.000 |
| [0.4, 0.5) | 40 | 0.449 | 0.025 |
| [0.5, 0.6) | 39 | 0.555 | 0.436 |
| [0.6, 0.7) | 142 | 0.668 | 0.972 |
| [0.7, 0.8) | 260 | 0.754 | 0.927 |
| [0.8, 0.9) | 199 | 0.846 | 0.563 |
| [0.9, 1.0) | 106 | **0.954** | **0.189** |

ECE(L) = **0.316**, ECE(V) = **0.187**; Brier(L) = **0.258**,
Brier(V) = **0.149**. Two failure shapes: L's top bin claims ≥ 0.9 and
delivers 0.189 — a 76-point gap on 106 items — and its ECE is three times
its marginal gap, because the table's internal inversion cancels in the
average. V is *not* well calibrated in absolute terms; it is less
miscalibrated, and far better at ranking, which is the next measurement.

**Step 3 — selective prediction.** Rank by score; answer the top-C fraction:

| coverage | n answered | risk L | risk V | risk oracle |
|---|---|---|---|---|
| 1.00 | 817 | 0.3525 | 0.3525 | 0.3525 |
| 0.90 | 735 | 0.2844 | 0.2803 | 0.2803 |
| 0.80 | 654 | 0.2951 | 0.2049 | 0.1911 |
| 0.70 | 572 | 0.3357 | 0.1416 | 0.0752 |
| 0.50 | 408 | **0.4608** | 0.0613 | 0.0000 |

AURC: L = **0.520**, V = **0.105**, oracle = **0.071**. Read the L column
slowly: the curve is *non-monotone* — risk falls to 0.284 at coverage 0.90
as low-confidence standard-wrong items drop out, then *rises* to 0.461 at
coverage 0.50 as the kept set fills with high-confidence adversarial-wrong
items; gating on token probability at half coverage is worse than answering
everything. The concentration is stark: the top 10% by L (82 items, mean
confidence 0.966) contains 70 errors, *all 70* on adversarial items —
accuracy 0.146 at self-reported 0.97. V's curve trades monotonically and
sits 3.4 AURC points above the oracle: the self-evaluation signal is not
honest, but it is *informative*, and those are different properties.

**Step 4 — the operating point, with its interval.** Deploy V at coverage
0.90: 735 answered, 206 errors, selective risk 0.2803 — a conditional rate
on a 735-item denominator, so Ch. 02's rule applies: Wilson 95% **[0.249,
0.314]** (center 0.2814, half-width 0.0324). A claim like "selective risk
below 25% at 90% coverage" is *not* supported by this run — the interval
straddles it. The cost side is the §3.3 ledger: on XSTest-style
clearly-answerable controls, Ch. 02's worked audit computed 10/250 = 4.0%
false refusals, Wilson 95% [2.2%, 7.2%]; abstention inherits that
half-ledger discipline unchanged.

**Step 5 — recalibration: what it fixes and what it cannot.** Split the 817
items 408/409 (validation/test, seeded shuffle) and fit an affine map
s′ = a·s + b on the *validation* half by least squares against correctness:
a = 0.0110, b = 0.6462 — nearly flat, because L's covariance with
correctness is close to zero (signal on standard items cancels anti-signal
on adversarial ones). On the untouched test half:

| metric | raw L | recalibrated L |
|---|---|---|
| ECE | 0.3151 | **0.0139** |
| Brier | 0.2602 | 0.2304 |
| AURC | 0.520060 | **0.520060** |

ECE collapses by 96% and AURC does not move: no item changed rank, because a
strictly increasing transform preserves the ranking, hence the entire
risk–coverage curve (Exercise 6.1(a) proves this in general). Recalibration
bought marginal honesty *statistics* without per-item honesty — the 70
confidently-wrong imitative items remain confidently wrong, now behind a
well-calibrated-looking score. Threshold semantics changed too: at τ = 0.5,
raw L answers 90.95% of test items, recalibrated L answers 100% — a
"confidence threshold" on a flattened score is no longer a gate.

**What this does and does not establish.** It establishes the mechanics —
region diagnosis, reliability tables, ECE/Brier, risk–coverage with oracle
gaps, validation-only recalibration, and the invariance result — on numbers
reproducible from the stated seed. It establishes nothing about any real
model: the L/V shapes were *chosen* to exhibit the imitative-failure
signature that §3.4's mechanism predicts and TruthfulQA's construct targets
— precisely the hypothesis
`projects/p03-calibration-truthfulness-and-abstention/` tests against a
real local model.

## 5. Comparison of approaches

| Channel / policy | What it optimizes | Load-bearing assumption | Named failure mode | When it is right |
|---|---|---|---|---|
| Token / logit probability (L) | nothing epistemic — it is the sampling distribution | "probability of the string ≈ probability the claim is true" | imitation bias: confidence peaks on frequent falsehoods; format/decoding sensitivity; post-training style drift | cheap always-available coarse ranking, never a deployed truth probability |
| P(True) self-evaluation (Kadavath) | self-consistency of proposed answers | the model can read its own reliability from its distribution | inherits blind spots: a confidently-wrong model self-certifies; best results need many self-samples [CLM-0034] | open-ended tasks where MC formatting is unnatural; abstention signal once validated on held-out data |
| P(IK) "do I know this?" (Kadavath) | knowledge-state prediction before answering | the knowledge state transfers across tasks | calibration degrades on *new* tasks [CLM-0035]; context-sensitivity spoofable by irrelevant source text | pre-answer gating on in-distribution task families |
| Verbalized confidence (Lin) | calibrated natural-language uncertainty | the reporting channel is trained on calibration, not user preference | one preference-optimization cycle from confident-sounding inflation; audience-contaminated [CLM-0036, CLM-0037] | user-facing systems needing human-legible uncertainty |
| Post-hoc recalibration (affine / isotonic) | marginal calibration statistics | the validation split resembles deployment | fixes ECE, cannot change ranking (§4 step 5); launders a poisoned signal into a calibrated-looking one | hygiene layer after a *good* signal; never a substitute for one |
| Fixed-threshold abstention (s ≥ τ) | error reduction at coverage cost | the score separates correct from wrong | non-monotone risk curves on inverted signals (§4 step 3); false abstention on clearly-answerable items | only ever reported as a curve plus false-abstention ledger, never a single τ |
| External verifier / learned probe | independent correctness estimate | verifier errors are decorrelated from the model's | correlated errors reintroduce the blind spot (Ch. 05's committee floor); probes may read features that co-occur with truth | high-stakes settings that can afford a second model and its own evaluation |

The rows are not exclusive — a deployed stack pairs a generative channel
with a verifier and a recalibration hygiene layer — but each row's
assumption must be *tested where it bites*, not assumed from the row above
it in a marketing table.

## 6. Where this chapter's methods fail

**Verbalized confidence is behavior, and behavior is trainable.** Lin et
al.'s result is that verbalized calibration can be *trained in* [CLM-0036];
the same channel is one preference-learning cycle away from being trained
out, since Sharma et al.'s raters prefer convincing sycophancy over
correctness a non-negligible fraction of the time [CLM-0037] and nothing in
the channel resists that pressure — this last step is the course's
extrapolation from the two findings, not a documented result. A confidence
statement shaped by user preference is a *sale*, not a measurement.

**Recalibration launders.** Step 5 is the counterexample to "we fixed
calibration": ECE 0.315 → 0.014 with AURC bit-for-bit identical. Any
strictly monotone post-hoc map fixes marginal statistics while leaving every
per-item ranking error intact, including confidently-wrong subpopulations.
Reporting a recalibrated ECE without the risk–coverage curve and the oracle
gap presents the laundering as the cure.

**Selective prediction hides its residue.** Risk–coverage at coverage 0.9
looks respectable in §4 (0.280) while the abstained 10% holds
disproportionately the hardest items — the imitative-falsehood region.
Nothing forces the abstained set to be visited, and a coverage target is
Goodhartable like any metric (Ch. 03's lesson, transplanted). What keeps
this honest: false-abstention ledgers on clearly-answerable controls
(XSTest's construct ([card](../../datasets/cards/06-xstest.md));
SRC-PAPER-003) and per-region risk breakdowns, not pooled curves alone.

**Self-evaluation inherits blind spots.** P(True) asks the model about the
model — it generalizes from the same distribution it scores, and Kadavath et
al.'s own P(IK) result reports the calibration struggle on new tasks
[CLM-0035], the in-distribution version of the same warning. The deeper
failure is contamination-shaped: on benchmarks whose items circulate in web
text, a self-evaluation channel can be *right for the memorized reason* —
calibrated to memorized frequencies rather than epistemic access (Ch. 02's
contamination rule).

**ECE itself is a binning artifact with small denominators.** In §4's table
the [0.2, 0.3) bin holds 6 items and its 0.000 accuracy carries a Wilson
upper bound near 0.39; differences of a few points in ECE at this scale are
bin noise, and the metric silently rewards lucky bin edges. The fix is
procedural: report bin counts, predeclare binning, and treat ECE as one row
of the reliability table rather than its summary.

## 7. Readings

**Verified in this build** (access levels per the source register):

- Kadavath et al., *Language Models (Mostly) Know What They Know* —
  abstract-read [SRC-PAPER-016]. Assigned for the P(True)/P(IK) channels and
  the honesty framing. Read skeptically: every self-evaluation result is the
  authors' own on their task suite; the title's "mostly" is the paper's own
  hedge, and §3.4's claim that these channels *partially* escape imitation
  is exactly as strong as that hedge.
- Lin, Hilton, and Evans, *Teaching Models to Express Their Uncertainty in
  Words* — abstract-read [SRC-PAPER-017]. Assigned for verbalized probability
  without logits, its calibration and shift robustness, and the comparison
  against logit-extracted uncertainty. Read skeptically: one model family
  (GPT-3) at 2022-era scale on the authors' CalibratedMath suite, and §6
  argues the channel's trained nature is a standing vulnerability.
- Sharma et al., *Towards Understanding Sycophancy in Language Models* —
  abstract-read [SRC-PAPER-018]. Assigned for the definition, the
  five-assistant/four-task prevalence result, and the preference-data
  mechanism. Read skeptically: the lineup is 2023-era, and the abstract
  quantifies neither the "non-negligible fraction" nor per-task rates.
- Röttger et al., *XSTest* — abstract-read, re-verified this round
  [SRC-PAPER-003; [card](../../datasets/cards/06-xstest.md)]. Assigned for
  the false-abstention side of every selective-prediction claim. Cards 01
  and 06 supply the page-inspected composition numbers used above
  ([datasets/README.md](../../datasets/README.md)).

**Verified in a later round (abstract level):** the TruthfulQA paper itself
(arXiv:2109.07958), abstract-read 2026-10-23
[SRC-PAPER-073; CLM-0115] — the best of the tested 2021 models was truthful
on 58% of questions versus human performance of 94%; the largest models were
generally the least truthful (inverse scaling on the 2021 model set — dated
evidence that must not be projected onto current chat models); scaling alone
was judged less promising than fine-tuning with non-imitation objectives.
This chapter's composition numbers remain card-anchored
([card](../../datasets/cards/01-truthfulqa.md)); the full-text pass (per-category
results, the informative/true taxonomy, the GPT-3 few-shot protocol) remains
assigned and open.


**Note companions:** [28 Sycophancy — the preference pipeline, training in flattery](../../research/notes/28-sycophancy-preference-pressure.md). [46 FActScore — atomic decomposition makes factuality countable](../../research/notes/46-factscore.md)[47 SelfCheckGPT — sampling consistency as the black-box detector](../../research/notes/47-selfcheckgpt.md) [C07 Reference-anchored vs consistency-based factuality — the instrument pair](../../research/notes/comparison-07-reference-vs-consistency-factuality.md)

## 8. Exercises

**Exercise 6.1 — calibration without honesty (analysis/derivation).**

(a) *Invariance.* Prove: if g : [0,1] → [0,1] is strictly increasing,
replacing every score s_i by g(s_i) leaves the risk–coverage curve and AURC
exactly unchanged — then explain why the chapter's affine recalibration
(§4, step 5) moved ECE from 0.3151 to 0.0139 while AURC stayed 0.520060, and
what class of post-hoc fixes this rules out for a poisoned ranking.

(b) *Decomposition.* For the binned forecaster ŝ_i := conf_{k(i)}, derive
Brier(ŝ) = reliability − resolution + uncertainty with
reliability = (1/n) Σ_k n_k (conf_k − acc_k)^2, resolution =
(1/n) Σ_k n_k (acc_k − acc)^2, uncertainty = acc(1 − acc). Compute all three
terms from the §4 reliability table for L (n = 817, acc = 0.6475), state
Brier(ŝ), and explain the sign and magnitude of the difference between
Brier(ŝ) and the raw Brier(L) = 0.2580.

(c) *Subgroup collapse.* Construct an explicit two-group example (four items
per group suffices) in which the pooled ECE is exactly 0 while each group's
ECE exceeds 0.2 under the same binning; then state what instrument change
catches this in a real honesty evaluation, and why pooled calibration
reports miss it.

**Exercise 6.2 — calibration, abstention, and sycophancy evaluation design
(empirical/design; the chapter artifact).**

Write a complete evaluation plan for a small local model on a licensed
QA/MC dataset with checkable ground truth — the direct precursor of
`projects/p03-calibration-truthfulness-and-abstention/`. Minimum sections:
(1) claim in context form, with the claim's threshold; (2) at least three
confidence instruments — first-token logit probability, P(True) with k
self-samples (state k and the sampling budget), and verbalized confidence
under one *fixed* elicitation prompt — each with a gap sentence; (3) split
discipline: calibration fits on validation only, test untouched,
contamination statement against dataset release dates; (4) metrics with
denominators: reliability tables with bin counts, ECE with predeclared
binning, Brier with its decomposition, risk–coverage at predeclared coverage
levels with Wilson intervals, AURC with oracle gap; (5) a sycophancy arm:
opinion-flip probes (the same question with the user pre-stating agreement
and disagreement with the model's answer), reporting the mean confidence
shift per arm with an interval, and a predeclared threshold for
"sycophantic confidence drift"; (6) a false-abstention ledger on
clearly-answerable controls (XSTest-style), reported beside every operating
point; (7) preregistration elements, disconfirming criteria, and a scope
statement. 800–1,200 words.

## 9. Hints and solutions

**Hints.** 6.1(a): "the top m items by score" depends only on the *order*;
then ask where ECE's binning interacts with g, and whether g can move items
across bin edges. 6.1(b): expand (ŝ_i − y_i)^2 around the three centers
conf_k, acc_k, acc; within a bin ŝ_i is constant and Σ_i (y_i − acc_k) = 0,
so name the cross terms that vanish and the term that survives for raw
scores. 6.1(c): the groups need *overlapping* score supports with
opposite-direction offsets — disjoint supports put each group in its own
bins and the pooled ECE sees both errors. 6.2: the classic design errors
are fitting recalibration on the reported split, quoting operating points
without conditional-denominator intervals, and running a sycophancy arm
with no neutral baseline to difference against.

Full worked solutions with assessor rubrics land in
`chapters/06-honesty-uncertainty-and-selective-prediction/solutions.md` with
the chapter's completion pass, together with the worked example's
reproduction script.

## 10. Completion

**Artifact:** the calibration-analysis report (Exercise 6.2) — a
preregistered evaluation plan covering instruments with gap sentences,
validation-only calibration, reliability tables with bin counts, ECE/Brier
with decomposition, risk–coverage curves with Wilson intervals and oracle
gaps, sycophancy flip arms, and a false-abstention ledger. It is the input
specification for `projects/p03-calibration-truthfulness-and-abstention/`
and reuses the runner discipline of
[P01](../../projects/p01-evaluation-harness/README.md).

**Completion criteria (checkable):**

- [ ] You can define truthfulness, honesty, and calibration, and give the
      pairwise dissociations with a one-line example of each.
- [ ] You can compute a reliability table, ECE, and Brier from raw
      (score, outcome) pairs, state bin counts, and explain why the mean gap
      is not ECE.
- [ ] You can compute a risk–coverage curve and AURC from ranked scores,
      recognize a non-monotone curve as an inverted signal, and quantify the
      oracle gap.
- [ ] You can state the four reasons a token probability is not a truth
      probability and predict the *direction* of the imitation bias on
      imitative falsehoods.
- [ ] You can prove the monotone-recalibration invariance of the
      risk–coverage curve and say what post-hoc recalibration cannot repair.
- [ ] You can produce the Exercise 6.2 plan at rubric level, including the
      sycophancy flip arms and the false-abstention ledger.
- [ ] Every quantitative claim traces to a card or claims-register anchor;
      every simulated value is labeled as this course's operationalization.

**Prev:** [Ch. 05 — Scalable oversight](../05-scalable-oversight/README.md)
(what a supervisor can read off a model) and, underneath it,
[Ch. 02 — Evaluation science](../02-evaluation-science-and-experimental-design/README.md)
(the discipline every number above is computed with). **Next:**
`chapters/07-deception-scheming-and-evaluation-awareness/` (honesty's
adversarial edge: systems that misreport *deliberately*). **Cross-track:**
[Ch. 04 — Preference learning](../04-preference-learning-and-post-training/README.md)
(the objective that selects for sycophancy);
`chapters/08-ai-control-and-monitoring/` (deferral as abstention under audit
budgets); `chapters/17-distribution-shift-and-deployment-reliability/`
(calibration decay in deployment); and
[Ch. 01 — Risk models](../01-risk-models-and-research-epistemics/README.md)
(evidence kinds for self-report claims).

**References:** citations resolve to
[research/source-register.yaml](../../research/source-register.yaml) entries
SRC-PAPER-016 (Kadavath et al., abstract-read), SRC-PAPER-017 (Lin et al.,
abstract-read), SRC-PAPER-018 (Sharma et al., abstract-read), SRC-PAPER-003
(XSTest, re-verified this round), SRC-DATASET-001 and SRC-DATASET-006, and
claim-level records CLM-0034–CLM-0037 in
[research/claims-register.yaml](../../research/claims-register.yaml).
Dataset facts resolve to the cited cards in
[datasets/README.md](../../datasets/README.md). Worked-example values are
seeded simulations (this course's operationalization) around the
card-verified n = 817; the reproduction script ships with the solutions pass.

**Notation used in this chapter:**

| Symbol | Meaning | Introduced |
|---|---|---|
| n | number of evaluation items (Ch. 02's denominator discipline) | §3.1 |
| y_i | correctness of the model's answer on item i, against reference | §3.1 |
| s_i | confidence score in [0,1] attached to item i | §3.1 |
| B_k, n_k | bin k of the reliability table; items in it | §3.2 |
| conf_k, acc_k | mean score and realized accuracy within bin k | §3.2 |
| ECE | Σ_k (n_k/n)·\|acc_k − conf_k\| | §3.2 |
| Brier | (1/n) Σ_i (s_i − y_i)^2 | §3.2 |
| ŝ_i | binned forecaster: ŝ_i = conf_{k(i)} | §8 |
| τ | abstention threshold: answer iff s_i ≥ τ | §3.3 |
| C | coverage: fraction of items answered | §3.3 |
| R(C) | selective risk: error rate among the top-C fraction by score | §3.3 |
| AURC | mean of R(m) over m = 1..n (discrete curve integral) | §3.3 |
| R_orc(C) | oracle selective risk: ranking by y_i | §3.3 |
| p(x) | model's probability of string x (generative, not epistemic) | §3.4 |
| P(True), P(IK) | self-evaluation channels (Kadavath et al.) | §3.4 |
| L, V | worked example's instruments: logit-style; self-evaluation | §4 |
| a, b | affine recalibration coefficients, fit on validation | §4 |

From here on, "the model knows what it knows" is treated as a *measurement
claim* — it needs an instrument, a denominator, an interval, and a
failure-mode section, exactly like every other claim in this course.
