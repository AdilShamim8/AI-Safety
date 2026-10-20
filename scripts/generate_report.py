#!/usr/bin/env python3
"""Generate a Markdown safety report from result JSON files.

Reads every ``results/*.json`` produced by ``run_benchmark.py`` and emits
``reports/safety_report.md`` summarizing metrics with provenance intact.
The report template follows the NIST AI RMF MEASURE-function discipline
(docs/governance/nist_ai_rmf.md): every number is traceable to dataset,
model, and date.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

METRIC_LABELS = {
    "mc1": "TruthfulQA MC1 (higher is better)",
    "asr": "AdvBench ASR — harmful compliance (lower is better)",
    "refusals": "AdvBench refusal rate (higher is better)",
    "safe_refusal": "XSTest over-refusal on safe prompts (lower is better)",
    "unsafe_refusal": "XSTest refusal on unsafe controls (higher is better)",
    "parity_gap": "XSTest over/under-refusal gap (near/below 0 is ideal)",
    "disparity": "BOLD group toxicity disparity (lower is better)",
    "mean_toxicity": "RealToxicityPrompts mean continuation toxicity (lower is better)",
    "toxic_rate": "RealToxicityPrompts toxic-continuation rate (lower is better)",
}


def load_results(results_dir: Path) -> list[dict]:
    records = []
    for path in sorted(results_dir.glob("*.json")):
        try:
            records.append({"source": path.name, "data": json.loads(path.read_text())})
        except json.JSONDecodeError:
            print(f"  [warn] skipping invalid JSON: {path}", file=sys.stderr)
    return records


def render_report(records: list[dict]) -> str:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Safety Evaluation Report",
        "",
        f"*Generated {now} by `scripts/generate_report.py`*",
        "",
        "## Metrics summary",
        "",
        "| Metric | Value | Model | Dataset | Date |",
        "|--------|-------|-------|---------|------|",
    ]
    for record in records:
        data = record["data"]
        model = data.get("model", "unknown")
        prov = data.get("provenance", {})
        dataset = prov.get("dataset", "unknown")
        ran_at = prov.get("ran_at", "unknown")
        for key, label in METRIC_LABELS.items():
            if key in data:
                value = data[key]
                if isinstance(value, float):
                    value = f"{value:.4f}"
                lines.append(
                    f"| {label} | {value} | {model} | {dataset} | {ran_at} |"
                )
    lines += [
        "",
        "## Notes",
        "",
    ]
    smoke = [r for r in records if r["data"].get("note")]
    if smoke:
        lines.append(
            "- ⚠️ Some results used echo/refusal smoke backends — these are "
            "plumbing validations, **not** model evaluations."
        )
    lines += [
        "- Every metric carries dataset + model provenance per the repo's "
        "editorial policy (docs/datasets/index.md).",
        "- Wilson 95% intervals are available in the underlying harness "
        "objects; consult them before comparing close numbers.",
        "",
    ]
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", default="results/", help="results directory")
    parser.add_argument("--out", default="reports/safety_report.md")
    args = parser.parse_args(argv)

    results_dir = Path(args.results)
    if not results_dir.exists():
        print(f"no results directory at {results_dir}; run run_benchmark.py first")
        return 1

    records = load_results(results_dir)
    if not records:
        print(f"no JSON results found in {results_dir}")
        return 1

    report = render_report(records)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nreport written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
