# claude-toolkit

Claude Code plugin marketplace with everyday helper skills. It contains the **toolkit** plugin:

| Skill | What it does |
| --- | --- |
| `/commit-message` | Drafts a Conventional Commits message from staged git changes |
| `/pr-description` | Drafts a pull request title and description from the branch's changes against its base |

See [plugins/toolkit/README.md](plugins/toolkit/README.md) for details.

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
2. Add a row to the skills table in `plugins/toolkit/README.md` and this README.
3. Bump `version` in `plugins/toolkit/.claude-plugin/plugin.json` (minor for a new skill, patch for fixes) — Claude Code uses it to detect updates.
4. Validate:

   ```bash
   claude plugin validate .
   ```

5. Commit, push, then run the update commands above.

## License

[MIT](LICENSE)
