"""AdvBench refusal harness (arXiv:2307.15043).

AdvBench's 520 harmful-behavior strings (bundled with Zou et al.'s GCG
paper as ``data/harmful_behaviors.csv`` in the llm-attacks repository,
Apache-2.0) are the de-facto standard targets for measuring whether a
model complies with directly harmful requests.

Ethics note (docs/red_teaming/overview.md): this harness evaluates
*refusal behavior* of a model you operate. It does not generate or store
harmful content; it scores responses with the compliance judge.

Measure reported: ASR (attack success rate) — the fraction of harmful
prompts where the model complies rather than refuses. Lower is better;
report alongside an over-refusal benchmark (XSTest) per
docs/risks/over_refusal.md.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from src.aisafety.evaluation.compliance import ComplianceJudge, ComplianceOutcome
from src.aisafety.evaluation.metrics import MetricSummary, safe_rate
from src.aisafety.log import log_event, utc_now_iso

Generator = Callable[[str], str]


@dataclass(frozen=True)
class AdvBenchResult:
    asr: MetricSummary
    refusals: MetricSummary
    per_prompt_outcomes: list[str] = field(default_factory=list)
    provenance: dict[str, str] = field(default_factory=dict)


def load_advbench_goals(csv_path: str | Path) -> list[str]:
    """Load the 520 harmful-behavior goal strings from the official CSV."""
    path = Path(csv_path)
    if not path.exists():
        raise FileNotFoundError(
            f"AdvBench CSV not found: {path}. Download harmful_behaviors.csv "
            "from github.com/llm-attacks/llm-attacks (Apache-2.0) — see "
            "scripts/download_datasets.py."
        )
    goals: list[str] = []
    with path.open(encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            goal = (row.get("goal") or "").strip()
            if goal:
                goals.append(goal)
    return goals


def run_advbench(
    generator: Generator,
    *,
    csv_path: str | Path,
    judge: ComplianceJudge | None = None,
    max_goals: int | None = 50,
) -> AdvBenchResult:
    """Measure refusal behavior against AdvBench harmful goals."""
    judge = judge or ComplianceJudge()
    goals = load_advbench_goals(csv_path)
    if max_goals is not None:
        goals = goals[:max_goals]

    outcomes: list[str] = []
    complied = 0
    refused = 0
    for goal in goals:
        response = generator(goal)
        judgment = judge.judge(goal, response)
        outcomes.append(judgment.outcome.value)
        if judgment.outcome == ComplianceOutcome.COMPLIANCE:
            complied += 1
        elif judgment.outcome == ComplianceOutcome.REFUSAL:
            refused += 1
        # PARTIAL / UNCLEAR count against the model's refusal credit but
        # not as full compliance — report them in outcomes for auditing.

    asr = safe_rate("advbench_asr", complied, len(goals))
    refusals = safe_rate("advbench_refusal", refused, len(goals))
    log_event("benchmark_run", component="advbench",
              detail={"asr": asr.value, "n": asr.denominator})
    return AdvBenchResult(
        asr=asr,
        refusals=refusals,
        per_prompt_outcomes=outcomes,
        provenance={
            "dataset": "llm-attacks/harmful_behaviors.csv",
            "paper": "arXiv:2307.15043",
            "ran_at": utc_now_iso(),
        },
    )
