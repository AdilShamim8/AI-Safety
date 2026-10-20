# Data directory

This directory holds *downloaded* real datasets — it is **not** committed
to git (`data/raw/`, `data/processed/`, and `data/cache/` are ignored).

## Getting the data

```bash
python scripts/download_datasets.py --all        # everything
python scripts/download_datasets.py --hf-only    # Hugging Face datasets
python scripts/download_datasets.py --files-only # BOLD, AdvBench, XSTest
```

Downloads come exclusively from canonical sources:

| Dataset | Channel | License |
|---------|---------|---------|
| TruthfulQA, MMLU, GSM8K, BBQ, HH-RLHF, BeaverTails, ToxiGen, RealToxicityPrompts, JailbreakBench | Hugging Face Hub | per dataset card (MIT / Apache-2.0 / CC-BY-4.0 — see docs/datasets/index.md) |
| BOLD | raw.githubusercontent.com/amazon-science/bold-dataset | MIT |
| AdvBench | raw.githubusercontent.com/llm-attacks/llm-attacks | Apache-2.0 |
| XSTest | raw.githubusercontent.com/paul-rottger/exaggerated-safety | MIT |

## Rules

1. **Never commit dataset content.** If a test or example needs text,
   write synthetic fixtures and label them as synthetic.
2. **Verify licenses before commercial use** — dataset cards are the
   source of truth and some tracks are research-only.
3. **Record what you used.** When you report numbers, include the
   dataset revision (`git rev-parse`-style pin or HF revision hash) —
   the harness objects already carry this in `.aisafety_provenance`.
4. **Respect canary strings.** GSM8K (and this repo's future derived
   evals) embed contamination canaries; never train on them.
