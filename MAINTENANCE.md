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

## Session-2 standing instruments (2026-10-25)

- **Coverage widget**: `build_dashboard.py::_note_coverage` renders
  notes-per-chapter as bars; a zero bar is a regression. It caught
  the nine-chapter silent-skip bug in production — keep it.
- **Incidents timeline**: era-grouped from the incidents README
  table; a new incident needs its era row (the builder assigns by
  incident number — update `_incidents` when the eras grow).
- **Progress trackers**: `roadmaps/progress/*.md` are hand-written;
  the dashboard's counts parse checkbox density per milestone. A
  tracker edit does not need a dashboard change unless milestones
  are added or renamed.
- **Register growth**: every note/incident/dataset addition moves
  the counts the freshness test pins — run the full gate, not just
  the file you touched (the session's own lesson, twice).
- **Count-drift instrument**: `tests/test_count_drift.py` recomputes
  the corpus counts (registers, notebook directories, catalog,
  glossary table, test suite) and requires every count-bearing prose
  surface to carry them — README's structure table, FAQ's source
  count, START_HERE's build state, CITATION.cff's abstract, both
  notes front doors, AWESOME. When the corpus grows, this test
  fails on purpose until the prose catches up: update the surfaces
  in the same commit as the growth, and write counts in digits (a
  number spelled out in words evades the check). Dated records
  (STATUS, CHANGELOG, the judge audit) are deliberately exempt.
  On first run it caught the drift this whole sweep exists for: the
  suite grew with its own eight tests and README still said 594.
- **Register re-check rotations**: URL liveness is sampled, not
  continuous. Two rotations run so far (26 URLs total): rotation 1
  sampled the early session-2 entries, rotation 2 the late ones
  (accountability-era reports and the highest-numbered papers) and
  caught one genuinely dead URL (the ACLU analysis behind incident
  14 had moved sections — corrected in the register with the move
  recorded in its limitations). The discipline for each rotation:
  fetch server-side; a 403/401 from a known bot wall (EEOC,
  Reuters) is alive-but-blocked — confirm via search-result text
  before recording; a 404 is dead until a live replacement is
  located, confirmed, and the register entry corrected in the same
  commit. Next rotation: sample the middle register band
  (SRC-PAPER-100..140, the notes 51-66 spine) plus any entry whose
  limitations mention an unreachable page — re-attempt those first
  (G7's rule: a soft-null stays null only if still unreachable).
- **Rotation 3 (2026-10-25, the link layer)**: redirected from the
  planned middle-band sample by the owner's directive — every URL
  cited in AWESOME.md was fetched and identity-checked before the
  file's entries became clickable links. Scope: all 91 distinct IDs
  cited on that page, through the new standing instrument
  `scripts/verify_links.py` with three priced channels — the arXiv
  spine (51 IDs) title-matched against the arXiv API, the course
  video via YouTube's oEmbed endpoint, and the rest (39) via direct
  server-side GET with title/og:title extraction and a token-overlap
  identity check. Result: 91/91 live, zero dead, zero wrong pages.
  78 title-verified LIVE; 9 YouTube channel/playlist pages alive but
  JS-shelled to this client (identity anchored by the register's
  same-day page inspection and exact handle URLs); 4 bot-blocked
  (OWASP's LLM Top 10, the American Bar Association, ACM's CACM,
  openai.com — all real pages the register corroborates). Honest
  drifts recorded: 80000hours.org/ai now serves "mitigate" where the
  register's fetch read "reduce"; matsprogram.org's page title is
  "MATS Research"; the EU AI Act timeline page leads with
  "Implementation Timeline". The rotation also caught two mis-cited
  governance IDs in AWESOME.md — the RSP and OpenAI Preparedness
  lines pointed at the MCP-spec and Invariant-Labs register entries
  (SRC-REPORT-005/006) instead of SRC-REPORT-008/009 — corrected
  before linking; SRC-REPORT-009's canonical 404 (register-recorded)
  returned 403 to this client and stays deliberately unlinked; its
  url field was cleaned of an inline annotation (the 404 record
  lives in its limitations). Going forward every new link passes
  `verify_links.py --ids <ID>` before landing (AWESOME.md's
  how-to-extend rule 5), pinned by tests/test_awesome_links.py.
  Next rotation: the planned middle register band
  (SRC-PAPER-100..140) plus the full-register sweep --all as the
  link layer's first annual re-check.

### Re-check rotation 4 (2026-10-27) — the lecture-library opening

Ten new sources entered the register with the lecture library:
SRC-VIDEO-011..018 (the four course playlists and their channels)
and SRC-CURR-012..013 (the Harvard course pages, full-text-read;
the CAIS textbook site). All ten were run through
`verify_links.py --ids` before any AWESOME.md link landed: the
YouTube playlist and channel URLs returned live with no
title-extractable page (JS-rendered; the register's limitations
fields carry the API corroboration), the Harvard course page
returned LIVE with a domain match, and the CAIS textbook site
returned live. 10/10 live; zero dead; zero wrong pages. The
AWESOME.md intro's verified-count claim is recomputed from the
file's own ID set by the same sync that regenerated the dashboard.

### Re-check rotation 5 (2026-10-27) — the session-closing sweep

The closing rotation re-verified every URL cited on AWESOME.md
through the same priced channels (arXiv API title-match, YouTube
oEmbed/playlist, server-side GET). The count of unique register IDs
cited on the page is recomputed by the count-sync instrument from the
file itself; the intro's claim carries it. The full-register sweep
(`--all`) ran the same day — see rotation 5b's record if present;
any drift found is recorded here, not silently fixed.

**Rotation 5 run record (2026-10-27):** `exit 0`. Tail of the instrument's report:

```
97/97 live; 0 hard failures
```
