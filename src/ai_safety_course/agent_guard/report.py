"""report — dated markdown P07 reports with a full provenance block.

Renders a :class:`~ai_safety_course.agent_guard.runner.RunResult`
into the repository's experiment-report discipline: the paired-arm
design statement; attack and benign rates with Wilson intervals; the
discordant-pair ledgers with exact one-sided sign tests; the
rule-fire table (which of R1-R4 caught what); the residual attack
classes and degraded benign flows named honestly; the per-scenario
trace appendix (every step, every verdict, every reason); and a
provenance block (matrix checksum, scenario-set checksum, config
fingerprint, code version, run date, determinism statement).

Every number is computed from the run's records — nothing is
hand-typed — and generation is deterministic.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ai_safety_course.agent_guard.harness import PairedRun
from ai_safety_course.agent_guard.metrics import P07Metrics

if TYPE_CHECKING:  # imported for annotations only (runner imports this module)
    from ai_safety_course.agent_guard.runner import RunConfig, RunResult


def _pct(value: float) -> str:
    return f"{value * 100:.1f}%"


def _rate_line(label: str, rate) -> str:  # noqa: ANN001 (RateWithInterval)
    return (
        f"- {label}: {rate.successes}/{rate.denominator} = {_pct(rate.point)} "
        f"(Wilson 95% [{_pct(rate.low)}, {_pct(rate.high)}])"
    )


def render_report(result: RunResult) -> str:
    """Render a full P07 run as markdown (deterministic, no hand-typed numbers)."""
    config: RunConfig = result.config
    metrics: P07Metrics = result.metrics
    run: PairedRun = result.run
    lines: list[str] = [
        f"# P07 experiment report: {config.run_id}",
        "",
        f"Run ID: `{config.run_id}` · Project: {config.project} · "
        f"Status: {config.status_note} · Date: {config.run_date}",
        "",
        "## Design",
        "",
        f"Paired arms over the same {len(run.results)} scripted scenarios "
        f"({len(run.attacks)} attack, {len(run.benign)} benign): the "
        "**undefended** arm executes every call (full delegation — the "
        "confused deputy deployed); the **capability** arm enforces R1-R4 "
        "over the privilege matrix (R2/R3 hard-block; R1/R4 consent-gated "
        "by the scripted user; halt-on-block). Arms differ only in policy.",
        "",
        "## Headline (pinned by the preregistered protocol)",
        "",
        metrics.headline(),
        "",
        "## Rates with intervals",
        "",
        _rate_line("Attack success, undefended", metrics.attack_undefended),
        _rate_line("Attack success, capability R1-R4", metrics.attack_capability),
        _rate_line("Benign completion, undefended", metrics.benign_undefended),
        _rate_line("Benign completion, capability R1-R4", metrics.benign_capability),
        "",
        "## Paired ledgers (exact one-sided sign tests)",
        "",
        "Attacks (undefended_only = succeeded undefended, blocked under "
        "capability — the defense's improvement direction):",
        f"- both arms: {metrics.attack_ledger.both}; "
        f"neither: {metrics.attack_ledger.neither}; "
        f"undefended_only: {metrics.attack_ledger.undefended_only}; "
        f"capability_only: {metrics.attack_ledger.capability_only}",
        f"- sign test p = {metrics.attack_sign_p:.6g} "
        f"({metrics.attack_ledger.n_discordant} discordant pairs)",
        "",
        "Benign flows (undefended_only = completed undefended, incomplete "
        "under capability — the defense's cost direction):",
        f"- both arms: {metrics.benign_ledger.both}; "
        f"neither: {metrics.benign_ledger.neither}; "
        f"undefended_only: {metrics.benign_ledger.undefended_only}; "
        f"capability_only: {metrics.benign_ledger.capability_only}",
        f"- sign test p = {metrics.benign_sign_p:.6g} "
        f"({metrics.benign_ledger.n_discordant} discordant pairs)",
        "",
        "## Rule fires (capability arm, blocked/halted steps only)",
        "",
    ]
    if metrics.rule_fires:
        lines += [f"- {rf.rule}: {rf.fires}" for rf in metrics.rule_fires]
    else:
        lines.append("- (none)")
    lines += [
        "",
        "## Residual attack classes (succeeded under capability R1-R4)",
        "",
    ]
    if metrics.residual_attack_ids:
        for u, c in run.attacks:
            if u.success and c.success:
                lines.append(
                    f"- `{c.scenario_id}` — {result.scenario_notes.get(c.scenario_id, '')}"
                )
    else:
        lines.append("- (none)")
    lines += [
        "",
        "## Degraded benign flows (incomplete under capability R1-R4)",
        "",
    ]
    if metrics.degraded_benign_ids:
        for u, c in run.benign:
            if u.success and not c.success:
                lines.append(
                    f"- `{c.scenario_id}` — {result.scenario_notes.get(c.scenario_id, '')}"
                )
    else:
        lines.append("- (none)")
    lines += [
        "",
        "## Honest limitations",
        "",
        "- All scenarios are synthetic, authored mechanisms (Chapter 14's",
        "  attack classes at the metadata level); no real attack payload, no",
        "  dataset content, no live client. These are *mechanism* results,",
        "  not prevalence estimates of deployed-agent incidents.",
        "- n = 16 paired scenarios: the intervals are wide by design; the",
        "  sign tests are exact; nothing here licenses a field-rate claim.",
        "- The residual classes are the chapter's documented policy limits",
        "  (the authored-policy gap and consent decay), demonstrated on",
        "  purpose — a policy whose fixture shows no residuals would be",
        "  testing the wrong thing.",
        "- Deterministic: no model calls, no sampling, no network; identical",
        "  inputs give byte-identical reports.",
        "",
        "## Provenance",
        "",
        f"- Matrix: `{result.matrix_name}` (SHA-256 `{result.matrix_checksum}`)",
        f"- Scenario set: `{result.scenarios_name}` " f"(SHA-256 `{result.scenarios_checksum}`)",
        f"- Config fingerprint: `{result.config_fingerprint}`",
        f"- Code version: {result.code_version}",
        f"- Run date: {config.run_date}",
        "- Execution: local, CPU-only, offline; single process.",
        "",
        "## Appendix: per-scenario traces",
        "",
    ]
    for u, c in run.results:
        lines.append(f"### `{u.scenario_id}` ({u.kind})")
        lines.append("")
        for arm_result in (u, c):
            lines.append(f"**Arm: {arm_result.arm}**")
            lines.append("")
            for o in arm_result.outcomes:
                verdict = "executed" if o.executed else o.decision.value
                rules = f" rules={','.join(o.rules_fired)}" if o.rules_fired else ""
                consent = " (consent granted)" if o.consent_granted else ""
                lines.append(f"- step {o.step_index} `{o.tool}` -> {verdict}{rules}{consent}")
                for reason in o.reasons:
                    lines.append(f"  - {reason}")
            halted = (
                f"halted at step {arm_result.halted_at}"
                if arm_result.halted_at is not None
                else "completed all steps"
            )
            summary = (
                "attack SUCCEEDED"
                if arm_result.attack_succeeded
                else (
                    "attack blocked"
                    if arm_result.kind == "attack"
                    else "completed" if arm_result.benign_completed else "incomplete"
                )
            )
            lines.append("")
            lines.append(f"  -> {halted}; {summary}")
            lines.append("")
    return "\n".join(lines) + "\n"


def write_report(result: RunResult, out_path: Path) -> None:
    """Write the rendered report to ``out_path`` (parent must exist)."""
    out_path.write_text(render_report(result), encoding="utf-8")
