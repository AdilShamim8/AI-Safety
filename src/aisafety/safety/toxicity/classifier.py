"""Toxicity classification with two interchangeable backends.

1. ``lexicon`` — offline heuristic scoring built from the insult/profanity
   term lists used in the toxic-comment literature (Jigsaw/Civil Comments
   lineage). Deterministic, dependency-free, and deliberately *not*
   presented as a replacement for production classifiers: it approximates
   a Perspective-API-style TOXICITY score for CI and offline triage.
2. ``perspective`` — Google Jigsaw's Perspective API (the same scoring
   system behind the RealToxicityPrompts dataset, arXiv:2009.11462).
   Requires ``PERSPECTIVE_API_KEY``; remote calls only happen in this
   backend.

Production deployments should prefer classifier models such as Llama
Guard (arXiv:2312.06674) or the OpenAI Moderation API; both wrap behind
this same interface easily.
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from typing import Any

from ..config import ToxicityConfig
from ..utils.text import clamp01


@dataclass(frozen=True)
class ToxicityResult:
    score: float                     # aggregate toxicity in [0, 1]
    backend: str
    matched_terms: list[str] = field(default_factory=list)
    attributes: dict[str, float] = field(default_factory=dict)
    detail: dict[str, Any] = field(default_factory=dict)


# Compact lexicon seeded from public toxic-comment word lists
# (Jigsaw Kaggle competitions; profanity lists in the ToxiGen/
# RealToxicityPrompts lineage). Terms are lowercase; multiword terms
# match with flexible whitespace.
_LEXICON: tuple[str, ...] = (
    "idiot", "stupid", "moron", "imbecile", "scum", "vermin", "retard",
    "bastard", "bitch", "asshole", "dumbass", "scumbag", "turd",
    "pathetic", "worthless", "trash", "garbage", "disgusting",
    "reprehensible", "despicable", "subhuman", "degenerate",
    "kill yourself", "go die", "drop dead", "hate you",
    "you people", "those people", "your kind",
    "shut up", "loser", "clown", "moronic", "braindead",
)


class ToxicityClassifier:
    """Score text toxicity via the configured backend."""

    def __init__(self, config: ToxicityConfig | None = None) -> None:
        self.config = config or ToxicityConfig()

    # ------------------------------------------------------------------ lexicon
    def _lexicon_score(self, text: str) -> ToxicityResult:
        lowered = text.lower()
        matched: list[str] = []
        for term in _LEXICON:
            pattern = r"\b" + re.escape(term) + r"\b"
            if re.search(pattern, lowered):
                matched.append(term)
        # crude severity weighting: distinct terms + intensifiers + slur-adjacent
        base = min(0.25 * len(matched), 0.9)
        if re.search(r"\b(f+u+c+k+|s+h+i+t+)\b", lowered):
            base = max(base, 0.4)
            matched.append("profanity")
        if re.search(r"\ball\s+(?:of\s+)?(?:you|them)\b", lowered) and matched:
            base = min(base + 0.1, 1.0)  # targeting a group worsens it
        score = clamp01(base)
        return ToxicityResult(
            score=score,
            backend="lexicon",
            matched_terms=sorted(set(matched)),
            attributes={"TOXICITY": score},
            detail={"note": "offline heuristic; calibrate before relying on it"},
        )

    # -------------------------------------------------------------- perspective
    def _perspective_score(self, text: str) -> ToxicityResult:
        api_key = os.environ.get("PERSPECTIVE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "PERSPECTIVE_API_KEY is not set; use backend='lexicon' for offline use"
            )
        try:
            import requests  # lazy import; optional dependency
        except ImportError as err:  # pragma: no cover
            raise RuntimeError("the 'requests' package is required") from err
        url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
        payload = {
            "comment": {"text": text},
            "languages": ["en"],
            "requestedAttributes": {
                attr: {} for attr in self.config.perspective_attributes
            },
        }
        response = requests.post(
            url, params={"key": api_key}, json=payload, timeout=10
        )
        response.raise_for_status()
        data = response.json()
        attributes = {
            name: clamp01(v["summaryScore"]["value"])
            for name, v in data.get("attributeScores", {}).items()
        }
        aggregate = max(attributes.values(), default=0.0)
        return ToxicityResult(
            score=aggregate,
            backend="perspective",
            attributes=attributes,
            detail={"api": "commentanalyzer.googleapis.com"},
        )

    # -------------------------------------------------------------------- api
    def score(self, text: str) -> ToxicityResult:
        """Score a single text with the configured backend."""
        if self.config.backend == "off":
            return ToxicityResult(score=0.0, backend="off")
        if self.config.backend == "perspective":
            return self._perspective_score(text)
        return self._lexicon_score(text)

    def is_toxic(self, text: str) -> bool:
        """True if the aggregate score exceeds the configured threshold."""
        return self.score(text).score >= self.config.threshold
