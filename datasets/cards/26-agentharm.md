# Dataset card: AgentHarm

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification date
2026-10-25 (arXiv abstract verified via API; title/authors/date checked)
· prepared by the course build · status: card at abstract-read level;
license open

## 1. Identity and provenance

- **What it is:** a benchmark for measuring **misuse of LLM agents** —
  models "which use external tools and can execute multi-stage tasks" —
  the abstract's diagnosis being that jailbreak robustness "has been
  studied primarily for LLMs acting as simple chatbots" while agent
  misuse "may pose a greater risk" and "remains underexplored."
- **Canonical home:** "AgentHarm: A Benchmark for Measuring Harmfulness
  of LLM Agents" (Andriushchenko et al., arXiv:2410.09024, 2024-10-11,
  API-verified 2026-10-25); benchmark and code released publicly per
  the paper's release statement.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-stated)

- **110 explicitly malicious agent tasks**, **440 with augmentations**
  — the abstract's own counts. The augmentation structure (variations
  of each task) is the design feature that matters: misuse evaluation
  needs *task families*, not isolated prompts, so defenses cannot
  pass by handling one phrasing.
- Tasks are explicitly multi-stage and tool-using by design — the
  benchmark's whole point is that harm through an agent is a
  *pipeline*, not a single completion.

## 3. Collection and labeling

- Abstract-level: curated explicit-maliciousness (no ambiguity about
  intent — the tasks are "explicitly malicious" by construction, which
  is the right design for *misuse* measurement as distinct from
  borderline-harm measurement).
- The paper's harmfulness-measurement approach for agent outputs is
  announced at abstract level; its scoring detail is body-level and
  unclaimed here.

## 4. Splits and leakage discipline

- Not established at abstract level. Course discipline: 110-task
  structure means results should be reported per task family (the 440
  augmentations are within-family), with any defense development on
  a disjoint subset — the grouped-split rule applied at task
  granularity.

## 5. Where the course uses it

- **Ch. 14** (agent/tool security): the misuse-side benchmark to pair
  with InjecAgent (card 27) — attack-via-content versus
  misuse-by-intent, the two halves of agent risk.
- **Ch. 20** (dangerous capabilities): explicitly-malicious task
  benchmarks as the misuse instrument for release evaluation — the
  "would the agent do it if asked" capability question, cleanly
  separated from disposition.
- **P10** (capstone dossier): the agent-harm evaluation tier's
  real-world candidate, cited with the same task-family reporting
  discipline the dossier's assurance case requires.

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; the task taxonomy's
  category list, the scoring rubric, and model results are body-level
  and unclaimed. The abstract truncates after the augmentation count —
  recorded as the API record's limit.
- Design caveat the course records: explicit malice by construction
  answers the *capability* question cleanly but not the *gray-zone*
  question (dual-use tasks where intent is ambiguous) — a different
  instrument, honestly noted so the benchmark is not asked to carry
  a claim it was not designed to support.
