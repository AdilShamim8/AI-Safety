"""Structured logging helpers.

Safety-relevant events (guardrail triggers, evaluation runs, injection
findings) should be logged in a machine-parseable form: EU AI Act
logging duties and ISO 42001 audit trails both consume structured
records more easily than prose. This module standardizes the shape.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any

 getLogger = logging.getLogger("aisafety")

_EVENT_KEYS = ("event", "component", "severity", "detail")


def utc_now_iso() -> str:
    """Current UTC time in ISO-8601 (Z-suffixed) form."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log_event(
    event: str,
    *,
    component: str = "aisafety",
    severity: str = "info",
    detail: dict[str, Any] | None = None,
    logger: logging.Logger | None = None,
) -> None:
    """Emit a structured one-line JSON event.

    Example:
        log_event("guardrail_block", component="injection",
                  severity="warning",
                  detail={"score": 0.93, "pattern": "instruction_override"})
    """
    record = {
        "ts": utc_now_iso(),
        "event": event,
        "component": component,
        "severity": severity,
        "detail": detail or {},
    }
    (logger or getLogger).info(json.dumps(record, default=str))


def setup(level: int = logging.INFO, *, json_lines: bool = False) -> logging.Logger:
    """Configure the aisafety logger with a handler (idempotent).

    json_lines=True emits machine-readable lines suitable for shipping
    to a log aggregator; default is human-readable format.
    """
    logger = getLogger
    if logger.handlers:  # already configured
        return logger
    handler = logging.StreamHandler(sys.stderr)
    if json_lines:
        handler.setFormatter(logging.Formatter("%(message)s"))
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s")
        )
    logger.addHandler(handler)
    logger.setLevel(level)
    return logger
