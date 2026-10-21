# Safety-case template

Used by chapter 22 and project P10. A safety case is an argument, made of
claims backed by evidence under stated assumptions, that a specific system
is acceptably safe in a specific deployment context. A compliance checklist
is not a safety case; an argument without rebuttals is not one either.

```markdown
# Safety case: <system / deployment context>
Version + date · Author · System commit/config · Deployment scope

## 1. Context and claim scope
The deployment: what the system does, for whom, with what permissions and
integration surface. The top-level claim in one sentence, in the
context-relative form: "in this defined workflow, with these controls, the
evidence supports keeping these specified risks below these stated limits."

## 2. Claim structure
Decompose the top-level claim into sub-claims. Format per claim:

### Claim C<k>: <statement>
- **Evidence E<k>.n:** what was actually run/measured, with report/run IDs,
  denominators, and uncertainty. Evidence must be recorded, not asserted.
- **Assumption A<k>.n:** what must hold for the evidence to carry; each
  with its failure condition (what observation would falsify it).
- **Rebuttal R<k>.n:** the strongest honest objection to this claim, and
  the response (or the concession, if the objection stands).
- **Residual risk:** what remains unmitigated after honest accounting.

## 3. Argument pattern
State the pattern used (e.g., enumerative over the risk register,
probabilistic over failure rates, elimination over causes) and why it fits.
If the pattern has known weaknesses (they all do), say which apply.

## 4. Evidence index
Table of every run/report referenced, with paths and statuses. No
unreferenced "trust us" artifacts; no referenced-but-nonexistent runs.

## 5. Gaps and conditions of use
- Open gaps: claims not yet supported, with the evidence needed.
- Conditions of use: what changes to the system, context, or adversary
  invalidate this case (model revision, new tool, new user population,
  adaptive attacker budget increase).
- Decision impact: what deployment decision this case actually changes,
  and who made it.

## 6. Sign-off
Who prepared it, who reviewed it (self-review labeled as self-review), and
what independent review would still be required before operational reliance.
```
