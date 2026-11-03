"""CampusX companion content — Module 2 (AI Security & Challenges).

Shared content for scripts/gen_campusx_companion.py. One entry per
lesson of the course's module 2 (4 lessons, 41.7 minutes as listed).
See campusx_content.py for the field contract and the honesty basis.
"""

CM2 = {
    "number": 2,
    "title": "AI Security & Challenges",
    "lessons": [
        {
            "slug": "m2-01-ai-security-challenges",
            "n": 1,
            "title": "AI Security & Challenges",
            "minutes": 9.8,
            "module": 2,
            "situation": (
                "Module 2's opening lesson (about 10 minutes as listed), the "
                "shortest of the four. It states what AI security means in "
                "this course and why it is harder than traditional application "
                "security, preparing the ground for the adversarial attacks "
                "lesson that follows."
            ),
            "beats": [
                (
                    "What AI security means here",
                    "The working definition the course builds on: securing the "
                    "application around the model — the RAG pipeline, the "
                    "tools, the memory, the channels — not only the model "
                    "itself. The course's scope is the practitioner's: every "
                    "component in the data flow, each getting its own security "
                    "layer by the end of the case studies.",
                ),
                (
                    "Why harder than application security",
                    "The three structural reasons restated as the challenge "
                    "list: outputs are non-deterministic, inputs are natural "
                    "language, and applications are connected to tools and "
                    "data. Traditional defenses assume deterministic outputs, "
                    "validated inputs, and a bounded system boundary — none "
                    "of which an LLM application provides.",
                ),
                (
                    "The bridge to the framework",
                    "The lesson's closing job: naming the challenges precisely "
                    "enough that the next lesson (adversarial attacks and "
                    "types) and the one after (the threat-modelling framework) "
                    "have something to organize. This repository's Ch. 13 is "
                    "the chapter-length version of the same ground.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "the application-security chapter at full depth.",
                ),
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "the adversarial side the next lesson details.",
                ),
            ],
            "angle": (
                "The compact statement of scope — the whole course's meaning "
                "of AI security in ten minutes, the layer the survey courses "
                "spend chapters approaching."
            ),
        },
        {
            "slug": "m2-02-adversarial-attacks-and-types",
            "n": 2,
            "title": "Adversarial Attacks & Types",
            "minutes": 8.77,
            "module": 2,
            "situation": (
                "The adversarial-attacks lesson (about 9 minutes as listed): "
                "the common types used to manipulate an LLM application, the "
                "lesson the course's demos were built for."
            ),
            "beats": [
                (
                    "The manipulation catalog",
                    "The course's published scope: adversarial attacks and the "
                    "common types used to manipulate an LLM application — the "
                    "attack families that show up in the two case studies. "
                    "From the description's own list: a RAG pipeline "
                    "manipulated end to end; an agent's tools and actions "
                    "turned against its operator; non-text inputs (images, "
                    "files) opening attack paths text-only defenses miss.",
                ),
                (
                    "The phase distinction the course uses",
                    "The course organizes attacks the way this repository's "
                    "chapters 12 and 13 do: by where the fault enters — "
                    "training-time versus inference-time, direct versus "
                    "indirect. Its two case-study families: jailbreaks and "
                    "prompt injection against the user query and the LLM "
                    "(module 3's lesson), and indirect prompt injection hidden "
                    "in retrieved documents and tool results (the agent "
                    "case).",
                ),
                (
                    "Every attack is shown working first",
                    "The course's evidence style: live demos of each attack "
                    "against the unsecured application, then the defense "
                    "layer that closes it. The lesson names the types; the "
                    "case-study modules run them.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/12-adversarial-ml-and-robustness/README.md",
                    "Ch. 12",
                    "the attack families at research depth.",
                ),
                (
                    "../../chapters/15-red-teaming-and-adversarial-evaluation/README.md",
                    "Ch. 15",
                    "finding the attacks systematically.",
                ),
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "the injection surfaces at chapter depth.",
                ),
            ],
            "angle": (
                "The attack catalog as the case studies will use it — each "
                "type paired with the component it attacks, which is the "
                "practitioner's taxonomy."
            ),
        },
        {
            "slug": "m2-03-tools-needed-to-secure-llm-applications",
            "n": 3,
            "title": "Tools Needed to Secure LLM Applications",
            "minutes": 11.34,
            "module": 2,
            "situation": (
                "The tools lesson (about 11 minutes as listed): the toolbox "
                "the course deploys across both case studies — named here "
                "before the framework lesson assigns each tool to a layer."
            ),
            "beats": [
                (
                    "The toolbox as the course names it in practice",
                    "From the published description and outline: PII detection "
                    "and masking (so customers' personal data never reaches "
                    "the vector database); authentication and authorization "
                    "at production level (pre-retrieval metadata filtering "
                    "that blocks restricted documents before the search "
                    "runs); input guardrails (stopping jailbreaks in the user "
                    "query); delimiters and a system prompt that treats "
                    "retrieved documents as data (the prompt-injection "
                    "defense); output guardrails built with NVIDIA NeMo "
                    "Guardrails (checking every answer for private data, "
                    "wrong facts, or a manipulated response before it reaches "
                    "the user); a separate guard model (reading every message "
                    "and every tool and MCP result); and Promptfoo for the "
                    "red-team pass at the close.",
                ),
                (
                    "Each tool answers a named attack",
                    "The organizing rule: no tool without an attack it "
                    "closes. Masking answers PII leakage; pre-retrieval "
                    "filtering answers unauthorized retrieval; input "
                    "guardrails answer jailbreaks; delimiters answer "
                    "injection from retrieved documents; output guardrails "
                    "answer manipulated responses; the guard model on tool "
                    "results answers indirect injection hidden in external "
                    "content.",
                ),
                (
                    "The open-source anchor",
                    "The course builds its output guardrails with NVIDIA NeMo "
                    "Guardrails and red-teams with Promptfoo — the two "
                    "open-source anchors of the practitioner layer, both now "
                    "carried as glossary rows in this repository.",
                ),
            ],
            "throughlines": [
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "the defense layer at chapter depth.",
                ),
                (
                    "../../chapters/16-privacy-provenance-and-supply-chains/README.md",
                    "Ch. 16",
                    "PII, masking, and the data protections.",
                ),
                (
                    "../../chapters/08-ai-control-and-monitoring/README.md",
                    "Ch. 08",
                    "monitoring every result as the control pattern.",
                ),
            ],
            "angle": (
                "The only lesson in the library that names the practitioner "
                "toolbox — masking, filtering, guardrails, delimiters, guard "
                "models, red-team harness — as one assignable set."
            ),
        },
        {
            "slug": "m2-04-threat-modelling-framework",
            "n": 4,
            "title": "Threat Modelling Framework",
            "minutes": 11.81,
            "module": 2,
            "situation": (
                "Module 2's capstone lesson (about 12 minutes as listed): the "
                "step-by-step framework the course repeats on any LLM "
                "application — the instrument both case studies run on."
            ),
            "beats": [
                (
                    "The five-step framework",
                    "As the course applies it in both case studies: (1) map "
                    "the application with Data Flow Diagrams — every "
                    "component, and every entry and exit point; (2) draw the "
                    "trust boundaries — where data crosses between levels of "
                    "trust; (3) examine every component through the "
                    "capability lens — what it can read, write, execute, or "
                    "reach; (4) find every weak point from the diagram; (5) "
                    "close each one with its own security layer. The course's "
                    "phrase for the method: repeatable to secure any "
                    "LLM-based application.",
                ),
                (
                    "The capability lens",
                    "The course's signature instrument: for each component, "
                    "ask what it can read, write, execute, or reach. The "
                    "lens turns a diagram into a risk list — a component "
                    "that can write is more dangerous than one that can "
                    "only read, which is exactly how the course explains why "
                    "an agent (with write and delete capabilities) is more "
                    "dangerous than a RAG (whose worst case changes an "
                    "answer).",
                ),
                (
                    "Why a framework at all",
                    "The course's argument: security work without the "
                    "framework is anecdote-driven — you fix the attack you "
                    "happened to see. The framework makes the search "
                    "systematic: every component visited, every capability "
                    "priced, every weak point closed with a named layer. "
                    "This repository's threat-model template and Ch. 13's "
                    "discipline are the same argument at chapter depth.",
                ),
            ],
            "throughlines": [
                (
                    "../../templates/threat-model.md",
                    "the threat-model template",
                    "the repository's own form for the same discipline.",
                ),
                (
                    "../../chapters/13-llm-application-security/README.md",
                    "Ch. 13",
                    "the chapter-length treatment.",
                ),
                (
                    "../../chapters/01-risk-models-and-research-epistemics/README.md",
                    "Ch. 01",
                    "capability and exposure as quantities.",
                ),
            ],
            "angle": (
                "The framework as a repeatable five-step procedure — the "
                "course's core deliverable, and the reason its two case "
                "studies are the same method twice."
            ),
        },
    ],
}
