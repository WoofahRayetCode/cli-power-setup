---
name: subagent-code-reviewer
description: Dispatches an isolated reviewer subagent to audit code changes, mod diffs, security implications, or edge cases before committing or publishing, without polluting the primary context.
---

# Subagent Code Reviewer

Use this skill before finalizing a significant feature, refactor, mod script, or package release.

## Purpose & Architecture
Instead of having the primary agent review its own code (which carries confirmation bias and context bloat), this skill dispatches an independent reviewer subagent via Antigravity's `invoke_subagent`.

## Review Checklist

The reviewer subagent must inspect:

1. **Correctness & Edge Cases:**
   - Are nil/null checks in place?
   - Are boundary conditions handled (empty inputs, zero-length files, negative offsets)?
   - For modding: are section headers, file encodings, and game asset formats valid?

2. **Clean Diffs & Scope:**
   - Are there any accidental debugging logs, print statements, or scratch files included?
   - Did the edits modify only the intended lines without reformatting unrelated code?

3. **Performance & Memory:**
   - Are file descriptors, sockets, or subprocess handles properly closed?
   - Are loops free of repeated expensive disk I/O or redundant allocations?

## Dispatch Pattern
When invoking the reviewer:
```json
{
  "TypeName": "research",
  "Role": "Code Reviewer",
  "Prompt": "Review the recent changes in git diff --cached (or the specific modified files). Check for edge cases, null safety, resource leaks, and adherence to project conventions. Return a concise report with any issues found and a clear PASS/FAIL verdict.",
  "Model": "flash"
}
```
Using `flash` keeps the review fast, thorough, and highly quota-efficient.
