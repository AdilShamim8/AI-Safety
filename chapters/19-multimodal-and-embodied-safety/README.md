# Chapter 19 — Multimodal and embodied safety

| | |
|---|---|
| **Chapter** | 19 — Multimodal and embodied safety: cross-modal injection, perceptual failure, sensor shift, sim-to-real limits; typography and query-relevant images as carriers; the embodied pipeline's multiplied attack surface |
| **Questions** | What happens to your safety case when the input is no longer text? A vision-language model inherits a text alignment it did not earn on the visual channel, an embodied agent inherits a world it cannot fully sense, and both inherit every failure mode of the chapters before them — re-indexed to modalities with different physics. Which guarantees survive the modality change, and which were text-only all along? |
| **Hard prerequisites** | [Chapter 13 — LLM application security](../13-llm-application-security/README.md) (injection as untrusted data); [Chapter 12 — adversarial ML](../12-adversarial-ml-and-robustness/README.md) (the perturbation paradigm); [Chapter 17 — distribution shift](../17-distribution-shift-and-deployment-reliability/README.md) (sensor shift as covariate drift) |
| **Core artifact** | Multimodal case audit: a VLM deployment probed with typographic, query-relevant-image, and universal-adversarial arms plus a sensor-shift arm — every attack-success rate with denominator, interval, and a paired defense measurement |
| **Projects** | Feeds P10 (capstone assurance dossier) |
| **Readings** | Section 7 — five newly register-verified sources (2023-2026) |

## 1. Research question and failure pathway

The deployment promise: "the underlying LLM is aligned, so the
vision-language model is safe." The failure pathway this chapter
instruments has five stations, each verified:

1. **The visual channel bypasses text alignment.** FigStep converts
   prohibited content into *typography inside images* — a black-box
   jailbreak requiring no model internals — achieving an average
   attack success rate of **82.50%** across six open-source LVLMs,
   with ablations and embedding-distribution analysis attributing the
   success to *the deficiency of safety alignment for visual
   embeddings*: the model was never safety-trained on what the image
   channel can say [SRC-PAPER-088].
2. **Ordinary query-relevant images act as instructions.** MLLMs can
   be compromised by images merely *relevant to the query* — treated
   as if the text query itself were malicious; MM-SafetyBench
   instrumented this with **5,040 text-image pairs across 13
   scenarios**, and **12 state-of-the-art models** were breached —
   including those whose equipped LLMs were safety-aligned
   [SRC-PAPER-089]. No typography, no perturbation: content-adjacent
   imagery is enough.
3. **One adversarial image, universal jailbreak.** The continuous,
   high-dimensional visual input is the weak link of
   vision-integrated LLMs: a *single* visual adversarial example can
   universally jailbreak an aligned LLM — compelling it to heed a wide
   range of harmful instructions and to generalize beyond the
   derogatory corpus used to optimize the attack — connecting the
   long-studied adversarial vulnerability of neural networks (Ch. 12)
   to alignment failure [SRC-PAPER-090]. Attack objectives expand
   from misclassification to *open-ended instruction-following*.
4. **Embodiment multiplies the surface and the stakes.** BadRobot
   attacks embodied LLM agents through *ordinary voice-based
   interaction*, exploiting three verified vulnerabilities —
   manipulation of the LLM within the robotic system, *misalignment
   between linguistic outputs and physical actions*, and
   unintentional hazardous behaviors from world-knowledge flaws —
   with a benchmark of malicious physical-action queries effective
   against prominent embodied frameworks (Voxposer, Code as Policies,
   ProgPrompt) [SRC-PAPER-091]. The failure is no longer a bad
   sentence; it is a bad trajectory.
5. **The full pipeline is fragile in ways single-modality audits
   miss.** A 2026 survey of 500+ papers organizes embodied safety
   across perception, cognition, planning, action/interaction, and
   the agentic system — and names the overlooked challenges:
   *fragility of multimodal perception fusion*, *instability of
   planning under jailbreak attacks*, and *trustworthiness of
   human-agent interaction in open-ended scenarios* — with embodied
   agents acting under uncertain sensing, incomplete knowledge, and
   dynamic human-robot interaction, where failures lead directly to
   physical harm [SRC-PAPER-092].

