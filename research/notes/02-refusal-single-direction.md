# Note: Refusal in Language Models Is Mediated by a Single Direction (2024)

Source: SRC-PAPER-037 · Access: full-text-read (arXiv v3 HTML, 132k
chars, spot-verified programmatically) · Read: 2026-10-21 · Note
level: **method-level**.

## The actual problem

The authors' framing: refusal behavior in instruction-tuned LLMs —
whether the model declines harmful requests — might be implemented as
a *linear* circuit component: one direction in activation space whose
removal disables refusal and whose addition induces it. The operational
version: if refusal is mediated by a single direction, then (a) jail-
breaking has a mechanistic account (attacks move activations off the
refusal direction), (b) ablation of the direction gives a controlled
"no-refusal" model for safety research, and (c) defense could in
principle strengthen the direction rather than patch behaviors one by
one.

## Method

Direction extraction: **difference-in-means** — run the model over a
set of harmful prompts and a matched set of benign prompts, take the
mean activation difference per layer per position, and use that vector
(r̂) as the candidate refusal direction. (The chapter-11 discipline:
this is the *cheapest* extraction — a trained probe's hyperplane
normal is a different object, and cosine < 1 always.)

The two interventions, symmetric by design:

- **Directional ablation** (remove refusal): project the direction out
  of every activation at every layer and position —
  x ← x − r̂(r̂·x) — and generate. Refusal disappears while other
  capabilities (the paper's coherence battery: MMLU/ARC/GSM8K/
  TruthfulQA-style task performance) are measured for collateral
  damage.
- **Direction addition** (induce refusal): add α·r̂ at chosen sites;
  benign requests start being refused — the converse experiment that
  makes the "mediates" claim bidirectional.

The **substring refusal classifier**: a practical probe built from the
direction's readout, used to score attack success in the ASR
comparisons. The ablation competes with optimization-class attacks
(GCG/PAIR-family): orthogonalizing activations against r̂ at
generation time versus adversarially optimized attack suffixes —
including the crucial with-and-without-system-prompt contrast (e.g.
Llama-2 7B GCG-M: 22.6% ASR with the model's default system prompt vs
79.9% without — the several-fold effect of dropping the safety-
oriented prompt, specific to the evaluated models and suite).

The clever part: the bidirectional intervention pair (ablation AND
addition from the same direction) is what upgrades "found a correlate"
to "found a mediator candidate" — one direction doing both jobs is the
strongest single-number evidence linear mediation can give. The
fragile part: difference-in-means over curated English single-turn
instruction distributions — the direction is whatever those two prompt
sets differ in, which is "refusal-related stuff," not necessarily
"refusal and only refusal."

## Central evidence

- Ablation disables refusal across the evaluated models while the
  coherence battery stays largely intact — the collateral-damage
  measurement is the difference between "we broke the model" and "we
  removed a behavior."
- Addition induces refusal on benign inputs — the bidirectional leg.
- The ASR table: direction orthogonalization competes with
  optimization-class attacks, and the system-prompt contrast (22.6% vs
  79.9% for the Llama-2 7B GCG-M row) shows the model's default
  prompt carrying a large share of what the attack must overcome.
- Directions are model-specific — the released directions are
  per-model artifacts, and cross-model transfer is not the claim.

What the evidence does NOT carry: no claim that the direction is THE
refusal feature (it is a mediator candidate under the evaluated
distributions — Chapter 11's A2 assumption row prices exactly this);
no multilingual or multi-turn coverage (curated English single-turn);
no claim that "single direction" means "single feature" (superposition
means a direction can be a mixture — Chapter 10's dictionary-
relativity lesson).

## Assumptions

Tested in-paper: the intervention pair's symmetry (both directions of
the effect); collateral capability (the coherence battery); the attack-
suite comparison (with/without system prompt).

Inherited: prompt-set representativeness (the direction is only as
"refusal" as the harmful/benign split is clean); linearity of the
mediation (the intervention is linear by construction, so non-linear
mediators would be invisible); single-turn English coverage; the
attack suite's strength at the evaluated budget (Chapter 12's adaptive
rule — the ASR numbers are against the attacks tried).

