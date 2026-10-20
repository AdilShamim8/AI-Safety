# OWASP Top 10 for LLM Applications

OWASP's **Top 10 for LLM Applications** is the application-security
checklist for LLM systems — the one security review your product will
actually be run against. First released **2023**; the **2025 revision**
reshuffled entries to track the field. Both are documented below since
most audits still cite the 2023 list.

## The 2023 list

| # | Risk | One-line description | Primary control |
|---|------|----------------------|-----------------|
| LLM01 | **Prompt Injection** | Untrusted text overrides instructions | Delimiter/spotlighting, output handling, least agency |
| LLM02 | **Insecure Output Handling** | Model output treated as trusted/executeable | Encode, never `eval`, escape per downstream (SQL/HTML/shell) |
| LLM03 | **Training Data Poisoning** | Malicious data alters model behavior | Supply-chain provenance, dataset auditing, canaries |
| LLM04 | **Model Denial of Service** | Resource exhaustion via crafted inputs | Rate limits, token caps, timeout/retry budgets |
| LLM05 | **Supply Chain Vulnerabilities** | Poisoned weights/plugins/SDKs | Pin & verify artifacts, SBOMs, weight provenance |
| LLM06 | **Sensitive Information Disclosure** | PII/secrets in output or logs | PII redaction (this repo's `safety/pii/`), output filtering, retention limits |
| LLM07 | **Insecure Plugin Design** | Plugins trust model-controlled arguments | Input validation at plugin boundary, per-action authz |
| LLM08 | **Excessive Agency** | Too much permission, too much autonomy | Allow-listed actions, human-in-the-loop, blast-radius caps |
| LLM09 | **Overreliance** | Hallucinated content trusted by users/other systems | Disclaimer + citation UX, verifier steps, calibration |
| LLM10 | **Model Theft** | Exfiltration of weights/IP | Access control, weight encryption, watermarking |

## What changed in 2025

The **2025 edition** (released ~late 2024/2025 per OWASP GenAI Security
Project) restructures around what matured: **System Prompt Leakage**
became its own entry (LLM07); **Vector & Embedding Weaknesses** (poisoned
RAG corpora, embedding inversion) entered at LLM08; **Misinformation**
(formerly overreliance) and **Unbounded Consumption** (resource abuse)
renamed/reframed; agent-specific concerns (multi-agent chains) appear in
companion guidance. Prompt injection stays **LLM01** — the field's most
stable fact.

## Engineering the checklist (what each item means in code)

1. **LLM01/LLM07 — boundary discipline.** Every place untrusted text
   enters a prompt (user input, retrieved docs, tool outputs, *other
   models' outputs*) goes through marking/spotlighting and an injection
   detector (this repo: `safety/injection/detector.py`).
2. **LLM02 — output is hostile until proven inert.** No `eval`, no
   shell-out, no SQL string-building from generations; renderers strip
   remote images/links (the markdown-exfil class); downstream parsers
   validate against schemas.
3. **LLM03/LLM05 — pin the supply chain.** Model artifacts by hash;
   datasets by revision (HF `revision=` pinning — the repo's loaders do
   this); plugins least-privileged; SBOM for the whole stack.
4. **LLM04/Unbounded Consumption — budgets everywhere.** Token limits,
   per-key quotas, recursion caps in agent loops (an agent stuck in a
   self-prompting loop is both DoS and cost attack).
5. **LLM06 — redact at the boundary.** PII detection on outputs that
   touch logs, third-party APIs, or humans (repo: `safety/pii/`);
   secrets-scanning on generations (models *do* emit training-data API
   keys — documented in the memorization literature, see
   [risks/privacy.md](../risks/privacy.md)).
6. **LLM08 — agency is the blast radius.** The agent gets *intent*,
   deterministic code gets *action*; every privileged action has an
   allow-list, rate cap, and (above a threshold) a human gate.
7. **LLM09 — design for verification.** Citations, confidence surfacing,
   and "checks before effects" (diff-review, dry-run modes) for anything
   consequential.
8. **LLM10 — treat weights like production secrets.** Access tiers,
   audit logs, egress monitoring; for open-weights strategy, document
   what threat that decision accepts.

## How to run a review

Walk the product's dataflow once with this page open and mark every edge
where: untrusted text → prompt (LLM01), generation → execution/ingestion
(LLM02), credentials → agent reachability (LLM08). Those three cover the
majority of real LLM app incidents to date (see
[incidents/case_studies.md](../incidents/case_studies.md) for the
supporting cases: Bing prompt leaks, chatbot SQL/UI injection cases, the
Chevrolet $1 Tahoe, and DPD's rogue bot).