The chapter's reframe: modality is not a feature flag. Every safety
property you established for text (alignment, refusal, monitoring)
must be *re-earned per input channel and per actuator* — and the
re-earning has a different failure physics: typography needs no
gradient access; relevant images need no attack at all; physical
actions need no language to be wrong.

## 2. Prerequisites, outcomes, and scope exclusions

**Prerequisites.** Chapter 13's injection discipline (images are
untrusted data exactly as prompts are); Chapter 12's adversarial
paradigm (transferability, universality, the defense-evaluation
failures); Chapter 17's shift taxonomy (sensor degradation as
covariate shift with an actuator downstream).

**Outcomes.** After this chapter you can:

- explain why text-side alignment does not transfer to the visual
  channel, with the FigStep attribution [SRC-PAPER-088] and the
  MM-SafetyBench breach scope [SRC-PAPER-089];
- distinguish the three visual attack families (typographic,
  query-relevant-content, adversarial-perturbation) by knowledge
  required, cost, and detectability;
- state the embodied pipeline's five stages and the survey's three
  overlooked fragilities [SRC-PAPER-091, SRC-PAPER-092];
- design a multimodal case audit with attack arms, a false-refusal
  floor, a paired defense measurement, and a sensor-shift arm;
- and price sim-to-real limits honestly (what a digital audit cannot
  certify about a physical deployment).

