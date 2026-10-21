"""ai_safety_course — shared tooling for the AI-Safety course repository.

This package holds the course's reproducible evaluation harnesses and
utilities. It is deliberately stdlib-first: the base dependency set is
pytest + PyYAML only (ADR-0002 in the repository's planning notes), and
every module is deterministic and offline so the full suite runs on a
fresh CPU-only environment.

Subpackages:
    evaluation: the P01 evaluation harness (cases, adapters, metrics,
        runner, report, scorer) implementing the Chapter 02 discipline
        of preregistered, denominator-explicit, interval-honest reporting.

Licensing: original course code, MIT (see the repository LICENSE file).
"""

__version__ = "0.1.0"

__all__ = ["evaluation", "__version__"]
