---
name: autogen-adversarial-redteam-critic
description: Emulates Microsoft AutoGen multi-persona red-teaming. Executes an internal Devil's Advocate audit to aggressively attack candidate fixes before committing code.
---

# AutoGen Adversarial Red-Team Critic (`autogen-adversarial-redteam-critic`)

Microsoft AutoGen demonstrated that single-agent generation frequently misses obvious edge cases due to positive reinforcement bias. In AutoGen, an internal **"Critic / Red-Team Persona"** actively tries to break the Implementer's proposed solution before execution.

This skill equips Gemini 4 Argon with an automated internal Red-Team pass during C++ engine modifications and Linux game modding.

---

## 1. Dual-Persona Reasoning Protocol

Before applying any code changes via `replace_file_content`:

```
+-------------------------------------------------------------+
| Step 1: IMPLEMENTER PROPOSAL                                |
| - Candidate C++ fix: Replace u32 cast with uintptr_t        |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
| Step 2: RED-TEAM CRITIC ATTACK                              |
| "How does this code crash in the live game?"                |
| - Attack A: What if H_Parent() returns NULL? (Null ptr deref)|
| - Attack B: Does uintptr_t serialize correctly to save file? |
| - Attack C: What happens on multi-threaded ALife tick?      |
+-------------------------------------------------------------+
                              │
                              ▼
+-------------------------------------------------------------+
| Step 3: HARDENED SYNTHESIS                                  |
| - Add explicit nullptr guard: if (!pOwner) return;          |
| - Verify serialization struct is unaltered                  |
| - Emit code diff ONLY after surviving all 3 attacks         |
+-------------------------------------------------------------+
```

---

## 2. Invariant Gate

- **The Rule:** If the Red-Team Critic discovers any plausible crash condition, the code is rejected in internal reasoning before a single file edit or compiler command is executed.
- **Quota Savings:** Eliminates runtime game crashes, saving 3–5 expensive test-run turns per defect.

## Related & Interoperating Skills
- **`argon-adversarial-verification-gate`**: Harnesses Gemini 4 Argon's deep reasoning capacity for formal adversarial self-critique, boundary-condition pr...
- **`chatgpt-o1-hypothesis-tree`**: Emulates ChatGPT o1/o3-mini Tree-of-Thought deliberation on Gemini 4 Argon. Branches into 3 competing hypothes...
- **`deliberative-reasoning-tree`**: DeepSeek R1 and OpenAI o1-style Tree-of-Thought reasoning, exploring 3 branching hypothesis paths, adversarial...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
