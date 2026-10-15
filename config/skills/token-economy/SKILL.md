---
name: token-economy
description: Output token optimization and high-density communication protocol. Use to minimize output token consumption, prevent transcript context bloat, and maintain concise progress visibility during long engineering workflows.
---

# Output Token Economy & High-Density Protocol

This skill enforces strict output token efficiency across agent sessions to preserve user quota and prevent context bloat.

## 1. Zero Conversational Overhead
- **Strip Preambles & Fillers:** Eliminate opening pleasantries ("Sure, I can do that!", "Here is what I found:") and closing conversational sign-offs ("Let me know if you need anything else!").
- **Lead with Results:** The first line of response should be the answer, the status indicator, or the action taken.

## 2. High-Density Status Indicators
Replace conversational status updates with compact markdown checklists:
- `[✓] Completed step / file path`
- `[→] In progress step`
- `[!] Warning or blocker`
- `[✗] Failure with 1-line error message`

## 3. Tool Execution & Output Discipline
- **Silent Success:** When terminal commands or tools succeed with standard expected output, do not paste the raw stdout into chat. Summarize cleanly:
  - *Verbose (bad):* Pasting 50 lines of compiler output.
  - *High-Density (good):* `cargo test: 18 passed, 0 failed (0.42s)`
- **Surgical Edits:** Use `replace_file_content` targeting only the lines that changed. Avoid rewriting entire 500+ line files when modifying a single function.

## 4. Offloading Heavy Content
- **Large Diffs, Logs, or Plans:** Write extensive documentation, plans, or test matrices into files or artifacts.
- Provide a single clickable file link and a 1-sentence summary rather than dumping 200 lines of markdown into the chat transcript.
