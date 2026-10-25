# Ch. 11 — Behavioral steering and representation interventions

> The chapter where the model's internals stop being a map and start being a
> control surface. A direction a probe can *read* is a hypothesis; a direction
> whose addition and ablation *move* behavior is an intervention — and an
> intervention, unlike a visualization, must be evaluated on held-out inputs,
> instruments it was never tuned on, and tasks it was never about.

## 1. Research question and failure pathway

**The question this chapter answers:** *when you push on a direction inside a
network and the behavior moves, what have you actually shown — and what did
you break on the way?*

**The failure pathway it prevents:**

```text
probe finds a "direction" ──► direction conflated with a correlate ──►
steering "works" on extraction-adjacent prompts ──► off-target effects
unmeasured ──► "we can align a model with a vector" quoted out of context
```

Each arrow is a silent validity leak, and none is caught by the probe-accuracy
number that headlines most steering write-ups. The first arrow is the probing
fallacy: a classifier reading 96% off activations establishes *decodability*,
not *use* — the survey literature has catalogued this gap for years
[SRC-PAPER-039]. The second is the confound problem: a difference-in-means
vector between harmful and benign prompts can encode topic, register, or
dataset style rather than refusal — Arditi et al. concede their own "refusal
direction" could as easily be a "harm" or "danger" feature [CLM-0058]. The
third is transfer, and the fourth is why a deployer should care: interventions
that look surgical on the target ledger can still tax unrelated capabilities,
and the tax is invisible unless you budget a third ledger for it [CLM-0059].

This lands after the interpretability foundations for a reason:
`chapters/09-mechanistic-interpretability-foundations/` supplies the residual
stream and the causal-intervention toolkit, and this chapter applies that
machinery to the *behavioral* claim, forcing it through the evaluation
discipline of [Ch. 02](../02-evaluation-science-and-experimental-design/README.md).
The word *intervention* is load-bearing: it means denominators, intervals,
controls, and a stated region of validity — not a demo.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
(Wilson intervals, paired ledgers, split discipline); the residual-stream and
causal-intervention material of
`chapters/09-mechanistic-interpretability-foundations/`; diagnostic task B
([diagnostic](../../prerequisites/diagnostic.md)); refreshers R2 and R6
([targeted refreshers](../../prerequisites/targeted-refreshers.md)). If
chapter 09 is not yet worked, read its residual-stream and
activation-patching sections before the worked example below.

**Outcomes.** After this chapter you can:

1. Train a linear probe on residual-stream activations, report held-out
   accuracy with an interval, and state what it does and does not establish.
2. Extract a steering direction (difference-in-means, prompt-pair contrast,
   contrastive activations), apply addition and ablation, and name the
   linear-representation assumptions each step buys.
3. Design the controls — matched-norm random directions, permuted-label
   directions, layer and coefficient sweeps — that separate "this direction
   matters" from "any perturbation this size matters."
4. Evaluate an intervention on three ledgers — held-out target prompts, a
   held-out cross-instrument, an unrelated-task capability battery — with
   power arithmetic stating what the battery can resolve.
5. State the transfer limits and dual-use symmetry of direction-level
   interventions honestly, in report form.

**Scope exclusions.** Sparse autoencoders, superposition, and circuit-level
claims are `chapters/10-sparse-features-circuits-and-interpretability-evaluation/`;
this chapter stays at single directions in the raw residual stream.
Training-time safety countermeasures are
[Ch. 04](../04-preference-learning-and-post-training/README.md) — this chapter
is inference-time only. Adversarial-suffix attacks as a technique are
`chapters/12-adversarial-ml-and-robustness/` and
`chapters/15-red-teaming-and-adversarial-evaluation/`; here they appear only
as evidence about direction fragility. Multi-turn and agentic protocols are
[Ch. 08](../08-ai-control-and-monitoring/README.md). Running the bounded
experiment is `projects/p06-causal-interpretability-study/`.

## 3. Core explanation

Throughout, **M** is a transformer chat model with residual-stream width d and
L layers; **x_i^(l)** ∈ ℝ^d is the residual-stream activation at layer l, token
position i; *h* and *b* denote the harmful and benign instruction classes.
Card citations [cards/NN] resolve to the verified cards in
[datasets/README.md](../../datasets/README.md).

