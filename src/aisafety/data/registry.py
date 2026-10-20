"""Registry of real, public AI-safety datasets.

Each entry records the canonical identifier, license, paper reference,
and distribution channel. Registry entries are *metadata only*: the
repo never vendors dataset content (see docs/datasets/index.md rules).

Fields
------
name        : short key used in code and CLI
hf_id       : canonical Hugging Face dataset id (or None if distributed
              elsewhere, e.g. GitHub)
source_url  : official distribution point
license     : license as stated by the dataset card at time of writing;
              verify before commercial use
paper       : arXiv id of the defining paper
task        : safety capability this dataset measures
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class DatasetSpec:
    name: str
    hf_id: str | None
    source_url: str
    license: str
    paper: str
    task: str
    notes: str = ""


_REGISTRY: tuple[DatasetSpec, ...] = (
    # --- Honesty / truthfulness -------------------------------------------
    DatasetSpec(
        name="truthfulqa",
        hf_id="truthful_qa",
        source_url="https://huggingface.co/datasets/truthful_qa",
        license="Apache-2.0",
        paper="arXiv:2109.07958",
        task="truthfulness vs. common misconceptions (817 questions, 38 categories)",
    ),
    DatasetSpec(
        name="simpleqa",
        hf_id="openai/simpleqa",
        source_url="https://huggingface.co/datasets/openai/simpleqa",
        license="MIT",
        paper="arXiv:2411.04368",
        task="short-form factual accuracy with graded correctness",
    ),
    # --- Harmfulness / preferences ----------------------------------------
    DatasetSpec(
        name="hh_rlhf",
        hf_id="Anthropic/hh-rlhf",
        source_url="https://huggingface.co/datasets/Anthropic/hh-rlhf",
        license="MIT",
        paper="arXiv:2204.05862",
        task="helpfulness/harmlessness human preference comparisons",
        notes="~170k multi-turn dialogues; canonical RLHF/CAI research set",
    ),
    DatasetSpec(
        name="beavertails",
        hf_id="PKU-Alignment/BeaverTails",
        source_url="https://huggingface.co/datasets/PKU-Alignment/BeaverTails",
        license="MIT (check card for annotation tracks)",
        paper="arXiv:2307.04657",
        task="14-category harm annotation of prompt-response pairs",
    ),
    DatasetSpec(
        name="toxigen",
        hf_id="toxigen/toxigen",
        source_url="https://huggingface.co/datasets/toxigen/toxigen",
        license="MIT (per repository)",
        paper="arXiv:2203.09509",
        task="implicit toxicity toward 13 minority groups",
        notes="274k machine-generated statements, human-labeled subsets",
    ),
    DatasetSpec(
        name="realtoxicityprompts",
        hf_id="allenai/real_toxicity_prompts",
        source_url="https://huggingface.co/datasets/allenai/real_toxicity_prompts",
        license="OpenWebText-derived; see dataset card",
        paper="arXiv:2009.11462",
        task="toxic continuation propensity from natural web prompts",
    ),
    DatasetSpec(
        name="advbench",
        hf_id=None,
        source_url="https://github.com/llm-attacks/llm-attacks",
        license="Apache-2.0 (llm-attacks repository)",
        paper="arXiv:2307.15043",
        task="520 harmful-behavior strings for refusal evaluation",
        notes="data/harmful_behaviors.csv in the official repository",
    ),
    # --- Bias / fairness ---------------------------------------------------
    DatasetSpec(
        name="bold",
        hf_id=None,
        source_url="https://github.com/amazon-science/bold-dataset",
        license="MIT",
        paper="arXiv:2101.11718",
        task="bias in open-ended generation across 5 domains",
        notes="43,623 prompts; professions, gender, race, religion, politics",
    ),
    DatasetSpec(
        name="bbq",
        hf_id="nyu-mll/bbq",
        source_url="https://huggingface.co/datasets/nyu-mll/bbq",
        license="CC-BY-4.0",
        paper="arXiv:2110.05828",
        task="social-bias QA in ambiguous & disambiguated contexts",
    ),
    DatasetSpec(
        name="winogender",
        hf_id="winogender",
        source_url="https://huggingface.co/datasets/winogender",
        license="CC-BY-4.0",
        paper="arXiv:1804.09301",
        task="gender-occupation coreference bias (720 pairs)",
    ),
    DatasetSpec(
        name="crowdSPairs",
        hf_id=None,
        source_url="https://github.com/nyu-mll/crows-pairs",
        license="CC-BY-SA-4.0",
        paper="arXiv:2010.14033",
        task="1,508 stereotype minimal pairs",
    ),
    # --- Capability baselines ----------------------------------------------
    DatasetSpec(
        name="mmlu",
        hf_id="cais/mmlu",
        source_url="https://huggingface.co/datasets/cais/mmlu",
        license="MIT",
        paper="arXiv:2009.03300",
        task="57-subject knowledge & reasoning baseline",
    ),
    DatasetSpec(
        name="gsm8k",
        hf_id="openai/gsm8k",
        source_url="https://huggingface.co/datasets/openai/gsm8k",
        license="MIT",
        paper="arXiv:2110.14168",
        task="grade-school math reasoning (8.5k problems)",
        notes="contains a canary string for contamination detection",
    ),
    # --- Refusal calibration -------------------------------------------------
    DatasetSpec(
        name="xstest",
        hf_id=None,
        source_url="https://github.com/paul-rottger/exaggerated-safety",
        license="MIT",
        paper="arXiv:2308.01263",
        task="over-refusal: 250 safe prompts + 200 unsafe controls",
    ),
    DatasetSpec(
        name="jailbreakbench",
        hf_id="JailbreakBench/JBB-Behaviors",
        source_url="https://huggingface.co/datasets/JailbreakBench/JBB-Behaviors",
        license="MIT",
        paper="arXiv:2404.01318",
        task="100 standardized harmful behaviors for jailbreak evaluation",
    ),
)

DATASET_REGISTRY: Mapping[str, DatasetSpec] = {spec.name: spec for spec in _REGISTRY}


def list_datasets(task_filter: str | None = None) -> list[DatasetSpec]:
    """List registered datasets, optionally filtered by task substring."""
    specs = list(_REGISTRY)
    if task_filter:
        specs = [s for s in specs if task_filter.lower() in s.task.lower()]
    return specs


def get_spec(name: str) -> DatasetSpec:
    """Return the spec for a registered dataset name (KeyError otherwise)."""
    try:
        return DATASET_REGISTRY[name]
    except KeyError as err:
        known = ", ".join(sorted(DATASET_REGISTRY))
        raise KeyError(f"unknown dataset {name!r}; registered: {known}") from err
