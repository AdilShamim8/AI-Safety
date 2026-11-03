"""The session-11 companion layer's own contract test.

The sixth course (CampusX, added 2026-11-03) differs from the five
before it: it is paid, its videos sit behind a paywall, and its
outline is marked TENTATIVE by the platform itself. This file pins
what that implies for the companion layer:

  1. the honesty basis — every note states the page-inspected basis,
     no video watched, nothing behind the paywall reproduced, and the
     one unpublished lesson carries its announced status;
  2. the coverage basis — 14 notes, the type/level/pricing facts the
     page renders, and both case studies named on the course page;
  3. the glossary crosswalk — 14 terms, each existing as a row in
     GLOSSARY.md;
  4. the register claims — the pinned numbers and named positions.
"""

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CX = REPO_ROOT / "courses" / "campusx-ai-security-guardrails"


def _read(name: str) -> str:
    return (CX / name).read_text(encoding="utf-8")


def test_every_note_states_the_honesty_basis() -> None:
    notes = sorted(CX.glob("m*-*.md"))
    assert len(notes) == 14
    for p in notes:
        text = p.read_text(encoding="utf-8")
        assert "## Honesty note" in text, p.name
        assert "SRC-CURR-016" in text, p.name
        assert "No video was watched" in text, p.name


def test_course_page_states_the_pinned_facts() -> None:
    page = _read("README.md")
    assert "TENTATIVE" in page
    assert "330.47" in page
    assert "14 lessons" in page
    assert "13 with published" in page
    assert "announced with duration" in page or "duration 0" in page
    assert "NovaBank" in page
    assert "doctor-booking agent" in page
    assert "capability lens" in page
    assert "Promptfoo" in page
    assert "NeMo Guardrails" in page


def test_unpublished_lesson_status_stated_in_note() -> None:
    note = _read("m4-01-threat-modelling-our-agentic-application.md")
    assert "not yet published" in note
    assert "duration 0" in note
    assert "announced scope" in note


def test_glossary_crosswalk_terms_all_exist_in_glossary() -> None:
    cw = _read("crosswalk-glossary.md")
    terms = re.findall(r"^\| \*\*(.+?)\*\* \|", cw, re.M)
    assert len(terms) == 14, len(terms)
    glossary = (REPO_ROOT / "GLOSSARY.md").read_text(encoding="utf-8")
    for term in terms:
        assert f"| **{term}** |" in glossary, f"crosswalk term missing from GLOSSARY.md: {term}"


def test_self_assessment_names_lesson_and_layer_pointers() -> None:
    sa = _read("self-assessment.md")
    questions = [ln for ln in sa.splitlines() if re.match(r"^\d+\. ", ln)]
    assert len(questions) == 10
    assert sa.count("*(module") >= 10


def test_register_claims_pin_the_pinned_numbers() -> None:
    """The six session-11 claims must exist with the numbers they pin."""
    import yaml

    reg = yaml.safe_load((REPO_ROOT / "research" / "claims-register.yaml").read_bytes())
    clm = {c["id"]: c for c in reg["claims"]}
    for cid in ("CLM-0213", "CLM-0214", "CLM-0215", "CLM-0216", "CLM-0217", "CLM-0218"):
        assert cid in clm, f"{cid} missing from the claims register"
    assert "330.47" in clm["CLM-0213"]["claim"]
    assert "1999" in clm["CLM-0214"]["claim"]
    assert "NovaBank" in clm["CLM-0215"]["claim"]
    assert "NeMo Guardrails" in clm["CLM-0216"]["claim"]
    assert "jailbreak gate" in clm["CLM-0217"]["claim"]
    assert "write and delete" in clm["CLM-0218"]["claim"]


def test_every_note_carries_a_worked_example() -> None:
    """The session-11 worked-example layer: all 14 notes carry the
    practitioner walk-through, each substantial."""
    notes = sorted(CX.glob("m*-*.md"))
    assert len(notes) == 14
    for p in notes:
        text = p.read_text(encoding="utf-8")
        assert "## Worked example (practitioner walk-through)" in text, p.name
        section = text.split("## Worked example (practitioner walk-through)")[1].split("## Through-lines")[0]
        assert len(section) > 300, p.name


def test_worked_examples_render_as_prose() -> None:
    """The 14 example sections flow as single paragraphs — no tables
    or code fences for the phone layer to wrap."""
    for p in sorted(CX.glob("m*-*.md")):
        text = p.read_text(encoding="utf-8")
        section = text.split("## Worked example (practitioner walk-through)")[1].split("## Through-lines")[0]
        assert "<table" not in section and "```" not in section, p.name
