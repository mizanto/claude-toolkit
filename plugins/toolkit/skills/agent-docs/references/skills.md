# Writing Skills (SKILL.md)

## Structure

```
skills/<skill-name>/
├── SKILL.md            # required: frontmatter + instructions
├── references/         # optional: detail loaded only when needed
└── scripts/            # optional: deterministic helpers the skill runs
```

- Directory and `name` in kebab-case; they should match.
- In a plugin, the skill is invoked as `/<plugin>:<skill-name>` (or `/<skill-name>` when unambiguous).

## Frontmatter

```yaml
---
name: skill-name
description: <what it does, in third person>. Use when <situations and literal phrases users say>, or runs /skill-name. <Key boundary, e.g. "It proposes text only and never commits.">
---
```

The description is the only part the model sees when deciding whether to load the skill. Treat it as the trigger:

- Say what the skill does and when to use it, in third person.
- Include the literal phrases users type ("write a commit message", "debug this") and the situations that should trigger it even without those phrases ("after a first fix attempt did not work").
- Distinguish it from neighboring skills. If two skills could match the same request, the descriptions must make the difference clear.
- Keep it to a few sentences. Long descriptions dilute matching and cost context in every session.

Optional fields used in Claude Code skills include `allowed-tools` (restrict tools), `argument-hint`, `model`, and `disable-model-invocation: true` (only runs when the user invokes it explicitly — use for skills with side effects the user should trigger deliberately).

## Body

- Target under ~500 lines; move anything longer into `references/` and point to it at the step where it is needed ("See `references/x.md` for the type table").
- Organize as numbered steps when the skill is a workflow; as sections when it is knowledge.
- Start with one or two sentences on the goal and the most important constraint.
- End with the output format: what the final reply contains.
- Prefer a script in `scripts/` for anything that must be exact and repeatable (parsing, validation, file generation); instruct the model to run it rather than reimplement it.
- Refer to other skills by name when chaining ("follow the verify-done skill"), rather than duplicating their content.

## Common failures

| Symptom | Likely cause | Fix |
| --- | --- | --- |
| Skill never triggers | Description too abstract or missing user phrasing | Add literal trigger phrases and situations |
| Triggers on unrelated requests | Description too broad | Add what it is *not* for; narrow the situations |
| Steps skipped | Too long, or key step buried mid-paragraph | Number the steps; move detail to references |
| Rigid, odd behavior | Rules without reasons | Add the why so the model can generalize |
| Example copied verbatim | Example presented as the template | Label it as an illustration; vary examples |
