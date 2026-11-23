### Opening a PR

Work on an isolated branch from trunk. In T3, use the existing worktree, or use `delegate_task` with `isolation: "worktree"` for a separate child checkout. Keep unrelated work out. Make small, landable commits. Use **unslop** before committing and **no-comments** before review.

Use a `type(scope): subject` title. Keep the body under 40 lines with these headings in order, dropping empty ones: **Why**, **What changed**, **Scope**, **Tradeoffs**, **Blast Radius**, **Verification**. State what the checks proved and link longer evidence.

Push and open with `pull_request_create` and `draft: false` unless the user requests a draft. It links the PR. Stack dependent changes by base branch and use `link_pull_request` for layers the thread does not yet track. If a T3 PR tool is unavailable, use the forge CLI and link the resulting PR. Opening a PR does not start a babysit.
