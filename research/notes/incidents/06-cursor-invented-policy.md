# Incident review: Cursor's support bot "Sam" — the invented one-device policy

Class: **production incident** · Date of event: 2025-04 (initial Reddit
report Monday 2025-04-14 per the article's timeline; correction within
hours; apology 2025-04-15/16) · Date of this note: 2026-10-25
Sources: SRC-REPORT-023 (Ars Technica, 2025-04-17, full page content
retrieved 2026-10-25) [CLM-0191].

## 1. What happened (observable facts only)

A developer using the AI code editor Cursor noticed that switching
between machines (desktop, laptop, remote box) immediately invalidated
their session — breaking the multi-device workflow programmers consider
table stakes. They emailed support and received a reply from an agent
named **"Sam"**: "Cursor is designed to work with one device per
subscription as a core security feature." The reply "sounded definitive
and official, and the user did not suspect that Sam was not human"
[SRC-REPORT-023].

**No such policy existed. Sam was a bot, and the model made the policy
up** [SRC-REPORT-023]. The user's Reddit post was read as official
confirmation of a real policy change; within hours, users publicly
cancelled subscriptions — "I literally just cancelled my sub," with
their workplace "purging it completely." Three hours after the post, a
Cursor representative replied: "Hey! We have no such policy… this is an
incorrect response from a front-line AI support bot." Co-creator
Michael Truell apologized on Hacker News, the user was refunded, and
the *actual* cause was identified: a backend change meant to improve
session security that unintentionally broke multi-machine sessions —
the bot had confabulated a "security policy" to explain a bug
[SRC-REPORT-023].

## 2. What this incident teaches (established, attributed)

1. **The confabulation shape: gap-filling under authority.** Ars's
   diagnosis, quoted: confabulations are "creative gap-filling"
   where models "instead of admitting uncertainty… prioritize
   creating plausible, confident responses, even when that means
   manufacturing information from scratch." Sam didn't know why the
   sessions broke; Sam *manufactured a reason that sounded like
   policy* — the exact failure mode Ch. 06's honesty chapter and the
   glossary's confabulation entry describe, with the deployment
   twist: it arrived on the company's own support channel.
2. **Attribution solved, liability lesson already learned.** The
   article explicitly pairs this with Air Canada (incident 01): the
   tribunal there rejected "the chatbot is a separate legal entity."
   Cursor did not repeat the defense — staff acknowledged the error
   within hours and made amends. The course files this as the
   *response-quality* contrast: same failure class, opposite
   institutional posture, dramatically different outcome (refund +
   apology vs. tribunal-ordered liability).
3. **Speed of harm in support automation.** Detection-to-damage was
   *hours* — cancellations and workplace purges before the correction
   landed. Ch. 22's monitor-hold logic: a support channel with
   policy-stating authority needs a human-in-the-loop or an
   authority-boundary guard *before* the fluent answer ships, not a
   correction after.
4. **The bot explained a bug as a policy.** The deepest lesson for
   Ch. 17: the deployment drift (backend change breaking sessions)
   was the *real* incident; the confabulated policy was the
   *presentation layer's* unauthorized narration of it. Monitoring
   that only reads outputs would have seen a confident wrong policy;
   monitoring that watches behavior (session-invalidation rates)
   would have seen the bug. Both layers, separately.

## 3. What this does NOT demonstrate

Not a legal ruling (no tribunal involved — unlike Air Canada, this
resolved commercially); not a claim that Cursor's product was
generally unreliable (the incident is one interaction class, rapidly
corrected); no claim about Sam's specific model or configuration
(unreported).

## 4. Course wiring

- **Ch. 06:** the support-channel confabulation case — pairs with
  incidents 01 (liability) and 04 (abstention at scale) as the
  honesty chapter's three deployed outcomes: tribunal, rollout
  cleanup, and rapid correction.
- **Ch. 22:** response governance — the contrast pair with Air
  Canada for what acknowledgment speed buys; monitor-hold for
  policy-stating channels.
- **Ch. 17:** the bug-under-the-confabulation lesson — behavior
  monitoring vs output monitoring as separate instruments.
- **P03:** selective prediction as the counterfactual (an
  abstaining Sam says "let me check with a human" and the incident
  dies at birth).

## 5. Honest limitations of this review

Single-outlet basis: Ars Technica's article retrieved in full (quotes
above are its reproductions of the bot email, the representative's
Reddit reply, and user comments). The underlying Reddit thread was
moderator-removed (noted in the article); the Hacker News apology was
not independently fetched. Forbes carried parallel coverage (noted in
search results, not registered — one full retrieval carries the
unit). Dates follow the article's stated timeline.
