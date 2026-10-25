# P05 — Weak-to-strong / scalable-oversight analogue

Status: **implemented** (offline, stdlib-only, deterministic) ·
Chapter link:
[05](../../chapters/05-scalable-oversight/README.md)
· Code: `src/ai_safety_course/w2s_audit/` · Tests:
`tests/test_w2s_audit.py` (7 tests, pinned numbers)


**Session-2 companion materials:** [CIRL](../../research/notes/62-cirl-assistance-games.md) (the formal frame of your grader's situation), [the off-switch game](../../research/notes/63-off-switch-game.md) (deference from held uncertainty), [situational awareness](../../research/notes/40-taken-out-of-context.md) (the transfer arm).
## What this project is

Chapter 05's scalable-oversight question as a minimal, fully
inspectable analogue: a **weak supervisor** labels training data with
i.i.d. flips at rate 30% (its limitation); a **strong learner** (a
linear logistic model on the raw 2-D features) trains *only* on the
weak labels; the **ground-truth upper reference** (the true, mildly
nonlinear boundary — invariant across the deployment) scores
everything. The measured quantity is the **oversight gap recovered**:
does the learner exceed the supervisor whose labels it learned from,
and does the recovery survive pure covariate shift?

## Pinned results (seed=5, deterministic; recomputed 2026-10-23)

| Instrument | Result |
|---|---|
| Weak supervisor, ID | 0.708 [0.661, 0.750] (≈ 1 − flip rate) |
| Strong learner (trained on weak labels), ID | **0.963 [0.939, 0.977]** |
| **Oversight gap recovered** | **+0.255** — disjoint intervals |
| Strong learner, OOD (covariate shift) | **0.975 [0.955, 0.986]** — the recovery *persists* |
| Weak supervisor, OOD | 0.677 |

**The headline (the weak-to-strong effect, demonstrated):** a learner
trained *only* on labels that are 30%-corrupted still reaches 96.3%
— **25.5 points above its supervisor** — because i.i.d. supervisor
errors are noise a higher-capacity learner can average out, and the
learner ends up approximating the *invariant* boundary rather than
the supervisor's noise. That is also why the recovery survives the
covariate shift (0.975 OOD): the boundary did not move, so the
learned approximation did not break.

## Small-analogue scope statement (the required honesty)

Real weak supervisors make *systematic* errors — annotator biases,
blind spots, worldview distortions — which are **not** i.i.d. and
**do not** average out; this analogue models the mechanism in its
cleanest form (i.i.d. noise + capacity) precisely so the effect and
its boundary conditions are visible. The correct reading: weak-to-
strong generalization is *possible* when supervisor errors are
noise-like relative to the learner's capacity; it is *not* a
guarantee about real oversight, where the error structure is the
question. The learner's 0.963 is also honestly below the Bayes rate
of a perfectly-informed nonlinear learner (the boundary is mildly
nonlinear; the linear learner has a real ceiling).

## Run it

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from ai_safety_course.w2s_audit import run_w2s
r = run_w2s(seed=5)
print(f'weak {r.weak_acc_id:.3f} vs strong {r.strong_acc_id:.3f}')
print(f'gap recovered {r.oversight_gap_recovered:+.3f}')
print(f'OOD: strong {r.strong_acc_ood:.3f} (recovery persists)')
"
```
