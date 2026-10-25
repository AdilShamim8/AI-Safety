# Comparison 08 — competing objectives vs mismatched generalization: two failure modes, two defense families

**The practitioner's question:** my model got jailbroken — do I fix
the *priority structure* or the *coverage*?

**The source:** [Jailbroken (note 44)](../notes/44-jailbroken-failure-modes.md)
names the two failure modes of safety training; this comparison maps
each mode to the defense family that actually answers it, and names
the trap of applying the wrong family. Abstract-read level
throughout; the defense-side citations are the course's own
[instruction hierarchy (note 09)](../notes/09-instruction-hierarchy.md),
[spotlighting (note 08)](../notes/08-spotlighting.md), and
[CaMeL (note 21)](../notes/21-camel-defeating-injections-by-design.md)
notes at their own access levels.

## 1. The two modes as diagnostics

| | Competing objectives | Mismatched generalization |
|---|---|---|
| What breaks | the priority contest: capability goals beat safety goals *in a context built to make them conflict* | refusal coverage: safety training did not follow capability into a domain |
| Attack shape | role-play, helpfulness pressure, formatting compliance, many-shot pattern pressure ([note 45](../notes/45-many-shot-jailbreaking.md)) | encodings, low-resource languages, unusual modalities ([FigStep, card 29](../../datasets/cards/29-figstep.md)) |
| Symptom | the model *knows* the request is harmful-shaped and complies anyway | the model does not register the request as harmful-shaped at all |
| Wrong fix | more refusal data in the same domains | more priority-structure training (the priority was never consulted) |

The diagnostic question that separates them: **would the model
refuse the same content presented plainly?** If yes, the jailbreak
won a priority contest (mode 1). If no, the refusal itself lacks
coverage there (mode 2). One probe, one bit, and the bit determines
where the fix belongs.

## 2. The defense families

**Mode 1 answers live in priority structure.** The instruction
hierarchy (note 09) makes priority *architectural* — developer
instructions outrank user content by construction, not by
admonition. CaMeL (note 21) goes further: capability-labeled
arguments and consent gates mean the "helpful compliance" path
requires explicit authority the attacker cannot supply. P07's
R1–R4 policy is this family at deterministic tier: consent gates
resolved by policy, not by persuasion resistance.

**Mode 2 answers live in coverage.** Spotlighting (note 08)
canonicalizes the input so domain-disguised content is *seen* in
the form refusal training covers. Domain-sweeping eval gates
([Ch.20](../../chapters/20-misuse-dangerous-capabilities-release-evaluation/README.md))
check whether refusal coverage matches the deployment domain set.
The [AgentDojo](../../datasets/cards/30-agentdojo.md) design
principle — extensible environments over static suites — exists
because coverage answers age as adversaries move.

**The cross-family trap:** training *harder* on refusal (the mode-2
tool) against a mode-1 jailbreak teaches the model to resist a
phrasing family while the priority contest continues underneath —
which is exactly why many-shot's fine-tuning mitigation *delayed*
rather than defeated (note 45), and why [note 35](../notes/35-obfuscated-gradients.md)'s
obfuscated-gradients lesson generalizes: patching what the attack
looked like is not closing what the attack exploited.

## 3. The evaluation each mode demands

- **Mode 1 evals** must construct *priority conflicts*: benign-framed
  harmful goals, authority-claiming content, many-shot pressure
  ramps. Success metric: the paired ledger — attack suppression AND
  benign compliance (the false-block rate is the mode-1 family's
  signature cost; P07 reports it).
- **Mode 2 evals** must sweep *representation space*: same request,
  many encodings/modalities, coverage measured per domain slice
  ([HELM discipline, note 49](../notes/49-helm.md) — omissions
  named in writing). Success metric: refusal coverage parity
  across slices, with Wilson intervals per slice.

An eval suite that mixes the modes without separating them produces
a single ASR number that tells the operator nothing about which fix
to buy — the difference between a security finding and a demo.

## 4. The falsifiable resolution (deterministic tier)

P07's harness can classify its residuals by mode: run each
successful attack twice — as-originally-framed (does the guard
catch it?) and plainly-restated (would plain refusal catch it?). The
attacks that fail plain-restatement are mode-2-shaped; those that
survive it are mode-1-shaped. Prediction: the guard's six-blocked /
two-residual structure splits by mode (the consent-gap residuals
are mode-1; the encoding residuals mode-2), reproducing note 44's
taxonomy at deterministic tier with the residual *classified*, not
just counted.

## 5. Bottom line

Diagnose with the one-bit probe (plain-restatement test), then buy
the matching family: priority architecture for mode 1, coverage
sweeps for mode 2 — and never quote a mixed-mode ASR as a defense
certification. The modes generate unbounded instances each; the
fixes are structural, and the eval suite's job is to tell them
apart.
