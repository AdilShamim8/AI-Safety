# Incident review: Meta's Galactica — plausible nonsense at scientific authority

Class: **production incident (research-tool rollout withdrawn)** · Date
of event: launched 2022-11-15; public demo taken down 2022-11-18
(**three days**) · Date of this note: 2026-10-25
Sources: SRC-REPORT-035 (MIT Technology Review, 2022-11-18,
page-inspected via search-result content), SRC-REPORT-036 (The
Conversation, 2022-11-29, page content retrieved 2026-10-25 — the
analysis with the mechanism) [CLM-0217].

## 1. What happened (observable facts only)

Meta launched **Galactica**, a large language model trained on
scientific knowledge, with a public online demo intended to help
scientists write and summarize research. The launch met "three days
of intense criticism," and the company **took down the public demo
on 2022-11-18** [SRC-REPORT-035]. The criticism's content, as the
coverage's own headline phrases it: the model **"spat out
alarmingly plausible nonsense"** [SRC-REPORT-036] — fluent,
authoritative-sounding scientific text that was wrong: fabricated
citations, plausible-but-false claims, content critics
characterized as "pseudoscience" and "biased" [per the corroborating
coverage in the search record — LinkedIn News summary; Silicon
Republic, 2022-11-22].

The Conversation's analysis named the mechanism the course pins:
Galactica was "trained on scientific knowledge" — and produced
confident nonsense anyway, because **training on the scientific
corpus is not grounding in scientific truth**: the model inherited
the *form* of science (its vocabulary, its citation grammar, its
confident register) without its verification layer [SRC-REPORT-036,
the analysis's diagnosis].

## 2. What this incident teaches (established, attributed)

1. **Authority presentation without a verification layer is a
   harm multiplier, again.** The same lesson as [MyCity
   (05)](05-nyc-mycity-chatbot.md) — trust context × wrong content —
   now in the science domain, where the audience was researchers
   themselves and the harm was epistemic: plausible nonsense
   wearing citations is *harder* to catch than obvious error.
2. **The form/truth gap.** Scientific corpora teach the *shape* of
   scientific writing. Fluency in the shape is what [HELM
   (note 49)](../49-helm.md)'s omissions and
   [FActScore (note 46)](../46-factscore.md)'s
   reference-checking exist to price: the instrument this demo
   lacked was atomic-claim verification against named sources.
3. **Three-day withdrawal as responsible response.** Unlike MyCity's
   keep-it-up, Meta pulled the demo — comparison 10's
   withdrawal posture, applied to a *research demo* before
   production harm materialized. The course files the contrast:
   the same organization, different surface, faster honest
   characterization.
4. **The audience was the safety lesson.** Scientists poking the
   demo *found* the failures within days — adversarial-grade
   users discovering the failure surface pre-deployment. The
   course's Ch. 15 argument for open red-teaming before release:
   this incident is its exhibit.

## 3. What this does NOT demonstrate

Not a claim about Galactica's downstream use (demo withdrawn; the
weights' later circulation is out of scope); not a rate of nonsense
generation (no denominator in the coverage — the note quotes none);
not a claim about current Meta models.

## 4. Course wiring

- **Ch. 06:** the factuality chapter's scientific-domain incident —
  pairs with AI Overviews (04) as the two "fluent authority without
  verification" cases, one at consumer search scale, one at
  research-tool scale.
- **Ch. 21/20:** the rollout-governance case — public demo as
  soft-launch gate, withdrawn on evidence.
- **Ch. 02:** construct validity at the model level: "trained on
  science" ≠ "scientifically reliable," the gap sentence this
  launch omitted.

## 5. Honest limitations of this review

MIT Technology Review inspected via search-result content (headline,
dates, and the three-day/withdrawal facts verified); The
Conversation's analysis retrieved in full (the mechanism quotes are
its own). Corroborating outlet summaries (LinkedIn News,
Silicon Republic) noted in the search record, not separately
registered — the two registered sources carry the unit.
