---
name: blueprint
description: This skill writes an implementation plan to docs/plans/ before any code is written. Use when the user asks to "plan this", "write a plan", "make an implementation plan", "break this down", "how should we build X", or runs /blueprint, and for any multi-step change touching several files where the approach is not yet agreed. It produces a plan file only and does not implement anything.
---

# Blueprint: Write an Implementation Plan

Turn a request, spec, or conversation into a plan file someone (including a fresh Claude session using the implement skill) can execute step by step without re-deriving the design. Do not write or change production code while planning.

## Step 1: Understand the goal

- Restate the goal in one or two sentences: what changes for the user or system when this is done.
- Read the relevant code before designing: entry points, the modules that will change, existing patterns for similar features, tests, and project conventions in CLAUDE.md / README / CONTRIBUTING.
- Answer questions from the code when possible. Ask the user only about things the code cannot answer and that change the plan (scope, behavior choices, constraints). Ask them together, once, before writing. For a deeper interrogation, suggest the critique skill.

## Step 2: Decide the approach

- Pick an approach that fits existing patterns. When there is a real choice, record the options considered and why one was chosen, in a sentence or two each.
- Define what is explicitly out of scope.
- Identify risks: migrations, public API changes, performance, security, places with no test coverage.

## Step 3: Break it into tasks

Each task must be:

- **Small:** one focused change, typically one commit's worth.
- **Ordered:** dependencies come first; the codebase should build and tests should pass after each task where possible.
- **Concrete:** names the files to create or change and what changes in each.
- **Verifiable:** states how to prove it works (a specific test to add or run, a command, an observable behavior).

Prefer tracer-bullet ordering: get a thin end-to-end path working first, then widen. Put tests in the same task as the code they cover, written first when the behavior is well defined.

## Step 4: Write the plan file

- Path: `docs/plans/YYYY-MM-DD-<short-slug>.md` using today's date and a kebab-case slug of the goal. Create `docs/plans/` if missing. If a plan for the same goal already exists, update it instead of creating another.
- Use the structure in `references/plan-template.md`. Omit sections that would be empty.
- Write for a reader with no access to this conversation: include decisions and context the conversation established.

## Step 5: Hand off

Reply with:

1. The plan file path.
2. A short summary: approach, number of tasks, key risks, open questions.
3. Next steps: review/edit the plan, optionally stress-test it with the critique skill, then execute it with the implement skill.

Do not start implementing in the same turn unless the user explicitly asks.
