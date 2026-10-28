# Ch. 09 — Exercises: hints, worked solutions, and rubrics

**Navigate:** [chapter README](README.md) · [course map](../../SYLLABUS.md) · [all chapters](../README.md)

Attempt every exercise before reading past its hint. Rubrics grade the reasoning
trail — which controls fire, which claims get fenced — at least as heavily as
the numbers. All arithmetic was recomputed programmatically with the repo's
Python (script kept in the build tree; every interval below is Wilson at
z = 1.96 per [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
conventions, every restoration fraction from raw logit-difference tables). The
worked example of [README](README.md) §4 is the course's own designed numerical
illustration on the reference model M12; recomputing it here is the point — a
restoration fraction you have not recomputed from its Δ table is a number you
are quoting, not using. Claims-register anchors ([CLM-0046]…[CLM-0050]) match
the README's References section.

## Solution 9.0 — the worked example, recomputed end-to-end

This section exists because the README promised "full grid recomputed in the
solutions." Constants: clean margin `Δ_c = +2.40`; corruption A (embedding
noise on question tokens) `Δ_kA = −1.60`; corruption B (subject substitution)
`Δ_kB = −0.80`. Total effects: `TE_A = 2.40 − (−1.60) = 4.00` logits;
`TE_B = 2.40 − (−0.80) = 3.20` logits. Restoration at a site is
`R(s) = (Δ_p(s) − Δ_k) / (Δ_c − Δ_k)` — the fraction of the
corruption-destroyed margin the patch reinstalls.

### (a) The full 24-site grid (corruption A)

| Layer | attn Δ_p | attn R | MLP Δ_p | MLP R |
|---|---|---|---|---|
| 0 | −1.52 | 0.02 | −1.48 | 0.03 |
| 1 | −1.32 | 0.07 | −1.24 | 0.09 |
| 2 | −1.28 | 0.08 | −1.12 | 0.12 |
| 3 | −0.96 | 0.16 | −0.68 | 0.23 |
| 4 | −0.64 | 0.24 | −0.28 | 0.33 |
| 5 | −0.16 | 0.36 | +0.16 | 0.44 |
| 6 | +0.24 | 0.46 | +0.64 | 0.56 |
| **7** | +0.56 | 0.54 | **+1.04** | **0.66** |
| 8 | +0.32 | 0.48 | +0.88 | 0.62 |
| 9 | +0.72 | 0.58 | +1.28 | 0.72 |
| 10 | +1.20 | 0.70 | +1.64 | 0.81 |
| 11 | +1.76 | 0.84 | +2.00 | 0.90 |

Every R in the representative rows of README §4 Step 2 reproduces exactly
(e.g. layer 7 MLP: `(1.04 − (−1.60)) / 4.00 = 2.64 / 4.00 = 0.66`). The two
readings the grid supports: mid-network MLP sites restore substantially
(layers 5–8, peak 0.66 at layer 7) — the shape the causal-tracing literature
reports for factual recall [CLM-0047] — while layers 10–11 restore *more*
(0.81, 0.90) because by then the answer already sits in the stream: late
sites relay, and patching them re-installs the conclusion. The informative
quantity is where restoration *first climbs*, not where it peaks.

### (b) Position refinement, controls, and replication (implied Δ_p values)

Position refinement at (layer 7, MLP): last subject token `Δ_p = +0.60 →
R = 0.55`; three-token subject span `Δ_p = +0.92 → R = 0.63`; non-subject
tokens `Δ_p = −1.28 → R = 0.08`. The signal rides on the subject tokens —
the subject-token signature of [CLM-0047]. Controls invert the arithmetic:
random-patch donor `R = 0.04` implies `Δ_p = 0.04 × 4.00 + (−1.60) = −1.44`;
matched-topic donor `R = 0.10` implies `Δ_p = −1.20`; both sit indistinguishable
from the corrupted baseline, so the site is question-specific, not merely
active. The corruption-B replication (`R = 0.68`) implies `Δ_p = 0.68 × 3.20 +
(−0.80) = +1.38` under substitution — stability across two corruptions is a
measured check here, not an assumed property (README §6).

### (c) Per-prompt statistics and the rate form

