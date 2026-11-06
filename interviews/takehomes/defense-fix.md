# Take-home: the defense fix — the P07 format

**Navigate:** [← take-homes](README.md) · [red-team bank](../questions/red-team-reading.md)

**The prompt as issued.** "Here is a small LLM app with an injection
surface. Harden it, then tell us what your hardening does not stop."

**The mapping.** [P07](../../projects/p07-injection-defense/README.md):
the named threat is the registered OWASP LLM01 (prompt injection);
the canonical indirect case is the
[Greshake note](../../research/notes/06-greshake-indirect-injection.md)
— retrieved content as the injection vector, which no
filter-the-input defense fully closes.

**The rubric.**
1. **Threat named before code.** LLM01 (and LLM05 if outputs flow to
   a consumer — the OWASP entry's own distinction).
2. **Defense measured, not asserted.** Before/after on the same case
   set — the paired ledger again, in security clothes.
3. **The not-covered list.** The second half of the prompt IS the
   test: distribution shift in the wild, indirect vectors the suite
   does not generate, and the admission that the suite is a proxy.
4. **No security theater.** A grader downgrades elaborate filtering
   that was never evaluated; the P07 habit is evaluate-then-claim.

**The honest tiers expected.** Coverage of the generated suite at
stated rates; the wild-distribution tier marked not-executed with the
reason. The submission that promises less and shows more wins this
format.
