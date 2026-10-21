# Third-party notices

This file inventories third-party material incorporated into this repository,
together with its license and provenance. Original repository content is
licensed as follows:

- Original **code** (`src/ai_safety_course/`, `tests/`, `scripts/`, project
  code under `projects/*/`, and configuration): MIT — see `LICENSE`.
- Original **instructional prose** (Markdown documents, templates, assessment
  material): CC BY 4.0 — see `LICENSE-DOCS`.

Datasets, model weights, and other external artifacts used by projects keep
their own terms; they are never relicensed here, and their provenance and
license are recorded in each project's data card and in the source register.

## Inventory

| Material | Location | Upstream | License | Notes |
|---|---|---|---|---|
| CC BY 4.0 legal code (the license text itself) | `LICENSE-DOCS` | https://creativecommons.org/licenses/by/4.0/legalcode | CC BY 4.0 | License text reproduced verbatim per its terms; the Creative Commons disclaimer paragraph is retained |
| (none other) | — | — | — | Entries are added at import time, in the same commit that introduces the material |

## Policy

1. Every import of third-party code, text, figures, or data must add a row to
   the inventory **in the same commit**, with upstream URL and verified
   license. "Verified" means the license statement was actually read at the
   recorded source, not assumed.
2. Never assume "publicly downloadable" means open source. Material without a
   locatable license is treated as all-rights-reserved and is not copied into
   the repository; it may only be linked, with access conditions noted.
3. Copied code is never relicensed; its notice is preserved and its license
   compatibility with MIT (for code) or CC BY 4.0 (for prose) is assessed
   before import.
4. License texts reproduced in this repository (such as `LICENSE-DOCS`) are
   themselves licensed material and remain listed here.
