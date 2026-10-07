# claude-toolkit

Claude Code plugin marketplace with everyday engineering skills. It contains the **toolkit** plugin:

| Skill | What it does |
| --- | --- |
| `/commit-message` | Drafts a Conventional Commits message from staged git changes |
| `/pr-description` | Drafts a pull request title and description from the branch's changes against its base |
| `/blueprint` | Writes an implementation plan to `docs/plans/` before any code is written |
| `/implement` | Implements step by step with verification — from a plan file (resumable) or directly for small tasks |
| `/verify-done` | Proves work is complete with fresh command output before claiming it |
| `/bughunt` | Finds the root cause of a bug or regression before fixing it |
| `/handle-review` | Checks review feedback against the code before acting on it |
| `/critique` | Stress-tests a plan or idea with a one-question-at-a-time interview |
| `/agent-docs` | Writes skills, CLAUDE.md/AGENTS.md files, subagents, and agent prompts |

Plus an always-on **git-safety** hook (see below).

Skills trigger automatically when your request matches, or explicitly as `/toolkit:<skill>`. No external services or credentials required; the hook needs `python3`.

## Skills

### commit-message

Ask Claude to "write a commit message" (or run `/commit-message`) with changes staged. The skill:

- Reads only staged changes (`git diff --cached`)
- Follows your repo's conventions: commitlint/commitizen config and the scopes and style in recent history
- Picks the type, scope, and breaking-change marker from what the change does
- Writes a subject line, plus a body explaining *why* when the change is non-trivial
- Warns when staged changes mix unrelated work and suggests how to split them
- Gives you a ready-to-run `git commit` command

It never commits, stages, or unstages anything. You run the commit yourself.

### pr-description

Ask Claude to "write a PR description" (or run `/pr-description`, optionally with a base branch like `/pr-description develop`). The skill:

- Compares the current branch with its base (named branch, else the remote default, else `main`/`master`/`develop`)
- Reads the commits and the branch-only diff (`git diff <base>...HEAD`)
- Fills in your repo's PR template if there is one; otherwise uses a Summary / Changes / Breaking changes / Testing / Notes structure, dropping empty sections
- Matches the repo's title style (Conventional Commits if used)
- Picks up issue references from the branch name and commits, never invents them
- Only states testing that the diff shows; leaves placeholders otherwise
- Gives you a ready-to-run `gh pr create` (or `gh pr edit`) command

It never pushes, creates, or edits a pull request. You run the command yourself.

### blueprint

Ask Claude to "plan this" (or run `/blueprint`). It reads the relevant code, asks only questions the code can't answer, and writes `docs/plans/YYYY-MM-DD-<slug>.md` with goal, context, approach (and alternatives), out-of-scope, small ordered tasks (each with files, change, and a verify step), risks, open questions, and a log. It does not implement anything.

### implement

Run `/implement` (optionally with a plan path). With a plan, it picks the latest unfinished one, reconciles it with `git status`/history, then implements one task at a time: implement → verify → check the box. It stops and asks when the plan stops fitting reality, logs approved deviations in the plan, and leaves the file resumable for the next session. Without a plan, it handles small, clear tasks directly with the same step-and-verify loop, and suggests `/blueprint` first for larger work. It does not commit unless you asked; it suggests `/commit-message` at checkpoints.

### verify-done

Used before claiming anything is done, fixed, or passing. Lists the claims, finds the project's real checks (scripts, CI config, CLAUDE.md), runs them fresh after the last edit, and reports **Verified / Not verified / Failed** with the commands and results. No "should work".

### bughunt

Used for bugs, failing or flaky tests, and slowdowns. Reproduce first (ideally as a failing test), test falsifiable hypotheses one at a time, confirm the cause ("X because Y, shown by Z"), then fix at the origin and verify. After three failed fixes it stops and reassesses with you. Asks before `git bisect`.

### handle-review

Give it pasted review comments or a PR number (reads via `gh` if installed). Each point is checked against the code and classified **Agree – fix / Agree – defer / Disagree / Unclear** with evidence, shown as a table for your approval before any code changes. Then it applies agreed fixes and drafts replies for you to post. It never posts, resolves, or pushes.

### critique

Run `/critique` on a plan file, doc, or idea. One question per message, most load-bearing first, each with a recommended answer; answers the code can answer get checked instead of asked. Ends with decisions, risks, open questions, and suggested plan changes, and offers to update the plan file.

### agent-docs

For writing or fixing skills, CLAUDE.md/AGENTS.md, subagents, and system prompts. Grounds the content in your real workflow, applies a short set of writing principles, and tests the result on realistic requests. Type-specific guidance lives in `references/`.

## Git safety hook

Whenever toolkit is enabled, a `PreToolUse` hook checks every shell command Claude runs. Git commands that publish, rewrite history, or discard work make Claude Code ask you first, with the reason shown:

- `push` (any, with extra detail for force pushes and remote deletes)
- `reset --hard/--merge/--keep`, `clean` (unless `-n`), `checkout -- <paths>` / `checkout .` / `-f`, `restore` (working tree), `switch -f`
- `branch -D` / force-move, `stash drop/clear`, `rebase`, `commit --amend`
- `filter-branch`, `filter-repo`, `reflog expire/delete`, `gc --prune`, `update-ref -d`, `tag -d/-f`, `remote remove/set-url`, `worktree remove -f`
- `rm -rf .git`

Everything else passes through. It asks rather than blocks, so you stay in control. To turn it off, disable the plugin (`claude plugin disable toolkit@claude-toolkit`) or edit `plugins/toolkit/hooks/hooks.json`.

Tests:

```bash
python3 -m unittest discover tests
```

## Install

```bash
claude plugin marketplace add mizanto/claude-toolkit
claude plugin install toolkit@claude-toolkit
```

Or from a local clone:

```bash
claude plugin marketplace add ~/Documents/projects/claude-toolkit
claude plugin install toolkit@claude-toolkit
```

## Update

After pushing changes, pull them into Claude Code:

```bash
claude plugin marketplace update claude-toolkit
claude plugin update toolkit@claude-toolkit
```

Restart Claude Code to apply.

## Adding a skill

1. Create `plugins/toolkit/skills/<skill-name>/SKILL.md` (frontmatter `name` and `description`, then instructions). Put long reference material in a `references/` folder next to it.
2. Add a row to the skills table and a section under **Skills** in this README.
3. Bump `version` in `plugins/toolkit/.claude-plugin/plugin.json` (minor for a new skill, patch for fixes) — Claude Code uses it to detect updates.
4. Validate:

   ```bash
   claude plugin validate .
   ```

5. If you touched the hook, run the tests: `python3 -m unittest discover tests`.
6. Commit, push, then run the update commands above.

## License

[MIT](LICENSE)
