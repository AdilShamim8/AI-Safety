# Dataset card: RobustBench

LICENSE not observed this session — the canonical site's licensing
terms were not inspected; **unknown (pending page-inspect)** ·
verification date 2026-10-25 (arXiv abstract verified via API;
title/authors/date checked) · prepared by the course build · status:
card at abstract-read level; license open

## 1. Identity and provenance

- **What it is:** the field's standardized adversarial-robustness
  benchmark, born from the abstract's two diagnoses: the community
  lacks "a systematic understanding of the progress on adversarial
  robustness," and — the load-bearing half — robustness *evaluation*
  is "often error-prone leading to **robustness overestimation**."
  RobustBench's goal, quoted: a benchmark "which as accurately as
  possible reflects the robustness of the considered models within a
  reasonable computational budget."
- **Canonical home:** "RobustBench: a standardized adversarial
  robustness benchmark" (Croce et al., arXiv:2010.09670, 2020-10-19,
  API-verified 2026-10-25); the canonical leaderboard and data live at
  robustbench.github.io.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-level)

- Scope: image classification, with explicit "restrictions (possibly
  loosened in the future) on the allowed models" — the standardization
  move that makes model-to-model comparison meaningful (fixed threat
  model, fixed attack protocol, fixed evaluation budget).
- The abstract announces evaluation "of adversa[arially trained
  models…]" — truncated in the API record; the leaderboard structure
  and per-model entries are body/site-level and unclaimed here.

## 3. Collection and labeling

- Abstract-level: not a collected corpus so much as a *protocol* —
  the benchmark's data is standard test imagery evaluated under a
  pinned adaptive attack (the site's AutoAttack lineage, which the
  course knows through note 07's Croce & Hein reliable-evaluation
  line). The card records the protocol character as the design fact.
- The evaluation-error diagnosis ties directly to note 35
  (obfuscated gradients): RobustBench exists *because* 7-of-9-style
  evaluation failures kept manufacturing false robustness — the
  benchmark is the institutional answer to the paper that diagnosed
  the disease.

## 4. Splits and leakage discipline

- The standardization itself is the leakage answer: pinned threat
  models and protocols mean a leaderboard number is (within its
  stated budget) an attack-aware estimate, not a non-adaptive
  artifact. Course discipline for use: cite the threat model
  alongside any number — a RobustBench figure without its epsilon and
  norm is a quote out of context.

## 5. Where the course uses it

- **Ch. 12:** the vision-side counterpart to the course's
  adaptive-evaluation discipline — paired with notes 05 (Carlini &
  Wagner), 07 (Croce & Hein), and 35 (obfuscated gradients) as the
  four-step story: attacks, reliable evaluation, the diagnosis of
  masked evaluation, and the standardized benchmark that locks the
  lessons in.
- **P09:** the reliability-audit template's reference for
  threat-model-pinned reporting (every number carries its attack
  condition).
- **Ch. 02:** benchmark-design study — what standardization buys and
  what it costs (scope restriction to classification; the "possibly
  loosened" clause is the honest scope boundary).

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; leaderboard entries,
  model restrictions' specifics, and the AutoAttack integration
  detail are site/body-level, unclaimed (truncation recorded).
- Scope: vision classification only — the LLM-side analogue (jailbreak
  evaluation standardization) is a different, younger project;
  StrongREJECT (card 23) is its closest cousin, and the card says so
  rather than stretching the vision benchmark's claims.