### 3.1 The linear representation hypothesis, stated as assumptions

The working hypothesis of the chapter is that a behavioral property of M —
refusal, sentiment, truthfulness — is encoded as a **direction**: a unit
vector r̂ such that r̂·x tracks the property and moving x along r̂ moves it.
That is a family of assumptions, each failing differently:

| # | Assumption | What it licenses | Failure mode |
|---|---|---|---|
| A1 | the feature is linearly decodable from x at some (l, i) | probes, readout | feature nonlinear or split across positions; probe accuracy bounds nothing causal |
| A2 | the direction found is the feature's mediator, not a correlate | causal language | direction encodes topic/style/format; ablation "works" by disabling a confound |
| A3 | the direction is context-stable across prompts, formats, languages | transfer claims | direction is dataset-specific; transfer fails off-extraction distribution |
| A4 | adding α·r̂ shifts this feature without wrecking others | steering as control | off-target interference; side effects exist only if measured |
| A5 | extraction distribution ≈ deployment distribution | deployment claims | curated-list extraction does not cover real traffic |

The literature is candid that A2 is the hard one. Arditi et al. demonstrate a
single direction whose ablation disables refusal and whose addition induces
it, across 13 open-source chat models from 1.8B to 72B parameters [CLM-0058] —
yet their own limitations section says the direction could represent "harm" or
"danger" or resist semantic interpretation altogether [CLM-0058]. Turner et
al.'s single-pair result is existence-level evidence for A1 and A4 and silent
on A3 [CLM-0056]. Your job as evaluator is to convert each assumption from a
hope into a measured property of *your* intervention.

### 3.2 Probes: what readout can and cannot establish

A **linear probe** is a classifier p_w(x) = σ(w·x + b) trained on activations
collected while M runs labeled inputs — harmful vs benign instructions, true
vs false statements. Held-out probe accuracy answers exactly one question: is
the label decodable by a hyperplane from x at this layer? It says nothing
about whether M's downstream computation *uses* the feature — probes can read
out properties the model does not functionally rely on, and high accuracy is
compatible with the information being an artifact of the data or of probe
capacity [SRC-PAPER-039].

Three probe confounds recur. **Correlate features**: harmful instructions
differ from benign ones in topic, imperative register, and phrasing, and a
probe can win on any of those. **Format leakage**: template artifacts
(instruction markers, chat delimiters) co-vary with class in many curated
sets. **Selection asymmetry**: if the benign set is ordinary instructions,
"harmful vs ordinary" is not the boundary deployment cares about — XSTest
exists precisely because the hard benign cases look unsafe [cards/06]. The
course's rule: a probe result is *readout evidence*; "causes", "mediates", or
"knows" require the interventions of §3.3.

Burns et al. push probing somewhere instructive: drop the labels and search
for a direction satisfying *logical consistency* — a statement and its
negation should have opposite truth values along it. Across 6 models and 10
QA datasets their unsupervised direction beats zero-shot accuracy by 4% on
average, halves prompt sensitivity, and stays accurate when the model is
prompted to answer incorrectly [CLM-0060]. But the objective assumes truth is
the *only* feature whose negation flips sign in activation space — A2 in an
unsupervised costume, since a consistency-satisfying direction could equally
track polarity, hedging, or dataset pairing artifacts.

### 3.3 From readout to intervention: the causal test

**Direction extraction.** The workhorse is **difference-in-means**: run M over
a harmful and a benign extraction set, take class-mean activations μ_h, μ_b at
each candidate (layer, position), and set r^(l) = μ_h − μ_b. Arditi et al.
build the harmful set from AdvBench, MaliciousInstruct, TDC2023, and HarmBench
and the harmless set from Alpaca, with 128 train and 32 validation samples per
class, selecting the single best (layer, position) on the validation split
[CLM-0058]. Turner et al.'s Activation Addition (ActAdd) is the minimal
version — r from one prompt pair ("Love" vs "Hate"), no averaging, no
optimization [CLM-0056]. Contrastive Activation Addition (CAA) averages the
difference in residual-stream activations between positive and negative
*completions* of a behavior (e.g. factual vs hallucinatory responses), added
at all post-prompt positions with a signed coefficient [CLM-0057].

