---
name: token-economy
description: Output token optimization and high-density communication protocol. Use to minimize output token consumption, prevent transcript context bloat, and maintain concise progress visibility during long engineering workflows.
---

# Output Token Economy & High-Density Protocol

This skill enforces strict token efficiency across agent sessions to preserve user quota and prevent compounding context bloat.

---

## 1. Zero Conversational Overhead
* **Strip Preambles & Fillers:** Eliminate opening pleasantries ("Sure, I can do that!", "Here is what I found:") and closing conversational sign-offs ("Let me know if you need anything else!").
* **Zero Prompt Restatement:** Never echo, paraphrase, or summarize the user's request. Lead directly with actionable technical data, indicators, or code actions.
* **Zero Code Duplication in Chat:** Once code has been created or modified via tools (`replace_file_content`, `write_to_file`, `Edit`), never re-paste the code blocks into chat text. State only the file link, line range, and a 1-sentence rationale.

---

## 2. High-Density Status Indicators
Replace conversational status updates with compact markdown checklists:
* `[✓] Completed step / file path`
* `[→] In progress step`
* `[!] Warning or blocker`
* `[✗] Failure with 1-line error message`

---

## 3. Active Context-Saving Enforcement Chain

To ensure the new frontier efficiency tools are always utilized:

* **Prompt Cache Prefix Stability (`prompt-cache-context-optimizer`):**
  Never interleave dynamic project files between static instructions. Maintain exact prefix order so Anthropic's **90% prompt caching discount** is never broken.
* **Symbol Lookups Over Full-File Reads (`semantic-codebase-indexing`):**
  Query `.code_index_tags.json` via `jq` to locate exact function lines before invoking `view_file`. Never read 500-line files when targeting a 10-line function.
* **Terminal Stream Sanitization (`log-output-sanitizer`):**
  Never allow verbose test suites or compiler logs to dump 200+ lines into chat. Use silent/short flags and surface only 1-line metrics or actionable stack traces.
* **Canvas Staged Diffs (`canvas-interactive-workspace`):**
  Stage proposed edits in `.canvas/` and output only targeted unified diff chunks. Prohibit full-file conversational rewrites.
* **Swarm Background Offloading (`subagent-swarm-orchestrator`):**
  Offload multi-file linter sweeps, build logs, and test suites to background worktree subagents, preventing thousands of lines of stdout from polluting the main conversation history.
* **Visual Artifacts Over ASCII Bloat (`generative-visual-artifacts`):**
  Never generate massive 50-line ASCII diagrams or markdown tables in chat. Offload visual UI mockups and telemetry graphs to self-contained HTML artifacts that open in the browser.
* **Reactive Micro-Apps Over Static Tables (`intelligent-interactive-ui`):**
  When generating calculators, ROI models, or parameter tuners, generate single-file reactive widgets rather than burning multi-turn conversational tokens on manual re-calculations.
* **Cropped Vision Over Full-DPI Dumps (`screen-vision-inspector`):**
  Crop screenshots to relevant bounding boxes and downscale to 1280px max dimension before vision ingestion to prevent vision token bloat.
* **Surgical Directive Formatting (`high-density-prompting`):**
  Format instructions with target file, line, exact action, and verification command, suppressing 75%–90% of reasoning token burn.
* **Dynamic Skill Routing Over Catalog Scanning (`dynamic-skill-router`):**
  When tackling complex or multi-domain tasks, query `skill_router.py` to identify the exact 2–3 expert skills rather than reading or injecting dozens of unrelated skill files into prompt context.
* **Episodic Checkpointing Across Compaction (`session-episodic-memory`):**
  Capture decision rationale and active hypotheses in `.agents/episodes/` before running `/compact`, ensuring zero token-cost amnesia upon conversation resumption.

---

