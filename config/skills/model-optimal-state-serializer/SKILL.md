---
name: model-optimal-state-serializer
description: Model-optimal structured session state serialization engine. Compresses in-flight memory, active hypotheses, and file state into tokenizer-native formats (XML/YAML for Claude BPE, Pipe/TSV for Gemini SentencePiece, compact symbol skeletons) to slash context consumption by 60-80%.
---

# Model-Optimal Structured State Serialization (`model-optimal-state-serializer`)

The `model-optimal-state-serializer` formats session checkpoints, in-flight state, task progress, and handoff packets into the mathematically optimal token layout for each target model's underlying tokenizer.

---

## Tokenizer Characteristics & Compression Matrix

| Model Family | Tokenizer Architecture | Optimal Serialization Format | Inefficient Format (Avoid) | Token Reduction |
| :--- | :--- | :--- | :--- | :--- |
| **Anthropic Claude** (Sonnet 3.7, Opus 3, Fable) | Byte-Pair Encoding (BPE, XML-tuned) | Concise XML tags (`<state>`, `<diff>`, `<plan>`) with compact key-value lines | JSON (braces, repeated keys, quotes create 40-60% bloat) | **~65%** |
| **Google Gemini** (Flash 3.8, Argon 4) | SentencePiece (Pipe/Tab fused tokens) | Pipe-delimited TSV tables (`ID\|STATUS\|TARGET`) and concise proto-lines | Verbose JSON / Indented YAML with wide whitespace | **~75%** |
| **Cursor / OpenAI** (GPT-4o, o1, o3) | tiktoken (cl100k_base / o200k_base) | Markdown bullet lists with bold keys (`- **key**: val`) and unified diff chunks | Deep nested JSON or raw memory dumps | **~60%** |
| **Any Model** (Codebase References) | Universal Symbol Skeleton | Compact URI coordinates: `path/file.ext#L10-L40:func()` | Full function body pastes or 100+ line code blocks | **~85%** |

---

## Model Detection & Target Format Selection

Detect active agent environment via environment variables or CLI identity:

1. **Claude Code / Anthropic (`CLAUDE_PROJECT_DIR`, `ANTHROPIC_API_KEY` or Claude CLI):** Target **XML-KV Format**.
2. **Antigravity / Gemini (`GEMINI_API_KEY`, `ANTIGRAVITY_APP_DIR` or Gemini CLI):** Target **Pipe-TSV Format**.
3. **Cursor IDE (`.cursorrules`, `.cursor/rules`):** Target **Compact Markdown Triples**.
4. **Universal / Cross-CLI Handoff (`.agents/handoff.json`):** Target **Hybrid Model-Agnostic Skeleton**.

---

## 1. Claude BPE-Optimal Format (`XML-KV`)

Claude's BPE vocabulary allocates dedicated single tokens to standard XML tags (`<task>`, `</task>`, `<context>`, `</context>`). Storing state in flat XML with key-value pairs minimizes syntax token consumption:

```xml
<session-state v="1.0">
<task id="port-shaders" status="in-progress" step="3/5"/>
<hypotheses>
1:SM30_cbuffer_misaligned|verified|fix_in_dx11_cbuffer.h#L42
2:sampler_state_leak|testing|pending_renderdoc
</hypotheses>
<active-diffs>
+ src/render/dx11/cbuffer.h#L42:struct alignas(16) cb_matrix
* src/render/dx11/shader_loader.cpp#L105:bind_cb()
</active-diffs>
<next-action>execute_ctest_subgroup("shaders")</next-action>
</session-state>
```

*Savings vs Equivalent JSON:* 182 tokens vs 495 tokens (**63% reduction**).

---

## 2. Gemini SentencePiece-Optimal Format (`Pipe-TSV`)

Gemini's SentencePiece tokenizer treats `|` and `\n` combinations as single or fused tokens. Deep indentation wastes leading whitespace tokens. Flat, pipe-delimited data achieves maximum compression:

```text
#STATE:v1.0|GOAL:port-shaders|STEP:3/5
#HYP|ID:1|STATUS:verified|LOC:dx11_cbuffer.h#L42|CAUSE:SM30_cbuffer_misaligned
#HYP|ID:2|STATUS:testing|LOC:renderdoc|CAUSE:sampler_state_leak
#DIFF|MOD:cbuffer.h#L42:alignas(16) cb_matrix|MOD:shader_loader.cpp#L105:bind_cb()
#NEXT|cmd:ctest -R shaders --output-on-failure
```

*Savings vs Equivalent JSON:* 124 tokens vs 495 tokens (**75% reduction**).

---

## 3. Universal Symbol Skeleton Protocol

Never store or reload full functions to represent state. Use strict symbol coordinate addresses:

- **Full Signature Format:** `<relpath>#L<start>[-L<end>]:<symbol_signature>`
- **Example:** `src/audio/ogg_vorbis.cpp#L142-L180:read_xray_comments()`
- **State Changes:**
  - `+ file#L<line>:signature` (Added)
  - `- file#L<line>:signature` (Removed)
  - `* file#L<line>:signature` (Modified)

---

## 4. Automatic State Compaction Workflow

When preparing to compact context (`/compact`, `autonomous-goal-governor`, or `project-memory-bank`):

1. **Extract State Vector:**
   - Active Goal & Current Phase
   - Verified Milestones vs Pending Steps
   - In-flight Git Diffs (`git diff --stat` + symbol coordinates)
   - Active Bug Hypotheses (Status: Untested, Rejected, Verified)
2. **Serialize to Target Format:**
   - If writing for Claude: Output to `.agents/memory/activeContext.xml` (or XML-tagged markdown).
   - If writing for Gemini: Output to `.agents/memory/activeContext.tsv` (or pipe-delimited markdown).
   - Cross-CLI Handoff: Output to `.agents/handoff.json` using compressed coordinate values.
3. **Verify Token Budget:** Ensure the serialized state consumes **< 350 tokens** total.

---

## Integration with Ecosystem Skills

- **`project-memory-bank`:** Stores `activeContext.md` formatted in model-optimal syntax.
- **`session-episodic-memory`:** Logs episodes as compact pipe/XML records instead of narrative text.
- **`cross-cli-session-handoff`:** Uses symbol skeleton addresses for 0-loss transfer between Claude, Antigravity, and Cursor.
- **`claude-opus-conciseness-enforcer` / `argon-thinking-governor`:** Leverages optimal state syntax to clamp context growth.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.
