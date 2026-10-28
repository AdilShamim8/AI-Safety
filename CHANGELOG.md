# Changelog

All notable changes to this repository are documented here. The format
follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); this
project does not yet issue semver releases, so entries accumulate under
Unreleased until a tagged release exists.

## [Unreleased]

### The zoom that sliced the phone (2026-10-28)

- The owner reported the phone still broken after the s7 guard, with a
  DevTools screenshot (Pixel 9 Pro, 427px): the kicker and the giant
  serif title cut off at the right edge, text magnified ~2.3x. The
  deployed page was verified current first (live HTML byte-identical
  to origin/main); forcing the guard class with its frozen --vgz
  reproduced the screenshot exactly — the root cause was the guard's
  own zoom compensation, not a deployment gap.
- `zoom:var(--vgz)` shrinks the layout viewport to the screen while
  every guard rule was written for the oversized canvas, so the 520px
  body cap and the px paddings overflowed the shrunken viewport: the
  guard produced the very sliced page it existed to prevent, in both
  its true-positive path (desktop-mode phone) and its false-positive
  path (a late-applied emulated viewport, where the frozen first-run
  verdict could never un-wrong itself).
- The s8 guard removes the zoom and compensates with type: the head
  script publishes `--vfs` (clientWidth over screen.width, clamped
  1.05..3) and the derived layer scales every font-size through
  `calc(*var(--vfs,2.2))`. Font sizes cannot change clientWidth, so
  the verdict no longer freezes — it re-measures on every event plus
  an 800ms late re-check and self-corrects. The derivation now
  mirrors the whole cascade (the base tier's 114 font rules are
  scaled too), the guard tail caps nothing (the full canvas at
  scaled type is the phone column), long unbreakable tokens break
  anywhere, and `overflow-x:clip` is the final insurance.
- Verified across 15 device scenarios: the owner's exact DevTools
  case and a load-at-980-then-resize-to-427 self-correction pin both
  render the ordinary phone layout; six meta-ignored combinations
  (320-600px screens over 800-1280px canvases) render guard mode
  with body type at 16.0px physical and the maximum element
  right-edge exactly equal to the canvas; 768-1920px untouched.
  Suite 638 → 640, README resynced, dashboard regenerated at 640.

### The guard's blind spots and the physical scale (2026-10-28)

- The owner reported the phone still unreadable after the guard shipped.
  The deployed page was verified current (live HTML byte-identical to
  origin/main, Pages build at HEAD), so the gap was between what the
  guard did and what the owner's hand actually held. A live-page device
  audit — 13 scenarios with true isMobile emulation, a desktop-mode
  simulation (980px canvas, spoofed phone screen dimensions), and a
  physical-scale (DPR 0.4) screenshot read by VLM — found three defects.
- Detection stopped at screen.width <= 500, so 540/600px CSS-width
  budget Androids — everyday hardware — never got the guard at all: a
  meta-ignoring browser on those screens still showed the sliced
  desktop page with the card tables off. The gate now reaches 620; a
  real tablet still never passes, because with the meta honored its
  clientWidth equals its screen.width under the 640 bar.
- A meta-ignoring browser does not merely lay the page out at ~980px —
  it also scales that canvas down to the glass at ~0.4x, so even the
  guard's correct phone column read as ~6pt text (the VLM's verdict on
  the physical-scale screenshot: "unusable… requires constant
  pinch-to-zoom"). The head script now freezes --vgz (canvas width
  over screen width, clamped 1.2..3, computed once from pre-zoom
  geometry so the verdict can never oscillate through resize
  re-entry), and the derived layer gains
  `html.vw-guard{zoom:var(--vgz,1)}`: the phone column returns to true
  physical size — audited at 980/390 → zoom 2.5128, 800/412 → 1.9417,
  980/540 → 1.8148, every normal phone/tablet/desktop untouched at 1,
  and the VLM reads the compensated view as comfortably readable.
- The last leak: slash-joined vocabulary runs in chapter descriptions
  ("hazard/capability/propensity/exposure/severity") are one
  unbreakable word to the line breaker — at 320px the first chapter
  alone pushed the layout viewport 15px past the screen. The 640px
  phone layer now sets `overflow-wrap:anywhere` on the four long-text
  containers (chapter descriptions, claim text, evidence lines,
  annotations); the guard layer inherits the rule by derivation.
- Pinned three more ways in tests/test_responsive.py (18 → 21 tests);
  suite 635 → 638 (401 package + 174 from-scratch + 63
  repo-instrument); README resynced; dashboard regenerated at 638.

### The viewport guard (2026-10-28)

- The owner's second phone screenshot showed a state no media query
  could fix: the page laid out on a ~980px desktop canvas — kicker
  clipped mid-word, the masthead a wall of cropped letters, a sideways
  scrollbar. Reproduced and confirmed structurally: the browser was
  ignoring the viewport meta (a desktop-mode request or an in-app
  WebView), so every breakpoint fix was invisible in that environment.
- The phone layout is now also driven by a guard: a head script
  detects the mismatch itself (coarse pointer, physical screen no
  wider than 500px, clientWidth over 640) and marks html.vw-guard;
  build_dashboard.py mechanically re-scopes the template's own 960px
  and 640px blocks under that class on every build — derived, never
  hand-maintained — plus one rule capping the body to a 520px centered
  column inside the oversized canvas.
- Verified by four-environment simulation: a desktop-mode phone and an
  800px-layout WebView get the full phone layout (contents toggle,
  56px masthead, card tables, two-column facts, zero overflow); a real
  390px phone and a 1440px desktop are untouched. The simulation also
  caught a derivation bug before it shipped: a single-line media
  stray was swallowing the print rules into the guard layer.
