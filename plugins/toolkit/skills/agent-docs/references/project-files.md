# Writing CLAUDE.md / AGENTS.md

These files load into every session in the project, so every line has a permanent cost. Include only what the agent needs repeatedly and cannot quickly discover itself.

## Include

- **Commands:** how to install, build, run, test (single test and full suite), lint, typecheck, format. Exact commands.
- **Project map:** a few lines on where the main parts live, only when the layout is not obvious.
- **Conventions that differ from defaults:** naming, error handling patterns, preferred libraries, things never to use and why.
- **Workflow rules:** branch naming, commit format, what requires asking first (migrations, dependency additions, public API changes).
- **Gotchas:** environment quirks, flaky tests, generated files not to edit, slow commands to avoid.
- **Pointers:** to deeper docs (`docs/architecture.md`) instead of copying their content.

## Leave out

- Generic advice the model already follows ("write clean code", "add tests").
- Information obvious from the code or `package.json`.
- Long explanations, history, and changelogs.
- Anything that will go stale quickly (current sprint, temporary state).

## Shape

- Short sections with headings; bullets over prose.
- Aim for under ~150 lines. If it grows past that, move topic detail into files the main document links to, or into skills that load on demand.
- In monorepos, put package-specific rules in that package's own CLAUDE.md / AGENTS.md; keep the root file for repo-wide rules.

## Maintaining

- When the agent repeats a mistake, add a specific rule with the reason, not a general one.
- When editing, remove rules that no longer apply; stale rules cause confident wrong behavior.
- CLAUDE.md is read by Claude Code; AGENTS.md by several other agents. If both exist, keep one as the source and have the other reference it (e.g. CLAUDE.md containing `@AGENTS.md`) rather than duplicating.
