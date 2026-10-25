# Dataset card: AgentDojo

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification date
2026-10-25 (arXiv abstract verified via API; title/authors/date checked)
· prepared by the course build · status: card at abstract-read level;
license open. Companion paper note: note 22 (AgentDojo's
explore-establish-exploit framing).

## 1. Identity and provenance

- **What it is:** an **evaluation framework for agents that execute
  tools over untrusted data** — the abstract's own scope — built
  around the prompt-injection threat: "data returned by external
  tools hijacks the agent to execute malicious tasks."
- **The design sentence the course pins:** "AgentDojo is not a static
  test suite, but rather an extensible environment for designing and
  evaluating new agent tasks, defenses, and **adaptive attacks**" —
  the abstract's own words, and the single most important property
  distinguishing it from every shipped-payload benchmark in this
  catalog.
- **Canonical home:** "AgentDojo: A Dynamic Environment to Evaluate
  Prompt Injection Attacks and Defenses" (Debenedetti et al.,
  arXiv:2406.13352, 2024-06-19, API-verified 2026-10-25); the ETH-SRI
  repository is the canonical code home.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-stated)

- **97 realistic tasks** — the abstract's count — of the
  email-client-managing, web-navigating class (the truncation cuts
  the task list; examples quoted only as far as the abstract's own
  text goes).
- Beyond tasks: the environment's structure supports injecting
  injections (the attack side), defending (the defense side), and
  *attacking the defenses* (the adaptive side) — a three-sided
  instrument where most benchmarks are one-sided.

## 3. Collection and labeling

- Abstract-level: tasks are realistic-scenario constructions; the
  payload and defense taxonomies are body-level, unclaimed here.
- The dynamic-design principle is the card's teaching payload:
  because attacks and defenses co-evolve, a *static* suite measures a
  snapshot that ages in months. The course's comparison-05 (static
  benchmarks vs adaptive evaluation) and note 35's obfuscated-
  gradients lesson both cite this design as the field's structural
  response.

## 4. Splits and leakage discipline

- The environment's own answer: no fixed eval set to leak —
  evaluation *generates* from the environment rather than memorizing
  a list. Course discipline for static use of the 97 tasks: standard
  grouped-split rules apply if any defense is tuned on them.

## 5. Where the course uses it

- **Ch. 14:** the dynamic-evaluation citation for agent security —
  paired with InjecAgent (card 27) and BIPIA (card 28) as the
  static-to-dynamic spectrum of injection evaluation.
- **Ch. 15:** the benchmark-design lesson (extensible environments
  over fixed suites) in the red-team methodology section, where note
  22 carries the full paper analysis.
- **P07/P10:** the reference architecture for what the guard's
  evaluation tier aspires to at model scale — the course's
  deterministic harness is deliberately the same shape (scriptable
  attacks, defenses, and adaptive follow-ups in one loop).

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; the 97-task list,
  defense-benchmark results, and the paper's headline findings
  (note 22 carries the competence-floor discussion at its own level)
  are body-level and unclaimed here.
- The framework's dynamism is also an adoption cost: results from
  different AgentDojo instantiations are not directly comparable —
  the course notes this so learners report the configuration they
  actually ran.
