---
name: first-principles-reasoning
description: First-principles decomposition, Chain-of-Verification (CoVe), adversarial red-teaming, and Ockham's Razor hypothesis ranking. Eliminates logical fallacies, confirmation bias, and cognitive overburn in complex engineering tasks.
---

# First-Principles & Chain-of-Verification Reasoning

This skill provides advanced cognitive models to elevate analytical thinking, eliminate confirmation bias, and accelerate problem-solving through **First-Principles Thinking**, **Chain-of-Verification (CoVe)**, and **Ockham's Razor Pruning**.

---

## 🧠 1. Cognitive Architecture & Mental Models

### 1. First-Principles Decomposition
* **Definition:** Break a problem down into its most fundamental, indisputable physical or code truths (e.g. CPU cache lines, byte endianness, OS system calls), rather than reasoning by analogy ("we do it this way because other projects do").
* **Rule:** When an implementation feels unnecessarily convoluted or fragile, discard intermediate abstractions and rebuild from the baseline invariants.

### 2. Chain-of-Verification (CoVe)
Mitigate AI overconfidence and hallucinations through a 4-stage verification cycle:
1. **Baseline Proposal:** Draft initial architecture or bug hypothesis.
2. **Generate Invariant Queries:** Automatically generate 3–5 skeptical questions targeting potential flaws (race conditions, memory leaks, invalid assumptions).
3. **Unbiased Execution:** Answer each question independently against actual logs, compiler outputs, or benchmarks.
4. **Synthesis:** Produce the final verified, hardened code.

### 3. Adversarial Red-Teaming (The Inversion Principle)
* *Carl Jacobi: "Invert, always invert."*
* Instead of asking *"How do I make this feature work?"*, ask:
  * *"What is the fastest way this implementation will corrupt state or cause a game crash?"*
  * *"If this test fails in production, what was the most probable overlooked assumption?"*

### 4. Ockham's Razor Debugging
* When multiple hypotheses explain a bug, rank them by `Likelihood / (Effort × Complexity)`.
* **Action:** Test the cheapest, most probable falsification first. Eliminates 80% of debugging dead-ends in minutes.

---

## 🛠️ 2. Verification Reasoner CLI

Use `verification_reasoner.py` to cross-examine complex technical proposals:

```bash
# 1. Generate Chain-of-Verification queries for an architectural claim
python3 config/skills/first-principles-reasoning/scripts/verification_reasoner.py \
  cove "Migrating from DX9 to DX11 will fix all stuttering in OGSR"

# 2. Rank debugging hypotheses by Ockham's Razor score
python3 config/skills/first-principles-reasoning/scripts/verification_reasoner.py \
  rank hypotheses.json

# 3. Offload Deep Chain-of-Verification Reasoning to Local Titan Reasoner (DeepSeek-R1 70B)
local-coprocessor generate --task reason \
  --prompt "Perform adversarial red-team analysis on this proposal: Migrating legacy X-Ray memory allocator to C++20 PMR. What are the 3 fastest ways this could cause undefined behavior?"
```

---

## ⚡ 3. Integration with Task Velocity & Execution

* **Pairing:** Combine `first-principles-reasoning` with `task-velocity-governor`.
* **Discipline:** High-depth reasoning happens *before* modifying code; execution remains surgical, timeboxed, and verified by tests.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

## Related & Interoperating Skills
- **`argon-adversarial-verification-gate`**: Harnesses Gemini 4 Argon's deep reasoning capacity for formal adversarial self-critique, boundary-condition pr...
- **`deliberative-reasoning-tree`**: DeepSeek R1 and OpenAI o1-style Tree-of-Thought reasoning, exploring 3 branching hypothesis paths, adversarial...
- **`dynamic-model-downshifter`**: Autonomous multi-tier model downshifting for CLI sessions. Enforces the 'Frontier Brain, Fast Hands' pattern b...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
