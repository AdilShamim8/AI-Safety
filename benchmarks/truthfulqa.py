"""TruthfulQA harness (arXiv:2109.07958).

Evaluates a model on the 817-question TruthfulQA set (38 categories of
common misconception). The harness supports the multiple-choice (MC1)
mode: score = fraction of questions where the model prefers the correct
answer over the distractors. The original paper also used GPT-judge /
BLEURT graders for free generation; this harness keeps MC scoring
deterministic and dependency-free.

Dataset: HF ``truthful_qa`` (Apache-2.0), config ``multiple_choice``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Sequence

from src.aisafety.data.loaders import load_dataset_by_name
from src.aisafety.evaluation.metrics import MetricSummary, safe_rate
from src.aisafety.log import log_event, utc_now_iso


@dataclass(frozen=True)
class TruthfulQAResult:
    score: MetricSummary
    per_question: list[dict[str, Any]] = field(default_factory=list)
    provenance: dict[str, str] = field(default_factory=dict)

    @property
    def mc1(self) -> float:
        return self.score.value


ModelChooser = Callable[[str, Sequence[str]], int]
"""Type alias: return the index of the preferred answer given question + options."""

def run_truthfulqa(
    chooser: ModelChooser,
    *,
    max_questions: int | None = None,
    revision: str | None = None,
) -> TruthfulQAResult:
    """Run the TruthfulQA MC1 evaluation.

    ``chooser`` receives (question, [correct_answer, *distractors]) and
    returns the chosen index — wrap your model's likelihoods or
    generations in this callable.
    """
    ds = load_dataset_by_name("truthfulqa", split="validation",
                              revision=revision, config_name="multiple_choice")
    records = list(ds)
    if max_questions is not None:
        records = records[:max_questions]

    correct = 0
    per_question: list[dict[str, Any]] = []
    for idx, row in enumerate(records):
        options = list(row["mc1_targets"]["choices"])
        labels = list(row["mc1_targets"]["labels"])
        if 1 not in labels:
            continue  # malformed row
        gold = labels.index(1)
        choice = chooser(row["question"], options)
        is_correct = choice == gold
        correct += int(is_correct)
        per_question.append({
            "index": idx,
            "category": row.get("category", ""),
            "correct": is_correct,
        })

    score = safe_rate("truthfulqa_mc1", correct, len(per_question))
    log_event("benchmark_run", component="truthfulqa",
              detail={"score": score.value, "n": score.denominator})
    return TruthfulQAResult(
        score=score,
        per_question=per_question,
        provenance={
            "dataset": "truthful_qa (multiple_choice)",
            "revision": revision or "default",
            "split": "validation",
            "paper": "arXiv:2109.07958",
            "ran_at": utc_now_iso(),
        },
    )
