# Incident-review template

Used by `notes/incidents/`. The taxonomy is strict: a **production incident**
happened to a deployed system; a **controlled demonstration** was staged in
a lab; a **tabletop scenario** is an exercise; a **hypothetical failure
mode** is an argument. Every note states which it is, and never attributes
intent or root cause that an investigation did not establish.

```markdown
# Incident review: <name>
Class: production incident | controlled demonstration | tabletop scenario |
hypothetical failure mode · Date of event · Date of this note
Sources: SRC-IDs (first-party reports preferred) · Access levels recorded

## 1. What happened (observable facts only)
The sequence of observable events, with timestamps where published. No
motive language ("the model wanted..."), no mechanism claims beyond what
the sources establish. Where sources disagree, both versions are recorded.

## 2. System and context
The system involved, its deployment context, and the controls that existed
at the time. What the system was supposed to do.

## 3. What the investigation established
Only the conclusions the actual investigation (or postmortem) reached, with
each attributed to its source. Root cause AS REPORTED, distinguished from
root cause as hypothesized by commentators.

## 4. What remains unknown
The open questions the investigation left, and any popular narratives that
go beyond the evidence (labeled as such, with what evidence would be needed
to confirm them).

## 5. Lesson extraction (mapped to course chapters)
- Which failure pathway this illustrates (with chapter cross-links).
- Which controls would have caught it, and their cost.
- What this incident does NOT demonstrate (the overreach to avoid).

## 6. Course application
The exercise or project this incident feeds (or would feed), and what
students should derive from it.

## 7. Source register updates
Which SRC entries were added/updated for this note, with access levels.
```

Rules: first-party incident reports outrank press coverage; if only press
coverage is available, the note is labeled accordingly; intent attribution
("malicious", "deliberate") requires an investigation finding, not a vibe.
