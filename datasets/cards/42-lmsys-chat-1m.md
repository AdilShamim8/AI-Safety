# Dataset card: LMSYS-Chat-1M

LICENSE observed at the live Hugging Face page on 2026-10-27: the
dataset is **gated** behind a custom **LMSYS-Chat-1M Dataset License
Agreement** (acceptance form with name/email/affiliation/country); the
agreement grants a limited, non-exclusive, non-transferable,
non-sublicensable license to use the dataset "for both research and
commercial purposes," subject to restrictions including
non-identification of individuals — **no ODC-BY statement appears
anywhere on the page; the earlier "ODC-BY family" note was a
paper-stated guess and is corrected here** · verification dates:
arXiv abstract 2026-10-25 (API); license page 2026-10-27 (page
inspected) · prepared by the course build · status: card at
abstract-read + license-page-inspected level

## 1. Identity and provenance

- **What it is:** a large-scale dataset of **one million real-world
  conversations with 25 state-of-the-art LLMs**, collected from
  **210K unique IP addresses** "in the wild" on the Vicuna demo and
  Chatbot Arena websites — the abstract's own scale facts, quoted.
- **Canonical home:** "LMSYS-Chat-1M: A Large-Scale Real-World LLM
  Conversation Dataset" (Zheng et al., arXiv:2309.11998,
  2023-09-21, API-verified 2026-10-25); distributed via Hugging
  Face under the project's open terms with a released sample.

## 2. Composition (abstract-stated)

- 1M conversations; 25 LLMs; 210K unique IPs; the wild-collection
  framing (not curated, not prompted by researchers). Language
  distribution, prompt categories, and the released-sample protocol:
  body-level, **unclaimed** here.

## 3. Collection and labeling

- Organic user traffic — the supply tier
  [comparison 12](../../research/notes/comparison-12-evaluation-supply-strategies.md)
  would call *found data*: no generation, no curation, distribution
  as-it-happened. That is both the value (real deployment-shaped
  usage) and the governance burden (the paper's own release notes
  on safety review and the redaction protocol — noted as existing,
  detail body-level).
- Course-relevant: what people actually ask is the distribution
  every deployed safety claim is about; curated sets measure what
  researchers thought to ask. WildChat (card 12)
  is the same instrument family; the two cards cross-reference.

## 4. Splits and leakage discipline

- The contamination direction is inverted: this is *training-side*
  found data — any model trained on it has seen real usage
  distributions; evaluation uses must respect the license and the
  paper's own usage guidelines (recorded as the card's honest
  pointer, uninspected).

## 5. Where the course uses it

- **Ch. 02/21:** the real-usage distribution reference — sampling
  frames for deployment-representative evaluation and the
  exposure analysis (who asks what).
- **P01/P09:** the "wild" arm of any coverage analysis — curated
  case families versus found-distribution slices, reported side by
  side.

## 6. Honest limitations (this card)

- License page inspected 2026-10-27 (see header): gated custom
  agreement, not ODC-BY. The raw README sits behind the gate, so the
  agreement text was read from the rendered public page. Language
  mix, category taxonomy, and the redaction protocol body-level; no
  content quoted or redistributed (the standing policy for all
  cards).
