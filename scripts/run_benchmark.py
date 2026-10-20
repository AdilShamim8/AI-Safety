#!/usr/bin/env python3
"""Run a benchmark harness against a model and write a structured result.

Model backends (choose with --model):
- ``echo``      : a trivial deterministic echo (plumbing smoke tests only —
                  results are NOT model evaluations and are labeled as such)
- ``refusal``   : a toy safety-policy responder that refuses anything
                  containing injection/toxicity signals (plumbing tests)
- ``openai``    : an OpenAI chat-completions wrapper (requires OPENAI_API_KEY
                  and the ``openai`` package)
- ``file:<path>``: replay responses from a JSONL file of
                  {"prompt": ..., "response": ...} records (offline analysis)

Every result record embeds provenance (dataset, revision, model id, date)
per the repo's editorial policy.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BENCHMARKS = ("truthfulqa", "advbench", "xstest", "bold", "realtoxicityprompts")

SMOKE_DISCLAIMER = (
    "echo/refusal/file backends are plumbing tests, not model evaluations"
)


def echo_model(prompt: str) -> str:
    return prompt


def refusal_model(prompt: str) -> str:
    risky = re.search(r"\b(kill|bomb|steal|hack|poison|weapon|exploit)\b",
                      prompt, re.I)
    if risky:
        return "I can't help with that request."
    return f"Here is a response to: {prompt}"


def openai_model(model_id: str, prompt: str) -> str:
    try:
        from openai import OpenAI  # optional dependency
    except ImportError as err:
        raise SystemExit("openai package required for --model openai") from err
    import os

    client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
    completion = client.chat.completions.create(
        model=model_id,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.0,
    )
    return completion.choices[0].message.content or ""


def file_model(path: str) -> object:
    records = {}
    with Path(path).open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            records[row["prompt"]] = row["response"]

    def respond(prompt: str) -> str:
        if prompt in records:
            return records[prompt]
        return "I can't help with that request."  # conservative default

    return respond


def build_model(spec: str):
    if spec == "echo":
        return echo_model
    if spec == "refusal":
        return refusal_model
    if spec.startswith("openai"):
        model_id = spec.split(":", 1)[1] if ":" in spec else "gpt-4o-mini"
        return lambda p: openai_model(model_id, p)
    if spec.startswith("file:"):
        return file_model(spec[5:])
    raise SystemExit(f"unknown model spec: {spec}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("benchmark", choices=BENCHMARKS)
    parser.add_argument("--model", default="refusal",
                        help="echo | refusal | openai[:id] | file:<path>")
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--max", type=int, default=None)
    parser.add_argument("--out", default=None, help="output JSON path")
    args = parser.parse_args(argv)

    model = build_model(args.model)
    out_path = Path(args.out or f"results/{args.benchmark}_{args.model.replace(':', '_')}.json")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # local imports so --help works without deps installed
    if args.benchmark == "advbench":
        from benchmarks.advbench import run_advbench
        result = run_advbench(model, csv_path=Path(args.data_dir) / "harmful_behaviors.csv",
                              max_goals=args.max)
        payload = {"asr": result.asr.value, "refusals": result.refusals.value,
                   "provenance": result.provenance}
    elif args.benchmark == "xstest":
        from benchmarks.xstest import run_xstest
        result = run_xstest(model, csv_path=Path(args.data_dir) / "xstest.csv",
                            max_prompts=args.max)
        payload = {"safe_refusal": result.safe_refusal.value,
                   "unsafe_refusal": result.unsafe_refusal.value,
                   "parity_gap": result.parity_gap,
                   "provenance": result.provenance}
    elif args.benchmark == "truthfulqa":
        from benchmarks.truthfulqa import run_truthfulqa
        def chooser(question, options):
            response = model(question + "\n\nOptions:\n" + "\n".join(options))
            for i, opt in enumerate(options):
                if opt.strip().lower() in response.lower():
                    return i
            return -1
        result = run_truthfulqa(chooser, max_questions=args.max)
        payload = {"mc1": result.score.value, "n": result.score.denominator,
                   "provenance": result.provenance}
    elif args.benchmark == "bold":
        from benchmarks.bold import run_bold
        result = run_bold(model, data_dir=args.data_dir, domain="gender",
                          max_prompts_per_group=args.max or 10)
        payload = {"domain": result.domain, "disparity": result.disparity,
                   "groups": [g.__dict__ for g in result.groups],
                   "provenance": result.provenance}
    else:  # realtoxicityprompts
        from benchmarks.realtoxicityprompts import run_realtoxicityprompts
        from src.aisafety.safety.toxicity.classifier import ToxicityClassifier
        scorer = lambda t: ToxicityClassifier().score(t).score
        result = run_realtoxicityprompts(model, scorer=scorer, max_prompts=args.max)
        payload = {"mean_toxicity": result.mean_toxicity,
                   "toxic_rate": result.toxic_rate.value, "n": result.n,
                   "provenance": result.provenance}

    payload["model"] = args.model
    payload["note"] = SMOKE_DISCLAIMER if args.model in ("echo", "refusal") else ""
    out_path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    print(json.dumps(payload, indent=2, default=str))
    print(f"\nresult written to {out_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
