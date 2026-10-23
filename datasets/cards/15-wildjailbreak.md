# Dataset card: WildJailbreak

ODC-BY (Hugging Face license tag, `allenai/wildjailbreak`) · verification
date 2026-10-23 · prepared by the course build · status: paper verified at
`abstract-read` level; hosting page inspected via the HF API

## 1. Identity and provenance

- **What it is:** a large-scale **open-source synthetic safety training
  dataset** — vanilla (direct request) and adversarial (complex jailbreak)
  prompt-response pairs with a contrastive benign arm — built by mining
  *in-the-wild* user-chatbot interactions for real jailbreak tactics
  rather than recruiting workers or running gradient-based search.
- **Canonical home:** `allenai/wildjailbreak` on Hugging Face [R2] (164
  likes, 6,196 downloads, last modified 2024-08-08 at inspection). Paper:
  *WildTeaming at Scale: From In-the-Wild Jailbreaks to (Adversarially)
  Safer Language Models*, arXiv:2406.18510, submitted 2024-06-26 [R1].
- **Authors (abstract-verified [R1]):** Liwei Jiang, Kavel Rao, Seungju
  Han, Allyson Ettinger, Faeze Brahman, and 6 further authors (11 total).
- **How WE obtained it:** abstract read + HF API page inspection on
  2026-10-23; no content downloaded or redistributed.

## 2. Composition (abstract-verified)

- **262K vanilla (direct request) and adversarial (complex jailbreak)
  prompt-response pairs** [R1].
- **Two contrastive query types** [R1]: (1) harmful queries (vanilla and
  adversarial) and (2) benign queries that *resemble* harmful queries in
  form but contain no harm — the exaggerated-safety control that makes
  the dataset usable for studying over-refusal during safety training.
- The mining framework (WildTeaming) discovered **5.7K unique clusters of
  novel jailbreak tactics** from in-the-wild user-chatbot interactions
  [R1].

## 3. Collection and labeling

- Tactics are mined from real user-chatbot interactions — users who were
  *not* instructed to break the system [R1] — then composed for systematic
  exploration of novel jailbreaks; the dataset itself is synthetic
  (responses generated), with the contrastive labels design-determined.
  The labeling/verification pipeline details live in the unread body.

## 4. Splits and leakage discipline

- The abstract positions the dataset for **safety training** (an open
  training resource in a field where safety training data is usually
  closed even when weights are open) [R1] — so train/eval reuse
  separation is the load-bearing discipline: a model trained on
  WildJailbreak must never be *evaluated* on jailbreak benchmarks whose
  items overlap its training distribution. Downstream evaluators should
  state the separation explicitly (Ch.02 contamination rule).

## 5. Uses and known misuse

- **Measures well / trains well:** the interplay of data properties and
  model capabilities during safety training; scaling effects of safety
  data; the balance of appropriate safeguarding without over-refusal
  (the paper's stated target) [R1].
- **Does not measure:** jailbreak *evaluation* hygiene when reused as an
  eval set post-training (leakage above); harm-category coverage
  (distribution follows in-the-wild tactics, not a designed risk
  taxonomy).
- Known misuse: citing the 4.6x attack-diversity/success comparison
  (WildTeaming vs state-of-the-art jailbreak methods [R1]) as a safety
  *guarantee* rather than an adversarial-strength statement about the
  evaluated methods.

## 6. What this dataset cannot support

- Claims that training on it produces provably safe models (the paper
  claims balanced behaviors, not guarantees).
- Real-user harm rates: the interactions are mined corpora, not
  representative samples of user intent.
- Per-category performance claims — category structure lives in the
  unread body.

## 7. Maintenance

- License: ODC-BY (Open Data Commons Attribution) per the HF tag [R2] —
  attribution obligation on redistribution; the paper's use restrictions
  (if any) live in the unread body.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2406.18510 (via arXiv API) | title (WildTeaming at Scale); 11 authors (Jiang, Rao, Han, Ettinger, Brahman, ...); submitted 2024-06-26; abstract (5.7K tactic clusters; 262K vanilla+adversarial pairs; contrastive harmful/benign design; 4.6x diversity/success vs SOTA; training-set motivation) | abstract-read | 2026-10-23 |
| [R2] | https://huggingface.co/api/datasets/allenai/wildjailbreak | id; license tag odc-by; arXiv tag 2406.18510; 164 likes; 6,196 downloads; last modified 2024-08-08 | page-inspected (API) | 2026-10-23 |

Explicitly **not** claimed: the tactic-clustering pipeline, response
generation details, train/eval splits, category distribution, and the
paper's experiment tables — all pending the full-text read.
