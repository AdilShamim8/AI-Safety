# Note: Adversarial Examples in the Physical World — attacks that survive deployment (2016)

Source: SRC-PAPER-139 · Access: **abstract-read** (arXiv API record,
title/authors/date verified 2026-10-25) · Note level: **abstract-level**.

## The actual problem

Adversarial examples were a digital phenomenon: perturbations
applied to pixels fed directly to a classifier. The deployment
question this paper answered: **do adversarial examples survive the
physical world** — printing, lighting, camera noise, distance,
angle? The method: generate perturbations, print them, photograph
them through a camera, classify. The finding: adversarial examples
**remain effective even under these conditions** — the attack
transfers from digital precision to physical imprecision, with the
paper demonstrating classification changes across varied
conditions (the abstract's own scope; quantitative robustness
rates are body-level, unclaimed).

The safety reading is the whole of Ch. 12's deployment section:
adversarial vulnerability is not a lab artifact that deployment
noise will wash out. The perturbation's signal survives the
channel — meaning every camera-fed deployment (vehicles, scanners,
robotics — and now [multimodal](../../chapters/19-multimodal-and-embodied-safety/README.md)
model front-ends) inherits the attack surface, physically.

## What the abstract establishes

1. The physical-transfer method (print → photograph → classify).
2. The persistence finding: adversarial examples remain effective
   under physical-world conditions and varied capture settings.

## Why this note exists in the course

1. **Ch. 12's deployment-relevance citation.** The chapter's
   threat-model grid asks whether an attack family survives the
   deployment channel; this note is the founding evidence that the
   answer was yes, early and physically.
2. **Ch. 19's embodied bridge.** Physical persistence is why
   embodied/multimodal systems inherit Ch. 12's entire discipline —
   the cross-Chapter wiring the course builds.
3. **The robustness lineage's first station.** [Carlini & Wagner
   (note 05)](05-carlini-wagner-robustness.md) → this note →
   [obfuscated gradients](35-obfuscated-gradients.md) → [RobustBench
   (card 32)](../../datasets/cards/32-robustbench.md): attacks
   strengthened, defenses checked, evaluation standardized — the
   physical-world note is the one that made it a *deployment*
   literature instead of a benchmark curiosity.

## What this note does NOT claim

No per-condition attack-success rates (body-level); no claim about
modern camera pipelines' defenses; no transfer claim to
LLM-vision front-ends beyond the structural point (channel
survivability) that the course labels as its own extension of the
finding.

## The falsifiable extension (deterministic tier)

The channel-survivability question is simulable on P02:

- Generate adversarial perturbations at digital precision; pass
  them through a *degradation channel* (quantization, blur, noise —
  the synthetic camera); measure attack survival at degradation
  levels.
- Prediction worth testing: survival decays but remains above
  chance far into the degradation range — the physical-persistence
  shape, as a curve.
- Falsifier: sharp collapse (survival → chance at mild degradation)
  would show this synthetic attack is channel-fragile — bounding
  the note's transfer and marking where channel-hardening is cheap.
