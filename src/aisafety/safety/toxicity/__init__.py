"""Toxicity classification hooks (lexicon offline or Perspective API)."""

from __future__ import annotations

from .classifier import ToxicityResult, ToxicityClassifier

__all__ = ["ToxicityResult", "ToxicityClassifier"]
