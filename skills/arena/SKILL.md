---
name: arena
description: "Spawn N parallel candidates at the same task, pick a base, graft the strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in the arena', or when one attempt at a non-trivial artifact would lock in the wrong shape."
disable-model-invocation: true
---

# Arena

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick runners from `arena runners` in `p3-models.md`. Resolve them with `orchestrator_capabilities`. A missing role can use one model per available provider. For `auto` or `inherit-parent`, omit the model override. If an entry is rejected, try the nearest available model from the same provider or drop the seat and say so. Keep at least two runners unless the role lists only one. Adjust effort per **p3-mode**.
4. Give each candidate its own output location (a git worktree where possible, otherwise `/tmp/arena-<slug>/candidate-<n>/`), per the **separate-before-serializing-shared-state** principle skill. A candidate that needs its own checkout gets `delegate_task` with `isolation: "worktree"`, which checks out the parent commit without uncommitted edits. Use `t3_thread_launch` with a `workspaceStrategy` only when it needs its own thread or branch. One writer per worktree.

## Phase B: Fan out

Spawn all N candidates in one turn with `delegate_task`, one per runner entry, each with `mode: "async"`. T3 child agents get only the brief, never the parent's context, so every brief stands alone: the task, the path to the shared grounding, its own output path, and instructions to produce the artifact and a short rationale naming the alternatives it considered and what it rejected.

Follow each delegate result's `next` instruction. If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After candidates finish writing, spawn one read-only judge with `delegate_task`. Use the first valid `arena cross-judge pool` entry from another model vendor. Different instances or families from the same vendor do not count as cross-vendor. Resolve availability with `orchestrator_capabilities`. Skip parent-model entries. If a configured entry fails, try the nearest available model from that vendor, then the next eligible entry. If none can run, say so and pick the base yourself. If you cannot identify the parent's vendor, use the first valid configured entry and disclose that gap. Give the judge the rubric and the candidates' paths. While you review them, the judge scores each criterion and recommends a base.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API, per the Laziness Protocol.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the **redesign-from-first-principles** principle skill, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the **prove-it-works** principle skill. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
