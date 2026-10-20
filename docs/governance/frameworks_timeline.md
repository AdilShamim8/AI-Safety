# Governance frameworks timeline

One page, chronological, so you can see the direction of travel:
voluntary → standardized → binding, with the measurement infrastructure
(benchmarks, evals) increasingly load-bearing for all of it.

| Date | Instrument | Type | One-line significance |
|------|-----------|------|----------------------|
| 2015 | Asilomar AI Principles (Future of Life Institute) | Voluntary principles | First mass-signed AI principles doc (8,000+ signatories incl. Hawking, Musk) |
| 2019 | OECD AI Principles | Intergovernmental | The reference taxonomy behind most later national policies |
| 2019 | Canada's Directive on Automated Decision-Making | Binding (federal procurement) | First algorithmic-impact-assessment regime |
| 2021 | EU "AI Act" proposal (COM(2021)206) | Draft regulation | Risk-pyramid structure introduced to lawmaking |
| 2023 Jan | NIST AI RMF 1.0 | Voluntary framework | The US vocabulary for AI risk management |
| 2023 Jun | China's Interim Measures for Generative AI Services | Binding | First generative-AI-specific national rules (effective Aug 15, 2023) |
| 2023 Oct | US EO 14110 | Executive order | Safety-test reporting duties for frontier training runs — **rescinded Jan 2025** |
| 2023 Oct | G7 Hiroshima Process Code of Conduct | Voluntary | OECD-aligned conduct for advanced AI orgs |
| 2023 Oct–Nov | Anthropic RSP / OpenAI Preparedness / DeepMind FSF | Corporate frameworks | Capability-tiered safety commitments with eval triggers |
| 2023 Nov | Bletchley Declaration (28 states + EU) | Intergovernmental | First AI-safety summit; institutes network begins |
| 2023 Nov | UK & US AI Safety Institutes | State institutions | Pre-deployment evaluation as a state function |
| 2023 Dec | ISO/IEC 42001 published | Certifiable standard | AI management systems certifiable |
| 2024 Mar | UN General Assembly AI resolution (A/78/L.49) | Consensus resolution | First global consensus AI text |
| 2024 May | Seoul Summit: Frontier AI Safety Commitments | Corporate commitments | 16 companies sign safety-framework commitments |
| 2024 Jul | NIST AI 600-1 (GenAI Profile) | Voluntary framework | The 12 GenAI risk categories + controls |
| 2024 Aug | EU AI Act in force (Reg. 2024/1689) | Binding regulation | Phased duties 2025–2027 |
| 2024 Sep | California SB 1047 vetoed | State bill (US) | Frontier-liability bill vetoed; the governance debate goes mainstream |
| 2024 Dec | Council of Europe Framework Convention on AI | Treaty | First binding international AI treaty (open for signature) |
| 2025 Jan | EO 14110 rescinded; "America's AI Action Plan" era | US policy shift | Federal posture moves from safety-testing to competitiveness |
| 2025 Feb | International AI Safety Report (Bengio) | Scientific assessment | IPCC-style standing report; Paris AI Action Summit |
| 2025 Feb | EU prohibited-practice prohibitions apply | Binding | Social scoring etc. banned in-market |
| 2025 Aug | EU GPAI obligations apply | Binding | Documentation/eval duties for foundation-model providers |
| 2025 Sep | California SB 53 signed | State law (US) | Frontier devs must publish safety frameworks + report incidents (effective 2026) |
| 2026 | EU high-risk full application (Aug 2) | Binding | Annex III conformity duties bite |
| 2026 | Colorado AI Act (SB 24-205) effective (Jun 30) | State law (US) | First comprehensive US state AI law (algorithmic-discrimination duties) |

## Reading the pattern

1. **Measurement is becoming mandatory.** Every binding instrument above
   (China's Measures, EU GPAI, SB 53) contains evaluation/adversarial-
   testing duties. Benchmarks graduate from research artifacts to
   compliance infrastructure — which is why this repo treats harness
   reproducibility as a governance feature.
2. **The US regulates by state & sector** after the EO rescission;
   California and Colorado effectively set national product standards
   (the "Brussels effect," Sacramento edition).
3. **Voluntary corporate frameworks converged on a template**:
   capability thresholds + eval triggers + graduated mitigations +
   incident reporting. RSP / Preparedness / FSF differ in details, not
   structure; SB 53 wrote that template into statute.
4. **The treaty layer (CoE Convention) is thin** — reporting and
   rights-based — but it's the first binding cross-border text, and its
   signatories will harmonize domestic law upward.

## For the working engineer

The compliance-relevant question for any LLM product in 2026 is three
lines long: *Who are your users (EU? CA? CO?), what tier does the product
fall in (GPAI deployer? high-risk Annex III? neither?), and where is
your evidence trail (evals, logs, incident records)?* Everything in this
directory exists to help answer the third.
