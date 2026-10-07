---
name: implement
description: This skill implements work step by step, verifying each step — from a plan file in docs/plans/ when one exists, otherwise from a clear, small request. Use when the user says "implement the plan", "run the plan", "execute the plan", "continue the plan", "next task", "implement this", "build this", or runs /implement, optionally with a plan file path. Also use to resume a partially completed plan in a new session.
---

# Implement

Build the requested change in small, verified steps. When a plan file exists, it is the source of truth for scope and progress, so work can stop and resume in any session.

## Step 1: Choose the mode

- **Plan mode** — the user gave a plan path, referred to "the plan", or `docs/plans/` contains an unfinished plan (status not Done) that matches the request. If several plausible plans exist, ask which one.
- **Direct mode** — no matching plan, and the request is small and clear (a few files, approach obvious from the code).
- **Plan first** — no matching plan, and the work is large or the approach is unclear (many files, design choices, migrations, public API changes). Suggest the blueprint skill and stop, unless the user says to proceed anyway.

## Step 2a: Plan mode — load and reconcile

- Read the whole plan: goal, context, approach, out-of-scope, tasks, open questions, log.
- If open questions block the next task, ask them before starting.
- Run `git status` and `git log --oneline -n 10`. Check that tasks marked done are actually in the code, and whether unchecked tasks were already done.
- If the code has diverged from what the plan assumes, report the mismatch and propose a plan update before continuing.
- Set the plan status to "In progress" if it was Draft or Approved.

## Step 2b: Direct mode — outline the steps

- Read the relevant code and the project's conventions.
- State the steps in a short numbered list (files and change per step, plus how each will be checked) and proceed. Ask first only if a step is destructive, outward-facing, or the request is ambiguous in a way that changes the result.

## Step 3: Execute one step at a time

For each task (plan mode) or step (direct mode):

1. Announce it in one line.
2. Implement only that step, following the plan's approach and the project's existing patterns. Write the step's tests first when the behavior is well defined.
3. Verify it: run the step's check plus directly affected tests, following the verify-done skill. A step is complete only when a fresh run proves it.
4. In plan mode, check the task's box in the plan file.
5. Give a short progress line: done, evidence, what is next.

Do not batch several steps into one change or move on while the current step fails verification.

## Step 4: Handle deviations

Stop and ask the user when:

- The planned approach turns out not to work, or a clearly better one appears.
- A step needs changes beyond its expected files that alter scope or touch out-of-scope areas.
- Verification fails and the fix is not obvious after a focused attempt (switch to the bughunt skill if it is a real bug).
- An action is destructive or outward-facing (migrations on shared data, pushes, deletions).

In plan mode, when the user approves a change of course, update the plan's tasks and add a dated entry under **Log** with what changed and why. Never silently diverge from the plan.

## Step 5: Commits

Do not commit unless the user asked for commits during this work. At natural checkpoints, suggest committing and offer the commit-message skill for the message.

## Step 6: Finish

1. Run the broader checks (relevant full test suite, typecheck, lint, build) per verify-done.
2. In plan mode, set the plan status to Done and add a final Log entry.
3. Summarize: what was built, evidence it works, deviations, follow-ups. Suggest the pr-description skill if the work is on a branch.

If work must stop partway in plan mode, make sure the plan file shows exactly which tasks are done and log where things were left, so the next session can resume with the implement skill.
