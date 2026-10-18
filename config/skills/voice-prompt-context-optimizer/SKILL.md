---
name: voice-prompt-context-optimizer
description: Autonomous voice-to-text prompt normalizer and context token saver. Eliminates conversational filler, corrects phonetic developer jargon (C++, OGSR, LTX, JSON), translates spoken commands into slash commands, and prevents compounding context bloat across voice-driven AI workflows.
---

# Voice Prompt Context Optimizer (`voice-prompt-context-optimizer`)

Slashes input context token burn and prevents conversational echoing when using speech-to-text voice dictation (`agy-mic-button`, Whisper, Vosk, or desktop speech).

## The Hidden Cost of Voice Dictation

1. **Conversational Bloat (3x–5x Token Multiplier):**
   - Natural spoken speech contains 300%–500% more tokens than written directives (*"Hey, can you please take a look at...", "um", "uh", "you know", "I was thinking maybe we could..."*).
2. **Context Compounding Across Multi-Turn Sessions:**
   - Every unnecessary spoken pleasantry remains in the transcript history and is re-billed on every single subsequent turn.
3. **Phonetic Transcription Glitches:**
   - Speech-to-text engines mistranscribe developer and modding terminology (*"see plus plus"* for `C++`, *"oh gee ess are"* for `OGSR`, *"ell tee ex"* for `LTX`, *"dot cpp"* for `.cpp`).
4. **The Conversational Mirroring Trap:**
   - When an AI receives conversational voice transcripts, it tends to respond conversationally (*"Sure! I'd be happy to help..."*), violating the Output Token Economy and wasting expensive output reasoning tokens.

---

## The Voice-to-Code Normalization Matrix

| Spoken Phonetic Speech | Normalized Code Token | Domain |
| :--- | :--- | :--- |
| *"see plus plus"* / *"c plus plus"* | `C++` | Languages & Compilers |
| *"c sharp"* / *"see sharp"* | `C#` | Languages & Compilers |
| *"pie test"* | `pytest` | Testing |
| *"cmake lists"* / *"sea make"* | `CMakeLists.txt` / `CMake` | Build Systems |
| *"dot cpp"* / *"dot hpp"* / *"dot h"* | `.cpp` / `.hpp` / `.h` | Source Files |
| *"dot ltx"* / *"dot ogf"* / *"dot dds"* | `.ltx` / `.ogf` / `.dds` | S.T.A.L.K.E.R. Assets |
| *"oh gee ess are"* / *"ogsr engine"* | `OGSR Engine` | Game Modding |
| *"ex ray"* / *"x ray engine"* | `X-Ray Engine` | Game Modding |
| *"ell tee ex"* | `LTX` | Game Configs |
| *"you input"* / *"dev uinput"* | `/dev/uinput` | Linux Input Systems |
| *"dev shm"* | `/dev/shm` | RAM-Disk tmpfs |
| *"rtx fifty sixty"* / *"optics"* | `RTX 5060` / `OptiX` | Hardware GPU |
| *"get status"* / *"get commit"* | `git status` / `git commit` | Version Control |
| *"reverse engineer anything"* / *"rea"* | `reverse-engineer-anything` | Binary RE |

---

## Spoken Natural-Language Slash Command Routing

When voice prompts contain spoken natural-language intent phrases, they map immediately to executable commands:

| Spoken Phrase | Automated Command | Target Skill & Workflow |
| :--- | :--- | :--- |
| *"Set a goal to..."* / *"Goal: ..."* | `/goal <task>` | `autonomous-goal-governor` (Autonomous contract execution) |
| *"Make a plan to..."* / *"Plan: ..."* | `/plan <task>` | `writing-plans` (Granular dependency-ordered tasks) |
| *"Use boost to..."* / *"Boost mode..."*| `/boost <task>` | `first-principles-reasoning` (Formal adversarial gate) |
| *"Grill me on..."* | `/grill-me <topic>` | `brainstorming` (Interactive requirements interview) |
| *"Clamshell mode"* | `laptop-perf clamshell-3d` | `laptop-performance-profile` (Lid-closed GPU render lock) |

---

## Agent Behavioral Directive for Voice Input

Whenever incoming prompts exhibit speech-to-text dictation characteristics (conversational filler, missing punctuation, phonetic jargon):
1. **Never Mirror Tone:** Do not respond with pleasantries, apologies, or preambles.
2. **Normalize Internally:** Read phonetic code terms as their exact symbolic equivalents.
3. **Lead Directly with Technical Action:** Formulate the structured checklist or execute the tool directly.
4. **Token Savings Line:** Include estimated token savings in multi-step workflows.

---

## CLI Usage

```bash
# Normalize spoken voice transcript in <2ms (0 cloud tokens)
voice-prompt-optimizer "hey can you please take a look at the see plus plus shaders in the xray engine and fix the bloom"

# Extreme distillation using local Qwen 1.5B coprocessor
voice-prompt-optimizer "long rambling multi-sentence voice dictation..." --slm

# Subshell pipe directly into agy or bash command
agy "$(voice-prompt-optimizer 'set a goal to port shaders and run tests' --exec)"
```

---

## Token Context Savings Ledger Integration
Every invocation of `voice-prompt-optimizer` automatically calculates the token delta (`orig_tokens - clean_tokens`) and logs cumulative prompt savings directly to `token_ledger.json` under `prompt_context_savings_by_technique["voice_prompt_context_optimizer"]`, feeding live token telemetry directly into `agy-quota-statusline`.

## Windows 10/11 & Cross-Platform Parity (`windows-linux-cross-os-runtime-bridge`)
- Compatible with both Linux and Windows 10/11 (`install.ps1` / `.cmd` shims, `Path(tempfile.gettempdir())`, and native toolchain resolution).

## Related & Interoperating Skills
- **`high-density-prompting`**: Compresses verbose prompts into surgical, quota-saving directives, eliminates speculative reasoning tokens, an...
- **`voice-speech-audio-synthesis`**: Speech-to-text transcription via Whisper, natural voice generation using Piper/Kokoro/OpenAI TTS, game NPC dia...
- **`claude-silent-dispatch`**: Eliminates pre-tool narration, commentary, and conversational play-by-plays in Claude Code, executing tool cal...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
