---
name: argon-long-haul-context-compaction-gate
description: Monitors context consumption during long-running Argon YOLO porting runs, triggering atomic milestone compaction at 250k tokens to maintain sub-second latency and 95% cache discounts.
---

# Argon Long-Haul Context Compaction Gate (`argon-long-haul-context-compaction-gate`)

Gemini 4 Argon features a 1,048,576 token context window. However, during continuous multi-hour YOLO porting runs spanning 50+ tool steps, accumulating 300k–500k tokens of intermediate test runs and file reads increases generation latency and increases attention dilution over early constraints.

This skill establishes an **Atomic Milestone Compaction Gate** at **250k tokens** to keep Argon operating at peak speed and 95% prompt cache efficiency indefinitely.

---

## 1. Compaction Boundary Directives

1. **The 250,000-Token Gate:**
   - When context fuel approaches **250k tokens (~25% of window)**, schedule an atomic compaction at the next clean test pass.
   - Never trigger compaction mid-edit or while a compiler error is unresolved.
2. **Pre-Compaction Memory Serialization:**
   - Serialize verified progress into `.agents/memory/activeContext.md` formatted in high-density SentencePiece tabular notation (< 300 tokens).
   - Snapshot git working state to `.agents/checkpoints/`.
3. **Execute `/compact`:**
   - Reset working conversation memory back to baseline.
4. **Instant Resumption:**
   - Upon post-compaction resume, immediately read `.agents/memory/activeContext.md` and proceed with the next planned step without prompting the user.

---

## 2. Token & Latency Impact

| Operating State | Context Depth | Turn-by-Turn Latency | Prompt Cache Status |
| :--- | :--- | :--- | :--- |
| **Unmanaged Long-Haul Run** | 500k – 800k tokens | 8 – 15 seconds per turn | 95% discount (but high memory overhead) |
| **Managed 250k Compaction Gate** | **35k – 250k tokens** | **1 – 3 seconds per turn** | **Continuous 95% discount locked permanently** |

## Related & Interoperating Skills
- **`claude-context-rot-shield`**: Mitigates Claude context window degradation and prompt cache misses. Enforces 80k-token milestone compaction b...
- **`argon-long-context-retrieval-anchor`**: Enforces boundary-edge semantic anchoring across Gemini 4 Argon's 1M-token context window to prevent attention...
- **`argon-yolo-quota-pacing-watchdog`**: Telemetry governor that paces Gemini 4 Argon autonomous YOLO execution, preventing 5-hour quota exhaustion by ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
