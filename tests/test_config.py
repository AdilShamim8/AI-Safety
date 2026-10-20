"""Tests for configuration dataclasses."""

from __future__ import annotations

from dataclasses import replace

from src.aisafety.config import (
    EvalConfig,
    GuardrailConfig,
    InjectionDetectionConfig,
    PIIRedactionConfig,
    ToxicityConfig,
    to_dict,
)


class TestDefaults:
    def test_guardrail_defaults_fail_closed(self):
        config = GuardrailConfig()
        assert config.fail_closed is True
        assert config.redact_inputs and config.filter_outputs

    def test_pii_defaults_enable_all_detectors(self):
        cfg = PIIRedactionConfig()
        assert all([
            cfg.detect_email, cfg.detect_phone, cfg.detect_credit_card,
            cfg.detect_ssn, cfg.detect_ip, cfg.detect_api_keys,
        ])
        assert cfg.mode == "redact"

    def test_injection_thresholds_ordered(self):
        cfg = InjectionDetectionConfig()
        assert 0 < cfg.threshold <= cfg.block_above <= 1

    def test_toxicity_default_offline(self):
        assert ToxicityConfig().backend == "lexicon"

    def test_eval_config_seed_and_output(self):
        cfg = EvalConfig()
        assert cfg.seed == 42
        assert cfg.output_dir == "results/"


class TestImmutability:
    def test_frozen(self):
        import pytest

        with pytest.raises(Exception):
            GuardrailConfig().fail_closed = False  # type: ignore[misc]

    def test_replace_creates_new(self):
        base = GuardrailConfig()
        tweaked = replace(base, fail_closed=False)
        assert tweaked.fail_closed is False
        assert base.fail_closed is True


class TestSerialization:
    def test_to_dict_nested(self):
        payload = to_dict(GuardrailConfig())
        assert payload["pii"]["mode"] == "redact"
        assert payload["injection"]["threshold"] == 0.5
        assert payload["toxicity"]["backend"] == "lexicon"
