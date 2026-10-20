"""aisafety: practical AI safety tooling for LLM applications.

The package is deliberately stdlib-first: the core safety filters (PII
detection/redaction, prompt-injection detection, toxicity hooks, guardrail
pipeline, evaluation metrics) run on the Python standard library alone so
they can be deployed in constrained environments (CI, serverless, edge).
Heavier dependencies (Hugging Face ``datasets``, remote moderation APIs)
are imported lazily where optional.

Module map
----------
- ``aisafety.config``       : runtime configuration objects
- ``aisafety.log``          : structured logging helpers
- ``aisafety.utils.text``   : shared text utilities
- ``aisafety.data``         : real-dataset registry + lazy loaders
- ``aisafety.safety.pii``   : PII detection and redaction
- ``aisafety.safety.injection`` : prompt-injection detection
- ``aisafety.safety.toxicity``  : toxicity classification hooks
- ``aisafety.safety.guardrails``: composable guardrail pipeline
- ``aisafety.evaluation``   : refusal / compliance / truthfulness metrics
"""

from __future__ import annotations

__version__ = "0.1.0"

__all__ = ["__version__"]
