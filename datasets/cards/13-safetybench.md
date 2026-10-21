# Dataset card: SafetyBench

license: **check pending** (not verified this round) · verification date
2026-10-21 · prepared by the course build · status: composition verified at
`page-inspected` level across repository and anthology pages

## 1. Identity and provenance

- **What it is:** a **multiple-choice safety evaluation benchmark** covering
  multiple safety concern categories in **both Chinese and English** — the
  bilingual coverage is its distinguishing property, and the reason Ch.23
  (governance) uses it: safety-category taxonomies are governance artifacts,
  and SafetyBench demonstrates what a taxonomy-turned-benchmark looks like
  in two languages.
- **Canonical home:** GitHub `thu-coai/safetybench` [R1]; Hugging Face
  `thu-coai/SafetyBench` (referenced from the repository). Paper: "Evaluating
  the Safety of Large Language Models", Zhang et al., **ACL 2024** long
  paper [R2]; arXiv:2309.07045 (referenced from search-level observation of
  the paper's HTML version — recorded at metadata-only strength, pending
  direct abstract read).
- **How WE obtained it:** page inspection only, 2026-10-21; no content
  downloaded or redistributed.

## 2. Composition (page-verified)

- **11,435 multiple-choice questions** [R1].
- **7 distinct categories of safety concerns** [R1]; the exact category
  names were not enumerated in this round's fetches — pending (recorded
  honestly; the arXiv HTML version's phrasing "11,435 Chinese and English"
  questions [R3-observation] confirms bilingual composition at page level).
- **Chinese and English data both included** [R1] — a two-language
  evaluation, not a translation of the same items (which it is vs. is not
  is a pending full-text question that matters for cross-language score
  comparability).
- Venue: ACL 2024, anthology 2024.acl-long.830 [R2].

## 3. Collection and labeling

- Construction method (who wrote items, how the 7 categories were defined,
  whether items were collected from existing sources or authored): not
  visible at page level; pending the full-text read.
- Correctness labels in an MCQ design are design-determined; the
  validity-critique exercise the course assigns (Ch.02) is: what does a
  "safety knowledge" MCQ actually measure — knowledge *about* safety norms
  vs safe *behavior*? These are different constructs, and MCQ benchmarks
  measure the former.

## 4. Splits and leakage discipline

- Split structure not inspected this round. Standard contamination
  discipline applies (items circulate publicly post-ACL-2024); results must
  state model cutoffs.

## 5. Uses and known misuse

- **Measures well:** safety-domain knowledge coverage in a fixed-option
  format, in two languages, with governance-mapped categories.
- **Known misuse patterns:** (a) equating high MCQ accuracy with safe
  behavior (knowledge ≠ conduct — the single most common inference error
  with MCQ safety benchmarks); (b) cross-language score comparison without
  knowing whether items are parallel translations or independent
  compositions; (c) quoting the category taxonomy as *the* taxonomy of
  safety — it is one project's mapping of it.

## 6. What this dataset CANNOT support

- Behavioral safety claims (refusal, compliance, harmful generation rates)
  — fixed-option items do not exercise generation behavior at all.
- Multilingual claims beyond the two included languages.
- Severity or risk-ranking claims across its categories.

## 7. Maintenance

- The same organization ships a newer **Agent-SafetyBench** (agent-safety
  environments, observed Dec 2024 [R4-observation]) — evidence of an active
  benchmark family; SafetyBench itself is treated as a stable ACL-2024
  artifact until version information is verified.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://github.com/thu-coai/safetybench | "11,435 diverse multiple choice questions spanning across 7 distinct categories of safety concerns"; bilingual Chinese+English statement | page-inspected | 2026-10-21 |
| [R2] | https://aclanthology.org/2024.acl-long.830 | ACL 2024 long-paper listing; authorship (Zhang et al.); abstract-level composition statement consistent with [R1] | page-inspected | 2026-10-21 |
| [R4-observation] | https://huggingface.co/datasets/thu-coai/Agent-SafetyBench | existence and date of the related Agent-SafetyBench release (recorded as adjacent observation, not a SafetyBench fact) | page-inspected | 2026-10-21 |

Explicitly **not** claimed: the 7 category names, arXiv identifier (pending
direct read), split structure, license, item-authorship method — all in the
catalog's pending-verification queue.
