# Writing Subagents and System Prompts

A subagent starts with no conversation history. Everything it needs must be in its definition or in the task message the caller sends.

## Subagent definition (`agents/<name>.md`)

```markdown
---
name: agent-name
description: <When the main agent should delegate to this one, with concrete situations.> Examples:
  <example>user: "..." → delegate because ...</example>
tools: Read, Grep, Glob, Bash
model: inherit
---

<System prompt: role, process, output format.>
```

- **description:** decides when the main agent delegates. Name the situations and include one or two short examples.
- **tools:** grant the minimum. A reviewer or researcher usually needs only read/search tools; withholding Write/Edit makes it safe to run unattended.
- **Body:** a system prompt, written as instructions to the subagent.

## System prompt content

1. **Role and goal** in one or two sentences, including what success looks like.
2. **Inputs** it should expect from the caller and what to do when they are missing.
3. **Process:** the steps, with where to look and what to check.
4. **Boundaries:** what it must not do (edit files, run destructive commands, contact external services), and when to stop and report instead of guessing.
5. **Output format:** exact structure of the final message — the caller usually parses or relays it. Ask for findings with file:line references, confidence, and evidence; ask it to state what it did not check.

## Task messages to a subagent

When delegating, include: the goal, relevant file paths and context already known, constraints, what has been ruled out, and the expected output format. A subagent cannot see the conversation, so "fix the bug we discussed" fails.

## Pitfalls

- Vague role ("you are an expert engineer") with no process: adds nothing.
- Unbounded scope: the agent wanders. State what is in and out of scope and when to stop.
- Free-form output: hard for the caller to use. Specify the format.
- Hidden assumptions about the environment: name the tools, paths, and commands it should use.
