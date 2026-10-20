"""Tests for PII detection and redaction (synthetic fixtures only)."""

from __future__ import annotations

from src.aisafety.safety.pii.detector import PIIType, PIIDetector
from src.aisafety.safety.pii.redactor import PIIRedactor

# 4532 1488 0343 6467 is a standard Luhn-valid *test* card number pattern
# used in payment-testing documentation; fixtures are synthetic.
VALID_CARD = "4532 1488 0343 6467"


class TestDetector:
    def test_email(self):
        findings = PIIDetector().find("contact alice.smith@example.org now")
        assert any(f.pii_type == PIIType.EMAIL for f in findings)

    def test_credit_card_luhn(self):
        findings = PIIDetector().find(f"card {VALID_CARD} charged")
        cards = [f for f in findings if f.pii_type == PIIType.CREDIT_CARD]
        assert cards and cards[0].confidence == 1.0

    def test_credit_card_invalid_luhn_low_confidence(self):
        findings = PIIDetector().find("card 1234 5678 9012 3456 charged")
        cards = [f for f in findings if f.pii_type == PIIType.CREDIT_CARD]
        if cards:  # matched by pattern but failed checksum
            assert cards[0].confidence < 0.5

    def test_ssn(self):
        findings = PIIDetector().find("ssn 123-45-6789 on file")
        assert any(f.pii_type == PIIType.SSN for f in findings)

    def test_openai_style_key(self):
        findings = PIIDetector().find("key sk-abcdefghij0123456789abcd present")
        assert any(f.pii_type == PIIType.API_KEY for f in findings)

    def test_github_token(self):
        findings = PIIDetector().find("token ghp_" + "A" * 36 + " leaked")
        assert any(f.pii_type == PIIType.API_KEY for f in findings)

    def test_ipv4(self):
        findings = PIIDetector().find("login from 192.168.1.44 detected")
        assert any(f.pii_type == PIIType.IP_ADDRESS for f in findings)

    def test_clean_text_no_findings(self):
        assert PIIDetector().find("just a normal sentence about refunds") == []

    def test_mask(self):
        findings = PIIDetector().find("email me at bob@example.com please")
        email = next(f for f in findings if f.pii_type == PIIType.EMAIL)
        assert "@" not in email.masked
        assert email.masked.startswith("bo")


class TestRedactor:
    def test_redact_preserves_placeholders(self):
        redactor = PIIRedactor()
        result = redactor.redact(
            "from bob@example.com call 415-555-0132 about card "
            + VALID_CARD
        )
        assert "bob@example.com" not in result.text
        assert "415-555-0132" not in result.text
        assert "[EMAIL_1]" in result.text
        assert result.removed >= 2

    def test_redact_generic_tokens(self):
        result = PIIRedactor().redact(
            "bob@example.com", preserve_format=False
        )
        assert result.text == "[REDACTED:EMAIL]"

    def test_clean_text_untouched(self):
        result = PIIRedactor().redact("nothing to redact here")
        assert result.text == "nothing to redact here"
        assert result.removed == 0

    def test_counts_by_type(self):
        counts = PIIDetector().counts_by_type(
            "a@x.com and b@y.net both wrote"
        )
        assert counts.get("email") == 2