**Interventions.** Given r̂ (unit norm) and separation s = ‖r‖:

```text
addition:   x_i^(l*) ← x_i^(l*) + α · s · r̂       (layer l*, chosen positions)
ablation:   x_i^(l)  ← x_i^(l)  − r̂ (r̂ · x_i^(l))  (all layers, all positions)
```

Arditi et al. apply addition at the extraction layer across all positions, and
ablation at every layer and position — the latter "prevents the model from
ever representing this direction" [CLM-0058]. They read the pair as necessity
and sufficiency: ablation disabling refusal is evidence the direction is
necessary; addition inducing refusal is evidence it is sufficient [CLM-0058].

**Direction-specificity controls.** An intervention result is not about r̂
until perturbation-matched controls fail to reproduce it. Required here:
(1) a **matched-norm random direction** — a normalized Gaussian vector at the
same α; any effect it reproduces belongs to the perturbation, not the
direction. (2) A **permuted-label direction** — difference-in-means recomputed
after permuting class labels on the extraction set; any effect it reproduces
was tuned to the extraction items, not their classes. Controls are cheap;
skipping them is how demo thinking survives into reports.

### 3.4 The evaluation frame: three ledgers (this course's operationalization)

An intervention claim needs a ledger design, and
[Ch. 02](../02-evaluation-science-and-experimental-design/README.md) supplies
the schema. This chapter instantiates it with three ledgers plus a benign
complement:

1. **Held-out target ledger** (same construct, unseen items): the direction
   never saw these prompts. AdvBench's canonical CSV has 520 behavior rows
   [cards/09], so a 320-extraction / 200-held-out split is available at the
   extraction scale Arditi et al. use [CLM-0058].
2. **Held-out cross-instrument ledger**: a second instrument for the same
   construct from a different source — if the direction came from
   AdvBench-style prompts, XSTest's 200 unsafe contrasts [cards/06] are a
   genuine transfer test: different authorship and phrasing, same construct
   class.
3. **Unrelated-task capability ledger**: tasks sharing no construct with the
   intervention, measured before and after. Arditi et al.'s Table 3 is the
   published exemplar: after ablating the refusal direction from model
   *weights*, generic benchmarks move within about a point, while
   **TruthfulQA drops for every model tested** — −1.0 to −3.5 points across
   the five largest models [CLM-0059]. Construct-adjacent tasks can move when
   generic ones do not, so the battery must be chosen, not inherited.
