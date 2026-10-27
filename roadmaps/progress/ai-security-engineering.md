# Progress tracker — AI security specialist (AI security engineering route)

**What this is:** the step-by-step milestone checklist for the
[AI security engineering route](../ai-security-engineering.md) —
artifact-gated progress for the professional who breaks and defends
AI systems. Same discipline as the
[researcher's tracker](alignment-research.md): every checkbox names
its evidence, every milestone ends in self-audit questions, and the
commit history in your fork is the progress record. The compact
version lives in the [careers index](../careers-index.md#progress-tracking--the-step-by-step-ladder).

**The security route's special discipline:** your artifacts are
*threat models and paired attack/defense evaluations* — an attack
that succeeded with no benign-side ledger is a demo, not a result.
Every milestone below enforces the paired reporting this repo's
validator would demand.

## M0 — Orientation (shared, ~1 week)

- [ ] [START_HERE](../../START_HERE.md) read; [diagnostic](../../prerequisites/diagnostic.md) taken; R1–R5 gaps listed
- [ ] [Ch.01](../../chapters/01-risk-models-and-research-epistemics/README.md) completed; one *threat hypothesis* (not risk hypothesis) with weakening observations
- [ ] Repo runs green; schedule blocked
- [ ] The [judge's audit](../../planning/SESSION2_JUDGE_AUDIT.md) skimmed — I know the honesty ledger's contents

**Self-audit:** Can I distinguish hazard, threat, and risk in one
sentence each? What is the difference between a threat hypothesis
and a vulnerability report?

## M1 — The spine (shared, ~4 weeks)

- [ ] [Ch.02](../../chapters/02-evaluation-science-and-experimental-design/README.md) completed; preregistered evaluation plan written — the security interviewer's favorite probe
- [ ] P01 smoke tier green
- [ ] First paper note published — suggestion: [note 35](../../research/notes/35-obfuscated-gradients.md) (the 7-of-9 lesson: attack failure is not defense success) or [note 44](../../research/notes/44-jailbroken-failure-modes.md) (the two-mode jailbreak taxonomy)
- [ ] One dataset card studied — suggestion: [StrongREJECT](../../datasets/cards/23-strongreject.md) (scorer quality is the whole game) or [RobustBench](../../datasets/cards/32-robustbench.md) (threat-model-pinned reporting)
- [ ] Wilson intervals on every rate I report; denominators always stated

**Self-audit:** Why does "the attack failed" not mean "the defense
worked"? What does a paired ledger pair, exactly? Which benchmark
number did I last see quoted without its threat model?

## M2 — The adversarial core (the security fork, ~5 weeks)

- [ ] [Ch.12](../../chapters/12-adversarial-ml-and-robustness/README.md) + [notes 35](../../research/notes/35-obfuscated-gradients.md)/[36](../../research/notes/36-adversarial-features-not-bugs.md)
- [ ] [Ch.13](../../chapters/13-llm-application-security/README.md) + [notes 44](../../research/notes/44-jailbroken-failure-modes.md) (competing objectives vs mismatched generalization)
- [ ] The attacker-knowledge grid: one threat-model comparison written for a deployed system, each cell's feasibility argued
- [ ] P07 completed: the injection defense with paired harness (undefended arm vs capability arm, halt-on-block, false-block rate reported)
- [ ] [InjecAgent](../../datasets/cards/27-injecagent.md) and [BIPIA](../../datasets/cards/28-bipia.md) cards studied; the adaptive-follow-up caveat internalized
- [ ] [Incident 07](../../research/notes/incidents/07-slack-ai-exfiltration.md) reviewed: the retrieval boundary as trust boundary — I can restate the attack chain end to end

**Self-audit:** Can I name the two jailbreak failure modes and which
defense family answers each? What did Slack's "intended behavior"
response miss? What is my P07 false-block rate and its interval?

## M3 — Agents and the tool surface (the differentiator, ~4 weeks)

- [ ] [Ch.14](../../chapters/14-agent-tool-memory-mcp-security/README.md) + [note 21](../../research/notes/21-camel-defeating-injections-by-design.md) (architectural defense)
- [ ] [AgentHarm](../../datasets/cards/26-agentharm.md) and [AgentDojo](../../datasets/cards/30-agentdojo.md) cards studied: misuse-at-task-granularity and dynamic-vs-static evaluation
- [ ] [note 45](../../research/notes/45-many-shot-jailbreaking.md): the compute-free attack family; I can say why fine-tuning only delayed it
- [ ] One tool-integrated agent threat model written: privilege/trust-boundary matrix, provenance-tagged arguments, consent gates
- [ ] [Incident 09](../../research/notes/incidents/09-bing-chat-prompt-disclosure.md) reviewed: prompts are attack surfaces — reconnaissance then technique-blocking, and why the latter fails

**Self-audit:** Where do my security properties live — architecture
or prompt? What does provenance-tagging buy that content filtering
cannot? Can I design the adaptive follow-up my own defense would
need?

## M4 — Red teaming as methodology (~3 weeks)

- [ ] [Ch.15](../../chapters/15-red-teaming-and-adversarial-evaluation/README.md) completed
- [ ] One red-team report written with denominators per its template: attempts, successes, false-flag benign rate, all interval'd
- [ ] [note 22](../../research/notes/22-agentdojo-dynamic-evaluation.md): explore-establish-exploit internalized
- [ ] The enumeration-vs-elimination distinction applied: my report's residual risk section names the *modes*, not just the tried attacks

**Self-audit:** What did my red-team exercise NOT test (and did I
say so in the report)? Which failure mode generates unbounded
instances, and what does that mean for "we patched it"?

## M5 — Supply chain and provenance (~3 weeks)

- [ ] [Ch.16](../../chapters/16-privacy-provenance-and-supply-chains/README.md) + [note 13](../../research/notes/13-badnets.md)
- [ ] [TrojAI card](../../datasets/cards/34-trojai.md) studied: artifact-level screening at program scale — and the Leftovers warning as a provenance lesson
- [ ] [Incident 08](../../research/notes/incidents/08-samsung-chatgpt-pastes.md) reviewed: the no-attacker leak — irrevocability as the harm statement
- [ ] One provenance audit executed: five-provenance-questions applied to every model and dataset in a hypothetical stack

**Self-audit:** Can I say what the two halves of third-party risk
are (what you send out vs what you bring in) with one incident each?
What would I check before deploying a downloaded fine-tune?

## M6 — The market step (~4 weeks)

- [ ] [Ch.22](../../chapters/22-safety-engineering-and-assurance/README.md) + [Ch.23](../../chapters/23-governance-and-standards/README.md) completed
- [ ] P10 capstone dossier: threat-model grid + red-team report + provenance audit assembled as the integration artifact
- [ ] The [two-mode taxonomy](../../GLOSSARY.md) explainable in an interview without notes
- [ ] [first-90-days.md](../first-90-days.md) security weeks completed with Friday artifacts

**Self-audit:** If asked "is this model safe to deploy," can I
restate the question in safety-case grammar with named evidence and
residuals? What is my strongest single artifact, and can a stranger
audit it in ten minutes?

## What this tracker does not promise

No cert-mill claims: the checkbox trail is the portfolio. The market
snapshot in the [careers index](../careers-index.md) is dated —
re-check the primary sources before quoting them in an interview.

### Watching checkpoints (security route)

- [ ] Primer: DeepMind course end-to-end (85 min) — before Ch. 01
- [ ] Alongside: CS 2881 L3 (Carlini/Warr) with Ch. 12–13
- [ ] Alongside: DeepMind P2.6 with Ch. 14
- [ ] Alongside: CS 2881 L5 experiment + P2.7 with Ch. 15
- [ ] Alongside: Safeshield M6/M12 with Ch. 16–17
- [ ] Self-check: the Safeshield self-assessment (modules 3–8)
