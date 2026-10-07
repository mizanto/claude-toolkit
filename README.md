# claude-toolkit

Claude Code plugin marketplace with everyday helper skills. It contains the **toolkit** plugin:

| Skill | What it does |
| --- | --- |
| `/commit-message` | Drafts a Conventional Commits message from staged git changes |
| `/pr-description` | Drafts a pull request title and description from the branch's changes against its base |

No external services or credentials required.

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

5. Commit, push, then run the update commands above.

## License

[MIT](LICENSE)
