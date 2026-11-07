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

### Re-check rotation 5 (2026-11-03) — the DataCamp companion opening

The fifth course's two register URLs were verified before linking:
SRC-CURR-014 (public catalog page) resolved LIVE with the title
corroborating the register entry; SRC-CURR-015 (the course URL)
resolved as the expected sign-in redirect (302) — recorded in the
entry's limitations as the account-wall, not as a failure. The
catalog-page fetch carried the chapter and lesson structure that
CLM-0207..0212 pin — those ids were renumbered to CLM-0224..0229 in S13-P07 after a collision audit found the course block duplicated paper claims; the record stands, the ids moved.

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

### Re-check rotation 5b (2026-10-27) — the full-register sweep

`verify_links.py --all` over every register entry (261 sources at
run time — a dated snapshot: the register has since grown to 264 with
the DataCamp and CampusX courses; the figure records what the sweep
covered that day, not the current total). The arXiv spine title-matched
through the API; YouTube
entries through oEmbed; the rest through server-side GET with title
checks. Bot-blocked hosts (the standing three plus any new) are
reported live-not-dead with register corroboration; the one
expected-dead URL (OpenAI Preparedness canonical 404) passes on its
recorded death. Results recorded below at run time.

**Run record:** exit 0; report tail: `261/261 live; 0 hard failures`.

### Re-check rotation 6 (2026-10-27) — the final double-check sweep

The user's closing request ("double-check everything") earned a sixth
full-register pass after the beginner-organization fixes landed:
`verify_links.py --all` over all 261 sources (that day's snapshot — see rotation 5b's note), exit 0. The YouTube
channel pages (SRC-VIDEO-013..018) report LIVE-NO-TITLE as in every
rotation — JS-rendered pages the register corroborates at page level;
the standing bot-blocked hosts behave identically to rotation 5b; the
one expected-dead URL passes on its recorded death. No register URL
changed state between the session-closing sweep and this one.

**Run record:** exit 0; report tail: `261/261 live; 0 hard failures`.

### The responsive duty (2026-10-28)

The dashboard's phone and desktop behavior is now instrumented twice.
The machine contract is tests/test_responsive.py — it runs in CI with
the suite and pins the viewport meta, both breakpoints, the chip
break-spaces, the reduced-motion gate, focus visibility, the named
table scrollers, the coarse-pointer block, and the two controls
against the template, which remains the only hand-edited surface.
The human instrument is scripts/visual_audit.py — playwright-based,
optional-dependency, run on demand before and after any template
change: it loads the generated page at 360/390/1440/1920 and fails
on horizontal overflow, naming the widest unclipped element. The
standing rule is unchanged in spirit: a template change regenerates
index.html in the same commit (the freshness test enforces it), and
now also answers the audit before it lands.

### The worked-example layer (2026-11-03)

The 44 worked examples were applied note by note through the idempotent applier; their content lives in three modules beside the generator, so the layer regenerates deterministically. No external URL was added by the extension; the register basis is unchanged from rotation 5.

### Re-check rotation 6 (2026-11-03) — the CampusX opening

SRC-CURR-016's URL was verified before linking: the course page
resolved LIVE to the platform's rendered page (title corroborating
the register entry), and the preview URL resolved LIVE to the same
outline in a second session. The curriculum data supplied the 14
lessons with durations that CLM-0213..0218 pin (renumbered CLM-0230..0235 in S13-P07, same collision fix); the platform's own
TENTATIVE marking on the outline is carried in the register entry's
limitations.

### The CampusX worked-example layer (2026-11-03)

The 14 practitioner walk-throughs were applied note by note through the idempotent applier (scripts/apply_campusx_example.py); their content lives in three modules beside the generator, so the layer regenerates deterministically. No external URL was added; the register basis is unchanged from rotation 6.

### The build-block layer (2026-11-03)

The fourteen chapter build blocks and the two project blocks were written directly into the chapter and project READMEs (the watching-companions rows carry the pairings; the build blocks carry the relationship in prose). No generated artifact is involved; the register basis is unchanged.

### Session 13 (2026-11-04) — the bug-hunt session: 32 units, commits 851 through 877

The user's final-check report ("still bugs you did not fix") was taken
as a re-diagnosis mandate, not a defense. Full re-audit across CI, the
five local gates, the live page (console, interactions, anchors, dead
links), and an axe pass found: the live page's two real defects were
color-contrast (ink-3 at 2.8-3.3:1, 15 nodes) and heading-order (three
h2→h4 skips because the group level was a styled div). Both fixed in
P01; axe now reports zero violations.

