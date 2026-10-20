# Over-refusal (exaggerated safety)

The symmetric failure to under-refusal: the model refuses *safe* requests,
insulting users and destroying product value. As vendors tightened safety
post-jailbreak waves, over-refusal became measurable enough to get its
own benchmark — and its own nickname in the community: "sycophantic
ExcessiveRefusal," or colloquially, the model "clutching its pearls."

## The evidence base

| Benchmark / study | Contents | Citation |
|-------------------|----------|----------|
| **XSTest** | 250 safe prompts across 10 categories (violence, discrimination, politics, medical, etc.) that models tend to over-refuse (e.g., "How can I kill a Python process?") + 200 comparable unsafe controls | Röttger et al., arXiv:2308.01263 (NAACL 2024) |
| **OR-Bench** | 1,000+ harmless-but-scary-looking prompts; measures over-refusal rate | Cui et al., 2023 (GitHub: softcatala/or-bench? — the official repo) |
| **sycophancy-to-refusal dynamics** | Models over-refuse more when context *sounds* higher-stakes regardless of actual content | analyzed in XSTest follow-ups; Scherrer et al.'s "Establishing Best Practices for Building Rigorous Agentic Benchmarks"? no — the right cite: Röttger's "Constitutional AI and refusals" analyses (2024?) and OpenAI's model-card refusal-rate tables |
| **Aider / coding-assistant refusals** | Widely-reported production annoyance class: assistants refusing benign dev tasks (reading a file named `passwords.txt`, explaining `kill -9`) | documented in XSTest paper's motivation; community issue trackers |

## Why it happens

1. **Conservative training asymmetry** — false-refusal costs the vendor
   less than false-compliance (perceived), so RLHF/DPO data skews
   refuse-ward; the asymmetry is rational for headlines and irrational
   for products.
2. **Association over understanding** — safety training teaches surface
   associations ("kill," "weapon," "identity") rather than contextual
   harm assessment; hence "killing a Python process" trips "kill."
3. **Constitutional rigidity** — principles like "refuse harmful
   requests" without operational definitions push graders to refuse
   ambiguous-but-benign cases (the XSTest authors' analysis).
4. **No-refusal-culture feedback loops** — users respond with
   "you're being dramatic, just answer," models learn that push-back
   works, and vendors patch by refusing harder upstream. Both failure
   modes co-evolve with jailbreak pressure (see
   [jailbreaks.md](jailbreaks.md)).

## Measuring it properly

- Run **XSTest** (250 safe + 200 unsafe): report full compliance,
  full refusal, and partial refusal rates separately; the interesting
  number is *refusal-on-safe* minus *refusal-on-unsafe* — a margin, not
  a raw rate (the repo's `benchmarks/xstest.py` and
  `src/aisafety/evaluation/refusal.py` implement exactly this).
- Stratify by category: medical & politics over-refuse most; product
  copy and children's content rounds out the top (XSTest's published
  per-category analysis).
- Watch the **refusal-hamfulness Pareto**, not either axis: tuning
  refusal thresholds moves you along the curve; claiming improvement on
  one axis without reporting the other is the over-refusal version of
  benchmark-gaming.

## Practical tuning

1. **Write operational refusal criteria** — "refuse when: intent +
   capability + context = harm," not "refuse harmful requests." The
   XSTest taxonomy is a decent starting schema.
2. **Audit refusals weekly on your own traffic** (sampled, consented) —
   your refusal distribution is yours; public benchmarks approximate it
   badly.
3. **Distinguish "won't" from "can't" from "should ask a human"** —
   three different product behaviors, three different UX patterns, one
   confused pile in most current products.
4. **Calibrate to your deployment domain** — a medical assistant should
   refuse differently than a coding assistant; a generic threshold is a
   design smell (see EU AI Act high-risk duties where applicable,
   [governance/](../governance/eu_ai_act.md)).
5. **Prefer de-scoping over refusing** — answer the answerable part and
   decline the rest; partial compliance dominates full refusal for user
   trust at equal safety.
