---
name: chatgpt-o1-hypothesis-tree
description: Emulates ChatGPT o1/o3-mini Tree-of-Thought deliberation on Gemini 4 Argon. Branches into 3 competing hypotheses, explores execution paths, and backtracks upon contradiction.
---

# ChatGPT o1 Hypothesis Tree (`chatgpt-o1-hypothesis-tree`)

ChatGPT o1 and o3-mini excel at hard architectural and debugging problems by utilizing **Tree-of-Thought (ToT) reasoning**: exploring multiple parallel solution paths, rigorously probing boundary conditions, and formally backtracking when a hypothesis leads to a contradiction.

This skill equips Gemini 4 Argon with o1-style branching deliberation when tackling complex engine segfaults, race conditions, and architectural designs.

---

## 1. The 3-Branch Deliberation Protocol

When confronted with an elusive runtime crash or complex refactor, structure internal reasoning into 3 competing branches before making edits:

```
                      Problem Statement
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
       [Branch A]       [Branch B]       [Branch C]
     Pointer Cast      Struct Padding   LuaJIT GC64
       Overflow          Mismatch        Boundary
            │                │                │
     Trace Execution  Trace Execution  Trace Execution
            │                │                │
      (Contradicts     (Supported by    (Unrelated to
       Callstack)       Dump Offsets)     Callstack)
            ▼                ▼                ▼
       [Backtrack]      ★ SELECTED ★     [Backtrack]
```

---

## 2. Invariant Reasoning Tags

Structure deep reasoning around explicit exploration markers:

1. `[HYPOTHESIS_A]`: Explore first candidate root cause. Trace callstack symbols against code coordinates.
2. `[BACKTRACK_CHECK]`: Test against known constraints. If contradictory: *"Contradiction detected: vertex ID is 16-bit, so overflow is impossible here. Backtracking."*
3. `[HYPOTHESIS_B]`: Explore second alternative.
4. `[SYNTHESIS_PROOF]`: Formulate the surviving hypothesis with mathematical/logical evidence before applying code diffs.

---

## 3. Quota Impact

By eliminating trial-and-error edits and blind code modifications:
- Solves complex bugs on **Turn 1** rather than Turn 5.
- Saves up to **80% of round-trip tokens** on difficult debugging sessions.