At the winning site: mean `R = 0.66`, SD `0.16`, `n = 100` →
`SE = 0.16/√100 = 0.016`, 95% CI `0.66 ± 1.96 × 0.016 = [0.629, 0.691]`,
reported `[0.63, 0.69]`. As a rate: 69/100 prompts restore at least half the
effect. Wilson: `p̂ = 0.69`, denominator `1 + z²/n = 1.0384`, center
`(0.69 + 0.0192)/1.0384 = 0.683`, half-width `z√(p̂(1−p̂)/n + z²/4n²)/denom =
0.0892`, interval **[0.594, 0.772]**, reported `[0.59, 0.77]`. The interval
excludes both "one or two runaway prompts" (rate floor 0.59) and "uniformly
strong mediation" (ceiling 0.77) — the honest width of a 100-prompt claim.

### (d) The α-sweep and collateral ledger

Scaling the clean-minus-corrupted contribution at the winning site
(contribution at α = 1 is `1.04 − (−1.60) = 2.64`): linear predictions
`Δ(α) = −1.60 + 2.64α` give `−0.28, +1.04, +2.36, +3.68` at α = 0.5, 1.0,
1.5, 2.0. Measured: `−0.26` (tracks), `+1.04` (by construction), `+1.92`
(saturates against 2.36), `+2.30` (degrades against 3.68, with 14/100 prompts
degenerating into repetition loops). Collateral on the 60-item unrelated QA
set: 49/60 = 0.8167 → Wilson [0.701, 0.894], reported [0.70, 0.89];
38/60 = 0.6333 → Wilson [0.507, 0.744], reported [0.51, 0.74]; drop =
(0.8167 − 0.6333) × 100 = **18.3 points** — the intervals overlap by 0.74 −
0.70 = 0.04 only, so the drop is real at the paired-ledger level, not a
margin-of-artifact story.

### (e) Multiplicity

`P(≥1 spurious site) = 1 − 0.95²⁴ = 0.708` (expected false positives
`24 × 0.05 = 1.2`): an uncorrected 24-site grid is more likely than not to
manufacture a "significant" site under the global null. Preselection,
correction, or replication on a second prompt set is not optional polish —
it is the difference between a localization claim and a lottery ticket.

### Common wrong answers — 9.0

- Reading the layer-11 row as "the site of the computation" because it
  restores most (0.90): stored ≠ computed — README §6's trivial-site confound.
- Quoting `R = 0.66` without its contrast: the number is defined *relative to
  corruption A*; under corruption B it is 0.68, and the claim sentence must
  say which (and that both were run).
- Computing the CI as `0.66 ± 1.96 × 0.16` (forgetting √100) — a ±0.31
  interval that silently shrinks the evidence.

### Grading rubric (assessor) — 9.0

| Criterion | Pass requires |
|---|---|
| Grid recomputation | ≥ 20 of 24 R values reproduced exactly from the Δ_p table |
| Late-site reading | Explicitly identifies layers 10–11 as relay/trivial, citing the stored-≠-computed distinction |
| Statistics | Both forms (mean CI and Wilson rate) attempted with correct denominators |
| Controls as inversions | At least one implied Δ_p back-computed from a stated R |
| Multiplicity | 0.708 (or 0.71) reproduced, interpreted as family-wise error |

## Solution 9.1 — auditing a "we found the refusal module" claim

### (a) Restoration fractions and the layer-5 interval (arithmetic)

Constants: `Δ_c = +1.80`, `Δ_k = −2.20`, so `TE = 1.80 − (−2.20) = 4.00`.

| Arm | Δ_p | R = (Δ_p + 2.20)/4.00 |
|---|---|---|
| layer-4 attention | −0.92 | 0.32 |
| layer-5 MLP | +0.64 | **0.71** |
| layer-6 MLP | +0.76 | 0.74 |
| layer-7 MLP | +1.12 | **0.83** |
| random-patch control | −1.96 | 0.06 |

Per-prompt interval at layer-5 MLP: mean 0.71, SD 0.24, n = 40 →
`SE = 0.24/√40 = 0.0379`, 95% CI `0.71 ± 0.0744 = [0.636, 0.784]`, reported
**[0.64, 0.78]**. (The patch-level R = 0.71 and the per-prompt mean agreeing
is a coincidence of the designed numbers, not a check — say so if you noticed.)

### (b) Why "layer-5 is where refusal lives" is unsupported — four problems

1. **The trivial-site confound, live.** Layer-7 MLP restores *more* (0.83 >
   0.71). By the stored-≠-computed rule (README §6), late sites are where the
   answer already sits; a claim that ignores the layer-7 row has not even
   read its own grid. The earliest substantial climb (layer 5) is the
   candidate *computation* site; layer 7 is a relay candidate.
