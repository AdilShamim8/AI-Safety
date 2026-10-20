"""Tests for the toxicity classifier (offline lexicon backend)."""

from __future__ import annotations

import pytest

from src.aisafety.config import ToxicityConfig
from src.aisafety.safety.toxicity.classifier import ToxicityClassifier


class TestLexiconBackend:
    def test_benign_text_low_score(self):
        result = ToxicityClassifier().score(
            "The meeting is at 3pm; please bring the quarterly report."
        )
        assert result.score < 0.3
        assert result.backend == "lexicon"

    def test_insulting_text_scores_high(self):
        result = ToxicityClassifier().score(
            "You are a worthless idiot and everyone despises you."
        )
        assert result.score >= 0.5
        assert result.matched_terms

    def test_group_targeting_boosts(self):
        classifier = ToxicityClassifier()
        base = classifier.score("you people are disgusting").score
        assert base >= 0.5

    def test_threshold_flagging(self):
        config = ToxicityConfig(threshold=0.5)
        classifier = ToxicityClassifier(config)
        assert classifier.is_toxic("you pathetic moron") is True
        assert classifier.is_toxic("have a lovely day") is False

    def test_off_backend_always_zero(self):
        classifier = ToxicityClassifier(ToxicityConfig(backend="off"))
        result = classifier.score("you worthless idiot")
        assert result.score == 0.0
        assert result.backend == "off"

    def test_result_attributes_populated(self):
        result = ToxicityClassifier().score("you are pathetic trash")
        assert "TOXICITY" in result.attributes


class TestPerspectiveBackend:
    def test_missing_key_raises(self):
        import os

        classifier = ToxicityClassifier(ToxicityConfig(backend="perspective"))
        saved = os.environ.pop("PERSPECTIVE_API_KEY", None)
        try:
            with pytest.raises(RuntimeError):
                classifier.score("anything")
        finally:
            if saved is not None:
                os.environ["PERSPECTIVE_API_KEY"] = saved
