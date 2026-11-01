---
name: orchestrate
description: Run a multi-day, many-PR program as a standing coordinator that decides which agent does each piece of work and checks what each produces.
---

### Orchestrate

**You run the program, never the code. Decide which agent does each piece of work, then check what each one produces.** For a standing project handed to one coordinator thread: multi-day, many stacked PRs, dozens to hundreds of delegated workers, few human turns. One task driven to a predicate is Autonomous run. One ambitious run that needs a bespoke workflow is figure-it-out. Work that one agent could finish inside the session's budget is not a program.

Run it with T3's own tools. Spawn workers with `delegate_task` or `t3_thread_launch`. Keep the program's state in one `orchestrate/<project-slug>/notes.md` in the project, and the PRs on this thread: `link_pull_request` every PR the moment it opens, and read them back with `list_thread_pull_requests`. Arm `watch_pull_request` on each PR you wait on, end the turn, and triage on wake. Arm one hourly `schedule_task` tick (`{"type":"interval","everyMs":3600000}`) as the heartbeat in case a wake never comes, and delete it with `delete_scheduled_task` at close. Call no scripts, run no polling loops, and never relay messages or status between agents.

#### Topology

- **One owner per PR.** The owner is a `t3_thread_launch` thread with its own worktree and branch (`workspaceStrategy`), the only writer of that branch, and it carries the PR from build to merge. Only the owner pushes, rebases, or retargets it. Closing or retargeting a base PR orphans every PR above it, so the owner does that only on your call. You never author or edit code. Conflicted merges, chain rebases, and fixes go to owners.
- **A fresh worker for each independent task.** A `delegate_task` in `mode: "async"`, drained with `task_status`, or with `isolation: "worktree"` when it needs its own checkout of the current commit. Its brief carries everything it needs, including each upstream report it depends on, pasted in full, because T3 child agents get only the brief and can't see their siblings. Work that needs this machine's live state, such as a `preview_*` or `device_*` runtime check, a simulator, or auth that exists only here, runs in a `t3_thread_launch` thread. Resolve each worker's role from `p3-models.md` through `orchestrator_capabilities`, and pick its effort in `target.options` for the job, per p3-mode's Subagents section.
- **A sub-coordinator only when one area has many parallel workers.** A `t3_thread_launch` thread that owns that area's workers and briefs and sends you one rollup, never raw worker reports. Stop at three levels: you, sub-coordinators, and workers. Keep about ten workers in flight per coordinator, and start the next one as each finishes instead of waiting on a whole batch.
- **Fork when new work needs a worker's built state,** such as its checkout, uncommitted changes, or a running process (`t3_thread_fork`). Message a worker (`t3_thread_send`) only for a follow-up on the same work. Never message one to check on it, because a message restarts an idle agent.
- **Each PR gets a verifier that isn't its author,** on a different provider. The owner merges only on that verifier's pass at the current head.
- **Start with one unit.** Take it through brief, owner, verifier, and merge before you fan out, so a flaw in the brief costs one agent instead of fifty. On near-identical cheap units, the first unit is that test.

#### Supervision

- **Each brief names the evidence that proves the work is done,** such as a command and its expected output, a `preview_*` or `device_*` check, or an artifact. It also names the goal, the paths the worker may and may not write, and the actions it must not take. If you can't name the evidence, the unit isn't scoped yet.
- **Read the diff or the artifact, not only the worker's summary.** Green CI is an input to a verdict, not a verdict. Behavioral work needs more than a type check. A verdict covers one head SHA, so a new push needs a new verdict. Read a sample of each sub-coordinator's briefs while its workers run, and fix its instructions when one fails.
- **Send back work that drifts from scope or grows past what was asked.** Keep only the fixes that block the program, and park the rest as follow-ups.
- **Check a PR's live state before you report on it,** with `gh pr view` and `gh pr checks`, not the worker's last report. Account for every worker you spawned as done, replaced, or absorbed into another worker's scope.
- **Stop or replace a worker that stalls or loops.** Judge it by its pushes and PR activity, not its status text (`task_status`, `t3_thread_read`). Stop it with `task_cancel` or `t3_thread_interrupt`. Retry by cause: a smaller scope after a context or memory limit, the same brief after a dropped connection, and a different model after a tool error. After two retries, drop the unit and replan around it. When a stopped worker returns late, check its result against the PR's current state, and hand any unique findings to a fresh worker.
- **Ask the user only for a real decision or a blocker,** such as an irreversible action, a product or preference call that no experiment settles, or a dead end that survived a replan. Rebase mechanics, retries, CI flakes, review triage, and "should I keep going" never reach the user.

**Reply:** what landed against the goal, each PR's live state and verdict with its link, what was dropped and why, and the decisions waiting on the user.
