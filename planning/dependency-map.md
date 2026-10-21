# Dependency map

Two dependency structures matter: what learners need before each chapter
(curriculum dependencies), and what software each component needs (tooling
dependencies). Both are kept explicit so neither the roadmap nor the install
instructions can quietly drift.

## Curriculum dependencies (common spine and specializations)

```text
                    ┌──────────────────────────────────────────────┐
                    │ Common methodological spine                   │
                    │ 01 risk models & epistemics → 02 evaluation   │
                    │ science & experimental design                 │
                    └───────────────┬──────────────────────────────┘
                                    │
        ┌───────────────────────────┼─────────────────────────────┐
        │ alignment research        │ AI security engineering     │ evaluations & assurance
        │ 03 specification          │ 12 adversarial ML           │ (shares 01-02 spine;
        │   ↓                       │   ↓                         │  route-specific depth)
        │ 04 preference learning    │ 13 LLM app security         │ 05 scalable oversight
        │ 05 scalable oversight     │ 14 agent/tool/MCP security  │   ↓
        │ 07 deception/scheming     │ 15 red teaming              │ 08 AI control
        │ 09-11 interpretability    │ 16 privacy & supply chains  │ 17 distribution shift
        │ 18 reasoning faithfulness │ 19 multimodal & embodied    │ 22 safety engineering
        │                           │                             │ 23 governance
        └───────────────────────────┴─────────────────────────────┘
                                    │
                    20 misuse & release evaluation
                    21 sociotechnical & systemic risk
                    24 research practice & capstone (P10)
```

Hard prerequisites (enforced by the roadmap, not by wishful reading):

- Chapter 02 requires 01 (threat hypotheses are evaluated in 02).
- Chapter 03 requires 01 (a proxy failure is a risk hypothesis first).
- Chapter 04 requires 03; 07 requires 03; 08 requires 05; 10 and 11 require 09.
- Chapter 13 requires 12 (trust boundaries before LLM-specific attacks);
  14 requires 13; 15 requires 02 and 13.
- Chapter 22 requires 01 and 08; 23 requires 22; 24 requires 02 and 22.
- Projects inherit their chapter prerequisites plus their own: P04 after 04;
  P05 after 05; P06 after 09; P07 after 13-15; P08 after 08; P09 after 17;
  P10 last (integrates P01 with P07/P08 and the assurance material of 22).

## Tooling dependencies

| Layer | Choice | Notes |
|---|---|---|
| Language floor | Python 3.12 (tested: 3.12.15) | modern typing syntax used in course code |
| Environment/lock | uv 0.13.x + `pyproject.toml` + committed `uv.lock` | one dependency workflow, reproducible installs (ADR-0002) |
| Core (always) | pytest, PyYAML, stdlib only otherwise | the core course package stays deliberately small so every project has a CPU smoke mode |
| Harness (P01+) | core + nothing model-dependent | local adapters first; optional Inspect integration documented, never required |
| ML tier (selected projects) | optional extra group: torch, transformers, datasets | installed only for projects that need local models; sizes/versions pinned in `uv.lock`; CPU smoke mode still required |
| Interpretability tier (P06) | optional extra: TransformerLens stack | only if environment supports the download; otherwise protocol-only with honest status |
| CI | GitHub Actions: markdown-link + YAML-schema + import smoke; rate-limited scheduled link check | no model downloads, no GPU in PR CI |

Rules of the road (binding, from the project brief):

1. No project forces every other project to import a large shared stack;
   incompatible research tools live in optional dependency groups.
2. Every project has a CPU smoke mode; model downloads stay out of PR CI.
3. Tool-specific code is written only against APIs imported and exercised
   locally first; versions tested are recorded with the code.
4. Model weights, datasets, and caches are never committed (`.gitignore`
   enforces; CI checks for oversize artifacts).
