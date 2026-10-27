# Contributing to AI Safety

Thank you for considering a contribution. This repository has unusual
obligations because it teaches safety engineering: contributions are held to
the honesty standards the course itself teaches. Please read this page before
opening an issue or PR.

## The three rules that matter most

1. **No unsupported claims.** Every substantive technical statement should
   trace to a source in `research/source-register.yaml` or be labeled as the
   author's reasoning. If you add a claim, add or cite a register entry; if
   you cannot verify it, say so in the text.
2. **No status inflation.** Maturity values in `planning/content-matrix.yaml`
   and report statuses (`protocol-only`, `implemented`, `smoke-tested`,
   `experiment-executed`) must match reality on disk. A half-written chapter
   is `drafting`, never `complete`.
3. **No dead links, no prefilling.** Navigation links point only at files
   that exist. New directories appear with real content, not placeholders.

## Development environment

The repository uses uv with a committed lockfile (ADR-0002):

```bash
# install uv: https://docs.astral.sh/uv/
uv sync --frozen           # core + dev tiers, exactly as locked
uv sync --group ml         # + model-project tier (group lands with P03/P04/P06)
uv run pytest              # run the test suite
uv run python scripts/validate_repo.py .   # YAML schema + local-link + size checks
```

Python 3.12 is the floor. Model-dependent extras are optional; every project
must keep a CPU smoke mode that runs on the core tier.

## What to check before every commit

- `python scripts/validate_repo.py .` passes (register schemas, internal
  links, no oversize artifacts).
- `python scripts/audit_missing.py` reports **0 hard findings** (register
  schemas, claims cross-references, unit paths, card license/verification
  statements, SRC-*/CLM-* existence across all prose).
- If you changed anything the dashboard displays (registers, catalog,
  matrix, incidents, notes): `python scripts/build_dashboard.py` was run
  and the regenerated `index.html` is in your commit. The page is
  generated output — hand-edits will fail CI's freshness test.
- The operating manual for all of this is [`MAINTENANCE.md`](MAINTENANCE.md)
  (the five commands, the change-X→must-also-do-Y table, how to add a
  source the honest way).
- Tests that cover the code you touched pass; the full suite if you touched
  shared code.
- Markdown renders sensibly (headings in hierarchy, tables well-formed).
- You have not committed: model weights, raw datasets, credentials, caches,
  or unreviewed raw logs. The `.gitignore` helps; the responsibility is yours.
- If you cite a new source: add the `research/source-register.yaml` entry
  with the **actual** access level you achieved, and the actual access date.
  A paper you read in full is `full-text-read`; one whose abstract you skimmed
  is `abstract-read`. Overstating access levels is the fastest way to get a
  PR rejected.

## Commit conventions

One coherent purpose per commit, Conventional-Commits-style prefixes
(`research:`, `docs:`, `feat:`, `fix:`, `test:`, `ci:`, `planning:`), with a
body explaining the defensible purpose. Update
`planning/STATUS.md`/`planning/content-matrix.yaml` in the same commit as the
unit they describe.

## Reporting problems

- **Bugs in repository code or content:** open an issue; include the command
  you ran, the expected vs. actual output, and your environment.
- **Factual/citation errors:** open an issue with the correction and the
  source that supports it. Corrections are fixed in visible commits; the
  register's `limitations` field records issues found in cited sources.
- **Security issues:** see `SECURITY.md` — do not open public issues for them.
- **Conduct problems:** see `CODE_OF_CONDUCT.md`.

## Licensing of contributions

By contributing, you agree that your original code contributions are licensed
under the repository's MIT license and your original prose contributions
under CC BY 4.0, and that third-party material you incorporate is properly
declared in `THIRD_PARTY_NOTICES.md` (see the policy there). If you cannot
agree to those terms, do not contribute; propose the change as an issue
instead and it can be reimplemented.

## Review expectations

Maintainers review for: technical accuracy, honest status reporting,
citation validity, licensing, and test coverage. Expect requests for evidence
rather than opinions — that is the course's culture applied to itself.

## Adding a course or lecture note to the lecture library

The `courses/` layer follows the repository's evidence discipline with
its own shape:

1. **Register before you link.** Every playlist, channel, and course
   page gets a source-register entry (13-field schema) with an honest
   access level: `page-inspected` for playlist structure verified via
   the API, `full-text-read` for course pages read end-to-end,
   `metadata-only` for channels identified from ownership. Run
   `scripts/verify_links.py --ids <NEW-IDS>` before any link lands in
   AWESOME.md, and record the run in MAINTENANCE.md.
2. **Notes are original companions, never transcripts.** No spoken
   content is transcribed or quoted. A note anchors to what is
   verifiable: the lecture's announced title and topic, the course
   page's published readings and experiment descriptions, and the
   literature this repository already registers (cite the SRC ID
   where one exists).
3. **One note, one commit, one row link.** The commit that adds a
   note links its table row in the course README in the same commit —
   never before (the committed tree must not carry dead links; the
   driver's committed-tree check enforces this).
4. **Honest in-progress states.** A note that does not exist yet is
   a plain backticked filename in the table; it becomes a link when
   it lands. Counters on pinned surfaces (README, CITATION,
   AWESOME's intro) are recomputed by the sync instrument — run the
   drift tests before pushing.
