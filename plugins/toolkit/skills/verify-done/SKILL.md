---
name: verify-done
description: This skill makes Claude prove work is complete before saying so. Use before claiming a task is done, a bug is fixed, tests pass, or a build works; before suggesting a commit or PR; when finishing a step of a plan; or when the user asks "is it done?", "did you check?", "verify this", or runs /verify-done.
---

# Verify Before Claiming Done

Never report work as done, fixed, or passing on the basis of having written the code. Report only what a command run *in this session, after the last change* has shown.

## Step 1: List the claims

Write down what is about to be claimed, as concrete statements. Typical claims:

- The requested behavior works (name the behavior, not "the feature").
- The bug no longer reproduces.
- Tests pass / types check / lint is clean / it builds.
- Nothing else broke.

Include implicit claims. "Fixed the login bug" also claims "existing login tests still pass".

## Step 2: Find the checks for each claim

Discover how this project verifies things rather than guessing:

- Scripts in `package.json`, `Makefile`, `justfile`, `pyproject.toml`, `Cargo.toml`, `*.xcodeproj` schemes, CI workflow files (`.github/workflows/*`), and CLAUDE.md / README instructions.
- Prefer the narrowest check that proves the claim first (the one test file, the one package), then the broader suite if the change could have wider effects.

Map each claim to a check:

| Claim | Check |
| --- | --- |
| Bug no longer reproduces | The reproduction command or failing test from before the fix |
| Behavior works | A test exercising it, or running the app/CLI/endpoint and observing output |
| Nothing else broke | The relevant test suite, typecheck, lint, build |

If a claim has no possible check (no tests, cannot run the app), say so explicitly instead of dropping the claim silently.

## Step 3: Run the checks fresh

- Run every check after the final edit. Output from before the last change does not count.
- Read the actual output. Look for failures, skipped tests, warnings that indicate real problems, and "0 tests ran".
- A command that exits 0 but did not exercise the change (wrong filter, test not collected, cached build) proves nothing; fix the invocation and rerun.
- If a check fails, the work is not done. Fix and rerun, or report the failure.

## Step 4: Report with evidence

Report in this shape:

- **Verified:** each claim with the command run and the relevant result (e.g. `npm test -- auth` → 14 passed, 0 failed).
- **Not verified:** anything that could not be checked and why, plus what the user should check manually.
- **Failed:** anything that failed, with the error.

Avoid hedged success language: "should work", "probably fixed", "looks good". Either the evidence shows it or the report says it was not verified.

Do not stage, commit, or push as part of verification.
