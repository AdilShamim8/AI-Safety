# Dataset card: InjecAgent

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification date
2026-10-25 (arXiv abstract verified via API; title/authors/date checked)
· prepared by the course build · status: card at abstract-read level;
license open

## 1. Identity and provenance

- **What it is:** a benchmark for **indirect prompt injection (IPI)** —
  the abstract's threat definition, quoted: attacks "where malicious
  instructions are embedded within the content processed by LLMs" (the
  external content an agent touches — emails, websites, documents),
  "aiming to manipulate these agents into executing detrimental actions
  against users." The benchmark exists because agent deployments make
  this attack class *imperative to assess* — the abstract's own words
  on the stakes.
- **Canonical home:** "InjecAgent: Benchmarking Indirect Prompt
  Injections in Tool-Integrated Large Language Model Agents" (Zhan et
  al., arXiv:2403.02691, 2024-03-05, API-verified 2026-10-25); code
  and data released per the paper.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-level)

- The abstract establishes the attack-class scope (indirect injection
  against tool-integrated agents) and the benchmark's purpose (assess
  and mitigate). Task counts, injection payload taxonomy, and the
  tool-integration surface are body-level and **not established at
  this access level** — recorded as the honest limit.
- The card's structural note: this is the *content-borne* attack
  benchmark — the adversary lives in data the agent processes, not in
  the user's prompt — which is the property that separates it from
  direct jailbreak sets (AdvBench, StrongREJECT) and allies it with
  BIPIA (card 28).

## 3. Collection and labeling

- Abstract-level: constructed injection scenarios against tool-using
  agents. The scenario taxonomy and evaluation criteria are
  body-level, unclaimed.
- Course-relevant design principle (from the threat definition):
  success criteria in IPI benchmarks are *actions taken*, not text
  produced — the agent's tool calls are the attack surface, so the
  benchmark measures manipulation-into-execution. P07's
  halt-on-block semantics and paired attack/benign design mirror
  this at deterministic tier.

## 4. Splits and leakage discipline

- Not established at abstract level. Course discipline: injection
  payloads are an adversarial search space — any defense evaluated
  only against the benchmark's shipped payloads inherits the
  non-adaptive-evaluation trap (note 35's obfuscated-gradients
  lesson, applied to agents), so course use always pairs shipped
  payloads with designed-follow-ups.

## 5. Where the course uses it

- **Ch. 14** (agent/tool/memory/MCP security): the canonical IPI
  benchmark — paired with Greshake (note 06) as the founding
  threat-model source and CaMeL (note 21) as the architectural
  defense line.
- **P07** (injection defense): the real-world evaluation candidate
  for the guard's tier-2 ambitions, with the paired-ledger and
  adaptive-follow-up discipline the project already implements.
- **Ch. 13**: the bridge citation where application security meets
  agent security — injection as the shared mechanism.

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; composition counts,
  payload taxonomy, and scoring rubric unclaimed (the abstract
  truncates mid-purpose-statement — recorded).
- The benchmark measures susceptibility to *shipped* scenarios; the
  course's standing caveat (adaptive attacks) applies to any headline
  number produced with it — the card says so to prevent the benchmark
  from being quoted as a defense certification.
