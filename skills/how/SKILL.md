---
name: how
description: "Use for \"how does X work\", code walkthroughs before changing something, and placement / ownership / layering questions (\"where should this live\", \"which package owns this\", \"is this the right layer\"). Explains subsystem architecture, runtime flow, onboarding mental models. Use why for motivation."
disable-model-invocation: true
---

# How

Explore the codebase to answer "how does X work?" questions.

If the scope is ambiguous, state your interpretation and explore. The user can redirect.

## 1. Explain

Spawn one `delegate_task` that explores and explains in one pass, on the parent thread's provider and model. Set its effort in `target.options` for the job, per the Subagents section of the **p3-mode** skill. The child gets only the brief, never this conversation, so give it the user's question and this brief, and say it is read-only: inspect only, no writes, no git commands.

> You are writing an architectural explanation for a senior engineer. Explore the codebase and write an explanation that a senior engineer unfamiliar with this area could read and walk away with a solid mental model. They should understand the architecture well enough to start working in it confidently. You have read-only access to the codebase.

Drain with `task_status`.

## 2. Present

Present the child's output. Light edits for clarity or context from the conversation are fine. Do not substantially rewrite it.
