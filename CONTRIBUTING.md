# Contributing to AI Safety

Thanks for your interest in improving this repository. Safety tooling benefits
from diverse reviewers — practitioners, researchers, auditors, and policy
analysts all catch different failure modes.

## Getting started

1. Fork the repository and create a branch:
   ```bash
   git checkout -b feat/my-contribution
   ```
2. Install development dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Make your change with tests. Run the suite before committing:
   ```bash
   make test          # pytest with coverage
   make lint          # ruff + black --check
   ```

## Commit conventions

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` new tooling or benchmark harness
- `docs:` documentation additions and corrections
- `test:` test additions
- `fix:` bug fixes
- `chore:` tooling, dependencies, configuration

Commits in this repository are intentionally **small and incremental** — one
logical change per commit — so the history reads like an audit trail.

## Content standards

Because this repository documents real research, we hold content to a high
evidentiary bar:

- **Cite primary sources.** Papers must be linked by arXiv ID or DOI;
  incidents must link to a news report, court filing, or official statement.
- **No fabricated data.** Never invent benchmark numbers, dataset sizes, or
  quotations. If a number is uncertain, say so or omit it.
- **Label evaluations.** Any performance figure produced by code in this repo
  must state the model, dataset, split, date, and random seed used.
- **Attack content policy.** Red-teaming documentation may describe attack
  *techniques* (prompt injection patterns, GCG, many-shot jailbreaking) and
  cite public research, but must not include operational payload strings
  beyond those already published in the cited papers.

## Reporting safety issues

For vulnerabilities in this repository itself, see [SECURITY.md](SECURITY.md).
For dangerous behavior you observed in a third-party model, please report it
to that model's vendor (most vendors run bug bounties for safety issues, e.g.
OpenAI's, Google's, and Anthropic's).

## Pull request process

1. Ensure `make test` and `make lint` pass locally.
2. Update `CHANGELOG.md` under the *Unreleased* section.
3. Describe *why* the change matters, not just what changed.
4. Maintainers review within a week; small, focused PRs land fastest.

## Code of conduct

By participating you agree to uphold the [Code of Conduct](CODE_OF_CONDUCT.md).
