# Pull request

## What is this PR for?

One defensible purpose, stated plainly. If it mixes unrelated changes, split
it — the build history is a review sequence (see `planning/BUILD_PLAN.md`).

## The honesty checklist

- [ ] Every new substantive claim traces to a `research/source-register.yaml`
      entry (added in this PR if new), with the access level **actually
      achieved**.
- [ ] Maturity values in `planning/content-matrix.yaml` and any report
      statuses match reality on disk after this PR (no status inflation).
- [ ] No navigation links to files that do not exist (run
      `uv run python scripts/validate_repo.py .`).
- [ ] Third-party material (code, text, figures, data) is declared in
      `THIRD_PARTY_NOTICES.md` in this PR.
- [ ] No secrets, model weights, raw datasets, caches, or unreviewed raw
      logs in the diff.
- [ ] Experiments: numbers come from committed per-case outputs computed by
      a committed script — not hand-typed tables.

## Checks run locally

- [ ] `uv sync --frozen && uv run python scripts/validate_repo.py .`
- [ ] `uv run pytest`
- [ ] `uv run ruff check scripts tests` and `uv run black --check scripts tests`
      (or note why the diff intentionally leaves these failing)

## Status and planning updates

- [ ] `planning/STATUS.md` / `planning/content-matrix.yaml` updated in this
      same PR if the change completes or starts a tracked unit.

## Notes for reviewers

What to look at hardest, and what you deliberately did NOT do in this PR.
