---
name: commit-message
description: This skill drafts a Conventional Commits message from the currently staged git changes. Use when the user asks to "write a commit message", "generate a commit message", "conventional commit for my staged changes", "what should I commit this as", "suggest a commit message", or runs /commit-message. It proposes the message only and never runs git commit.
---

# Conventional Commit Message from Staged Changes

Draft a commit message that follows the Conventional Commits 1.0.0 spec, based strictly on what is staged. Propose the message only — never run `git commit`, `git add`, `git reset`, or any command that changes repository state.

## Step 1: Inspect the staged changes

Run these read-only commands:

```bash
git rev-parse --is-inside-work-tree
git diff --cached --stat
git diff --cached
```

- If not inside a git repository, say so and stop.
- If nothing is staged, say so. If `git status --short` shows unstaged or untracked changes, mention them and suggest `git add <paths>`; do not stage anything.
- For very large diffs, start from `--stat` and read the diff per file (`git diff --cached -- <path>`), skipping lockfiles and generated files beyond noting that they changed.

Base the message only on staged content. Ignore unstaged changes.

## Step 2: Learn the repository's conventions

Check, in this order, and let anything found override the defaults:

1. Commitlint or similar config: `commitlint.config.*`, `.commitlintrc*`, a `commitlint` key in `package.json`, `.czrc`, `.cz.toml`, or `[tool.commitizen]` in `pyproject.toml`. Respect allowed types, scopes, case rules, and length limits.
2. Recent history: `git log --oneline -n 20`. Reuse the scope names, casing, and style already in use (e.g. `feat(api):` vs `feat(API):`). If the history does not use Conventional Commits, still use the spec but mention that.
3. Contributing docs (`CONTRIBUTING.md`) if they mention commit format.

## Step 3: Classify the change

Choose the single type that best describes the *intent* of the change. See `references/types-and-rules.md` for the type table and edge cases. Key heuristics:

- New user-visible capability → `feat`. Corrects wrong behavior → `fix`.
- Restructuring with no behavior change → `refactor`.
- Only tests → `test`; only docs/comments → `docs`; only build/deps → `build`; only CI config → `ci`.
- When in doubt between `feat` and `fix`, ask: did the code previously fail to do what it claimed? If yes, `fix`.

Pick a scope from the main area touched (package, module, directory, or component), matching existing scopes from history when possible. Omit the scope if the change spans the whole project or no natural scope exists.

Detect breaking changes: removed or renamed public APIs, changed function signatures, changed config keys or CLI flags, changed response formats, dropped runtime/platform support. Mark with `!` after the type/scope and add a `BREAKING CHANGE:` footer describing what users must do.

## Step 4: Check for mixed changes

If the staged changes contain clearly unrelated work (e.g. a bug fix plus an unrelated refactor, or two independent features):

1. Warn the user that the staged set mixes concerns.
2. Suggest a split: list each logical commit with its proposed message and the files (or hunks) belonging to it, and the commands to do it, e.g. `git restore --staged <paths>` then `git add -p`.
3. Still provide one combined message using the dominant type, in case the user prefers a single commit.

Do not warn for changes that naturally belong together (a feature plus its tests and docs is one `feat` commit).

## Step 5: Write the message

Format:

```
<type>(<scope>)!: <subject>

<body>

<footers>
```

Subject rules:
- Imperative mood, present tense: "add", not "added" or "adds".
- Lowercase first letter after the colon (unless repo config says otherwise), no trailing period.
- Keep the whole first line at 72 characters or less (aim for 50); respect any configured limit.
- Describe what the change does, not which files changed.

Body — include only when the change is non-trivial (multiple files with a shared purpose, non-obvious motivation, behavior changes, or anything a reviewer would ask "why?" about):
- Blank line after the subject; wrap at 72 characters.
- Explain *why* and any notable *what*; the diff already shows *how*.
- Short bullet points are fine for several related changes.
- Skip the body for trivial changes like typo fixes, version bumps, or one-line obvious fixes.

Footers — include only when applicable:
- `BREAKING CHANGE: <description>` for breaking changes.
- Issue references only if they appear in the branch name (`git branch --show-current`), the diff, or the user's request, e.g. `Refs: #123` or `Closes: PROJ-42`. Never invent issue numbers.

## Step 6: Present the result

Output:

1. The proposed message in a fenced code block so it can be copied as-is.
2. One or two lines explaining the type and scope choice if not obvious.
3. A ready-to-run command, using a heredoc for multi-line messages:

   ```bash
   git commit -F- <<'MSG'
   feat(auth): add token refresh on 401 responses

   Expired access tokens previously forced users to log in again.
   MSG
   ```

   For single-line messages, `git commit -m "<message>"` is fine.

4. If relevant, the mixed-change warning and split suggestion from Step 4.

Offer to adjust the type, scope, wording, or detail level. Do not run the commit, even if asked to "just do it" within this skill's flow — tell the user to run the command themselves.
