# Dataset card: JailbreakBench (JBB-Behaviors)

MIT (dataset page license section, verbatim [R1]; repository LICENSE read
directly 2026-10-23 — MIT, copyright (c) 2023 JailbreakBench Team [R4]) ·
verification date 2026-10-21 (license confirmed 2026-10-23) · prepared by
the course build · status: fully verified at `page-inspected` level,
including field-level schema

## 1. Identity and provenance

- **What it is:** an **open, standardized jailbreak benchmark** built to fix
  the field's reproducibility problem: attack papers used different targets,
  judges, and refusal criteria, making numbers incomparable. JBB fixes the
  target set (behaviors), the comparison protocol, and public leaderboards.
- **Canonical hosting inspected:** Hugging Face `JailbreakBench/JBB-Behaviors`
  [R1] (DOI 10.57967/hf/2540 [R1]). Paper: arXiv:2404.01318 [R1]. The
  project spans code + dataset + leaderboard; this card covers the behaviors
  artifact.
- **How WE obtained it:** page inspection only, 2026-10-21, including the
  dataset viewer's field schema; no content downloaded or redistributed.

## 2. Composition (page-verified [R1])

- **behaviors subset: 200 rows**, split into **100 harmful + 100 benign**
  behaviors [R1] — the benign half is a design commitment to measuring
  over-refusal *alongside* attack success, the same paired-ledger discipline
  the course teaches (XSTest card is the instrument analogue).
- **judge_comparison subset: 300 rows** [R1] (materials for studying judge
  reliability; exact composition pending deeper inspection).
- **Field schema (from the dataset viewer [R1]):** `Index`, `Goal`,
  `Target`, `Behavior`, `Category` (10 values), `Source` (3 values).
- **10 behavior categories**, aligned with OpenAI's usage policies [R1]:
  harassment/discrimination, malware/hacking, physical harm, economic harm,
  fraud/deception, disinformation, sexual/adult content, privacy, expert
  advice, government decision-making.
- **Source provenance field** [R1]: behaviors are traceably sourced from
  `TDC/HarmBench`, `AdvBench`, and `Original` — i.e., the benchmark is
  partially *derived*, with lineage in-file. This is the best
  provenance-in-design example in the catalog.

## 3. Collection and labeling

- Curation process (how behaviors were selected/merged across sources, and
  how the benign set was authored): paper-level, pending full-text read.
- No crowd annotation layer at page level; the `judge_comparison` subset
  [R1] is the artifact that makes judge disagreement *measurable* — the
  card records its existence without yet claiming its contents.

## 4. Splits and leakage discipline

- Fixed published behavior set; the leakage question for JBB is *attack
  publicness*: submissions and artifacts circulate, so defense results must
  state model versions and dates. The 100-benign control set must be
  reported together with the 100-attack set, always (P07's report template
  enforces this).

## 5. Uses and known misuse

- **Measures well:** attack success and over-refusal on a common, sourced
  behavior set — designed for comparability across methods and over time.
- **Known misuse patterns:** (a) quoting JBB ASR without the benign-side
  refusal rate; (b) comparing attacks that used different judges or
  substring criteria (the standardization only works if you use the
  standard); (c) treating the 10 categories as a severity taxonomy — they
  are usage-policy categories, not a severity ranking.

## 6. What this dataset CANNOT support

- Open-ended harm discovery: the behavior list is fixed; finding *new*
  attack behaviors is out of scope by design.
- Claims about multimodal or agentic attack surface (text-only behaviors as
  inspected).
- Legal conclusions about policy violations (categories are aligned with
  usage policies, not statutes).
- Multilingual robustness claims.

## 7. Maintenance

- Active project (DOI assigned, leaderboard live at page level [R1]); the
  course's P07/P10 record artifact revision + date with every result.

## References (where each fact was collected)

| Marker | Source | What was collected | Access level | Date |
|--------|--------|--------------------|--------------|------|
| [R1] | https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors | license text verbatim ("This dataset, like the code, is released under MIT License."); behaviors 200 rows (100 harmful + 100 benign); judge_comparison 300 rows; 10 category names; Source field values (TDC/HarmBench, AdvBench, Original); field schema (Index, Goal, Target, Behavior, Category, Source); DOI 10.57967/hf/2540; arXiv 2404.01318 | page-inspected | 2026-10-21 |
| [R4] | https://github.com/JailbreakBench/jailbreakbench (LICENSE via GitHub license API) | MIT License, copyright (c) 2023 JailbreakBench Team (1,076 bytes); SPDX MIT — independently confirms the HF-page statement [R1] from the canonical repository | page-inspected | 2026-10-23 |

Explicitly **not** claimed: leaderboard methodology, judge protocol
details, paper authorship, artifact-version history — pending the
full-text read of arXiv:2404.01318.
