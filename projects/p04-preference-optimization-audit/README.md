# P04 — Preference optimization audit

Status: **implemented** (offline, stdlib-only, deterministic) · Chapter
link: [04](../../chapters/04-preference-learning-and-post-training/README.md)
· Code: `src/ai_safety_course/pref_audit/` · Tests:
`tests/test_pref_audit.py` (8 tests, pinned numbers)

## What this project is

Chapter 04's audit discipline as executable code, on a seeded
synthetic preference corpus (40 items, 200 pairs, logistic labeler
with label noise — the labeler is a *noisy proxy* for quality,
exactly as the chapter frames r_φ):

1. **The BT/DPO machinery**, implemented and numerically checked:
   Bradley-Terry pair loss with the stable log-sigmoid; its gradient
   (finite-difference-verified in tests); the DPO objective on
   synthetic log-ratios; the closed-form KL-constrained optimal
   policy `pi* ∝ exp(r/β)` (the chapter's own derivation).
2. **Instrument 1 — proxy vs held-out.** A logistic reward model is
   fit on the (noisy) preference labels from a noisy feature view of
   true quality; the DPO-optimal policy's *proxy* score is compared
   with its *expected true quality*.
3. **Instrument 2 — the label-bias condition.** The first k% of
   labels are adversarially flipped (concentrated, not diffuse — the
   audit's worst case); the reward model is re-fit; the held-out
   objective's drift is measured.
4. **Instrument 3 — SFT-vs-preference.** The uniform-on-observed
   (SFT-style) policy vs the DPO-optimal policy, on both proxy and
   held-out.

## Pinned results (seed=7, deterministic; recomputed 2026-10-23)

| Quantity | Value |
|---|---|
| Proxy score, DPO policy | 2.9024 |
| Proxy score, SFT policy | 2.8540 (proxy gain **+0.0484**) |
| Held-out true quality, DPO | +0.0093 |
| Held-out true quality, SFT | −0.0687 (held-out gain **+0.0780**) |
| Label-bias 20% flips: held-out | +0.0093 → **−0.0552** (drift **−0.0645**) |

**The headline (the Ch. 04 seam, measured):** the proxy gain
(+0.048) and the held-out gain (+0.078) *diverge by more than either
is large* — knowing the proxy improvement certifies almost nothing
about the true-quality improvement — and under a 20% adversarial
label-bias condition the same pipeline *loses* 6.5 quality points of
held-out true quality while the proxy machinery reports nothing
wrong. The policy optimizes the proxy wherever it can, including
where the proxy is wrong.

## What is honestly NOT here (tier honesty)

- No real model, no real RLHF run: the corpus is synthetic and the
  "policy" is the closed-form optimum — the project is the *audit
  protocol* with correct math, not a training pipeline.
- The labeler's noise model is logistic-on-quality-difference; real
  labeler bias structures (annotator populations, order effects) are
  Ch. 04's §6 material, not modeled here.
- The reward model is 1-D logistic on a noisy feature — deliberately
  minimal so every number is explainable; richer features change the
  magnitudes, not the audit's logic.

## Run it

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from ai_safety_course.pref_audit import *
data = make_preference_data(seed=7)
res = run_audit(data, beta=1.0)
bias = label_bias_condition(data, flip_fraction=0.2)
print(f'proxy gain {res.proxy_dpo - res.proxy_sft:+.4f}')
print(f'held-out gain {res.heldout_dpo - res.heldout_sft:+.4f}')
print(f'label-bias drift {bias.drift:+.4f}')
"
```

Every number above is pinned in `tests/test_pref_audit.py`; the
deterministic fixture makes regressions visible.