2. **The paraphrase drop is a transfer failure.** 0.71 → 0.44 on paraphrases
   is a 38% relative drop in mediation. The claim's scope shrinks to
   near-exact prompt forms; "where refusal lives" is a claim about the model,
   and their own number says the effect is substantially prompt-bound.
3. **No multiplicity plan.** A single 4-site (at least; likely full-grid)
   scan with no correction, n = 40, CI half-width ±0.07 — the layer-5/layer-6
   difference (0.71 vs 0.74) is *inside* the noise, so "the" site is not even
   uniquely identified among adjacent MLP layers.
4. **"Computes the refusal decision" is a construct overclaim.** What was
   measured is mediation of a refusal *margin* under one corruption
   (embedding noise) on 40 harmful requests. Mediation ≠ decision-making ≠ a
   module; the random-patch control (R = 0.06) buys question-specificity, not
   any of those stronger words.

### (c) The claim they are actually entitled to

> In this 8-layer model, on these 40 harmful-request prompts, layer-5 MLP
> activations at [positions unspecified by the team] mediate a substantial
> share of the refusal margin under embedding-noise corruption
> (R = 0.71, 95% CI [0.64, 0.78]); the mediation is question-specific
> (random-patch control R = 0.06) but transfers only partially to paraphrases
> (R = 0.44), and the adjacent layer-6 (0.74) and later layer-7 (0.83) sites
> restore comparably or more — the latter consistent with relay rather than
> computation. Nothing here establishes a refusal *module*, a *decision*
> locus, or transfer beyond this prompt distribution and corruption.

### (d) Two missing control arms and what each rules out

| Missing arm | What it would rule out |
|---|---|
| Matched-topic donor (different harmful prompt, same register/positions) | "The site is merely active on harmful-topic text" — if it restores under matched-topic donors, the mediation is topic-general, not request-specific |
| Clean-into-clean sanity patch (patch clean activations into the clean run) | "The patching machinery itself perturbs the run" — any measured Δ from this arm is experimenter artifact, and every other number inherits it |
| (also credit: a second corruption, e.g. subject substitution) | Corruption-specificity — mediation defined only by embedding noise is a property of the noise, not the behavior |

### Common wrong answers — 9.1

- Grading the team's claim as *wrong numbers*: the numbers are fine; the
  inference is the failure. (b) must name inference-level problems.
- Defending "layer-5" because the per-prompt mean is 0.71: the layer-6
  interval overlaps almost entirely; "the site" is not identified.
- Writing the entitled claim without the corruption qualifier — dropping
  "under embedding-noise corruption" re-widens the scope silently.

### Grading rubric (assessor) — 9.1

| Criterion | Pass requires |
|---|---|
| (a) arithmetic | All five R values exact; CI [0.64, 0.78] with shown SE |
| (b) critique | ≥ 3 distinct problems, *must* include the layer-7/trivial-site point and the paraphrase-transfer point |
| (c) claim | Fenced: model, prompts, corruption, interval, transfer limits, no module/decision language |
| (d) controls | Two arms, each with the specific confound it rules out (not generic "more controls") |

## Solution 9.2 — a patching protocol for a harmfulness feature (the chapter artifact)

A model solution at rubric depth; 700–1,200 words was the brief, and every
element below maps to a rubric row. XSTest supplies 250 safe prompts across
ten superficial-similarity types plus 200 unsafe contrast prompts
[datasets/cards/06-xstest.md].

**Construct.** The behavioral construct is *harmful-request discrimination*:
the model's internal computation that separates requests it should refuse
from superficially similar requests it should answer. Gap sentence (mandatory):
the logit margin we instrument is a proxy for the refusal *policy* we care
about — a model can refuse for compliance reasons with no harmfulness
discrimination, and the protocol cannot see the difference. XSTest exists
precisely because surface features fail
[datasets/cards/06-xstest.md]; the construct inherits that failure mode.

**Metric.** Δ = logit(refusal-continuation) − logit(answer-continuation),
scored on the designated continuation pair per prompt. A margin, not a rate:
per-prompt continuous readout gives the patching experiment statistical
power a binary refusal rate cannot (Ch. 02 §5), and the paired clean/corrupt
ledger needs per-prompt values.

**Arms.**

1. *Clean*: original prompts, per-type stratified sampling (25 safe per
   XSTest type, matched unsafe), pinned by index list before any run.
