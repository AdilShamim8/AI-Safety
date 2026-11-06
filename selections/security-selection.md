# The security selection — the corpus's AI-security canon

**Navigate:** [← selections](README.md) · [security role](../interviews/roles/security-specialist.md) ·
[market: the workforce gap](../interviews/market/workforce-gap.md)

**What this selection is.** The curated path through the corpus for
the security family — the chapters, projects, notes, courses, and
standards that train AI security engineering, in the order that
builds, each entry saying what it is for.

## The path, in order

1. **The threat landscape** —
   [Ch.13 LLM application security](../chapters/13-llm-application-security/README.md)
   and [Ch.14 agent/tool/MCP security](../chapters/14-agent-tool-memory-mcp-security/README.md):
   the named risks (OWASP LLM Top 10 from the registered entry;
   MITRE ATLAS) and the surfaces agents add.
2. **The classic attacks that still teach** —
   [BadNets](../research/notes/13-badnets.md) (poisoning),
   [model extraction](../research/notes/14-model-extraction.md),
   [membership inference](../research/notes/15-membership-inference.md):
   the confidentiality/integrity attacks every security interview
   expects you to know cold.
3. **The defense discipline** —
   [P07 injection defense](../projects/p07-injection-defense/README.md)
   plus [Ch.12 adversarial ML](../chapters/12-adversarial-ml-and-robustness/README.md):
   measure-then-claim, with the robustness-accuracy tradeoff as a
   structural result ([Carlini-Wagner](../research/notes/05-carlini-wagner-robustness.md),
   [Madry](../research/notes/20-madry-adversarial-training.md)).
4. **The red-team craft** —
   [Ch.15 red teaming](../chapters/15-red-teaming-and-adversarial-evaluation/README.md):
   the direct/indirect distinction the
   [Greshake note](../research/notes/06-greshake-indirect-injection.md)
   defines.
5. **Practice** — the [red-team reading bank](../interviews/questions/red-team-reading.md)
   and the [defense-fix take-home](../interviews/takehomes/defense-fix.md).

## The courses that pair

[AI security engineering](../roadmaps/ai-security-engineering.md) is
the route; the layer's courses — the CampusX guardrails series and
the DataCamp security-risk course (both with full companion notes)
— supply the practitioner register this selection assumes.

## The market that prices it

[The workforce gap](../interviews/market/workforce-gap.md): 5.5M
active, 4.8M gap, +19% YoY (ISC2 2024) — the strongest demand signal
in the market layer. In the US, the [employment
outlook](../interviews/market/employment-outlook.md) (BLS: median
$129,180, +21% 2025-2035).

**The selection's one rule.** Every defense named here carries its
not-covered list; every threat is named from a registered source.
Security claims without boundaries are the failure mode this whole
selection exists to prevent.
