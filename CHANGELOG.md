# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Guardrail pipeline presets for RAG and agent contexts
- Llama Guard 3 integration for policy-based classification
- Automated red-team corpus built from JailbreakBench artifacts

## [0.1.0] - 2026-10-20

### Added
- Documentation library: AI safety introduction & taxonomy, history, and
  organization landscape.
- Alignment guides: RLHF, DPO, Constitutional AI, scalable oversight, and
  open alignment problems.
- Interpretability guides: mechanistic interpretability, sparse
  autoencoders, activation steering.
- Risk guides: hallucination, prompt injection, jailbreaks, bias &
  fairness, privacy, misuse, deceptive alignment, specification gaming,
  over-refusal.
- Governance guides: NIST AI RMF, EU AI Act, OWASP LLM Top 10,
  ISO/IEC 42001, and a frameworks timeline.
- Red-teaming methodology and incident case-study library (real, cited
  events only).
- `aisafety` Python package: PII detection/redaction, prompt-injection
  detection, toxicity hooks, guardrail pipeline, evaluation metrics.
- Benchmark harnesses for real public datasets: TruthfulQA, BOLD,
  RealToxicityPrompts, AdvBench, XSTest.
- Dataset registry covering TruthfulQA, GSM8K, MMLU, BBQ, ToxiGen,
  HH-RLHF, BeaverTails, JailbreakBench, and more.
- Scripts for dataset download, benchmark execution, and report generation.
- Pytest suite and GitHub Actions CI.
