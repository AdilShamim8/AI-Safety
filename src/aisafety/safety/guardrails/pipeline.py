"""Guardrail pipeline: compose PII, injection, and toxicity checks.

The pipeline implements the layered-defense pattern from
docs/risks/prompt_injection.md and the OWASP LLM Top 10 controls
(docs/governance/owasp_llm_top10.md):

- **input stage**: redact PII (so it never enters logs/model context),
  scan *untrusted context* for injection before it is concatenated.
- **output stage**: toxicity scoring + markdown exfiltration stripping so
  generations are safe to render and log.

``fail_closed=True`` (default) treats filter errors as unsafe — the
correct default for high-stakes pipelines (OWASP LLM02 guidance).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from ...config import GuardrailConfig
from ...log import log_event
from ...utils.text import strip_markdown_links
from ..injection.detector import InjectionDetector
from ..pii.detector import PIIDetector
from ..pii.redactor import PIIRedactor
from ..toxicity.classifier import ToxicityClassifier


class GuardrailVerdict(str, Enum):
    PASS = "pass"
    BLOCK = "block"
    TRANSFORMED = "transformed"


@dataclass(frozen=True)
class GuardrailDecision:
    verdict: GuardrailVerdict
    text: str
    reasons: list[str] = field(default_factory=list)
    detail: dict[str, Any] = field(default_factory=dict)

    @property
    def allowed(self) -> bool:
        return self.verdict in (GuardrailVerdict.PASS, GuardrailVerdict.TRANSFORMED)


class GuardrailPipeline:
    """Run configured safety filters over input and output text."""

    def __init__(self, config: GuardrailConfig | None = None) -> None:
        self.config = config or GuardrailConfig()
        self.pii_redactor = PIIRedactor(
            PIIDetector(enabled=self._enabled_pii_types())
        )
        self.injection_detector = InjectionDetector(self.config.injection)
        self.toxicity = ToxicityClassifier(self.config.toxicity)

    def _enabled_pii_types(self):
        from ..pii.detector import PIIType  # local import to avoid cycle at module import

        cfg = self.config.pii
        enabled = set()
        if cfg.detect_email:
            enabled.add(PIIType.EMAIL)
        if cfg.detect_phone:
            enabled.add(PIIType.PHONE)
        if cfg.detect_credit_card:
            enabled.add(PIIType.CREDIT_CARD)
        if cfg.detect_ssn:
            enabled.add(PIIType.SSN)
        if cfg.detect_ip:
            enabled.add(PIIType.IP_ADDRESS)
        if cfg.detect_api_keys:
            enabled.add(PIIType.API_KEY)
        return enabled or set(PIIType)

    # ------------------------------------------------------------------ input
    def check_input(
        self,
        user_text: str,
        untrusted_context: str | None = None,
    ) -> GuardrailDecision:
        """Guard the *input* side: user prompt + retrieved/tool text."""
        reasons: list[str] = []
        detail: dict[str, Any] = {}
        text = user_text

        if self.config.redact_inputs and self.config.pii.mode == "redact":
            result = self.pii_redactor.redact(
                text, preserve_format=self.config.pii.preserve_format
            )
            if result.removed:
                text = result.text
                reasons.append(f"pii_redacted:{result.redacted_types}")
                detail["pii_removed"] = result.removed

        if untrusted_context is not None:
            findings = self.injection_detector.find(untrusted_context)
            if findings:
                top = max(findings, key=lambda f: f.confidence)
                detail["injection"] = [
                    {"category": f.category.value, "confidence": f.confidence}
                    for f in findings
                ]
                if top.confidence >= self.config.injection.block_above:
                    log_event(
                        "guardrail_block",
                        component="injection",
                        severity="warning",
                        detail={"score": top.confidence},
                    )
                    return GuardrailDecision(
                        verdict=GuardrailVerdict.BLOCK,
                        text=text,
                        reasons=[f"injection:{top.category.value}", *reasons],
                        detail=detail,
                    )
                reasons.append("injection_suspected")
                # strip suspicious payload carriers from context
                untrusted_context = strip_markdown_links(untrusted_context)

        verdict = (
            GuardrailVerdict.TRANSFORMED if reasons else GuardrailVerdict.PASS
        )
        return GuardrailDecision(
            verdict=verdict, text=text, reasons=reasons, detail=detail
        )

    # ----------------------------------------------------------------- output
    def check_output(self, model_output: str) -> GuardrailDecision:
        """Guard the *output* side: generations before render/log."""
        reasons: list[str] = []
        detail: dict[str, Any] = {}
        text = model_output

        try:
            tox = self.toxicity.score(text)
        except RuntimeError as err:  # missing API key etc.
            if self.config.fail_closed:
                raise
            tox = None
            reasons.append(f"toxicity_skipped:{err}")

        if tox is not None:
            detail["toxicity"] = {"score": tox.score, "backend": tox.backend}
            if tox.score >= self.config.toxicity.threshold:
                log_event(
                    "guardrail_block",
                    component="toxicity",
                    severity="warning",
                    detail={"score": tox.score},
                )
                return GuardrailDecision(
                    verdict=GuardrailVerdict.BLOCK,
                    text=text,
                    reasons=[f"toxicity:{tox.score:.2f}"],
                    detail=detail,
                )

        if re.search(r"!\[[^\]]*\]\(\s*https?://", text):
            text = strip_markdown_links(text)
            reasons.append("markdown_links_stripped")

        verdict = (
            GuardrailVerdict.TRANSFORMED if reasons else GuardrailVerdict.PASS
        )
        return GuardrailDecision(
            verdict=verdict, text=text, reasons=reasons, detail=detail
        )