2. *Corrupted (the contrast that defines scope)*: safety-irrelevant
   perturbation that destroys the discriminative margin — paraphrase the
   request's *surface* while preserving the superficial trigger type. This
   family is the scope-defining choice: a site found under
   surface-paraphrase corruption mediates discrimination *against surface
   variation*, not against, e.g., role-play framing — the claim sentence
   must say so.
3. *Random-patch donor*: unrelated prompts — rules out site-activity.
4. *Matched-type donor*: same XSTest type, different prompt — rules out
   type-general activity; the harmfulness computation must be
   request-specific.

**Grid and multiplicity.** All layers × {attn, MLP} × subject vs request
tokens, *pre-registered* site list (annotation before runs), Holm–Bonferroni
across the site family; primary site preselected by first-climb heuristic
(earliest layer where lower-confidence bound on R exceeds 0.2), peak-R
reported only as relay diagnostic (Solution 9.0's lesson).

**Statistics.** Per-prompt R with mean CI and Wilson rate form (≥ half
restoration), n per stratum ≥ 25 so per-type Wilson intervals are quotable;
both corruption arms reported; paired ledger per Ch. 02.

**Off-distribution checks.** Transfer: paraphrase set (same prompts),
cross-type held-out (novel XSTest types), α-sweep at the winning site with a
collateral ledger (accuracy on the safe-prompt answering task — collateral
*is* the product metric here: over-steering harms benign answering, the
XSTest core finding [datasets/cards/06-xstest.md]).

**Stopping rules / disconfirming criteria (pre-stated).** Stop the grid
after one pre-registered pass plus one replication on a second index list.
Disconfirming: Wilson lower bound on the rate form < 0.5 at the primary
site; transfer-to-paraphrase R < 0.4; matched-type control R within 0.1 of
the primary site. Any of these ⇒ the localization claim is not written.

**The claim sentence if everything passes.**

> In [model], on [n] XSTest-modeled harmful-vs-safe request pairs, layer-[L]
> [block] activations at the request tokens mediate a substantial share of
> the refusal margin under surface-paraphrase corruption
> (R = [·], 95% CI [·]; rate form [·]), replicate under [second corruption],
> are absent under random-patch ([·]) and matched-type ([·]) controls, and
> transfer to paraphrases ([·]) and held-out types ([·]); collateral cost at
> 1.5× amplification is [accuracy drop] with interval [·]. The claim covers
> this model, these prompt distributions, and this corruption contrast.

**Two ways it misleads anyway.** (1) *Redundancy under single-site patching*:
a duplicate harmfulness computation elsewhere masks the site's causal role
until it is broken (ablation-with-backup, [CLM-0048]) — single-site R can
read low while the behavior depends on the site. (2) *The margin is not the
policy*: if the model's refusal behavior is driven by compliance tuning
rather than harmfulness discrimination, the protocol perfectly localizes a
computation that is not the safety-relevant one — the construct gap again,
unmeasurable inside this design.

### Common wrong answers — 9.2

- A protocol whose corruption is "make the prompt harmless": that contrast
  localizes *harmfulness content detection*, a different (legitimate but
  unnamed) construct — the claim's scope sentence must name the contrast.
- Binomial rate-only statistics: loses per-prompt power and the paired
  ledger; the margin is the instrument.
- Omitting the collateral ledger from the α-sweep: the most safety-relevant
  number in the design (safe-prompt answering degradation) goes unmeasured.

### Grading rubric (assessor) — 9.2

| Criterion | Pass requires |
|---|---|
| Construct + gap | Construct stated in one sentence; gap sentence present and honest |
| Arms | ≥ 2 control donors with the specific confound each rules out; corruption family named as scope-defining |
| Multiplicity | Pre-registered sites + explicit correction; first-climb vs peak-R distinction present |
| Statistics | Per-prompt CI *and* rate form; denominators stated; both corruptions reported |
| Off-distribution | Paraphrase + cross-type transfer AND α-sweep with collateral ledger |
| Claim discipline | The model claim sentence is fully fenced (model, prompts, corruption, intervals, transfer limits) |
| Self-critique | Two *protocol-level* misleading modes, not generic "could be wrong" |

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **CS 2881**, [lecture-10-mechanistic-interpretability](../../courses/boaz-barak-cs2881/lecture-10-mechanistic-interpretability.md) — watch before working the residual-stream exercises.
