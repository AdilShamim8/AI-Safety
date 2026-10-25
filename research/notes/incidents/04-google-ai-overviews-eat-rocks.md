# Incident review: Google AI Overviews — "eat rocks," glue pizza, and the popularity-truth collapse

Class: **production incident** · Date of event: 2024-05 (rollout of AI
Overviews to hundreds of millions of users; viral screenshots late
2024-05-23/24; Google's response statements through 2024-05-30) · Date
of this note: 2026-10-25
Sources: SRC-REPORT-017 (The Verge, 2024-05-24, page-inspected via
search-result content 2026-10-25), SRC-REPORT-018 (BBC News, 2024-05-24,
page-inspected via search-result content 2026-10-25), SRC-REPORT-019
(The Conversation, 2024-05-27, full page content retrieved 2026-10-25 —
the mechanism analysis) [CLM-0189].

## 1. What happened (observable facts only)

Google rolled out **AI Overviews** — generative-AI summaries atop search
results — to hundreds of millions of users in May 2024 [SRC-REPORT-019].
Within days, users documented absurd and dangerous answers: the overview
telling users to **put non-toxic glue on pizza** to help cheese stick,
and to **eat at least one small rock per day** because "rocks are a
vital source of minerals and vitamins" [SRC-REPORT-019; the quotes are
the article's reproductions of overview text]. The BBC's report states
the responses "said geologists recommend humans eat one rock per day"
and quotes a Google spokesperson acknowledging issues [SRC-REPORT-018].
The Verge reported Google "scrambling to manually remove weird AI
answers" one by one [SRC-REPORT-017], and a follow-up Verge piece
(2024-05-30) covered Google's public defense of the product
[SRC-REPORT-017, same outlet's follow-up noted in the register].

The **mechanism**, established by the retrieved analysis
[SRC-REPORT-019]: the rock-eating recommendation traced to a
**satirical article from The Onion** — "there aren't a lot of articles
on the web about eating rocks as it is so self-evidently a bad idea…
there is, however, a well-read satirical article from The Onion about
eating rocks. And so Google's AI based its summary on **what was
popular, not what was true**." The piece's diagnosis, quoted for the
course's purposes: "generative AI tools don't know what is true, just
what is popular."

## 2. What this incident teaches (established, attributed)

1. **The abstention gap at search scale.** A system with no
   selective-prediction layer answered self-evidently unanswerable
   queries with fluent confidence — Ch. 06's entire subject, at the
   largest deployment surface in software. The failure is not
   hallucination frequency; it is the *absence of an "I cannot verify
   this" channel* (P03's instruments exist for exactly this).
2. **Popularity is not a truth oracle.** Retrieval-grounded generation
   inherits the retrieved corpus's satire, pranks, and consensus
   errors as candidate "sources" — note 41's instrument-circularity
   warning, deployed rather than warned about. The Onion attribution
   makes this the cleanest documented instance of **satire laundering**
   into authoritative presentation.
3. **Manual removal does not scale.** Google's whack-a-mole response
   [SRC-REPORT-017] is the incident's second lesson: a deployed
   generator's failure surface is combinatorial; incident-driven
   patching is a *monitoring* strategy, not a *prevention* one —
   Ch. 22's release-gate argument in miniature.
4. **Rollout asymmetry.** A feature shipped to hundreds of millions
   on a competitive timeline ("playing catch-up with OpenAI and
   Microsoft" [SRC-REPORT-019]) discovered its failure profile in
   production. The course files this under Ch. 21's sociotechnical
   risk: the deployment decision, not the model, was the incident's
   proximate cause.

## 3. What this does NOT demonstrate

Not a general claim that "AI search is useless" (many overviews were
fine); not a measurement of hallucination *rate* (no denominator
exists in the press record — the course refuses to quote one); not
evidence about current-generation models (2024-era, scale-drift
honesty applies). The incident demonstrates a *mechanism class*, not a
rate.

## 4. Course wiring

- **Ch. 06** (honesty/abstention): the flagship deployed-system case
  for selective prediction — pairs with FActScore (note 46) and
  SelfCheckGPT (note 47) as the instrument set this incident lacked.
- **Ch. 17** (deployment reliability): the position/coverage lesson —
  long-tail queries are the shift surface.
- **Ch. 22**: the gate design that would have asked "what is the
  abstention rate on unanswerable queries?" before rollout.
- **P03**: the incident's deterministic-tier twin — the project's
  threshold policies are the counterfactual instrument.

## 5. Honest limitations of this review

Press-coverage basis: The Verge and BBC pages were inspected via
search-result content (quotes and dates verified; full articles not
independently fetched); The Conversation piece was retrieved in full.
Google's internal postmortem is not public; remediation details
beyond "manual removals" are unrecorded here. The "hundreds of
millions" rollout scale is the analysis piece's figure, quoted with
its source.
