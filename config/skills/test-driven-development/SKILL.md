---
name: test-driven-development
description: Test-Driven Development (TDD) workflow. Use when developing testable features, parsers, codecs, utilities, or bug fixes to write tests before implementation.
---

# Test-Driven Development (TDD)

Use this skill when developing algorithms, file parsers, archive packers, crypto utilities, or fixing verified bugs.

## The TDD Cycle

1. **Write the Failing Test First (Red):**
   - Define a unit test, integration test, or verification script that asserts the expected behavior.
   - Run the test and confirm that it fails for the expected reason (e.g. `AssertionError`, missing function, or incorrect return value).
   - If the test passes before writing code, the test is invalid or testing the wrong condition.

2. **Implement Minimal Code (Green):**
   - Write the simplest, cleanest code that satisfies the test.
   - Run the test suite and confirm that the test now passes.

3. **Refactor & Harden:**
   - Clean up code structure, improve variable naming, and remove redundancy while ensuring tests remain green.
   - Add boundary and edge cases (e.g. empty buffers, invalid headers, corrupted data).

## Related & Interoperating Skills
- **`task-velocity-governor`**: Enforces task completion velocity, strict timeboxing, step budgeting, anti-thrashing loops, and diminishing re...
- **`coverage-guided-mutation-testing`**: AST-based fault injection, mutant survival analysis, and automated test synthesis to self-improve test suite d...
- **`writing-plans`**: Breaks down complex engineering tasks, refactors, and mod implementations into granular, dependency-ordered, v...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
