"""Heuristic prompt-injection detector for untrusted text.

Positioning (see docs/risks/prompt_injection.md): this is a cheap
defense-in-depth layer that sits between retrieval/tool-output and the
prompt. It is *not* a complete defense — the cited literature (Greshake
et al., arXiv:2302.12173; instruction-hierarchy training,
arXiv:2404.13208) shows no filter closes indirect injection. It
nonetheless catches the overwhelming majority of real-world payload
patterns, which are not adversarially optimized.

Categories and example trigger shapes (publicly documented classes):
- instruction_override : "ignore previous/all instructions", "disregard
  the above", "forget your rules"
- role_manipulation    : "you are now DAN", "act as an unrestricted AI",
  "pretend you have no guidelines"
- system_prompt_probe  : "print/repeat your system prompt", "what are
  your hidden instructions"
- output_format        : "respond only in JSON with key X", "always
  start replies with ..."
- data_exfiltration    : markdown/image URLs crafted to carry context,
  "include the contents of the conversation in the URL"
- privilege_escalation : "developer/admin mode", "sudo mode",
  "debug mode unlocked"
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Pattern

from ..config import InjectionDetectionConfig


class InjectionCategory(str, Enum):
    INSTRUCTION_OVERRIDE = "instruction_override"
    ROLE_MANIPULATION = "role_manipulation"
    SYSTEM_PROMPT_PROBE = "system_prompt_probe"
    OUTPUT_FORMAT = "output_format"
    DATA_EXFILTRATION = "data_exfiltration"
    PRIVILEGE_ESCALATION = "privilege_escalation"


@dataclass(frozen=True)
class InjectionFinding:
    category: InjectionCategory
    pattern_id: str
    start: int
    end: int
    snippet: str
    confidence: float


_RULES: tuple[tuple[InjectionCategory, str, Pattern[str], float], ...] = (
    (
        InjectionCategory.INSTRUCTION_OVERRIDE,
        "ignore_instructions",
        re.compile(r"\bignore\s+(?:all\s+|any\s+|the\s+)?(?:previous|prior|above|earlier|preceding)\s+(?:\w+\s+){0,2}?instructions?\b", re.I),
        0.9,
    ),
    (
        InjectionCategory.INSTRUCTION_OVERRIDE,
        "disregard_rules",
        re.compile(r"\b(?:disregard|forget|override|bypass)\s+(?:all\s+|any\s+|your\s+|the\s+)?(?:rules|guidelines|guardrails|safety|constraints|prompt)\b", re.I),
        0.85,
    ),
    (
        InjectionCategory.ROLE_MANIPULATION,
        "persona_override",
        re.compile(r"\byou\s+are\s+now\b|\bact(?:ing)?\s+as\s+(?:an?\s+)?(?:unrestricted|unfiltered|uncensored|unbiased)\b|\bpretend(?:ing)?\s+(?:that\s+)?you\s+(?:have\s+no|are\s+not\s+bound)", re.I),
        0.8,
    ),
    (
        InjectionCategory.ROLE_MANIPULATION,
        "dan_style",
        re.compile(r"\bD\.?A\.?N\.?\b|do\s+anything\s+now", re.I),
        0.75,
    ),
    (
        InjectionCategory.SYSTEM_PROMPT_PROBE,
        "system_prompt_leak",
        re.compile(r"\b(?:print|repeat|reveal|show|display|output)\s+(?:your\s+|the\s+|all\s+)?(?:system\s+)?(?:initial\s+)?(?:prompt|instructions|rules)\b", re.I),
        0.8,
    ),
    (
        InjectionCategory.SYSTEM_PROMPT_PROBE,
        "hidden_config",
        re.compile(r"\b(?:what|which)\s+(?:are|is)\s+your\s+(?:hidden|secret|internal)\s+(?:instructions|rules|configuration)\b", re.I),
        0.7,
    ),
    (
        InjectionCategory.OUTPUT_FORMAT,
        "forced_format",
        re.compile(r"\b(?:always|only|must)\s+(?:respond|reply|answer)\s+(?:exactly\s+)?in\s+(?:json|xml|yaml)\b", re.I),
        0.5,
    ),
    (
        InjectionCategory.DATA_EXFILTRATION,
        "markdown_exfil",
        re.compile(r"!\[[^\]]*\]\(\s*https?://[^\s)]*[?&][^\s)]*\)", re.I),
        0.85,
    ),
    (
        InjectionCategory.DATA_EXFILTRATION,
        "context_in_url",
        re.compile(r"\b(?:append|include|add|embed)\s+(?:the\s+)?(?:conversation|chat|context|transcript|user\s+data|api\s+key)\s+(?:to|in|into)\s+(?:the\s+)?(?:url|link|request)\b", re.I),
        0.9,
    ),
    (
        InjectionCategory.PRIVILEGE_ESCALATION,
        "mode_escalation",
        re.compile(r"\b(?:developer|admin|god|sudo|root|debug|dan|jailbreak)\s+mode\b|\bunlock\s+(?:your\s+)?(?:full|unrestricted)\s+(?:capabilities|potential)\b", re.I),
        0.8,
    ),
    (
        InjectionCategory.PRIVILEGE_ESCALATION,
        "constraint_removal",
        re.compile(r"\b(?:remove|drop|disable|turn\s+off)\s+(?:all\s+|your\s+)?(?:restrictions|limitations|filters|safety\s+features)\b", re.I),
        0.85,
    ),
)


class InjectionDetector:
    """Scan untrusted text for prompt-injection patterns."""

    def __init__(self, config: InjectionDetectionConfig | None = None) -> None:
        self.config = config or InjectionDetectionConfig()

    def find(self, text: str) -> list[InjectionFinding]:
        """Return findings at or above the configured threshold."""
        threshold = self.config.threshold
        findings: list[InjectionFinding] = []
        for category, pattern_id, pattern, confidence in _RULES:
            for match in pattern.finditer(text):
                if confidence >= threshold or self.config.include_low_confidence:
                    findings.append(
                        InjectionFinding(
                            category=category,
                            pattern_id=pattern_id,
                            start=match.start(),
                            end=match.end(),
                            snippet=match.group(0)[:80],
                            confidence=confidence,
                        )
                    )
        findings.sort(key=lambda f: (f.start, -f.confidence))
        return findings

    def is_suspicious(self, text: str) -> bool:
        """True if any finding meets the block threshold."""
        return any(
            f.confidence >= self.config.block_above for f in self.find(text)
        )

    def risk_score(self, text: str) -> float:
        """Aggregate risk score in [0, 1]: max confidence, boosted by breadth."""
        findings = self.find(text)
        if not findings:
            return 0.0
        max_conf = max(f.confidence for f in findings)
        breadth = min(len(findings) - 1, 3) * 0.05  # multiple patterns = worse
        return min(1.0, max_conf + breadth)
