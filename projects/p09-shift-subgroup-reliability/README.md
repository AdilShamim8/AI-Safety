# P09 — Distribution shift and subgroup reliability

Status: **implemented** (offline, stdlib-only, deterministic) ·
Chapter link:
[17](../../chapters/17-distribution-shift-and-deployment-reliability/README.md)
· Code: `src/ai_safety_course/shift_audit/` · Tests:
`tests/test_shift_audit.py` (6 tests, pinned numbers)


**Session-2 companion materials:** [lost in the middle](../../research/notes/39-lost-in-the-middle.md) (position subgroups), [inverse scaling](../../research/notes/48-inverse-scaling.md) (upgrade drift), [underspecification](../../research/notes/66-underspecification.md) (the mechanism your slices expose), [FEVER](../../datasets/cards/33-fever.md)/[Civil Comments](../../datasets/cards/41-civil-comments.md)/[HateXplain](../../datasets/cards/35-hatexplain.md) (slice sources), [incidents 13](../../research/notes/incidents/13-eeoc-itutorgroup.md)/[14](../../research/notes/incidents/14-amazon-recruiting-tool.md) (the subgroup audit that would have caught them).
## What this project is

Chapter 17's audit discipline as executable code on a seeded
synthetic deployment with a *group structure and a spurious
correlation that flips under shift*:

- two groups with different base rates **and different core-signal
  noise** (group 0's core signal is weaker, so ID training leans
  harder on the spurious feature for group 0 — the worst-group
  setup);
- the spurious feature x2 correlates with the label in-distribution
  and **anti-correlates** in the OOD slice (the flip that breaks
  classifiers that leaned on it);
- a 2-feature logistic classifier fit on ID, evaluated ID/OOD/per
  group with Wilson intervals;
- binned ECE for calibration under shift;
- one mitigation — group-cost reweighting (DRO-*lite*) — and the
  honest result.

## Pinned results (seed=11, deterministic; recomputed 2026-10-23)

| Instrument | Result |
|---|---|
| ID accuracy | 0.899 [0.879, 0.916] |
| OOD accuracy | **0.674 [0.632, 0.714]** — a 22.5-point drop; disjoint intervals |
| ID groups | g0 0.840 [0.805, 0.870] vs g1 0.958 [0.937, 0.972] — the 0.899 aggregate hides both tails |
| OOD worst-group | **0.612** vs average-group 0.674 (gap 6.2 points) |
| ECE | ID 0.039 → OOD **0.115** (calibration degrades with accuracy — Ch. 17's station 4) |
| Mitigated (DRO-lite) OOD worst | **0.608** — *no better than unmitigated* (0.612), and the average drops to 0.652 |

**The headline:** the shift drop is real (disjoint intervals), the
group structure survives the aggregate, calibration degrades with
accuracy — and the half-recipe mitigation **fails honestly**: group
reweighting fit on ID groups does not transfer across the shift,
which is exactly the GroupDRO coupling caveat Ch. 17 prices ("the
recipe is DRO *plus* regularization; reproducing half of it is the
documented failure mode"). The project reproduces the half-recipe's
failure as a pinned, deterministic artifact.

## What is honestly NOT here

- No licensed public dataset is re-distributed: the shift mechanism
  (spurious flip + group noise) is synthetic precisely so every
  number is explainable; the dataset cards' real-world composition
  anchors the *discipline*, this code anchors the *arithmetic*.
- The mitigation is deliberately the half-recipe — implementing full
  GroupDRO with the regularization coupling is the student exercise
  the pinned failure motivates.
- One shift type (spurious flip); the taxonomy's other classes
  (label shift, concept shift) are exercise extensions.

## Run it

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from ai_safety_course.shift_audit import run_shift_audit
r = run_shift_audit(seed=11)
print(f'ID {r.id_acc:.3f} vs OOD {r.ood_acc:.3f}')
print(f'worst-group {r.worst_group:.3f}; ECE {r.ece_id:.3f} -> {r.ece_ood:.3f}')
print(f'DRO-lite mitigated worst: {r.mitigated_worst:.3f} (the half-recipe fails)')
"
```
