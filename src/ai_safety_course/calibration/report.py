"""report — dated markdown calibration reports with a provenance block.

Renders a :class:`~ai_safety_course.calibration.runner.RunResult` into
the repository's experiment-report discipline as markdown: the
validation/evaluation split statement; one section per (instrument,
calibrator) pair with the reliability table (per-bin counts, mean
confidence, accuracy, Wilson intervals), ECE with its binning stated,
Brier, clipped log loss, the mean gap (labeled as a marginal), the
risk–coverage summary (AURC, oracle ceiling, gap, full-coverage risk),
and the threshold table with BOTH sides of the abstention ledger; a
cross-pair comparison table (the deployer's view); an honest-limitations
section; and a full provenance block (case-set checksum, config
fingerprint, code version, run date).

Every number is computed from the run's records — nothing is
hand-typed — and generation is deterministic.
"""

from pathlib import Path

from ai_safety_course.calibration.runner import RunResult


def _fmt(value: float, digits: int = 4) -> str:
    text = f"{value:.{digits}f}"
    if text.startswith("-") and float(text) == 0.0:
        return text[1:]
    return text


def _pct(value: float, digits: int = 1) -> str:
    return f"{value:.{digits}%}"


def _header(result: RunResult) -> list[str]:
    status = result.config.status_note or "implemented"
    return [
        f"# P03 experiment report: {result.config.run_id}",
        "",
        f"Run ID: `{result.config.run_id}` · Project: {result.config.project} · "
        f"Status: {status} · Date: {result.config.run_date}",
        "",
        f"Split: {len(result.validation_indices)} validation / "
        f"{len(result.evaluation_indices)} evaluation items "
        "(round-robin by case order — even validation, odd evaluation; "
        "calibrators fit on validation only and frozen before evaluation).",
        "",
    ]


def _pair_section(record: object, num_bins: int) -> list[str]:
    lines = [
        f"## Pair: `{record.instrument}` under `{record.calibrator_kind}`",
        "",
        f"Calibration map (frozen before evaluation): {record.fit_report}",
        "",
        "### Reliability table (evaluation split)",
        "",
        "Per-bin rows carry count, mean confidence, accuracy, and the Wilson 95%",
        "interval on accuracy (z at full precision).",
        "",
        "| bin | n | conf | acc | Wilson 95% | gap |",
        "|---|---|---|---|---|---|",
    ]
    for row in record.reliability_rows:
        lower, upper, count, conf, acc, lo, hi = row
        lines.append(
            f"| [{lower:.1f}, {upper:.1f}) | {count} | {conf:.3f} | "
            f"{acc:.3f} | [{lo:.3f}, {hi:.3f}] | {acc - conf:+.3f} |"
        )
    lines.extend(
        [
            "",
            f"ECE = {_fmt(record.ece)} at K = {num_bins} "
            f"(bin counts: {', '.join(str(c) for c in record.bin_counts)}) — "
            "ECE is a binning artifact; the counts ride along.",
            "",
            "### Proper scores and marginals (evaluation split)",
            "",
            f"- Brier: {_fmt(record.brier)} (proper score: punishes "
            "miscalibration and rewards discrimination)",
            f"- Log loss: {_fmt(record.log_loss_value)} (clipped at 1e-15)",
            f"- Mean gap: {_fmt(record.mean_gap_value)} (marginal "
            "confidence − accuracy; NOT a calibration measure — bins cancel)",
            "",
            "### Selective prediction (evaluation split)",
            "",
            f"- AURC: {_fmt(record.aurc)} (mean selective risk over all " "coverage levels)",
            f"- Oracle AURC: {_fmt(record.oracle_aurc)} (correct-first " "ceiling for this set)",
            f"- AURC gap: {_fmt(record.aurc_gap_value)} (ranking "
            "information the score failed to extract)",
            f"- Full-coverage risk: {_fmt(record.full_coverage_risk)} " "(answering everything)",
            "",
            "| tau | answered | coverage | errors | selective risk | "
            "false abstentions | false-abstention rate |",
            "|---|---|---|---|---|---|---|",
        ]
    )
    for t in record.thresholds:
        risk = "—" if t["selective_risk"] is None else _fmt(t["selective_risk"])
        lines.append(
            f"| {t['tau']:.2f} | {t['answered']} | {_pct(t['coverage'])} | "
            f"{t['errors']} | {risk} | {t['false_abstentions']} | "
            f"{_pct(t['false_abstention_rate'])} |"
        )
    lines.append("")
    return lines


def _comparison_table(result: RunResult) -> list[str]:
    lines = [
        "## Cross-pair comparison (the deployer's view)",
        "",
        "| Instrument | Calibrator | Brier | Log loss | ECE | AURC | "
        "AURC gap | Full-coverage risk |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for r in result.results:
        lines.append(
            f"| {r.instrument} | {r.calibrator_kind} | {_fmt(r.brier)} | "
            f"{_fmt(r.log_loss_value)} | {_fmt(r.ece)} | {_fmt(r.aurc)} | "
            f"{_fmt(r.aurc_gap_value)} | {_fmt(r.full_coverage_risk)} |"
        )
    lines.extend(
        [
            "",
            "Reading rules: a calibrator earns its parameters only if it beats "
            "identity *on the evaluation split* (Brier/log loss); an AURC above "
            "the full-coverage risk means the gate is worse than answering "
            "everything (the inverted-signal signature); the AURC gap is the "
            "information the score failed to extract, not an error bar.",
            "",
        ]
    )
    return lines


def _limitations_section(result: RunResult) -> list[str]:
    return [
        "## Honest limitations",
        "",
        "- The instruments are scripted confidence scores over synthetic "
        "items — the *measurement discipline* (splits, intervals, both "
        "ledger sides) is the deliverable; the numbers are properties of "
        "the authored fixture, not of any deployed model.",
        "- Calibration maps are fit on a round-robin validation split of "
        "the same authored distribution; a deployment-grade fit needs an "
        "external calibration set, and the ml compute tier is where that "
        "lands (marked honestly in the project README).",
        "- ECE is reported at the configured K only; sensitivity to K is a "
        "property of the binning, not the instrument (the metrics tests "
        "pin the K-dependence).",
        "- Threshold operating points carry conditional rates whose "
        "denominators move with tau; the Wilson intervals ride along and "
        "small-n points are correspondingly wide.",
        "",
    ]


def _provenance_section(result: RunResult) -> list[str]:
    provenance = result.provenance()
    return [
        "## Provenance",
        "",
        "| Field | Value |",
        "|---|---|",
        f"| run id | `{provenance['run_id']}` |",
        f"| config SHA-256 | `{provenance['config_sha256']}` |",
        f"| case set | {provenance['case_set']} {provenance['case_set_version']} "
        f"(`{provenance['case_set_sha256'][:16]}…`) |",
        f"| binning | K = {provenance['num_bins']} |",
        f"| split | {provenance['split']} |",
        f"| code version | {provenance['code_version']} |",
        f"| python | {provenance['python_version']} |",
        f"| run date | {provenance['run_date']} |",
        "",
        "Reproduce: `PYTHONPATH=src python -m ai_safety_course.calibration.runner "
        "<config.yaml>` — outputs are byte-stable for a fixed configuration.",
        "",
    ]


def render_report(result: RunResult) -> str:
    """Render the full markdown report (deterministic)."""
    lines: list[str] = []
    lines.extend(_header(result))
    for record in result.results:
        lines.extend(_pair_section(record, result.config.num_bins))
    lines.extend(_comparison_table(result))
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
