# What is AI safety?

**AI safety** is the discipline of building AI systems that behave as
intended, fail gracefully when they don't, and remain beneficial under
adversarial pressure, distribution shift, and scaling. It is distinct from —
though overlapping with — *AI security* (protecting systems from attack) and
*AI ethics* (normative questions about what systems should do). Safety asks
an engineering question: **how do we make the thing we built keep working
the way we meant it to?**

A useful canonical framing is Amodei et al.'s *Concrete Problems in AI
Safety* (arXiv:1606.06565, 2016), which decomposed the goal into five
technical problems that still structure the field today:

1. **Avoiding negative side effects** — the system optimizing its objective
   without trampling things we care about.
2. **Reward hacking** (specification gaming) — exploiting loopholes in the
   specified objective rather than fulfilling its spirit.
3. **Scalable oversight** — cheaply supervising a system more capable than
   the supervisor at the task.
4. **Safe exploration** — learning without taking catastrophic actions along
   the way.
5. **Robustness to distributional shift** — performing well off-training-
   distribution, where most real harm happens.

## Modern LLM safety has three layers

For large language models specifically, practitioners usually mean:

**1. Misuse safety (front of model + guardrails).** Preventing users from
eliciting harmful content: toxicity, CBRN assistance, targeted harassment.
Practically implemented via safety fine-tuning (RLHF on harmlessness — see
Bai et al., arXiv:2204.05862), input/output classifiers (Meta's Llama Guard,
arXiv:2312.06674; OpenAI's free Moderation API), and structured guardrail
pipelines (NVIDIA NeMo Guardrails; Guardrails AI). This is where most
applied work today lives — and what this repository's `aisafety` package
implements.

**2. Honesty and reliability (model quality).** Hallucination, calibration,
and brittleness. TruthfulQA (arXiv:2109.07958) showed that larger models
imitate human falsehoods *more*: common misconceptions are well-represented
in training text, so scale alone does not fix honesty.

**3. Alignment in the strong sense (specification and oversight).** Whether
the model's optimization target is actually what we want, especially for
future systems that exceed our ability to evaluate outputs directly. This is
the subject of Russell's *Human Compatible* (2019), Christiano et al.'s
iterated amplification (arXiv:1810.08575), debate (arXiv:1805.00899), and
OpenAI's weak-to-strong generalization program (arXiv:2312.09390).

## What AI safety is *not*

- **Not a filter bolted on at deployment.** Safety properties are baked in
  by data curation, training objectives (RLHF/DPO), and evaluation — filters
  are a last line of defense, not the defense.
- **Not only about existential risk.** The same discipline that worries
  about deceptive alignment (arXiv:2401.05566) also ships PII redaction and
  prompt-injection detection. This repo deliberately covers both ends.
- **Not solved by benchmarks alone.** Goodhart's law applies: saturating
  TruthfulQA does not make a model truthful. Benchmarks are smoke detectors,
  not certificates.

## Where to go next

- [Taxonomy of safety problems](taxonomy.md) — the full map
- [History](history.md) — how the field got here
- The repo's [toolkit quickstart](../../README.md) — safety filters you can run today
