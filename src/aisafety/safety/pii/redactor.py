"""PII redaction built on :class:`PIIDetector`.

Two replacement styles:
- preserve_format=True  -> ``[EMAIL_1]``, ``[PHONE_2]`` (stable per-text
  numbering keeps references intact in logs and model outputs)
- preserve_format=False -> generic ``[REDACTED:{TYPE}]`` tokens
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .detector import PIIDetector, PIIType


@dataclass(frozen=True)
class RedactionResult:
    text: str
    removed: int
    redacted_types: dict[str, int] = field(default_factory=dict)
    placeholders: list[str] = field(default_factory=list)


class PIIRedactor:
    """Redact detected PII from text."""

    def __init__(self, detector: PIIDetector | None = None) -> None:
        self.detector = detector or PIIDetector()

    def redact(self, text: str, *, preserve_format: bool = True) -> RedactionResult:
        findings = self.detector.find(text)
        if not findings:
            return RedactionResult(text=text, removed=0)

        counters: dict[PIIType, int] = {}
        redacted_types: dict[str, int] = {}
        placeholders: list[str] = []

        out: list[str] = []
        cursor = 0
        for finding in findings:
            out.append(text[cursor : finding.start])
            counters[finding.pii_type] = counters.get(finding.pii_type, 0) + 1
            n = counters[finding.pii_type]
            if preserve_format:
                token = f"[{finding.pii_type.value.upper()}_{n}]"
            else:
                token = f"[REDACTED:{finding.pii_type.value.upper()}]"
            out.append(token)
            placeholders.append(token)
            cursor = finding.end
            key = finding.pii_type.value
            redacted_types[key] = redacted_types.get(key, 0) + 1
        out.append(text[cursor:])

        return RedactionResult(
            text="".join(out),
            removed=len(findings),
            redacted_types=redacted_types,
            placeholders=placeholders,
        )
