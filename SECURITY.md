# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.1.x   | yes       |

## Reporting a vulnerability

We treat security issues in this repository seriously, including issues that
would only matter when the tooling is deployed in production (e.g., a regex
ReDoS in the PII detector, SSRF in a dataset loader, or unsafe deserialization).

**Please do not open public issues for vulnerabilities.** Instead, use
GitHub's **private vulnerability reporting** on this repository
(*Security → Report a vulnerability*). Include:

1. A description of the issue and its impact.
2. Steps or proof-of-concept to reproduce it.
3. Affected versions and configurations.
4. Any suggested mitigation.

We aim to acknowledge reports within 72 hours and to ship a fix or documented
mitigation within 30 days for confirmed issues.

## Scope — AI-specific threats we track

This project's threat model (aligned with the OWASP Top 10 for LLM
Applications and the NIST AI RMF) explicitly considers:

- **Prompt injection and indirect prompt injection** against any code in this
  repo that feeds untrusted text into an LLM call.
- **Training-data and dataset supply-chain risks** — loaders must pin dataset
  revisions and must not execute arbitrary code from dataset cards.
- **PII handling** — anything committed to the repository must not contain
  personal data; demo fixtures use synthetic or public-benchmark text only.
- **Sandboxing of evaluation harnesses** — benchmark code assumes the model
  under test is adversarial; outputs are never `exec`'d or `eval`'d.

## Out of scope

- Vulnerabilities in third-party model APIs (report to the vendor).
- DoS requiring impractical volumes of traffic.
- Social-engineering attacks against repository maintainers.
