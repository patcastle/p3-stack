### Feature

**You own the design. Plan, review, and verify.**

1. Trace the affected subsystem.
2. Use **architect** to compare code shapes when the change crosses a function boundary.
3. When the request authorizes delegation, use `delegate_task` (`mode: "async"`, a self-contained brief) using the `feature, refactoring` role from `p3-models.md`, resolved through `orchestrator_capabilities`, with a specific scope (file paths, named data shape and its organizing structure per **principle-model-the-domain**, a state machine over scattered booleans, a table/registry over branching, a typed model over repeated shape assumptions, chosen before the delegate writes logic, and success criteria). Pick each delegate's effort for the job in `target.options`, per the Subagents section. When the implementation admits multiple valid shapes (error handling, abstraction layer, test structure), delegate via the **arena** skill instead so the runners surface the alternatives and the cross-judge guards the pick. Follow the result's `next` instruction. Otherwise, implement directly. Surgical edits, re-ground against the source for upstream-derived files. Port shared-primitive improvements to all consumers and verify each. Commit liberally.
4. Verify on the matching surface. "Inconclusive" or wrong-surface is not a pass. Flag it.
5. Rebase into small, ordered commits. Stack follow-ups.
   Use the **sequence-verifiable-units** principle skill, building, verifying, and committing each small unit before the next.
6. If the design is contested, `interrogate` before shipping.
7. Run **Opening a PR** (`playbooks/opening-a-pr.md`).

**Reply:** what you built, what you chose and why, and open decisions.
