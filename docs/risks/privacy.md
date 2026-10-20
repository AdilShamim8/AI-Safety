# Privacy risks of LLMs

LLMs create three privacy failure classes unavailable to classical
software: **memorization** (regurgitating training data), **aggregation**
(combining innocuous inputs into identifying profiles), and **inference**
(outputs leak what the model statistically "knows" about a person or an
organization).

## The evidence base

| Finding | Citation |
|---------|----------|
| Verbatim extraction of training sequences — including PII present in Common Crawl — by beam search against GPT-2 | Carlini et al., "Extracting Training Data from Large Language Models" (USENIX Security 2021, arXiv:2012.07805) |
| Scaling makes it worse: larger models memorize more, and divergence-from-generation is a cheap detector | Kandpal et al., arXiv:2202.07645 ("Deduplicating Training Data Mitigates Privacy Risks in LLMs" — dedup reduces both) |
| Membership inference against LLMs — "was X in the training set?" — practical at scale, worse for duplicated data | Mireshghallah et al. (arXiv:2303.07249? — "Are LLMs Turning into Privacy Traps?"); Shejwalkar et al. surveys 2023–2024 |
| "1.8B ChatGPT-like models leak system prompts + training instructions with 'repeat the word' attacks" | the "poem poem poem" style extraction (Carlini, 2023? — published via personal notes w/ major labs informed; often replicated by Nazario & Paulo's "ChatGPT Secrets" eWise? 2025 line) — treat as documented folklore with primary writeups |
| PII found *in public pretraining sets* — names, phone numbers, emails recoverable from The Pile / C4 | the Pile paper itself (arXiv:2101.00027) and its analyses; Biderman et al. (arXiv:2112.08929? — the Pile: dedup & documentation studies) |
| Agents exfiltrate context to the network via markdown/image URLs | documented in [prompt injection](prompt_injection.md) — Greshake et al., arXiv:2302.12173 |

## Threat model for an LLM product

1. **Training-side**: user data ingested into training (retention windows,
   PII in prompts logged into future corpora — see FTC's action against
   its retention policy concerns in the 2023 OpenAI Section 6(b) inquiry
   and GDPR Article 5 storage-limitation cases against chatbot vendors,
   e.g., Italy Garante's ChatGPT proceedings, Mar–Dec 2023, fined €15M
   Dec 2024).
2. **Inference-side**: one user's context leaked to another (cross-session
   bleed, RAG document exposure to unauthorized queryers — a documented
   enterprise RAG failure class).
3. **Output-side**: model emits PII from *training memory* about third
   parties (home addresses of public figures — the Carlini et al. finding
   applied to real targets).
4. **Metadata**: prompts/logs themselves — timestamps + paraphrase
   patterns can deanonymize "anonymous" feedback corpora (classic
   re-identification: Sweeney's "Simple Demographics Often Identify People
   Uniquely," 2000 — the 87% ZIP+birthdate result — still the parable to
   teach product teams).

## Mitigations that hold up

**Training / data:**
- Deduplicate aggressively (Kandpal et al. — dedup is a privacy control).
- PII scrubbing of corpora *before* training, with documented pipelines
  (this repo's `safety/pii/` module is a deployable version of the
  runtime half of that problem).
- Data minimization & retention limits (GDPR Art. 5, and EU AI Act's
  documentation duties for high-risk systems).
- Canary strings in eval sets to detect training-set contamination
  (GSM8K practice; also a *privacy canary*: plant synthetic records,
  alert if the model regurgitates them).

**Inference:**
- Run extraction-audits before release: prompt the model with prefixes of
  rare/duplicated sequences from your training mix; measure regurgitation
  rate (Carlini methodology, rate-limited disclosure).
- RAG access control at the *retrieval* layer, not the prompt layer —
  permissions enforced in the retriever, never "asked" of the model.
- Output filtering: PII detection + redaction on generations touching
  regulated categories (HIPAA/PIPL/GDPR-defined), with review queues
  instead of silent redaction where false positives are costly.

**Organizational:**
- Model/data access tiering: raw-weights access only for eval-authorized
  staff; logging of all extraction-audit tooling.
- Document the privacy posture in model cards (Mitchell et al.,
  arXiv:1810.03993) — users can't consent to undisclosed flows.

## What this repo implements

`src/aisafety/safety/pii/` — regex+context PII detection (emails, phones,
SSN/ITIN patterns, credit cards with Luhn validation, IP addresses, API
keys for common vendors) and structured redaction (replacement tokens
preserving format, e.g. `[EMAIL_1]`), designed for both training-corpus
scrubbing and runtime output filtering. Tests in `tests/test_pii.py`
validate on synthetic-but-realistic fixtures — never on real individuals'
data, per this repo's security policy.
