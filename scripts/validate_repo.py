#!/usr/bin/env python3
"""Pre-commit validator for the AI-Safety course repository.

Checks (run before every commit):
  1. YAML registers parse and carry the required schema fields.
  2. Markdown files contain no hyperlinks to non-existent local files
     (plain-text mentions in backticks are allowed; only real md links count).
  3. No file exceeds a sanity size (catches accidental data/weights commits).

Usage: python3 validate_repo.py /path/to/repo
Exit code 0 = all checks pass.
"""

import re
import subprocess
import sys
from pathlib import Path

import yaml

REQUIRED_SOURCE_FIELDS = [
    "id",
    "title",
    "authors_or_organization",
    "url",
    "source_type",
    "publication_date",
    "version",
    "accessed_on",
    "access_level",
    "evidence_class",
    "peer_review_status",
    "supports",
    "limitations",
    "license",
]
REQUIRED_CLAIM_FIELDS = [
    "id",
    "claim",
    "source",
    "section_or_page",
    "evidence_strength",
    "assumptions",
    "counterevidence",
    "date",
]
VALID_ACCESS_LEVELS = {
    "full-text-read",
    "abstract-read",
    "page-inspected",
    "metadata-only",
    "unavailable",
}
MAX_FILE_BYTES = 2 * 1024 * 1024  # 2 MiB per tracked text file

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s]+)[^)]*\)")


def check_yaml(repo: Path) -> list:
    errors = []
    src_path = repo / "research" / "source-register.yaml"
    clm_path = repo / "research" / "claims-register.yaml"
    for path, fields, kind in (
        (src_path, REQUIRED_SOURCE_FIELDS, "source"),
        (clm_path, REQUIRED_CLAIM_FIELDS, "claim"),
    ):
        if not path.exists():
            continue  # registers appear in the first research commit
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            errors.append(f"{path.name}: YAML parse error: {e}")
            continue
        entries = (data or {}).get(f"{kind}s") or []
        if not isinstance(entries, list) or not entries:
            errors.append(f"{path.name}: no {kind} entries found")
            continue
        for entry in entries:
            missing = [f for f in fields if f not in entry]
            if missing:
                errors.append(f"{path.name}: {entry.get('id', '?')} missing fields: {missing}")
            if kind == "source":
                lvl = entry.get("access_level")
                if lvl and lvl not in VALID_ACCESS_LEVELS:
                    errors.append(f"{path.name}: {entry.get('id')} invalid access_level {lvl!r}")
    return errors


def check_links(repo: Path) -> list:
    errors = []
    md_files = sorted(repo.rglob("*.md"))
    for md in md_files:
        text = md.read_text(encoding="utf-8", errors="replace")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if target.startswith(("http://", "https://", "mailto:", "#", "mailto:")):
                continue
            if target.startswith("#"):
                continue
            local = target.split("#", 1)[0]
            if not local:
                continue
            candidate = (md.parent / local).resolve()
            try:
                candidate.relative_to(repo.resolve())
            except ValueError:
                errors.append(f"{md.name}: link escapes repo: {target}")
                continue
            if not candidate.exists():
                errors.append(f"{md.name}: broken local link: {target}")
    return errors


def _tracked_files(repo: Path) -> list[Path] | None:
    """Files git would commit (the index), or None if not a real git repo."""
    try:
        out = subprocess.run(
            ["git", "-C", str(repo), "ls-files", "-z"],
            capture_output=True,
            check=True,
        ).stdout.decode()
    except (subprocess.SubprocessError, OSError):
        return None
    return [repo / p for p in out.split("\0") if p]


def check_sizes(repo: Path) -> list:
    """Flag tracked files above the sanity cap.

    Size limits apply to what would be committed, not to local working
    state: with a real git repo we check the index; the directory walk
    fallback (used in tests with fake repos) skips .git and .venv.
    """
    errors = []
    tracked = _tracked_files(repo)
    if tracked is not None:
        candidates = [f for f in tracked if f.is_file()]
    else:
        candidates = [
            f
            for f in repo.rglob("*")
            if f.is_file() and ".git" not in f.parts and ".venv" not in f.parts
        ]
    for f in candidates:
        if f.stat().st_size > MAX_FILE_BYTES:
            errors.append(f"oversize file ({f.stat().st_size} bytes): {f}")
    return errors


def main() -> int:
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    if not (repo / ".git").exists():
        print(f"not a git repo: {repo}")
        return 2
    errors = check_yaml(repo) + check_links(repo) + check_sizes(repo)
    if errors:
        print("VALIDATION FAILED")
        for e in errors:
            print(f"  - {e}")
        return 1
    print("validation OK: yaml schema, local links, file sizes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
