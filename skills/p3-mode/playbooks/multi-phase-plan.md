### Multi-phase or multi-PR plan

Write a plan an owner can execute and an operator can verify. Hand back the plan before implementation.

1. For one or two files with an obvious approach, skip the plan.
2. Settle open questions with [Prototype](prototype.md). Ask the operator about choices that an experiment cannot settle.
3. Write the plan under the project's `docs/` unless the user names another location. Give the outcome, landing order, and dependency graph. For each PR, list its files, dependencies, one change, observable result, and verification in checkboxes. Select [Autopilot-full](autopilot-full.md) when the run may merge or [Autopilot-stack](autopilot-stack.md) when the operator lands it.
4. Give every PR unit, live, and performance checks. Each live check names a scenario on the real surface and a pass condition. Use `preview_*` for browser work and `device_*` for simulators. Give performance checks the metric, probe, trunk baseline, and failure threshold. Interaction changes wait for the operator's review before merge.
5. Report the plan path, PR dependencies, review gates, and what remains unproven. Start execution on the operator's go.
