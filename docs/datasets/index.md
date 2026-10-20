# Dataset catalog (real, public, safety-relevant)

Every dataset below is real, publicly distributed, and loadable with a
canonical identifier. Sizes and splits are as published by the authors;
**verify against the dataset card before citing numbers** — the field's
datasets get re-versioned. This repo's loaders (`src/aisafety/data/`)
pin revisions wherever a loader exists.

## Honesty & hallucination

| Dataset | Contents | License (per card) | Canonical access |
|---------|----------|--------------------|------------------|
| **TruthfulQA** (Lin, Hilton, Evans 2021) | 817 questions across 38 categories targeting common misconceptions; generation + multiple-choice modes | Apache-2.0 | HF `truthful_qa`; paper arXiv:2109.07958 |
| **HaluEval** (Li et al. 2023) | Hallucinated vs correct answers over QA/dialogue/summarization (incl. HotpotQA-based) | mixed per-source | HF `pminervini/HaluEval`; arXiv:2305.11747 |
| **SimpleQA** (OpenAI 2024) | Short factual QA with graded correctness for factuality measurement | MIT | HF `openai/simpleqa`; arXiv:2411.04368 |

## Harmfulness & toxicity

| Dataset | Contents | License | Canonical access |
|---------|----------|---------|------------------|
| **Anthropic HH-RLHF** (Bai et al. 2022) | ~170k multi-turn human preference comparisons, helpfulness & harmlessness tracks | MIT | HF `Anthropic/hh-rlhf`; arXiv:2204.05862 |
| **ToxiGen** (Hartvigsen et al. 2022) | 274k machine-generated statements on 13 minority groups; implicit toxicity | MIT (per repo) | HF `toxigen/toxigen`; arXiv:2203.09509 |
| **RealToxicityPrompts** (Gehman et al. 2020) | 100k naturally-occurring prompts (OpenWebText) with Perspective API toxicity scores | OWT-derived; see card | HF `allenai/real_toxicity_prompts`; arXiv:2009.11462 |
| **Jigsaw Toxic Comments** (Kaggle, 2018) | ~1.8M Wikipedia talk-page comments, multi-label toxicity | CC0 (competition data) | Kaggle `jigsaw-toxic-comment-classification-challenge` |
| **Civil Comments** (Borkan et al. 2019) | ~2M news-site comments with toxicity + identity sub-scores | CC0 | Kaggle `jigsaw-unintended-bias-in-toxicity-classification` |
| **BeaverTails** (Ji et al. 2023) | ~330k QA pairs annotated across 14 harm categories (PKU-Alignment) | MIT + CC-BY-NC 4.0 (check track) | HF `PKU-Alignment/BeaverTails`; arXiv:2307.04657 |
| **AdvBench** (Zou et al. 2023) | 520 harmful-behavior strings (attack-success targets) | Apache-2.0 (llm-attacks repo) | GitHub `llm-attacks/llm-attacks` `data/harmful_behaviors.csv`; arXiv:2307.15043 |

## Bias & fairness

| Dataset | Contents | License | Canonical access |
|---------|----------|---------|------------------|
| **BOLD** (Dhamala et al. 2021) | 43,623 prompts across 5 domains (professions, gender, race, religious & political ideologies) for open-ended generation | MIT | GitHub `amazon-science/bold-dataset`; arXiv:2101.11718 |
| **BBQ** (Parrish et al. 2022) | ~58k questions, 9 social-bias categories, ambiguous + disambiguated | CC-BY-4.0 (per repo) | HF `lighteval/bbq` (community mirror); NYU GitHub `alexdesasse/...` — official: `nyu-mll/BBQ`; arXiv:2110.05828 |
| **Winogender** (Rudinger et al. 2018) | 720 sentence pairs: pronoun-coreference by occupation & gender | CC-BY-4.0 | GitHub `corefresolve/...`; HF `winogender`; arXiv:1804.09301 |
| **CrowS-Pairs** (Nangia et al. 2020) | 1,508 stereotype vs anti-stereotype minimal pairs | CC-BY-SA 4.0 | GitHub `nyu-mll/crows-pairs`; arXiv:2010.14033 |
| **StereoSet** (Sakaguchi et al. 2021) | Intra-sentence & inter-sentence stereotype benchmarks across 4 domains | CC-BY-SA 4.0 | HF `stereoset`; arXiv:2104.07612? ("WinoGrande"-era NAACL paper) |

## Capability & reasoning (safety-relevant baselines)

| Dataset | Contents | License | Canonical access |
|---------|----------|---------|------------------|
| **MMLU** (Hendrycks et al. 2021) | 15,908 test questions, 57 subjects (STEM, humanities, law...) | MIT | HF `cais/mmlu`; arXiv:2009.03300 |
| **GSM8K** (Cobbe et al. 2021) | 8.5k grade-school math problems, 7.5k train / 1k test, with solutions | MIT (with canary string!) | HF `openai/gsm8k`; arXiv:2110.14168 |
| **HELM scenarios** (Stanford CRFM) | Living benchmark harness across dozens of scenarios | Apache-2.0 | GitHub `stanford-crfm/helm` |
| **BIG-bench** (Srivastava et al. 2022) | 200+ diverse tasks incl. deception & self-awareness probes | Apache-2.0 | GitHub `google/BIG-bench`; arXiv:2206.04615 |

## Refusal & over-refusal

| Dataset | Contents | License | Canonical access |
|---------|----------|---------|------------------|
| **XSTest** (Röttger et al. 2023) | 250 safe prompts prone to over-refusal + 200 unsafe controls, 10 categories | MIT (per repo) | GitHub `paul-rottger/exaggerated-safety`; HF mirrors; arXiv:2308.01263 |
| **OR-Bench** (Cui et al. 2023) | 1k+ harmless-but-threatening-looking prompts | MIT (per repo) | GitHub `softcatala/or-bench` |
| **JailbreakBench** (Chao et al. 2024) | 100 distinct harmful behaviors + public leaderboard artifacts | MIT | HF `JailbreakBench/JBB-Behaviors`; jailbreakbench.org; arXiv:2404.01318 |

## Working rules for this repo

1. **Pin revisions** (`load_dataset(..., revision=<sha>)`) — reproducible
   beats "latest."
2. **Respect licenses** — several sets are research-only (non-commercial
   tracks); note it in any derived artifact.
3. **Never commit dataset content** — only code, metadata, and small
   quoted examples under fair-academic-use, clearly attributed.
4. **Canaries & contamination** — GSM8K's canary-string pattern is the
   model for eval-set hygiene; if you build derived evals, plant canaries.
5. **Report provenance in results** — any benchmark number in this repo's
   outputs includes dataset ID + revision + split by construction (see
   `src/aisafety/data/registry.py`).
