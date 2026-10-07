---
name: pr-description
description: This skill drafts a pull request title and description from the commits and diff between the current branch and its base branch. Use when the user asks to "write a PR description", "describe this PR", "draft a pull request", "summarize my branch for a PR", "generate PR notes", or runs /pr-description, optionally naming a base branch (e.g. "/pr-description develop"). It proposes the text only and never creates or edits a pull request.
---

# Pull Request Description from Branch Changes

Draft a PR title and description covering everything on the current branch that is not on the base branch. Propose the text only — never run `gh pr create`, `gh pr edit`, `git push`, or any command that changes a repository or remote.

## Step 1: Determine the branch and base

Run read-only commands:

```bash
git rev-parse --is-inside-work-tree
git branch --show-current
```

- If not inside a git repository, say so and stop.
- If on a detached HEAD, use `HEAD` and mention it.

Choose the base branch in this order:

1. A base the user named (argument or request).
2. The remote default branch: `git symbolic-ref --short refs/remotes/origin/HEAD` (strip the `origin/` prefix for display).
3. The first of `main`, `master`, `develop` that exists (`git rev-parse --verify --quiet <name>`).

Prefer comparing against `origin/<base>` when it exists, so stale local branches do not skew the result. If the current branch *is* the base, say there is nothing to describe and stop.

## Step 2: Collect the changes

```bash
git log --no-merges --format='%h %s%n%b' <base>..HEAD
git diff --stat <base>...HEAD
git diff <base>...HEAD
```

- Use three dots for the diff so only this branch's changes appear, not changes made on the base since branching.
- If there are no commits ahead of base, say so and stop.
- For large diffs, work from `--stat` and the commit messages, then read per-file diffs (`git diff <base>...HEAD -- <path>`) for the important files. Note lockfiles and generated files without reading them.
- Check `git status --short`. If there are uncommitted or unpushed changes, mention that the description covers committed work only, and whether the branch has been pushed (`git rev-parse --abbrev-ref @{upstream}` fails if not).

## Step 3: Learn the repository's conventions

1. **PR template** — look for, in order: `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE/*.md`, `docs/pull_request_template.md`, `pull_request_template.md` (any case). If one exists, fill in its sections exactly in its order and headings instead of the default structure. Keep checkboxes; tick only items the diff actually proves (e.g. "tests added" when test files changed). Leave the rest unticked.
2. **Title style** — check recent merged PR titles with `git log --merges --oneline -n 15 <base>` and recent commit subjects with `git log --oneline -n 20 <base>`. If the repo uses Conventional Commits, write the title in that format (see the commit-message skill's rules: `type(scope): subject`, imperative, lowercase, no period). Otherwise match the existing style.
3. **Contributing docs** — skim `CONTRIBUTING.md` for PR requirements if present.

## Step 4: Understand and group the changes

Read the commits for intent and the diff for substance. Commit messages can be stale or vague ("wip", "fix") — trust the diff when they disagree.

- Identify the single main purpose of the branch. That becomes the title and summary.
- Group supporting changes by theme (e.g. "API", "UI", "tests", "refactoring") rather than listing files or commits one by one.
- Detect breaking changes using the same signals as for commits: removed/renamed public APIs, changed signatures, config keys, CLI flags, response shapes, raised minimum versions, required migrations.
- Look for issue references in the branch name (e.g. `feat/PROJ-123-...`, `fix/456-...`), commit messages, and the user's request. Never invent issue numbers.
- If the branch mixes unrelated work, say so in the reply (not in the description) and suggest splitting it into separate PRs.

## Step 5: Write the title and description

**Title:** at most 72 characters, describes the outcome, not the files. Imperative mood.

**Description:** use the repo template if found. Otherwise use the default structure in `references/description-template.md`, dropping any section that would be empty or filler. Guidelines:

- Lead with *why*: the problem or goal, in one to three sentences. Reviewers should understand the point before reading code.
- Describe *what* changed at the level a reviewer needs — behavior, design decisions, tradeoffs. Do not narrate the diff line by line.
- Say how it was tested only from evidence: test files added or changed, CI config, or what the user said. If there is no evidence, leave a short placeholder for the user to fill in (e.g. `<!-- describe manual testing -->`) rather than claiming testing happened.
- Call out anything reviewers should look at closely: risky areas, migrations, new dependencies, config or env var changes, follow-up work.
- Keep it scannable: short paragraphs and bullets. Scale length with the change — a one-line fix gets a two-line description.
- Use `Closes #123` / `Fixes #123` only for issues the change fully resolves; otherwise `Refs #123`.

Do not claim things the diff does not show (performance gains, test coverage, screenshots). Do not include a commit list unless the repo template asks for one.

## Step 6: Present the result

Output:

1. The title on its own line.
2. The description in a fenced `markdown` code block so it can be copied as-is.
3. A ready-to-run command, using a heredoc so formatting survives:

   ```bash
   gh pr create --base main --title "feat(auth): add token refresh on 401 responses" --body-file - <<'MSG'
   ## Summary
   ...
   MSG
   ```

   If `gh pr view --json number,url` (read-only) shows a PR already exists for the branch, give `gh pr edit --title "..." --body-file - <<'MSG'` instead. If the branch is not pushed, put `git push -u origin <branch>` first. If `gh` is not installed, skip the command and say the text can be pasted into the PR form.

4. Brief notes outside the description: placeholders the user should fill in, a mixed-work warning, or uncommitted changes that are not covered.

Offer to adjust the tone, length, or sections. Do not run the commands — the user runs them.
