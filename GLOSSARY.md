# Glossary

Terms are added **with the chapters that need them**; this file grows as the
course builds. Each entry: definition, notation/aliases, common confusions,
and the chapters that use the term. Sources are cited where a definition
follows a specific document; otherwise the definition is this course's own
operationalization.

| Term | Definition | Aliases / notation | Common confusion | Chapters |
|---|---|---|---|---|
| **AI safety** | Studying and reducing harms from AI systems, including failures of objectives, robustness, oversight, deployment, misuse, and human institutions. | — | Treated as a property of a model ("a safe model") instead of a claim about a system-in-context (see *safety claim*). | all |
| **AI alignment** | Making system behavior and learned objectives compatible with intended human goals, constraints, and values — including the question of whose intentions count. | — | Used interchangeably with *safety*; alignment is one family of causes of (un)safety. | 03–08, 24 |
| **AI security** | Protecting models, data, tools, infrastructure, and AI-enabled workflows against adversaries, exploitation, and unauthorized actions. | — | Security *of* AI vs. AI *for* cybersecurity — different fields, overlapping techniques. | 12–16, 19 |
| **AI assurance** | Assembling and challenging evidence about a system's behavior and risks in a specified deployment context. | — | Assurance ≠ testing: assurance organizes evidence for a decision; testing produces evidence. | 02, 22, 23 |
| **Safety claim (context-relative)** | The workable form: in this defined workflow, with these permissions and controls, the evidence supports keeping these specified risks below these stated limits. | σ, κ, h, τ notation (Ch. 01) | Re-using a claim from one context in another after the system, tools, or users changed. | 01, 22 |
| **Hazard** | A potential source of harm (wrong output, leaked data, unauthorized action, harmful capability used). | h | Confused with *risk* (which adds likelihood and exposure); confused with *threat* (which implies an adversary). | 01, 13, 22 |
| **Capability** | What a system can do that enables a hazard. | — | Capability ≠ propensity: being able to do X says nothing about how often X is done in context. | 01, 20 |
| **Propensity** | How often, in a specified context, the system actually exhibits the enabling behavior (a rate with a denominator). | — | Estimated without a context or denominator — the most common unoperationalized word in safety prose. | 01, 02, 15 |
| **Exposure** | Who or what is positioned to be harmed (users, data, downstream systems). | — | Omitted entirely in model-only risk talk. | 01, 21 |
| **Severity** | Magnitude of harm conditional on realization. | — | Averaged into single "expected loss" numbers that hide tail structure. | 01, 22 |
| **Causal pathway** | The mechanism chain from trigger through behavior to harm. | p | Drawn as a diagram and then never attached to evidence — the pathway becomes decoration. | 01, 13, 17 |
| **Threat hypothesis** | Operational form: in context κ, system σ exhibits behavior b via pathway p, producing harm exceeding threshold τ; with pre-stated weakening observations. | H(·) | A hypothesis with no pre-stated weakening observations is a position, not a hypothesis. | 01, 15, 22 |
| **Evidence kinds** | The course's six: documented incidents, controlled experiments, formal results, benchmark results, forecasts, ethical judgment. | — | Treating the hierarchy as one ladder; kind must match the claim being made. | 01, 02, all |
| **Aleatory / epistemic / model uncertainty** | Randomness in the process / things true but unknown to you / the decomposition itself possibly wrong. | — | Collapsing all three into one number, or using "uncertain" to mean "no evidence." | 01, 02, 17 |
| **Disagreement** | Experts holding different model structures or values — distinct from uncertainty; recorded, not averaged away. | — | Laundered into variance and averaged. | 01, 21, 23 |
| **Mesa-optimization** | A learned model that is itself an optimizer; its objective may differ from the training loss. Introduced by Hubinger et al. (arXiv:1906.01820). | inner optimization | Treated as established fact about current models rather than a hypothesis with conditions (the source paper's own framing is careful here). | 01 (method lesson), 03, 07 |
| **Accident (Concrete Problems sense)** | Unintended and harmful behavior emerging from poor design of real-world ML systems. From Amodei et al. (arXiv:1606.06565). | — | Read as "rare stochastic event"; the source meaning is design-induced harmful behavior, frequency unspecified. | 01, 03 |
| **Rubber-stamp rate** | Course term (Ch. 01 solutions): share of system-flagged items approved by humans that fail independent re-review. | — | Measured without a pre-deployment baseline — then the number has no referent. | 01, 21 |
