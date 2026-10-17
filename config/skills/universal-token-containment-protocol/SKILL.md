---
name: universal-token-containment-protocol
description: Universal cross-model and cross-domain token containment protocol across all 197 skills (Sonnet, Opus, Fable, Flash, Argon). Mandates zero chat duplication, strict file/artifact offloading, and output clamping across 3D modeling, binary reverse engineering, web design, and game modding.
---

# Universal Token Containment Protocol (`universal-token-containment-protocol`)

Regardless of the model family (Claude Sonnet/Opus/Fable or Gemini Flash/Argon), the single largest source of token and context inflation is **chat transcript pollution**: agents dumping raw data, code blocks, HTML templates, assembly dumps, or full configuration files directly into conversation messages.

This skill establishes universal output containment rules that apply across all engineering tasks and skills.

---

## 1. Domain-by-Domain Containment Rules

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   UNIVERSAL OUTPUT CONTAINMENT MATRIX                  │
├──────────────────────────┬─────────────────────────┬───────────────────┤
│ Domain                   │ Strictly Prohibited     │ Enforced Standard │
├──────────────────────────┼─────────────────────────┼───────────────────┤
│ 3D Modeling (Blender)    │ Vertex/polygon tables in│ Standalone .py in │
│                          │ chat (20k–40k tokens)   │ scratch/ + 3-line │
│                          │                         │ CLI telemetry     │
├──────────────────────────┼─────────────────────────┼───────────────────┤
│ Binary Reverse Eng.      │ Dumping 100+ lines of   │ Max 30 lines      │
│ (objdump, Ghidra, REA)   │ raw disassembly/hex     │ disassembly; full │
│                          │                         │ dumps to scratch/ │
├──────────────────────────┼─────────────────────────┼───────────────────┤
│ Web & Micro-Apps         │ Pasting full HTML/CSS/JS│ Write directly to │
│ (Three.js, D3, Starlight)│ into chat messages      │ disk/artifact;    │
│                          │                         │ return link only  │
├──────────────────────────┼─────────────────────────┼───────────────────┤
│ Game Modding (LTX/C++)   │ Re-printing full LTX    │ Surgical chunk    │
│ (X-Ray, OGSR, ZoneForge) │ configs or source files │ replacements only │
│                          │                         │ (replace_file_ct) │
├──────────────────────────┼─────────────────────────┼───────────────────┤
│ Test Suites & Compilers  │ 5,000-line passing logs │ Quiet flags       │
│ (pytest, cargo, ctest)   │ in context              │ (pytest -q,       │
│                          │                         │ cargo test -q)    │
└──────────────────────────┴─────────────────────────┴───────────────────┘
```

---

## 2. The Artifact & File Offloading Mandate

- **The Rule:** Any content exceeding **40 lines** (contracts, SOWs, HTML templates, architectural designs, detailed logs) must be written directly to a file on disk or an artifact in `<appDataDir>/brain/<conversation-id>/`.
- **Response Format:** Return a 1-line headline and a clickable markdown file link:
  ```markdown
  [✓] Architecture plan created: [`system_architecture.md`](file:///path/to/system_architecture.md)
  ```
- **Prohibited:** Re-summarizing the entire file contents in the chat text after creating it.

---

## 3. Zero Code Duplication in Messages

- Once code is edited via `replace_file_content` or `write_to_file`, **never re-paste the code snippet into the conversation**.
- State only:
  - The modified file link and line range: `[xrEngine.cpp#L45-L62](file:///path/to/xrEngine.cpp#L45-L62)`
  - A 1-line technical rationale.

---

## 4. Closing Token Economy Signature

Conclude multi-step workflows with the standard token economy savings metric:
```text
📉 Token Economy: ~<N> tokens saved (<surgical diffs, artifact offload, quiet flags>)
```

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`blender-headless-token-shield`**: Quota and context token protector for 3D modeling and Blender workflows. Prohibits dumping raw vertex coordina...
- **`cross-agent-context-deduplicator`**: Eliminates redundant transcript ingestion and context pollution between Argon orchestrators and Flash subagent...
- **`cross-model-switch-pruner`**: Pre-switch state compaction and history virtualization engine when switching models (Sonnet to Fable, Opus, or...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