- Pinned four ways in tests/test_responsive.py (14 → 18 tests),
  including a character-for-character parity test that rebuilds the
  guard layer from the template and demands it verbatim in the
  generated page. Suite 631 → 635 (401 package + 174 from-scratch +
  60 repo-instrument), README resynced.

### The phone table pass (2026-10-28)

- The owner's second read of the phone screen: the page *fit* 390px
  after session 5, but the register tables still didn't *read* —
  dataset names wrapped into jagged four-line fragments, fields
  broke mid-word, the sticky ID column spent prime width on
  "DS-002", and nothing said the table scrolled. Six units, each
  committed and pushed one at a time with its remote head verified.
- The registers now restack as labeled cards on phones
  (max-width:640px): every field cell carries a `data-label` the
  row builders stamp at render time, so a card names its own data;
  the columns the 960px layer had to hide (organization, type,
  fetched, strength, registered…) come back — a phone reads MORE
  of a register than a tablet does — and the horizontal scroller
  disappears from the phone layout entirely.
- Where tables stay columnar (measured 660px: the dataset table
  overflows 80px), a right-edge fade — toggled only while
  `scrollWidth` exceeds `clientWidth`, re-checked on resize and
  after every re-render through a MutationObserver — signals
  "more to the right" instead of reading as clipped.
- Chrome ergonomics: topbar action links lift from 11.5px baseline
  text to 35px-tall thumb targets, and the seven-item
  standing-facts line restacks from a ragged dot-separated run
  into a two-column grid.
- Pinned: tests/test_responsive.py grows 10 → 14 tests holding the
  card rules, the label stamps (template AND generated page), the
  affordance fade, and the chrome. Suite 627 → 631 (401 package +
  174 from-scratch + 56 repo-instrument), README resynced, the
  dashboard regenerated with its own counter at 631. Visual audit
  passes at all four widths with zero overflow; the card view was
  additionally verified by rendered-DOM measurement and screenshot
  review at 390px.

### The responsive site (2026-10-28)

- The owner's brief — better on a phone screen and a desktop screen —
  opened with a measurement: at a 390px viewport the dashboard carried
  303px of horizontal overflow. The cause was one line of rendering
  script: AWESOME id chips appended with no break opportunities, so a
  bold title plus four nowrap chips formed a single unbreakable run.
  Fixed first (S5-A01), then pinned so it cannot return.
- The phone layer (max-width:640px) arrived as seventeen one-concern
  units — frame breathing room, topbar compaction, thumb-sized TOC
  targets, masthead type, a wrappable organizing chain, compacted
  ledger and cards, stacked rungs and honesty rows, denser data
  tables with the ID column pinned inside their scrollers, full-width
  search, compact steps and schedules, tracker bars without label
  noise, compact FAQ/AWESOME/colophon, scaled headings, and iOS
  safe-areas with landscape handling.
- Desktop and accessibility landed as eleven more: keyboard focus
  visibility, a back-to-top control, a 1600px wide-screen frame, the
  topbar scroll state, contained table scrollers, coarse-pointer hit
  areas, the reduced-motion scroll gate (smooth scrolling had stayed
  on for everyone), text-size/tap-highlight ground rules, a skip
  link, print catch-up, and a sticky-header offset fix per
  breakpoint.
- Navigation became part of responsive reading: all 24 chapter READMEs
  carry a chapter-nav line and a closing next pointer, all 24
  solutions files carry their way back, and 20 hub pages carry
  navigate lines — 68 surfaces in all, every link resolving, pinned
  by tests/test_site_navigation.py.
- The contracts: tests/test_responsive.py (10 tests) pins the
  viewport, breakpoints, chip break-spaces, motion gating, focus
  visibility, scrollers, touch targets, and the two controls;
  ADR-0004 records the decision; scripts/visual_audit.py measures
  the generated page at four widths on demand.


### The final double-check sweep (2026-10-27)

- The owner's closing request — double-check everything, organize for
  beginners — earned eight one-at-a-time units (F-01..F-08), each
  pushed and remote-verified, plus a sixth full-register link
  rotation (261/261 live, zero state changes since the closing
  sweep). Four defects a beginner would have felt were found and
  fixed: the START_HERE step sequence read out of order (Step 0.5
  filed inside Step 1), the README's 60-second tour had step 5 ending
  mid-sentence with its tail welded into step 6, the FAQ still said
  "22 datasets" and "43 cards" against the catalog's real 47, and the
  courses index contradicted itself (build-in-progress language above
  a complete-library statement).
