# Dataset card: HarmBench

license: **check pending** (not verified this round) · verification date
2026-10-21 · prepared by the course build · status: paper verified at
`abstract-read` level; behavior-set composition pending

## 1. Identity and provenance

- **What it is:** a **standardized evaluation framework for automated red
  teaming and robust refusal** — not just a behavior list but an attack
  method registry, behavior sets, a classifier-based judge, and a
  comparison protocol, so that attack/defense papers can be compared on
  equal terms.
- **Canonical home:** GitHub `centerforaisafety/HarmBench` [R2] (page-level
  confirmation of repo existence and description). Paper: arXiv:2402.04249
  [R1]. An official HF dataset exists under the HarmBench organization, but
  the exact HF dataset ID was **not confirmed in this round's fetches** (one
  attempted path 404'd; a mirror `walledai/HarmBench` was observed [R3]) —
  recorded honestly rather than guessed.
- **Authors (page-verified [R1]):** Mantas Mazeika, Long Phan, Xuwang Yin,
  Andy Zou, Zifan Wang, Norman Mu, Elham Sakhaee, Nathaniel Li, Steven
  Basart, Bo Li, David Forsyth, Dan Hendrycks.
- **How WE obtained it:** abstract + page inspection only, 2026-10-21; no
  content downloaded or redistributed.

## 2. Composition (abstract-verified [R1])

- The abstract's scale claims, verified verbatim: a **large-scale comparison
  of 18 red teaming methods and 33 target LLMs and defenses** [R1], plus a
  new **adversarial training method** that improves robustness across
  attacks [R1].
- Behavior-set sizes (the commonly quoted "200 behaviors", contextual vs
  standard behavior splits): **NOT verified this round** — the abstract
  does not state counts, and the dataset pages were not successfully
  inspected. This card deliberately leaves the composition section thin
  until the repository README is read; the pending-verification queue in
  [the catalog](../README.md) carries this item.

## 3. Collection and labeling

- Framework design goals (adaptive evaluation, unified judging, open
  submission): abstract-level [R1]. The judge's construction and validation
  is the load-bearing component for all HarmBench numbers and is pending
  full-text reading — the course treats judge validation as a first-class
  evaluation-science topic (Ch.02) precisely because frameworks like this
  make judge quality the hidden global constant.

## 4. Splits and leakage discipline

- Not determinable at achieved access level. Noted for the next round:
  behavior sets with contextual variants need session-isolation when
  attacks run multi-turn.

## 5. Uses and known misuse

- **Measures well (by design intent):** cross-method, cross-target
  comparability of automated red teaming, with refusal robustness on the
  same axis.
- **Known misuse patterns:** (a) citing "HarmBench attack success" without
  naming the behavior set variant and judge version — the framework's
  value collapses without its provenance; (b) treating the framework's
  classifier judge as ground truth without its measured error rates.

## 6. What this dataset CANNOT support

- Any composition-level claim beyond [R1]'s abstract facts until further
  verification (this is the card's honesty boundary).
- Manual red teaming coverage claims (its construct is *automated* red
  teaming).
- Over-refusal measurement — the robust-refusal construct here is attack
  resistance, not benign-prompt calibration (JBB-Behaviors' benign split or
  XSTest cover that).

## 7. Maintenance

- Repository observed live [R2]; framework release cadence pending. Ch.15
  and P10 reference it as the standardization exemplar; no course project
  depends on unverified composition facts.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2402.04249 | title; 12-author list; v1 2024-02-06 / v2 2024-02-27; abstract (standardized framework; 18 red teaming methods; 33 target LLMs and defenses; adversarial training contribution) | abstract-read | 2026-10-21 |
| [R2] | https://github.com/centerforaisafety/HarmBench | repository existence; description consistent with paper | page-inspected | 2026-10-21 |
| [R3] | https://huggingface.co/datasets/walledai/HarmBench | mirror existence (not used as a source of composition facts) | page-inspected | 2026-10-21 |
