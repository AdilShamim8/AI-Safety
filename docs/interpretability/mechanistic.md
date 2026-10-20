# Mechanistic interpretability

Mechanistic interpretability aims to decompose a trained network into
human-understandable computational parts: features, circuits, and
algorithms. The founding text is the Distill *Circuits* series
(Cammaratano et al., 2020 — "Zoom In: An Introduction to Circuits"); the
modern canon lives at Anthropic's transformer-circuits.pub.

## The vocabulary

- **Feature**: a human-interpretable property of the input/activation
  space the model represents. The superposition hypothesis (Elhage et al.,
  arXiv:2209.10652, "Toy Models of Superposition") explains why features
  are hard to find: models store *more* features than they have neurons,
  in non-orthogonal directions, trading interference for capacity. This
  is why single-neuron analysis fails ("multimodal neurons," OpenAI's
  multimodal-neuron paper, 2021) and why dictionary learning (SAEs) became
  the tool of choice.
- **Circuit**: the sub-graph of attention heads and MLPs implementing a
  behavior. The classic positive result: **induction heads** (Olsson et
  al., 2022, "In-context Learning and Induction Heads") — a two-head
  circuit `[prev-token head] → [induction head]` implementing
  `A B ... A ? → B`, which appears to be the engine of in-context
  learning and explains the sharp "phase change" in-context learning
  curve during training.
- **QK / OV decomposition**: each attention head splits into the
  query-key circuit (where to attend from) and the output-value circuit
  (what is written once attending) — the unit of circuit analysis.

## Landmark results worth knowing

| Result | Finding | Source |
|--------|---------|--------|
| Induction heads | In-context learning ≈ pattern-matching circuit; emergent phase change | Olsson et al., transformer-circuits 2022 |
| ROME | Factual recall is localized in mid-MLPs; facts editable with rank-one updates | Meng et al., arXiv:2202.05262 (NeurIPS 2022) |
| Knowledge neurons | Individual neurons whose ablation deletes specific facts | Dai et al., arXiv:2104.08664 (ACL 2022) |
| Grokking circuits | Networks that "grok" modular arithmetic build clean Fourier circuits | Nanda et al., arXiv:2301.05217 (ICLR 2023 notable) |
| Refusal direction | LLM refusals are (largely) a single linear direction; removing it breaks refusal across phrasings | Arditi et al., arXiv:2406.11717 |
| Trigram → cross-layer reasoning | Analysis of o1-style test-time compute found "multi-step" mechanisms in a single forward pass... in toy models; production-model circuit tracing is just beginning | Anthropic "On the Biology of a Large Language Model" (2025) |

## Method: how a mechanistic investigation actually goes

1. **Find the behavior** you care about, with a minimal reproducible
   dataset (e.g., 100 prompts where the model refuses).
2. **Attribute.** Activation patching — run the clean and corrupted
   (behavior-flipped) inputs, swap activations at one site, and measure
   behavior restoration — localizes components (principled primer: Zhang
   & Nanda, "Towards Best Practices of Activation Patching," arXiv:2309.16042).
3. **Decompose** the critical sites with SAEs to see which features are
   active (see [saes.md](saes.md)).
4. **Validate causally.** Ablate the hypothesized circuit; behavior should
   disappear *and* unrelated behaviors should survive. Correlational
   evidence (attention maps, probe accuracy) is insufficient — the field's
   most-repeated methodological lesson.
5. **Check generality.** Does the circuit transfer across phrasings,
   distributions, model sizes? Many published circuits are
   distribution-specific.

## Safety applications, present tense

- **Backdoor scanning**: SAE features firing on trigger strings (Anthropic
  found a code-vulnerability-backdoor feature in Claude 3 Sonnet; Scaling
  Monosemanticity, 2024) offer a route to detecting sleeper-agent
  behavior (arXiv:2401.05566) that behavioral evals can miss.
- **Refusal mechanics**: understanding *how* refusal works (arXiv:2406.11717)
  cuts both ways — it enables both stronger refusal training and surgical
  jailbreaks; disclosure norms for such results are a live governance
  issue (see [red_teaming/overview.md](../red_teaming/overview.md)).
- **Honesty probes** deployed as runtime monitors (ITI,
  arXiv:2306.03341) — with the caveat that a monitored probe is a
  Goodhart-able signal.

## What "mechanistic" buys over behavioral

Behavioral evals tell you *that* a model fails; mechanistic analysis tells
you *why*, which is what you need to fix it without retraining, to predict
similar failures, and to give auditors something to verify. That gap —
from black-box metrics to inspectable mechanisms — is the entire reason
this subfield is on labs' critical path.