- The count-drift instrument learned both lessons: the FAQ is now
  pinned for dataset cards as well as sources (every mention must
  agree, not just one), and the README's suite-size parenthetical is
  pinned to the collected three-way split (the stale "32
  repo-instrument" was real 36, then 38 after the new pins). Suite
  611 → 613: 401 package + 174 from-scratch + 38 repo-instrument.
- The dashboard quickstart now opens with the 90-minute DeepMind
  primer START_HERE recommends before the diagnostic, so the two
  beginner surfaces tell the same story in the same order; a
  structural sweep (heading order, list sequences, empty-body
  heading doubles) now guards all 19 entry documents and found
  nothing further.

### The lecture library (2026-10-27)
- Mid-session checkpoint (102/200 units): the lecture library's core
  is complete and integrated — 4 course pages, 61 companion notes
  (18 Harvard, 16 DeepMind, 8 CAIS, 14 Safeshield, plus 5 pedagogy
  and study-plan pages), 10 register entries, the AWESOME
  full-courses track with rotation-4 link verification, the
  lecture-library structure test (suite 607 → 611), and all 24
  chapters' watching-companions blocks. CI green on every unit since
  the batch-linking fix (3-43); the committed-tree link check now
  runs before every push.

- **Fix-forward: the batch-linking CI defect (caught by CI, fixed in
  the driver).** Units 3-09 through 3-41 earned red CI runs in a
  characteristic pattern — every unit green at its batch's end, red in
  the middle. Cause: the note generators linked ALL of a course
  README's note rows upfront, while each unit commits only its own
  note file — so an intermediate commit's README pointed at note files
  that existed only in the working tree, and a fresh CI checkout
  (which sees the commit, not the working tree) failed
  `validate_repo.py`'s local-link check. The working-tree gate could
  not catch it by construction. Two fixes landed: note rows are now
  linked by the driver **per unit** (the commit that adds a note is
  the commit that links it), and the driver now runs a
  committed-tree link check after every commit and before every push
  — `git show HEAD:<file>` over the unit's files, resolving every
  local markdown link against the commit itself. The historical red
  runs stay in the Actions record as the honest trace; the tree at
  every batch boundary and at HEAD is green.

- Opened `courses/` — the video-course companions layer for the four
  courses the owner selected: Harvard CS 2881 (Boaz Barak), the Google
  DeepMind AGI Safety Course, the Center for AI Safety's AI Safety,
  Ethics & Society course, and Safeshield Training's AI Governance
  series. Each course now has a course page with its complete verified
  video index (57 videos across the four playlists, retrieved through
  YouTube's playlist API on 2026-10-27), its announced structure and
  guest lecturers, and a mapping table to the 24 chapters.
- Ten new register entries (SRC-VIDEO-011..018, SRC-CURR-012..013)
  document exactly what was verified and how: playlist structures via
  the API, the Harvard course pages read in full (both iterations,
  including every lecture's reading list and student experiment), the
  CAIS textbook site inspected. No video was watched and no spoken
  content is transcribed or quoted — the companion-note discipline is
  the same one the video library has held since it opened.
- `courses/how-courses-organize.md` records the cross-course pedagogy
  analysis the owner asked for: how each course gathers, organizes, and
  manages knowledge, and what this repository adopted from each
  architecture.
- The count-sync instrument is now wrap-tolerant: unit 3-02's sync left
  the README's line-wrapped status line saying 251 registered sources
  where the register held 254, `test_count_drift` caught it red in CI,
  and unit 3-03's fix-forward corrects both the count and the
  instrument (the `setnum` helper preserves the original line wrapping
  while updating the digits).

### The link layer (2026-10-25)

- `AWESOME.md` entries now carry their live links — 94 external
  markdown links (80 bold titles plus the prose mentions: the
  companion repository and video course, the control paper, the RSP,
  the three liability-era incidents, the AI Incident Database root).
  Every link was verified before landing, not assumed: the new
  standing instrument `scripts/verify_links.py` fetched all 91 URLs
  cited on the page through three priced channels (arXiv API title
  match for the 51-paper spine, YouTube oEmbed for the course video,
  server-side GET with title/og:title identity checks for the rest) —
  91/91 live, zero dead, zero wrong pages. The run is recorded as
  re-check rotation 3 in `MAINTENANCE.md`, with honest drifts noted
  (80000hours.org/ai now says "mitigate" where the register's fetch
  read "reduce"; matsprogram.org titles itself "MATS Research").
- Verification caught and fixed two mis-cited governance IDs: the
  Anthropic RSP and OpenAI Preparedness lines in AWESOME.md pointed
  at the MCP-spec and Invariant-Labs register entries
  (SRC-REPORT-005/006) instead of SRC-REPORT-008/009. The OpenAI
  Preparedness canonical URL (404 recorded in the register; 403 to
  datacenter clients at rotation) stays deliberately unlinked, and
  its register url field was cleaned of an inline annotation.
- The link discipline is now enforced, not just stated: rule 5 of
  AWESOME.md's how-to-extend section sends every new link through
  `verify_links.py --ids <ID>` first, and
  `tests/test_awesome_links.py` (4 tests, suite now 607) pins that
  every bold entry links to exactly its register URL, that no
  unregistered external link ships, and that the intro's
  verified-count claim matches the file's own ID set.
- `scripts/build_dashboard.py` renders AWESOME.md entry titles as
  anchors (the website's resource-map section is clickable to the
  live sources); `index.html` regenerated.

### Resource index expansion (2026-10-25)

- `AWESOME.md` reorganized into media layers for future growth: a new
  **video library** (four watching tracks — from-scratch and
  foundations, safety explainers, paper explainers and technical talk,
  frontier coverage and lab channels), a new **blogs and ongoing
  commentary** section (alignment theory, LLM security practice,
  post-training technical practice, strategy and measurement), a
  paper-spine bridge section, three new course/on-ramp entries, and a
  closing **how-to-extend** section stating the register-first
  admission discipline for future videos, channels, blogs, papers, and
  resources.
- 20 new register entries, every one opened at page level via
  search-engine renders on 2026-10-25 and priced with per-source
  limitations: 9 video channels (Rob Miles AI Safety, Andrej Karpathy,
  3Blue1Brown's neural-networks series, Yannic Kilcher, Machine
  Learning Street Talk, AI Explained, AI Coffee Break with Letitia,
  Anthropic's official channel, Computerphile's Rob Miles playlist),
  8 blogs (AI Alignment Forum, LessWrong, Simon Willison's
  prompt-injection series, Interconnects, Lil'Log, Cold Takes, Epoch
  AI, Redwood Research), and 3 resources (AI Safety Camp,
  AISafety.info/Stampy, Neel Nanda's interpretability getting-started
  guide). No spoken video content is quoted anywhere; perishable
  counts (subscribers, posts) carry fetch dates.
- Register now 251 sources / 206 claims; README (two places), FAQ
  (one place), and the dashboard/website counts regenerated to match.

### Final verification pass (2026-10-25)

- Full-corpus external re-verification: all 142 arXiv-URL sources
  resolve to the exact papers the register claims (title-level API
  comparison, zero mismatches); all 43 dataset cards correspond to
  real, publicly reachable datasets — 155 reference URLs checked
  (200/redirect/restricted-only); independently confirmed size facts
  for TruthfulQA (817 validation rows), GSM8K (7,473/1,319 in both
  configurations), MMLU (14,042/1,531/285/99,842), and HarmBench's
  authorship record (12 authors, Mazeika first, v2 2024-02-27).
- **Correction of this changelog's own record:** the Session 1 entry
  below claims "the corrupted `branches: ain]` trigger fixed." A
  hex-level audit of every historical version of
  `.github/workflows/ci.yml` (66b8574, 795f34e, 6f3f910, HEAD) shows
  the file has read `branches: [main]` since creation — the
  "corruption" was a terminal-display artifact that strips the `[m`
  escape prefix, making `[main]` render as `ain]`. The workflow was
  never broken and no fix was applied at 6f3f910 (its diff adds only
  the audit step). The earlier claim stands corrected; commit
  messages are immutable and are annotated here instead.
- `datasets/catalog.yaml` reference hygiene: DS-011's R3 and DS-022's
  R3 `url` fields carried prose contamination ("(fetched and parsed
  2026-10-23)" and "+ datasets-server size API" inside the URL
  values); both cleaned to bare URLs, DS-011's gaining the `/blob/main`
  path segment (verified HTTP 200).
- Two honestly-open license gaps closed by observation (HF API,
  fetched 2026-10-25, each with a new R2 reference): DS-024
  Do-Not-Answer is apache-2.0 on the live LibrAI/do-not-answer
  hosting — the earlier-recorded librarian-bots/do-not-answer id now
  returns HTTP 401 and the catalog's `hf_id` is corrected accordingly;
  DS-025 PKU-SafeRLHF is cc-by-nc-4.0 (non-commercial). Both cards'
  headers and honest-limitation sections updated to match.

### Session 3 - the website (2026-10-25)

- `index.html` redesigned from a dark widget dashboard into the full
  editorial website the repository's front door deserves: seventeen
  section-numbered surfaces on warm paper with ink typography and one
  oxblood accent, a sticky table of contents with scrollspy, a drop-cap
  masthead with the generated standing-facts line, the evidence ladder
  with real access-level counts, the honesty ledger, the complete
  SYLLABUS course catalog grouped by route with a route filter, all ten
  projects with their honest headlines, the full notebook index (search
  + method-level filter), the fourteen-incident four-era timeline,
  searchable dataset/source/claims/glossary explorers, the careers layer
  with route sequences and progress trackers, the quickstart with the
  three schedules, the FAQ, the AWESOME resource map with register-ID
  chips, and a colophon.
- `scripts/build_dashboard.py` gains eight extraction surfaces, all
  parsed from the repository's own documents (SYLLABUS, GLOSSARY, FAQ,
  AWESOME, study schedules, notes index, chapter directories, access
  counts); `tests/test_dashboard.py`'s payload contract is unchanged and
  still green.
- AWESOME.md count drift caught and corrected ("22 verified cards" vs
  the 43-card catalog); `tests/test_count_drift.py` now pins the
  corrected phrase.

### Session 2 — the judged deepening (opened 2026-10-25)

- `planning/SESSION2_JUDGE_AUDIT.md` — the LLM-as-judge pass over the whole
  build: seven gaps (G1–G7), each with named collection points, and the
  150-commit backlog in judged priority order. STATUS opened the session.
- The note corpus doubled and doubled again: 42 paper notes (33–74) added
  behind arXiv-API verification — the load-bearing spine from Concrete
  Problems and Othello-GPT through the oversight family (CIRL, the
  off-switch game, power-seeking, reward tampering), the memorization
  family (Secret Sharer, training-data extraction, the memorization
  laws), the instrument family (Llama Guard, activation probes, ROME,
  CheckList, Dynabench, HELM, inverse scaling), the defense family
  (randomized smoothing, TRADES), the scale family (double descent,
  scaling laws, TDC2023), and the adversarial quartet (FGSM, universal
  perturbations, HotFlip, ensemble training). Five draft arXiv IDs were
  caught wrong by API title checks before a single one was cited.
- Six comparison notes C07–C12, each settling a practitioner decision a
  single paper leaves open: the factuality instrument pair (FActScore vs
  SelfCheckGPT), the one-bit jailbreak diagnostic and its two defense
  families, budgeting drift vs gating value, the response-posture
  hierarchy extracted from eleven incidents, the two drifts
  instrumented separately, and supply strategies vs the blind spot.
- 21 dataset cards (23–43) at honest abstract-read levels with licenses
  pending-where-uninspected: the safety-evaluation dozen (StrongREJECT,
  Do-Not-Answer, PKU-SafeRLHF, AgentHarm, InjecAgent, BIPIA, FigStep,
  AgentDojo, CounterFact/ROME, RobustBench) and the bias/agent/multimodal
  dozen (HateXplain, DynaHate, StereoSet, ANLI, WebArena, GAIA, Civil
  Comments, LMSYS-Chat-1M, MM-SafetyBench, FEVER, TrojAI).
- 11 incident reviews (04–14), each page-inspect-gated: the
  rollout-and-channel era (AI Overviews, NYC MyCity, Cursor, Slack
  exfiltration, Samsung pastes), the history era (Bing prompt
  disclosure, Tay, Sydney), and the accountability era (Galactica, the
  EEOC's first AI-bias settlement, Amazon's scrapped recruiter).
  Registers SRC-REPORT-017..041.
- The owner's explicit ask, delivered: four career-route progress
  trackers under `roadmaps/progress/` (117 artifact checkboxes across 25
  milestones, every box naming its evidence), plus the dashboard
  progress widget, incidents timeline, and notes-coverage bars — the
  coverage widget caught a real nine-chapter sweep bug in production.
- The deepening wired into the spine: chapter cross-links for every new
  note and incident, project companions for P01–P10, the from-scratch
  track's literature anchors, first-90-days wired to the trackers, and
  GLOSSARY growth to 296 terms.
- The closing surface: the count-drift sweep (seven hand-written surfaces
  had survived six phases of growth with stale numbers — README's
  structure table, FAQ, START_HERE, CITATION.cff, both notes front
  doors, AWESOME), the count-drift instrument (`tests/test_count_drift.py`)
  pinning every count-bearing surface to the registers it describes,
  CITATION.cff's first real `version:`/`date-released:` keys with the
  refreshed abstract, and two G7 re-check rotations over 26 sampled
  register URLs — one genuinely dead ACLU URL caught, corrected, and
  recorded in the entry's limitations.
- **The session closed at its 300-commit target** (300/300, every commit
  pushed individually and remote-verified; 603-test suite green at close;
  231 sources / 206 claims / 74 paper notes + 12 comparisons + 14 incident
  reviews / 43 dataset cards / 296 glossary terms). Final state recorded
  in `planning/STATUS.md`; the owner's standing action on session end is
  to rotate the exposed push token.
- **Fixed (the closure's fix-forward)**: a black-formatting violation in
  `scripts/build_dashboard.py` that had kept CI red for 95 consecutive
  runs (246–340) — introduced by the dashboard-widget commits of the
  deepening stretch and never caught locally because the session's local
  gate script ran ruff, pytest, the validator, and the audit but omitted
  `black --check`, while CI ran black on src/scripts/tests. The file is
  formatted, the local gate now mirrors CI exactly, and the lesson is
  the session's own rule restated: a gate that does not match the
  checker of record is not a gate.
### Added (2026-10-25 — the milestone build: incidents, notes, learner surface)

- Three production incident reviews (`research/notes/incidents/`):
  Moffatt v. Air Canada 2024 BCCRT 149 (the generation channel is not
  a source of record; "nobody checked" reads as negligence), the DPD
  post-update regression (same-channel instructions are not a
  boundary; behavior-changing releases need behavioral gates), and
  the Chevrolet of Watsonville commitment-authority incident (a
  public LLM channel with commitment authority and no boundary will
  be tested by the public). All strict-template: facts first,
  unknowns kept unknown, what-this-does-NOT-demonstrate sections.
  Sources SRC-REPORT-013..016 (page-inspected, honest limitations).
- Twelve paper notes (21–32: CaMeL, AgentDojo, Sandbagging,
  Explore-Establish-Exploit, DPO, InstructGPT, Debate, Sycophancy,
  Mirage, Constitutional AI, GCG, Verbalized confidence) + comparison
  C06 (safety cases vs red-team reports) — the notebook grows to
  32 + 6, every note ending in a falsifiable extension runnable at
  course scale.
- The learner surface: `prerequisites/verifying-sources.md` (the
  field guide with the five-minute drill), `roadmaps/audit-only.md`
  (the reviewer's route), `roadmaps/first-90-days.md` (week-by-week
  plans per role, artifact-gated), `FAQ.md`, `MAINTENANCE.md` (the
  operating manual), and `AWESOME.md` (the annotated resource index —
  the README's promised-but-unbuilt item, delivered).
- GLOSSARY +18 terms; chapter cross-links (ch.04/05/06/07/13/15/20/22
  gain note and incident companions); README/START_HERE/SYLLABUS/
  ROADMAP honest-state corrections and the dashboard as front door;
  CITATION.cff and THIRD_PARTY_NOTICES updated for the completed
  scope and the new quoted material.
- CI hardened: the corrupted `branches: ain]` trigger fixed, the
  missing-values audit as a CI step, the dashboard freshness test
  (committed payload vs fresh build, field-by-field), the PR-template
  audit/regeneration checkboxes, and the AGENTS.md resume protocol
  carrying the session's own two push-then-fail lessons.

### Added (2026-10-25 — the dashboard website and the careers layer)

- `index.html` + `scripts/build_dashboard.py` +
  `scripts/dashboard_template.html`: the whole course as one
  self-contained verified website — nine widget sections (build
  numbers, the judge's evidence ladder, chapter map, project cards,
  dataset/source/claims explorers with live filters, the three career
  tracks with the progress ladder, the beginner quickstart). Generated
  from the repository's own registers; zero external dependencies;
  6 generator tests pin the contract.
- `scripts/audit_missing.py`: the repo-wide missing-values audit as a
  permanent instrument (six checks; first run caught three stale
  content-matrix paths; runs in CI with 4 regression tests).
- `roadmaps/careers-index.md`: the three role families mapped to the
  live job market — dated demand signal with per-claim provenance
  (553+900 open roles, SANS four-titles-hiring-today, MATS terms and
  self-reported outcomes, employer-disclosed salary ranges), entry
  mechanisms per role, and the five-rung artifact-based progress
  ladder. Registers +4 sources (SRC-CURR-005..008, page-inspected) and
  +4 claims (CLM-0164..0167) with counterevidence.
- README/START_HERE: stale status lines corrected (the README still
  said 0/24 chapters); the dashboard is now the front door.

### Added (2026-10-25 — P10 capstone: agent evaluation and assurance dossier)

- `src/ai_safety_course/assurance/`: the course's integrating artifact —
  P07's guard + Ch. 08 monitor/audit-budget + step budget as one bounded
  agent, three-arm paired comparison over a held-out nine-trial set,
  Ch. 22 claim/evidence/caveat grammar, per-scenario trace logs,
  fail-closed checksums, and the preregistered verdict the numbers
  dictate: NOT DEPLOYABLE at the pinned configuration (attacks 3/5
  stopped; benign completion 1/4 [0.046, 0.699] against the 50% floor),
  with improvement actions quantified per failed benign. 11 pinned
  tests; genuine example dossier committed.

### Added (2026-10-25 — P06 causal interpretability study)

- `src/ai_safety_course/patch_audit/`: the causal-interpretability
  discipline of Ch. 09–11 as a deterministic two-branch model organism —
  shortcut-learning readout pinned (w_b 2.661 > w_a 2.247), linear
  probes that favor the spurious site (0.915 vs 0.825), an
  activation-patching grid under two topic-matched contrasts with
  Wilson intervals, exact binomial tests and Holm correction, the
  trivial-band pinning (s0/s3 restore everything; ends of flow
  localize nothing), random-patch and matched-magnitude controls, and
  the deployment-flip intervention that rejects the vendor-shaped
  claim (flip-slice 0.335 -> b-ablated 0.770, McNemar 102 vs 15,
  p = 2.2e-17) with the in-distribution two-sided ledger priced
  (0.915 vs 0.805). 14 pinned tests; compute tier honestly marked
  not-executed.

### Added (2026-10-23 — P08 control protocol; the build's 100th commit)

- `src/ai_safety_course/control_protocol/`: the Ch. 08 frontier as
  code — paired three-protocol comparison (no-monitor /
  simple-monitor / defer-to-trusted) with identical seeded flagging,
  showing the monitor's recall as the safety ceiling and defer
  buying usefulness back at the audit budget's price (61 trusted
  executions, ~23% of throughput). 6 pinned tests.

### Added (2026-10-23 — P05 weak-to-strong analogue)

- `src/ai_safety_course/w2s_audit/`: the scalable-oversight
  question as a minimal deterministic analogue — a 30%-flip weak
  supervisor, a strong learner trained only on its labels, and the
  invariant ground-truth boundary. Weak-to-strong effect
  demonstrated: +0.255 oversight gap recovered with disjoint
  intervals, persisting under covariate shift. Small-analogue scope
  statement carried in the README. 7 pinned tests.

### Added (2026-10-23 — P09 shift/subgroup reliability)

- `src/ai_safety_course/shift_audit/`: Chapter 17's audit as code —
  group-structured synthetic deployment with a spurious flip under
  shift; ID vs OOD with disjoint intervals; worst-group vs average;
  ECE degradation; and the DRO-lite half-recipe mitigation failing
  honestly (the GroupDRO coupling caveat reproduced deterministically).
  6 pinned tests.

### Added (2026-10-23 — P04 preference optimization audit)

- `src/ai_safety_course/pref_audit/`: Chapter 04's audit as code —
  BT/DPO machinery (numerically checked), logistic reward model on a
  noisy feature, the closed-form KL-constrained optimum, and three
  instruments: proxy-vs-held-out divergence, the concentrated
  20% label-bias condition (held-out drift −0.0645 while the proxy
  stays silent), and SFT-vs-preference. 8 pinned deterministic
  tests; synthetic-corpus tier honesty documented.

### Added (2026-10-23 — chapter 24; all 24 chapters complete)

- `chapters/24-research-practice-and-capstone-execution/`: the
  methodology assembled into the capstone — falsifiable scoping,
  baselines that can win, preregistration, the benchmark-lottery
  arithmetic (flip probabilities computed per comparison), the
  ablation grid as inward-facing safety case, negative results
  written to be useful, and the ethical-release review. The worked
  example is the P10 proposal in miniature with all arithmetic
  shown.
- Registers +3 (SRC-PAPER-105..107); claims +3 (CLM-0161..0163);
  GLOSSARY +6 terms. Chapter spine: 24/24.

### Added (2026-10-23 — chapter 23)

- `chapters/23-governance-and-standards/`: instruments sorted by
  what they are — guidance (NIST AI RMF 1.0, voluntary, revision
  named), obligation (EU AI Act with in-force/pending arithmetic),
  knowledge bases (ATLAS with pinned counts), community lists
  (OWASP), self-commitments (RSP/Preparedness). The standards map
  with versions, the cited-vs-actual column, and the four-question
  citation-forensics protocol. Not-legal-advice boundary enforced.
- Registers +3 (SRC-REPORT-010..012; NIST four functions at
  JS-rendering honesty); claims +3 (CLM-0158..0160); GLOSSARY +5.

### Added (2026-10-23 — chapter 22)

- `chapters/22-safety-engineering-and-assurance/`: the safety case
  as an argument built to be attacked — hazard-derived decomposition,
  evidence with confidence ratings, named defeaters with rebuttals
  or acceptances, the ISCaP-style linking argument, quantified-or-
  stated residual risk, and re-audit triggers. The Meridian worked
  example cites the course's own committed results as evidence.
- Registers +5 (SRC-PAPER-100..104, incl. the one-day-old CoT
  monitoring roadmap at maximum-recency honesty); claims +5
  (CLM-0153..0157); GLOSSARY +6 terms.

### Added (2026-10-23 — chapter 21)

- `chapters/21-sociotechnical-and-systemic-risk/`: the system around
  the model — overreliance measurement (complementarity gap, AI-error
  catch rate), the normative step before any fairness metric, the
  fairness impossibility landscape with the trade-off statement it
  forces, 50 years of testing-history context, and coverage mapped as
  exclusion. Ceres loan-screening worked example with every rate
  recomputed.
- Registers +4 (SRC-PAPER-096..099); claims +4 (CLM-0149..0152);
  GLOSSARY +6 terms.

### Added (2026-10-23 — chapter 20)

- `chapters/20-misuse-dangerous-capabilities-release-evaluation/`:
  the release gate as a pre-registered causal claim — uplift studies
  with paired statistics, the elicitation ladder with lower-bound
  grammar, the metric-mirage check, safety-level frameworks read as
  auditable claim structures, and the Prometheus worked example with
  a measured/assumed/waived release memo. Non-operational scope
  enforced throughout.
- Registers +5 (SRC-PAPER-093..095; SRC-REPORT-008 RSP
  page-inspected; SRC-REPORT-009 Preparedness with 404-honesty);
  claims +5 (CLM-0144..0148); GLOSSARY +5 terms.

### Added (2026-10-23 — chapter 19)

- `chapters/19-multimodal-and-embodied-safety/`: the modality change
  as a safety-case change — five verified failure stations (typographic
  jailbreaks with the visual-embedding attribution, query-relevant
  image compromise, universal visual jailbreak, BadRobot's embodied
  vulnerabilities, the survey's pipeline fragilities), the Vantage
  five-instrument audit with exact recomputed statistics, and the
  sim-to-real honesty limit.
- Registers +5 (SRC-PAPER-088..092); claims +5 (CLM-0139..0143);
  GLOSSARY +6 terms.

### Added (2026-10-23 — chapter 18)

- `chapters/18-reasoning-faithfulness-and-monitorability/`: the CoT
  as a monitored channel — five verified failure stations (unfaithful
  explanations, partial/inverse-scaling faithfulness, obfuscation
  under optimization, oversight-conditional amplification, CoT
  controllability for evasion), the Meridian four-instrument audit
  with exact recomputed statistics, the monitorability tax, and the
  oversight flip as a paired measurement.
- Registers +5 (SRC-PAPER-083..087: Turpin, Lanham, Baker, Jaworski,
  Dolev — the two 2026-10 papers carried at explicit high-recency
  honesty); claims +5 (CLM-0134..0138); GLOSSARY +6 terms.

### Added (2026-10-23 — dataset queue completion round)

- Final four pending datasets verified and promoted to cards (catalog
  DS-019..DS-022): CrowS-Pairs, Winogender, MMLU, GSM8K. The
  pending-verification queue is now empty.
- Honest discrepancy records: GSM8K's abstract 8.5K vs released
  8,792 (7,473+1,319); CrowS-Pairs license authority is the README
  statement (no LICENSE file in the repo).
- Registers +8 (SRC-PAPER-079..082, SRC-DATASET-021..024); claims +8
  (CLM-0126..0133). Catalog: 18 -> 22 datasets.

### Added (2026-10-23 — pending-dataset verification round)

- Five datasets promoted from the metadata-only pending queue to full
  cards (catalog DS-014..DS-018): OR-Bench, WildJailbreak, WMDP,
  HaluEval, SimpleQA. Each card carries the verification trail
  (abstract-read papers, HF API page inspections, direct README/CSV
  reads) with honest gaps.
- SimpleQA's canonical CSV parsed directly: 4,326 questions with the
  full topic distribution (sum-checked); the 4,333 naive line count
  explained as a multi-line-quoted-field artifact.
- Registers +10 (SRC-PAPER-074..078, SRC-DATASET-016..020); claims +10
  (CLM-0116..0125). Catalog: 13 -> 18 datasets.

### Added (2026-10-23 — dataset license and composition verification round)

- Six license gaps closed by direct canonical LICENSE reads: ToxiGen (MIT
  text, Microsoft copyright, TOXIGEN header; GitHub NOASSERTION nuance
  recorded), BBQ (CC-BY-4.0), HarmBench (MIT), SafetyBench (MIT), AdvBench
  (MIT, llm-attacks canonical), JailbreakBench (MIT, repo-level
  confirmation). Register: SRC-REPO-002..007.
- HarmBench behavior-set composition verified by direct CSV read: 400 text
  behaviors (200 standard / 100 copyright / 100 contextual; test 320, val
  80; multimodal 110) with the semantic-category distribution — closes the
  "behavior-set size NOT verified" marker.
- Datasets catalog, six cards, index table, and pending-verification queue
  updated; all arithmetic cross-checked (41+159=200, 20+80=100, 19+81=100).

### Added (2026-10-23 — pending-paper verification round)

- Source register +4: SRC-PAPER-070 (PPO, abstract-read), SRC-PAPER-071
  (HH-RLHF, abstract-read), SRC-PAPER-072 (BeaverTails, abstract-read),
  SRC-PAPER-073 (TruthfulQA, abstract-read). Claims +4: CLM-0112..0115.
- Chapters 02/04/06 readings: every "assigned, verification pending"
  paper marker closed with the actual abstract-page fetch; WILDS's
  stale pending line corrected to the already-verified SRC-PAPER-067.
- The InstructGPT register limitation note about PPO-pending closed.

### Added (2026-10-22 — AI Researcher From Scratch track)

- `research/ai-researcher-from-scratch/`: the owner-directed 7-module
  track distilling the video "Become AI Researcher From Scratch - Full
  Course" (Vuk Rosic, 2025, CC-BY, page-inspected — SRC-VIDEO-001) and
  its MIT-licensed companion repository zero-to-ai-researcher
  (SRC-REPO-001, full-text-read) into notes plus stdlib-only code.
- `src/ai_safety_course/from_scratch/`: six code modules (tensors,
  activations, neuron, network, attention, transformer, moe) with 174
  tests — every backward pass finite-difference-checked; a TinyGPT
  trains on next-token prediction and regenerates its training string
  (deterministic, pinned in CI).
- `research/ai-researcher-from-scratch/07-research-methodology.md`:
  three preregistered protocol templates (ablation, hyperparameter
  search, architecture-configuration search) mapping the companion's
  research methodology onto the course's own evaluation discipline.
- Registers: SRC-VIDEO-001, SRC-REPO-001; claims CLM-0071..0073 (the
  paper's findings priced at abstract strength). GLOSSARY +10 terms;
  THIRD_PARTY_NOTICES +2 entries.


### Added (2026-10-21 — fresh start)

The repository was reset to its initial commit and rebuilt from the project
brief dated 2026-10-20 (research baseline 2026-10-20; build execution began
2026-10-21). Everything below is part of that rebuild.

- Research provenance layer: `research/research-method.md` (search scope,
  verification standards, honest limitations), `research/reference-article-map.md`
  (owner's article mapped to modules with a truthful access record — full
  text fetched 2026-10-21, conclusion not retrieved, article treated as
  inspiration not validation), `research/source-register.yaml` (5 entries
  verified by live fetch), `research/claims-register.yaml` (5 claims with
  counterevidence).
- Planning layer: `planning/BUILD_PLAN.md` (definition of done per artifact,
  phase gates), `planning/STATUS.md` (durable progress record; truthful
  counters), `planning/content-matrix.yaml` (24 chapters + 10 projects
  inventoried, all honestly `planned`), `planning/dependency-map.md`
  (curriculum prerequisites + tooling tiers), ADRs 0001 (architecture and
  licensing) and 0002 (uv, Python 3.12, optional dependency groups).
- Governance layer: MIT `LICENSE` for code, CC BY 4.0 `LICENSE-DOCS` for
  prose, `THIRD_PARTY_NOTICES.md` (inventory + import policy),
  `CITATION.cff` (no invented DOI or affiliation), `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md` (verifiable GitHub contact route; no invented email),
  `SECURITY.md` (verified: private vulnerability reporting disabled at
  2026-10-21; documented alternative route; repository-vulnerability vs
  model-behavior reports distinguished), `RESPONSIBLE_RESEARCH.md`.
- `AGENTS.md`: binding operating contract for agent sessions (auth via
  environment secret, one coherent commit at a time, honesty rules, untrusted
  data handling, resume protocol).
- Eight content templates (`templates/`): chapter, paper-note,
  experiment-report, threat-model, dataset-card, safety-case,
  research-proposal, incident-review — each with embedded quality rules
  (mandatory failure-mode sections, denominators, no hand-typed tables,
  strict incident taxonomy).
- Learner entry layer: `START_HERE.md`, `ROADMAP.md` (three schedules with
  honest arithmetic), `SYLLABUS.md` (24-unit catalog),
  `prerequisites/diagnostic.md` (five tasks with worked answers and skip
  guidance), `prerequisites/targeted-refreshers.md` (R1–R6),
  `roadmaps/` (three specialization pages + study schedules with
  adaptation rules).
- Engineering baseline: `pyproject.toml` + committed `uv.lock` (uv workflow,
  Python 3.12 floor, exact dev-tool pins verified against PyPI 2026-10-21),
  `.python-version`, in-repository pre-commit validator
  `scripts/validate_repo.py` with 7 regression tests, real CI workflow
  (actions pinned to verified commit SHAs), bug-report and content-error
  issue templates, pull-request template with the honesty checklist.

### Removed (2026-10-21)

- All prior agent-generated content and history after the owner's initial
  commit, per owner instruction (force-reset of `main` to the initial commit;
  issue tracker and Actions artifacts cleaned correspondingly).

### Notes

- No curriculum chapters or projects are complete yet; see
  `planning/STATUS.md` for the live, truthful state.

- Message-hygiene record: commit `ebd1407` says "P02" in its title but
  its content is P03's companion line (an interrupted loop crossed
  streams mid-commit). P01 and P02's own lines landed correctly in the
  two commits prior. Recorded rather than force-pushed — history stays
  append-only; messages get caught by honesty.

### Session 3 closed — the lecture library complete (2026-10-27)

Two hundred units, one commit and one push at a time, each pushed
and remote-verified individually: the four-course companion layer
(4 course pages, 61 notes, 5 pedagogy/study-plan pages, 4
self-assessments, 3 framework crosswalks, 3 cross-course
comparisons, 2 exercise walkthroughs, 4 reading maps, 1 honesty
ledger), 10 register entries with live-verified URLs (rotation 4),
4 verified real-world dataset cards (GDPval, RE-Bench, METR
time-horizons, Canaries — catalog at 47), 14 new glossary terms
(325 total), watching companions in all 24 chapter READMEs and
watching pointers in all 24 solutions files, progress-ladder
checkpoints on all four routes, the AWESOME full-courses track,
the lecture-library structure test (suite 607 → 611), ADR-0003,
and the session's own protocol lessons in AGENTS.md. The count
instrument was hardened three times in public (units 3-03, 3-131
through 3-134): line-wrapped numbers, internally-wrapped phrases,
and phrase variants — each caught red by the drift tests before CI,
each fixed forward, each recorded. The token rule held: credentials
only ever transient; the owner rotates the exposed token after
this session.

- Closed at 200/200, plus the closure's earned fix-forward (the session-2 precedent): the 200th unit's STATUS row is filled by the commit AFTER it — the trailing-SHA pattern necessarily leaves the final row to its successor — and the session's record is append-only and complete.
