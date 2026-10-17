---
name: writing-plans
description: Breaks down complex engineering tasks, refactors, and mod implementations into granular, dependency-ordered, verifiable task lists. Use when planning multi-step work.
---

# Writing Implementation Plans

Use this skill to convert requirements and designs into structured, bite-sized tasks that can be safely executed and verified.

## Plan Structure Guidelines

Every implementation plan must follow these criteria:
1. **Granular Tasks:** Each task should ideally modify 1-3 related files or perform a discrete action that can be independently verified.
2. **Dependency Ordering:** Lay out foundational models, parsers, and utilities before the consumers or UI layers that depend on them.
3. **Explicit Verification Steps:** Every task must specify how it will be verified:
   - Automated tests (e.g. `pytest`, unit test command).
   - CLI sanity check (e.g. `python -m ...`, `zoneforge doctor`).
   - Structural or syntax check (e.g. LTX syntax, JSON validity, XML format).
4. **Rollback & Safety:**
   - Always preserve original files or reference vanilla unpacked assets.
   - Demarcate new, modified, or deleted files clearly.

## Integration with Antigravity
When creating implementation plans in Antigravity:
- Write the plan artifact to `<appDataDir>/brain/<conversation-id>/<plan_name>.md`.
- Include `request_feedback: true` and `user_facing: true` in `ArtifactMetadata`.
- Do not re-summarize the plan in chat once created; direct the user to the artifact.

## Automatic Model Escalation for Planning (Argon for Plans, Flash for Execution)
When operating on Gemini 3.8 Flash or standard tiers:
- For complex architectural plans or multi-file mod designs, the agent should automatically dispatch a **`pro` (Argon tier)** subagent via `invoke_subagent` (`Model: "pro"`, `Role: "Lead Architect Planner"`).
- The `pro` subagent leverages deep reasoning to evaluate edge cases, write the plan artifact, and return the strategy.
- The primary agent then presents the plan. Once approved by the user, the primary agent executes the tasks directly using **Flash** to conserve quota.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`executing-plans`**: Step-by-step execution of approved implementation plans. Use when executing a multi-step plan to track progres...
- **`verification-before-completion`**: Final quality gate and evidence collector. Use before claiming any task, feature, or bug fix is finished to ve...
- **`superpowers`**: Core engineering methodology and discipline engine. Use when starting non-trivial tasks to evaluate if brainst...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
