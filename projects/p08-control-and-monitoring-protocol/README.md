# P08 — Control and monitoring protocol

Status: **implemented** (offline, stdlib-only, deterministic) ·
Chapter link:
[08](../../chapters/08-ai-control-and-monitoring/README.md) · Code:
`src/ai_safety_course/control_protocol/` · Tests:
`tests/test_control_protocol.py` (6 tests, pinned numbers)


**Session-2 companion materials:** [unfaithful CoT](../../research/notes/38-unfaithful-explanations.md)/[measuring faithfulness](../../research/notes/43-measuring-cot-faithfulness.md) (your monitor-validation items), [the off-switch game](../../research/notes/63-off-switch-game.md) (halt semantics' formal ancestor), [incident 11](../../research/notes/incidents/11-bing-sydney-persona-collapse.md) (the drift tripwire's case), [C11](../../research/notes/comparison-11-situational-awareness-vs-persona-drift.md).
## What this project is

Chapter 08's control setting in miniature: an untrusted policy
executes tasks (200 benign + 60 attacks); an external monitor with
**70% recall / 10% false-flag rate** flags suspicious outputs; three
protocols route the work differently, evaluated on **paired trials**
(identical flagging across protocols — fresh same-seeded monitors):

1. **no_monitor** — untrusted output used directly;
2. **simple_monitor** — flagged outputs halt;
3. **defer_to_trusted** — flagged tasks route to a trusted policy
   that catches every routed attack, completes 95% of routed benign
   tasks, and spends the audit budget per execution.

## Pinned results (seed=9, deterministic; recomputed 2026-10-23)

| Protocol | Safety (attacks blocked) | Usefulness (benign completed) | Trusted executions |
|---|---|---|---|
| no_monitor | 0.000 [0.000, 0.060] | 1.000 | 0 |
| simple_monitor | 0.717 [0.592, 0.815] | 0.910 [0.862, 0.942] | 0 |
| defer_to_trusted | 0.717 [0.592, 0.815] | **1.000** [0.981, 1.000] | **61** |

**The headline (the frontier, honestly read):** both monitor-bearing
protocols share the *same* safety — 17/60 violations, safety 0.717 —
because the **monitor's recall is the safety ceiling**: the 17
attacks it never flagged execute under every protocol, and no
downstream routing can block what was never seen. What defer buys is
**usefulness** (1.000 vs 0.910 — the false-flagged benign tasks
complete under trusted execution), at the price of **61 trusted
executions** (the audit budget — Ch. 08's trusted-labor arithmetic:
61/260 ≈ 23% of throughput routed to the expensive path). The
identical safety intervals across protocols are the paired-design
fact that makes the ceiling visible.

## What is honestly NOT here

- The "policies" are scripted tables, not models: the project
  measures the *protocol arithmetic* (recall ceilings, usefulness
  costs, budget consumption), not monitor quality.
- Collusion (the untrusted model deliberately evading the monitor)
  is Ch. 08's adaptive-attack extension, not modeled here — the
  monitor's 70% recall is given, not adversarially earned.
- The trusted policy's 100% attack-catch is the control setting's
  *definition* of trusted, priced only through its benign-failure
  rate and budget cost.

## Run it

```bash
python -c "
import sys; sys.path.insert(0, 'src')
from ai_safety_course.control_protocol import frontier
for r in frontier(seed=9):
    print(f'{r.name:18} safety {r.safety:.3f} usefulness {r.usefulness:.3f} trusted {r.trusted_executions}')
"
```