## Limitations

Authors' stated (fairly represented): curated English single-turn
instruction distributions; model-specific directions; the several-fold
ASR multiplication from dropping the system prompt is specific to the
evaluated models and attack suite.

Ones I see that they do not foreground: the difference-in-means
extraction bakes the prompt-set contrast into the direction — any
systematic difference between the two prompt sets (topic, register,
length) rides along, and the paper's own controls (the chapter-11
random-patch and matched-topic controls discipline) bound but do not
eliminate this; "coherence battery intact" is measured at task level,
not at distribution level (rare-context degradation — the Chapter 10
lesson that reconstruction metrics miss structured error — applies to
capability preservation too).

## Nearest alternatives

- **Contrastive activation addition (CAA)** and prompt-pair steering
  (Chapter 11's recipe family): extract directions from prompt pairs
  and add at generation; same linear-intervention logic, weaker
  bidirectional evidence, broader behavior coverage.
- **Probing-only work (logistic probes for refusal-relevant info)**:
  shows the information is present; without the intervention leg it
  cannot distinguish mediator from correlate — this paper's ablation
  leg is precisely the upgrade.
- **GCG-class optimization attacks (SRC-PAPER-004)**: the adversary
  side of the same coin — the ASR comparison makes the paper partly a
  defense evaluation, and the system-prompt contrast shows attack
  numbers are prompt-context-conditioned (a generalization the
  jailbreak literature often leaves implicit).

## Replication feasibility

High at course scale — this is why Chapter 11's worked example is
built on it. Needs: a locally hosted open model (the `ml` tier), an
authored harmful/benign prompt pair set (metadata-level design, the
course's no-redistribution discipline), hooks for activation capture
and intervention (TransformerLens-class tooling), and a coherence
battery (licensed eval subsets). What breaks first: the ASR
comparisons need an attack implementation (compute and care), but the
core bidirectional mediation result — extract, ablate, add, measure —
is a weekend-scale project at 7B with the chapter's evaluation
discipline attached.

## Falsifiable extension

Hypothesis: the refusal direction extracted from a single-turn English
pair set fails to mediate refusal on multi-turn escalated conversations
— the "single direction" claim is distribution-conditioned. Design:
extract r̂ per the paper; measure refusal rate on (a) the paper-style
single-turn set and (b) an authored multi-turn escalation set, under
identity, ablation, and addition; report the mediation symmetry factor
(addition-induced refusal minus baseline) per condition with Wilson
intervals. Baseline: the paper's single-turn numbers. Stopping rule:
one condition pair per run; three escalation depths. What counts
against: if mediation symmetry holds at all depths, the single-
direction claim generalizes beyond its extraction distribution — and
my distribution-conditioning premise fails.

## My interpretation vs. their claims

Their claims: (1) refusal is mediated by a single direction in the
evaluated models — bidirectional intervention evidence; (2) the
direction enables both a controlled no-refusal research model and an
orthogonalization defense that competes with optimization attacks; (3)
directions are model-specific and the results are conditioned on the
evaluated distributions.

My interpretation: (1) the bidirectional intervention pair is the
paper's real methodological contribution — it is the minimal evidence
standard that separates mediator claims from probe-accuracy claims,
and the course adopts it as such (Chapter 11's three-ledger frame);
(2) the defense framing deserves more caution than it gets in
downstream citation: orthogonalization competes with the attacks tried
at the budget tried — the Chapter 12 adaptive rule applies unchanged,
and a direction-aware adversary is the obvious next red team; (3) the
system-prompt contrast (22.6 vs 79.9) is quietly one of the paper's
most deployment-relevant numbers — it quantifies how much safety the
prompt layer was carrying, which is exactly the layer Chapter 13 says
cannot carry security; (4) "single direction" is a claim about the
mediation the interventions can see — superposition (Chapter 10)
guarantees that a one-direction account is at best a projection of a
richer feature structure, and the paper is careful in ways its
citation graph is not.
