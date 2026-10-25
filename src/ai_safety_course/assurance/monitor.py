"""P10 monitor — the deterministic flagging layer of the bounded agent.

The monitor is the second safety layer of the capstone system
(Ch. 08's control discipline integrated with Ch. 14's capability
policy): it inspects calls the guard ALLOWED and holds the suspicious
ones for review, paying for each hold from a shared audit-credit
budget. When the budget is exhausted the call proceeds UNREVIEWED
(fail-open at the margin) — the deployment choice whose price the
dossier measures, never hides.

Layer separation (deliberate, and load-bearing for the capstone's
lesson): capability references are the GUARD's domain (R1/R2 over the
declared table); the MONITOR's domain is web-derived data (W) about
to reach any tool that can change state or send externally — the
exact signature of the authored-policy gaps the guard cannot see,
because the matrix never declared those arguments as capability
references at all. A monitor that re-flags what the guard already
vetted would only burn audit credits on duplicate review.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from ai_safety_course.agent_guard.matrix import PrivilegeMatrix, ToolSpec
from ai_safety_course.agent_guard.policy import Provenance, ToolCall

#: Why a call was flagged.
REASON_WEB_WRITE = "web-derived-argument-on-non-read-only-tool"

#: What the monitor did.
ACTION_HOLD = "hold"
ACTION_UNCOVERED = "uncovered-pass-through"


@dataclass(frozen=True)
class MonitorEvent:
    """One monitor decision, in the trace log."""

    step_index: int  # 1-based
    tool: str
    reason: str
    action: str
    credits_before: int
    credits_after: int


@dataclass
class FlaggingMonitor:
    """Flags allowed calls that carry web-derived data (W) into any
    tool that can change state or send externally.

    Read-only tools are never flagged: they only FEED untrusted data
    into the system (Ch. 14's feeds), they do not act on it.
    Capability-reference arguments are the guard's domain and are
    deliberately NOT re-inspected here — see the module docstring.
    """

    matrix: PrivilegeMatrix
    credits: int = 2
    events: list[MonitorEvent] = field(default_factory=list)

    def _flags(self, call: ToolCall) -> str | None:
        tool: ToolSpec = self.matrix.tool(call.tool)
        if tool.authority == "read-only":
            return None
        for arg in call.arguments:
            if arg.provenance is Provenance.WEB:
                return REASON_WEB_WRITE
        return None

    def consider(self, call: ToolCall, step_index: int) -> MonitorEvent | None:
        """Inspect one allowed call: hold it (paying a credit) or let it
        pass uncovered when the budget is exhausted. Returns None when
        the call is not flagged at all."""
        reason = self._flags(call)
        if reason is None:
            return None
        if self.credits > 0:
            self.credits -= 1
            event = MonitorEvent(
                step_index=step_index,
                tool=call.tool,
                reason=reason,
                action=ACTION_HOLD,
                credits_before=self.credits + 1,
                credits_after=self.credits,
            )
        else:
            event = MonitorEvent(
                step_index=step_index,
                tool=call.tool,
                reason=reason,
                action=ACTION_UNCOVERED,
                credits_before=0,
                credits_after=0,
            )
        self.events.append(event)
        return event

    @property
    def credits_remaining(self) -> int:
        return self.credits
