---
name: interrogate
description: "Use for \"interrogate\", \"adversarial review\", \"multi-model review\", \"challenge this\", \"stress test this code\", \"find blind spots\", or \"tear this apart\". Adversaries try to break a change or design, and only findings proven by a run survive."
disable-model-invocation: true
---

# Interrogate

Adversaries try to break a change or a design. A finding survives only when a run proves it. Report the findings. Do not apply fixes.

## Frame

The scope is what the user names. Otherwise it is the branch diff from its merge base with the base branch, through the working tree. State the intent with the **in-your-own-words** skill, from the user's message, the commits, and the PR description. Ask the user when the intent is unclear.

## Fan out

Run Phase A steps 3 and 4 and Phase B of the **arena** skill, with these changes.

- Read the `interrogate reviewers` line in `p3-models.md` in place of `arena runners`, one adversary per entry. If that line is missing, use arena's fallback for a missing runners line. No other line is needed.
- Spawn each adversary with `delegate_task`, `mode: "async"`, `role: "test"`, and `isolation: "worktree"`. Adversaries write and run repros, so they are not read-only. The worktree is a fresh checkout of your current commit. If the scope is a ref you have not checked out, name its commit in the brief and have the adversary run `git checkout --detach <commit>` first.
- The worktree leaves out uncommitted edits. When the scope has any, write them once to a `mktemp -d` folder outside the repo: `git diff --binary HEAD` as a patch, plus a copy of each untracked file from `git ls-files -o --exclude-standard`. Have each adversary `git apply` the patch and copy the files in before it starts.
- If `delegate_task` refuses `isolation: "worktree"`, have each adversary make its own checkout with `git worktree add --detach <path outside the repo> <commit>` and remove it when done. Never let an adversary write in your checkout.
- In place of the arena task and rationale, give each adversary the scope, the intent, the commit and patch path, and this brief. The brief is self-contained. A delegated adversary gets only the brief, never your context.

> Break this change. Prove each finding with a run against the real code, such as a failing test, a repro script, or command output that shows the wrong behavior. For a design or plan, run a prototype or probe the current tree. Keep repros in your own worktree. Report each finding with a title, the exact command, the output it printed, and the output the intent requires. Leave out anything you did not run. That covers style, naming, structure, and risks that need a future change to matter. No findings is a valid result. Do not commit, push, or post anything. Report the absolute path of your worktree.

Drain the adversaries with `task_status`. Wait for every one.

## Verify

Verify each finding per arena Phase F by rerunning its command in that adversary's worktree, or in a fresh worktree with its repro copied in. Never leave repro files in the scope's checkout. Keep a finding when the output shows the failure and the failure breaks the intent. Drop the rest. Merge findings that share a root cause.

Skip arena Phases C, D, and E. Adversaries find different failures, so the verdict keeps every verified finding, not one adversary's list.

## Output

- **Intent**: the restatement.
- **Adversaries**: each one's provider and model, and its count of reported and verified findings.
- **Act on**: each verified finding that breaks the intended case, with the command, its output, how it breaks the intent, and the adversaries that found it.
- **Consider**: each verified finding that fails only outside the intended case, such as another path or a rare input, in the same form.
- **Dismissed**: for each adversary, the count of dropped findings and why.

Say "no verified findings" when none survive.
