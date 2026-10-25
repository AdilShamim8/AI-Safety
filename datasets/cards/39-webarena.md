# Dataset card: WebArena

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification
date 2026-10-25 (arXiv abstract verified via API; title/authors/date
checked) · prepared by the course build · status: card at
abstract-read level; license open

## 1. Identity and provenance

- **What it is:** a **highly realistic and reproducible environment
  for language-guided agents that perform tasks on the web** — the
  abstract's own scope. The diagnosis it answers: agents "are
  primarily created and tested in simplified synthetic environments,
  leading to a disconnect with real-world scenarios."
- **Canonical home:** "WebArena: A Realistic Web Environment for
  Building Autonomous Agents" (Zhou et al., arXiv:2307.13854,
  2023-07-25, API-verified 2026-10-25).

## 2. Composition (abstract-level)

- The environment-first design (reproducible web world, not a
  static task list) with self-hostable sites; task counts and site
  inventory are body-level, **unclaimed** here (the API abstract
  truncates into the construction detail).

## 3. Collection and labeling

- Environment construction with tasks defined over real-site
  replicas — the "dynamic environment" tier of
  [comparison 12](../../research/notes/comparison-12-evaluation-supply-strategies.md)'s
  supply spectrum: evaluation exists as a *world* the agent acts
  in, with success predicates executable in that world.

## 4. Splits and leakage discipline

- Environment-based evaluation resists memorization (tasks are
  interactions, not strings); the course still applies its
  contamination discipline to any model trained on task corpora.

## 5. Where the course uses it

- **Ch. 14:** the realistic-agent-environment citation — pairing
  with AgentDojo (card 30) (injection-focused,
  dynamic) and AgentHarm (card 26) (misuse
  tasks) as the three-legged agent evaluation cabinet:
  realism, adversarial dynamics, and misuse.
- **P10:** the dossier's agent-evaluation tier names it as the
  realism reference — success predicates executable, not
  judge-scored.

## 6. Honest limitations (this card)

- Abstract-read: license uninspected; task counts, site inventory,
  and the benchmark's headline agent-failure findings are
  body-level, unclaimed.
