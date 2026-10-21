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
