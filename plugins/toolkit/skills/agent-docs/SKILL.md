---
name: agent-docs
description: This skill writes and improves instructions meant for AI agents — Claude Code skills (SKILL.md), CLAUDE.md / AGENTS.md project files, subagent definitions, slash commands, and system prompts. Use when the user asks to "write a skill", "create a skill", "improve this skill", "why isn't my skill triggering", "write a CLAUDE.md", "update AGENTS.md", "write a subagent", "write a prompt for an agent", or runs /agent-docs.
---

# Write Instructions for Agents

The reader is a capable model with no memory of this conversation, limited attention, and a habit of taking text literally. Write so it does the right thing on the first read.

## Step 1: Identify the document type

| Type | Purpose | Reference |
| --- | --- | --- |
| Skill (`skills/<name>/SKILL.md`) | A reusable capability loaded on demand when its description matches | `references/skills.md` |
| CLAUDE.md / AGENTS.md | Always-loaded project context and rules | `references/project-files.md` |
| Subagent (`agents/<name>.md`) or system prompt | A delegated role with its own context | `references/agents.md` |

Read the matching reference before writing. If editing an existing file, read it fully first and keep what works.

## Step 2: Gather the substance

- Get the actual workflow, rules, and gotchas from the user or the codebase — not generic best practice. Ask for real examples of inputs and desired outputs.
- Find what the model gets wrong without the document. Those failure modes are what the instructions must address.
- Check for existing docs that overlap (other skills, CLAUDE.md, README) so instructions do not conflict or duplicate.

## Step 3: Write

Principles that apply to every type:

- **Lead with what to do.** Imperative, verb-first steps ("Run the tests", "Read the config"), not "You should consider…".
- **Explain why for non-obvious rules.** A reason lets the model generalize to cases the rule did not anticipate. A bare rule gets applied rigidly or ignored.
- **Be specific.** Exact commands, file paths, names, thresholds, output formats. Replace "handle errors appropriately" with what appropriate means here.
- **Spend words where the model would go wrong.** Skip what a capable model already does well. Every line costs attention for everything else.
- **Show, briefly.** One good example beats a paragraph of description. Mark examples as illustrations so they are not copied verbatim.
- **State boundaries.** What not to do, when to stop and ask, what is out of scope — especially for destructive or outward-facing actions.
- **Avoid shouting.** Reserve emphasis (MUST, NEVER, bold) for the one or two rules that truly matter; emphasizing everything emphasizes nothing.
- **No contradictions.** Re-read the whole document for rules that conflict with each other or with other loaded docs.
- **Progressive disclosure.** Keep the main file lean; move long references, schemas, and examples into separate files and say when to read them.

## Step 4: Test it

- Walk through two or three realistic requests and check, step by step, whether the instructions lead to the right behavior. Include one request that should *not* trigger a skill.
- When practical, test with a fresh agent (a subagent with no context) given only the document and a realistic task, and compare its behavior to what was intended. Revise the parts it misread.
- For skills, check that the description alone would make the right selection among similar skills.

## Step 5: Deliver

- Write the file in the correct location for its type.
- Summarize what the document makes the agent do differently, and any assumptions to confirm.
- If the file lives in a plugin, remind the user to bump the plugin version and validate (`claude plugin validate <path>`).
