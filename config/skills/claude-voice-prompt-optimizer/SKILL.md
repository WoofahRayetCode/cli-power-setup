---
name: claude-voice-prompt-optimizer
description: Eliminates conversational mirroring and normalizes stream-of-consciousness voice dictation from agy-mic-button into direct, high-density Claude Code actions.
---

# Claude Voice Prompt Optimizer (`claude-voice-prompt-optimizer`)

When users interact with Claude Code via voice dictation or the system-wide microphone button (`agy-mic-button`), transcription models often generate conversational filler, thinking pauses ("um", "uh"), and phonetic approximations of programming terms.

This skill equips Claude Code with **Zero Conversational Mirroring** and **Automatic Phonetic Code Normalization**.

---

## 🎙️ 1. Zero Conversational Mirroring

- **Strip Conversational Filler**: Never reply in a conversational tone just because the prompt was spoken.
- **No Pleasantries**: Omit conversational openers ("Sure!", "I'd be happy to help with that!").
- **Lead Directly with Technical Action**: Output only actionable checklists, command results, or surgical diffs.

---

## 🗣️ 2. Natural-Language Slash Command Routing

Translate spoken phrases directly into Claude actions:
- Spoken *"set a goal..."*, *"run a goal..."* $\rightarrow$ Formulate a verifiable goal contract in `.agents/memory/activeContext.md` and execute end-to-end.
- Spoken *"make a plan..."* $\rightarrow$ Activate `/plan` planning workflow.
- Spoken *"use boost..."* $\rightarrow$ Engage `claude-adversarial-verification-gate`.
- Spoken *"grill me..."* $\rightarrow$ Run interactive interview questions before implementation.
- Spoken *"clamshell mode"* $\rightarrow$ Execute `laptop-perf clamshell-3d`.

---

## 🔤 3. Phonetic Code Term Normalization

| Spoken Transcription | Normalized Technical Code Token |
| :--- | :--- |
| "see plus plus" | `C++` |
| "oh gee ess are" | `OGSR` |
| "ex ray" | `X-Ray` |
| "ell tee ex" | `LTX` |
| "dot cpp" | `.cpp` |
| "you input" | `/dev/uinput` |
| "pie test" | `pytest` |
| "cmake lists" | `CMakeLists.txt` |
| "get status/commit/push" | `git status/commit/push` |
