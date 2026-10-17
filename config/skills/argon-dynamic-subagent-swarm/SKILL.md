---
name: argon-dynamic-subagent-swarm
description: Spawns and coordinates parallel Gemini Flash worker subagents to execute high-volume asset conversion, audio processing, and test sweeps simultaneously, slashing porting turnaround time by 80%.
---

# Argon Dynamic Subagent Swarm (`argon-dynamic-subagent-swarm`)

When executing massive game mod migrations (e.g. converting 50,000 Wwise audio events, hundreds of weapon ballistic curves, and high-resolution textures from S.T.A.L.K.E.R. 2 to OGSR), running tasks serially in a single conversational thread burns hours of wall-clock time and clutters the orchestrator's context window.

This skill equips Gemini 4 Argon with **Parallel Subagent Swarm Orchestration**, allowing Argon to dispatch concurrent Flash worker agents to tackle distinct tasks simultaneously.

---

## 1. Hierarchical Swarm Architecture

```
+-------------------------------------------------------------+
|               ORCHESTRATOR: GEMINI 4 ARGON                  |
| - High-level plan decomposition                             |
| - Invariant & architecture enforcement                      |
| - Final verification & integration assembly                 |
+-------------------------------------------------------------+
               /                      |                      \
              v                       v                       v
+-------------------+   +-------------------+   +-------------------+
| WORKER 1 (Flash)  |   | WORKER 2 (Flash)  |   | WORKER 3 (Flash)  |
| Audio Transcoder  |   | Texture Converter |   | Curve Transpiler  |
| - Wwise .wem ->   |   | - TGA/PNG -> DDS  |   | - Parse curves -> |
|   Ogg GSC headers |   |   BC7/DXT5 + THM  |   |   weapons.ltx     |
+-------------------+   +-------------------+   +-------------------+
```

---

## 2. Parallel Swarm Dispatch Directive

Argon dispatches all 3 workers in a single parallel tool invocation using `invoke_subagent`:

```json
{
  "Subagents": [
    {
      "TypeName": "self",
      "Role": "Audio Transcoding Worker",
      "Model": "flash",
      "Prompt": "Convert intermediate Wwise audio in /tmp/s2_audio to Ogg Vorbis using game-audio-ogg-gsc-encoder and place in gamedata/sounds/."
    },
    {
      "TypeName": "self",
      "Role": "Texture Baking Worker",
      "Model": "flash",
      "Prompt": "Batch compress diffuse and normal textures in /tmp/s2_textures to DDS BC7 and BC5 with .thm headers in gamedata/textures/."
    },
    {
      "TypeName": "self",
      "Role": "Ballistics Curve Transpiler",
      "Model": "flash",
      "Prompt": "Parse extracted pakchunk16 AimingWeapon curves and map dispersion parameters into gamedata/config/weapons/."
    }
  ]
}
```

---

## 3. Quota & Velocity Multipliers

1. **Wall-Clock Acceleration:** Running 3 workers simultaneously cuts multi-hour batch asset conversions down to minutes.
2. **Context Isolation:** Hundreds of repetitive command lines stay contained within the Flash workers' isolated contexts.
3. **Argon Quota Preservation:** Argon burns zero weekly quota during the heavy conversion passes, receiving only the final pass/fail tallies from each worker.

## Windows 10/11 & Cross-Platform CLI Interop (`windows-linux-cross-os-runtime-bridge`)
- **Cross-OS Deployment (`install.ps1` & `install.sh`):** All CLI tools (`agy-cheatsheet` / `cs`, `repo-auto-sync`, `skill-evolve`, `skills-audit-update`, `adaptive-model-router`) run natively on Windows 10/11 via `.cmd`/PowerShell shims in `$HOME\.local\bin` and use `Path(tempfile.gettempdir())` instead of hardcoded `/tmp`.
- **Multi-Agent Split Terminal:** On Windows 10/11, use **Windows Terminal (`wt.exe`)** split panes (`wt -p "PowerShell" \; split-pane -V ...`) in place of Linux `tmux`/`kitty`, and `sccache` / MSVC `/MP` for shared build caching across git worktrees.

## Related & Interoperating Skills
- **`argon-subagent-dispatch-routing`**: Implements the 'Argon Brain, Flash Hands' subagent swarm dispatch pattern to offload high-volume read, search,...
- **`argon-hierarchical-worktree-isolator`**: Sandboxes concurrent subagent file modifications into isolated git worktrees, preventing file lock collisions ...
- **`argon-subagent-payload-compressor`**: Enforces high-density structured return envelopes on Gemini subagent messages, eliminating conversational fluf...
- **`dynamic-repo-model-cheatsheet` (`agy-cheatsheet` / `cs`)**: Live statusline & repo model/effort router.
