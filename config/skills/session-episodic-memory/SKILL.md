---
name: session-episodic-memory
description: Multi-session milestone checkpointing, chronological episode logging (.agents/episodes/), decision rationales, and seamless restoration across /compact events. Use during long-running tasks to prevent conversational amnesia and maintain an audit trail of engineering decisions.
---

# Session Episodic Memory & Milestone Checkpointing

While `project-memory-bank` preserves static project briefs and architecture patterns, **Session Episodic Memory** captures the *chronological narrative* of what happened, why decisions were made, which hypotheses failed, and the exact state before `/compact` events.

---

## 1. Episodic Storage Structure

Episodic logs live in `.agents/episodes/` inside the project root:
```text
.agents/episodes/
├── 2026-10-15_1830_video_pipeline.md      # Episode record: AV1 NVENC pipeline setup
├── 2026-10-15_1900_android_ndk.md         # Episode record: JNI bridge & tombstone symbols
└── current_milestone.json                 # Fast atomic state checkpoint
```

Each episode file is a compact, high-density record (<40 lines) structured as:
```markdown
# Episode: [YYYY-MM-DD HH:MM] - [Task Title]

### 1. Objective & Hypothesis
* Target: Implement JNI zero-copy ByteBuffer bridge.
* Hypothesis: Pass direct memory pointer to avoid JVM GC pinning.

### 2. Key Decisions & Rationale (ADR)
* Decision: Use `GetDirectBufferAddress` over `GetByteArrayElements`.
* Why: Eliminates 12MB/sec memory copy on 60 FPS camera frame feed.

### 3. Dead Ends & Discarded Alternatives
* Rejected: `PushLocalFrame(16)` was insufficient for inner loop; raised to 64.

### 4. Immediate Checkpoint State
* Verified: C++ compilation clean, tests pass.
* Next Task: Connect Oboe audio callback in Android ViewModel.
```

---

## 2. Pre-Compaction Checkpointing Protocol

When context consumption crosses **50%–60%** and `context-pruning-watchdog` prompts for `/compact`:

1. **Write Episode Snapshot:** Create `.agents/episodes/<timestamp>_<task>.md` summarizing the recent turns.
2. **Update `activeContext.md`:** Reference the latest episode file link.
3. **Execute `/compact`:** The chat transcript is cleared.
4. **Instant Hydration:** Upon resumption, the agent reads the last episode file in <200 tokens and continues with **zero loss of mental state or reasoning history**.

---

## 3. Benefits & Quota Impact

* **Eliminates Conversational Amnesia:** You can pause a project for two weeks, return, and the agent knows exactly where it left off and why it chose a specific implementation path.
* **Prevents Circular Debugging:** Discarded alternatives are logged, stopping the agent from trying a known broken solution 5 turns later.
* **Saves 80% of Re-Explanation Tokens:** No need to re-prompt the agent with "remember what we were doing earlier?".
