# AI Safety

A practical, research-grounded toolkit and knowledge base for **AI safety**: building, evaluating, and governing machine-learning systems — with a focus on large language models (LLMs) — so they remain reliable, honest, harmless, and aligned with human intent.

This repository combines three things that are usually scattered across the field:

1. **Documentation** — a curated library covering alignment (RLHF, DPO, Constitutional AI), mechanistic interpretability, safety risks (hallucination, prompt injection, jailbreaks, bias, privacy leakage, deceptive alignment), governance frameworks (NIST AI RMF, EU AI Act, OWASP Top 10 for LLM Applications), and red-teaming methodology. Every page cites real papers, real incidents, and real public datasets.

2. **Tooling** — a Python package (`aisafety`) providing PII detection and redaction, prompt-injection detection, toxicity classification hooks, a composable guardrail pipeline, and evaluation metrics (refusal rate, over-refusal, compliance, truthfulness scoring).

3. **Benchmark harnesses** — reproducible evaluators built exclusively on real, public, widely-used datasets: [TruthfulQA](https://arxiv.org/abs/2109.07958), [GSM8K](https://arxiv.org/abs/2110.14168), [MMLU](https://arxiv.org/abs/2009.03300), [RealToxicityPrompts](https://arxiv.org/abs/2210.04210), [BOLD](https://arxiv.org/abs/2101.11718), [BBQ](https://arxiv.org/abs/2110.05828), [ToxiGen](https://arxiv.org/abs/2203.09509), [AdvBench](https://arxiv.org/abs/2307.15043), [XSTest](https://arxiv.org/abs/2308.01263), [Anthropic HH-RLHF](https://arxiv.org/abs/2204.05862), [BeaverTails](https://arxiv.org/abs/2307.04657), and [JailbreakBench](https://arxiv.org/abs/2404.01318).

## Why AI safety matters

Language models are now deployed in customer support, healthcare triage, hiring assistance, education, and software engineering. Each deployment inherits the model's failure modes: confident fabrication (hallucination), social bias, leakage of training-data PII, susceptibility to prompt injection and jailbreaks, and over-refusal that destroys usefulness. Recent real-world incidents — from the [Air Canada chatbot tribunal ruling](https://decisions.bccrt.ca/bccrt/2000464) (2024) to the [$25M deepfake CFO fraud in Hong Kong](https://arstechnica.com/security/2024/02/deepfake-cfo-scam-tricks-finance-worker-out-of-25-million/) — show these are operational risks, not hypothetical ones.

## Quick start

```bash
git clone https://github.com/AdilShamim8/AI-Safety.git
cd AI-Safety
pip install -e ".[dev]"
pytest                        # run the test suite
python examples/guardrail_quickstart.py
```

## Documentation map

| Area | Contents |
|------|----------|
| `docs/introduction/` | What AI safety is, taxonomy, history, key organizations |
| `docs/alignment/` | RLHF, DPO, Constitutional AI, scalable oversight, open problems |
| `docs/interpretability/` | Mechanistic interpretability, sparse autoencoders, activation steering |
| `docs/risks/` | Hallucination, prompt injection, jailbreaks, bias, privacy, misuse, deception |
| `docs/governance/` | NIST AI RMF, EU AI Act, OWASP LLM Top 10, ISO/IEC 42001 |
| `docs/red_teaming/` | Methodologies, attack taxonomies, disclosure practices |
| `docs/incidents/` | Documented real-world case studies (Tay, COMPAS, Bing/Sydney, and more) |
| `docs/datasets/` | Catalog of the real public datasets used by this project |

## License

MIT — see [LICENSE](LICENSE).
