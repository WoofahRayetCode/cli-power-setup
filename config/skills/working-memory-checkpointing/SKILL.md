---
name: working-memory-checkpointing
description: Atomic snapshotting and 1-command rollback of in-flight git diffs, hypotheses, and active working state to safeguard complex multi-step refactors against dead-end debugging loops.
---

# Working Memory Checkpointing & Safe Speculation

When implementing speculative fixes or complex refactors across multi-turn sessions, an agent may pursue a hypothesis that proves invalid. Without checkpointing, recovering a clean workspace requires multiple rounds of manual file reverting, re-running builds, and re-grepping the repository—**burning 10,000+ tokens and causing cognitive context confusion**.

**`working-memory-checkpointing`** takes atomic, sub-second snapshots of uncommitted file diffs, active hypotheses, and test results into `.agents/checkpoints/`, enabling instantaneous 1-command rollback.

---

## ⚡ 1. Checkpoint CLI Workflow

### A. Snapshot Before Risky or Speculative Changes
Before testing an unverified hypothesis or making a major architectural edit:
```bash
python3 config/skills/working-memory-checkpointing/scripts/state_checkpoint.py save "pre-shader-refactor" -m "Attempting bindless descriptor migration"
```
* Captures uncommitted git diffs, git branch/commit SHA, and working state in `.agents/checkpoints/`.

### B. List Available Checkpoints
```bash
python3 config/skills/working-memory-checkpointing/scripts/state_checkpoint.py list
```

### C. Instant 1-Command Rollback on Failure
If the hypothesis fails or tests break catastrophically:
```bash
python3 config/skills/working-memory-checkpointing/scripts/state_checkpoint.py restore pre-shader-refactor
```
* Reverts dirty edits and cleanly re-applies the exact working tree snapshot in <100ms.

### D. Auto-Pruning Rolling Buffer
```bash
python3 config/skills/working-memory-checkpointing/scripts/state_checkpoint.py prune --keep 5
```

---

## 🛡️ Best Practices & Cognitive Guardrails

1. **Pre-Experiment Snapshot Gate:** When testing one of multiple possible fixes in `systematic-debugging`, always snapshot working state before modifying code.
2. **Zero Context Thrashing:** Never manually re-type original file contents from conversation memory after an experiment fails; restore the checkpoint cleanly.
3. **Commit Clean Checkpoints:** Once a hypothesis passes tests, delete or prune experimental checkpoints and make a clean git commit.

---

## 🔄 Interoperability & Handoffs

* **Handoff to `systematic-debugging`:** Checkpoints state between hypothesis tests.
* **Handoff to `session-episodic-memory`:** When a checkpoint succeeds, log the resolution episode into `.agents/episodes/`.
* **Handoff to `token-economy`:** Cuts recovery cost from 5+ conversational turns down to 1 command.
