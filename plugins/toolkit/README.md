# toolkit

A collection of everyday helper skills. Add new skills under `skills/<skill-name>/SKILL.md`.

## Skills

| Skill | What it does |
| --- | --- |
| `commit-message` | Drafts a [Conventional Commits](https://www.conventionalcommits.org/) message from staged git changes |
| `pr-description` | Drafts a pull request title and description from the branch's changes against its base |

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

No external services or credentials required.
