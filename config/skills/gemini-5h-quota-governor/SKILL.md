---
name: gemini-5h-quota-governor
description: Real-time telemetry governor for Gemini 3.8 Flash rolling 5-hour quota windows. Throttles tool verbosity and paces autonomous execution to guarantee uninterrupted workflow between rollover cycles.
---

# Gemini 5-Hour Quota Governor (`gemini-5h-quota-governor`)

Gemini models operate on a **continuous 5-hour rolling compute window**. As old turns pass beyond the 5-hour boundary, quota replenishes automatically. However, rapid autonomous execution can outpace replenishment, triggering throttling pauses.

This skill balances task velocity against the 5-hour rollover timer to ensure continuous, uninterrupted execution.

---

## 1. Burn Rate Velocity Monitoring

The governor inspects live telemetry via `agy-quota-statusline`:

```text
⚡ agy [Flash] | 5h: 72% (reset 18:56) | Wk: 55%
```

### Velocity Zones:

| Zone | 5-Hour Headroom | Time to Reset | Action Policy |
| :--- | :--- | :--- | :--- |
| **Green** | > 60% | Any | Standard execution; normal tool calls |
| **Yellow** | 30%–60% | > 2 hours | Engage `headless-test-condenser`; suppress verbose diffs |
| **Orange** | 15%–30% | > 1 hour | Strict micro-slice reads only; single test re-runs |
| **Red (Reserve)** | < 15% | Imminent | Safe checkpoint to `.agents/memory/activeContext.md`; wait for rollover |

---

## 2. Dynamic Tool Output Throttling

When entering the **Yellow or Orange zone**:
- **Test Runs:** Enforce quiet flags (`pytest -q`, `cargo test -q`).
- **File Edits:** Limit multi-file batch operations to 1 file per turn.
- **Diff Inspection:** Avoid printing full git diffs into chat; inspect commit stats with `git diff --stat` instead.

---

## 3. Rollover Wait-for-Refresh Discipline

If the 5-hour quota reaches **$\le$ 10%**:
1. Do not abort or fail the task.
2. Snapshot all working state to `.agents/memory/activeContext.md`.
3. Sleep cleanly until the recorded reset timestamp passes.
4. Verify quota replenishment via `agy-quota-statusline` and resume execution seamlessly.

---

## 4. Weekly 50% Safe Headroom Offloading

When the weekly quota reaches or drops to **$\le$ 50%**:
1. **Aggressive Local Offload:** Shift mechanical edits, unit test drafting, and code implementation to local models (`local-coprocessor`, `deepseek-coder-v2:16b`, `qwen2.5:72b-iq2`, `phi3.5:latest`, `deepseek-r1:1.5b`).
2. **Cloud Quota Preservation:** Clamp Cloud Gemini 3.8 Flash to lightweight, single-shot verification passes (`--effort low`).
3. **Safe Reserve Lock:** Guarantees that the remaining 50% weekly cloud compute remains available for complex end-of-week milestones until the scheduled refresh.

---

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`argon-yolo-quota-pacing-watchdog`**: Telemetry governor that paces Gemini 4 Argon autonomous YOLO execution, preventing 5-hour quota exhaustion by ...
- **`gemini-flash-cache-aligner`**: Maximizes Gemini 3.8 Flash prompt caching discounts (>90% savings) through strict prefix stabilization, 4,096-...
- **`context-pruning-watchdog`**: Live telemetry monitoring of active context consumption; automatically stages memory state into activeContext....
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
