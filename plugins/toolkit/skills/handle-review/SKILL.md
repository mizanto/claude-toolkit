---
name: handle-review
description: This skill evaluates code review feedback critically before acting on it. Use when the user shares review comments, says "address the review", "handle these comments", "fix the PR feedback", "what do you think of this review", pastes reviewer notes, or runs /handle-review, optionally with a PR number. Also use when acting on findings from an automated or AI code review.
---

# Handle Code Review Feedback

Treat review comments as claims to check, not instructions to obey. A reviewer can be wrong, missing context, or right for a reason different from the one they gave. Agree only with what holds up against the code, and say so plainly when it does not.

## Step 1: Collect the feedback

- If the user pasted comments or a review report, use that.
- If given a PR number or URL and `gh` is available, read it (read-only): `gh pr view <n> --comments` and `gh api repos/{owner}/{repo}/pulls/<n>/comments` for inline comments with file and line.
- Number each distinct point. Split comments that contain several requests.

## Step 2: Check each point against the code

For each point:

1. Restate what the reviewer is asking for and the problem they believe exists.
2. Read the referenced code and enough surrounding context (callers, tests, related modules) to judge it.
3. Verify factual claims directly where possible: run the test, reproduce the edge case, check the docs or the actual API behavior. Do not accept "this will throw" or "this is O(n²)" without checking.
4. Classify:
   - **Agree — fix:** correct and in scope.
   - **Agree — defer:** correct but out of scope for this change; propose a follow-up.
   - **Disagree:** incorrect or not worth the cost; give the technical reason with evidence (code reference, test result, doc link).
   - **Unclear:** cannot judge without more information; state exactly what is missing.

Avoid performative agreement ("Great catch!", "You're absolutely right") and avoid reflexive pushback. Base each verdict on what the code shows.

## Step 3: Present the triage before changing code

Show a table:

| # | Feedback (short) | Verdict | Reason / evidence | Proposed action |
| --- | --- | --- | --- | --- |

Then wait for the user to confirm or override verdicts. Do not edit code for points the user has not agreed to address. If the user says to proceed with everything marked "Agree — fix", that is enough.

## Step 4: Apply agreed fixes

- Address one point at a time; keep each fix minimal and focused on the point raised.
- When a comment reveals a pattern (the same issue elsewhere), mention the other occurrences and fix them only if the user agrees.
- After all fixes, run the relevant checks following the verify-done skill.

## Step 5: Draft replies

Draft a short reply per point for the user to post (never post them):

- Fixed: what changed, in one line, with the commit or file reference if known.
- Deferred: acknowledge and link or describe the follow-up.
- Disagree: the reasoning and evidence, stated respectfully and specifically; invite the reviewer to point out what was missed.
- Unclear: the specific question.

Do not commit, push, resolve threads, or post comments; leave those to the user.
