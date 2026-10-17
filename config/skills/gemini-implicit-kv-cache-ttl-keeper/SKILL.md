---
name: gemini-implicit-kv-cache-ttl-keeper
description: Prevents 150k-200k uncached input token spikes caused by Gemini implicit KV-cache TTL eviction during long playtests, C++ builds, and background tasks by enforcing pre-wait compaction gates and log-tail redirection.
---

# Gemini Implicit KV-Cache TTL Keeper (`gemini-implicit-kv-cache-ttl-keeper`)

Telemetry analysis across 10,600+ Antigravity turns reveals that `cache_read_tokens` drops to `0` (`100%` cache miss, re-billing `160,000–195,000` uncached input tokens in a single turn) whenever an agent waits **`> 110–300 seconds`** on a long background task, playtest (`autowalk.sh`), or full engine build while holding a large (`> 120k` token) context window.

---

## 1. Root Cause of Zero-Cache Wakeup Spikes

1. **Implicit Cache Slot Eviction (`TTL ≈ 3–5 min`):**
   When a command runs asynchronously or blocks for several minutes, the backend implicit KV-cache slot can expire or route the wakeup `<SYSTEM_MESSAGE>` to a cold replica.
2. **Multiplicative Penalty of Bloated Context:**
   - If active context is `35k` tokens when a cache slot expires, the cold-start penalty is only `35k` tokens.
   - If active context has bloated to `193k` tokens, a single cold-start wakeup bills **`193,686` uncached input tokens**!

---

## 2. Mandatory Cache-Preserving Execution Rules

1. **Pre-Long-Job Compaction Gate (`> 120k` Context Ceiling Before Long Tasks):**
   - Before launching any playtest, benchmark, or compilation expected to run for `> 60 seconds`, check the statusline `🧠 Ctx:` gauge.
   - If `Ctx > 120k` tokens, stage current progress to `.agents/memory/activeContext.md` and compact **before** starting the long job so the wakeup turn is lightweight.
2. **Redirect Playtest & Compiler Output to `/dev/shm` + `tail -n 25`:**
   - Never stream hundreds of lines of Wine/Proton, CMake/Ninja, or Blender stdout into the tool response.
   - Always run:
     ```bash
     ./tools/autowalk.sh > /dev/shm/autowalk.log 2>&1; tail -n 25 /dev/shm/autowalk.log
     ```
3. **Maximize Synchronous `WaitMsBeforeAsync` (`10000ms`) for Medium Tasks:**
   - For commands that finish in `2–10 seconds`, always set `WaitMsBeforeAsync: 10000` so the command completes in a single synchronous turn rather than spawning an extra async `<SYSTEM_MESSAGE>` wakeup turn (which doubles turn count and risks replica hopping).

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Stage temporary command logs to `/dev/shm` on Linux or `$env:TEMP` on Windows 10/11.

## Related & Interoperating Skills
- **`gemini-copy-then-patch-edit-governor`**: Eliminates 20k+ output token spikes via `cp` + surgical diffs.
- **`gemini-ast-symbol-window-slicer`**: Enforces strict `StartLine`/`EndLine` line slicing on `view_file`.
- **`argon-context-cache-guard`**: Anchors Gemini 4 Argon context for maximum 95% KV caching discounts.
