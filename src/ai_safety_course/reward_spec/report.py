"""report — dated markdown experiment reports with a provenance block.

Renders a :class:`~ai_safety_course.reward_spec.runner.RunResult` into
the repository's experiment-report discipline as markdown: the construct
and gap sentence from the environment's own construct notes; the
pressure-ladder table pairing the proxy-optimized primary against the
intended-optimized control at matched pressure; preregistered gate
verdicts judged by interval bounds; the side-effect ledger comparison
(the damage the proxy cannot price); episode-paired primary-vs-control
comparisons; the held-out divergence series; the revised-proxy readout
when the environment provides one; an honest-limitations section
(saturated ladder points, small denominators); and a full provenance
block (config checksum, environment and optimizer identity, seed, code
version, run date).

Every number in the generated report is computed from the run's cell
records — nothing is hand-typed — and generation is deterministic: the
same ``RunResult`` always renders the same text.
"""

from pathlib import Path

from ai_safety_course.reward_spec.runner import RunResult

_Z_NOTE = "Wilson 95% intervals at z = 1.959963984540054 (full precision)."


def _fmt(value: float, digits: int = 3) -> str:
    """Fixed-width float formatting (negative zero normalized)."""
    text = f"{value:.{digits}f}"
    if text.startswith("-") and float(text) == 0.0:
        return text[1:]
    return text


def _pct(value: float, digits: int = 1) -> str:
    """Format a proportion [0, 1] as a percentage (the % spec scales by 100)."""
    return f"{value:.{digits}%}"


def _pct_interval(lower: float, upper: float, digits: int = 1) -> str:
    return f"[{_pct(lower, digits)}, {_pct(upper, digits)}]"


def _escape(text: str) -> str:
    return text.replace("|", "\\|").replace("\n", " ")


def _header(result: RunResult) -> list[str]:
    status = result.config.status_note or "implemented"
    return [
        f"# P02 experiment report: {result.config.run_id}",
        "",
        f"Run ID: `{result.config.run_id}` · Project: {result.config.project} · "
        f"Status: {status} · Date: {result.config.run_date}",
        "",
    ]


def _construct_section(result: RunResult) -> list[str]:
    lines = ["## Construct and measures", ""]
    lines.extend(f"- {note}" for note in result.construct_notes)
    lines.extend(
        [
            "- Pressure semantics: " + _pressure_semantics(result.optimizer_kind),
            "- Primary arm: the policy optimized under the installed proxy "
            "R_hat at each pressure. Control arm: a policy optimized under the "
            "intended objective R at *matched* pressure (the Chapter 03 oracle).",
            "- " + _Z_NOTE,
            "",
        ]
    )
    return lines


def _pressure_semantics(optimizer_kind: str) -> str:
    if optimizer_kind == "bon-width":
        return "best-of-n selection width under the installed judge (alpha = n)."
    if optimizer_kind == "budgeted-search":
        return "total policy evaluations spent (alpha = evaluation budget)."
    if optimizer_kind == "local-search":
        return "accepted hill-climbing improvement steps (alpha = moves)."
    return f"optimizer regime {optimizer_kind!r}."


