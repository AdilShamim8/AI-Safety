# Part 2.6 — Safer design patterns: architecture as a safety decision

*Course companion note · [Google DeepMind AGI Safety Course](README.md) ·
video: [Part 2: 6. Safer design patterns](https://www.youtube.com/watch?v=jWNPqYSH2_o) (3:47) · [playlist](https://www.youtube.com/playlist?list=PLw9kjlF6lD5UqaZvMTbhJB8sV-yuXu5eW)*

## What this part covers

The fifth mechanism (3 minutes): safety-relevant
*architecture* — how you structure the model, its tools, and its
deployment shape — as a first-class design layer rather than a
post-training patch.

## Core ideas, explained

### 1. The patterns catalogue

The family the part surveys: tool separation and privilege
boundaries (agents with least privilege); sandboxed execution;
human-approval gates on irreversible actions; dual-model patterns
(planner/executor separation, quarantined LLMs); capability scoping
(the system does one bounded thing rather than everything). The
repo's [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md)
is the full agent-security treatment, and the CaMeL design paper
(register-registered) is the flagship worked example.

### 2. Why design beats patching

A prompt can be re-engineered, a filter fine-tuned away — but an
architecture where untrusted data *cannot* reach privileged
instruction channels removes the vulnerability class instead of
defending against each exploit. The prompt-injection literature's
convergent conclusion is exactly this move to the design layer; the
repo's comparison note on prompt defenses vs. authorization
boundaries stages the argument.

### 3. The cost side, priced

Design constraints trade against capability and latency (the Harvard
F26 systems lecture's bandwidth lesson applies: every gate is
middleware). Honest design docs state the cost — the repo's project
READMEs model this by marking each defense's measured overhead.

## Through-line to this repository's chapters

- [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) —
  agent and tool security.
- [research/notes/21-camel-defeating-injections-by-design.md](../../research/notes/21-camel-defeating-injections-by-design.md) —
  the flagship design paper.
- [research/notes/comparison-04-prompt-defenses-vs-authorization-boundaries.md](../../research/notes/comparison-04-prompt-defenses-vs-authorization-boundaries.md) —
  the staged argument.

## Honesty note

This is an original study companion written to the part's announced
topic (its title as verified in the playlist fetch, 2026-10-27). The video
itself was not watched; no spoken content is transcribed or quoted.
The explanation below is grounded in the literature this repository
registers — where a claim has a register entry, it is linked.
