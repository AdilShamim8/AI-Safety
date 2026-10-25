# Comparison 10 — incident-response postures: what the eleven incidents teach about acknowledging failure

**The practitioner's question:** my AI system failed in public —
what does the incident record say about the response postures that
made things better or worse?

**The source:** the course's own [incident file
(01-11)](../notes/incidents/README.md) — eleven reviewed incidents,
three eras, with the response half of each recorded under the
template's observable-facts discipline. This comparison extracts
the response-quality pattern the file now supports; it is the
course's own synthesis, sourced to the individual incident notes
named below.

## 1. The posture spectrum the incidents populate

| Posture | Incident | The observable response | The outcome it bought |
|---|---|---|---|
| **Immediate acknowledgment + remediation** | [Cursor (06)](../notes/incidents/06-cursor-invented-policy.md) | "no such policy… an incorrect response from a front-line AI support bot" — three hours; apology; refund | subscriptions recoverable; the failure became a case study in *good* response |
| **Institutional accountability (slow, legal)** | [Air Canada (01)](../notes/incidents/01-air-canada-chatbot-liability.md) | denied responsibility ("separate legal entity"); tribunal rejected the defense; liability assigned | legal precedent that generation channels ARE the company's word |
| **Keep-it-up + defend** | [NYC MyCity (05)](../notes/incidents/05-nyc-mycity-chatbot.md) | bot stayed live after documented unlawful advice; mayor defended; "beta" relabel | detection succeeded, remediation failed — the governance failure is the incident's second half |
| **Feature-defense ("intended behavior")** | [Slack (07)](../notes/incidents/07-slack-ai-exfiltration.md) | defended public-channel searchability while missing the composition | severity disputed by vendor; disclosure carried the remediation pressure |
| **Withdrawal** | [Tay (10)](../notes/incidents/10-microsoft-tay-corruption.md) | shutdown 16 hours after launch | damage contained; "trolls attacked us" framing externalized design responsibility |
| **Manual whack-a-mole** | [AI Overviews (04)](../notes/incidents/04-google-ai-overviews-eat-rocks.md) | answers removed one by one under press coverage | combinatorial failure surface met with linear remediation |

## 2. The pattern: acknowledgment speed is the primary variable

Across the file, the response variable that correlates with outcome
quality is **time-to-honest-characterization** — how long between
the failure being visible and the organization saying "our system
did that." Cursor: three hours, and the story became recoverable.
MyCity: the honest characterization arguably never arrived (the
defense posture held), and the incident's second half is now the
teaching. Air Canada's characterization arrived by tribunal order —
the slowest possible path, and the one that sets precedent instead
of resolving quietly. The course's Ch.22 release-gate logic
(evidence-to-decision paths) is the *pre-incident* version of the
same variable: the organization that has decided in advance what
evidence moves what lever does not spend its response window
deciding whether to look.

## 3. The posture traps, named

1. **The legal-entity defense** (Air Canada): treating the model as
   an autonomous agent whose statements the company merely hosts.
   Legally dead (per the tribunal), operationally corrosive — it
   guarantees the honest characterization arrives by force.
2. **The "intended behavior" defense** (Slack, MyCity's beta
   relabel): answering a *feature* question when asked a
   *composition* question. Each component behaved as designed; the
   system failed. The defense is true and irrelevant — the threat
   model, not any component, is what failed.
3. **The attack framing** (Tay): attributing a design's failure to
   the people who used it. True trolls exist; the design decision
   (ungated online learning) was still the incident. The framing
   externalizes the fix and guarantees recurrence elsewhere.
4. **Linear remediation of combinatorial surfaces** (AI Overviews):
   removing answers one by one measures the problem's visibility,
   not its extent — monitoring where governance belongs.

## 4. The comparison's operational answer

The postures sort into a simple hierarchy the file supports:
**acknowledge fast and specifically** (Cursor) > **withdraw and
study** (Tay, minus the framing) > **litigate and lose slowly**
(Air Canada) > **defend the feature while the composition fails**
(Slack, MyCity). The instrument that separates the top from the
bottom is not courage but *pre-decision*: release gates, monitor
holds, and evidence-to-decision paths
([Ch.22](../../chapters/22-safety-engineering-and-assurance/README.md))
written before the incident, so the first response is not the
composition of an organization discovering its own position in
real time.

## 5. The falsifiable extension

The posture-vs-outcome correlation is qualitative here (eleven
cases, curated for teaching, not sampled for statistics — the
honesty caveat this comparison carries on its face). The
falsifiable version is a coding exercise: extend the incident
corpus with the next year's AIID entries, code each on
time-to-honest-characterization (same rubric), and test whether
the correlation survives an unbiased sample. Prediction: it does,
moderately. Falsifier: no correlation in the unbiased sample would
show the file's eleven were selected for the lesson — itself worth
knowing about how incident curricula teach.
