---
name: verification-before-completion
description: Final quality gate and evidence collector. Use before claiming any task, feature, or bug fix is finished to verify with concrete execution evidence.
---

# Verification Before Completion

Use this skill before announcing that any work is finished.

## Completion Checklist

Before declaring a task done, you must verify the following:

1. **Concrete Evidence:**
   - Did you execute the tests, build commands, or verification scripts?
   - Is there terminal output showing a successful exit code (`0`) and passing assertions?
   - Never say "This should now work" without having run the command that confirms it.

2. **No Regressions:**
   - Run the broader project test suite or sanity checks (e.g. `pytest`, `zoneforge doctor`, lints).
   - Ensure temporary debug scripts, scratch files, or unwanted changes are cleaned up or properly committed.

3. **User Documentation:**
   - For complex tasks, summarize the changes in a walkthrough artifact or concise explanation with direct clickable file links.
