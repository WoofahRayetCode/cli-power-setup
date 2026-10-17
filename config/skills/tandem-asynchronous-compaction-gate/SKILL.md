---
name: tandem-asynchronous-compaction-gate
description: Synchronizes compaction boundaries between Argon and Fable, staging active peer state to .agents/handoff.json before /compact to lock 90-95% cache discounts without amnesia.
---

# Tandem Asynchronous Compaction Gate (`tandem-asynchronous-compaction-gate`)

In long-running sessions, context eventually reaches milestone compaction limits (~80k tokens on Claude Fable to maintain 90% prompt cache pricing, and ~200k tokens on Argon).

If an agent compacts its memory while a cross-agent task is in-flight, it can suffer from "conversational amnesia", forgetting what its counterpart is working on or re-running previously solved tasks.

This skill coordinates compaction boundaries so both agents preserve active peer context across compaction cycles.

---

## 1. Pre-Compaction State Staging

Before triggering `/compact` in either agent:

```
[ Active Agent (Approaching Compaction Threshold) ]
                     |
                     v
 1. Snapshot in-flight git diff to .agents/checkpoints/
 2. Write active peer vector & next immediate step to .agents/handoff.json
 3. Execute /compact (Reset context fuel to baseline)
                     |
                     v
 4. Re-read .agents/handoff.json (<300 tokens)
 5. Seamlessly resume task execution with 100% state continuity
```

---

## 2. Invariant Continuity Tag

The pre-compact state is serialized using model-optimal token syntax:

```json
{
  "compaction_event": {
    "timestamp": "2026-10-16T18:30:00Z",
    "agent": "fable",
    "pre_compact_tokens": 82400,
    "active_vector": "xrGame/weapon_ak74.cpp: pointer truncation fix verified",
    "sibling_dependency": "Waiting for Argon pakchunk16 audio transcode",
    "next_step": "Run ctest -R WeaponSanityTest"
  }
}
```

---

## 3. Cache Discount Protection

1. **Claude Fable (80k Boundary):** Compacting before 100k resets working context down to ~2,000 tokens, maintaining the **90% prompt cache discount** indefinitely.
2. **Gemini 4 Argon (32k+ Floor):** Ensure Argon's post-compact context remains above the **32,768-token cache threshold** by retaining static rules and tool schemas, preserving the **95% prompt cache discount**.
