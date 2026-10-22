"""matrix — the privilege and trust-boundary matrix (P07 core artifact).

Chapter 14's audit discipline as code: every tool in a deployment,
mapped to its credential scope, its data reach, which untrusted
channels feed it, and what it can do if the model is fully hijacked.
The two structural findings the chapter reads out of the matrix are
computed here, not eyeballed:

- the *exfiltration pairs*: entry tools that put attacker-chosen
  content into context crossed with egress tools that move data out
  under real credentials;
- the *authority gradient*: tools grouped by how bad a hijacked call
  is (irreversible-external, irreversible-internal,
  reversible-with-effort, read-only).

The matrix is the coverage claim of a capability audit: a policy
checked against a matrix that missed a tool is a policy that does not
cover that tool's authority. Loading is fail-closed — any schema
violation raises :class:`MatrixError` rather than degrading silently
(the Chapter 02 rule, carried into agent security).
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

#: The only matrix schema version this loader understands.
MATRIX_SCHEMA = "p07-privilege-matrix/v1"

#: Authority levels, most to least severe. The names carry the
#: chapter's operational meaning, not an abstract taxonomy.
AUTHORITY_LEVELS = (
    "irreversible-external",  # egress + cannot undo (mail.send, pay.invoice)
    "irreversible-internal",  # destroys/rewrites internal state (files.write)
    "reversible-with-effort",  # repairable sabotage (calendar.write)
    "read-only",  # disclosure but no state change (mail.read, files.read)
)


class MatrixError(ValueError):
    """Raised when a tool specification or matrix file is invalid."""


@dataclass(frozen=True)
class ToolSpec:
    """One row of the privilege and trust-boundary matrix.

    Attributes mirror the chapter's five columns exactly; the audit
    questions are functions of these fields, never of the tool's
    self-description (the MCP rule: descriptions are untrusted).
    """

    name: str
    credential_scope: str
    data_reach: str
    untrusted_feeds: tuple[str, ...] = ()
    authority: str = "read-only"
    is_egress: bool = False
    writes_shared_store: bool = False

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise MatrixError(f"tool name must be non-empty: {self.name!r}")
        if self.authority not in AUTHORITY_LEVELS:
            raise MatrixError(
                f"tool {self.name!r}: authority {self.authority!r} not in " f"{AUTHORITY_LEVELS}"
            )
        if self.is_egress and self.authority != "irreversible-external":
            raise MatrixError(
                f"tool {self.name!r}: an egress tool moves data out under real "
                "credentials; authority must be 'irreversible-external'"
            )

    @property
    def entry_channel(self) -> bool:
        """True when an untrusted channel feeds this tool's outputs into context.

        These are the tools whose *results* become attacker-influenced
        state S (mail.read, files.read over synced docs, web.fetch) —
        the entry half of every exfiltration pair.
        """
        return bool(self.untrusted_feeds)


@dataclass(frozen=True)
class PrivilegeMatrix:
    """The audited toolset: the artifact a capability policy is written against."""

    tools: tuple[ToolSpec, ...] = ()
    source_name: str = "<in-memory>"
    checksum: str = "<none>"
    schema_version: str = MATRIX_SCHEMA

    def __post_init__(self) -> None:
        names = [t.name for t in self.tools]
        if len(set(names)) != len(names):
            dupes = sorted({n for n in names if names.count(n) > 1})
            raise MatrixError(f"duplicate tool names in matrix: {dupes}")

    # -- the chapter's two structural findings ------------------------------

    def tool(self, name: str) -> ToolSpec:
        """Return the tool spec for ``name``; raise MatrixError if absent."""
        for t in self.tools:
            if t.name == name:
                return t
        raise MatrixError(f"tool {name!r} not in matrix (a policy referencing it is uncovered)")

    def entry_tools(self) -> tuple[ToolSpec, ...]:
        """Tools whose results inject attacker-writable text into context."""
        return tuple(t for t in self.tools if t.entry_channel)

    def egress_tools(self) -> tuple[ToolSpec, ...]:
        """Tools that move data out under real credentials."""
        return tuple(t for t in self.tools if t.is_egress)

    def exfiltration_pairs(self) -> tuple[tuple[ToolSpec, ToolSpec], ...]:
        """Every (entry, egress) pair that turns a hijack into a data leak.

        Neither tool alone is an incident; the pair is the standard
        exfiltration pathway of a hijacked assistant (Ch. 14 §4.1).
        Note the entry tool *of a pair* need not be the one whose call
        the attacker corrupted — the pairing is a property of the
        deployment, not of any single attack trace.
        """
        return tuple(
            (entry, egress) for entry in self.entry_tools() for egress in self.egress_tools()
        )

    def authority_gradient(self) -> dict[str, tuple[str, ...]]:
        """Tool names grouped by authority level, most severe first."""
        gradient: dict[str, tuple[str, ...]] = {}
        for level in AUTHORITY_LEVELS:
            names = tuple(t.name for t in self.tools if t.authority == level)
            if names:
                gradient[level] = names
        return gradient

    def store_writers(self) -> tuple[ToolSpec, ...]:
        """Tools that write stores other tools later read (slow-store poisoning).

        A hijacked ``crm.update`` or ``files.write`` can leave content
        behind that a *later honest* flow discloses — blast radius is
        not just what a tool reads, but what it can leave for other
        tools to read (Ch. 14 exercise 14.1's sharp finding).
        """
        return tuple(t for t in self.tools if t.writes_shared_store)

    def audit_summary(self) -> dict[str, Any]:
        """A machine-readable summary of the matrix's structural findings."""
        pairs = self.exfiltration_pairs()
        return {
            "tools": len(self.tools),
            "entry_tools": [t.name for t in self.entry_tools()],
            "egress_tools": [t.name for t in self.egress_tools()],
            "exfiltration_pairs": [[e.name, g.name] for e, g in pairs],
            "exfiltration_pair_count": len(pairs),
            "authority_gradient": self.authority_gradient(),
            "store_writers": [t.name for t in self.store_writers()],
        }


# -- loading -----------------------------------------------------------------


def _require_fields(tool: Mapping[str, Any], fields: Sequence[str]) -> None:
    missing = [f for f in fields if f not in tool]
    if missing:
        raise MatrixError(f"tool entry missing fields {missing}: {dict(tool)!r}")


def parse_matrix(data: Mapping[str, Any], source_name: str = "<mapping>") -> PrivilegeMatrix:
    """Validate and build a :class:`PrivilegeMatrix` from a parsed mapping."""
    if data.get("schema_version") != MATRIX_SCHEMA:
        raise MatrixError(f"schema_version {data.get('schema_version')!r} != {MATRIX_SCHEMA!r}")
    raw_tools = data.get("tools")
    if not isinstance(raw_tools, list) or not raw_tools:
        raise MatrixError("matrix must carry a non-empty 'tools' list")
    allowed = {
        "name",
        "credential_scope",
        "data_reach",
        "untrusted_feeds",
        "authority",
        "is_egress",
        "writes_shared_store",
    }
    tools: list[ToolSpec] = []
    for entry in raw_tools:
        if not isinstance(entry, Mapping):
            raise MatrixError(f"tool entry must be a mapping: {entry!r}")
        _require_fields(entry, ("name", "credential_scope", "data_reach", "authority"))
        unknown = set(entry) - allowed
        if unknown:
            raise MatrixError(f"tool {entry.get('name')!r}: unknown fields {sorted(unknown)}")
        feeds = entry.get("untrusted_feeds", [])
        if not isinstance(feeds, list) or not all(isinstance(f, str) for f in feeds):
            raise MatrixError(
                f"tool {entry.get('name')!r}: untrusted_feeds must be a list of strings"
            )
        tools.append(
            ToolSpec(
                name=str(entry["name"]),
                credential_scope=str(entry["credential_scope"]),
                data_reach=str(entry["data_reach"]),
                untrusted_feeds=tuple(feeds),
                authority=str(entry["authority"]),
                is_egress=bool(entry.get("is_egress", False)),
                writes_shared_store=bool(entry.get("writes_shared_store", False)),
            )
        )
    return PrivilegeMatrix(
        tools=tuple(tools),
        source_name=source_name,
        checksum="<mapping>",
    )


def load_matrix(path: Path) -> PrivilegeMatrix:
    """Load and checksum-pin a matrix YAML file (fail-closed)."""
    raw = path.read_bytes()
    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:  # pragma: no cover - defensive
        raise MatrixError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, Mapping):
        raise MatrixError(f"{path}: top level must be a mapping")
    matrix = parse_matrix(data, source_name=str(path))
    return PrivilegeMatrix(
        tools=matrix.tools,
        source_name=str(path),
        checksum=hashlib.sha256(raw).hexdigest(),
    )


