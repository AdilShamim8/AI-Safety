"""CampusX companion content — Module 1 (Why Study AI Security?).

Shared content for scripts/gen_campusx_companion.py. One entry per
lesson of the course's module 1 (2 lessons), as listed on the public
course page 2026-11-03 (outline marked TENTATIVE by the platform;
durations as listed). The teaching beats are grounded in the course
page's own published description — the announced scope; no video was
watched, and nothing behind the paywall is reproduced.

Each lesson dict: slug, n, title, minutes, module, situation, beats
[(heading, body)], throughlines [(relpath, label, why)], angle.
"""

CM1 = {
    "number": 1,
    "title": "Why Study AI Security?",
    "lessons": [
        {
            "slug": "m1-01-why-study-ai-security",
            "n": 1,
            "title": "Why Study AI Security?",
            "minutes": 27.98,
            "module": 1,
            "situation": (
                "The course's opening lesson (the longest in module 1, about 28 "
                "minutes as listed). It sets the thesis the whole course runs on: "
                "LLM applications built without security in mind are open to "
                "attack, and a partial understanding of RAG, agents, and "
                "multimodal agents leaves applications insecure — because every "
                "retriever, tool, and input channel you add without thinking "
                "about security becomes a new way in for an attacker."
            ),
            "beats": [
                (
                    "Built without security in mind means open to attack",
                    "The course's first claim, stated as a default: an LLM "
                    "application assembled for capability alone — a retriever "
                    "added for knowledge, a tool added for action, a file "
                    "channel added for convenience — ships every one of those "
                    "additions as an attack surface. The security question is "
                    "not asked after the architecture exists; the course's "
                    "position is that it must be asked while the architecture "
                    "is being chosen, which is what its threat-modelling "
                    "framework (module 2) exists to enforce.",
                ),
                (
                    "Partial understanding is the specific failure mode",
                    "The course targets a precise audience gap: practitioners "
                    "who can build RAG, agents, and multimodal agents but have "
                    "a partial understanding of what those systems are "
                    "security-wise. Each pattern imports its own weak points — "
                    "a RAG brings a vector database and a retriever; an agent "
                    "brings tools and actions; a multimodal app brings "
                    "non-text inputs. Knowing the pattern's capability without "
                    "knowing its exposure is the partial understanding the "
                    "course exists to correct.",
                ),
                (
                    "Every component added is a new way in",
                    "The counting rule the course teaches: attack surface grows "
                    "with every retriever, tool, and input channel. This "
                    "repository's own risk-model chapter states the same rule "
                    "as exposure — a hazard needs a pathway, and every new "
                    "component is a new pathway. The course's version is the "
                    "practitioner's statement of it, and its Data Flow Diagrams "
                    "(module 2) are the instrument for counting.",
                ),
                (
                    "The course's method: secure from the ground up",
                    "The closing move of the opening: security is designed in, "
                    "not patched on. The course promises a repeatable "
                    "step-by-step threat-modelling framework applied end to end "
                    "to two production-grade case studies — a RAG application "
                    "for a bank and a doctor-booking agent — each component "
                    "getting its own security layer. That ground-up promise is "
                    "what distinguishes this course from the four video "
                    "courses in this repository's lecture library, which teach "
                    "the concepts at research level without building the "
                    "layers.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "the application-security chapter this course works at " "production level.",
                ),
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "exposure and pathway as quantities — the disciplined "
                    "version of every-component-is-a-way-in.",
                ),
                (
                    "../../chapters/14-agent-tool-memory-mcp-security/README.md",
                    "Ch. 14",
                    "the agent surface: tools, memory, MCP.",
                ),
            ],
            "angle": (
                "The only course in the library that opens by counting attack "
                "surface per added component and promises to close every one "
                "of them with a named security layer in two worked case "
                "studies."
            ),
        },
        {
            "slug": "m1-02-why-ai-security-practical-landscape",
            "n": 2,
            "title": "Why AI Security? | Practical Landscape",
            "minutes": 22.97,
            "module": 1,
            "situation": (
                "Module 1's second lesson (about 23 minutes as listed). It "
                "draws the line the course considers load-bearing: AI security "
                "is harder than traditional application security, for three "
                "structural reasons — outputs are non-deterministic, inputs "
                "are natural language, and applications are connected to tools "
                "and data — and it surveys the practical landscape with the "
                "live demos the course runs."
            ),
            "beats": [
                (
                    "Three structural differences from application security",
                    "The course's own list, stated as the reason traditional "
                    "defenses do not transfer wholesale: outputs are "
                    "non-deterministic (the same input does not guarantee the "
                    "same output, so output checking cannot be a string "
                    "match); inputs are natural language (the attack surface "
                    "is every phrasing a human can produce, not a typed field "
                    "with a validator); and applications are connected to "
                    "tools and data (the model is not the whole system — the "
                    "retriever, the tools, the stores, and the channels around "
                    "it are half the surface).",
                ),
                (
                    "The live demos the course runs",
                    "As the published description states: live demos show how "
                    "a RAG pipeline can be manipulated, how an attacker can "
                    "turn an agent's tools and actions against you, and how "
                    "images, files, and other non-text inputs open attack "
                    "paths that text-only defenses miss. The demos are the "
                    "course's evidence style: each attack is shown working "
                    "before the defense for it is built.",
                ),
                (
                    "The practical landscape: what is actually deployed",
                    "The lesson positions the course against the landscape of "
                    "shipped LLM applications — RAG pipelines, agents with "
                    "tools and shared memory, multimodal assistants — and the "
                    "gap between what works and what is safe. Its emblem, "
                    "delivered in module 3: a RAG that works is not yet safe "
                    "for a bank.",
                ),
                (
                    "Where this sits in the library",
                    "The four video courses teach the risk landscape at survey "
                    "level; this course is the practitioner layer — the same "
                    "landscape with the defenses built. This repository's "
                    "chapters 12 and 13 are the deep treatments of the two "
                    "sides the lesson names: adversarial manipulation, and "
                    "the application surface built around the model.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "the three structural differences at chapter depth.",
                ),
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "the manipulation demos at research depth.",
                ),
                (
                    "../../chapters/19-multimodal-and-embodied-safety/README.md",
                    "Ch. 19",
                    "non-text inputs as an attack surface.",
                ),
            ],
            "angle": (
                "The only lesson in the library that states the "
                "non-determinism / natural-language / connectedness triple as "
                "the reason application security does not transfer — and then "
                "builds the defenses that answer each part."
            ),
        },
    ],
}
