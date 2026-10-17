---
name: speculative-multi-step-drafting
description: Bundles predictable consecutive edits and multi-file modifications into single-turn atomic dispatches, slashing multi-turn reasoning overhead and saving up to 75% input tokens.
---

# Speculative Multi-Step Drafting (`speculative-multi-step-drafting`)

Modern speculative decoding runtimes accelerate generation by drafting multiple predictable tokens or steps in a single forward pass.

In interactive coding assistants, agents routinely burn 4 separate conversational turns to make 4 predictable edits:
1. Turn 1: Edit Header (`.h`), wait for user/tool return.
2. Turn 2: Edit Implementation (`.cpp`), wait for return.
3. Turn 3: Edit Config (`.ltx`), wait for return.
4. Turn 4: Run compiler test.

Each turn re-bills the entire conversation context. This skill enforces **Speculative Multi-Step Bundling**, executing all predictable modifications in a single turn.

---

## 1. Bundled Execution Architecture

```
Traditional Serial Turns (4 Turns = 4x Full Context Re-read):
  Turn 1: Edit .h ----> Turn 2: Edit .cpp ----> Turn 3: Edit .ltx ----> Turn 4: Build

Speculative Multi-Step Drafting (1 Turn = 1x Context Re-read):
  Turn 1: [ Edit .h + Edit .cpp + Edit .ltx + Run Build ] (75% Quota Saved!)
```

---

## 2. Invariant Bundling Rules

1. **Parallel Tool Invocation:** When multiple changes are deterministic and independent, emit all `replace_file_content` tool calls in the exact same model turn.
2. **Pre-flight Speculation:** If adding a function requires updating both a header and an implementation, never emit the header change alone—bundle both changes together.
3. **Automated Verification Included:** Append the pre-flight syntax check or test runner command in the same turn so verification occurs immediately.

---

## 3. Token Economics

| Execution Strategy | Turns Required | Input Tokens Billed (at 100k context) | Output Overhead |
| :--- | :--- | :--- | :--- |
| **Serial Execution** | 4 turns | 400,000 tokens | 4x preambles |
| **Speculative Bundling** | **1 turn** | **100,000 tokens (75% saved)** | **1x preamble** |
