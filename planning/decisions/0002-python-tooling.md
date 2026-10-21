# ADR-0002: Python dependency workflow (uv, Python 3.12)

- **Status:** accepted
- **Date:** 2026-10-21
- **Deciders:** repository build agent (on instruction of the repository owner)

## Context

The brief requires: choose **one** Python dependency workflow; select a
currently supported Python version; pin a tested environment; verify imports
and a tiny forward pass before writing tool-specific code; keep model
downloads and GPU runs out of PR CI; use optional groups or separate
environments for incompatible research tools so no project forces a large
shared stack on every other project.

Environment verified on 2026-10-21: Python 3.12.15 and uv 0.13.0 available in
the build environment; pytest and PyYAML importable.

## Decision

1. **uv as the single dependency workflow**: `pyproject.toml` (PEP 621,
   setuptools-free via uv's build backend or hatchling — finalized when the
   first package code lands in Phase C) plus a **committed `uv.lock`** for
   reproducible installs. One workflow, no parallel requirements.txt drift.
2. **Python 3.12 as the minimum/floor** (tested on 3.12.15). The floor is
   recorded in `pyproject.toml` `requires-python`; CI runs one supported
   interpreter version rather than a matrix, because the brief prioritizes a
   tested, pinned environment over breadth.
3. **Dependency groups**:
   - `core`: pytest, PyYAML — the always-installable tier that every project's
     CPU smoke mode runs on.
   - `ml` (optional): torch, transformers, datasets — only for local-model
     projects (P03, P04, P06, and model paths of P01/P08).
   - `interp` (optional): TransformerLens/SAELens stack — only for P06.
   - `dev`: ruff, black, mypy pins — exact versions pinned for deterministic
     checks (lesson recorded from the prior build: unpinned linters drift).
4. **CPU smoke mode is a release requirement**, not a convenience: every
   project's smoke path must run on the `core` group alone.
5. **Import verification rule**: no code is committed against a tool API that
   was not imported and exercised in the build environment at the recorded
   version. Tool versions tested are stated in the project README.

## Consequences

- Contributors need uv (single well-supported tool; documented install
  command) instead of juggling pip/venv/requirements files.
- The lockfile is committed and updated in deliberate dependency commits.
- Optional groups keep the default install light (no torch download for
  prose-only learners).
- Pinning lint/format tools exactly trades update latency for determinism;
  updates happen as explicit dependency commits with the diff reviewed.
