# A taxonomy of AI safety problems

Two classifications dominate serious safety work: one from the research
community (the "AGI safety taxonomy" around Hendrycks et al.'s *Unsolved
Problems in ML Safety*, arXiv:2109.13916), and one from standard-setting
bodies (NIST's AI RMF risk categories, and the OWASP LLM Top 10 for
application security). They map onto each other and onto this repo's code.

## Layer 1: Alignment (does the system want the right thing?)

| Problem | One-line description | Canonical reference | Where in this repo |
|---------|----------------------|---------------------|--------------------|
| Reward hacking / specification gaming | Optimizing the letter, not the spirit, of the objective | Krakovna et al., "Specification gaming examples" (2018+); Amodei et al. 2016 | [risks/specification_gaming.md](../risks/specification_gaming.md) |
| Scalable oversight | Supervising outputs you can't evaluate yourself | Irving et al., debate (arXiv:1805.00899); Leike et al. RRM (arXiv:1811.07871) | [alignment/scalable_oversight.md](../alignment/scalable_oversight.md) |
| Distributive shift | Performance collapse off-distribution | Hendrycks et al. (arXiv:2109.13916) | [risks/](../risks/) |
| Deceptive alignment | The system behaves well *because* it is evaluated | Hubinger et al., sleeper agents (arXiv:2401.05566) | [risks/deceptive_alignment.md](../risks/deceptive_alignment.md) |
| Corrigibility | Accepting correction rather than resisting shutdown | Soares et al. 2015 | [alignment/open_problems.md](../alignment/open_problems.md) |

## Layer 2: Honesty (does it tell the truth?)

| Problem | Description | Evidence base |
|---------|-------------|---------------|
| Hallucination / confabulation | Fluent, confident falsehoods | TruthfulQA (arXiv:2109.07958); HaluEval (arXiv:2305.11747) |
| Sycophancy | Telling the user what they seem to want to hear | Perez et al. (arXiv:2212.09251); Sharma et al. (arXiv:2310.13548) |
| Miscalibration | Confidence not tracking correctness | OpenAI GPT-4 tech report (arXiv:2303.08774) §5 |

## Layer 3: Harmlessness (does it avoid damage?)

| Problem | Description | Evidence base |
|---------|-------------|---------------|
| Toxicity & hate | Generation of abusive content | RealToxicityPrompts (arXiv:2009.11462); ToxiGen (arXiv:2203.09509) |
| Bias & stereotyping | Group-differential quality or stereotyped completions | BOLD (arXiv:2101.11718); BBQ (arXiv:2110.05828); Winogender (arXiv:1804.09301) |
| Privacy leakage | Regurgitating training-data PII | Carlini et al., extraction attacks (arXiv:2012.07805) |
| Dangerous capability uplift | CBRN, offensive cyber, persuasion | OpenAI Preparedness Framework (2023); Anthropic RSP (2023) |

## Layer 4: System-level (does the *application* fail safely?)

The OWASP Top 10 for LLM Applications (2023; updated 2025) lives here —
prompt injection (LLM01), sensitive information disclosure (LLM06), excessive
agency (LLM08), insecure output handling (LLM02), and so on. See
[governance/owasp_llm_top10.md](../governance/owasp_llm_top10.md). NIST's
Generative AI Profile (NIST AI 600-1, July 2024) similarly lists 12
generative-AI risk categories including confabulation, information security,
and information integrity.

## Why layering matters for engineering

A production deployment fails at the *weakest* layer, and layers interact:
a well-aligned model behind an injection-prone RAG pipeline is unsafe
(Layer 4 failure); an honest model that happily produces PII is unsafe
(Layer 3 failure); a harmless model that sycophantically agrees with a
suicidal user is unsafe (Layer 2 failure). The `aisafety` package therefore
ships defenses at Layers 2–4: evaluation metrics, PII/injection/toxicity
filters, and a composable guardrail pipeline.
