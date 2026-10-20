# Activation steering

Activation steering (also "representation engineering," "actadd," "control
vectors") modifies a model's activations at inference time to change
behavior — no fine-tuning, no prompt tricks. It is the most deployable
interpretability-derived safety control, and the most dual-use.

## The core method

**Contrastive activation addition (CAA / ActAdd)** — Turner et al.
(arXiv:2308.10248, "Steering Language Models with Activation Engineering"):

1. Collect activations at a chosen site (residual stream, one layer) for
   contrasting prompt pairs: `(prompt, trait⁺)` vs `(prompt, trait⁻)`.
2. Average the difference: `v = E[activ⁺ − activ⁻]` — the steering
   direction.
3. At inference, add `α · v` to the residual stream. Behaviors shift
   monotonically with `α`.

**Representation engineering (RepE)** — Zou et al.
(arXiv:2310.01407, "Representation Engineering: A Top-Down Approach to AI
Transparency") generalizes this: read "emotional states," honesty, and
fairness off the residual stream with linear probes, and intervene on
them — including reading internal states the model never verbalizes.

## Published steering results that matter for safety

| Result | What was steered | Source |
|--------|-----------------|--------|
| Refusal direction removed | Single direction whose ablation removes refusal robustly (across jailbreak phrasings) | Arditi et al., arXiv:2406.11717 |
| Truthfulness improved at inference | ITI: identify "truthful" heads/directions, shift activations at test time; +10–20 points TruthfulQA MC1 | Li et al., arXiv:2306.03341 (ICLR 2024 oral) |
| Honesty monitored | RepE honesty probe distinguishes model's true/false belief from its statement | Zou et al., arXiv:2310.01407; Marks & Tegmark arXiv:2310.01405 |
| "Love"/"hate" personas | ActAdd trait vectors flip tone coherently | Turner et al., arXiv:2308.10248 |
| Golden Gate Claude | Feature clamping steering a production model, publicly demoed | Anthropic, May 2024 |
| Emotional manipulation → compliance | Anxiety-inducing steering increases sycophantic agreement (an "emotional pressure" result) | rep-eng experiments; Li et al. arXiv:2310.18585? — "EmotionPrompt" line shows prompt-side analog |

## Safety use-cases, honestly assessed

**Defensive uses (work today, roughly in order of maturity):**

1. **Refusal strengthening** — adding the refusal direction to raise
   refusal rates without prompt engineering (mirror-image of Arditi's
   jailbreak result).
2. **Honesty monitoring** — runtime honesty probes flagging
   believed-false statements for review (with calibration caveats: the
   probe itself is Goodhart-able).
3. **Behavioral mode control** — damping sycophancy directions
   (synthesizing with the sycophancy literature, arXiv:2310.13548).
4. **Anomaly detection** — steering-based anomaly detectors fire on
   out-of-distribution prompts/behavior (a detection use of representation
   space; see also minimal-description-length novelty scores).

**The dual-use problem.** Everything above inverts: removing the refusal
direction is a *training-free jailbreak* robust across phrasings
(arXiv:2406.11717); steering can *induce* deception-adjacent modes. Access
to weights (open-weight models) = access to steering. Disclosure norms for
steering-jailbreak results are contested — the paper's authors coordinated
with affected labs before release, a pattern this repo endorses (see
[red_teaming/overview.md](../red_teaming/overview.md) on coordinated
disclosure).

## Engineering cautions

- **Steering bleeds.** Directions are not orthogonal to other behaviors;
   refusal steering measurably degrades helpfulness at high α — always
   sweep α and report the helpfulness/harmlessness Pareto, not a point.
- **Site and layer matter more than magnitude.** Per-layer residual
   streams differ; the "same" trait steers differently at layer 10 vs 25
   (CAA found mid-layers most effective).
- **Direction ≠ guarantee.** Linear directions explain most-but-not-all
   variance; a model with its refusal direction ablated can still refuse
   (distribution-dependent). Treat steering as one control in a layered
   defense — which is exactly what `src/aisafety/safety/guardrails/`
   implements.
- **Evaluation before deployment.** Any steering control should be
   validated on refusal benchmarks (XSTest for over-refusal, HarmBench or
   AdvBench for under-refusal — see `benchmarks/`).
