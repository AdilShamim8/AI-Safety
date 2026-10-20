# AI Safety Documentation

This documentation library is written for engineers and reviewers who need to
*deploy* large language models responsibly, not just read about the field.
Every page cites primary sources: peer-reviewed papers (arXiv/DOI where
available), official regulatory texts, and documented real-world incidents.

## Reading order

New to the field? Read in this order:

1. [What is AI safety?](introduction/what_is_ai_safety.md) — definitions and scope
2. [A taxonomy of AI safety problems](introduction/taxonomy.md) — the map of the territory
3. [A short history](introduction/history.md) — from Asilomar 1975 to frontier-lab safety frameworks
4. [Key organizations](introduction/key_organizations.md) — who does what

Then dive into practice areas:

## Practice areas

| Area | Pages | Start here |
|------|-------|------------|
| Alignment | [overview](alignment/overview.md), [RLHF](alignment/rlhf.md), [DPO](alignment/dpo.md), [Constitutional AI](alignment/constitutional_ai.md), [scalable oversight](alignment/scalable_oversight.md), [open problems](alignment/open_problems.md) | Techniques for making models want the right things |
| Interpretability | [overview](interpretability/overview.md), [mechanistic](interpretability/mechanistic.md), [sparse autoencoders](interpretability/saes.md), [steering](interpretability/steering.md) | Understanding what models compute and how to intervene |
| Risks | [hallucination](risks/hallucination.md), [prompt injection](risks/prompt_injection.md), [jailbreaks](risks/jailbreaks.md), [bias & fairness](risks/bias_fairness.md), [privacy](risks/privacy.md), [misuse](risks/misuse.md), [deceptive alignment](risks/deceptive_alignment.md), [specification gaming](risks/specification_gaming.md), [over-refusal](risks/over_refusal.md) | The failure-mode catalog |
| Governance | [NIST AI RMF](governance/nist_ai_rmf.md), [EU AI Act](governance/eu_ai_act.md), [OWASP LLM Top 10](governance/owasp_llm_top10.md), [ISO/IEC 42001](governance/iso_42001.md), [timeline](governance/frameworks_timeline.md) | Rules and standards you may be accountable to |
| Red teaming | [overview](red_teaming/overview.md), [methodologies](red_teaming/methodologies.md) | Finding failures before users do |
| Incidents | [case studies](incidents/case_studies.md) | 15+ documented real-world failures and what they teach |
| Datasets | [catalog](datasets/index.md) | The real public datasets this project's harnesses use |

## Editorial standards

- **Primary sources only.** Claims about papers cite the arXiv ID; claims
  about incidents link to reporting or filings; claims about regulations link
  to official texts.
- **No invented numbers.** Dataset sizes, benchmark results, and dates are
  taken from the cited source or omitted.
- **Defensiveness about recency.** The field moves fast; pages record the
  "as known" date of key facts in their footnotes.
