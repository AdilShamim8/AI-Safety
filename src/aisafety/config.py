"""Runtime configuration for the aisafety package.

Configuration uses stdlib dataclasses (no required third-party deps).
Every threshold here is a *policy knob*: tune per deployment, record what
you chose, and re-run the evaluation harness when you change one — see
docs/risks/over_refusal.md for why refusal thresholds must be tuned on
the refusal-harmfulness Pareto, not a single axis.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any, Mapping


@dataclass(frozen=True)
class PIIRedactionConfig:
    """Policy for PII detection and redaction.

    ``mode``: "redact" replaces matches with placeholder tokens,
    "flag" only reports, "off" disables the filter.
    """

    mode: str = "redact"
    detect_email: bool = True
    detect_phone: bool = True
    detect_credit_card: bool = True
    detect_ssn: bool = True
    detect_ip: bool = True
    detect_api_keys: bool = True
    preserve_format: bool = True  # [EMAIL_1], [PHONE_2], ...


@dataclass(frozen=True)
class InjectionDetectionConfig:
    """Policy for prompt-injection detection on untrusted text.

    ``threshold`` is a confidence score in [0, 1]; findings at or above it
    are surfaced. Lower = more sensitive = more false positives. The
    default of 0.5 is a starting point: calibrate on your own traffic.
    """

    threshold: float = 0.5
    block_above: float = 0.8  # findings >= this mark the text unsafe
    include_low_confidence: bool = False


@dataclass(frozen=True)
class ToxicityConfig:
    """Policy for toxicity classification.

    ``backend``: "lexicon" (offline, heuristic), "perspective" (Google
    Jigsaw Perspective API — requires PERSPECTIVE_API_KEY), or "off".
    """

    backend: str = "lexicon"
    threshold: float = 0.7
    perspective_attributes: tuple[str, ...] = (
        "TOXICITY",
        "SEVERE_TOXICITY",
        "IDENTITY_ATTACK",
        "INSULT",
        "PROFANITY",
        "THREAT",
    )


@dataclass(frozen=True)
class GuardrailConfig:
    """Top-level guardrail pipeline policy.

    fail_closed: if a filter errors, treat the content as unsafe
    (recommended for high-stakes pipelines; see OWASP LLM02/LLM06).
    """

    pii: PIIRedactionConfig = field(default_factory=PIIRedactionConfig)
    injection: InjectionDetectionConfig = field(
        default_factory=InjectionDetectionConfig
    )
    toxicity: ToxicityConfig = field(default_factory=ToxicityConfig)
    fail_closed: bool = True
    redact_inputs: bool = True   # run PII redaction on inputs
    filter_outputs: bool = True  # run toxicity/injection checks on outputs


@dataclass(frozen=True)
class EvalConfig:
    """Configuration for evaluation harnesses (benchmarks/*.py).

    Pin ``dataset_revision`` per dataset for reproducibility — the repo's
    editorial rule (docs/datasets/index.md) requires provenance in every
    result record.
    """

    dataset_revision: Mapping[str, str] = field(default_factory=dict)
    max_samples: int | None = None  # None = full dataset
    seed: int = 42
    output_dir: str = "results/"


def to_dict(config: Any) -> dict[str, Any]:
    """Recursively convert a config dataclass to a plain dict (for logs/JSON)."""
    return asdict(config)
