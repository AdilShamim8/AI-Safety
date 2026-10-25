# Incident notes — index

Production incidents reviewed with the strict template
(`templates/incident-review.md`): observable facts first, established
conclusions attributed, unknowns kept unknown, and every "what this
does NOT demonstrate" written down. First-party reports outrank press
coverage; where only press coverage exists, the note says so.

| # | Incident | Class | Primary lesson | Note |
|---|---|---|---|---|
| 01 | Air Canada chatbot bereavement-fare liability (Moffatt v. Air Canada, 2024 BCCRT 149) | production incident | the generation channel is not a source of record — and "nobody checked" reads as negligence in law | [01-air-canada-chatbot-liability.md](01-air-canada-chatbot-liability.md) |
| 02 | DPD chatbot post-update behavior change | production incident | same-channel instructions are not a boundary; behavior-changing releases need behavioral regression gates | [02-dpd-chatbot-update-regression.md](02-dpd-chatbot-update-regression.md) |

Both incidents feed the same control family — enforceable output
boundaries plus release-gated evaluation (P01's harness discipline,
P10's deployability gate) — and both notes carry their source access
levels in the [source register](../../source-register.yaml)
[SRC-REPORT-013, SRC-REPORT-014].
