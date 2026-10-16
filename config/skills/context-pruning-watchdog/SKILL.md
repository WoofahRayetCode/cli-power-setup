---
name: context-pruning-watchdog
description: Live telemetry monitoring of active context consumption; automatically stages memory state into activeContext.md and prompts for lossless compaction before hitting quota thresholds.
---

# Context Pruning Watchdog & Compaction Safeguard

This skill monitors conversation growth and actively prevents sessions from crossing expensive context thresholds (where rolling 5-hour quotas burn rapidly and model responses slow down).

---

## 🚨 Trigger Thresholds

* **Healthy Tier (0–40% Context, <80k tokens):** Full speed, maximum prompt caching discount, rapid streaming.
* **Warning Tier (40–60% Context, 80k–120k tokens):** Advise staging task state into memory bank; avoid large multi-file `view_file` calls.
* **Compaction Gate (>60% Context, >120k tokens):** Mandatory execution of the **Lossless Compaction Protocol**.

---

## 🔄 The Lossless Compaction Protocol

Before the context window degrades or triggers rolling quota penalties:

1. **Stage Current State:**
   Write current status, completed checklist items, and immediate next steps directly into:
   ```text
   .agents/memory/activeContext.md
   ```
2. **Preserve Open In-Flight Drafts & Interactive Widgets:**
   Ensure any uncommitted edits in `.canvas/` or newly generated widgets in `templates/` are noted in `activeContext.md`.
3. **Vision Token Preservation:**
   When multimodal images from `screen-vision-inspector` enter context, verify downscaling to 1280px max dimension and remove temporary captures from `/tmp/` before session compaction to prevent image token compounding.
4. **Prompt User for `/compact`:**
   Output a single high-density prompt:
   ```text
   [!] Context Watchdog: Session context has reached ~120k tokens (60%).
   [✓] State saved to .agents/memory/activeContext.md.
   👉 Run /compact now to reset the context window to <2,000 tokens with zero loss of progress.
   ```
5. **Hydrate on Resumption:**
   Upon restarting or post-compaction, read `activeContext.md` first (<300 tokens) and resume execution immediately.

---

## 🔄 Interoperability & Handoffs

* **Handoff to `project-memory-bank`:** Owns the persistent `.agents/memory/` directory structure.
* **Handoff to `prompt-cache-context-optimizer`:** Ensures the compacted resume prompt hits the 90% prompt cache tier.
* **Handoff to `screen-vision-inspector`:** Enforces local bounding box crops and downsizes to protect the context fuel gauge.
