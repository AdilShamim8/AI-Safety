# Responsible research

This repository runs experiments in AI safety and AI security. Those
experiments must be conducted in a way that could itself survive the scrutiny
the course teaches. This page is binding for the repository's own experiments
and is taught as practice in chapter 24.

## Bounded experiments

1. **Local or explicitly authorized targets only.** The security projects
   (P07, P08, P10) run against applications built inside this repository,
   with synthetic documents and synthetic secrets. No external systems are
   probed. If a demonstration requires an external service, it requires the
   owner's explicit, recorded authorization first, and the target's terms.
2. **Bounded resources.** Agent exercises bound recursion depth, wall-clock
   runtime, memory, tool-call counts, and monetary spending in their
   configuration. A runaway loop is a design bug, not an accepted risk.
3. **No host trust by default.** Untrusted execution (model outputs, dataset
   content, retrieved documents) never receives host credentials, the Docker
   socket, or unrestricted filesystem/network access. Egress is disabled or
   filtered for the agent-security labs.
4. **Remote code execution off by default.** Dataset and model loading
   disables `trust_remote_code`-style execution paths unless a specific,
   reviewed exception is documented with the code.

## Data and secrets

- No real credentials in any fixture. Synthetic test values are labeled as
  synthetic (for example, published test-pattern card numbers, never real
  PANs).
- Personal information does not enter the repository. Datasets that contain
  person-level data are used only through their documented access path, under
  their license, with minimization applied before anything is stored.
- Raw experiment logs stay local unless sanitized; published outputs are the
  observable model behaviors, actions, scores, and concise explanations.
  Private reasoning traces are not fabricated, and sensitive raw prompts are
  not stored.

## High-consequence domains

Dangerous-capabilities material (chapter 20) stays at a **non-operational**
evaluation and governance level: no operational uplift, no working
capability demonstrations in high-consequence domains (CBRN-class topics,
offensive cyber operations). The chapter teaches evaluation design and
release decision-making, not the capabilities themselves.

## Reporting and disclosure

- Repository vulnerabilities: `SECURITY.md` route.
- Model-behavior findings from course experiments: recorded in the exercise
  report; reported to the model provider through its channel when warranted.
- Educational attack examples focus on the failure mechanism and the defense
  evaluation, not on maximizing impact.

## Citation and evidence integrity

- No fabricated authors, quotes, DOIs, benchmark numbers, licenses, or
  experimental evidence (this is also an acceptance criterion for the build).
- Negative results, failed attempts, exclusions, and deviations are reported
  with positive results.
- Self-review passes are labeled as self-reviews; nothing in this repository
  claims peer review or independent validation it did not receive.

## Ethical treatment of human subjects

The curriculum's exercises do not involve human subjects. If a contributor
adds anything that does (surveys, user studies), it requires IRB-equivalent
review or an explicit documented exemption under their institution's rules
before it can be merged. Do not improvise human-subjects research.
