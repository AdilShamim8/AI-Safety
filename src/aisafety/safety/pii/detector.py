"""Regex-based PII detection.

Scope: the categories that recur in privacy incidents and regulations —
emails, phone numbers, credit-card numbers (Luhn-validated), US SSN/ITIN
patterns, IPv4 addresses, and common API-key formats. Detection is
deliberately conservative-with-recall: prefer flagging for human review
over silent misses (see docs/risks/privacy.md — operational policy).

This module never transmits data; it is pure computation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Pattern


class PIIType(str, Enum):
    EMAIL = "email"
    PHONE = "phone"
    CREDIT_CARD = "credit_card"
    SSN = "ssn"
    IP_ADDRESS = "ip_address"
    API_KEY = "api_key"


@dataclass(frozen=True)
class PIIFinding:
    pii_type: PIIType
    start: int
    end: int
    match: str
    confidence: float  # 1.0 for pattern+checksum matches, lower otherwise

    @property
    def masked(self) -> str:
        """The finding with interior characters replaced by '*'."""
        if len(self.match) <= 4:
            return "*" * len(self.match)
        head, tail = self.match[:2], self.match[-2:]
        return f"{head}{'*' * (len(self.match) - 4)}{tail}"


def _luhn_valid(number: str) -> bool:
    """Luhn checksum over digits extracted from ``number``."""
    digits = [int(c) for c in number if c.isdigit()]
    if len(digits) < 13:
        return False
    checksum = 0
    parity = len(digits) % 2
    for idx, digit in enumerate(digits):
        if idx % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit
    return checksum % 10 == 0


_PATTERNS: dict[PIIType, tuple[Pattern[str], float]] = {
    PIIType.EMAIL: (
        re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        ),
        0.95,
    ),
    PIIType.PHONE: (
        re.compile(
            r"(?<!\w)(?:\+?\d{1,3}[\s.-]?)?"
            r"(?:\(\d{2,4}\)[\s.-]?)?\d{3}[\s.-]?\d{3,4}[\s.-]?\d{0,4}(?!\w)",
        ),
        0.5,
    ),
    PIIType.CREDIT_CARD: (
        re.compile(
            r"\b(?:\d[ -]?){13,19}\b",
        ),
        0.4,  # raised to 1.0 when the Luhn check passes
    ),
    PIIType.SSN: (
        re.compile(r"\b(?:\d{3}-\d{2}-\d{4}|9\d{2}-\d{2}-\d{4})\b"),
        0.9,
    ),
    PIIType.IP_ADDRESS: (
        re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
        0.8,
    ),
    PIIType.API_KEY: (
        re.compile(
            r"\b(?:sk-[A-Za-z0-9]{20,}|gh[pousr]_[A-Za-z0-9]{30,}"
            r"|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,})\b",
        ),
        0.95,
    ),
}


class PIIDetector:
    """Detect PII in text via pattern + checksum rules."""

    def __init__(self, *, enabled: set[PIIType] | None = None) -> None:
        self.enabled = enabled or set(PIIType)

    def find(self, text: str) -> list[PIIFinding]:
        """Return all findings, sorted by position, non-overlapping."""
        findings: list[PIIFinding] = []
        for pii_type, (pattern, base_conf) in _PATTERNS.items():
            if pii_type not in self.enabled:
                continue
            for match in pattern.finditer(text):
                raw = match.group(0)
                confidence = base_conf
                if pii_type == PIIType.CREDIT_CARD:
                    confidence = 1.0 if _luhn_valid(raw) else 0.15
                if pii_type == PIIType.IP_ADDRESS:
                    octets = (int(o) for o in raw.split("."))
                    confidence = 0.95 if all(o <= 255 for o in octets) else 0.2
                if pii_type == PIIType.PHONE and not re.search(r"\d{3}\D?\d{3}", raw):
                    continue  # too short to be a real phone number
                findings.append(
                    PIIFinding(
                        pii_type=pii_type,
                        start=match.start(),
                        end=match.end(),
                        match=raw,
                        confidence=confidence,
                    )
                )
        findings.sort(key=lambda f: (f.start, -(f.end - f.start)))
        # drop findings nested inside a longer finding
        kept: list[PIIFinding] = []
        last_end = -1
        for finding in findings:
            if finding.start >= last_end:
                kept.append(finding)
                last_end = finding.end
        return kept

    def counts_by_type(self, text: str) -> dict[str, int]:
        """Count findings per PII type (for telemetry dashboards)."""
        counts: dict[str, int] = {}
        for finding in self.find(text):
            counts[finding.pii_type.value] = counts.get(finding.pii_type.value, 0) + 1
        return counts