def _ladder_table(result: RunResult) -> list[str]:
    lines = [
        "## Pressure ladder: primary (R_hat-optimized) vs control (R-optimized)",
        "",
        "Matched pressure on both sides. G is the signed Goodhart gap "
        "J(pi; R_hat) - J(pi; R) for the named policy; events are side-effect "
        "ledger events (collateral damage the proxy prices at zero).",
        "",
        "| Arm | alpha | primary: J(R_hat) | primary: J(R) | primary: G | "
        "primary events | control: J(R) | control: G | control events |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for cell in result.cells:
        lines.append(
            f"| {cell.arm} | {cell.pressure} | "
            f"{_fmt(cell.gap_primary['proxy_return'])} | "
            f"{_fmt(cell.gap_primary['intended_return'])} | "
            f"{_fmt(cell.gap_primary['gap'])} | "
            f"{cell.side_effects_primary['event_count']} | "
            f"{_fmt(cell.gap_control['intended_return'])} | "
            f"{_fmt(cell.gap_control['gap'])} | "
            f"{cell.side_effects_control['event_count']} |"
        )
    lines.append("")
    return lines


def _gates_section(result: RunResult) -> list[str]:
    lines = [
        "## Preregistered gates (judged by interval bounds)",
        "",
        "G1 (degradation): worst-case drop of the gated metric relative to the "
        "same-arm untuned reference, computed from the point's Wilson *lower* "
        "bound. G2 (floor): the point's Wilson lower bound in percentage "
        "points. A gate that only the point estimate passes is a gate that "
        "failed honestly.",
        "",
        "| Arm | alpha | gated metric | point (k/n) | baseline (k/n) | "
        "worst-case degr. | G1 | lower bound | G2 |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for cell in result.cells:
        gate = cell.gates
        point, baseline = gate["point"], gate["baseline"]
        g1 = "pass" if gate["g1_pass"] else "**FAIL**"
        g2 = "pass" if gate["g2_pass"] else "**FAIL**"
        lines.append(
            f"| {gate['arm']} | {gate['pressure']} | "
            f"{_escape(gate['metric_name'])} | "
            f"{point['successes']}/{point['denominator']} "
            f"({_pct(point['rate'], 1)}) | "
            f"{baseline['successes']}/{baseline['denominator']} "
            f"({_pct(baseline['rate'], 1)}) | "
            f"{_fmt(gate['worst_case_degradation_pp'], 1)}pp | {g1} | "
            f"{_fmt(gate['worst_case_floor_pp'], 1)}pp | {g2} |"
        )
    lines.append("")
    return lines


def _side_effects_section(result: RunResult) -> list[str]:
    lines = [
        "## Side-effect ledger: the damage the proxy cannot price",
        "",
        "Collateral damage stays visible as discrete events — never folded "
        "into a scalar score. The primary-vs-control event counts at matched "
        "pressure are the P02 headline: pressure under R_hat keeps producing "
        "events that the same pressure under R eliminates or never creates.",
        "",
        "| Arm | alpha | primary events | primary damaged episodes | "
        "primary damage rate (Wilson 95%) | control events | "
        "control damage rate (Wilson 95%) |",
        "|---|---|---|---|---|---|---|",
    ]
    for cell in result.cells:
        primary, control = cell.side_effects_primary, cell.side_effects_control
        lines.append(
            f"| {primary['arm']} | {cell.pressure} | "
            f"{primary['event_count']} | {primary['damaged_episodes']}/"
            f"{primary['episode_count']} | "
            f"{_pct(primary['rate']['successes'] / primary['rate']['denominator'])} "
            f"{_pct_interval(primary['rate']['lower'], primary['rate']['upper'])} | "
            f"{control['event_count']} | "
            f"{_pct(control['rate']['successes'] / control['rate']['denominator'])} "
            f"{_pct_interval(control['rate']['lower'], control['rate']['upper'])} |"
        )
    lines.extend(
        [
            "",
            "Event kinds are environment-specific (vase-broken in the warehouse; "
            "misleading-answer in the judge environment); magnitudes are carried "
            "in results.json, not collapsed here.",
            "",
        ]
    )
    return lines


def _paired_section(result: RunResult) -> list[str]:
    lines = [
        "## Episode-paired primary-vs-control comparison (intended value)",
        "",
        "Per-episode pairing on the intended objective: the same episodes (or "
        "the same seeded item draws) under both policies. A negative mean "
        "difference says the proxy-optimized policy is *worse than the "
        "matched-pressure control on the objective that actually matters*.",
        "",
        "| Arm | alpha | pairs | mean primary | mean control | mean diff | "
        "W/T/L | primary win rate (Wilson 95%) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for cell in result.cells:
        paired = cell.paired
        win = paired["win_rate"]
        lines.append(
            f"| {cell.arm} | {cell.pressure} | {paired['pairs']} | "
            f"{_fmt(paired['mean_primary'])} | {_fmt(paired['mean_control'])} | "
            f"{_fmt(paired['mean_difference'])} | "
            f"{paired['primary_wins']}/{paired['ties']}/{paired['control_wins']} | "
            f"{_pct(win['successes'] / win['denominator'])} "
            f"{_pct_interval(win['lower'], win['upper'])} |"
        )
    lines.append("")
    return lines


def _divergence_section(result: RunResult) -> list[str]:
    divergence = result.to_json_dict()["divergence"]
    lines = [
        "## Held-out divergence across the ladder",
        "",
        "The proxy-value and intended-value series per arm at matched "
        "pressure (the primary, R_hat-optimized policy on both arms). The "
        "Chapter 03 discriminator: proxy failure keeps the shifted proxy "
        "score high while the intended objective collapses.",
        "",
    ]
    for series_name in ("proxy", "intended"):
        series = divergence[series_name]
        arms = sorted(series["values"])
        header = "| alpha | " + " | ".join(f"J({series_name}) · {arm}" for arm in arms) + " |"
        lines.append(header)
        lines.append("|---|" + "---|" * len(arms))
        for index, pressure in enumerate(series["pressures"]):
            row = f"| {pressure} | " + " | ".join(
                _fmt(series["values"][arm][index]) for arm in arms
            )
            lines.append(row + " |")
        lines.append("")
    return lines


def _revision_section(result: RunResult) -> list[str]:
    if not result.revision_note:
        return []
    return [
        "## Revised-proxy readout",
        "",
        result.revision_note,
        "",
    ]


def _limitations_section(result: RunResult) -> list[str]:
    lines = ["## Honest limitations", ""]
    saturated = [cell for cell in result.cells if cell.primary.get("stopped_early")]
    if saturated:
        cells_text = ", ".join(f"{cell.arm}@{cell.pressure}" for cell in saturated)
        lines.append(
            f"- Saturated ladder points (the search ran out of improvements "
            f"before the requested pressure): {cells_text}. These are facts "
            "about the policy space, reported as achieved, not rounded up."
        )
    small_n = [cell for cell in result.cells if cell.gates["point"]["denominator"] < 30]
    if small_n:
        lines.append(
            "- Small gated-metric denominators (n < 30 per cell): the gate "
            "verdicts are correspondingly conservative — exactly what "
            "interval-bound judging is for (Ch. 02 small-n discipline)."
        )
    lines.extend(
        [
            "- Both environments are synthetic model organisms authored for "
            "this course: the *mechanisms* (proxy blindness, pressure-driven "
            "gap growth, patch displacement) are the teaching content; the "
            "specific numbers are properties of the authored instances, not "
            "measurements of any deployed system.",
            "- The control arm optimizes the authored intended objective R — "
            "in deployment R is not directly optimizable; that asymmetry is "
            "the point of the demonstration, not a bug.",
            "",
        ]
    )
    return lines


def _provenance_section(result: RunResult) -> list[str]:
    provenance = result.provenance()
    return [
        "## Provenance",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| run id | `{provenance['run_id']}` |",
        f"| config SHA-256 | `{provenance['config_sha256']}` |",
        f"| environment | {provenance['environment']} {provenance['environment_version']} |",
        f"| optimizer | {provenance['optimizer_kind']} |",
        f"| pressures | {', '.join(str(p) for p in provenance['pressures'])} |",
        f"| arms | {', '.join(provenance['arms'])} |",
        f"| seed | {provenance['seed']} |",
        f"| code version | {provenance['code_version']} |",
        f"| python | {provenance['python_version']} |",
        f"| run date | {provenance['run_date']} |",
        "",
        "Reproduce: `python -m ai_safety_course.reward_spec.runner <config.yaml>` "
        "with the committed configuration — outputs are byte-stable for a fixed "
        "configuration.",
        "",
    ]


def render_report(result: RunResult) -> str:
    """Render the full markdown report (deterministic)."""
    lines: list[str] = []
    lines.extend(_header(result))
    lines.extend(_construct_section(result))
    lines.extend(_ladder_table(result))
    lines.extend(_gates_section(result))
    lines.extend(_side_effects_section(result))
    lines.extend(_paired_section(result))
    lines.extend(_divergence_section(result))
    lines.extend(_revision_section(result))
    lines.extend(_limitations_section(result))
    lines.extend(_provenance_section(result))
    return "\n".join(lines)


def write_report(result: RunResult, output_dir: Path) -> Path:
    """Write report.md under the output directory (deterministic text)."""
    path = output_dir / "report.md"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(render_report(result), encoding="utf-8")
    tmp.replace(path)
    return path
