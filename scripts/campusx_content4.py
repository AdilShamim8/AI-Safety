"""CampusX companion content — Module 4 (Threat Modelling our Agentic Application).

Shared content for scripts/gen_campusx_companion.py. One entry per
lesson of the course's module 4 (2 lessons; the first listed with
duration 0 — announced, not yet published — and the second at 34.15
minutes as listed). See campusx_content.py for the field contract and
the honesty basis.
"""

CM4 = {
    "number": 4,
    "title": "Threat Modelling our Agentic Application",
    "lessons": [
        {
            "slug": "m4-01-threat-modelling-our-agentic-application",
            "n": 1,
            "title": "Threat Modelling our Agentic Application",
            "minutes": 0,
            "module": 4,
            "situation": (
                "The agent case study opens. Listed with duration 0 on the "
                "course page — announced in the outline, not yet published "
                "at verification time (2026-11-03); the platform marks the "
                "whole outline TENTATIVE. The companion note is written to "
                "the case study's announced scope, which the published "
                "description states in full: the doctor-booking agent, the "
                "five-step framework run on it, and why write and delete "
                "capabilities make an agent more dangerous than a RAG."
            ),
            "beats": [
                (
                    "The doctor-booking agent, as the description states it",
                    "The case study's system: an agent for a website that "
                    "lists doctors. It searches doctors' pages with a tool, "
                    "checks free slots and books appointments through an MCP "
                    "server, and learns from past conversations through a "
                    "shared memory. Anyone on the internet can use it without "
                    "logging in — the standing condition the threat model "
                    "has to accept.",
                ),
                (
                    "Write and delete make an agent more dangerous than a RAG",
                    "The case study's central claim, from the description: "
                    "running the same five-step framework, you see how write "
                    "and delete capabilities make an agent more dangerous "
                    "than a RAG — an attack no longer just changes an "
                    "answer, it makes the agent take real actions, such as "
                    "leaking patients' details, steering patients to one "
                    "doctor, or cancelling bookings. The capability lens "
                    "prices this exactly: the RAG's worst case is a wrong "
                    "answer; the agent's worst case is a wrong action.",
                ),
                (
                    "The four security layers the case study builds",
                    "From the published description, the announced scope the "
                    "lesson teaches: a jailbreak gate (a separate guard model "
                    "reading every message along with recent turns, inside "
                    "delimiters, blocking authority claims, requests for "
                    "other people's data, and attempts to override the "
                    "agent's rules); a guard model on every tool and MCP "
                    "result (stopping indirect prompt injection hidden in "
                    "doctors' pages and schedule notes); memory protection "
                    "(custom instructions and a judge that checks every "
                    "write, so personal data and poisoned lessons never "
                    "reach the shared memory); and output guardrails "
                    "checking every answer against the platform's policies "
                    "— the fee cap, no promised cures, no links to other "
                    "sites, no other patients' data.",
                ),
                (
                    "Why this lesson's honest status is different",
                    "The verification note this companion carries: the "
                    "lesson is announced with duration 0. Its scope is known "
                    "from the description; its recording was not available "
                    "to check against. The note states what is announced, "
                    "and the honesty section says exactly that.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/14-agent-tool-memory-mcp-security/README.md",
                    "Ch. 14",
                    "the agent surface — tools, memory, MCP — at chapter " "depth.",
                ),
                (
                    "../../projects/p08-control-and-monitoring-protocol/README.md",
                    "the P08 project",
                    "the repository's own control-and-monitoring exercise " "for agent systems.",
                ),
                (
                    "../../chapters/08-ai-control-and-monitoring/README.md",
                    "Ch. 08",
                    "checking every action as the control pattern.",
                ),
            ],
            "angle": (
                "The only lesson in the library whose case study is an agent "
                "with tools, MCP booking, shared memory, and no login — and "
                "the wrong-answer-versus-wrong-action distinction as its "
                "organizing claim."
            ),
        },
        {
            "slug": "m4-02-securing-from-jailbreak-attacks",
            "n": 2,
            "title": "Securing from Jailbreak Attacks",
            "minutes": 34.15,
            "module": 4,
            "situation": (
                "The course's closing applied lesson (about 34 minutes as "
                "listed): the jailbreak gate as the agent case study's first "
                "built layer — the defense the whole course has been "
                "building toward, at the input channel that matters most "
                "for an agent."
            ),
            "beats": [
                (
                    "A separate guard model reads every message",
                    "The gate's architecture, from the published description: "
                    "a separate guard model reading every message, along "
                    "with recent turns, inside delimiters — blocking "
                    "authority claims, requests for other people's data, and "
                    "attempts to override the agent's rules. The design "
                    "choices are the lesson: separate (its own model, not "
                    "the agent's), contextual (recent turns, not the message "
                    "alone), and delimited (the conversation arrives inside "
                    "boundaries the guard treats as data).",
                ),
                (
                    "What the gate blocks, named",
                    "The three block categories the description lists: "
                    "authority claims (I am the administrator), requests for "
                    "other people's data (patients' details), and attempts "
                    "to override the agent's rules (ignore your "
                    "instructions). Each is a jailbreak family the course "
                    "named in module 2, now closed at the gate.",
                ),
                (
                    "The method completes: every layer on both case studies",
                    "The lesson closes the course's arc: the same five-step "
                    "framework, the same one-layer-per-weak-point method, "
                    "now on the agent — gate on the conversation, guard on "
                    "every tool and MCP result, judge on every memory write, "
                    "guardrails on every answer, and (as the description "
                    "promises) Promptfoo red-teaming at production level on "
                    "both secured applications.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/14-agent-tool-memory-mcp-security/README.md",
                    "Ch. 14",
                    "the gate in the agent's architecture.",
                ),
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "the jailbreak families at research depth.",
                ),
                (
                    "../../chapters/15-red-teaming-and-adversarial-evaluation/README.md",
                    "Ch. 15",
                    "testing the gate systematically.",
                ),
            ],
            "angle": (
                "The jailbreak gate built as its own model with recent-turn "
                "context and delimiters — the only lesson in the library "
                "that implements the conversation-level gate and names the "
                "three block categories it exists to catch."
            ),
        },
    ],
}
