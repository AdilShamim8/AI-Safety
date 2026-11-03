# Threat Modelling our Agentic Application

*Course companion note · [AI Security & Guardrails](README.md) ·
module 4 lesson 1 (announced) · [course page](https://learnwith.campusx.in/courses/AI-Security--Guardrails-6ad0c6fb17f468ce3c894053)*

## Where this lesson sits

The agent case study opens. Listed with duration 0 on the course page — announced in the outline, not yet published at verification time (2026-11-03); the platform marks the whole outline TENTATIVE. The companion note is written to the case study's announced scope, which the published description states in full: the doctor-booking agent, the five-step framework run on it, and why write and delete capabilities make an agent more dangerous than a RAG.

## Core ideas, explained

### 1. The doctor-booking agent, as the description states it

The case study's system: an agent for a website that lists doctors. It searches doctors' pages with a tool, checks free slots and books appointments through an MCP server, and learns from past conversations through a shared memory. Anyone on the internet can use it without logging in — the standing condition the threat model has to accept.

### 2. Write and delete make an agent more dangerous than a RAG

The case study's central claim, from the description: running the same five-step framework, you see how write and delete capabilities make an agent more dangerous than a RAG — an attack no longer just changes an answer, it makes the agent take real actions, such as leaking patients' details, steering patients to one doctor, or cancelling bookings. The capability lens prices this exactly: the RAG's worst case is a wrong answer; the agent's worst case is a wrong action.

### 3. The four security layers the case study builds

From the published description, the announced scope the lesson teaches: a jailbreak gate (a separate guard model reading every message along with recent turns, inside delimiters, blocking authority claims, requests for other people's data, and attempts to override the agent's rules); a guard model on every tool and MCP result (stopping indirect prompt injection hidden in doctors' pages and schedule notes); memory protection (custom instructions and a judge that checks every write, so personal data and poisoned lessons never reach the shared memory); and output guardrails checking every answer against the platform's policies — the fee cap, no promised cures, no links to other sites, no other patients' data.

### 4. Why this lesson's honest status is different

The verification note this companion carries: the lesson is announced with duration 0. Its scope is known from the description; its recording was not available to check against. The note states what is announced, and the honesty section says exactly that.

## Worked example (practitioner walk-through)

Run the capability table on the doctor-booking agent and watch the danger change kind. The system: a web listing of doctors; an agent that searches doctors' pages with a tool, checks free slots and books through an MCP server, and learns from past conversations in a shared memory — usable by anyone without login. The table's honest rows: the tool — read external pages (which you do not control: injection lives there); the MCP server — write the schedule (a real action in the world); the memory — read and write across sessions (whatever it holds, the agent believes); the answer — write to the patient. Read the ranking: the RAG's worst case was a wrong answer; this system's worst cases are wrong actions — a poisoned page that says "book Dr. X for everyone" becomes a booking script; a memory that has learned "patients prefer Dr. X" becomes a steering engine; a jailbreak that claims authority becomes a canceller of bookings. That is the course's central claim as a worked table: write and delete price higher than read, and the defense plan changes shape accordingly — a gate on the conversation, a guard on every tool result, a judge on every memory write.

## Through-lines to this repository's chapters

- [Ch. 14](../../chapters/14-agent-tool-memory-mcp-security/README.md) — the agent surface — tools, memory, MCP — at chapter depth.
- [the P08 project](../../projects/p08-control-and-monitoring-protocol/README.md) — the repository's own control-and-monitoring exercise for agent systems.
- [Ch. 08](../../chapters/08-ai-control-and-monitoring/README.md) — checking every action as the control pattern.

## What only this course does

The only lesson in the library whose case study is an agent with tools, MCP booking, shared memory, and no login — and the wrong-answer-versus-wrong-action distinction as its organizing claim.

## Honesty note

This lesson is listed with duration 0 on the course page — announced in the outline, not yet published at verification time. The note is written to the case study's announced scope, which the course's published description states in full; the recording was not available to check against. Original study companion written to the lesson's announced scope. The course page (public, no login; its outline is marked TENTATIVE by the platform itself) was fetched and read in full on 2026-11-03 and is registered as SRC-CURR-016; the lesson titles, order, and durations are taken from its published curriculum data, and the teaching beats are grounded in the page's own published description. No video was watched by this repository, nothing behind the paywall is reproduced, and no lesson content beyond the page is transcribed. Where an idea is also carried by a source this repository registers, the register ID appears and the source is linked.
