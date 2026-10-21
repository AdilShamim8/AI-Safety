"""report — dated markdown evaluation reports with a provenance block.

The report generator turns a :class:`~ai_safety_course.evaluation.runner.RunResult`
into the repository's experiment-report discipline as markdown: explicit
numerators and denominators for every rate, Wilson 95% intervals per
Chapter 02, a paired refusal/compliance ledger, per-category breakdowns,
an error-analysis section listing every mismatch, the scorer-validation
status, bracketing-baseline comparison rows when supplied, and a
provenance block (case-set checksum, adapter configuration fingerprint,
seed, code and environment versions).

Every number in the generated report is computed from the run's
per-case records — nothing is hand-typed — and generation is
deterministic: the same ``RunResult`` always renders the same text, so
committed reports can be byte-reproduced from the committed runner.
"""

from collections.abc import Sequence
from pathlib import Path

from ai_safety_course.evaluation.metrics import (
    LABEL_COMPLIANCE,
    LABEL_REFUSAL,
    MetricSummary,
    rate_metric,
)
from ai_safety_course.evaluation.runner import RunResult
from ai_safety_course.evaluation.scorer import (
    KNOWN_LIMITATION_EXAMPLES,
    REFUSAL_PATTERNS,
)


def _pct(value: float, digits: int = 1) -> str:
    """Format a proportion as a percentage string."""
    return f"{value:.{digits}%}"


def _wilson_cell(metric: MetricSummary) -> str:
    """Render a metric's Wilson interval as a table cell."""
    return f"[{_pct(metric.interval.lower)}, {_pct(metric.interval.upper)}]"


def _metric_row(metric: MetricSummary) -> str:
    """One ledger table row: name | k | n | rate | Wilson 95%."""
    return (
        f"| {_escape(metric.name)} | {metric.successes} | {metric.denominator} "
        f"| {_pct(metric.rate, 2)} | {_wilson_cell(metric)} |"
    )


def _escape(text: str) -> str:
    """Make free text safe for a markdown table cell."""
    return text.replace("|", "\\|").replace("\n", " ")


def _ledger_table(result: RunResult) -> list[str]:
    """The overall paired-ledger section lines."""
    ledger = result.ledger()
    lines = [
        "## Paired ledger (overall)",
        "",
        "Numerator over explicit denominator for every rate; Wilson 95% intervals",
        "computed per Chapter 02 (z = 1.96).",
        "",
        "| Metric | k | n | rate | Wilson 95% |",
        "|---|---|---|---|---|",
    ]
    lines.extend(_metric_row(entry) for entry in ledger.entries())
    lines.append("")
    return lines


def _category_section(result: RunResult) -> list[str]:
    """Per-category refusal-rate rows, both sides, with explicit n."""
    categories = result.case_set.categories()
    lines = [
        "## Per-category rates with Wilson 95% intervals",
        "",
        "Refusal rate on each side of the ledger, per category. Categories here are",
        "small by design (a fixture, not a census): with only a few cases per cell the",
        "intervals are wide by construction — per-category point estimates are",
        "diagnostic, not decision-grade (Ch. 02 small-n discipline).",
        "",
        "| Category | Side | k | n | rate | Wilson 95% |",
        "|---|---|---|---|---|---|",
    ]
    for category in categories:
        rows = [record for record in result.records if record.category == category]
        for side, expected in (
            ("expected=refuse", "refuse"),
            ("expected=comply", "comply"),
        ):
            side_rows = [record for record in rows if record.expected_behavior == expected]
            if not side_rows:
                lines.append(f"| {category} | {side} | — | 0 | — | (side absent) |")
                continue
            refusals = sum(1 for record in side_rows if record.label == LABEL_REFUSAL)
            metric = rate_metric(f"{category} · {side}", refusals, len(side_rows))
            lines.append(
                f"| {category} | {side} | {metric.successes} | {metric.denominator} "
                f"| {_pct(metric.rate, 2)} | {_wilson_cell(metric)} |"
            )
    lines.append("")
    return lines


def _mismatch_section(result: RunResult) -> list[str]:
    """Error analysis: every case where observed ≠ expected."""
    lines = ["## Mismatches (error analysis)", ""]
    mismatches = result.mismatches()
    if not mismatches:
        lines.append(
            f"No mismatches — the adapter matched the expected behavior on all "
            f"{len(result.records)} cases."
        )
        lines.append("")
        return lines
    lines.extend(
        [
            "| Case | Category | Expected | Observed | Response excerpt |",
            "|---|---|---|---|---|",
        ]
    )
    for record in mismatches:
        expected_label = LABEL_REFUSAL if record.expected_behavior == "refuse" else LABEL_COMPLIANCE
        excerpt = _escape(record.response[:60])
        suffix = "…" if len(record.response) > 60 else ""
        lines.append(
            f"| {record.case_id} | {record.category} | {expected_label} "
            f"| {record.label} | {excerpt}{suffix} |"
        )
    lines.append("")
    return lines


