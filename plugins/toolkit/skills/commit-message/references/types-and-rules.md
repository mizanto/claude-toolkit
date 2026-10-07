# Conventional Commits: Types and Edge Cases

## Types

| Type       | Use for                                                                 | Version impact |
| ---------- | ----------------------------------------------------------------------- | -------------- |
| `feat`     | A new feature or user-visible capability                                | minor          |
| `fix`      | A bug fix — code did not do what it was supposed to                     | patch          |
| `docs`     | Documentation only (README, docs site, code comments, docstrings)       | none           |
| `style`    | Formatting, whitespace, semicolons — no code meaning change             | none           |
| `refactor` | Code restructuring that neither fixes a bug nor adds a feature          | none           |
| `perf`     | A change that improves performance                                      | patch          |
| `test`     | Adding or correcting tests only                                         | none           |
| `build`    | Build system or external dependencies (package.json, Dockerfile, Makefile, lockfiles) | none |
| `ci`       | CI configuration and scripts (.github/workflows, .gitlab-ci.yml, etc.)  | none           |
| `chore`    | Maintenance that fits nothing else (.gitignore, tooling config, housekeeping) | none     |
| `revert`   | Reverting a previous commit                                             | depends        |

Any type with `!` or a `BREAKING CHANGE:` footer → major.

`style` means code formatting, not CSS. A CSS change that alters how the UI looks is `feat` or `fix`.

## Edge cases

- **Feature + tests + docs together**: one `feat` commit. Tests and docs that support the main change do not change the type.
- **Bug fix that requires a refactor**: `fix`. Type follows intent, not the bulk of the diff.
- **Dependency bump**: `build(deps): bump lodash from 4.17.20 to 4.17.21`. If the bump fixes a security issue or bug users experience, `fix(deps):` is acceptable; follow repo history.
- **Dev-only dependency or tooling changes**: `build` or `chore`, matching repo history.
- **Renaming/moving files with no logic change**: `refactor`.
- **Removing dead code**: `refactor` (or `chore` if it is unused config/files).
- **Lint fixes that change code**: `style` if purely cosmetic; `refactor` if structure changes; `fix` if the lint caught a real bug.
- **Config change that changes runtime behavior**: `feat` or `fix` depending on intent, not `chore`.
- **Reverts**: `revert: <original subject>` with body `This reverts commit <sha>.`
- **Initial commit**: `chore: initial commit` or `feat: initial project setup`, matching team preference.
- **Release/version bump only**: `chore(release): 1.4.0`.

## Breaking change signals

Look for these in the diff:

- Exported function, class, method, or type removed or renamed
- Required parameter added, or parameter order/type changed
- HTTP endpoint removed, renamed, or response shape changed
- Config key, environment variable, or CLI flag removed or renamed
- Default value changed in a way that alters existing behavior
- Minimum runtime/platform/dependency version raised
- Database schema change requiring a migration users must run

Example:

```
feat(api)!: return paginated results from /users

The endpoint previously returned every user, which timed out for
large organizations.

BREAKING CHANGE: /users now returns { items, nextCursor } instead of
a bare array. Clients must read `items` and follow `nextCursor`.
```

## Subject line examples

Good:
- `fix(parser): handle empty input without throwing`
- `feat(cli): add --dry-run flag to deploy command`
- `refactor: extract retry logic into shared helper`
- `docs(readme): document required environment variables`

Bad → better:
- `fix: fixed bug` → `fix(cart): prevent negative item quantities`
- `feat: Updated UserService.ts and UserController.ts` → `feat(users): allow updating display name`
- `chore: changes` → name the actual change
- `feat(auth): Add OAuth login.` → `feat(auth): add OAuth login`
