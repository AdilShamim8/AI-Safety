# How the CampusX course organizes knowledge

**Navigate:** [← the CampusX companion](README.md) · [reading map](reading-map.md)

*A pedagogy analysis · part of the [CampusX companion](README.md) ·
written 2026-11-03 from the verified course page*

## The question this note answers

How does the course gather, organize, and manage information — the
question the lecture library's index asks of every course. This one's
answer is unique in the library: it teaches security as construction.

## The capability-lens architecture

| Axis | The CampusX course |
|---|---|
| Unit of instruction | one component of a data flow, priced and closed |
| Core artifact | Data Flow Diagrams + the capability table + one named layer per weak point |
| Evidence discipline | demos first: every attack shown working before its defense is built |
| Case studies | two production-grade systems (a bank RAG; a doctor-booking agent) |
| The grade | a Promptfoo red-team pass on the secured stack, per layer |
| Who it is for | practitioners who can build RAG and agents and need the security half |
| What only it does | guardrails engineering as a construction discipline, layer by layer |

## What the architecture chooses to believe

**The course bets on the framework over the anecdote.** Security work
without the five-step method fixes the attack you happened to see;
with it, every component is visited, every capability priced, every
weak point closed. The bet is that methodical beats clever — and the
red-team grade at the end is there to prove the method held.

**The capability lens is the load-bearing idea.** Read, write,
execute, reach: the four verbs that turn a diagram into a risk list.
The lens explains the course's central claim — why an agent (write
and delete) is more dangerous than a RAG (read and answer) — and it
is the same instrument this repository's threat-model template asks
for, which is why the pairing works.

**Demos first is an honesty device.** Every attack is shown working on
the unsecured application before the layer that closes it is built.
The course never asserts a defense works; it runs the attack, builds
the layer, and red-teams the result. That is the same evidence
discipline this repository's evaluation chapters enforce.

## What this repository took from it

The per-component capability framing (now in the glossary as its own
row); the pre-retrieval versus post-retrieval filtering distinction;
the conversation-level jailbreak gate as a design pattern; the
per-layer red-team report as the output of a security review; and the
two case studies as the working exemplars the chapters and projects
point to.

## The construction discipline, stated once more

What the course adds to the library is the thing survey courses cannot teach by their nature: the moment of building. The layers exist in code with names, the stack has an order, the red-team grade has a per-layer report, and the whole sequence is repeatable on the next application. That repeatability — not any single layer — is the course's actual product, and it is why this repository pairs it with the chapters that name the patterns and the projects that audit them.
