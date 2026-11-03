# The CampusX course × the glossary

**Navigate:** [← the CampusX companion](README.md) · [crosswalk: chapters](crosswalk-chapters.md)

*Part of the [CampusX companion](README.md) · 2026-11-03 · the 14
terms the course prompted, each now carried as a row in
[GLOSSARY.md](../../GLOSSARY.md) with the chapters that use it.*

| Term | One-line meaning | Taught in lesson | Glossary chapters |
|---|---|---|---|
| **Guardrails (LLM applications)** | The engineering layers placed around an LLM application's channels — input, retrieval, prompt, tool, memory, output — each closing a named attack; the construction discipline of securing component by component. | all modules | 13, 14, 22 |
| **Input guardrails** | The gate on the user-query channel that stops jailbreaks before the query reaches the retriever or the LLM. | 3.04 | 13, 12 |
| **Output guardrails** | The last-check layer on the answer channel — every answer checked for private data, wrong facts, or a manipulated response before it reaches the user; built with NVIDIA NeMo Guardrails in the course. | 3.05 | 13, 08 |
| **Guard model** | A separate model that reads traffic and blocks by rule — on the conversation (the jailbreak gate) or on every tool and MCP result — so the defense does not share the protected model's context. | 4.01, 4.02 | 14, 08 |
| **PII masking** | Detection and redaction/tokenization of personal identifiers in the ingestion path, so customers' personal data never reaches the vector database. | 3.02 | 16 |
| **Pre-retrieval metadata filtering** | Authorization enforced as metadata filtering that blocks restricted documents BEFORE the search runs — the search never touches what the requester may not see. | 3.03 | 13, 14 |
| **Delimiter defense** | Retrieved documents delivered inside explicit boundaries with a system prompt that treats them as data, never instructions — the defense against injection from retrieved content. | 3.04 | 13, 14 |
| **Data Flow Diagram (DFD)** | The map of an LLM application's components and flows — every entry and exit point and trust boundary — the first step of the threat-modelling framework. | 2.04, 3.01 | 13, 01 |
| **Capability table** | The instrument that prices every component by what it can read, write, execute, or reach — turning a diagram into a risk list. | 2.04, 3.01 | 14, 01 |
| **Jailbreak gate** | The conversation-level guard: a separate model reading every message with recent turns inside delimiters, blocking authority claims, other people's data, and rule-override attempts. | 4.02 | 14, 12 |
| **Trust boundary** | A line in the diagram where data crosses between levels of trust — the boundaries the framework draws before any weak point is named. | 2.04, 3.01 | 13, 16 |
| **Shared memory (agent)** | The agent's cross-session store of past conversations — a write surface: personal data and poisoned lessons must never reach it, which is why a judge checks every write. | 4.01 | 14 |
| **Promptfoo** | The open-source red-team harness the course uses to grade the secured stack — attack prompts as cases, the security layers as the code under test, results as a per-layer report. | 3.06 | 15, 02 |
| **Multimodal attack surface** | Images, files, and other non-text inputs as attack paths that text-only defenses miss — every input channel added is a new way in. | 1.01, 1.02 | 19, 13 |

The glossary rows carry the full definitions with aliases,
common confusions, and chapter mappings; this table is the
course-to-glossary index.

Pairs across the library: guardrails (the layers) pair with prompt injection and jailbreaking (the attacks they close); PII masking pairs with data minimization and anonymization (session 10's rows); the guard model pairs with safeguard models (the research-side term); pre-retrieval filtering pairs with authorization itself; the capability table pairs with threat modelling (the discipline); and the per-layer red-team report pairs with red teaming and evaluation science. Each pair is the practitioner term and the research term for the same object.
