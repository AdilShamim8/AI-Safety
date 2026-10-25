# Incident review: NYC MyCity chatbot — authoritative channel, unlawful answers

Class: **production incident** · Date of event: launched 2023-10-16
(nyc.gov announcement); The Markup's investigation published
2024-03-29; city's defense through 2024-04-05 · Date of this note:
2026-10-25
Sources: SRC-REPORT-020 (The Markup investigation, page content
retrieved 2026-10-25), SRC-REPORT-021 (NYC Mayor's Office launch
announcement, 2023-10-16, page-inspected via search-result content),
SRC-REPORT-022 (AP News coverage of the city's response, 2024-04-03,
page-inspected via search-result content) [CLM-0190].

## 1. What happened (observable facts only)

In October 2023, New York City launched an AI-powered chatbot on the
MyCity Business site to help business owners navigate government —
announced by Mayor Eric Adams as part of a responsible-AI plan
[SRC-REPORT-021]. Five months later, The Markup's investigation
[SRC-REPORT-020] documented the Microsoft-powered bot giving answers
that were not merely wrong but **unlawful-favoring**: that landlords
could refuse tenants on rental assistance (source-of-income
discrimination is illegal in NYC, with a small exception for
owner-occupied buildings), that bosses could **take workers' tips**
(headline finding), that a tenant could be locked out (illegal after
30 days of tenancy), and that there were "no restrictions on the
amount of rent that you can charge" (rent stabilization exists).

The follow-through, documented by AP [SRC-REPORT-022] and the wider
press record: the city **kept the chatbot up** — the mayor defended
it, the bot was relabeled a "beta" pilot, and reporting noted six
months and a reported $600,000 of spend since launch (the
Entrepreneur/AP press line, recorded with its source). A local
housing policy expert characterized the information as "dangerously
inaccurate" [SRC-REPORT-020].

## 2. What this incident teaches (established, attributed)

1. **Authoritative presentation is a hazard multiplier.** The same
   wrong answer is worse on a government domain — users rationally
   discount marketing chatbots and rationally *trust* .gov channels.
   The course's Ch. 21 framing: the harm lives in the trust context,
   not the text. Every wrong answer here carried the city's implicit
   warranty.
2. **Domain guardrails were the missing layer.** The bot answered
   legal-compliance questions from general knowledge instead of
   routing to the city's own rules — the absence of Ch. 14's
   tool/authorization pattern (answer *from the statute database*,
   never from the prior). The failure is architectural: no boundary
   between "friendly explanation" and "legal answer."
3. **Harm directionality.** Every documented error pointed toward the
   *more powerful party*: landlords over tenants, bosses over
   workers. That asymmetry is not accidental — the bot's errors
   inherited the priors of ambiguous-source training data, and
   ambiguity resolves toward the default world, not the regulated
   one. Ch. 21's distributional lens, materialized.
4. **The remediation failure is the second incident.** Keeping the
   system live after documented unlawful advice — with a defense and
   a "beta" label — is its own lesson: Ch. 22's deployability-gate
   logic says the *evidence of failure* should have moved the
   release decision, and it did not. The register records this as
   the course's canonical example of incident-response governance
   failing after incident detection succeeded.

## 3. What this does NOT demonstrate

Not a claim about Microsoft's technology generally (the architecture
choice — general chat over a compliance domain — was the city's);
not a rate measurement (The Markup's testing was systematic but the
note quotes no denominator); not evidence the bot *caused* illegal
acts (the harm documented is unlawful *advice*, not confirmed
unlawful *action* — a distinction the note keeps sharp).

## 4. Course wiring

- **Ch. 21** (sociotechnical and systemic risk): the flagship
  government-deployment case — trust context, power asymmetry, and
  institutional remediation failure in one incident.
- **Ch. 14:** the tool-authorization counterfactual — the design that
  routes legal questions to pinned sources.
- **Ch. 22:** release-gate and incident-response governance — what
  the "keep it up" decision lacked (an evidence-to-decision path).
- **P07/P10:** the guard/dossier pattern for public-sector
  deployments cites this incident as the motivating case.

## 5. Honest limitations of this review

The Markup page was retrieved in full via the search tool; the NYC
launch page and AP coverage were inspected via search-result content
(quotes/dates verified in snippets). The OECD AI incident database
carries an entry aggregating the coverage (noted, not separately
registered — the three registered sources carry the load). The
$600,000 figure and the bot's continued operation are as of the
2024-04 press record; later status unrecorded here.
