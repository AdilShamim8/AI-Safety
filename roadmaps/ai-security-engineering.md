# Route: AI security engineering

**Primary purpose:** secure AI applications and agent workflows — from
classical adversarial ML through LLM application security to agent/tool
security — producing engineering-grade artifacts: threat models, isolated
attack/defense evaluations, regression suites, remediation reports.

**You:** a security engineer who can pass diagnostic tasks B/D/E (and will
likely need R4 for chapter 03 and R1/R2 light for chapter 12), or an ML
engineer who needs R5. The route deliberately teaches both languages; the
diagnostic tells you which side to refresh.

**Session-2 readings now in the route's spine:** [obfuscated
gradients](../research/notes/35-obfuscated-gradients.md) and
[non-robust features](../research/notes/36-adversarial-features-not-bugs.md)
(Ch.12), [the two-mode jailbreak taxonomy](../research/notes/44-jailbroken-failure-modes.md)
with [the one-bit diagnostic](../research/notes/comparison-08-jailbreak-modes-defense-families.md)
(Ch.13), [many-shot](../research/notes/45-many-shot-jailbreaking.md) and
[Llama Guard](../research/notes/65-llama-guard-safeguard-model.md) (Ch.13/15),
[HotFlip](../research/notes/73-hotflip.md) for the text-attack lineage,
the memorization trilogy — [Secret Sharer](../research/notes/56-secret-sharer-memorization.md),
[extraction](../research/notes/57-extracting-training-data.md),
[quantification](../research/notes/58-quantifying-memorization.md) — with
[trojan detection](../research/notes/69-trojan-detection-llms.md) (Ch.16),
and the incident quartet: [Slack exfiltration](../research/notes/incidents/07-slack-ai-exfiltration.md),
[Bing's spilled prompt](../research/notes/incidents/09-bing-chat-prompt-disclosure.md),
[Samsung's pastes](../research/notes/incidents/08-samsung-chatgpt-pastes.md),
[Tay](../research/notes/incidents/10-microsoft-tay-corruption.md).

## Sequence
[**Track your progress:**](progress/ai-security-engineering.md) the security route's expanded milestone checklist (M0–M6, paired ledgers enforced).



| Step | Unit | ≈ hours | Evidence produced |
|---|---|---|---|
| 1 | Ch.01 risk models & epistemics | 8 | threat hypothesis |
| 2 | Ch.02 evaluation science | 12 | preregistered evaluation plan |
| 3 | P01 evaluation harness (smoke tier) | 20 | harness + scorer validation (reused by P07/P10) |
| 4 | Ch.12 adversarial ML & robustness | 10 | attacker-knowledge comparison table |
| 5 | Ch.13 LLM application security | 10 | injection-to-framework mapping |
| 6 | Ch.14 agent, tool, memory & MCP security | 10 | privilege & trust-boundary matrix |
| 7 | P07 local RAG + agent injection defense | 25 | attack/defense evaluation: unauthorized-action rate vs. benign completion vs. false blocks, on unseen cases |
| 8 | Ch.15 red teaming & adversarial evaluation | 10 | red-team report with explicit denominators |
| 9 | Ch.16 privacy, provenance & supply chains | 8 | provenance audit |
| 10 | Ch.19 multimodal & embodied safety | 8 | cross-modal case analysis |
| 11 | Ch.08 AI control & monitoring (shared with evals route) | 10 | control protocol + failure conditions |
| 12 | P08 control & monitoring protocol | 20 | usefulness-failure tradeoff under audit budget |
| 13 | paper notes (≥8 on this route) | 16 | notes/papers/* |
| 14 | Ch.24 research practice | 8 | remediation-report structure |
| 15 | capstone P10: agent evaluation & assurance dossier | 40 | threat model + regression suite + safety case + deployment-decision impact |

Core sequence ≈ 225 h; the 24-week part-time schedule covers steps 1–12;
schedule A covers steps 1–8 plus a mini-capstone (threat model + regression
suite from P07's hardened build). All security labs run **locally against
synthetic targets only** (see [RESPONSIBLE_RESEARCH.md](../RESPONSIBLE_RESEARCH.md)).

## Exit criteria (portfolio evidence)

1. **A threat model:** P07/P10's system modeled with trust boundaries,
   attacker-controlled inputs, and authorization decisions — the artifact
   diagnostic task D previews.
2. **An isolated attack/defense evaluation:** prompt-only defense vs.
   enforceable authorization boundary, benign controls included, false-block
   rate reported (not just attack success).
3. **A regression suite:** the hardened build's tests that fail if the
   enforcement layer regresses — safety as a CI property, not a document.
4. **A remediation report:** what was found, what was fixed, what residual
   risk remains, with evidence for each claim.

### The lecture-library pairing

This route's chapters pair with the video layer as follows (full
mapping in [courses/study-plans.md](../courses/study-plans.md) and
each chapter's watching-companions block):
- CS 2881's robustness lecture (Carlini and Warr as guests) with the
  adversarial and application-security chapters (Ch. 12–15).
- The DeepMind design-patterns video with agent security (Ch. 14).
- The Safeshield privacy and lifecycle modules with the deployment
  chapters (Ch. 16–17).

## Pitfalls this route is designed to prevent

- Treating all attacks as equivalent (Ch.12 separates threat models:
  white-box evasion ≠ poisoning ≠ extraction).
- Prompt-level "fixes" reported as defenses (Ch.13/P07 measure their leak
  rate honestly).
- Attack-success numbers without denominators or benign controls (Ch.15's
  reporting standard).
- Agent demos with unbounded tools, host mounts, or real credentials
  (P07/P10 enforce the boundary instead of assuming it).
