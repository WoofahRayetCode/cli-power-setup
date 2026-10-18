---
name: claude-adversarial-verification-gate
description: Formal adversarial self-critique, boundary-condition proofing, and confirmation-bias elimination for Claude 3.7+ Sonnet and Opus prior to declaring tasks complete.
---

# Claude Adversarial Verification Gate (`claude-adversarial-verification-gate`)

This skill brings Claude Code up to par with Gemini Argon 4's deep deliberative reasoning capacity. Before declaring any code modification, game engine port, or bug fix complete, Claude Code must pass through a strict **4-Stage Adversarial Verification Gate** to eliminate confirmation bias and prevent broken commits.

---

## 🛡️ The 4-Stage Verification Gate

### Stage 1: Invert the Fix (Devil's Advocate)
- Explicitly assume the implemented solution is defective.
- Formulate 2 plausible failure modes (e.g. edge-case null pointer dereferences, off-by-one buffer indices, 64-bit pointer truncation, unhandled file I/O exceptions).
- Check: Did the fix introduce new compiler warnings, broken imports, or regressions in existing tests?

### Stage 2: Boundary Condition Proofing
Verify safety across critical runtime boundaries:
- **Empty & Null Cases**: What happens on empty collections, missing LTX sections, null texture pointers, or disconnected D-Bus services?
- **64-Bit Memory Alignment**: On 64-bit engine ports (X-Ray/OGSR), verify that 64-bit pointers were not cast to 32-bit `long` or `int`, and struct alignments match C++ ABI standards.
- **Concurrency & Reentrancy**: Does the code introduce data races across CPU threads or GPU command queues?

### Stage 3: Live Terminal Evidence Gate
**Never declare a task complete based on theoretical assumptions.**
- Execute the actual build or test runner via Bash:
  - C++ / Engine: `cmake --build build -j$(nproc)` or `ninja`
  - Python: `pytest tests/ -v` or `python3 -m py_compile <file>`
  - Bash: `shellcheck <script>` or `bash -n <script>`
  - Assets: Parse LTX/XML syntax with validation scripts (`game-dialogue-tool`).
- Verify exit code 0 and capture the stdout proof before reporting back to the user.

### Stage 4: Output Token Economy Audit
- Verify that only surgical diffs were applied (`replace_file_content` / targeted edits).
- Verify that large templates or reports were written to disk rather than dumped into the conversation transcript.
- Conclude with the mandatory token savings line: `📉 Token Economy: ~<N> tokens saved`.
