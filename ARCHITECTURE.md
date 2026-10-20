# Architecture

How the repository fits together, and why it is shaped this way.

```
AI-Safety/
├── docs/                    # knowledge library (markdown, citation-first)
│   ├── introduction/        # what/why/history/who
│   ├── alignment/           # RLHF, DPO, CAI, oversight, open problems
│   ├── interpretability/    # mech interp, SAEs, steering
│   ├── risks/               # the failure-mode catalog (9 pages)
│   ├── governance/          # NIST / EU AI Act / OWASP / ISO + timeline
│   ├── red_teaming/         # methodology + reporting
│   ├── incidents/           # real cited case studies
│   └── datasets/            # the real-dataset catalog
├── src/aisafety/            # the Python package (stdlib-first)
│   ├── config.py            # frozen dataclass policies
│   ├── log.py               # structured JSON events
│   ├── utils/text.py        # shared text helpers (exfil stripping...)
│   ├── data/                # registry (15 real datasets) + lazy loaders
│   └── safety/              # the filters:
│       ├── pii/             #   detection + redaction      (LLM06)
│       ├── injection/       #   prompt-injection detector  (LLM01)
│       ├── toxicity/        #   lexicon/Perspective hooks
│       ├── guardrails/      #   composable pipeline (input+output stages)
│       └── evaluation/      #   refusal / compliance / metrics
├── benchmarks/              # harnesses: truthfulqa, bold,
│                            # realtoxicityprompts, advbench, xstest
├── scripts/                 # download_datasets / run_benchmark / report
├── examples/                # runnable quickstarts (offline)
├── tests/                   # pytest suite (92 tests; synthetic fixtures)
└── .github/                 # CI (test/lint/links) + security + dependabot
```

## Design decisions

**1. Stdlib-first filters.** The safety filters run without ML
dependencies so they can execute in CI, serverless, and air-gapped
environments. Heavy dependencies (`datasets`, `torch`, API clients) are
imported lazily inside the functions that need them. This mirrors how
real guardrail layers get deployed: as cheap, fast checks wrapped around
expensive model calls.

**2. Config as frozen dataclasses.** Policies (thresholds, modes) are
explicit, immutable values, serializable with `dataclasses.asdict` —
auditable configuration rather than scattered magic numbers. Changing a
threshold is a reviewable diff, which the guardrail docs pair with
re-running the evaluation harnesses (the refusal-parity discipline from
`docs/risks/over_refusal.md`).

**3. Findings as typed records.** Every filter returns structured
findings (`PIIFinding`, `InjectionFinding`) rather than booleans, so
downstream code can log, aggregate, and build regression tests from the
same objects — the same "findings as code" pattern the red-team
methodology page prescribes.

**4. Provenance on everything.** Dataset loads attach provenance
records; benchmark results embed dataset+revision+model+timestamp. The
CI doc-link check enforces that documentation cross-references resolve.
This is the NIST-RMF MEASURE-function discipline in miniature.

**5. Dual import paths.** In-repo code (benchmarks/scripts/tests) imports
via the `src.aisafety` namespace and runs from the repository root;
installable consumers use the `aisafety` package installed from
`pyproject.toml` (`pip install -e .`). Relative imports inside the
package keep both paths coherent.

**6. Tests never touch real PII or real dataset content.** Fixtures are
synthetic and labeled as such; real datasets are downloaded on demand by
`scripts/download_datasets.py` from their canonical sources and stay out
of git (`.gitignore`'s `data/raw/`).

## Data flow (guardrail pipeline)

```
user input ──▶ [PII redaction] ──▶ prompt assembly ──▶ model ──▶ output guard
                                  ▲                                  │
retrieved docs / tool output ─────┘                                  ├─▶ toxicity check
   (injection scan + link stripping first)                           ├─▶ markdown-strip
                                                                     └─▶ render / log
```

Both stages emit structured events via `aisafety.log`, and failures
close by default (`fail_closed=True`) — the OWASP LLM02 posture.
