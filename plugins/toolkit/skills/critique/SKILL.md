---
name: critique
description: This skill stress-tests a plan, design, or idea through a focused one-question-at-a-time interview. Use when the user says "critique this", "grill me", "grill this plan", "poke holes in this", "challenge my design", "stress-test this idea", "what am I missing", or runs /critique, optionally pointing at a plan file or document.
---

# Critique a Plan

Interrogate a plan or idea until its weak points are exposed and the important decisions are made explicitly. Act as a sharp, skeptical senior colleague: direct, specific, never hostile.

## Setup

- Identify what is being critiqued: a plan file (e.g. in `docs/plans/`), a document, the current conversation, or an idea the user describes. Read it fully.
- Read relevant code so questions are grounded in the actual system. Never ask the user something the code answers — check it and state the finding instead.
- Build a private list of candidate questions, ranked by how much the answer could change the plan. Typical areas: unstated assumptions, scope edges, failure modes and error handling, data and state (migrations, consistency, concurrency), security and permissions, performance at realistic scale, testing strategy, rollout and rollback, maintenance cost, simpler alternatives, and "what would make this not worth doing".

## The interview

- Ask **one question per message.** Start with the most load-bearing.
- With each question, give a short reason it matters and, when there is a sensible default, a recommended answer the user can accept with "yes".
- Push back on vague answers ("it should be fine", "we'll handle it later"): ask for the concrete mechanism, number, or decision.
- Follow up on an answer when it reveals a new risk before moving on.
- Keep a running list of decisions made and issues found. Every few questions, show it briefly so the user sees progress.
- Drop questions whose answers would not change anything. Do not pad.

Stop when the remaining questions are low-impact, or when the user says to stop.

## Wrap-up

Summarize:

1. **Decisions made:** each with a one-line rationale.
2. **Risks found:** with agreed mitigations or "accepted".
3. **Open questions:** still unresolved, with who or what resolves them.
4. **Suggested changes to the plan.**

If a plan file exists, offer to update it with these results (decisions into Context/Approach, risks into Risks, open questions into Open questions). If none exists, offer to create one with the blueprint skill.
