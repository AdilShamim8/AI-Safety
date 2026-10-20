# The EU AI Act

**Regulation (EU) 2024/1689** — the AI Act — is the first comprehensive
AI law in a major jurisdiction. Entered into force **August 1, 2024**, it
phases obligations in through 2026–2027. If you deploy LLM products to
EU users, this is your compliance perimeter.

## The risk pyramid

| Tier | Examples | Duty |
|------|----------|------|
| **Unacceptable (prohibited)** | Social scoring by governments; manipulative techniques causing harm; untargeted facial-image scraping; emotion recognition in workplaces/schools; certain predictive policing; real-time remote biometric identification (with exceptions) | Banned from **Feb 2, 2025** |
| **High-risk** | Annex III systems: employment/hiring, credit, education grading, essential services, law enforcement, migration, critical infrastructure; Annex I safety products | Conformity assessment, data governance, logging, human oversight, post-market monitoring — full application **Aug 2, 2026** (with some Aug 2027 dates for regulated products) |
| **Limited-risk transparency** | Chatbots ("you are talking to AI"), deepfakes ("synthetic content" labels), emotion-sensitive systems | Disclosure duties, phased from Aug 2026 |
| **Minimal** | Everything else | Voluntary codes |

## The GPAI / foundation-model chapter (most relevant to LLM work)

General-purpose AI model providers owe duties that began applying
**August 2, 2025**:

- **All GPAI providers**: technical documentation, copyright-policy
  compliance (with the TDM opt-out regime), training-data summaries,
  information to downstream deployers.
- **Systemic-risk GPAI** (training compute > 10^25 FLOPs presumption, or
  EU-designated): model evaluations (including adversarial testing),
  systemic-risk assessment and mitigation, incident reporting,
  cybersecurity — with a **Code of Practice** route (the Commission's
  GPAI Code of Practice, finalized 2025) or equivalent internal
  documentation.

Fines: up to **€35M / 7% of global turnover** for prohibited practices;
€15M / 3% for most other violations.

## What this means for an engineering team (practical translation)

1. **Are you a deployer, provider, or both?** Putting your brand on a
   model, or substantially modifying one, makes you a *provider* — the
   heavier duty set. Fine-tuning counts.
2. **Logging is a legal requirement**, not telemetry hygiene: high-risk
   systems must automatically keep records for post-market monitoring
   for the regulation's periods; design retention in from day one.
3. **Human oversight must be real**: someone empowered to overrule the
   system, with the competence and information to do so — "we have an
   approval checkbox" has been the compliance failure of every earlier
   product-liability regime; expect the same enforcement pattern.
4. **Evals-as-evidence**: systemic-risk duties translate to running
   adversarial testing and documenting it — public benchmarks
   (TruthfulQA, BBQ, XSTest-style) plus internal red-team corpora, with
   versioned artifacts. This is the same evidence set NIST-RMF and lab
   RSPs consume.
5. **Copyright & data documentation**: training-data summaries and
  TDM-opt-out respect are GPAP duties with active rightsholder litigation
  around them (NYT v. OpenAI & Microsoft, filed Dec 27, 2023; Getty v.
  Stability AI, filed Jan 2023 — still the leading cases at time of
  writing).

## Interactions to track

- **GDPR**: AI Act assumes GDPR compliance underneath it; automated
  decision-making (Art. 22 GDPR) duties compound with high-risk
  classification.
- **DSA**: platform duties for recommender/synthetic content
  distribution.
- **Product liability revision** (PLD 2024/2853, applying 2026): software
  & AI explicitly in scope — deployer documentation becomes liability
  evidence.
- **Enforcement bodies**: national AI authorities per member state +
  the EU AI Office for GPAI codes; complaint channels open early
  (Feb 2025 for prohibited-practice violations).

## Sources (primary)

- Regulation text: EUR-Lex, Regulation (EU) 2024/1689.
- Commission AI Office pages: GPAI Code of Practice, template
  documentation guidelines.
- Implementation timeline as applied: EU official journal phased
  application dates (Feb 2, 2025; Aug 2, 2025; Aug 2, 2026; Aug 2,
  2027).

This page tracks the Act as it stood entering late 2026 — implementing
acts and codes continue to land; check EUR-Lex for amendments before
relying on any specific date.
