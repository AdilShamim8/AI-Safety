# Roadmap

Planned work, in rough priority order. Items are scoped against the
open-problems page (`docs/alignment/open_problems.md`): this repo builds
*measurement and mitigation* tooling; it does not claim to solve them.

## v0.2 — guardrail depth

- [ ] Llama Guard 3 integration as a `toxicity` backend
      (policy categories S1–S14, arXiv:2312.06674)
- [ ] OpenAI Moderation API backend (free tier) with cached mode
- [ ] Injection detector v2: context-aware scoring (position of payload,
      instruction-distance weighting) + published WIPI-style eval
- [ ] Multi-turn guardrail state: track Crescendo-style drift across a
      conversation, not just single turns
- [ ] Rate-limit + anomaly hooks for agent loops (OWASP unbounded
      consumption)

## v0.3 — benchmark coverage

- [ ] BBQ harness (bias under ambiguity, arXiv:2110.05828)
- [ ] Winogender coreference harness (arXiv:1804.09301)
- [ ] JailbreakBench artifacts integration (100-behavior set, v2)
- [ ] TruthfulQA generation mode with LLM-judge (validated on 100
      human-labeled samples first, per the repo's judge policy)
- [ ] Many-shot jailbreak probe (long-context ASR curve,
      arXiv:2405.18678) behind an ethics flag

## v0.4 — evaluation infrastructure

- [ ] Result store with schema versioning + diffing between runs
- [ ] Statutory-reporting export (EU AI Act Art. 55-style evidence
      bundles: eval records + red-team findings + incident log)
- [ ] Contamination canaries for derived eval sets (GSM8K practice)
- [ ] Weak-to-strong style consistency checks for LLM-judged metrics

## v1.0 — production hardening

- [ ] 1.0 API freeze for the guardrail pipeline with deprecation policy
- [ ] Performance benchmarks for filters (targets: <5ms per KB text,
      regex ReDoS audits published)
- [ ] Deployment guides: FastAPI middleware, LangChain/LlamaIndex
      adapters, gateway sidecar
- [ ] External audit of the toolkit itself (the eval harness needs eval)

## Standing rules (not scheduled — always)

- Every new benchmark must cite its dataset's license and pin revisions
- Every new filter must ship tests + a doc page mapping to the risk
  taxonomy
- No fabricated numbers; smoke-backbone results must carry the disclaimer
  (already enforced in `scripts/run_benchmark.py` output)
