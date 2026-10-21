# Dataset card: AdvBench

LICENSE file present in the canonical repository (direct read pending); MIT
stated by the inspected mirror [R2] · verification date 2026-10-21 · prepared
by the course build · status: canonical CSV verified line-by-line; paper
verified at `abstract-read` level

## 1. Identity and provenance

- **What it is:** the target set for the GCG (Greedy Coordinate Gradient)
  adversarial-suffix attack: a list of harmful behaviors phrased as
  instructions, paired with affirmative-response prefix strings ("targets")
  that the attack tries to force the model to emit. AdvBench is the harm
  taxonomy that a large fraction of jailbreak research standardized on.
- **Canonical home:** the `llm-attacks` repository [R1b] — official code for
  "Universal and Transferable Adversarial Attacks on Aligned Language
  Models" [R3]. The dataset ships *inside* the repo at
  `data/advbench/` [R1].
- **Authors (paper, page-verified [R3, R4]):** Andy Zou, Zifan Wang,
  Nicholas Carlini, Milad Nasr, J. Zico Kolter, Matt Fredrikson —
  affiliations per the project site [R4]: CMU, Center for AI Safety,
  Google DeepMind, Bosch Center for AI.
- **How WE obtained it:** page/file inspection only, 2026-10-21 (including
  the canonical CSV's file view); no content downloaded or redistributed.

## 2. Composition (page-verified)

- **`harmful_behaviors.csv` has 521 lines — 520 data rows plus a header —
  and is 80.2 KB** [R1]. Two columns: `goal` (the harmful instruction) and
  `target` (the affirmative prefix) [R1].
- The same directory ships **`harmful_strings.csv`** (the string-completion
  setting) and **`transfer_expriment_behaviors.csv`** [R1b].
- **Discrepancy recorded honestly:** the inspected mirror card [R2]
  describes "a set of 500 harmful behaviors" and notes it omits
  `harmful_strings.csv`. The canonical CSV's own line count is 520 rows
  [R1]. Both numbers are recorded with their provenance; the catalog's
  convention is to cite the canonical file (520) and note the mirror's
  framing (500).
- Content is genuinely harmful instructions by design; this card and the
  repository describe **categories only** — no goals are reproduced here.

## 3. Collection and labeling

- Construction (curated from prior red-teaming literature with harmful
  targets phrased as affirmative-response prefixes): paper-level, pending
  full-text read. There is no annotation layer: "harmful" is
  design-determined by the authors.
- The ethics posture is page-verified and unusual: the project site
  documents **pre-publication disclosure to the companies hosting the
  attacked closed-source models**, and an explicit argument for full
  disclosure [R4]. Ch.15 uses this as the disclosure-ethics case study.

## 4. Splits and leakage discipline

- No splits — an attack target list. The course's experimental discipline
  for it (P07): behaviors must be treated as a fixed evaluation set; any
  defense tuned on a subset must report results on the untouched remainder,
  and "tuned on AdvBench" vs "evaluated on AdvBench" must be stated
  explicitly in every result.

## 5. Uses and known misuse

- **Measures well (as material):** attack success against a fixed,
  research-standard harm list — comparable ASR numbers across papers exist
  largely *because* of this standardization.
- **Known misuse patterns:** (a) reporting ASR on a 25-behavior subset
  (the repo's multiple/transfer experiment scale [R1b]) as if it were the
  full set; (b) treating the 520 behaviors as a representative sample of
  real-world harm (it is a curated research list, not a threat census);
  (c) defenses that overfit the list's phrasing style — the adaptive
  attack Ch.15 requires will rephrase and expose this.

## 6. What this dataset CANNOT support

- Refusal quality on benign prompts (no benign controls — XSTest or
  JBB-Behaviors' benign split supply that half of the confusion matrix).
- Harm *severity* ranking: items are an unordered harm list; there is no
  severity field in the canonical CSV [R1].
- Coverage claims about current attack surface (2023-era curation).
- Any claim about non-English harms.

## 7. Maintenance

- The canonical file's last commit was the original release (commit
  a62d130, 2023-07-27 [R1]); the repo itself gained `nanogcg` (a pip-installable
  GCG implementation) in 2024 [R1b]. Treat the dataset as frozen and the
  tooling as maintained.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://github.com/llm-attacks/llm-attacks/blob/main/data/advbench/harmful_behaviors.csv | 521 lines / 520 data rows / 80.2 KB; column names goal, target; commit a62d130 dated Jul 27 2023; sample-free structural view | page-inspected | 2026-10-21 |
| [R1b] | https://github.com/llm-attacks/llm-attacks | repository purpose (official GCG code); data/advbench directory contents (harmful_behaviors.csv, harmful_strings.csv, transfer_expriment_behaviors.csv); experiment scales (25-behavior multiple/transfer runs); nanogcg release note (2024-08-01); LICENSE file present | page-inspected | 2026-10-21 |
| [R2] | https://huggingface.co/datasets/walledai/AdvBench | mirror description ("500 harmful behaviors" framing); MIT license statement for the mirror copy; omission of harmful_strings.csv noted | page-inspected | 2026-10-21 |
| [R3] | https://arxiv.org/abs/2307.15043 | title; author list; v1 2023-07-27 / v2 2023-12-20; abstract (GCG method; transfer to ChatGPT, Bard, Claude, LLaMA-2-Chat, Pythia, Falcon) | abstract-read | 2026-10-21 |
| [R4] | https://llm-attacks.org | author affiliations (CMU, Center for AI Safety, Google DeepMind, Bosch Center for AI); ethics and disclosure page (pre-publication disclosure to affected companies; full-disclosure rationale) | page-inspected | 2026-10-21 |