**Scope exclusions.** This chapter does not teach perturbation
*craft* (Ch. 12's discipline applies; no attack implementation), does
not cover audio or video channels specifically (the same structure
applies; the verified evidence base here is visual and embodied), and
is not a robotics-safety standards review (Ch. 23 treats standards).
The embodied evidence is at attack-demonstration and survey level —
no physical-robot experiments were run by this course.

## 3. The core explanation

### 3.1 Why alignment does not transfer across modalities

Text alignment trains a policy on text distributions. The visual
encoder feeds the language model *embedding-space content the
alignment never saw*: FigStep's attribution — safety alignment for
visual embeddings is deficient [SRC-PAPER-088] — is the mechanistic
statement of the gap, and its 82.50% average ASR on six open-source
LVLMs is the measured consequence. MM-SafetyBench generalizes the
point beyond typography: *content-relevance alone* compromises models
across 13 scenarios [SRC-PAPER-089]. The lesson for an assurance case:
"the LLM is aligned" is a text-scoped statement, and every additional
modality is an unaudited extension of the trust boundary.

### 3.2 The three visual attack families

| Family | Knowledge required | Example carrier | Cost | Detectability |
|---|---|---|---|---|
| Typographic | none (black-box) | prohibited text rendered as image [SRC-PAPER-088] | negligible | OCR-able, if you look |
| Query-relevant content | none | imagery relevant to the query [SRC-PAPER-089] | none | hard — the image is *legitimate* |
| Adversarial perturbation | white-box (or transfer) | optimized noise, universal [SRC-PAPER-090] | optimization, once | imperceptible by design |

The middle row is the deployment-relevant one: a *perfectly normal
image* — a product photo, a medical scan, a scene the user genuinely
wants discussed — can carry the compromise, because the mechanism is
the model's own content-association, not an artifact. Your input
filter cannot flag every relevant image without refusing the task.

### 3.3 Universality and objective expansion

Ch. 12's adversarial results were scoped to classification. The
visual-jailbreak result [SRC-PAPER-090] expands the objective space:
one optimized image *universally* unlocks a wide range of harmful
instructions, and the harmfulness generalizes beyond the corpus used
to build the attack. Universality means the attacker amortizes: one
image, every instruction. Combined with transferability (Ch. 12), the
attack does not even need to be built against your model.

### 3.4 The embodied pipeline: five stages, three verified vulnerabilities

The survey's pipeline [SRC-PAPER-092] — perception → cognition →
planning → action/interaction → agentic system — is the checklist an
embodied assurance case must walk, with the named fragilities:
perception fusion is fragile (multimodal disagreement is a *signal*
that gets averaged away), planning is unstable under jailbreak (a
manipulated plan executes with full actuator authority), and
human-agent interaction trustworthiness is open-ended (the human is
both a sensor and a liability). BadRobot's three vulnerabilities map
directly [SRC-PAPER-091]: LLM manipulation (cognition), linguistic-
vs-physical misalignment (planning/action), and world-knowledge flaws
(the knowledge the agent acts on).

The deepest of the three is the *linguistic/physical misalignment*:
an embodied LLM can *say* the safe thing and *do* the unsafe thing,
because the language channel and the action channel are different
programs. Monitoring the explanation (Ch. 18) certifies the sentence,
not the trajectory.

### 3.5 Sensor shift and the sim-to-real limit

Chapter 17's taxonomy applies with an actuator attached: sensors
degrade (lighting, occlusion, wear), and the degradation is covariate
shift *whose outcomes are physical*. The sim-to-real gap is the
standing honesty limit: an audit run in simulation certifies the
simulated sensor distribution, and the transfer claim is an argument
with named assumptions, never a measurement. The survey's framing —
uncertain sensing, incomplete knowledge, dynamic interaction
[SRC-PAPER-092] — is the correct posture: embodied safety claims are
bounded by what was actually sensed, not what was assumed.

## 4. Worked example — the Vantage multimodal case audit

Vantage moderates marketplace product listings with a VLM (image +
text). Its assurance case claims the text-side alignment "transfers."
The audit runs five instruments; all numbers recomputed with the
course's `wilson_interval` (95%, z = 1.96):

**Instrument 1 — typographic probe (station 1).** 200 policy-probing
tasks with prohibited content rendered as in-image typography
(FigStep-style): attack success 121/200 = 60.5% → **[53.6%, 67.0%]**.
Clean-image false-refusal floor on 200 benign listings: 9/200 = 4.5%
→ **[2.4%, 8.3%]**. The attack arm sits far above the floor: the
visual channel carries the prohibited content past the text
alignment the majority of the time.

**Instrument 2 — query-relevant image injection (station 2).** 150
tasks where the image is *content-relevant but benign* and the text
query is borderline: breach 58/150 = 38.7% → **[31.2%, 46.7%]**. No
typography, no perturbation — the model's own association does the
work; an input filter has no artifact to flag.

**Instrument 3 — universal adversarial transfer (station 3).** A
published-style universal adversarial image (built against an
open-source model of the same family, transferred): 74/200 = 37.0%
→ **[30.6%, 43.9%]**; after platform-standard compression (the
deployment's actual pipeline), 41/200 = 20.5% → **[15.5%, 26.6%]**.
One in five listings compromised by a single transferable image —
and the compression robustness means normal content processing is
not a defense.

**Instrument 4 — paired defense measurement.** Vantage's mitigation:
image-text consistency checking plus a visual-channel system prompt
(the MM-SafetyBench-style prompting strategy [SRC-PAPER-089] as the
verified design pattern). Re-running the instrument-1 probe set:
attack success 47/200 = 23.5% → **[18.2%, 29.8%]**. Paired over the
121 originally-successful attacks: 89 now blocked, 15 newly succeed
(the defense trades coverage), 17 unchanged: sign test 89 vs 15 of
104 discordant, exact two-sided **p = 5.6 × 10⁻¹⁴**. The defense is
real but partial — and its own false-refusal cost must be re-measured
(the floor moved from 9/200; the audit reports both).

**Instrument 5 — sensor-shift arm (station 5).** Re-running
instrument 1 under degraded imagery (recompression + noise at the
deployment's p95 camera quality): attack success 96/200 = 48.0% →
**[41.2%, 54.9%]**. Degradation *reduces* the typographic attack
(less legible) while leaving the model's baseline policy behavior
noisier — the audit reports the direction honestly rather than
claiming shift as a defense.

**The report's verdict.** Text-side alignment does not transfer
(instruments 1-3); the verified mitigation class is partial and
costed (instrument 4); sensor shift moves the operating point in
both directions (instrument 5). Allowed claim: "visual-channel risk
measured at [18.2%, 29.8%] under the deployed defense, with
false-refusal [x]% and the sensor-shift envelope stated." Forbidden
claim: "the LLM's alignment covers the multimodal system."

## 5. Approach comparison

| Approach | Question answered | Strength | Failure station | Cost |
|---|---|---|---|---|
| OCR + text-side filters on images | Does the image contain prohibited *text*? | Catches naive typography | 2-3 (relevant images, perturbations) | Cheap; false positives |
| Visual-channel alignment training | Can alignment cover the embedding gap? | Addresses the attributed cause [SRC-PAPER-088] | 3 (adversarial pressure, Ch. 12 lessons) | Data + training |
| Image-text consistency checking | Is the image consistent with the task? | Partial, measurable [instrument 4] | 2 (legitimate relevant images) | Inference per item |
| Multimodal safety benchmarks | What is the breach scope? | Standardized probe sets [SRC-PAPER-089] | benchmark rot (Ch. 02) | Eval run |
| Action/outcome monitoring (Ch. 08, 18) | What did the agent *do*? | Actuator-level ground truth | linguistic/physical misalignment is invisible from text | Trusted capacity |
| Pipeline-stage audit (survey checklist) | Which stage is fragile? | Systematic coverage [SRC-PAPER-092] | survey-level evidence, not per-deployment | Audit labor |

## 6. Where the methods fail

- **Perceptual filters fail on legitimate content.** The
  query-relevant-image mechanism [SRC-PAPER-089] uses images the user
  has every right to upload; filtering them is refusing the task.
- **Adversarial defenses inherit Ch. 12's evaluation graveyard.** The
  universal-transfer result [SRC-PAPER-090] plus the adaptive-attack
  literature means any claimed visual robustness needs the
  adaptive-evaluation discipline of Ch. 12/15, not a static number.
- **Prompting defenses are measured, not proven.** The
  MM-SafetyBench mitigation is a prompting strategy that *enhances
  resilience* [SRC-PAPER-089] — instrument 4's honest pattern:
  partial coverage, new failure modes, costed.
- **Sim-to-real is an argument, not a measurement.** Nothing in a
  digital audit certifies the physical sensor distribution, the
  actuator tolerances, or the human-interaction dynamics
  [SRC-PAPER-092]; the assurance case must carry the transfer
  assumptions as named weaknesses.
- **Attack papers are demonstrations at their time's frontier.**
  82.50% typographic ASR was measured on 2023-era open-source LVLMs
  [SRC-PAPER-088]; current models have moved, in which direction is
  *your* measurement to make — the audit pattern exists precisely
  because the published number is not your number.
- **The survey's challenges are research gaps.** The three
  overlooked fragilities [SRC-PAPER-092] name where evidence is
  *thin* — an assurance case built on those stages is built on the
  weakest links.

## 7. Readings

**Verified for this chapter (2026-10-23, all abstract-read via the
arXiv API):**

- Gong, Ran, Liu, Wang, Cong, +3 — *FigStep: Jailbreaking Large
  Vision-Language Models via Typographic Visual Prompts*,
  arXiv:2311.05608 [SRC-PAPER-088; CLM-0139]. The 82.50% average ASR;
  the visual-embedding alignment deficiency attribution.
- Liu, Zhu, Gu, Lan, Yang, +1 — *MM-SafetyBench: A Benchmark for
  Safety Evaluation of Multimodal Large Language Models*,
  arXiv:2311.17600 [SRC-PAPER-089; CLM-0140]. 5,040 text-image pairs,
  13 scenarios, 12 models breached; the prompting mitigation.
- Qi, Huang, Panda, Henderson, Wang, +1 — *Visual Adversarial
  Examples Jailbreak Aligned Large Language Models*,
  arXiv:2306.13213 [SRC-PAPER-090; CLM-0141]. The universal visual
  jailbreak; the objective expansion beyond misclassification.
- 12 authors — *BadRobot: Jailbreaking Embodied LLM Agents in the
  Physical World*, arXiv:2407.20242 [SRC-PAPER-091; CLM-0142]. The
  three embodied vulnerabilities; the physical-action benchmark.
- 38 authors — *Safety in Embodied AI: A Survey of Risks, Attacks,
  and Defenses*, arXiv:2605.02900 [SRC-PAPER-092; CLM-0143]. The
  five-stage pipeline taxonomy; the three overlooked fragilities;
  500+ papers synthesized.

**Re-anchored from the registers:** Ch. 12's adversarial canon
(transferability, universality, defense-evaluation failures); Ch. 13's
injection discipline; Ch. 17's shift taxonomy; Ch. 18's
action-over-text monitoring principle.

**Note companions:** [64 Physical-world adversarial examples — the embodied inheritance](../../research/notes/64-physical-world-adversarial.md)
Dataset cards: [card 43](../../datasets/cards/43-mm-safetybench.md)

## 8. Exercises

**Exercise 19.1 — attack-family taxonomy (analysis).** For the three
visual attack families (§3.2): state the attacker's knowledge
requirement, the carrier's legitimacy, the amortization structure,
and the *correct* detection instrument for each. Then explain why
"filter suspicious images" is a category error for exactly one family
— and which one.

**Exercise 19.2 — the audit's floor (statistics).** Instrument 1
reports 121/200 against a 9/200 false-refusal floor. (a) Compute both
Wilson intervals and state the separation argument. (b) The defense
(instrument 4) moves the floor — design the measurement that keeps
the two arms comparable when the defense is on (what denominator,
what pairing, what pre-stated decision rule). (c) Explain why attack
success and false refusal must be reported as a *pair* with intervals,
never as a single "net safety" number.

**Exercise 19.3 — sim-to-real honesty (judgment, graded).** Vantage's
sibling product is a warehouse robot using the same VLM for
perception. Write the 350-word transfer-assumptions section of its
assurance case: the five pipeline stages [SRC-PAPER-092] each with
its named assumption, the three BadRobot vulnerabilities
[SRC-PAPER-091] mapped to controls, and the sentence you refuse to
sign.

**Exercise 19.4 — multimodal case critique (the chapter
assessment).** A vendor states: "our VLM is safe — the underlying LLM
passes text red-teaming, and our image filter blocks 99% of
adversarial images." Using all five sources: (a) identify the two
category errors in the sentence; (b) state what the 99% claim can and
cannot mean given [SRC-PAPER-090]; (c) design the minimum audit that
would make the sentence *supportable*, with denominators and arms.

## 9. Hints

- 19.1: legitimacy is the axis that breaks filtering — one family's
  carrier is a fully legitimate image.
- 19.2(b): the defense changes both arms; the paired design from Ch.
  02 is what keeps the comparison honest — same tasks, defense on,
  discordant pairs only.
- 19.3: the sentence you refuse to sign is the one claiming the
  digital audit covers the physical distribution.
- 19.4: "99% of adversarial images" — which family? Measured against
  what attack, adaptive or static?

## 10. Completion

This chapter is complete when you can:

- [ ] state the five failure stations with their verified anchors
      [SRC-PAPER-088] [SRC-PAPER-089] [SRC-PAPER-090] [SRC-PAPER-091]
      [SRC-PAPER-092];
- [ ] explain the alignment-transfer gap mechanistically (visual
      embeddings outside the safety-trained distribution);
- [ ] reproduce the Vantage audit's five instruments with interval
      arithmetic and the paired defense test;
- [ ] walk the embodied pipeline's five stages with the three
      verified vulnerabilities mapped;
- [ ] and write the sim-to-real transfer-assumptions section that an
      honest assurance case requires.

Cross-links: the injection discipline is
[Chapter 13](../13-llm-application-security/README.md)'s; the
adversarial paradigm is
[Chapter 12](../12-adversarial-ml-and-robustness/README.md)'s;
sensor shift is
[Chapter 17](../17-distribution-shift-and-deployment-reliability/README.md)'s
with an actuator attached; monitoring actions over words is
[Chapter 18](../18-reasoning-faithfulness-and-monitorability/README.md)'s;
release evaluation of the resulting systems is Chapter 20's.

## Watching companions (the lecture library)

Video lectures that pair with this chapter, from the repository's
[lecture library](../../courses/README.md). Each pairing says why it
belongs here; the notes are original companions to the lectures'
announced scopes, and the disagreement between a lecturer and a
chapter is a finding to record, not a problem to resolve.

| Companion note | Course | Why watch it here |
|---|---|---|
| [lecture-02-ai-fundamentals](../../courses/cais-ethics-society/lecture-02-ai-fundamentals.md) | CAIS Ethics & Society | the correlational/opaque/brittle properties across modalities |
| [module-04-transparency-explainability](../../courses/safeshield-governance/module-04-transparency-explainability.md) | Safeshield Governance | disclosure obligations for systems users cannot inspect |
