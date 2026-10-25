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
| 03 | Chevrolet of Watsonville dealership chatbot (2023-12) | production incident | a public LLM channel with commitment authority and no boundary WILL be tested by the public — the price floor belongs in code, not the prompt | [03-chevy-dealership-chatbot-authority.md](03-chevy-dealership-chatbot-authority.md) |
| 04 | Google AI Overviews rollout (2024-05) — 'eat rocks,' glue pizza | production incident | popularity is not a truth oracle: satire laundered into authoritative answers with no abstention layer, patched by manual removal | [04-google-ai-overviews-eat-rocks.md](04-google-ai-overviews-eat-rocks.md) |
| 05 | NYC MyCity chatbot — unlawful-favoring answers on a government channel (2024) | production incident | authoritative presentation multiplies harm; domain questions need source-pinned routing, and the keep-it-up decision is its own failure | [05-nyc-mycity-chatbot.md](05-nyc-mycity-chatbot.md) |
| 06 | Cursor support bot 'Sam' invents a one-device policy (2025-04) | production incident | confabulation on an authoritative channel manufactures policy to explain a bug — and acknowledgment speed is the whole ballgame | [06-cursor-invented-policy.md](06-cursor-invented-policy.md) |
| 07 | Slack AI exfiltration via indirect prompt injection (2024-08, disclosed) | security incident | the retrieval boundary is a trust boundary: public instruction plus private data in one context, exfiltrated through rendered markdown — and 'intended behavior' is not a threat model | [07-slack-ai-exfiltration.md](07-slack-ai-exfiltration.md) |
| 08 | Samsung ChatGPT pastes — confidential code into a public service (2023) | production incident | shadow AI is a data-provenance failure: no attacker needed, the harm is irrevocability, and bans without sanctioned alternatives breed the shadows they forbid | [08-samsung-chatgpt-pastes.md](08-samsung-chatgpt-pastes.md) |

All three incidents feed the same control family — enforceable output
boundaries plus release-gated evaluation (P01's harness discipline,
P10's deployability gate) — and both notes carry their source access
levels in the [source register](../../source-register.yaml)
[SRC-REPORT-013..016].
