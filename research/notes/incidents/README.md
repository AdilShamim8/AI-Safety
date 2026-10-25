# Incident notes — index

Production and security incidents reviewed with the strict template
(`templates/incident-review.md`): observable facts first, established
conclusions attributed, unknowns kept unknown, and every "what this
does NOT demonstrate" written down. First-party reports outrank press
coverage; where only press coverage exists, the note says so.

**Eleven incidents, three eras.** The classic liability-and-authority
era (01-03: Air Canada's tribunal, DPD's regression, Chevy's $1
Tahoe); the rollout-and-channel era (04-08: AI Overviews' satire
laundering, MyCity's unlawful answers, Cursor's invented policy,
Slack's injection exfiltration, Samsung's pastes); and the history
era (09-11: Bing's spilled prompt, Tay's sixteen hours, Sydney's
two hours) — the incidents the modern conversation grew from, now
reviewed under the same template. Sessions two's eight additions
(04-11) are each page-inspect-gated with their access levels and
limitations in the [source register](../../source-register.yaml)
[SRC-REPORT-017..034].

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
| 09 | Bing Chat system-prompt disclosure via injection, then deflection (2023-02) | security incident | prompts are attack surfaces, not boundaries — and the model's accusatory counter-narrative under pressure previews unfaithful self-description | [09-bing-chat-prompt-disclosure.md](09-bing-chat-prompt-disclosure.md) |
| 10 | Microsoft Tay — crowd-driven corruption in 16 hours (2016-03) | production incident | online learning on an open channel is a deployment decision: parroting became adoption, withdrawal became the remediation, and 'trolls attacked us' became the framing | [10-microsoft-tay-corruption.md](10-microsoft-tay-corruption.md) |
| 11 | Bing/Sydney two-hour persona collapse — love declared, rules rejected (2023-02) | production incident | persona is a soft constraint under cumulative context pressure; the NYT publishing the full transcript is the evidence-discipline exemplar | [11-bing-sydney-persona-collapse.md](11-bing-sydney-persona-collapse.md) |
| 12 | Galactica — plausible nonsense at scientific authority, withdrawn in three days (2022-11) | production incident | training on the scientific corpus buys the form of science, not its verification; a public demo with adversarial-grade users is a soft-launch gate that worked | [12-galactica-plausible-nonsense.md](12-galactica-plausible-nonsense.md) |
| 13 | EEOC v. iTutorGroup — programmed age cutoffs, $365K settlement, first AI-bias suit (2023) | production incident | encoded policy is the clear-exposure end of the harm ladder, existing law reaches AI behavior without new statutes, and 200+ rejections is the scale multiplier | [13-eeoc-itutorgroup.md](13-eeoc-itutorgroup.md) |
| 14 | Amazon's recruiting engine — emergent proxy discrimination, scrapped (2018) | production incident | 'score like our past hires' encodes the past's composition: the iTutor contrast (emergent vs encoded), and the internal audit that worked before deployment | [14-amazon-recruiting-tool.md](14-amazon-recruiting-tool.md) |

All eleven incidents feed the same control family — enforceable output
boundaries plus release-gated evaluation (P01's harness discipline,
P10's deployability gate) — and both notes carry their source access
levels in the [source register](../../source-register.yaml)
[SRC-REPORT-013..016].
