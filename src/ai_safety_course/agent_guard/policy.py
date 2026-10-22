"""policy — the capability policy checker: provenance tags and rules R1-R4.

Chapter 14 §4.2 as executable code. Every value an agent handles
carries a *provenance tag* (user-typed/private **U**, web- or
mail-derived **W**, agent-generated **A**); every tool argument is
either plain data or a *capability reference* — an argument that
selects an object with rights (a mail recipient, a payee, a file
path). The four rules:

- **R1 (exfiltration, consent-gated):** a ``U``-tagged value may not
  reach an egress tool's *non-destination* arguments unless the user
  consented to that specific destination this session. The
  destination argument itself is exempt — a user-typed destination
  is the normal case; it is the *content* flowing to a destination
  that must be consented.
- **R2 (argument integrity, hard block):** a ``W``-tagged value may
  not fill a capability-reference argument of *any* tool. No consent
  screen can make untrusted data a safe capability selector — this
  is the rule consent-decay cannot erode.
- **R3 (memory provenance, hard block):** a store-writing tool must
  record the tag of every fact it stores. Untagged writes are never
  authorized: provenance-at-write is unrecoverable after the fact.
- **R4 (consent, consent-gated):** the first invocation of an
  irreversible-external tool in a session surfaces an authorization
  request naming the capability and any ``W``-derived arguments.

Decision precedence: a hard-block rule (R2/R3) dominates; consent
rules (R1/R4) yield :attr:`Decision.CONSENT_REQUIRED`, resolved by
the session's scripted user. The checker never asks whether the model
"looks suspicious" — it inspects the trace's provenance against the
matrix's authority facts. That is the chapter's whole point: nothing
here relies on the model noticing anything.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import Enum

from ai_safety_course.agent_guard.matrix import PrivilegeMatrix, ToolSpec


class Provenance(Enum):
    """Where a value came from — the tag that travels with every argument."""

    USER = "U"  # user-typed / user-owned private data
    WEB = "W"  # web- or mail-derived data (attacker-writable channels)
    AGENT = "A"  # agent-generated derived content


class PolicyError(ValueError):
    """Raised when a policy configuration or call is structurally invalid."""


#: Rule identifiers, stable for reports and tests.
R1 = "R1-exfiltration"
R2 = "R2-argument-integrity"
R3 = "R3-memory-provenance"
R4 = "R4-consent"

#: Rules whose violation is consentable versus not, ever.
HARD_BLOCK_RULES = frozenset({R2, R3})
CONSENT_RULES = frozenset({R1, R4})


@dataclass(frozen=True)
class Argument:
    """One tool-call argument: a value, its provenance tag, and its role.

    ``is_capability_ref`` marks arguments that *select* an object with
    rights (recipient, payee, path, destination). Mislabeling one as
    plain data is the authored-policy gap of Ch. 14 §6 — the checker
    cannot discover capability references; the matrix audit must
    declare them.
    """

    name: str
    value: str
    provenance: Provenance
    is_capability_ref: bool = False


@dataclass(frozen=True)
class ToolCall:
    """A tool invocation the policy is asked to mediate."""

    tool: str
    arguments: tuple[Argument, ...] = ()

    def argument(self, name: str) -> Argument:
        for a in self.arguments:
            if a.name == name:
                return a
        raise PolicyError(f"call to {self.tool!r} has no argument {name!r}")

    def has(self, name: str) -> bool:
        """True when this call carries an argument named ``name``."""
        return any(a.name == name for a in self.arguments)


class Decision(Enum):
    """What the policy does with a call (stable string values for reports)."""

    ALLOW = "allow"
    BLOCK = "block"
    CONSENT_REQUIRED = "consent-required"


@dataclass(frozen=True)
class PolicyResult:
    """The verdict on one call: the decision, the rules that fired, and why."""

    decision: Decision
    rules_fired: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()
    capability_ref_args: tuple[str, ...] = ()

    @property
    def executed(self) -> bool:
        """True when the call runs without further user interaction."""
        return self.decision is Decision.ALLOW

    @property
    def hard_blocked(self) -> bool:
        """True when a non-consentable rule (R2/R3) fired."""
        return self.decision is Decision.BLOCK


@dataclass
class Session:
    """Per-session consent state — the human half of the policy.

    ``consented_destinations`` holds destinations the user explicitly
    approved *this session* (R1); ``consented_tools`` holds tools the
    user has authorized this session (R4). Empty by default: least
    privilege starts closed.
    """

    consented_destinations: set[str] = field(default_factory=set)
    consented_tools: set[str] = field(default_factory=set)

    def consent_to(self, tool: str, destination: str | None = None) -> None:
        """Record a user consent for a tool and optionally a destination."""
        self.consented_tools.add(tool)
        if destination is not None:
            self.consented_destinations.add(destination)


#: Argument names that are capability references, per tool. This table
#: IS the authored policy's coverage claim; tools absent from it have
#: no capability-reference arguments *as declared* (Ch. 14 §6's gap,
#: demonstrated deliberately in the P07 fixture: ``crm.update``'s
#: ``value`` argument is not declared, and the poisoned-well scenario
#: walks straight through it).
DEFAULT_CAPABILITY_REFS: dict[str, frozenset[str]] = {
    "mail.send": frozenset({"recipient"}),
    "pay.invoice": frozenset({"payee"}),
    "files.write": frozenset({"path"}),
    "files.read": frozenset({"path"}),
    "web.fetch": frozenset({"url"}),
    "crm.export": frozenset({"destination"}),
    "crm.update": frozenset({"record_id", "field"}),
    "calendar.write": frozenset({"event_id"}),
    "memory.write": frozenset(),
    "memory.read": frozenset(),
    "mail.read": frozenset(),
    "mail.list": frozenset(),
    "files.list": frozenset(),
    "calendar.read": frozenset(),
    "crm.search": frozenset(),
}

#: The argument of each egress tool that carries the destination —
#: R1's "specific destination" for consent, and the argument exempt
#: from the U-content scan (a user-typed destination is the normal
#: case; U *content* flowing to it is what consent must cover).
DEFAULT_EGRESS_DESTINATION_ARGS: dict[str, str] = {
    "mail.send": "recipient",
    "crm.export": "destination",
    "web.fetch": "url",
}


@dataclass(frozen=True)
class CapabilityPolicy:
    """The R1-R4 policy, checked against a privilege matrix.

    ``capability_refs`` maps tool name -> argument names that are
    capability references. ``egress_destination_args`` names each
    egress tool's destination argument (R1's consent target and the
    exempt argument). ``store_tools`` are the tools whose writes must
    carry provenance (R3).
    """

    matrix: PrivilegeMatrix
    capability_refs: Mapping[str, frozenset[str]] = field(
        default_factory=lambda: dict(DEFAULT_CAPABILITY_REFS)
    )
    egress_destination_args: Mapping[str, str] = field(
        default_factory=lambda: dict(DEFAULT_EGRESS_DESTINATION_ARGS)
    )
    store_tools: frozenset[str] = frozenset({"memory.write"})
    require_consent_irreversible: bool = True

    def __post_init__(self) -> None:
        for tool_name in self.capability_refs:
            self.matrix.tool(tool_name)  # fail-closed: policy must be covered

    # -- rule implementations ---------------------------------------------

    def _capability_ref_names(self, tool: ToolSpec) -> frozenset[str]:
        return self.capability_refs.get(tool.name, frozenset())

    def destination_of(self, call: ToolCall) -> str | None:
        """The destination argument's value for an egress call, if present."""
        tool = self.matrix.tool(call.tool)
        dest_name = self.egress_destination_args.get(tool.name)
        if dest_name and call.has(dest_name):
            return call.argument(dest_name).value
        return None

    def check(self, call: ToolCall, session: Session) -> PolicyResult:
        """Apply R1-R4 to one call; hard blocks dominate, consent gates follow."""
        tool = self.matrix.tool(call.tool)
        cap_refs = self._capability_ref_names(tool)
        cap_ref_args = tuple(a.name for a in call.arguments if a.name in cap_refs)

        hard_reasons: list[str] = []
        consent_reasons: list[str] = []
        rules: list[str] = []

        # R2: a W-tagged value may not fill a capability-reference argument.
        for a in call.arguments:
            if a.is_capability_ref or a.name in cap_refs:
                if a.provenance is Provenance.WEB:
                    rules.append(R2)
                    hard_reasons.append(
                        f"argument {a.name!r} of {tool.name!r} is a capability "
                        "reference filled with web/mail-derived data (W)"
                    )

        # R1: U-tagged content may not reach an egress tool's non-destination
        # arguments unless this specific destination was consented this session.
        if tool.is_egress:
            dest_name = self.egress_destination_args.get(tool.name)
            destination = (
                call.argument(dest_name).value if dest_name and call.has(dest_name) else None
            )
            for a in call.arguments:
                if a.provenance is not Provenance.USER:
                    continue
                if dest_name is not None and a.name == dest_name:
                    continue  # the destination itself is exempt
                if destination is None or destination not in session.consented_destinations:
                    rules.append(R1)
                    consent_reasons.append(
                        f"user-private data (U) in argument {a.name!r} of egress "
                        f"tool {tool.name!r} without a consented destination"
                    )
                    break

        # R3: store writes must record provenance for every fact stored.
        if tool.name in self.store_tools:
            if not any(a.name == "record_tags" for a in call.arguments):
                rules.append(R3)
                hard_reasons.append(
                    f"store write via {tool.name!r} without per-fact provenance "
                    "tags (provenance-at-write is unrecoverable after the fact)"
                )

        # R4: first use of an irreversible-external tool in a session.
        if (
            self.require_consent_irreversible
            and tool.authority == "irreversible-external"
            and tool.name not in session.consented_tools
        ):
            rules.append(R4)
            consent_reasons.append(
                f"first invocation of irreversible tool {tool.name!r} this session"
            )

        if hard_reasons:
            return PolicyResult(
                decision=Decision.BLOCK,
                rules_fired=tuple(dict.fromkeys(rules)),
                reasons=tuple(hard_reasons + consent_reasons),
                capability_ref_args=cap_ref_args,
            )
        if consent_reasons:
            return PolicyResult(
                decision=Decision.CONSENT_REQUIRED,
                rules_fired=tuple(dict.fromkeys(rules)),
                reasons=tuple(consent_reasons),
                capability_ref_args=cap_ref_args,
            )
        return PolicyResult(decision=Decision.ALLOW, capability_ref_args=cap_ref_args)


class AllowAllPolicy:
    """The full-delegation arm: execute every call regardless of provenance.

    The confused deputy, deployed — used as the comparison arm in the
    paired harness so the arms differ *only* in policy, never in
    scenario or matrix.
    """

    def __init__(self, matrix: PrivilegeMatrix) -> None:
        self.matrix = matrix

    def check(self, call: ToolCall, session: Session) -> PolicyResult:  # noqa: ARG002
        """Always ALLOW — no provenance inspection, no consent gates."""
        return PolicyResult(decision=Decision.ALLOW)