The deeper findings were data errors no prior session had a test for:
ch05's false-rejection mass stated 10.45% (true 10.44); twelve course
claims issued duplicate ids (CLM-0207..0218, colliding with paper
claims) renumbered to CLM-0224..0235; chapter 02's exercises numbered
in chapter 01's namespace; four dataset cards missing the honest-
boundary section; SRC-PAPER-034's access_level field contradicting its
own prose; SYLLABUS's projects column three cells stale; ROADMAP's
route diagram missing P02; comparison-01's header still saying "1 of
5 planned" with twelve on disk; and five stale count surfaces (FS
track 174→176, p02 157→150, p03 98→87, p01 quickstart 78→876+, the
content-matrix's 20/20-era notes section).

Thirty units landed: P01 a11y, P02-P03 the solutions-math layers (74
parametrized recomputations), P04 doc-count resync, P05 syllabus,
P06 the glossary-ref grammar, P07 register-id uniqueness, P08 register
supports-closure, P09 exercise alignment, P10 dataset cards, P11
notes-closure, P12 the courses layer, P13 roadmaps arithmetic, P14
the FS track, P15 the project-count surfaces, P16 built-page a11y
structure, P17 planning matrix, P18 the chapter sweep, P19 AWESOME,
P20 roadmap diagram, P21 z-convention agreement, P22 meta closures,
P23 incidents, P24 comparisons, P25 ledger, P26 catalog, P27 the glossary columns pin, P28 FAQ, P29 course claims, P30 banner. Suite 832 to 922; every
P30 banner. Suite 832→922; every
count surface now recomputed from disk/collection on each CI run.

P31 addressed the CI root cause: CI had been red since P17 — the planning-
layer test verifies STATUS rows against git objects, but the workflow
cloned shallow (fetch-depth 1), so every pre-P17 sha failed cat-file
on the runner while passing locally on full history. The checkout now
fetches depth 0; the STATUS rows for all 31 units were appended in the
same commit, and this record's own numbers were corrected (it first
shipped saying 903→925 from a build line never re-checked).

P32 closed the session: P31's workflow edit shipped unparsable YAML —
the checkout step's rationale carried ': ' inside a two-line name, so
the run failed with zero jobs and no logs to debug. The fix moved the
rationale to a comment and the file now round-trips a YAML parser
locally before every push. With CI green on both workflows, the
session's STATUS rows are pinned to real shas for all thirty-two
units — every row verified by the planning test, no placeholder left
in the table.
### Session 14 (2026-11-06) — the interview-preparation and selection layers: 46 units, commits 879 through 924
Opened on the user's finding: the corpus had no interview-preparation
layer and no curated security/safety selections. This session adds an
interviews/ layer grounded only in registered, real-world data (WEF,
ISC2, BLS, Stack Overflow, levels.fyi, OWASP, NIST, EU AI Act, lab
safety frameworks), a selections/ layer, a beginner-first README, and
keeps every surface recomputed from disk. STATUS rows now land one
commit after their unit with the real sha — no placeholder, ever.
Closed with the user's final-verification pass. Delivered: the interviews
layer complete (market, roles, question banks, take-homes — 24 content
pages + 5 indexes, every figure from registered real-world sources with
access levels stated), the selections layer complete (security, safety,
interview, beginner + index), sources 264->275 and claims 218->238
(CLM-0236..0255) with README/CITATION/FAQ surfaces synced and index.html
rebuilt in the same commit as every register change.

The check failures the user flagged were root-caused, not papered over:
the cancelled pages deploy was a push race (a newer push landing mid-
deploy), fixed by making the unit driver wait after every push until
that commit's own CI and pages checks complete green; the final pass
then caught the same hole in the driver's retry path (a superseded
pages failure on eec1a04 slipped through) and closed it — a retry now
waits like the normal path. The live site was verified to serve the
current build (claims 238). One cut background run (P44/P45) was
recovered through the driver's retry path with the recovery recorded
in the commit message.

Honest remaining map (future sessions, not gaps in what shipped):
dashboard rendering for the two new layers, integrity tests for them,
the beginner README rewrite, and selections cross-links from
START_HERE. Recorded in download/session-14-delivery-record.md with
entry points; nothing was padded to reach a number.
