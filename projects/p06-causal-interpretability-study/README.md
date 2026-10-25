# P06 — Causal interpretability study

Status: **implemented** (offline, stdlib-only, deterministic) ·
Chapter links:
[09](../../chapters/09-mechanistic-interpretability-foundations/README.md),
[10](../../chapters/10-sparse-features-circuits-and-interpretability-evaluation/README.md),
[11](../../chapters/11-behavioral-steering-and-representation-interventions/README.md) · Code:
`src/ai_safety_course/patch_audit/` · Tests: `tests/test_patch_audit.py`
(14 tests, pinned numbers)


**Session-2 companion materials:** [Othello-GPT](../../research/notes/34-emergent-world-representations.md) (the probe-plus-intervention pattern your battery implements), [induction heads](../../research/notes/50-induction-heads.md) (the six-argument ladder), [ROME](../../research/notes/52-rome-factual-associations.md) (the weight-tier edit your rank-one extension mirrors), [CounterFact card](../../datasets/cards/31-counterfact-rome.md).
## What this project is

The causal-interpretability discipline of Chapters 09–11 as executable
code on a deterministic two-branch "model organism" with known ground
truth:

- three input channels — a noisy **core** signal (sign agreement with the
  label ≈ 82%), a clean **spurious** signal (90% agreement
  in-distribution), and a label-independent **topic** nuisance;
- four sites — `s0` embedding, parallel branches `s1` (core path) and
  `s2` (spurious path, with a 3% cross-leak), and `s3` mixer;
- a logistic readout fit on in-distribution `s3` activations — which
  demonstrably leans on the **clean spurious** channel more than the
  noisy core channel (the shortcut-learning setup of Ch. 03/17).

The audit then answers a vendor-shaped claim — *"the model's behavior
lives in the s2/b circuit; our probe reads it out better, our patching
restores it, locality confirms it"* — with the full instrument battery:
two corruption contrasts (label-flip and b-isolate, both topic-matched),
per-site restoration in gap form and decision form with Wilson
intervals, exact one-sided binomial tests with Holm-Bonferroni
correction over the site grid, random-patch and matched-magnitude
controls, and the deployment-flip **intervention** that settles the
question.

## Pinned results (seed=11, deterministic; recomputed 2026-10-25)

| Instrument | Result |
|---|---|
| Readout weights (a, b) | w_a = 2.247 < w_b = 2.661 — **the shortcut is learned** |
| Linear probes on held-out | s1 (core) **0.825** vs s2 (spurious) **0.915** — the probe favors the spurious site |
| C1 label-flip grid | s0 166/166 and s3 166/166 restored (the **trivial band** — ends of the flow localize nothing); s1 (core site) **0/166 restored**, gap-R only 0.194; s2 **166/166 restored**, gap-R 0.806, Holm p ≈ 4.3e-50 |
| C2 b-isolate grid | window exactly at s2 (200/200, gap-R 0.991); s1 0/200, gap-R 0.009 — locality confirmed |
| Random / matched controls at s1 | **0/166** and **1/166** — nothing restores at the core site, clean donor included |
| Random / matched controls at s2 | 53/166 and 20/166 — the clean-donor patch (166/166) sits far outside its own control band |
| Deployment-flip slice | accuracy **0.335** [0.273, 0.403] — the b-reliant model collapses |
| b-ablation on flip slice | **0.770** [0.707, 0.823] — disjoint from the collapse; paired McNemar 102 vs 15, exact p = 2.2e-17 |
| b-ablation in-distribution | 0.805 vs 0.915 with b — **the two-sided ledger**: the same circuit helps in-distribution and breaks under flip |

**The headline:** every instrument the vendor cites is *correctly
executed* — the probe does read better at s2, patching s2 does restore
every decision under the label-flip contrast, and locality does hold
under b-isolate — and the conclusion is still wrong. The label-flip grid
shows why: restoring the **true** channel (s1) restores *zero* decisions
(0/166) because the patching grid measures the model's *reliance
structure*, not the information's truth-value. What s2 carries is a
shortcut: the deployment-flip intervention (ablating b recovers 43.5
points, McNemar p = 2.2e-17) demonstrates causally that the s2 reliance
is a deployment liability, while the s1 path alone sustains 0.770 — the
a-only ceiling. Probe readout is not causation (Ch. 11); restoration is
not information (Ch. 09); and only an intervention under distribution
shift separates reliance from behavior.

The gap-form vs decision-form divergence at s2 (0.806 vs 1.000) is
itself a pinned lesson: the two restoration forms answer different
questions, and reporting only one of them is how patching tables get
oversold.

## What is honestly NOT here

- **No real open model.** The compute tier (a small open model with
  TransformerLens-style hooking, real refusal-direction patching per the
  Ch. 09 exercise protocol) is scoped in the chapter and honestly marked
  not-executed; this organism is deterministic precisely so every number
  above is explainable line-by-line.
- **No licensed public dataset is re-distributed.** The dataset cards'
  real-world compositions anchor the *discipline*; this code anchors the
  *arithmetic* of contrasts, controls, intervals, and multiplicity.
- **Two branches, one readout head.** Multi-head organisms, feature
  splitting (Ch. 10), and dictionary-learning confounds are exercise
  extensions; the cross-leak here is a fixed 3%, not a learned
  superposition.
- The b-isolate contrast flips 200/200 decisions — the causal window is
  the *entire* behavior for this organism. A less shortcut-reliant
  readout would show partial windows; parameter-sweeping that is the
  follow-up exercise.

## Run it

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from ai_safety_course.patch_audit import run_patch_audit
r = run_patch_audit(seed=11)
print(f'shortcut learned: {r.shortcut_learned} (w_a={r.readout.w[0]:.3f} < w_b={r.readout.w[1]:.3f})')
print(f'probes: s1(core) {r.probe_s1:.3f} vs s2(spurious) {r.probe_s2:.3f}')
print(f'C1 restore: s1(core) {r.c1[\"s1\"].k}/{r.c1[\"s1\"].n}  s2(spurious) {r.c1[\"s2\"].k}/{r.c1[\"s2\"].n}')
print(f'flip slice {r.flip_acc:.3f} -> ablated {r.flip_ablated_acc:.3f} (McNemar p={r.flip_mcnemar_p:.1e})')
"
```

## Protocol registration

H1 (vendor claim): "the s2/b circuit carries the model's behavior."
Falsifier: the deployment-flip intervention — if ablating b on the flip
slice recovers accuracy toward the a-only ceiling with a paired
significance test, the b-circuit's causal role is *shortcut*, not
*behavior*, and H1 is rejected regardless of probe and patching evidence.
H2 (locality): the b-isolate contrast window sits at s2 and not at s1.
H3 (trivial band): patching s0 or s3 restores ≥ the informative sites,
localizing nothing. Stopping rule: all three pre-registered comparisons
pinned at seed=11 with controls; disconfirming criterion for H2 would be
a C2 window ≥ 5% at s1 (observed: 0/200).
