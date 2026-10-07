# Plan Template

```markdown
# <Goal as a short title>

- **Status:** Draft | Approved | In progress | Done
- **Created:** YYYY-MM-DD
- **Branch:** <branch name, if known>

## Goal

<1–3 sentences: what will be true when this is done, and why it matters.>

## Context

<What the reader needs to know: current behavior, relevant modules and files, constraints, links to issues or specs. Decisions from the conversation that are not obvious from the code.>

## Approach

<The chosen design in a short paragraph or bullets.>

**Alternatives considered:**
- <Option> — <why not>

## Out of scope

- <Things deliberately not done in this plan>

## Tasks

- [ ] **1. <Imperative task title>**
  - Files: `path/to/file.ts` (change), `path/to/new.ts` (create)
  - Change: <what to do, specific enough to execute>
  - Verify: <test to add/run or command and expected result>

- [ ] **2. <...>**
  - Files: ...
  - Change: ...
  - Verify: ...

## Risks

- <Risk> — <mitigation>

## Open questions

- <Question> — <who/what resolves it>

## Log

<!-- implement appends dated notes here: deviations, decisions made during execution, blockers. -->
```

## Guidance

- 3–12 tasks is typical. More than ~15 suggests splitting into multiple plans or phases.
- A task's "Verify" line should be runnable by someone else and give an unambiguous pass/fail.
- Keep code in the plan to signatures, schemas, or tricky snippets. The plan says *what* and *where*; implementation happens during execution.
