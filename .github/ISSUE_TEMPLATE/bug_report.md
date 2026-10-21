---
name: Bug report
about: Something in the repository's code or tooling does not work as documented
labels: bug
---

## What happened

A clear description of the wrong behavior. If it is a crash, paste the
traceback.

## What you ran

The exact command(s), including the working directory and tier (smoke /
pilot / full) if a project is involved.

## Expected vs. actual

What the documentation said would happen, and what happened instead.

## Environment

- OS:
- Python: output of `uv run python --version` (or `python3 --version`)
- Commit / release affected:
- Any relevant local changes:

## Minimality check

Did you try to reproduce on a clean checkout of the same commit? If not,
what makes that hard?
