# Experiment-report template

Every project experiment produces exactly one report from this template.
The report's numbers must be computed by a committed script from recorded
per-case outputs — never hand-typed. Status labels are defined in
`planning/BUILD_PLAN.md` and must match reality.

```markdown
# Experiment report: <project/run title>
Run ID: <id> · Project: <P-id> · Status: protocol-only | implemented |
smoke-tested | experiment-executed · Date: <date>

## Question and hypotheses
The falsifiable question, the hypothesis, and the pre-stated criterion that
would count as evidence AGAINST it. If this report is exploratory rather
than confirmatory, say so and date both the protocol and this report.

## Protocol
- Design: conditions, splits (train/dev/test roles, grouping), seeds,
  stopping rules.
- Baselines and ablations: the baseline you beat-or-explain, and the
  ablation that isolates the mechanism you claim.
- Benign controls: how you measure the cost of any safety mechanism.

## Provenance
Model ID + revision · dataset + revision + license · configuration hash ·
code commit (the revision actually executed) · environment (Python,
package versions, OS, hardware) · seed · timestamps · known
nondeterminism sources.

## Results
- The summary table, computed by scripts/<name>.py from results/ per-case
  outputs (include the command).
- Numerators WITH denominators (n, skipped, invalid) for every rate.
- Uncertainty that respects the sampling unit (which unit, which method,
  how many units).
- Effect sizes and paired/cluster structure where applicable.

## Error analysis
Where it failed, stratified by condition/case group; the interesting
failures, not just the aggregate. Include at least one concrete failure
case (sanitized).

## Interpretation
What the evidence supports, what it does not, and the difference between
the two lists. Separate confirmatory conclusions from exploratory
observations.

## Deviations
Everything that deviated from the protocol, with reasons. A clean report
with a hidden deviation is a fabrication.

## Reproduction
Exact commands (smoke / pilot / full tiers), expected runtime, RAM/VRAM,
download sizes — measured or estimated, labeled which.
```

The result schema (per-case rows) lives in each project's code:
`run_id, project_id, case_id, case_group_id, split, seed, model_id,
model_revision, dataset_revision, configuration_hash, code_commit,
condition, metric_name, metric_value, judge_id, judge_revision, error_type,
duration_seconds, estimated_or_actual_cost, execution_status, timestamp`.
