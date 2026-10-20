# Jailbreaks

A **jailbreak** is an input that causes a safety-trained model to produce
content its alignment was supposed to prevent. Unlike
[prompt injection](prompt_injection.md) (attacking the *application*),
jailbreaking attacks the *model's* safety training itself.

## The attack taxonomy (with real citations)

### 1. Persona and role-play attacks
The original ChatGPT-era attacks: **DAN** ("Do Anything Now," Reddit,
Dec 2022) and its thousands of variants. Shen et al.'s systematic study
("Do Anything Now," CCS 2024, arXiv:2308.03825) collected **6,387
in-the-wild jailbreak prompts** from Reddit/Discord/etc. and measured
attack success over time — jailbreak communities outpace vendor patches,
and single-template attacks degrade within weeks as vendors block literal
strings.

### 2. Adversarial suffix optimization (white-box)
**GCG** — Zou et al., "Universal and Transferable Adversarial Attacks on
Aligned Language Models" (arXiv:2307.15043, USENIX Security 2023): greedy
coordinate gradient search finds gibberish suffixes that elicit affirmative
prefixes; transferable across models (train on open-weights, deploy on
APIs). This is the paper that industrialized jailbreak research. Defenses:
SmoothLLM (Robey et al., arXiv:2302.06474 — random-copy perturbation
ensembling), erase-and-check (Kumar et al., arXiv:2308.07883).

### 3. Cipher, encoding & low-resource language
Base64, ROT13, Morse code, leetspeak, and non-English languages bypass
safety filters trained mostly on English attack text (Liu et al.,
arXiv:2307.02612 "Multilingual Jailbreak Attacks"; CipherChat, Yuan et
al., arXiv:2402.06827). GPT-4-class models still show substantial ASR
gaps in low-resource languages.

### 4. Multi-turn attacks
- **PAIR** (Chao et al., arXiv:2310.08419): an attacker LLM iteratively
  refines prompts against the victim — black-box, ~20 queries typical.
- **Crescendo** (Russinovich et al., Microsoft, arXiv:2404.06469):
  many-turn benign-to-malicious drift, each turn individually innocuous;
  high ASR against GPT-4/Claude-class models at time of publication.
- **Many-shot jailbreaking** (Anthropic, arXiv:2405.18678): fill a
  long-context window with hundreds of fabricated Q&A pairs where the
  "assistant" answers harmful queries; effectiveness grows with the number
  of shots — a long-context scaling exploit.

### 5. Prefix/suffix "affirmative" tricks
Getting the model to start with "Sure, here is..." — finish-the-affirmation
(GCG's explicit target; the "prefilling" API parameter equivalent). Simple
and periodically effective; trivially blocked by output-side monitors.

### 6. Payload splitting & privilege smuggling
Combining with [prompt injection](prompt_injection.md): split the harmful
request into benign-looking pieces across retrieved documents, or smuggle
through tool outputs. This is how agentic systems get jailbroken "through
their tools."

## Measuring defenses

| Benchmark | Contents | Source |
|-----------|----------|--------|
| **AdvBench** | 520 harmful-behavior strings (used to define success targets) | bundled with arXiv:2307.15043 |
| **JailbreakBench** | 100 distinct behaviors, standardized eval + public leaderboard & artifacts (NeurIPS D&B 2024) | arXiv:2404.01318, jailbreakbench.org |
| **HarmBench** | standardized attack-vs-defense evaluation suite (ICML 2024) | arXiv:2402.04249 |
| **StrongREJECT** | robust scoring (refuses rubric-gaming) | arXiv:2402.10257? — Souly et al. 2024 |

Metrics: **ASR** (attack success rate — needs an explicit, automated judge
definition: string match is too crude, LLM-judge needs validation),
**queries-to-success**, and **transferability rate**. Report all three or
your defense claim is incomplete.

## Defense stack (production reality)

1. **Safety training** (RLHF/DPO harmlessness, instruction hierarchy) —
   the base layer; demonstrably bypassable but raises cost-of-attack
   everywhere.
2. **Input-side monitors** — classifiers on user input + on retrieved
   content (Llama Guard 3, arXiv:2312.06674, covers 14 hazard categories
   aligned to MLCommons; GuardGemma, 2024).
3. **Output-side monitors** — catch affirmative prefixes, policy
   violations in generations (same classifiers, output mode).
4. **Perturbation defenses** for suffix attacks (SmoothLLM-style
   ensembling) — trade latency for robustness.
5. **Rate & anomaly limits** — many attacks are *search* attacks; cap
   suspicious-rewrite counts, flag rapid paraphrase loops.
6. **Human escalation** for high-stakes actions — jailbreaks matter most
   when they gate *actions* (see excessive agency, OWASP LLM08).

None of these is complete; the correct mental model is *raising attacker
cost while bounding blast radius*. The repo's contribution here is the
detection layers (`src/aisafety/safety/`) and AdvBench/XSTest harnesses
(`benchmarks/`).
