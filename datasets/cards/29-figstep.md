# Dataset card: FigStep

LICENSE not observed this session — the canonical repository's license
was not inspected; **unknown (pending page-inspect)** · verification date
2026-10-25 (arXiv abstract verified via API; title/authors/date checked)
· prepared by the course build · status: card at abstract-read level;
license open

## 1. Identity and provenance

- **What it is:** a **black-box jailbreak against Large
  Vision-Language Models** whose move is modality arbitrage: "instead
  of feeding textual harmful instructions directly," FigStep con[veys
  them through the visual channel — the abstract's own design
  statement, truncated in the API record precisely where the
  mechanism is named (typography inside images, per the paper's
  title-adjacent description "via Typographic…"). The attack exploits
  the safety gap between what the LLM spine was trained to refuse and
  what the vision front-end happily renders.
- **Canonical home:** "FigStep: Jailbreaking Large Vision-Language
  Models via Typographic..." (Gong et al., arXiv:2311.05608,
  2023-11-09, API-verified 2026-10-25); data and code released.
- **How WE obtained it:** arXiv API abstract read only, 2026-10-25; no
  content downloaded or redistributed.

## 2. Composition (abstract-level)

- The abstract establishes: the black-box character (no model access
  needed), the modality-transfer design (harmful content enters
  through images, not text), and the target class (LVLMs whose
  "safety… remains adequately underexplored" with "potential
  overreliance on the safety assurances purported by their underlying
  LLMs" — the abstract's diagnosis, and the card's reason for
  existing).
- Benchmark sizes and attack-success magnitudes: body-level, unclaimed
  at this access level.

## 3. Collection and labeling

- Abstract-level: constructed visual payloads for jailbreak
  evaluation. The payload taxonomy is body-level.
- Course-relevant honesty: FigStep's significance is *structural* — it
  demonstrates that alignment coverage does not automatically transfer
  across modality boundaries. The LLM spine's refusal training did
  not cover "harmful content arriving pre-rendered as pixels" — the
  cleanest available instance of note 44's mismatched-generalization
  mode, at the modality boundary rather than the domain boundary.

## 4. Splits and leakage discipline

- Not established at abstract level. Course discipline: visual
  jailbreak payloads are an enumerable attack family — defenses
  evaluated on the shipped set need designed follow-ups (font
  variants, scene embedding, mixed-modality splits) before any
  robustness claim.

## 5. Where the course uses it

- **Ch. 19** (multimodal and embodied safety): the canonical
  modality-boundary jailbreak — the citation for "safety training
  does not ride the modality bus for free," pairing with BIPIA
  (card 28) as the two multimodal-adjacent attack instruments.
- **Ch. 13**: the application-security reading of the same attack —
  input channels as separate trust surfaces (the spotlighting note's
  canonicalization logic, extended to pixels).
- **P10:** the dossier's multimodal-risk section cites it as the
  evidence that multimodal deployments widen the eval surface.

## 6. Honest limitations (this card)

- Abstract-read access: license uninspected; composition counts,
  success rates, and the payload-generation detail unclaimed. The
  abstract truncates mid-mechanism — recorded as the API record's
  limit; the card claims only what the untruncated text states plus
  the title's own "Typographic" descriptor.
