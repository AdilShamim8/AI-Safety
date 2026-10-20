# Interpretability: overview

Interpretability is the science of answering *what does this model compute,
and where* — with evidence strong enough to intervene on. For safety it
serves three functions: **diagnosis** (find the circuit producing a harmful
behavior), **monitoring** (detect activation signatures of deception or
jailbreaks at inference time), and **intervention** (steer behavior by
editing activations rather than prompts).

Two cultures coexist:

- **Mechanistic interpretability** — reverse-engineer weights into
  algorithms. Lineage: Circuits (Cammaratano et al., 2020, Distill) →
  induction heads (Olsson et al., 2022) → superposition (Elhage et al.,
  arXiv:2209.10652) → sparse-autoencoder feature extraction (Bricken et
  al., "Towards Monosemanticity," 2023; Templeton et al., "Scaling
  Monosemanticity," 2024). Primary venue: transformer-circuits.pub.
- **Behavioral/representation-level interpretability** — probing,
  steering, and representation engineering: linear probes for truthfulness
  (Marks & Tegmark, arXiv:2310.01405; ITI, Li et al., arXiv:2306.03341),
  activation steering (ActAdd, Turner et al., arXiv:2308.10248), RepE (Zou
  et al., arXiv:2310.01407).

## The tool landscape

| Tool | Question it answers | Representative work | Maturity for production |
|------|--------------------|--------------------|------------------------|
| Linear probes | "Is property X linearly represented?" | Alain & Bengio 2016; ITI (arXiv:2306.03341) | Research |
| Activation patching / path patching | "Which components matter for behavior Y?" | Meng et al. ROME (arXiv:2202.05262); Golden 2022 primer | Research |
| Sparse autoencoders (SAEs) | "What features exist, decomposed from superposition?" | Bricken et al. 2023; Gao et al. JumpReLU SAEs (arXiv:2404.01456? — see OpenAI's GPT-4 SAE release, 2024) | Maturing; released SAEs for Gemma/Llama/GPT-4 exist |
| Attribution (gradients, attention) | "Which inputs drove this output?" | Integrated gradients (Sundararajan et al., 2017) | Fragile; useful as hint, not evidence |
| Logit lens / tuned lens | "What does each layer believe?" | nostalgebraist 2021; Belrose et al. (arXiv:2303.08112) | Diagnostic |
| Attribution patches / circuit tracing on transcripts | "What is the model's step-by-step reasoning?" | Anthropic circuit-tracing on Claude (2025) | Frontier research |

## Why safety people should care, concretely

1. **Jailbreak detection without string-matching.** Activation-space
   classifiers detect jailbreaks that share no surface form (illustrated by
   Arditi et al.'s refusal-direction work, arXiv:2406.11717: refusals live
   in a single direction; removing it jailbreaks across phrasings).
2. **Honesty monitoring.** ITI improved TruthfulQA scores by double digits
   by editing along a "truthful" direction — proof that honesty has
   linear structure worth exploiting (and debating: Marks & Tegmark
   distinguished truthful *beliefs* from truthful *statements*,
   arXiv:2310.01405).
3. **Feature-level auditing.** Scaling Monosemanticity found features for
   code backdoors, sycophantic praise, and deception-adjacent behavior in
   Claude 3 Sonnet — the "audit the model, not just the outputs" pipeline
   labs now run internally.
4. **Steering as a safety control.** Anthropic's Golden Gate Claude demo
   (May 2024) made activation steering a user-facing fact; the same
   mechanism can dial refusal strength or calm sycophancy — see
   [steering.md](steering.md).

## Honest caveats

- Superposition means feature-count is not a solved quantity — SAEs give
  *a* decomposition, not *the* decomposition (arXiv:2209.10652).
- Probes measure correlations that can be spurious; "probe finds X" ≠
  "model uses X" — causal tests (patching) are the standard
  (Antverg & Belinkov, arXiv:2203.01245? — "On the pitfalls of analyzing
  individual neurons").
- Circuits found in 2-layer attention-only models often fail to transfer
  to production models; interpretability results need the same
  held-out-evaluation discipline as benchmarks.

Deep dives: [mechanistic.md](mechanistic.md),
[saes.md](saes.md), [steering.md](steering.md).