## 4. Offloading Heavy Content
* **Large Diffs, Logs, or Plans:** Write extensive documentation, plans, or test matrices into files or artifacts.
* **Documents & Web Templates:** When generating HTML landing pages, PDF templates, invoices, proposals, or contracts, write the entire content directly to disk via `write_to_file`. **Never dump 200+ lines of raw HTML, CSS, or legal text into the chat transcript.**
* **Video Filtergraphs & Subtitles:** When generating long complex FFmpeg filtergraphs, word-level `.ass` / `.srt` subtitle transcripts, or ADB logcat dumps, write them directly to script files or disk assets rather than printing them in full to chat.
* **Shader Code & SPIR-V Disassemblies:** When generating or disassembling extensive shaders (HLSL/GLSL/SPIR-V), write them directly to shader files (`.vert`, `.frag`, `.hlsl`, `.spvasm`) rather than dumping 300+ lines of shader code into chat.
* **Android Native Dumps & Gfxinfo Metrics:** When dumping raw tombstones, HPROF traces, or 200+ frame `dumpsys gfxinfo` tables, capture them to `/tmp/` log files, presenting only the symbolized crash frames or jank frame percentage in chat.
* **VFS Archive Listings & Physics Contact Matrices:** When unpacking or inspecting large asset archives (`vfs_asset_packer.py --list`) or dumping physics contact manifold tables, pipe results to files or artifacts, presenting only summary counts (file count, total payload size, active contact pairs) in chat.
* **ECS Dumps & Save State Payloads:** When inspecting entity archetype tables or raw save state payloads (`save_state_inspector.py --inspect`), offload detailed byte hex dumps to disk/artifacts, presenting only container header validation, schema versions, and compression statistics in chat.
* **Discord API Payloads & Gateway Event Logs:** When querying large Discord API endpoints (guild member lists, audit logs, role hierarchies) or capturing raw WebSocket Gateway dispatch JSON, stream them to temporary `.json` files, presenting only counts, user tags, or permission flags in chat.
* **Audio Waveform Arrays & Loudness Tables:** When generating procedural audio or running FFmpeg loudness filter analysis (`ebur128`), write raw sample arrays and multi-pass JSON logs to disk, outputting only target integrated LUFS, True Peak dB, and file paths in chat.
* **Security Audits, SBOM Manifests & Binary Disassembly:** When generating multi-thousand-line CycloneDX/SPDX SBOM manifests, full `cargo-audit` dependency advisory trees, or native binary disassembly dumps, write them to disk/artifacts, presenting only the vulnerability count, severity breakdown, and `checksec` status table in chat.
* **Proton Logs, Crash Traces & PE Import Tables:** When capturing verbose `PROTON_LOG=1` traces (often 10,000+ lines), Windows Event ID 1000 crash dumps, or extensive PE Import Address Tables, redirect stdout to disk log files, surfacing only the faulting module, exception offset, or missing DLL names in chat.
* **Threat Model Matrices & Pen-Test Logs:** When generating extensive STRIDE threat matrices, DAST penetration test outputs, or network packet captures (`pcap`), offload them to structured artifacts or disk files, presenting only the critical risk score and remediations in chat.
* **Wine Relay Traces & Handheld Performance Logs:** When capturing `WINEDEBUG=+relay` execution traces (hundreds of thousands of Win32 calls) or multi-minute MangoHud/Steam Deck frametime CSVs, pipe them directly to files in `/tmp/`, reporting only the specific hanging function call or 1% low FPS metrics in chat.
* **GameMaker YYP Projects & Room Layout JSON:** When inspecting large GameMaker `.yyp` project manifests or room layer JSON files (tens of thousands of JSON lines), offload to disk/artifacts, presenting only resource counts or modified layer names in chat.
* Provide a single clickable file link and a 1-sentence headline rather than dumping large blocks of markdown or HTML into the chat transcript.

---

## 5. Token Savings Metric Footer
Conclude plans, refactors, and multi-step tasks with a single high-density token economy line quantifying estimated output/quota savings achieved through these constraints:
`📉 Token Economy: ~<N> tokens saved (<breakdown: e.g. cache hits, symbol lookup, swarm offload, surgical diffs>)`
