# Engineering & Game Modding Rules

## Engineering Discipline
- **Plan Before Major Modifications:** When working on complex tasks, multi-file refactors, or new mod architectures, outline the implementation plan or invoke `writing-plans` / `/plan`.
- **Systematic Debugging:** Trace bugs and game crashes to root causes via engine logs, stack traces, and reproducible test cases before changing code. Do not speculate or randomly alter values.
- **Evidence-Based Completion:** Verify that code builds, unit tests pass, and assets parse before declaring any task complete.

## Game Modding & S.T.A.L.K.E.R. EE Rules
- **Protect Vanilla Baselines:** Treat unpacked game archives (e.g. `unpacked/`) as strictly read-only references for diffs. Mod files belong in project mod source directories.
- **LTX Syntax Discipline:** Respect case-sensitivity, correct section headers (`[section]`), inheritance (`[child]:parent`), and avoid trailing commas or malformed keys.
- **Audio Integrity:** When modifying or converting S.T.A.L.K.E.R. audio, never use standard editors that strip the proprietary GSC binary engine chunk from the Ogg Vorbis comment header. Use ZoneForge asset replacement tools to preserve distance and volume parameters.
- **Texture Standards:** Use DXT1 for opaque/1-bit alpha and DXT5 for smooth alpha. In shared UI atlas sheets (e.g. `ui_menu_backgraund`), use region replacement rather than overwriting the entire atlas sheet.
- **Autonomous Hands-Free Playtest & QA:** When testing ported mods (e.g. S.T.A.L.K.E.R. Complete to OGSR) without live user input, immediately launch `stalker-playtest-runner` to autonomously take control of character movement via `/dev/uinput`, monitor frames for missing textures/freezes, and auto-triage crash dialogs.

## Output Token Economy & High-Density Visibility
- **Zero Conversational Fluff:** Omit pleasantries, preambles ("Sure, I can help with that", "Now I will proceed to..."), and conversational sign-offs. Lead directly with the technical result or action.
- **High-Density Status:** Report multi-step progress using compact checklists (`[✓] Step complete`, `[→] In progress`) rather than multi-sentence narratives.
- **Silent Tool Success:** Do not narrate routine tool executions or echo entire successful command outputs into chat. Show only actionable errors, test pass/fail tallies, and critical metrics.
- **Surgical Edits Over Rewrites:** Always prefer targeted chunk replacements (`replace_file_content`) over full-file overwrites to minimize token thrashing.
- **Artifact & File Offloading:** For extensive plans, large reports, detailed logs, HTML templates, reactive micro-apps, landing pages, contracts, proposals, and invoices, write them directly to files or artifacts and provide a clickable link with a 1-line headline, rather than dumping large blocks of text, HTML, or markdown directly into the chat transcript.
- **Zero Code & Template Duplication in Chat:** Once code, HTML templates, or documents are created or modified via tools, never re-paste the content blocks into chat. State only the file link, line range, and rationale.
- **Zero Prompt Restatement:** Never echo or paraphrase the user's request. Lead immediately with the action, data, or checklist.
- **Token Economy Visibility:** Conclude plans, refactors, and multi-step workflows with a single high-density token savings line: `📉 Token Economy: ~<N> tokens saved (<breakdown, e.g. surgical diffs, artifact offload, Flash routing>)`.

## Hardware-Aware High-Performance Execution
- **Dynamic Thread Saturation:** Automatically saturate all available CPU threads when compiling, running test suites, or packing assets (`-j$(nproc)` / `MAKEFLAGS="-j$(nproc)"`, `CARGO_BUILD_JOBS=$(nproc)`, `CMAKE_BUILD_PARALLEL_LEVEL=$(nproc)`). Never default to single-threaded builds.
- **Hardware-Aware Tool Dispatch:** Direct heavy GPU tasks (Blender Cycles, voice inference, numerical compute) to CUDA / OptiX or Vulkan rather than slow CPU fallback.
