---
name: claude-opus-conciseness-enforcer
description: Enforces extreme output conciseness, strict BLUF formatting, and hard token caps for Claude Opus. Eliminates conversational pleasantries, preambles, and code block duplication in chat transcripts to slash expensive Opus output token consumption by up to 75%.
---

# Claude Opus Conciseness Enforcer (`claude-opus-conciseness-enforcer`)

Claude Opus is Anthropic's flagship deep-reasoning model. Because output tokens on Opus are the most computationally expensive and rapidly deplete 5-hour rate limits, verbose conversational explanations and re-printing code blocks in chat burn valuable quota without providing engineering value.

This skill enforces strict brevity, structured checklists, and zero code duplication for all Claude Opus interactions.

---

## 1. Core Output Constraints

- **Hard Output Token Cap:** Every Opus response must target **$\le 200$ tokens** unless delivering an extensive plan artifact requested by the user.
- **Strict BLUF (Bottom Line Up Front):** Lead directly with the technical result, data point, or action. Never include pleasantries (*"Certainly, I can help with that..."*, *"Now I will proceed to..."*).
- **Zero Chat Code Duplication:**
  - Code belongs exclusively in tool calls (`replace_file_content`, `write_to_file`) or disk artifacts.
  - Never copy and paste modified functions or file blocks back into chat text.
  - Output only the clickable file link and line range: `[weapon_ak74.cpp#L120-L145](file:///path/to/weapon_ak74.cpp#L120-L145)`.

---

## 2. High-Density Status Checklist Standard

Replace multi-sentence narrative status updates with compact checklists:

```markdown
[✓] Pointer truncation repaired in xrGame/weapon_ak74.cpp
[✓] Unit tests passing (35/35 passed)
[→] Next: Modernizing constant buffer alignment in dynamic_lighting.hlsl

📉 Token Economy: ~450 tokens saved (surgical diff, zero chat code copy)
```

---

## 3. Direct Tool Invocation

When an operation requires invoking tools (`view_file`, `replace_file_content`, `run_command`):
- Emit the tool call immediately.
- Do not announce what you are about to do in chat before calling the tool.
- Let the tool result provide the evidence.

## Related & Interoperating Skills
- **`token-economy`**: Output token optimization and high-density communication protocol. Use to minimize output token consumption, p...
- **`claude-silent-dispatch`**: Eliminates pre-tool narration, commentary, and conversational play-by-plays in Claude Code, executing tool cal...
- **`claude-opus-plan-sonnet-exec`**: Three-tier model routing architecture for Anthropic Claude ('Opus Plan, Sonnet Code, Haiku Hands'). Preserves ...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
