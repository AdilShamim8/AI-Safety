# Key organizations in AI safety

Who actually does safety work, and what are they known for? (Snapshot of
major players; roles evolve quickly in this field.)

## Frontier labs (internal safety teams)

| Organization | Safety org | Known for |
|--------------|-----------|-----------|
| Anthropic | Core safety; alignment science; interpretability | Constitutional AI (arXiv:2212.08073), HH-RLHF dataset, Responsible Scaling Policy with ASL levels, mechanistic interpretability (transformer-circuits.pub), sleeper-agents research (arXiv:2401.05566) |
| OpenAI | Preparedness; safety systems | GPT-4 system card & dangerous-capability evals (arXiv:2303.08774), Moderation API, Preparedness Framework (2023), weak-to-strong generalization (arXiv:2312.09390) |
| Google DeepMind | Safety & alignment; responsibility | Frontier Safety Framework, AI Safety Gridworlds (arXiv:1711.09883), concrete-problems agenda, Gemma Shield safety classifiers |
| Meta | Fundamental AI research | Llama open weights, Llama Guard classifiers (arXiv:2312.06674), Purple Llama cyber-safety suite |
| Microsoft | Office of Responsible AI; research | Jailbreak detection tooling; "Crescendo" multi-turn jailbreak research (2024); deployment governance for OpenAI models |

## Government & standards bodies

| Body | Role |
|------|------|
| **NIST** (US) | AI Risk Management Framework 1.0 (Jan 2023) and Generative AI Profile AI 600-1 (Jul 2024); hosts the US AI Safety Institute (est. Nov 2023) |
| **UK AI Safety Institute** (AISI) | First dedicated state safety institute (Nov 2023); publishes model-evaluation and safeguards guidance; pre-deployment testing agreements with labs |
| **European Commission / AI Office** | EU AI Act administration (Reg. 2024/1689); GPAI codes of practice |
| **ISO/IEC JTC 1/SC 42** | ISO/IEC 42001:2023 (AI management systems), 23894:2023 (AI risk management) |
| **OECD.AI** | OECD AI Principles (2019, updated 2024) — the reference taxonomy behind many national policies |
| **MLCommons** | AI Safety working group; AILuminate hazard benchmarks for chat assistants (2024–2025) |

## Research nonprofits & academia

| Organization | Focus |
|--------------|-------|
| Center for AI Safety (CAIS) | US-based; the 2023 extinction-risk statement; compute infrastructure for safety research |
| Future of Life Institute (FLI) | MIT-affiliated; the 2023 six-month pause letter; policy work (shut down Jan 2025 — its archive remains a key primary source) |
| Alignment Research Center (ARC) | Elicitation of latent knowledge; early GPT-4 dangerous-capability evaluations |
| METR (Model Evaluation & Threat Research) | Time horizons of agentic tasks; hazardous-capability evaluations for labs |
| Apollo Research | Model honesty and in-context deception evals — demonstrated sandbox deception in frontier reasoning models (2024) |
| Redwood Research | Alignment for deceptive models; control methods |
| MIRI | Formal agent foundations (corrigibility, decision theory) |
| CHAI (Berkeley) / Stuart Russell's group | Assistance games / CIRL |
| Stanford CRFM / HAI | HELM evaluation framework; Foundation Model Transparency Index |
| MATS (ML Alignment & Theory Scholars) | The field's main talent pipeline: places researchers with safety mentors |

## Industry consortia

- **Partnership on AI** — safety grants, red-teaming guidance.
- **Frontier Model Forum** (Anthropic, Google, Microsoft, OpenAI, later
  others) — best-practice sharing; safety research fund.
- **Network of AI Safety Institutes** — UK, US, Japan, Singapore, Canada
  and others coordinating evaluations post-Seoul 2024.

## Caveat

Organizational roles shift quickly: safety teams reorganize, individuals
move between labs, and funding situations change. Treat this page as a map
of *functions that must exist somewhere* (capability evals, interpretability,
policy, red-teaming, standards) more than a stable directory.
