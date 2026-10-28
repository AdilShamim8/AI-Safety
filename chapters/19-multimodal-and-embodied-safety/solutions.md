# Chapter 19 — Solutions and rubrics

**Navigate:** [chapter README](README.md) · [course map](../../SYLLABUS.md) · [all chapters](../README.md)

## Exercise 19.1 — attack-family taxonomy

**Full-credit solution.**

| Family | Attacker knowledge | Carrier legitimacy | Amortization | Correct detection instrument |
|---|---|---|---|---|
| Typographic [SRC-PAPER-088] | none (black-box) | low — rendered text is anomalous in legitimate imagery | per-query (cheap but repeated) | OCR the image and run the *text-side* policy on what the OCR reads |
| Query-relevant content [SRC-PAPER-089] | none | **high — a fully legitimate image** | per-query, zero cost | image-text consistency checking + visual-channel alignment (no artifact exists to filter) |
| Adversarial perturbation [SRC-PAPER-090] | white-box on a same-family model (transfer) | medium — imperceptible noise on a real image | **once — universality** | adversarial-training-style robustness + adaptive re-evaluation (Ch. 12 discipline) |

"Filter suspicious images" is a category error for the *query-relevant*
family: the image is exactly what the user was asked to upload — the
product photo for the listing, the scan for the diagnosis. There is
nothing suspicious to detect; the compromise mechanism is the model's
own content association [SRC-PAPER-089], so the only real controls are
architectural (visual-channel alignment) or consistency-based
(instrument-4-style), not filtration.

**Rubric.** Four attributes correct per family (4 pts); the
category-error family correctly identified as query-relevant with the
mechanism stated (3); the OCR insight for typography (i.e., reduce a
new-modality attack to a solved-modality detector) (2); universality
named as the amortization structure for perturbations (1).

## Exercise 19.2 — the audit's floor

**Full-credit solution.**

(a) Attack arm: 121/200 = 0.605, Wilson 95% **[53.6%, 67.0%]**.
False-refusal floor: 9/200 = 0.045, Wilson **[2.4%, 8.3%]**. The
intervals are disjoint with a gap of 45.3 points between the floor's
upper bound and the attack arm's lower bound — the attack effect is
not explainable by the monitor flagging everything; the measurement
has signal by construction.

(b) When the defense is on, both arms must be re-run under it: the
same 200 attack tasks and the same 200 benign tasks, defense active,
with the *pairing preserved by task id*. The decision rule must be
pre-stated: the defense is adopted only if the attack arm's interval
upper bound falls below a stated threshold *and* the false-refusal
interval's lower bound stays below a stated service ceiling. The
denominators never change silently — 200 and 200, reported again.

(c) A single "net safety" number hides the trade: a trivially "safe"
system refuses everything (attack 0%, refusal 100%). The two rates
are the axes of the operating point, and each has sampling error —
reporting them as a pair *with intervals* is what lets a reviewer see
both the point and its uncertainty. Collapsing them into one number
(e.g., accuracy-like blends) is exactly the construct-laundering
pattern Chapter 02 drills.

**Rubric.** Correct intervals and the disjointness argument (3);
paired re-run design with fixed denominators and pre-stated adoption
rule (3); the refuse-everything degenerate case as the reason for
paired reporting (4).

## Exercise 19.3 — sim-to-real honesty

**Full-credit transfer-assumptions section (skeleton).**

*Perception.* Assumption: the deployed camera distribution at p95
quality matches the audit's degradation envelope (instrument 5's
arm); occlusion patterns and wear states are drawn from the same
family. Control: rolling re-audit against camera-health telemetry.

*Cognition.* Assumption: the VLM's visual-channel behavior in the
warehouse domain matches the moderation-domain audit's — a domain
transfer assumption, explicitly *not* covered by the text-side
red-teaming [SRC-PAPER-088's mechanism]. Control: domain-specific
probe pack.

*Planning.* Assumption: plan stability under adversarial input
matches the digital audit — but planning instability under jailbreak
is a named open fragility [SRC-PAPER-092], so this assumption is
carried as a *weak link*, with plan-level sanity checks on
force/speed/geometry invariants as the independent backstop
(BadRobot's linguistic/physical misalignment [SRC-PAPER-091] is the
failure this catches: the sentence says safe, the trajectory is not).

*Action/interaction.* Assumption: human-robot proximity dynamics in
the audit's staged runs represent production shifts. Control:
geofencing and force limits independent of the model — the
actuator-level controls do not trust the model at all.

*Agentic system.* Assumption: the tool surface and communication
channels match Ch. 14's audited configuration; any new tool re-opens
this section.

*The sentence we refuse to sign:* "The digital audit demonstrates the
robot is safe in the warehouse." What the evidence supports:
"The digital audit bounds the model-level failure modes; physical
safety rests on actuator-level controls that do not depend on the
model being correct."

**Rubric.** All five stages with assumptions and controls (5);
BadRobot's misalignment vulnerability mapped to a trajectory-level
(not text-level) control (3); the refused sentence and its
evidence-supported replacement (2).

## Exercise 19.4 — multimodal case critique

**Full-credit solution.**

(a) Two category errors: (1) *text red-teaming does not transfer to
the visual channel* — the alignment deficiency for visual embeddings
is the attributed mechanism [SRC-PAPER-088], and safety-aligned LLMs
were breached by relevant images in 12 of 12 tested models
[SRC-PAPER-089]; "the underlying LLM passes" certifies the text
distribution only. (2) *"adversarial images" names one family of
three* — the filter's 99% (even if real) says nothing about
typography (different artifact) and *nothing at all* about
query-relevant legitimate images, where there is no adversarial
artifact to block [SRC-PAPER-089].

(b) The 99% claim [against SRC-PAPER-090's family]: it can mean a
static measured blocking rate against a *fixed, non-adaptive*
perturbation set — which the Ch. 12/15 canon (adaptive attacks
defeat static defenses; evaluations that don't re-attack
overestimate) prices as an upper bound at best. It cannot mean
robustness to *adaptive* perturbations, to *transferred universal*
images (one image amortized across instructions), or to the other
two families. And "blocks" must not silently mean "blocks or
refuses" — the false-refusal cost is a separate axis (exercise
19.2).

(c) Minimum audit: the Vantage five-instrument pattern, scoped to
the vendor's domain — (i) typographic probe at n = 200 with (ii) the
benign false-refusal floor at n = 200, both with Wilson intervals;
(iii) query-relevant-image arm at n ≥ 150 (the family the filter
cannot touch); (iv) *adaptive* adversarial arm: the attacker
re-optimizes against the deployed filter (Ch. 12's discipline),
reported as the post-adaptation rate; (v) paired defense measurement
with exact discordant-pair statistics and both arms' costs. Adoption
rule pre-stated. Anything less and the vendor's sentence stays
unsupportable.

**Rubric.** Both category errors with their source attributions (4);
the static-vs-adaptive and universal-transfer pricing of "99%" (3);
the five-arm audit with adaptive re-attack and paired statistics (3).

## Watching pointers for the exercises

The [lecture library](../../courses/README.md) pairs with this
chapter's exercises: watch the listed companions first, and treat any
disagreement between a lecturer's framing and an exercise's rubric as
a finding to note in your solution.

- **CAIS course**, [lecture-02-ai-fundamentals](../../courses/cais-ethics-society/lecture-02-ai-fundamentals.md) — watch before working the brittleness exercises.
