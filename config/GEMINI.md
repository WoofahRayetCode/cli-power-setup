# Engineering & Game Modding Rules

## Engineering Discipline
- **Plan Before Major Modifications:** When working on complex tasks, multi-file refactors, or new mod architectures, outline the implementation plan or invoke `writing-plans` / `/plan`.
- **Systematic Debugging:** Trace bugs and game crashes to root causes via engine logs, stack traces, and reproducible test cases before changing code. Do not speculate or randomly alter values.
- **Evidence-Based Completion:** Verify that code builds, unit tests pass, and assets parse before declaring any task complete.

## Game Modding & S.T.A.L.K.E.R. EE Rules
- **Protect Vanilla Baselines:** Treat unpacked game archives (e.g. `unpacked/`) as strictly read-only references for diffs. Mod files belong in project mod source directories.
- **LTX Syntax Discipline:** Respect case-sensitivity, correct section headers (`[section]`), inheritance (`[child]:parent`), and avoid trailing commas or malformed keys.
- **Audio Integrity:** When modifying or converting S.T.A.L.K.E.R. audio, never use standard editors that strip the proprietary GSC binary engine chunk from the Ogg Vorbis comment header. Use ZoneForge asset replacement tools to preserve distance and volume parameters.
- **Autonomous Hands-Free Playtest & QA:** When testing ported mods (e.g. S.T.A.L.K.E.R. Complete to OGSR) without live user input, immediately launch `stalker-playtest-runner` (interoperating with `self-improving-qa`, `nav-graph-recorder`, and `game-window-helper`) to autonomously dismiss 'Press any key to play' loading screens, inject god mode / infinite ammo cheats, take control of character movement via `/dev/uinput`, monitor frames for missing textures/freezes, and auto-triage crash dialogs.
- **X-Ray Crash Interception & Modal Dismissal:** When OGSR or X-Ray crashes under Wine/Proton and spawns a Notepad or BugTrap crash log window (`xray_*.log - Notepad`), immediately run `xray_crash_handler.py sweep` or rely on `stalker-playtest-runner` to extract the crash stack trace and terminate `notepad.exe` so tests never hang.
- **Dialogue & Conversation UI Integrity:** When editing string tables or conversation scripts, validate XML syntax, missing string IDs, text overflow, and talk dialog formatting with `game-dialogue-tool` to prevent runtime truncation or CTDs.
- **Weather, Lighting & Telemetry Tuning:** Balance sun shafts, bloom, and dynamic skyboxes using `weather-lighting-tuner`, and monitor live rendering metrics using `mangohud-configurator`.
- **Task Velocity & Anti-Thrashing Discipline:** Enforce `task-velocity-governor` (5-step targeted rule, stop once tests pass, break 3-strike file churn loops) and `first-principles-reasoning` (Chain-of-Verification, Ockham's razor on bug hypotheses) to ensure porting tasks don't take longer than necessary.
- **Laptop Acoustics & Night Governance:** Interoperate with `laptop-performance-profile` (use `laptop_performance_controller.py sleep-mode` during overnight runs or when muted, and `boost-exec` for heavy parallel builds).
- **Lore Research & Web Architecture:** When documenting game lore, faction histories, or creating modding web portals, leverage `humanities-lore-research`, `creative-web-design-archetypes`, `static-site-architecture`, and `interactive-data-visualization-web`.

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

## Quota Governance & Uninterrupted Execution
- **Never Quit on Available Quota:** Quota percentages (e.g. 5h: 86%, Wk: 96%) indicate healthy available headroom. Never quit, halt, or abort autonomous goals or test runners when quota is available (> safe reserve limits).
- **5-Hour Exhaustion Wait-for-Refresh:** If rolling 5-hour quota reaches or drops below safe reserve during autonomous runs, do not abort or fail the task. Stage working state to `.agents/memory/activeContext.md`, safely sleep until the recorded reset timestamp passes, verify quota replenishment, and seamlessly resume execution.
- **Smart Checkpoint at 25% Weekly Reserve:** When weekly quota nears 25% remaining, automatically snapshot all uncommitted diffs, git branch, and active hypothesis context to `.agents/checkpoints/` and update `.agents/memory/activeContext.md` before continuing execution.
- **Uninterrupted Compaction & Seamless Goal Resumption:** Compaction must **never** interrupt an active goal, plan, or test run. Always execute compaction at clean step boundaries (immediately after a tool or test run completes, before the next edit cycle). Before `/compact`, verify `.agents/memory/activeContext.md` contains the active goal, current in-flight state, and resumption instructions. Upon resuming post-compaction, immediately read `activeContext.md` (<300 tokens) and proceed directly to the next step without pausing or asking the user for direction.

## Gemini 4 Argon Thinking Governance & Internal CoT Quota Clamping
- **Direct Tool Action Over Monologue:** When calling tools (`view_file`, `replace_file_content`, `run_command`, `write_to_file`), invoke the tool call directly without preamble, internal speculative monologues, or reciting file contents in reasoning.
- **Thinking Token Budgeting:** Restrict internal reasoning to structural problem-solving (e.g. edge cases, compiler error diagnosis, architecture). Routine file edits, syntax fixes, and bash command dispatches must execute with minimal reasoning overhead.
- **Hybrid "Argon Brain, Flash Hands" Protocol:** For execution-heavy tasks, prefer dispatching file editing and terminal commands via Flash (`--effort low` or `gemini-3.8-flash-low`), reserving Argon (`pro` / `--effort high`) for complex architectural analysis, difficult debugging, and plan formulation.

## Claude Fable 5.1 Quota, Context & Token Governance
- **Subsystem Slice Virtualization:** When operating under Claude Fable 5.1, never load whole multi-thousand-line source trees or raw engine files. Ingest only 30k-token interface skeletons (`fable-virtual-context-manager`, `polyglot-ast-interface-pruner`, `fable_slice_extractor.py`) to avoid re-billing the 1M-token context window on each turn.
- **Atomic 30-Line Diff Chunking:** Restrict all code changes to surgical `replace_file_content` chunks $\le$ 30 lines. Never execute full-file overwrites (`write_to_file`) on existing source code (`fable-atomic-diff-sequencer`).
- **Thinking Token Clamp on Routine Operations:** Enforce low thinking budget on file inspection, line edits, compiler runs, and git status checks. Reserve high thinking budgets exclusively for root-cause crash triage and 64-bit alignment proofs (`claude-thinking-budget-governor`).
- **Hard 80k Compaction Boundary:** Monitor the statusline context fuel gauge. When context approaches 50%–60% (~80k tokens), proactively stage the current active vector to `.agents/memory/activeContext.md` and trigger `/compact` to reset working context back down to baseline, locking the 90% prompt cache discount indefinitely (`context-pruning-watchdog`, `claude-context-rot-shield`).
- **Local Pre-Flight Syntax Gates:** Validate syntax with local host linters (`luac -p`, `ruff`, compiler checks) before executing diffs to prevent expensive Fable trial-and-error reasoning loops (`local-preflight-syntax-gate`).
- **Tokenizer-Native Memory Serialization:** When serializing memory or handoff states, format exclusively in flat XML-KV tags for Claude's BPE tokenizer to slash state token overhead by ~65% (`model-optimal-state-serializer`).