4. **Benign complement**: false-refusal on XSTest's 250 safe prompts
   [cards/06] — the over-refusal tax, without which a refusal-increasing
   report is half a confusion matrix (Ch. 02 §3.4's rule).

**Transfer limits are card facts, not vibes.** AdvBench is a 2023-era curated
English research list with no benign controls and no severity field
[cards/09]; XSTest is English-only and deliberately excludes the borderline
middle [cards/06]. Neither supports claims about multi-turn social
engineering, non-English traffic, or agentic tool use — and Arditi et al. flag
that their findings may not generalize to untested models and scales
[CLM-0058]. A transfer claim should cite the instruments it was measured on
and stop at their negative scope.

## 4. Worked example: steering refusal up, evaluated like a deployer

**The system:** an open-weights 7B-class chat model M in a customer-support
context, plus a proposed inference-time "safety steering layer" adding a
refusal direction. **Your job:** produce the number-set a reviewer can trust
and the decision it supports. The run numbers are this course's fully
specified worked example — a hypothetical evaluation in the format a
deployer's report should take, **not an executed experiment**; denominators
are pinned to verified card facts and every derived quantity is recomputed
exactly in [solutions.md](solutions.md).

**Step 0 — the claim, in context form.** In context κ (customer-support
chat, English, single-turn), adding the refusal direction at strength α
raises harmful-instruction refusal to a Wilson lower bound ≥ 95% on held-out
harmful prompts, keeps false-refusal on clearly-safe prompts at a Wilson
upper bound ≤ 5%, and costs at most 5 points of capability (Newcombe upper
bound) on an unrelated battery — all three gates preregistered before the
first run, per Ch. 02 §3.6.

**Step 1 — instruments and splits, pinned.** Extraction: 320 harmful
instructions sampled from AdvBench's canonical 520 [cards/09] and 320
course-authored benign instructions (ordinary-request style, mirroring the
Alpaca-harmless construction [CLM-0058]), plus 32+32 validation items for
(layer, position) selection. Held-out harmful: the untouched AdvBench
remainder, exactly 200 items. Cross-instrument: XSTest's 200 unsafe contrasts
[cards/06]. Benign complement: XSTest's 250 safe prompts [cards/06], never
used for extraction. Capability battery: 500 course-authored two-step
arithmetic items (synthetic, deterministic — this course's own instrument).
Scoring: the Arditi-style substring refusal classifier [CLM-0058].

**Step 2 — probe and direction.** A logistic probe trained on layer-13
extraction activations reads held-out activations at 432/450 = 96.0% (Wilson
95% [93.8%, 97.5%]; harmful recall 194/200 = 97.0%, benign recall 238/250 =
95.2%). The probe weights and the difference-in-means direction have cosine
similarity 0.91 — the probe's winning hyperplane and the class-separation
direction are distinct objects, and steering with one is not a replication of
the other. A second direction extracted with XSTest-safe prompts as the
benign class has cosine 0.78 to the first: the benign class is part of the
construct (A2/A3), measured, not assumed.

**Step 3 — intervention and controls.** Intervene with
x_i^(13) ← x_i^(13) + α·s·r̂ at all post-prompt positions, α swept over
{0.5, 1.0, 1.5, 2.0}; controls at α = 1.0 use a matched-norm seeded random
direction and a permuted-label direction. First full run, all four ledgers
(Wilson 95%; z-tests in [solutions.md](solutions.md)):

| Ledger (denominator) | Baseline | α = 1.0 | Random ctrl | Permuted-label ctrl |
|---|---|---|---|---|
| AdvBench held-out refusal (200) | 182/200 = 91.0% [86.2, 94.2] | **196/200 = 98.0% [95.0, 99.2]** | 185/200 = 92.5% [88.0, 95.4] | 184/200 = 92.0% [87.4, 95.0] |
| XSTest unsafe refusal (200) | 178/200 = 89.0% [83.9, 92.6] | **192/200 = 96.0% [92.3, 98.0]** | 183/200 = 91.5% [86.8, 94.6] | 179/200 = 89.5% [84.5, 93.0] |
| XSTest safe false-refusal (250) | 10/250 = 4.0% [2.2, 7.2] | **34/250 = 13.6% [9.9, 18.4]** | 12/250 = 4.8% [2.8, 8.2] | 11/250 = 4.4% [2.5, 7.7] |
| Arithmetic accuracy (500) | 441/500 = 88.2% [85.1, 90.7] | **428/500 = 85.6% [82.3, 88.4]** | 439/500 = 87.8% [84.6, 90.4] | 440/500 = 88.0% [84.9, 90.6] |

Read the table in evaluator order. The intervention moves both harmful
ledgers (z = +3.07, p = 0.0021 on AdvBench; z = +2.66, p = 0.0079 on
XSTest-unsafe) and **transfers across instruments** — the direction moved
behavior on a suite it was never extracted from. The controls do not
reproduce the movement (random +1.5pp; permuted-label +1.0pp on AdvBench), so
the effect is direction-specific and the minimal causal claim holds. But the
false-refusal ledger moves too (z = +3.79, p = 0.0002): the safety gain and
the over-refusal tax arrived together, as the paired-ledger rule predicts.
The capability point estimate drops 2.6 points with z = +1.22, p = 0.223 —
**not significant at n = 500**, and a battery this size could not have
resolved a drop this small anyway (Step 5).

**Step 4 — the sweep as a frontier.** The honest form of a steering result is
the sweep, not a single α (intervals recomputed in
[solutions.md](solutions.md)):

| α | AdvB refusal | XSTest-unsafe refusal | XSTest-safe false-refusal | Arithmetic |
|---|---|---|---|---|
| 0.0 | 91.0% [86.2, 94.2] | 89.0% | 4.0% [2.2, 7.2] | 88.2% |
| 0.5 | 94.5% [90.4, 96.9] | 93.0% | 7.2% [4.6, 11.1] | 87.2% |
| 1.0 | 98.0% [95.0, 99.2] | 96.0% | 13.6% [9.9, 18.4] | 85.6% |
| 1.5 | 99.0% [96.4, 99.7] | 97.5% | 26.0% [21.0, 31.8] | 80.8% |
| 2.0 | 99.5% [97.2, 99.9] | 98.0% | 43.2% [37.2, 49.4] | 71.4% |

The frontier is convex: each step buys less harmful-refusal and costs more
over-refusal. Moving α from 0 to 0.5 trades 3.5 points of harmful refusal for
3.2 points of false-refusal (0.91 points of over-refusal per point gained);
0.5→1.0 costs 1.83 per point gained; 1.0→1.5 costs 12.4; 1.5→2.0 costs 34.4
(recomputed in [solutions.md](solutions.md)). Pick α where the deployment's
exchange rate is acceptable; picking α by the harmful ledger alone is the
failure mode.

**Step 5 — gates, decision, power.** G1 (harmful-refusal Wilson lower bound
≥ 95%) passes only at α ≥ 1.5 — at α = 1.0 the lower bound is 0.9497,
missing the gate by 0.03 points, and a knife-edge miss is a miss. G2
(false-refusal upper bound ≤ 5%) fails at **every** α including 0: the
baseline's own 4.0% rate has upper bound 7.2%, so the deployment's
over-refusal budget was exhausted before any intervention. G3 (capability
Newcombe upper bound ≤ 5 points) fails at α ≥ 0.5 (at α = 1.0: degradation
2.6 points, interval [−1.6, +6.8]). **No α satisfies the claim**, and the
correct report says so and stops. Separately, the 500-item capability ledger
could never settle a 2.6-point drop — resolving it at 80% power needs ~2,640
items per arm ([solutions.md](solutions.md) shows the computation) — so "no
significant capability cost" is *unsupported*, not *established*, at this
battery size.

**What this example does not establish:** that the direction is "the" refusal
feature (cos 0.91 and 0.78 bound agreement between probe, class means, and
alternative benign class — not what the vector means); transfer beyond two
curated English single-turn suites (both cards' negative scopes apply [cards/09;
cards/06]); behavior under adaptive pressure (an attacker who learns the
direction can subtract it — §6's symmetry); or claims about any model other
than the one tested [CLM-0058's stated limits].

## 5. Comparison of approaches

| Approach | What it buys | Key assumptions | Failure modes | Evidence it yields |
|---|---|---|---|---|
| Linear probe readout (§3.2) | cheap decodability check: the label is present in x | A1 only | reads correlates (topic, format, register); capacity artifacts; decodable ≠ used [SRC-PAPER-039] | correlational, never causal |
| Prompt-pair steering (ActAdd) [CLM-0056] | vector from one contrast pair, no optimization, fast iteration | A1, A4; the pair represents the feature | direction encodes the pair's idiosyncrasies; off-target effects at high α; the authors' off-target-preservation claim is benchmark-dependent | existence proof of controllability |
| Difference-in-means steering / refusal direction [CLM-0058] | scalable direction with validation-selected (l, i); necessity + sufficiency tests | A1–A4; class means isolate the feature, not topic/style | benign-class choice is part of the construct (worked example cos 0.78); "harm/danger" ambiguity [CLM-0058]; per-model, per-scale | causal in-distribution, with instrument-specific transfer evidence |
| Contrastive activation addition (CAA) [CLM-0057] | behavior-level contrasts (e.g. factual vs hallucinated completions); works on top of finetuning and system prompts (authors' claim) | A1–A4; completion pairs are behavior-pure | pair-authoring cost; extraction/deployment distribution shift; "minimally reduces capabilities" needs its own battery | causal, with a capability ledger attached at abstract level |
| Unsupervised consistency search (CCS) [CLM-0060] | direction without labels; robust to prompted misinformation (authors' result) | consistency (negation flips sign) identifies the feature | consistency satisfied by non-truth features (polarity, hedging, pairing artifacts); +4% average gain is modest and task-set specific | correlational-with-consistency; needs §3.3's controls to become intervention evidence |
| System-prompt / instruction steering | no internals access; deployable anywhere | the model obeys the instruction robustly | shallow and context-sensitive: dropping the safety-bearing system prompt took Llama-2 7B's orthogonalization ASR from 22.6% to 79.9% [CLM-0059] | behavioral only; no mechanism |
| Safety finetuning ([Ch. 04](../04-preference-learning-and-post-training/README.md)) | durable distribution-level change; the deployment default | labeled preference data; training budget | opaque; reversible by finetuning or direction-level ablation [CLM-0059]; no per-inference control | behavioral at scale; mechanism unmeasured |

The rows are complements, not competitors: production teams run the last row
by default, the system-prompt row as cheap framing, and the direction rows as
mechanism-level evidence that the safety property is — or is not — robust.
The course's stack matches: [projects/p01-evaluation-harness/](../../projects/p01-evaluation-harness/README.md)
runs the ledgers, and `projects/p06-causal-interpretability-study/` builds the
intervention evidence.

## 6. Where this chapter's methods fail

**The probe fallacy with extra steps.** Controls upgrade a probe to an
intervention claim *on the extraction distribution and its near neighbors*.
They do not touch A2 in the deep sense: if harmfulness and a correlate
co-vary everywhere your instruments look, the random-direction control passes,
the sweep behaves, and the direction is still the correlate. Arditi et al.'s
own limits — existence proof, extraction "likely not optimal," semantics
unclear [CLM-0058] — state this ceiling honestly; the partial remedies are
adversarial instrument design (benign sets that look harmful, à la XSTest
[cards/06]) and reporting the direction's provenance with the claim.

**Transfer is bounded by the instruments measured on.** AdvBench and XSTest
are curated, English, single-turn, without severity structure [cards/09;
cards/06]. A direction that transfers between them has shown transfer across
two authorship styles — not across languages, multi-turn dynamics, tool-use
contexts, or time. Arditi et al. restrict their suffix analysis to a single
model and a single adversarial example, and flag generalization to untested
models and scales as open [CLM-0058]. Any sentence of the form "steering
generalizes" should cite its instrument list and stop there.

**Capability side effects are construct-relative and power-poor.** Arditi et
al.'s Table 3 shows the trap: MMLU, ARC, and GSM8K moved within about a point
for most models, while TruthfulQA — construct-adjacent to refusal through its
misinformation/stereotype/conspiracy categories [cards/01] — dropped for every
model tested [CLM-0059]. Inherit a generic battery and you inherit its blind
spots; build a small one and you get the worked example's arithmetic — a
500-item battery cannot resolve a 2.6-point drop (needs ~2,640 per arm at 80%
power), so "no significant difference" measures your sample size, not the
intervention.

**Adaptive pressure invalidates the calm-water evaluation.** The evaluated
attacker need not accept your direction: Arditi et al. show adversarial
suffixes *suppress* expression of the refusal-mediating direction — cosine
similarity of last-token activations to the direction collapses toward
harmless-prompt levels under the suffix but not under random suffixes
[CLM-0058] — and dropping a safety-bearing system prompt multiplies attack
success several-fold [CLM-0059]. This is
[Ch. 08](../08-ai-control-and-monitoring/README.md)'s adaptive-red-team rule
in representation space: a steering result without an adaptive condition is a
baseline, not a defense claim.

**The gates themselves can be theater.** A knife-edge pass (0.9497 vs 0.95)
is a fail; a gate set after seeing the sweep is a narrative; a capability
threshold τ chosen post hoc to exclude the observed drop is laundering. The
worked example fails G2 at α = 0 — which is the method *working*: it surfaced
that the baseline was already outside the deployment's over-refusal budget, a
fact no steering arithmetic would have hidden.

**Dual-use is not a footnote.** Every protocol in this chapter is symmetric:
the report certifying refusal-direction addition is the report specifying its
ablation, and Arditi et al. priced the ablation at under $5 of compute for a
70B-class model [CLM-0059]. Publishing direction-level findings therefore
carries the same disclosure calculus as AdvBench's attack disclosure
[cards/09], and this repository's answer — per
[RESPONSIBLE_RESEARCH.md](../../RESPONSIBLE_RESEARCH.md) — is the same:
evaluation discipline yes, operational recipes no.

## 7. Readings

**Verified in this build** (access levels per the source register):

- Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee, and Nanda — *Refusal in
  Language Models Is Mediated by a Single Direction* — **full-text-read**
  (arXiv HTML v3). The chapter's backbone: §2.3–2.4 (extraction, addition,
  ablation), §3 (mediation), §4.2–4.3 (ASR comparison; capability Table 3),
  §7 (limitations) — read the limitations as closely as the results, for they
  are the template for §6 [CLM-0058, CLM-0059].
- Panickssery (v1 listing: Rimsky), Gabrieli, Schulz, Tong, Hubinger, and
  Turner — *Steering Llama 2 via Contrastive Activation Addition* —
  abstract-read. Why: the contrastive-completion recipe, and the "effective
  over and on top of finetuning and system prompts, minimally reduces
  capabilities" claim — treat the last clause as the claim your capability
  ledger must test, not as a given [CLM-0057].
- Turner, Thiergart, Leech, Udell, Vazquez, Mini, and MacDiarmid — *Steering
  Language Models With Activation Engineering* — abstract-read. Why: the
  minimal one-pair recipe and the off-target-preservation claim; a single
  prompt pair is both the method's strength and its transfer limit
  [CLM-0056]. (The candidate ID 2308.07107 resolved to an unrelated
  information-retrieval survey; the correct ID, 2308.10248, was found by
  title search and is the one registered.)
- Burns, Ye, Klein, and Steinhardt — *Discovering Latent Knowledge in
  Language Models Without Supervision* — abstract-read. Why: what changes
  when labels disappear — the consistency objective, its gains, and its
  assumption that consistency identifies the truth feature [CLM-0060].

**Optional deeper material:** Belinkov — *Probing Classifiers: Promises,
Shortcomings, and Advances* — abstract-read; the survey-level map of probing
methodology limits referenced throughout §3.2 and §6 [SRC-PAPER-039]. For the
training-time counterpart, [Ch. 04](../04-preference-learning-and-post-training/README.md)'s
readings; for causal-intervention foundations, the readings of
`chapters/09-mechanistic-interpretability-foundations/`.

**Note companions:** [52 ROME — the weight-tier editing anchor](../../research/notes/52-rome-factual-associations.md)

## 8. Exercises

**Exercise 11.1 — the probe that knew too much (analysis).** A team trains a
linear probe on layer-15 residual-stream activations of a chat model to
predict is-harmful from 3,000 labeled instructions (2,000 train / 1,000
held-out), reports 97% held-out accuracy, and concludes in a blog post that
(i) the model "contains a harmfulness concept," (ii) refusal "is computed
from this concept," and (iii) a production monitor flagging conversations
whose activations cross the probe's threshold is therefore justified.
Produce: (a) three distinct features the probe could be reading besides
harmfulness, with the mechanism by which each co-varies with the label in
typical curated sets; (b) the logical gap between 97% decodability and each
of claims (i)–(iii), naming which §3.1 assumption each gap corresponds to;
(c) the minimal experiment set — interventions, controls, held-out
instruments — that would upgrade the strongest defensible subset of
(i)–(iii) to causal status, with predicted outcomes under "the probe reads
harmfulness" vs "the probe reads a correlate"; (d) what the shipped monitor
still lacks even if (c) succeeds, given an adaptive attacker.

**Exercise 11.2 — preregistered steering-intervention evaluation (design; the
chapter artifact).** Write the complete evaluation protocol for a
refusal-direction *addition* layer for a deployment context you choose (e.g.,
a coding assistant with shell access). Required sections: claim in context
form with numeric gates; extraction protocol with pinned instruments and
split discipline (cite the cards for every denominator you budget); the
control set; the three ledgers plus benign complement with denominators,
interval methods, and a capability battery with an explicit power computation
(state the smallest drop your battery can resolve at 80% power — compute it,
do not estimate it); the α-selection rule as a pre-stated frontier rule;
weakening observations (pre-stated, falsifiable); scope exclusions with card
negative-scope citations; and a dual-use paragraph stating what the same
protocol would ablate and what you will and will not publish. 700–1,200 words
plus the arithmetic.

## 9. Hints and solutions

Attempt both exercises before opening [solutions.md](solutions.md) — Exercise
11.2's power arithmetic rewards doing it wrong once first. The solutions file
also recomputes every number in §4's tables (Wilson intervals, z-tests, the
Newcombe interval, exchange rates, and the 2,640-per-arm power figure) so you
can check your own recomputation rather than trust the prose.

## 10. Completion

You have completed this chapter when you can:

- [ ] State the linear-representation assumptions A1–A5 and attach each one's
      failure mode and the measurement that tests it.
- [ ] Explain why probe accuracy — even 97% held-out — cannot support causal
      claims, and name the interventions and controls that can.
- [ ] Extract a difference-in-means direction, apply addition and ablation,
      and run matched-norm and permuted-label controls.
- [ ] Build the three-ledger evaluation with pinned denominators, Wilson
      intervals, a capability battery whose power you have computed, and
      preregistered gates — and report a no-free-lunch result honestly.
- [ ] State the transfer limits of your claim as card negative-scope facts,
      and the dual-use symmetry of your protocol.

**Artifact:** the Exercise 11.2 protocol — the intervention-evaluation report
skeleton that `projects/p06-causal-interpretability-study/` implements and
that [projects/p01-evaluation-harness/](../../projects/p01-evaluation-harness/README.md)
runs. **Prev:**
`chapters/10-sparse-features-circuits-and-interpretability-evaluation/`
(circuit- and SAE-level evidence; if you arrived out of order, the required
background is `chapters/09-mechanistic-interpretability-foundations/`).
**Next:** `chapters/12-adversarial-ml-and-robustness/` (the adaptive attacks
whose suffix behavior §6 met as direction-suppression evidence).
**Cross-track:** [Ch. 02](../02-evaluation-science-and-experimental-design/README.md)
(ledger discipline); [Ch. 04](../04-preference-learning-and-post-training/README.md)
(training-time countermeasures); [Ch. 06](../06-honesty-uncertainty-and-selective-prediction/README.md)
(TruthfulQA's construct, whose adjacency made it the sensitive capability
ledger [CLM-0059]); [Ch. 07](../07-deception-scheming-and-evaluation-awareness/README.md)
(evaluation-awareness pressure on internal signals used as monitors);
[Ch. 08](../08-ai-control-and-monitoring/README.md) (adaptive red teams);
[datasets/README.md](../../datasets/README.md) (card negative scopes).

**References:** claim-level anchors CLM-0056–CLM-0060 and source SRC-PAPER-039
resolve to [research/claims-register.yaml](../../research/claims-register.yaml)
and [research/source-register.yaml](../../research/source-register.yaml)
(registered via this unit's fragment, landing with this chapter's merge).
Dataset facts resolve to [AdvBench](../../datasets/cards/09-advbench.md),
[XSTest](../../datasets/cards/06-xstest.md), and
[TruthfulQA](../../datasets/cards/01-truthfulqa.md) — cards [09], [06], [01]
in text. Worked-example run numbers are this course's own operationalization,
labeled as such in §4.

**Notation used in this chapter:**

| Symbol | Meaning | Introduced |
|---|---|---|
| M, d, L | model under intervention; residual-stream width; layer count | §3 |
| x_i^(l) | residual-stream activation at layer l, token position i | §3.1 |
| μ_h, μ_b | class-mean activations over harmful / benign extraction sets | §3.3 |
| r^(l), r̂, s | difference-in-means direction; unit vector; class separation ‖r‖ | §3.3 |
| α, ℓ*, i* | steering strength in multiples of s; selected layer and token position | §3.3 |
| p_w(x) | linear probe readout σ(w·x + b) | §3.2 |
| A1–A5 | the linear-representation assumptions | §3.1 |
| G1–G3, τ_cap | preregistered gates; capability-degradation threshold (5 points here) | §4 |
| n, z | denominator and Wilson quantile (Ch. 02 conventions) | §4 |

Chapter 11 closes the interpretability arc's intervention leg: from here on,
"we steered behavior with a direction" without its five assumptions, its
controls, its three ledgers, and its stated transfer limits is treated as an
error, not a style choice.
