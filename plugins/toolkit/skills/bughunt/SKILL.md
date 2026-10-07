---
name: bughunt
description: This skill finds the root cause of a bug, test failure, or performance regression before fixing it. Use when the user reports something broken, throwing, failing, flaky, or slow, says "debug this", "why is this failing", "find the root cause", "hunt this bug", "this used to work", or runs /bughunt. Also use after a first fix attempt did not work.
---

# Bughunt: Find the Root Cause, Then Fix

Do not propose or apply a fix until the cause is identified and supported by evidence. Patching symptoms produces fixes that do not hold and hide the real problem.

## Step 1: Pin down the symptom

- Collect the exact error, stack trace, logs, failing test output, or measured slowness. Read them fully, including the first error rather than only the last.
- Establish expected versus actual behavior in one sentence each.
- Note what changed recently: `git log --oneline -n 20`, recent dependency or config changes, environment differences (works locally but not in CI?).

## Step 2: Reproduce it

- Find the smallest reliable reproduction: a failing test (preferred), a script, a command, or exact steps.
- Write the reproduction as an automated test when feasible; it later proves the fix and prevents regressions.
- For flaky failures, run repeatedly to measure the failure rate and look for ordering, timing, shared state, or environment dependence.
- For performance problems, measure first with a repeatable benchmark or timing; record the baseline number.
- If it cannot be reproduced, say so and gather more evidence (logging, user steps, environment details) rather than guessing.

## Step 3: Narrow it down

Form hypotheses and test them one at a time, cheapest and most likely first:

- Write each hypothesis as a falsifiable statement: "the cache returns stale data because the key omits the locale".
- Design a small experiment that distinguishes it: a targeted log line, an assertion, a debugger breakpoint, a minimal input, toggling one variable.
- Use binary search when the cause location is unknown: comment out halves, bisect inputs, or bisect history with `git bisect` (ask before running it, since it changes the checked-out commit; finish with `git bisect reset`).
- Change one thing per experiment and record each result, including dead ends.

Trace data backward from where it goes wrong to where it was first wrong. The root cause is the earliest point where behavior diverges from intent, not where the error surfaces.

## Step 4: Confirm the cause

Before fixing, be able to state: "X happens because Y, shown by Z." Confirm by predicting a behavior the cause implies and checking it. If the explanation does not account for every observed symptom, keep digging.

## Step 5: Fix and verify

- Fix the cause at its origin with the smallest correct change. Avoid defensive patches at the symptom site unless they are also genuinely needed.
- Make the reproduction test pass; run the surrounding tests. Follow the verify-done skill.
- Check for the same bug pattern elsewhere and mention it.
- Remove temporary logging and experiments.

## Stop rule

If three fix attempts fail, stop changing code. Summarize what is known, what was ruled out, and the remaining hypotheses, then reassess the approach with the user. Repeated failed fixes usually mean the mental model of the system is wrong.

## Report

Give: symptom, root cause (with evidence), the fix, the verification results, and any related risks or follow-ups.
