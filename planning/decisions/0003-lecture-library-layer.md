# ADR-0003: the lecture library — video-course companions as a repository layer

Date: 2026-10-27 · Status: accepted

## Context

The owner directed (2026-10-27) that four external courses — Harvard
CS 2881 (Boaz Barak), the Google DeepMind AGI Safety Course, the
CAIS AI Safety, Ethics & Society course, and the Safeshield Training
governance series — be transcribed into the repository, with their
information-gathering and organization methods documented, and
integrated with the 24-chapter course.

## Decision

Add a `courses/` layer of **companion notes** rather than transcripts
or copies: per course, a course page (identity, verified video
index, chapter mapping), one original note per lecture anchored to
the course's published scope and readings, per-course pedagogy
analyses, and study plans. Register every playlist, channel, and
course page with honest access levels; verify every URL live before
it lands in AWESOME.md; integrate by watching-companion blocks in
all 24 chapter READMEs and watching pointers in all 24 solutions
files; pin the structure with tests.

## Consequences

- (+) The repository becomes the complete written map of the four
  courses — every video, every published reading list, every
  experiment description — without reproducing any protected
  content, consistent with the no-spoken-content rule the video
  library has held since it opened.
- (+) The chapter spine gains a scheduled video layer (the watch
  guide) without changing its own sequence or hours.
- (−) The notes' strength is capped at "announced-scope companion":
  lectures can surprise beyond their syllabus, and the notes cannot
  know. The honesty markers state this per note.
- (−) Playlist structure is perishable (courses publish recordings
  on delay); the register prices the fetch date, and re-verification
  is scheduled through the MAINTENANCE rotation discipline.