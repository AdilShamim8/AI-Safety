# Chapter template

Copy this skeleton for each new chapter directory. Fill every section with
real content or remove the section deliberately (with a one-line reason in
the chapter README); a template section left as placeholder text means the
chapter is not complete. The chapter definition of done is the ten-element
checklist in `planning/BUILD_PLAN.md`.

```markdown
# Ch. NN — <Title>

## 1. Research question and failure pathway
The concrete failure this chapter helps you prevent, and the question it
answers. One paragraph, no throat-clearing. State why the question matters
to someone deploying a system, not just to a researcher.

## 2. Prerequisites, outcomes, scope exclusions
- Prerequisites: chapters + diagnostic tasks (with refresher pointers).
- Outcomes: measurable verbs (derive, design, distinguish, produce).
- Out of scope: what this chapter deliberately does not cover, and where
  it is covered instead.

## 3. Core explanation
Original treatment with defined notation. Introduce notation once, use it
consistently, and keep a notation table at the end. Equations only where
they carry weight; explain every symbol the first time.

## 4. Worked example / derivation / case
At least one carried all the way through: setup, steps, result, and what
the result does and does not establish.

## 5. Comparison of approaches
Assumptions, failure modes, and evidence quality per approach — a table if
that is clearer. Name the conditions under which each wins.

## 6. Counterexample / failure condition
Where the chapter's own methods fail. This section is mandatory: a chapter
without a failure mode is marketing.

## 7. Readings
2-4 essential primary sources: why each is assigned, which sections matter,
what to read skeptically. Each must exist in research/source-register.yaml
at the stated access level before the chapter is marked complete. Optional
deeper material clearly separated.

## 8. Exercises
One analysis/derivation exercise and one empirical/design/critical
exercise. Demanding = a prepared learner needs 1-3 hours and cannot
bullshit it.

## 9. Hints and solutions (separate file: solutions.md)
Hints here; full solutions or an assessor rubric in solutions.md, so the
prompts stay uncontaminated.

## 10. Completion
- Concrete artifact this chapter produces.
- Completion criteria (checkable statements).
- Prev/next/cross-track links.
- References (with claim-level citation anchors into the claims register).
- Notation table.
```

Cross-links to add when the chapter lands: glossary entries for new terms
(same commit), `planning/content-matrix.yaml` maturity update (same commit),
and paper notes for the chapter's core readings (same phase, not deferred to
the end).
