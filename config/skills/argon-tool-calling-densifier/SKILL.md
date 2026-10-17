---
name: argon-tool-calling-densifier
description: Enforces compact parallel tool invocation and parameter density on Gemini 4 Argon to minimize output token generation costs and round-trip latency.
---

# Argon Tool Calling Densifier (`argon-tool-calling-densifier`)

Under Gemini 4 Argon, model generation output is priced at **$10.00 / 1M tokens** (5x higher than input tokens). When Argon performs multi-step modifications or diagnostics:
- Emitting tool calls one-by-one across separate conversational turns burns output tokens on repetitive conversational preambles and tool declarations.
- Serialized tool calling increases wall-clock latency and context growth.

This skill enforces parallel tool bundling and zero conversational fluff during tool dispatches.

---

## 1. Principles of Tool Densification

### 1. Parallel Batching
When multiple independent actions are needed (e.g. inspecting 3 files, creating 2 sibling modules):
- **Never:** Issue 1 tool call, wait for the response, issue the 2nd tool call, wait, issue the 3rd.
- **Always:** Issue all 3 tool calls in a single turn.

### 2. Zero-Preamble Execution
- Do not generate sentences explaining what tool is about to be called (e.g. *"Now I am going to view file X to see if..."*).
- Emit the tool call directly. Argon's output tokens are reserved purely for the tool call payload itself.

### 3. Argument Minimization
- Pass only essential parameters.
- When replacing file content, target specific 15–30 line chunks (`replace_file_content`) instead of rewriting whole multi-hundred line files (`write_to_file`), cutting Argon output tokens by up to **90%**.

---

## 2. Token Impact

| Dispatch Pattern | Turns Required | Output Tokens Generated | Cost Ratio |
| :--- | :--- | :--- | :--- |
| **Serial Tool Execution (with preamble)** | 4 turns | ~1,200 tokens | 1.0x (Baseline) |
| **Parallel Bundled Dispatch (zero fluff)** | 1 turn | ~280 tokens | **0.23x (77% saved)** |
