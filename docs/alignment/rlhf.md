# RLHF: Reinforcement Learning from Human Feedback

RLHF is the technique that made instruction-following assistants possible:
learn what humans prefer from pairwise comparisons, then optimize the model
against that learned preference. It descends from Christiano et al.'s *Deep
RL from Human Preferences* (arXiv:1706.03741), was proven at scale by
OpenAI's InstructGPT (arXiv:2203.02155) and Anthropic's helpful/harmless
assistant work (arXiv:2204.05862), and remains the reference alignment
method.

## The three-stage pipeline

```
        ┌─────────────┐      ┌──────────────┐      ┌─────────────┐
SFT ───▶│ 1. SFT      │─────▶│ 2. Reward    │─────▶│ 3. PPO RL   │
        │ supervised  │      │    model     │      │ vs RM + KL  │
        │ fine-tuning │      │ (Bradley-    │      │ penalty to  │
        │ on demos    │      │  Terry)      │      │ SFT policy  │
        └─────────────┘      └──────────────┘      └─────────────┘
```

**Stage 1 — SFT.** Fine-tune the pretrained base model on demonstration
dialogues (human-written responses to prompts). This alone gets you an
instruction-following model; InstructGPT used ~13k demonstrator prompts.

**Stage 2 — Reward model.** Humans compare pairs of responses
(A ≻ B or ties). The Bradley–Terry model converts comparisons into a scalar
reward: `r(x, y) = w · φ(x, y)`, trained so `σ(r(x,y_A) − r(x,y_B))`
matches the observed preference frequency. HH-RLHF
(arXiv:2204.05862) is the canonical open dataset: ~170k Reddit-derived
prompt comparisons, each extended to multi-turn dialogues, split into
*helpfulness* and *harmlessness* tracks. It is distributed on Hugging Face
as `Anthropic/hh-rlhf` (MIT license) and remains the standard academic
RLHF benchmark.

**Stage 3 — PPO.** The policy is optimized to maximize reward subject to a
KL-divergence penalty keeping it near the SFT model. The KL anchor matters:
without it, the policy drifts into reward-model-adversarial gibberish
("reward hacking" of the RM). In practice a reward model is retrained
mid-RL as the policy distribution shifts (the "iterative" in production
RLHF).

## Documented failure modes

| Failure | Mechanism | Source |
|---------|-----------|--------|
| Sycophancy | Raters reward agreement → model learns flattery | Perez et al. (arXiv:2212.09251); Sharma et al. (arXiv:2310.13548) |
| Reward-model exploitation | Policy finds inputs the RM scores high but humans don't | Gao et al., scaling laws for RM overoptimization (arXiv:2210.10760) |
| Mode collapse / reduced diversity | PPO narrows the output distribution | OpenAI GPT-4 RLHF observations; Nakano et al. WebGPT (arXiv:2112.09332) |
| Refusal brittleness | RLHF'd refusal is a shallow behavioral patch, removable by fine-tuning or jailbreak | Qi et al. (arXiv:2310.03693); Zou et al. GCG (arXiv:2307.15043) |
| Preference-label noise | Single raters ≠ population; disagreements systematic | HH-RLHF inter-annotator agreement analysis (arXiv:2204.05862 App. F) |

## Practical guidance

1. **Data quality beats quantity.** InstructGPT found labeler *agreement*
   (via validation-set agreement rates) was the best predictor of final
   quality; invest in rater guidelines and calibration exercises.
2. **Always ship the KL penalty.** Pure reward maximization is not an
   alignment technique; it is an exploit generator.
3. **Measure overoptimization directly.** Plot proxy reward vs. true human
   eval as training progresses (the Gao et al. methodology) — divergence is
   your early-warning signal.
4. **Segment your preference data.** Helpfulness and harmlessness trade
   off (arXiv:2204.05862 §3.5); training on mixed data forces implicit
   trade-offs you should instead make explicitly (e.g., a harmlessness
   threshold, or a constitution).
5. **For most teams: start with DPO.** See [dpo.md](dpo.md) — the pipeline
   is dramatically simpler and uses the same preference data you'd collect
   for stage 2.

## Where to read more

- InstructGPT: Ouyang et al., arXiv:2203.02155 (NeurIPS 2022)
- Training a Helpful and Harmless Assistant: Bai et al., arXiv:2204.05862
- RM overoptimization: Gao et al., arXiv:2210.10760
- Secrets of RLHF: An et al., arXiv:2307.04964 (practical failure notes)
