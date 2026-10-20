#!/usr/bin/env python3
"""PII detection and redaction demo.

Runs the detector over realistic (synthetic) customer-service text — the
fixture text is synthetic on purpose: this repo never ships real
individuals' data (see SECURITY.md). Shows findings, counts, and the
redacted output with stable placeholders.

Run:  python examples/pii_redaction_demo.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.aisafety.safety.pii.detector import PIIDetector
from src.aisafety.safety.pii.redactor import PIIRedactor

SAMPLES = [
    (
        "Customer John Doe emailed support from j.doe42@example-mail.com "
        "about his order; call back at (415) 555-0132 x22."
    ),
    (
        "Payment failed for card 4242 4242 4242 4242; retry with the "
        "backup key sk-proj-4gH7zZ0aBcDeFgHiJkLmNoPqRsTuV."
    ),
    (
        "The audit log shows access from 203.0.113.42 and the employee "
        "record lists SSN 123-45-6789 for verification."
    ),
    (
        "No personal data in this one — just a question about refund timing."
    ),
]


def main() -> None:
    detector = PIIDetector()
    redactor = PIIRedactor(detector)

    for i, text in enumerate(SAMPLES, 1):
        print(f"--- sample {i} " + "-" * 50)
        print(f"input   : {text}")
        counts = detector.counts_by_type(text)
        print(f"findings: {counts or 'none'}")
        result = redactor.redact(text)
        print(f"redacted: {result.text}")
        print(f"removed {result.removed} item(s): {result.redacted_types}")
        print()


if __name__ == "__main__":
    main()
