"""Safety filters: PII, prompt injection, toxicity, and guardrails.

The subpackage layout mirrors the risk pages in docs/risks/ so code and
documentation cross-reference cleanly:

- ``pii/``        -> docs/risks/privacy.md (OWASP LLM06)
- ``injection/``  -> docs/risks/prompt_injection.md (OWASP LLM01)
- ``toxicity/``   -> docs/risks/bias_fairness.md, misuse.md
- ``guardrails/`` -> composes the above into one pipeline
"""

from __future__ import annotations

__all__ = ["pii", "injection", "toxicity", "guardrails"]
