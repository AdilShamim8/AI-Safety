# ADR-0001: Repository architecture and licensing

- **Status:** accepted
- **Date:** 2026-10-21
- **Deciders:** repository build agent (on instruction of the repository owner)

## Context

The repository starts from the owner's initial commit containing a one-line
README on GitHub (`AdilShamim8/AI-Safety`). The project brief (2026-10-20)
specifies a Markdown-first, GitHub-native repository that must function as a
curriculum, a course, a research notebook, an experiment collection, an
annotated index, and a maintained open-source project. Licensing defaults are
specified by the brief: MIT for original code, CC BY 4.0 for original
instructional prose, with third-party content keeping its own terms.

## Decision

1. **Markdown-first, GitHub-native.** All instructional content is plain
   Markdown in the directory structure defined by the brief (chapters/,
   projects/, notes/, prerequisites/, roadmaps/, research/, assessment/,
   templates/, planning/, plus root-level entry documents). No documentation
   site, custom frontend, or styling work until the repository is complete and
   only if it adds value. No badges unless they represent a real workflow or
   fact.
2. **File coverage map for licenses.** `LICENSE` (MIT) covers original code:
   `src/ai_safety_course/`, `tests/`, `scripts/`, project code under
   `projects/*/`, and configuration. `LICENSE-DOCS` (CC BY 4.0) covers original
   instructional prose: `*.md` files, templates, and assessment material.
   `THIRD_PARTY_NOTICES.md` records third-party content and its terms. Dataset
   and model artifacts keep their upstream terms and are documented per-use in
   data cards, never relicensed.
3. **One default branch (`main`) with direct verified commits.** The owner's
   instruction for this build is sequential verified commits to `main`.
   Task branches and a reviewable PR are permitted when the workflow needs
   them; merges require separate authorization.
4. **English** is the repository language, matching the brief and the audience
   definition (experienced ML/security engineers and aspiring technical AI
   safety researchers).
5. **No prefilling.** Directories and files appear only with their real content
   as each unit is implemented; navigation links point only at existing files.
   The content matrix carries `planned` entries so the roadmap can describe the
   future without dead links pretending it exists.

## Consequences

- GitHub renders everything without tooling; reviewers can diff prose.
- The license split requires diligence: every imported snippet must be checked
  into THIRD_PARTY_NOTICES.md at import time, not "later".
- A later documentation site would be additive, not structural.
- Direct-to-main commits trade PR review for velocity; compensating controls
  are the per-commit validator, the same-commit status updates, and honest
  maturity labels in the content matrix.
