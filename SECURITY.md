# Security policy

## Reporting a vulnerability in this repository

**Contact route (verified 2026-10-21):** GitHub private vulnerability reporting
is **not enabled** on this repository. To report a security issue in the
repository's own code, contact the repository owner through GitHub — open a
**draft security advisory** if available on the repository's Security tab, or
otherwise contact **@AdilShamim8** via GitHub's profile contact mechanism.
No email address is published by this repository; any address claiming to
belong to it is not ours.

A recommendation on record: the owner should enable GitHub private
vulnerability reporting (Settings → Code security → Private vulnerability
reporting) so reports have a confidential channel.

**What to include:** affected file(s) and commit, reproduction steps, impact
assessment, and any PoC. Please do not open a public issue for security
problems.

**Safe harbor:** good-faith research on this repository's code, conducted
without harming other users or the repository itself, will not be treated as
a violation of conduct.

## Two different things people call "security reports"

1. **A vulnerability in this repository** (code, CI configuration, dependency
   with a known CVE): report as above.
2. **A model behavior you find concerning** (a jailbreak against some model,
   a harmful output, a deceptive-looking response observed while running the
   course experiments): this is *not* a repository vulnerability and has no
   private channel here. Use the model provider's own reporting mechanism.
   The exercises in this course are designed to run against local or
   explicitly authorized targets; findings from them belong in the exercise's
   report template (`templates/experiment-report.md`), not in a security
   disclosure to this repository.

## Supported versions

| Version | Supported |
|---|---|
| `main` (development) | yes — fixes land on `main` |
| tagged releases | each release's README states its support status; no support commitment is implied beyond fixes to `main` |

## Scope

In scope: the repository's own Python code, test and CI configuration,
dependency manifests (report known-vulnerable pins), and documents that
instruct people to run commands. Out of scope: vulnerabilities in third-party
services we merely link to, and model behaviors (see above).

## Security posture of the course itself

The course deliberately demonstrates attack mechanisms in bounded, local,
synthetic settings:

- no real credentials or secrets in examples (synthetic secrets only);
- no external targets in the security labs (agent egress disabled or bounded
  by the exercise configuration);
- recursion, runtime, memory, tool calls, and spending bounded in agent
  exercises;
- host credentials and the Docker socket are never mounted into untrusted
  execution;
- remote code execution in dataset/model loaders is disabled by default, with
  documented exceptions only.

See `RESPONSIBLE_RESEARCH.md` for the full responsible-research rules.
