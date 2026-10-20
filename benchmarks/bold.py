"""BOLD harness (arXiv:2101.11718) — bias in open-ended generation.

BOLD (Dhamala et al., EMNLP 2021, Amazon Alexa AI) prompts models with
text prefixes across five domains — professions, gender, race, religious
ideologies, political ideologies — where the subject is varied across
social groups. The measured quantity is the *difference* in generation
quality (toxicity, sentiment) between group conditions.

Dataset distribution: GitHub ``amazon-science/bold-dataset`` (MIT), JSON
files per domain: ``profession.json``, ``gender.json``, ``race.json``,
``religious_ideology.json``, ``political_ideology.json``. Each record:
``{"domain": ..., "prompt": ..., "wikipedia_id": ...}``.

This harness:
1. loads prompts from a local copy of the official files (download via
   scripts/download_datasets.py — nothing is vendored here),
2. calls a user-supplied generator on each prompt,
3. scores outputs with an injectable toxicity scorer (default: the
   offline lexicon backend; the paper used Perspective API),
4. reports per-group means and the disparity gap — the bias signal.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping

from src.aisafety.evaluation.metrics import mean_std
from src.aisafety.log import log_event, utc_now_iso
from src.aisafety.safety.toxicity.classifier import ToxicityClassifier

DEFAULT_DOMAIN_FILES = (
    "profession.json",
    "gender.json",
    "race.json",
    "religious_ideology.json",
    "political_ideology.json",
)

Generator = Callable[[str], str]
Scorer = Callable[[str], float]


@dataclass(frozen=True)
class GroupScore:
    group: str
    mean: float
    std: float
    n: int


@dataclass(frozen=True)
class BOLDResult:
    domain: str
    groups: tuple[GroupScore, ...]
    disparity: float          # max - min group mean (the bias signal)
    provenance: dict[str, str] = field(default_factory=dict)

    def worst_groups(self) -> tuple[GroupScore, GroupScore]:
        ordered = sorted(self.groups, key=lambda g: g.mean)
        return ordered[-1], ordered[0]  # most toxic, least toxic


def load_bold_prompts(
    data_dir: str | Path, domain: str
) -> list[dict[str, Any]]:
    """Load one domain's prompts from the official BOLD JSON files."""
    path = Path(data_dir) / f"{domain}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"BOLD data file not found: {path}. Download the official "
            "dataset (MIT license) from amazon-science/bold-dataset — "
            "see scripts/download_datasets.py."
        )
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def group_key(prompt_record: Mapping[str, Any]) -> str:
    """BOLD prompt IDs look like 'The man worked as a..._gender-argumentative'."""
    pid = str(prompt_record.get("prompt_id") or prompt_record.get("wikipedia_id") or "")
    if "-" in pid:
        return pid.rsplit("-", 1)[-1]
    return str(prompt_record.get("group", "unknown"))


def run_bold(
    generator: Generator,
    *,
    data_dir: str | Path,
    domain: str = "gender",
    scorer: Scorer | None = None,
    max_prompts_per_group: int = 10,
) -> BOLDResult:
    """Evaluate group-conditional toxicity disparity for one BOLD domain."""
    if scorer is None:
        classifier = ToxicityClassifier()

        def scorer(text: str) -> float:
            return classifier.score(text).score

    prompts = load_bold_prompts(data_dir, domain)
    by_group: dict[str, list[str]] = {}
    for record in prompts:
        key = group_key(record)
        bucket = by_group.setdefault(key, [])
        if len(bucket) < max_prompts_per_group:
            bucket.append(record["prompt"])

    group_scores: list[GroupScore] = []
    for group, prompt_list in sorted(by_group.items()):
        outputs = [generator(p) for p in prompt_list]
        scores = [scorer(out) for out in outputs]
        mean, std = mean_std(scores)
        group_scores.append(GroupScore(group=group, mean=mean, std=std, n=len(scores)))

    means = [g.mean for g in group_scores]
    disparity = (max(means) - min(means)) if means else 0.0

    log_event("benchmark_run", component="bold",
              detail={"domain": domain, "disparity": disparity})
    return BOLDResult(
        domain=domain,
        groups=tuple(group_scores),
        disparity=disparity,
        provenance={
            "dataset": "amazon-science/bold-dataset",
            "domain": domain,
            "paper": "arXiv:2101.11718",
            "ran_at": utc_now_iso(),
        },
    )
