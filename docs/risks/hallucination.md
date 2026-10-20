# Hallucination (confabulation)

"Hallucination" is the field's standard term for fluent, confident output
that is false or unsupported by the input or world. In medicine and law the
preferred word is *confabulation*, and in high-stakes deployment language
matters: a model that fabricates case citations (as in *Mata v. Avianca*,
2023 — see [incidents/case_studies.md](../incidents/case_studies.md)) is
not "creative," it is generating liabilities.

## Why it happens (the real mechanisms)

1. **Imitation of the distribution.** LMs reproduce text patterns; if
   plausible-sounding falsehoods are frequent in training data, they are
   *likely* outputs. TruthfulQA (arXiv:2109.07958) showed models repeat
   common misconceptions, and that falsehood often wins the likelihood
   race — the paper's core finding, still the canonical citation.
2. **No grounded truth signal.** Pretraining optimizes prediction, not
   accuracy; nothing in the loss rewards calibrated true belief (Gekhman
   et al., arXiv:2402.10178? — "Does Fine-Tuning LLMs on New Knowledge
   Encourage Hallucinations?" shows fine-tuning on unknown facts increases
   hallucination).
3. **RLHF amplifies confidence.** Kalai & Vempala (arXiv:2402.10862) show
   RLHF-style training systematically distorts probabilities toward
   over-confident extremes — hallucination becomes *asserted*, not
   hedged. Related: "verbalized confidence" miscalibration (Xiong et al.,
   arXiv:2306.13063, "Can LLMs Express Their Uncertainty?").
4. **Retrieval failure modes in RAG**: retrieved-but-irrelevant passages
   "license" fabrication (CUAD-style contract benchmarks show models
   inventing terms when evidence is absent); the fix is evidence-grounding
   *enforcement*, not just retrieval.

## Measuring it (real benchmarks only)

| Benchmark | What it measures | Source |
|-----------|-----------------|--------|
| TruthfulQA | 817 questions targeting common misconceptions; MC + generation modes | arXiv:2109.07958; HF `truthful_qa` |
| HaluEval | Hallucinated vs. right answers on QA, dialogue, summarization | arXiv:2305.11747 |
| FELM | Factuality evaluation of LLMs, knowledge-domain sliced | arXiv:2305.12073? — Chen et al. (Tencent) |
| FaithDial / SummHalluc... | Faithfulness in dialog & summarization | see SacreBLEU-era survey below |
| SimpleQA | Short factual QA with graded correctness (OpenAI, Dec 2024) | arXiv:2411.04368 |
| Vectara hallucination leaderboard | Summarization faithfulness rate (industry, ongoing) | hallucinationsindex.com |

Survey of the field: Ji et al., "Survey of Hallucination in Natural
Language Generation," ACM Computing Surveys 2023 (arXiv:2202.03629).

## Mitigations that actually work (with evidence)

1. **Grounding & attribution**: require answers to cite retrieved
   evidence; reject unsupported claims (reduces but does not eliminate
   fabrication; standard in production search assistants).
2. **Retrieval when unsure**: self-knowledge routing — query an external
   source when internal confidence is low; pairs with calibrated
   confidence elicitation (Lin et al., arXiv:2207.05200 — "Teaching Models
   to Express Their Uncertainty in Words," the Lin et al. semantic
   entropy follow-up: Farquhar et al., Nature 2024, arXiv:2406.15927).
3. **Semantic entropy**: sample multiple answers, cluster by meaning;
   high entropy = likely hallucination. Farquhar et al. (Nature, 2024)
   showed large hallucination-detection AUUC gains across models/tasks.
4. **Verifier ensembling / self-consistency**: majority-vote reasoning
   paths (Wang et al., arXiv:2203.11171) reduce reasoning errors though
   not factual unknowns.
5. **RLHF on honesty**: train raters to penalize confident-wrong answers
   explicitly — InstructGPT-style pipelines adopted this; effect decays
   under distribution shift.
6. **Don't ask for what you can't support**: prompt-side "answer only from
   the provided documents; say 'not found' otherwise" measurably reduces
   unsupported claims — the cheapest mitigation, and the one the repo's
   guardrail pipeline defaults to.

## Operational policy for deployments

- Never let a hallucinating agent *act* (send emails, file documents,
  order goods) without a verification step — see excessive-agency risks
  ([governance/owasp_llm_top10.md](../governance/owasp_llm_top10.md) LLM08).
- Log the model's uncertainty signals (verbalized confidence, entropy)
  with the output; they're cheap and post-hoc-correlatable with errors.
- Human escalation path for "I don't know" — if your UX punishes refusal,
  you have built a hallucination machine (see
  [over_refusal.md](over_refusal.md) for the symmetric failure).
