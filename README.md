# AI Safety

> A practical, research-grounded toolkit and knowledge base for **AI safety** —
> building, evaluating, and governing LLM systems so they stay reliable,
> honest, harmless, and aligned with human intent.

**What's inside:** a 30-page documentation library citing only real papers
and incidents · a stdlib-first Python safety toolkit (PII redaction,
prompt-injection detection, toxicity hooks, guardrail pipeline) ·
benchmark harnesses for 15 real public datasets · a 92-test pytest suite
and CI with security scanning.

---

## Why this exists

Language models now sit in customer support, hiring pipelines, healthcare
triage, and software engineering. Every deployment inherits the model's
failure modes: confident fabrication, social bias, training-data leakage,
prompt injection, jailbreaks, and the mirror-image failure — over-refusal
that makes products useless. The real incidents are documented and
citiable: the [Air Canada chatbot tribunal ruling](https://decisions.bccrt.ca/bccrt/2000464)
(2024), the [$25M Arup deepfake CFO fraud](https://www.cnn.com/2024/02/04/asia/hong-kong-deepfake-fraud/index.html)
(2024), [NYT v. OpenAI](https://www.nytimes.com/2023/12/27/business/media/new-york-times-open-ai-microsoft-lawsuit.html)
(2023). This repo turns that literature into runnable code and a
reviewable knowledge base.

## Quick start

```bash
git clone https://github.com/AdilShamim8/AI-Safety.git
cd AI-Safety
pip install -e ".[dev]"

make test                    # 92 tests, offline
python examples/guardrail_quickstart.py    # see the pipeline work
```

Evaluate a model (after downloading the real datasets):

```bash
python scripts/download_datasets.py --all
python scripts/run_benchmark.py xstest --model openai:gpt-4o-mini
python scripts/run_benchmark.py advbench --model openai:gpt-4o-mini
python scripts/generate_report.py
```

Smoke-mode runs (`--model refusal|echo`) validate plumbing without
spending API credits — their results are labeled as such, never as model
evaluations.

## The toolkit (`src/aisafety/`)

| Module | What it does | Maps to |
|--------|--------------|---------|
| `safety/pii/` | Email/phone/card/SSN/IP/API-key detection, Luhn validation, format-preserving redaction | OWASP LLM06 |
| `safety/injection/` | 11 documented injection-pattern rules with confidence scoring; exfiltration-link stripping | OWASP LLM01 |
| `safety/toxicity/` | Offline lexicon scorer + Perspective API backend, swappable | RealToxicityPrompts lineage |
| `safety/guardrails/` | Composable input/output pipeline, fail-closed by default | OWASP LLM02/08 |
| `evaluation/` | XSTest-style 3-way refusal taxonomy, compliance judge, Wilson-interval metrics | over/under-refusal parity |
| `data/` | Registry of 15 real datasets (license + paper + canonical ID) with lazy HF loaders | provenance discipline |

```python
from src.aisafety.safety.guardrails.pipeline import GuardrailPipeline

pipeline = GuardrailPipeline()
decision = pipeline.check_input(user_text, untrusted_context=retrieved_doc)
if decision.allowed:
    output = model(decision.text)
    safe_output = pipeline.check_output(output)
```

## Documentation map

| Area | Pages |
|------|-------|
| Introduction | [what is AI safety](docs/introduction/what_is_ai_safety.md) · [taxonomy](docs/introduction/taxonomy.md) · [history](docs/introduction/history.md) · [organizations](docs/introduction/key_organizations.md) |
| Alignment | [overview](docs/alignment/overview.md) · [RLHF](docs/alignment/rlhf.md) · [DPO](docs/alignment/dpo.md) · [Constitutional AI](docs/alignment/constitutional_ai.md) · [scalable oversight](docs/alignment/scalable_oversight.md) · [open problems](docs/alignment/open_problems.md) |
| Interpretability | [overview](docs/interpretability/overview.md) · [mechanistic](docs/interpretability/mechanistic.md) · [SAEs](docs/interpretability/saes.md) · [steering](docs/interpretability/steering.md) |
| Risks | [hallucination](docs/risks/hallucination.md) · [prompt injection](docs/risks/prompt_injection.md) · [jailbreaks](docs/risks/jailbreaks.md) · [bias & fairness](docs/risks/bias_fairness.md) · [privacy](docs/risks/privacy.md) · [misuse](docs/risks/misuse.md) · [deceptive alignment](docs/risks/deceptive_alignment.md) · [specification gaming](docs/risks/specification_gaming.md) · [over-refusal](docs/risks/over_refusal.md) |
| Governance | [NIST AI RMF](docs/governance/nist_ai_rmf.md) · [EU AI Act](docs/governance/eu_ai_act.md) · [OWASP LLM Top 10](docs/governance/owasp_llm_top10.md) · [ISO 42001](docs/governance/iso_42001.md) · [timeline](docs/governance/frameworks_timeline.md) |
| Practice | [red teaming](docs/red_teaming/overview.md) · [methodologies](docs/red_teaming/methodologies.md) · [incident case studies](docs/incidents/case_studies.md) · [dataset catalog](docs/datasets/index.md) |
| Engineering | [ARCHITECTURE.md](ARCHITECTURE.md) · [ROADMAP.md](ROADMAP.md) · [CHANGELOG.md](CHANGELOG.md) · [data policy](data/README.md) |

## Real datasets referenced (all public)

TruthfulQA (817 Qs) · MMLU (57 subjects) · GSM8K (8.5k problems) ·
BBQ (~58k bias Qs) · BOLD (43,623 prompts) · Winogender (720 pairs) ·
CrowS-Pairs (1,508 pairs) · ToxiGen (274k statements) ·
RealToxicityPrompts (100k prompts) · HH-RLHF (~170k comparisons) ·
BeaverTails (~330k annotations) · AdvBench (520 behaviors) ·
XSTest (250+200 prompts) · JailbreakBench (100 behaviors) · SimpleQA —
full catalog with licenses and access points:
[docs/datasets/index.md](docs/datasets/index.md).

## Contributing & license

- Contribution guide with evidence standards: [CONTRIBUTING.md](CONTRIBUTING.md)
- Security policy & threat model: [SECURITY.md](SECURITY.md)
- MIT license: [LICENSE](LICENSE)
- Cite the repo: see [CITATION.cff](CITATION.cff)
