# Global Antigravity (agy) Engineering Rules

## 1. Output Token Economy & Communication
- **Zero Fluff:** Omit opening pleasantries, prompt restatements, and closing filler. Lead directly with technical results or actions.
- **Silent Tool Execution:** Do not narrate routine tool calls or dump raw command output. Report only outcomes, pass/fail tallies, and actionable errors.
- **Bounded Reads & Scans:** Use `find -maxdepth 2` and pipe verbose logs through `tail -n 25` or `grep`. For files >300 lines, locate symbols with `grep -n` first and read targeted line ranges (`StartLine`/`EndLine`).
- **Surgical Edits:** Use `edit_file` for targeted replacements; never rewrite whole files unless replacing the majority of content. Do not re-read a file solely to confirm an edit succeeded.
- **Artifact Offloading:** Write extensive plans, reports, or templates to artifacts/files and link them cleanly using `[basename](file:///abs/path#L1-L10)` syntax.

## 2. Subagents, Multi-Model Routing & Local Fleet Offload
- **Main Thread Protection:** Keep the main thread focused on architectural decisions and edits. Delegate broad multi-file searches or codebase reconnaissance to the `research` subagent (`Model: "flash"` or `"flash_lite"`), requesting synthesis in <=15 lines.
- **Zero-Quota Local Ollama Fleet:** Offload mechanical drafting, boilerplate, regex, math proofs, and bulk code analysis to the local RTX 5060 + 32-thread Ollama fleet via `local-coprocessor` or `local-worker` (`qwen3-coder:30b`, `gpt-oss:20b`, `deepseek-coder-v2:16b`, `OpenReasoning-Nemotron:7b`, `nemotron-3-nano:4b`).
- **Anti-Looping & Checkpointing:** Stop and report after 3 failed attempts at the same bug. On multi-milestone tasks, record state in `.agents/memory/activeContext.md` (`<300` tokens) to survive `/compact` seamlessly.

## 3. Workspace Confinement, Environment & Verification
- **Strict Directory Confinement:** Keep all file edits and build outputs strictly inside the active target repository. Never write project files or scratch outputs to `~`, `~/.gemini/`, or `Desktop` unless explicitly asked.
- **Hermetic Environment & Safety:** In Python projects, always use `.venv/bin/python` / `.venv/bin/pytest`. Never run `pip install` globally or invoke `sudo` without explicit user approval. Never echo or commit secrets/API keys.
- **Evidence-Based Completion:** Trace bugs to root causes via logs/stack traces before editing. Before claiming done, run the real build/test (`pytest`, `cargo check`, `luajit -b`, `cmake --build`), confirm it passed, and preserve all unrelated comments/docstrings.
- **Voice Input Normalization:** Strip conversational filler from dictated prompts and normalize phonetic code terms (*"oh gee ess are"* -> `OGSR`, *"ell tee ex"* -> `LTX`, *"see plus plus"* -> `C++`, *"you input"* -> `/dev/uinput`).

## 4. Gemini 4 Argon Reasoning & Token Clamping
- **Effort Clamping by Default:** Run Argon on `medium` effort for standard architecture and debugging. Escalate to `high` or `max` only for formal mathematical proofs, complex multi-threading race conditions, or binary decompiler algorithm reconstruction.
- **Upstream Subagent File Slicing:** Never let Argon read raw logs or files >200 lines directly. Delegate file reading and symbol search to a Flash subagent (`invoke_subagent` with `Model: "flash"` or `"flash_lite"`), returning a <=15-line targeted synthesis to Argon.
- **Constraint-Bound Prompts:** Always specify exact input types, expected return contracts, and failure modes. Unambiguous boundaries collapse Argon's internal Tree-of-Thought branching from 5+ exploration paths down to 1 direct proof path.
- **Local Fleet Offloading for Implementation:** Use Argon strictly for architectural design, algorithmic strategy, and verification plans. Offload bulk code typing, regex, test fixtures, and AST checks to the local Ollama fleet (`local-coprocessor` with `qwen3-coder:30b` or `nemotron-3-nano:4b`).
- **Turn-Boundary Compaction:** After Argon establishes an architectural decision or closes a major bug, record state in `.agents/memory/activeContext.md` and recommend `/compact` to purge intermediate deliberation tokens before proceeding.

## 5. Prompt Caching & Local KV-Cache Preservation
- **Static Prefix Invariant:** Keep system rules (`GEMINI.md`) and project instructions strictly immutable during an active session. Never edit rules or append transient state to early context headers; changes to earlier tokens invalidate all subsequent cached tokens for both Argon and Flash.
- **Append-Only Context Discipline:** When recording state or updating progress, always write to disk files (`.agents/memory/activeContext.md`, `docs/WORK_LOG.md`) rather than mutating early system messages. Keep the in-flight conversation trajectory strictly append-only.
- **Stable Command Outputs:** Avoid injecting high-frequency timestamps, random seeds, or dynamic process IDs into prompt messages. Normalized command outputs allow the prompt cache to match previous turns across repeated runs.
- **Local Fleet KV-Cache Alignment:** In `local-coprocessor` and `local-worker` invocations, reuse standardized system prompts so Ollama's local KV-cache remains warm in RTX 5060 VRAM, achieving instant time-to-first-token (TTFT).
- **Turn-Boundary Compaction:** Execute `/compact` only when a milestone completes and background tasks are idle. Compacting mid-task flushes the warm prefix cache; compacting at milestone boundaries establishes a fresh, clean prefix anchor.
