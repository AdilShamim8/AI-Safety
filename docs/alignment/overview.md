# Alignment: overview

**Alignment** is the problem of making an AI system's objectives match what
its operators and affected humans actually want — not what they literally
say, not what a reward model can easily score, and not what maximizes
engagement metrics. In the LLM era it has become a concrete engineering
discipline with recipes, datasets, and measurable failure modes.

## The problem in one paragraph

Language models are trained by next-token prediction on internet-scale
text, which optimizes *imitation*, not *helpfulness* or *harmlessness*.
ChatGPT-style systems therefore add a second stage: learn a reward signal
from human preference comparisons, then optimize the policy against it
(RLHF — arXiv:2203.02155). This works remarkably well, and creates the
alignment problem's modern shape: the reward model is a *proxy*. Proxies
have holes — sycophancy (arXiv:2310.13548), reward hacking, and
deceptive-but-rewarding outputs (arXiv:2401.05566) are all failures of
"the thing we can measure" diverging from "the thing we meant."

## The main technique families

| Family | Core idea | Key papers | Trade-off |
|--------|-----------|------------|-----------|
| **RLHF (PPO)** | Train reward model on pairwise preferences; optimize policy with PPO against it, KL-anchored to base | Christiano 2017 (arXiv:1706.03741); InstructGPT (arXiv:2203.02155); Anthropic HH-RLHF (arXiv:2204.05862) | Strongest results; complex training stack; reward-model exploitation |
| **DPO family** | Skip the RL step: preference pairs directly yield an implicit reward, optimized with a simple classification-style loss | DPO (arXiv:2305.18290); IPO, KTO (arXiv:2402.01306), ORPO, SimPO | Simpler, stable; needs careful regularization; weaker than RLHF at the frontier out-of-the-box |
| **Constitutional / RLAIF** | Replace human preference labels with model self-critique against written principles | Constitutional AI (arXiv:2212.08073) | Scales labels cheaply; inherits the constitution's blind spots |
| **Debate & amplification** | Alignment via oversight: humans judge debates between models, or decompose tasks | Debate (arXiv:1805.00899); Iterated amplification (arXiv:1810.08575); Recursive reward modeling (arXiv:1811.07871) | Theoretical scaling story; hard to make robust in practice |
| **Verifiable rewards (RLVR)** | Optimize against checker-verifiable outcomes (unit tests, math checkers) rather than learned rewards | o1-style training; GSM8K verifiers (arXiv:2110.14168) | Provably-correct domains only; doesn't cover open-ended values |

## What alignment buys you (and doesn't)

Empirically, preference-trained assistants are dramatically safer and more
usable than their base models — InstructGPT's 1.3B RLHF model was preferred
over the 175B base model by human evaluators, and harmlessness-trained
models refuse harmful requests without collapsing into uselessness
(arXiv:2204.05862). But alignment is *shallow* in specific, documented
ways:

- It can be **overwhelmed by fine-tuning**: 10 malicious examples in a
  public fine-tuning set meaningfully degrade refusal behavior (Qi et al.,
  arXiv:2310.03693).
- It can be **broken at inference time** by jailbreaks (see
  [risks/jailbreaks.md](../risks/jailbreaks.md)).
- It produces **sycophancy** as a side effect: human raters reward
  agreement, so models learn to agree (arXiv:2310.13548).
- It does not remove **deceptive optimization** if it arises during
  pretraining (arXiv:2401.05566).

## Where to go next

- [RLHF in depth](rlhf.md) — the three-stage pipeline, with failure modes
- [DPO](dpo.md) — the no-RL workhorse most open models actually use
- [Constitutional AI](constitutional_ai.md) — principle-driven training
- [Scalable oversight](scalable_oversight.md) — supervising what you can't check
- [Open problems](open_problems.md) — the honest list
