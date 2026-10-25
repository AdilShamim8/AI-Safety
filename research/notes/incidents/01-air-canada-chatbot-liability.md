# Incident review: Air Canada chatbot — the liability that stayed

Class: **production incident** · Date of event: advice given 2023,
ruling 2024-02-14 (decision published as 2024 BCCRT 149) · Date of this
note: 2026-10-25
Sources: SRC-REPORT-013 (ABA Business Law Today analysis, page-inspected
2026-10-25) · Access level recorded honestly: the tribunal's own decision
page was unreachable at fetch time, so every ruling detail below is
second-hand through the ABA summary — flagged in the register [CLM-0168].

## 1. What happened (observable facts only)

A passenger, Jake Moffatt, asked Air Canada's website chatbot about
bereavement fares when booking a flight to attend his grandmother's
funeral. The chatbot replied that a reduced bereavement fare could be
claimed retroactively: submit the ticket through an online form within
ninety days of issuance and the difference would be refunded. Moffatt
bought the ticket relying on that reply, submitted the claim as
instructed — and Air Canada refused it, pointing to pages elsewhere on
its own website stating the opposite (bereavement discounts must be
requested before travel). Moffatt took the airline to British Columbia's
Civil Resolution Tribunal. The tribunal found Air Canada liable for the
chatbot's misrepresentation and awarded roughly CAD 650 in damages plus
pre-judgment interest and filing fees [CLM-0168].

## 2. System and context

A customer-facing chatbot embedded in the airline's public website, in
the same channel where the airline's authoritative fare rules were
published. No separation was presented to the user between "the chatbot
answers" and "the website answers" — and, critically, none was
recognized by the tribunal either. The control that did NOT exist:
any check that the chatbot's claims about fare policy matched the
policy pages a few clicks away, and any output boundary limiting the
chatbot to verified policy statements.

## 3. What the investigation established

Per the ABA summary of the decision [SRC-REPORT-013]:

- Air Canada argued the chatbot was "a separate legal entity that is
  responsible for its own actions." The tribunal rejected this: the
  chatbot is part of the website, and the airline is responsible for
  all information on its site, static page or generated text alike.
- The airline owed the passenger a duty of care; publishing a
  misstatement in a channel it controlled, without reasonable care to
  ensure accuracy, breached it (negligent misrepresentation).
- The "correct information existed elsewhere on the site" defense
  failed: a consumer cannot be expected to double-check one part of a
  company's website against another.

## 4. What remains unknown

- Whether the failure was pure hallucination, a stale fine-tuned
  policy answer, or a retrieval miss — no technical postmortem was
  ever published, and the vendor/model behind the chatbot was not
  named in the coverage this note read.
- How Air Canada's controls changed afterward (the record visible here
  shows the ruling, not the remediation).
- The popular narrative "courts now hold companies liable for chatbot
  hallucinations generally" overreads one small-claims tribunal
  decision in one province about one channel design; the boundary of
  the precedent is for other lawyers to argue.

## 5. Lesson extraction (mapped to course chapters)

- **Failure pathway:** an unverified generation channel was given the
  same authority-in-appearance as the policy pages it contradicted —
  Ch.13's output-handling discipline (the generation channel is not a
  source of record) and Ch.14's delegation audit (what does a tool
  call authenticate? here: nothing did).
- **The controls that would have caught it:** (a) a policy-grounded
  guard — generation constrained to retrieved policy text with the
  citation attached, so a contradiction is visible to the user;
  (b) an evaluation harness running held-out policy questions against
  the pages of record — exactly P01's paired case-set design at
  smoke-tier scale; (c) Ch.22's safety-case grammar: the airline could
  not produce ANY evidence the chatbot was tested, and the tribunal
  treated that absence as negligence, not as an acceptable unknown.
- **What this incident does NOT demonstrate:** it is not evidence that
  chatbots are "unreliable in general" (a claim about a rate), nor
  that users were deceived at scale (a claim about a population). It
  establishes one deployment, one reliance, one liability finding.

## 6. Course application

Feeds Ch.13 (§ output handling: the generation channel must not be
able to invent financial commitments), Ch.22 (§ the assurance
argument: "we tested the channel against the record" is the claim a
deployer must be able to make), and the P10 dossier's deployability
gate as the institutional answer — the gate exists precisely so that
"nobody checked" is never the post-incident finding. Exercise angle
for students: write the two-sided ledger Air Canada needed (claims the
bot may make vs. pages of record), then price the harness that checks
it nightly.

## 7. Source register updates

- SRC-REPORT-013 added (page-inspected, 2026-10-25) with the
  primary-decision-unreachable limitation recorded.
- CLM-0168 added with the second-hand-summary assumption and its
  counterevidence (the unreachable primary text).
