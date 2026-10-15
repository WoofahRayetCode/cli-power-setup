---
name: executing-plans
description: Step-by-step execution of approved implementation plans. Use when executing a multi-step plan to track progress, verify checkpoints, and ensure safe rollbacks.
---

# Executing Plans

Use this skill when implementing an approved plan.

## Execution Rules

1. **Step-by-Step Discipline:**
   - Execute one task at a time.
   - Do not jump ahead or batch unrelated changes.

2. **Verify at Every Checkpoint:**
   - After applying changes for a task, run its declared verification step immediately (test command, syntax check, or tool run).
   - If a test or check fails:
     - Stop immediately.
     - Switch to `systematic-debugging` to diagnose and fix the failure before moving to the next task.
     - Never ignore a failing test to continue with subsequent tasks.

3. **Targeted Edits:**
   - Use pinpoint edits (`replace_file_content`) rather than rewriting entire files.
   - Preserve existing unrelated code, comments, and structure.

4. **Progress Visibility:**
   - Briefly communicate progress as tasks are completed and verified.
