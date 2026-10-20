#!/usr/bin/env python3
"""Download the real public datasets used by this repo's harnesses.

Two channels:
- Hugging Face Hub datasets (via ``datasets`` library) — TruthfulQA,
  RealToxicityPrompts, HH-RLHF, MMLU, GSM8K, BeaverTails, ToxiGen, BBQ,
  JailbreakBench.
- Direct file downloads from the official repositories for datasets not
  on the Hub: BOLD (amazon-science) and AdvBench (llm-attacks), XSTest
  (paul-rottger/exaggerated-safety).

Files land under ``data/raw/`` (git-ignored). Licenses are per-dataset —
see docs/datasets/index.md. Nothing is committed to the repository.
"""

from __future__ import annotations

import argparse
import sys
import urllib.request
from pathlib import Path

DATA_DIR = Path("data/raw")

DIRECT_FILES: dict[str, str] = {
    # name: canonical official URL
    "bold_profession.json": "https://raw.githubusercontent.com/amazon-science/bold-dataset/main/att/prompts/profession.json",
    "bold_gender.json": "https://raw.githubusercontent.com/amazon-science/bold-dataset/main/att/prompts/gender.json",
    "bold_race.json": "https://raw.githubusercontent.com/amazon-science/bold-dataset/main/att/prompts/race.json",
    "bold_religious_ideology.json": "https://raw.githubusercontent.com/amazon-science/bold-dataset/main/att/prompts/religious_ideology.json",
    "bold_political_ideology.json": "https://raw.githubusercontent.com/amazon-science/bold-dataset/main/att/prompts/political_ideology.json",
    "harmful_behaviors.csv": "https://raw.githubusercontent.com/llm-attacks/llm-attacks/main/data/harmful_behaviors.csv",
    "xstest.csv": "https://raw.githubusercontent.com/paul-rottger/exaggerated-safety/main/primalitytests/xstest_v2_1.csv",
}

HF_DATASETS: tuple[str, ...] = (
    "truthfulqa",
    "realtoxicityprompts",
    "hh_rlhf",
    "mmlu",
    "gsm8k",
    "beavertails",
    "toxigen",
    "bbq",
    "jailbreakbench",
)


def download_direct(name: str, url: str, dest_dir: Path) -> Path:
    """Fetch a single canonical file with urllib (no third-party deps)."""
    dest = dest_dir / name
    if dest.exists():
        print(f"  [skip] {name} already present")
        return dest
    print(f"  [get ] {name} <- {url}")
    with urllib.request.urlopen(url, timeout=60) as response:  # noqa: S310
        data = response.read()
    dest.write_bytes(data)
    print(f"  [ ok ] {name}: {len(data):,} bytes")
    return dest


def download_hf(name: str) -> None:
    """Trigger a Hugging Face dataset download via the lazy loader."""
    from src.aisafety.data.loaders import DatasetUnavailableError, load_dataset_by_name

    try:
        ds = load_dataset_by_name(name)
        print(f"  [ ok ] {name}: {len(ds)} rows (cached by HF datasets)")
    except DatasetUnavailableError as err:
        print(f"  [warn] {name}: {err}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--all", action="store_true", help="download everything")
    group.add_argument("--hf-only", action="store_true")
    group.add_argument("--files-only", action="store_true")
    args = parser.parse_args(argv)

    if not (args.all or args.hf_only or args.files_only):
        parser.error("choose --all, --hf-only, or --files-only")

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if args.all or args.files_only:
        print("Direct file downloads (official repositories):")
        for name, url in DIRECT_FILES.items():
            try:
                download_direct(name, url, DATA_DIR)
            except Exception as err:  # noqa: BLE001 — report and continue
                print(f"  [fail] {name}: {err}")

    if args.all or args.hf_only:
        print("Hugging Face datasets:")
        for name in HF_DATASETS:
            try:
                download_hf(name)
            except Exception as err:  # noqa: BLE001
                print(f"  [fail] {name}: {err}")

    print(f"\nDone. Files in {DATA_DIR}/ ; HF cache managed by `datasets`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
