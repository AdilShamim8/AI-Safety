# Dataset card: WMDP (Weapons of Mass Destruction Proxy)

MIT (Hugging Face license tag, `cais/wmdp`) · verification date
2026-10-23 · prepared by the course build · status: paper verified at
`abstract-read` level; hosting page inspected via the HF API

## 1. Identity and provenance

- **What it is:** a public **proxy benchmark for hazardous knowledge** —
  multiple-choice questions measuring knowledge relevant to
  biosecurity, cybersecurity, and chemical security, built to be an
  *unlearning* target: models are evaluated on how much hazardous
  proxy knowledge they retain after unlearning interventions.
- **Canonical home:** `cais/wmdp` on Hugging Face [R2] (26,806 downloads,
  32 likes at inspection; last modified 2024-04-27). Project site:
  `wmdp.ai` [R1]. Paper: *The WMDP Benchmark: Measuring and Reducing
  Malicious Use With Unlearning*, arXiv:2403.03218, v1 2024-03-05,
  v7 2024-05-15 [R1].
- **Authors (abstract-verified [R1]):** Nathaniel Li, Alexander Pan,
  Anjali Gopal, Summer Yue, Daniel Berrios, and 52 further authors
  (57 total — a consortium of academics and technical consultants).
- **How WE obtained it:** abstract read + HF API page inspection on
  2026-10-23; no question content downloaded or redistributed.

## 2. Composition (abstract-verified)

- **3,668 multiple-choice questions** serving as a proxy measurement of
  hazardous knowledge in **biosecurity, cybersecurity, and chemical
  security** [R1].
- The questions were **stringently filtered to eliminate sensitive
  information** prior to public release [R1] — the property that makes
  a hazardous-knowledge benchmark publishable at all: it is a proxy,
  not the hazardous material itself.
- Dual role by design: (1) an evaluation for hazardous knowledge in
  LLMs and (2) a benchmark for unlearning methods to remove such
  knowledge [R1].

## 3. Collection and labeling

- Developed by a consortium of academics and technical consultants,
  with the filtering step load-bearing [R1]. The authorship
  consortium's composition, the per-domain question counts, and the
  filtering rubric details live in the unread body.

## 4. Splits and leakage discipline

- A public, fixed evaluation set — the contamination consideration is
  unusual and worth teaching: this is one of the few benchmarks where
  *training on the test set* is the intervention being studied
  (unlearning), so evaluation hygiene (separate retained-capability
  checks like MMLU biology) is built into the paper's design [R1].
  The paired public counterpart for measuring *retained general
  capability* is the paper's stated evaluation structure [R1].

## 5. Uses and known misuse

- **Measures well:** proxy hazardous-knowledge retention; unlearning
  method comparison (RMU is the paper's state-of-the-art method,
  reducing WMDP performance while maintaining general capabilities in
  areas such as biology and computer science [R1]).
- **Does not measure:** actual capability to execute harmful projects —
  proxy knowledge is not demonstrated capability (the gap the paper is
  explicit about filling with a *proxy*).
- Known misuse: quoting WMDP scores as a safety certification; a low
  WMDP score without the retained-capability ledger is just damage to
  the model.

## 6. What this dataset cannot support

- Claims about real-world uplift (the paper's proxy framing forbids
  this at abstract level).
- Per-domain score decomposition (per-domain counts/results live in
  the unread body).
- Any statement about unlearning robustness against adversarial
  relearning — that literature postdates the abstract's claims.

## 7. Maintenance

- License: MIT per the HF tag [R2]. The benchmark's sensitive-filtering
  maintenance process (how future questions are screened) lives in the
  unread body / project site.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://arxiv.org/abs/2403.03218 (via arXiv API) | title; 57 authors (Li, Pan, Gopal, Yue, Berrios, ...); v1 2024-03-05 / v7 2024-05-15; abstract (3,668 MCQ; bio/cyber/chem domains; stringent filtering; dual eval+unlearning role; RMU method; wmdp.ai; White House EO context) | abstract-read | 2026-10-23 |
| [R2] | https://huggingface.co/api/datasets/cais/wmdp | id; license tag mit; arXiv tag 2403.03218; 32 likes; 26,806 downloads; last modified 2024-04-27 | page-inspected (API) | 2026-10-23 |

Explicitly **not** claimed: per-domain question counts, the filtering
rubric, RMU's technical details and per-model results, and the paired
retained-capability benchmark's composition — all pending the
full-text read.
