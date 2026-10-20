"""Benchmark harnesses built on real, public datasets.

Each harness module:
- loads a registered real dataset (see src/aisafety/data/registry.py),
- runs a model-agnostic evaluation via a caller-supplied callable,
- emits a structured result record with provenance (dataset id, revision,
  split, date) per the repo's editorial standards.

Harnesses never fabricate numbers: without a model callable they run in
``smoke`` mode which validates plumbing only.
"""

from __future__ import annotations

__all__ = ["truthfulqa", "bold", "realtoxicityprompts", "advbench", "xstest"]