@dataclass(frozen=True)
class MatrixAudit:
    """Result of auditing a loaded matrix for structural red flags."""

    matrix: PrivilegeMatrix
    notes: tuple[str, ...] = field(default=())

    @property
    def ok(self) -> bool:
        """True when no structural red flag fired (notes may still carry advisories)."""
        return not any(n.startswith("RED FLAG") for n in self.notes)


def audit_matrix(matrix: PrivilegeMatrix) -> MatrixAudit:
    """Audit the matrix itself for the chapter's structural red flags.

    Red flags are properties of the deployment that no per-tool review
    reveals: exfiltration pairs, store writers that feed egress tools,
    and egress tools reachable with user credentials.
    """
    notes: list[str] = []
    pairs = matrix.exfiltration_pairs()
    if pairs:
        names = ", ".join(f"{e.name}->{g.name}" for e, g in pairs)
        notes.append(f"RED FLAG exfiltration pairs ({len(pairs)}): {names}")
    writers = matrix.store_writers()
    if writers:
        names = ", ".join(t.name for t in writers)
        notes.append(f"RED FLAG slow-store writers (poisoned-well persistence): {names}")
    gradient = matrix.authority_gradient()
    severe = gradient.get("irreversible-external", ())
    if severe:
        notes.append(f"authority gradient: irreversible-external tools = {severe}")
    return MatrixAudit(matrix=matrix, notes=tuple(notes))
