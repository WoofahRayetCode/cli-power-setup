# Universal Agent Engineering Guidelines

## 1. Interaction & Protocol
- No conversational preamble or repetitive recaps. State actions, test statuses, and diffs cleanly.
- Report tool execution outcomes concisely rather than dumping raw stdout.
- Use targeted replacements (`edit_file`) rather than full-file rewrites.

## 2. Directory Confinement & Sandboxing
- Confine all file creations and modifications strictly within the target repository root.
- Use hermetic package runtimes (`.venv/bin/python`, `cargo`) without touching host packages.
- Never write credentials or sensitive data to disk or git history.

## 3. Verification & Memory
- Always verify changes with actual compiler/test commands prior to marking a milestone done.
- Document progress, architectural discoveries, and dead ends in `.agents/memory/activeContext.md`.
