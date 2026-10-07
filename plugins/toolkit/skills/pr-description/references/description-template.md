# Default PR Description Structure

Use when the repository has no PR template. Omit any section that would be empty. Small PRs may need only Summary.

```markdown
## Summary

<1–3 sentences: the problem or goal and the approach taken.>

## Changes

- <Grouped by theme, focused on behavior and decisions, not files>
- <...>

## Breaking changes

<What breaks and what users or callers must do. Omit if none.>

## Testing

- <Tests added or updated, from the diff>
- <Manual verification steps — placeholder if unknown: <!-- describe manual testing -->>

## Notes for reviewers

<Risky areas, migrations, new dependencies, config/env var changes, known follow-ups.>

Closes #<issue>
```

## Sizing guide

| Change size | Description shape |
| --- | --- |
| Trivial (typo, one-line fix, version bump) | Summary only, one or two sentences |
| Small (single concern, few files) | Summary + Changes (2–4 bullets) + Testing |
| Medium/large | All relevant sections; group Changes under bold sub-labels if there are several themes |

## Examples

### Small fix

Title: `fix(cart): prevent negative item quantities`

```markdown
## Summary

Decrementing an item at quantity 1 set it to 0 and then -1, producing negative totals at checkout. Quantity is now clamped at 1, and the remove button handles deletion.

## Testing

- Added unit tests for the quantity reducer at the lower bound
```

### Feature with breaking change

Title: `feat(api)!: paginate /users responses`

```markdown
## Summary

`/users` returned every user in one response, which timed out for organizations with more than ~20k members. This adds cursor-based pagination.

## Changes

- `/users` returns `{ items, nextCursor }` with a default page size of 100 (max 500 via `?limit=`)
- New `UserCursor` helper encodes the sort key and id
- Web client follows `nextCursor` in the members table with infinite scroll

## Breaking changes

`/users` no longer returns a bare array. API clients must read `items` and follow `nextCursor` to get all users.

## Testing

- Added integration tests for first page, middle page, last page, and invalid cursors
- <!-- describe manual testing -->

## Notes for reviewers

The new index on `(org_id, created_at, id)` is in `migrations/0042_users_cursor_idx.sql` — please check it will build online on the large orgs table.

Closes #812
```
