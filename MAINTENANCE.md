# MAINTENANCE — keeping the course true

The operating manual for the repository's living parts: what to
regenerate when something changes, which checks must stay green, and
how to add information without breaking the verification chain. If you
are a first-time contributor, read this top to bottom once; every
command is one line and every check is fast.

## The five commands that matter

```bash
uv sync                                          # 1. install (pytest + PyYAML + dev pins)
uv run pytest                                    # 2. the full deterministic suite must pass
uv run python scripts/validate_repo.py           # 3. yaml schemas, local links, file sizes
uv run python scripts/audit_missing.py           # 4. the missing-values audit (0 hard findings)
uv run python scripts/build_dashboard.py         # 5. regenerate index.html after any data change
```

All five run in CI on every push. A commit whose fifth command was not
run is a commit whose dashboard lies — the page is generated, never
hand-maintained.

## What to do when you change X

| You changed | You must also |
|---|---|
| `research/source-register.yaml` | run the audit (4) and regenerate (5); the dashboard's evidence ladder counts update |
| `research/claims-register.yaml` | same — and every claim you cite in prose must keep its CLM-id |
| `datasets/catalog.yaml` or a card | the audit checks card/license/verification statements; regenerate (5) |
| `planning/content-matrix.yaml` (a unit's status) | regenerate (5) — the chapter map and project cards read from it |
| `chapters/`, `projects/`, `roadmaps/` prose | the validator (3) catches broken local links; new SRC-*/CLM-* mentions are audit-checked for existence |
| `tests/` or `src/` | `uv run ruff check . && uv run black .` then the suite (2) — the same quality gate every commit here passed |
| anything the dashboard shows | **regenerate (5) and commit the updated `index.html` in the same commit** |

## How to add a source (the honest way)

1. **Fetch it yourself.** Actually open the arXiv abstract page / the
   canonical repo / the license file. Do not register from memory or
   from someone else's citation.
2. **Decide the access level**: full-text-read, abstract-read,
   page-inspected, metadata-only, or unavailable (a failed fetch is a
   registrable fact — record it).
3. **Append to `research/source-register.yaml`** with all fourteen
   fields: id, title, authors_or_organization, url, source_type,
   publication_date (verified or null — never inferred from a URL),
   version, accessed_on (today), access_level, evidence_class,
   peer_review_status, supports, limitations, license. Copy an entry
   near yours for the house style.
4. **Register the claim, not the vibe**: if prose will cite a number
   from it, add the claim to `research/claims-register.yaml` with the
   five parts (statement with date and n, source id, evidence
   strength, assumptions, counterevidence).
5. Run the audit (4). It will catch a missing field, a bad access
   level, or a claim pointing at a nonexistent source before CI does.

The learner-facing version of this discipline — with worked examples
and the five-minute drill — is
[prerequisites/verifying-sources.md](prerequisites/verifying-sources.md).

## How to add an incident review

Follow `templates/incident-review.md` strictly: production incident /
controlled demonstration / tabletop / hypothetical, stated up front;
observable facts first; established conclusions attributed; unknowns
kept unknown; the "what this does NOT demonstrate" section is
mandatory. Register the sources first (fetch the tribunal ruling, the
first-party postmortem, or the best press you can actually reach — and
say which it is). Add the row to
`research/notes/incidents/README.md` — the dashboard's incident cards
parse that table. See the three existing notes for the house style.

## The registers' invariants (what the audit enforces)

- **Every source has all fourteen fields** and an access level from
  the five-value vocabulary.
- **Every claim references an existing source** and carries its own
  counterevidence field (even if "none observed this session").
- **Every content-matrix unit** that is complete has a verification
  date, and its path exists on disk.
- **Every dataset card** states a license (as observed, with where)
  and a verification date.
- **Every SRC-*/CLM-* id mentioned in any prose file exists in the
  registers** — across all 134+ markdown files, machine-checked.

## The dashboard's data contract

`scripts/build_dashboard.py` reads: the two registers, the dataset
catalog, the content matrix, the incident index table, the
from-scratch track directory, the note files, the test count (via
`pytest --collect-only`), and the commit count (shallow-clone aware —
CI checkouts have no history and the generator says so honestly). If
you add a widget's data, extend `build_data()`; if you change the
page, edit `scripts/dashboard_template.html` — `index.html` itself is
generated output, committed so the page is always browsable at the
repo root and on GitHub Pages without a build step.

## CI

`.github/workflows/` runs the quality gates on every push to `main`,
pinned to verified action SHAs (ADR-0002 discipline). A red check is
a finding, never an inconvenience: recent example — the dashboard
commit-count test failed on CI because GitHub's shallow clone has no
history; the fix made the generator honest about shallow clones
instead of making the test weaker. Keep that order of operations.
