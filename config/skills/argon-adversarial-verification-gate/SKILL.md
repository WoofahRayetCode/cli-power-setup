---
name: argon-adversarial-verification-gate
description: Harnesses Gemini 4 Argon's deep reasoning capacity for formal adversarial self-critique, boundary-condition proofing, and confirmation-bias elimination prior to declaring tasks complete.
---

# Argon Adversarial Verification Gate (`argon-adversarial-verification-gate`)

Large language models routinely suffer from "confirmation bias"—once an agent generates a code fix, it naturally seeks arguments confirming its own hypothesis rather than searching for flaws.

Gemini 4 Argon possesses the deepest internal reasoning and chain-of-thought capacity in the Gemini family. This skill harnesses that deep reasoning budget specifically for **pre-completion adversarial self-auditing**, rigorously challenging fixes before presenting them to the user.

---

## 1. Adversarial Audit Protocol

Before declaring any architectural refactor, low-level binary hook, or complex algorithmic task complete, execute a structured 3-part adversarial audit in internal reasoning:

```
+-------------------------------------------------------------+
|                 ADVERSARIAL SELF-CRITIQUE                   |
| 1. Boundary Condition Attack:                               |
|    - What happens on empty input, 0-length buffers, or null?|
| 2. Concurrency & Race Condition Audit:                      |
|    - Does this hold under multithreaded engine execution?   |
| 3. Memory & GC Lifetime Proof:                              |
|    - Are pointers valid across frame boundaries?            |
+-------------------------------------------------------------+
```

---

## 2. The 3 Counter-Example Rule

When validating a complex modification:
1. **Formulate 3 Hostile Edge Cases:** Explicitly hypothesize 3 specific scenarios designed to break the implementation (e.g. integer overflow, missing fallback branch, unhandled exception in Wine/Proton).
2. **Verify Immunity:** Trace execution through the proposed code against each hostile edge case.
3. **Evidence-Based Acceptance:** Only accept the solution if all 3 hostile scenarios are demonstrably handled or proven mathematically impossible under the system constraints.

---

## 3. Scope of Activation

- **Activate For:**
  - C++ 64-bit pointer/struct alignment.
  - LuaJIT GC64 memory boundary bridges.
  - Multi-threaded file I/O and game loop hooks.
  - Cryptographic and token parsing logic.
- **Bypass For:**
  - Routine typo fixes, static documentation updates, and standard git operations (to conserve reasoning quota under `argon-effort-auto-calibrator`).

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.
