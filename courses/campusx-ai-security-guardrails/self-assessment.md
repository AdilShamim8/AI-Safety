# Self-assessment — the CampusX course

**Navigate:** [← the CampusX companion](README.md) · [reading map](reading-map.md) · [pedagogy](pedagogy.md)

Ten judgment questions. Answer from the course and its companion
notes; every question names the lesson that teaches it and the
repository layer that deepens it.

1. Your RAG answers every demo query correctly. Name the thesis that
   says it is not yet safe for a bank, and the instrument that finds
   out. *(module 1 and 3.01; Ch. 01, Ch. 13)*
2. State the three structural differences from application security,
   and say which defense in the toolbox answers each one. *(module
   1.02 and 2.03; Ch. 13)*
3. Walk the five-step framework on any LLM application you have built
   — diagram, boundaries, capability table, weak points, layers.
   *(module 2.04; templates/threat-model.md)*
4. Why does the vector database leak PII, and what is the layer that
   closes it — and where in the pipeline does that layer sit? *(module
   3.02; Ch. 16)*
5. Pre-retrieval metadata filtering versus post-retrieval filtering:
   which does the course build, and why does the other leak? *(module
   3.03; Ch. 13, Ch. 14)*
6. The user query and the retrieved documents are two different
   channels. Name the defense for each, and the attack each one
   closes. *(module 3.04; Ch. 12, Ch. 13)*
7. What three things does the output guardrail check every answer
   for, and why is the check per-answer rather than per-release?
   *(module 3.05; Ch. 08, Ch. 22)*
8. Why is an agent with write and delete more dangerous than a RAG?
   Give the lens answer and the case-study examples. *(module 4.01;
   Ch. 14)*
9. The jailbreak gate reads every message with recent turns inside
   delimiters. Name the three block categories and why the gate is a
   separate model. *(module 4.02; Ch. 14, Ch. 15)*
10. What does the Promptfoo red-team pass actually grade, and why is
    the per-layer report the finding rather than a pass/fail?
    *(module 3.06; Ch. 02, Ch. 15, P07)*

Scoring: eight or more with the lens or the layer named — you carried
the method. Fewer — re-run the case studies' lessons; the notes are
the map back.
