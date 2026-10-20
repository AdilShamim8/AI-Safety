# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Llama Guard 3 toxicity backend (v0.2 — see ROADMAP.md)
- BBQ and Winogender bias harnesses
- Multi-turn guardrail state against Crescendo-style drift
- JailbreakBench artifacts integration

## [0.1.0] - 2026-10-20

### Added — Documentation library (33 pages, citation-first)
- Introduction: AI safety definitions & Concrete Problems framing, risk
  taxonomy, history (Wiener 1960 → SB 53 2025), organization landscape.
- Alignment: overview, RLHF pipeline & failure modes, DPO & variant zoo,
  Constitutional AI / RLAIF, scalable oversight (debate, amplification,
  weak-to-strong), open problems list.
- Interpretability: tool landscape, mechanistic interpretability,
  sparse autoencoders (variants, releases, failure modes), activation
  steering with dual-use analysis.
- Risks (9 pages): hallucination, prompt injection, jailbreaks, bias &
  fairness, privacy, misuse, deceptive alignment, specification gaming,
  over-refusal.
- Governance: NIST AI RMF + GenAI Profile, EU AI Act, OWASP LLM Top 10
  (2023 + 2025 editions), ISO/IEC 42001, frameworks timeline.
- Red teaming: evidence base, organizational patterns, attack-class
  playbook, structured finding template.
- Incidents: 20+ real cited cases (Tay, COMPAS, toeslagenaffaire, Bing/
  Sydney, Chevrolet, Air Canada, DPD, Arup deepfake, and more).
- Datasets: catalog of 15 real public datasets with licenses and
  canonical access points.

### Added — `aisafety` package (stdlib-first)
- PII: detection (email/phone/card/SSN/IP/API-keys, Luhn validation) +
  format-preserving redaction.
- Injection: 11 documented pattern rules, confidence scoring, risk
  aggregation.
- Toxicity: offline lexicon backend + Perspective API backend.
- Guardrails: composable input/output pipeline, fail-closed semantics,
  markdown-exfiltration stripping.
- Evaluation: XSTest 3-way refusal taxonomy, compliance judge (pattern +
  LLM-grader backends), Wilson-interval metrics.

### Added — Benchmarks, scripts, examples
- Harnesses on real datasets: TruthfulQA (MC1), BOLD (group disparity),
  RealToxicityPrompts, AdvBench (ASR), XSTest (parity gap).
- Scripts: dataset downloader (canonical sources), benchmark runner CLI
  (echo/refusal/openai/file backends), Markdown report generator with
  provenance table.
- Examples: guardrail quickstart, PII redaction demo, evaluation demo.

### Added — Quality infrastructure
- 92-test pytest suite (offline; synthetic fixtures only).
- CI: multi-Python tests + coverage, ruff/black, whole-tree syntax gate,
  internal doc-link checker.
- Security: gitleaks secret scan, pip-audit, CodeQL; dependabot.
- Pre-commit hooks; py.typed marker; CITATION.cff; data usage policy.