def _baseline_section(baselines: Sequence[RunResult]) -> list[str]:
    """Bracketing-baseline comparison rows (echo / all-refuse adapters)."""
    lines = ["## Baselines (bracketing adapters)", ""]
    if not baselines:
        lines.extend(
            [
                "No baseline runs recorded in this report. The protocol's bracketing",
                "baselines — the echo adapter (never refuses: attack-side floor) and a",
                "scripted all-refuse adapter (never complies: benign-side floor) — are",
                "exercised deterministically by the project's test suite.",
            ]
        )
        lines.append("")
        return lines
    lines.extend(
        [
            "| Run | Adapter | Refusal on expected=refuse | False refusal on expected=comply |",
            "|---|---|---|---|",
        ]
    )
    for baseline in baselines:
        ledger = baseline.ledger()
        lines.append(
            f"| {baseline.run_id} | {baseline.adapter_kind} "
            f"| {ledger.refusal_when_refuse_expected.successes}/"
            f"{ledger.refusal_when_refuse_expected.denominator} "
            f"({_pct(ledger.refusal_when_refuse_expected.rate, 1)}) "
            f"| {ledger.refusal_when_comply_expected.successes}/"
            f"{ledger.refusal_when_comply_expected.denominator} "
            f"({_pct(ledger.refusal_when_comply_expected.rate, 1)}) |"
        )
    lines.append("")
    return lines


def _scorer_section(result: RunResult) -> list[str]:
    """Scorer-validation status and documented limitations."""
    lines = [
        "## Scorer validation",
        "",
        f"Instrument: `{result.scorer_name}` — {len(REFUSAL_PATTERNS)} refusal patterns,",
        "English-only keyword/regex rules (see `src/ai_safety_course/evaluation/scorer.py`).",
        "",
        f"{result.scorer_validation}",
        "",
        "Documented limitations (the score is a proxy for the construct — Chapter 02's",
        "gap sentence applies):",
    ]
    for example in KNOWN_LIMITATION_EXAMPLES:
        lines.append(
            f"- misclassifies {_escape(example.response[:70])}… (true label: "
            f"{example.expected_label});"
        )
    lines.extend(
        [
            '- refusals phrased only as redirection ("let\'s talk about something else")',
            "  are missed (false compliance);",
            "- the scorer reads only the response text, not the prompt, and has no",
            "  semantic understanding; it is validated only against the committed",
            "  hand-verified fixture.",
        ]
    )
    lines.append("")
    return lines


def _provenance_section(result: RunResult) -> list[str]:
    """The provenance block required by the experiment-report template."""
    case_set = result.case_set
    lines = [
        "## Provenance",
        "",
        f"- Case set: `{case_set.name}` v{case_set.version} — `{case_set.path}`",
        f"- Case-set SHA-256: `{case_set.sha256}`",
        f"- Case-set provenance: {case_set.provenance.get('authorship', 'unknown')}; "
        f"design model: {case_set.provenance.get('design_model', 'unknown')}",
        f"- Adapter: `{result.adapter_kind}` (config SHA-256 `{result.adapter_config_sha256}`)",
        f"- Seed: {result.seed}",
        f"- Code: `{result.code_version}`",
        f"- Environment: Python {result.python_version}, PyYAML {result.pyyaml_version}, "
        "CPU-only, offline",
        f"- Run date: {result.run_date} · resumed cases: {result.resumed_cases} of "
        f"{len(result.records)}",
        "- Known nondeterminism: none for scripted/echo adapters; the seed is threaded",
        "  to every adapter call so stochastic adapters can be made deterministic.",
        "",
    ]
    return lines


def _reproduction_section(result: RunResult) -> list[str]:
    """Exact reproduction commands (plain-text paths, no local links)."""
    lines = [
        "## Reproduction",
        "",
        "From the repository root (Python 3.12, stdlib + PyYAML, CPU-only):",
        "",
        "```bash",
        "uv sync",
        "PYTHONPATH=src uv run python -m ai_safety_course.evaluation.runner <run-config.yaml>",
        "```",
        "",
        f"Per-case outputs for this run live in `{result.run_id}`'s `results.json`",
        "(written under the configured output directory; raw run directories are not",
        "committed — only curated reports are).",
        "",
    ]
    return lines


def render_report(result: RunResult, baselines: Sequence[RunResult] = ()) -> str:
    """Render the dated markdown report for ``result``.

    Args:
        result: the completed run to report.
        baselines: optional bracketing baseline runs (e.g. the echo and
            all-refuse adapters) rendered as comparison rows.

    Returns:
        The full markdown report as a string (deterministic).
    """
    lines: list[str] = [
        f"# Evaluation report: {result.report_title}",
        "",
        f"Run ID: `{result.run_id}` · Project: P01 · Status: implemented "
        "(scripted-adapter demonstration over synthetic cases — not a model "
        f"evaluation) · Date: {result.run_date}",
        "",
        "## Construct and scores",
        "",
        "- Construct: refusal calibration of the adapter under test — the paired rate",
        "  at which it refuses cases whose expected behavior is `refuse` (attack side)",
        "  versus cases whose expected behavior is `comply` (false-refusal side).",
        f"- Score: refusal/compliance labels assigned by `{result.scorer_name}`",
        "  (keyword/regex scoring of the response text only).",
        "- Gap sentence: the score is evidence for the *scored-label* construct, except",
        "  that keyword scoring can miss redirection-only refusals and can flag hedged",
        f"  compliances; scorer validation for this run: {result.scorer_validation}.",
        f"- Instruments: `{result.case_set.name}` v{result.case_set.version} "
        f"({len(result.records)} synthetic cases, checksum-pinned below).",
        "",
    ]
    lines.extend(_ledger_table(result))
    lines.extend(_category_section(result))
    lines.extend(_mismatch_section(result))
    lines.extend(_baseline_section(baselines))
    lines.extend(_scorer_section(result))
    lines.extend(_provenance_section(result))
    lines.extend(_reproduction_section(result))
    return "\n".join(lines)


def write_report(
    result: RunResult,
    path: Path | str,
    baselines: Sequence[RunResult] = (),
) -> None:
    """Write the markdown report for ``result`` to ``path``.

    Raises:
        OSError: if the path cannot be written.
    """
    Path(path).write_text(render_report(result, baselines), encoding="utf-8")
