# Lecture 3 — Adversarial robustness, jailbreaks, prompt injection, and weight security

*Course companion note · [Harvard CS 2881](README.md) · video:
[AI Safety (CS 2881) Lecture 3: Robustness](https://www.youtube.com/watch?v=pfKO4MlvM-Y) (1:36:26) · Fall 2025 iteration ·
[course page](https://boazbk.github.io/mltheoryseminar)*

## Where this lecture sits

The security lecture, co-taught with guest lecturers Nicholas
Carlini and Keri Warr (both then at Anthropic). Announced topics:
adversarial robustness; jailbreaks; prompt injection; lessons from
vision and software security (buffer overflows, SQL injection);
defense in depth; securing weights.

## The announced scope

The full security surface of deployed LLMs: from the 2014
adversarial-example literature through production data extraction to
agent-framework injection and the physical security of model weights.
Experiment: a red-team/blue-team many-shot jailbreak and
reasoning-effort study.

## The published reading list (Fall 2025, as listed on the course page)

Pre-reading: Carlini et al., "Are Aligned Neural Networks Adversarially
Aligned?" (2023); Nasr et al., "Scalable Extraction of Training Data from
(Production) Language Models" (2023); chapters 1–2 of Ross Anderson's
*Security Engineering*; the RAND report on securing AI model weights.
Optional list includes the GCG universal-suffix paper (Zou et al. 2023 —
the repo carries [research/notes/31-gcg-universal-suffixes.md](../../research/notes/31-gcg-universal-suffixes.md)),
the instruction hierarchy, Anthropic's Constitutional Classifiers,
inference-time-compute-for-robustness, AgentDojo, the CaMeL design paper,
the prompt-injection wiki, Szegedy et al. 2014, and the SQL-injection
literature. The full list with links lives on the
[course page](https://boazbk.github.io/mltheoryseminar).

## Core ideas, explained

### 1. Adversarial examples as the oldest continuous result in the field

Szegedy et al. (2014) showed that classifier confidence breaks under
imperceptible perturbation; a decade later the phenomenon has merely
changed substrate — from pixel noise to token-space suffixes. The
lecture's through-line is that jailbreaks are not a novel LLM failure
but the same underlying geometry (high-dimensional functions with
adversarially reachable low-probability regions), which is why the guest
lecturers are Carlini and Warr — the security community's tradition of
*adversary-first thinking* applied to models.

### 2. The extraction result: alignment does not imply privacy

Nasr et al.'s divergence attack pulled training data (PII included) out
of a production chatbot. The result matters to the lecture's argument
because it severs a comforting inference: a model that refuses harmful
requests is not thereby a model that keeps secrets. Refusal is a
behavioral overlay on a representation that still encodes its training
distribution; with the right optimization pressure, the encoding
speaks. The repo treats this as
[Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md)'s
foundational result.

### 3. Prompt injection: the unsolved interface bug

The lecture teaches prompt injection as the LLM era's SQL injection —
an untrusted-data-as-instruction confusion — with the crucial
difference that the "parser" is now a learned system whose instruction
channel cannot be cleanly separated from its data channel. Every agent
framework inherits this: any web page or tool output an agent reads is
potential instruction. The defense landscape (spotlighting, instruction
hierarchy, dual-LLM quarantines, capability-level designs like CaMeL)
is the repo's [Ch. 13](../../chapters/13-llm-application-security/README.md)
and [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md).

### 4. Weight security: the physical layer

The RAND model-weights report reframes "who has the weights" as a
physical-security and insider-threat problem — a frontier model's
weights are a stealable strategic asset, and the securing-weights
discussion belongs beside nuclear-materials accounting, not beside
software licensing. It is the lecture's reminder that the threat model
must include the facility, not just the model.

### 5. The experiment: red team vs blue team

The Fall 2025 experiment runs a many-shot jailbreak red team against a
blue team varying reasoning effort — test-time scaling as a defensive
resource. That structure (attack budget vs defense budget, both priced)
is exactly how [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md)
frames adversarial evaluation.

## Through-line to this repository's chapters

- [Ch. 12](../../chapters/12-adversarial-ml-and-robustness/README.md) —
  the adversarial-ML tradition this lecture inherits.
- [Ch. 13](../../chapters/13-llm-application-security/README.md) and
  [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) —
  prompt injection and agent security as the applied layer.
- [Ch. 16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) —
  extraction and the privacy substrate.
- [Ch. 15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md) —
  the red/blue experiment discipline.

## Honesty note

This is an original study companion written to the lecture's **announced**
scope — the topics, readings, and experiment published on the course page
[SRC-CURR-012], verified 2026-10-27. The lecture video itself was not watched;
no spoken content is transcribed or quoted. Where an idea below is also
carried by a source this repository registers, the register ID appears and
the source is linked — that is the evidence trail, and it is the reader's
choice whether to follow the lecture or the paper first.
