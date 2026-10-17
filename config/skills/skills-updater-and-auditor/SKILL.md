---
name: skills-updater-and-auditor
description: Automated health auditing, synchronization, and upstream updates for all installed agent skills. Verifies YAML frontmatter integrity, helper script syntax/permissions, host CLI dependencies, and cross-CLI parity across Antigravity and Claude Code.
---

# Skills Updater & Health Auditor

This skill maintains the health, synchronization, and currency of all autonomous agent skills installed across your system. It prevents skill drift, verifies host tool dependencies, repairs script execution permissions, and pulls upstream updates from GitHub with zero manual intervention.

---

## 1. Multi-Environment Synchronization Topology

The system operates across three linked environments:
```text
                  GitHub Upstream Repository
                              │
                    (git pull / git fetch)
                              ▼
        [1] Source Repository: config/skills/ (cli-power-setup)
                     │                 │
           (sync)    │                 │    (sync)
                     ▼                 ▼
[2] Google Antigravity           [3] Claude Code CLI
    ~/.gemini/config/skills/         ~/.claude/skills/
```

* **The Problem:** Adding or modifying a skill in one directory (or pulling updates on another branch) leaves active CLIs running stale, broken, or desynchronized skills.
* **The Solution:** `skills-audit-update` continuously audits all 3 directories to guarantee 100% parity, valid YAML frontmatter, and correct executable permissions.

---

## 2. CLI Command & Usage Reference

The CLI utility is installed to `~/.local/bin/skills-audit-update` and available globally:

### A. Run a Full Health & Integrity Audit
```bash
skills-audit-update --audit
```
* **Checks performed:**
  1. **Parity Check:** Ensures every skill in `config/skills/` exists in `~/.gemini/config/skills/` and `~/.claude/skills/`.
  2. **YAML Frontmatter Validation:** Verifies that every `SKILL.md` contains valid `---` boundaries and non-empty `name:` and `description:` keys.
  3. **Script Syntax & Execution Perms:** Runs `py_compile` on all `.py` scripts, `bash -n` on all `.sh` scripts, and checks executable permissions.
  4. **Host Dependency Detection:** Scans for host tools (`ffmpeg`, `adb`, `glslangValidator`, `spirv-opt`, `renderdoccmd`, `vulkaninfo`, `nvcc`, `cargo`, `cmake`).
  5. **Upstream Git Status:** Queries `origin/main` to detect if remote commits or new skills are waiting to be pulled.

### B. Auto-Repair Permissions and Syntax
```bash
skills-audit-update --fix
```
Automatically applies `chmod +x` to any helper scripts missing executable bits.

### C. Synchronize Skills Across All Environments
```bash
skills-audit-update --sync
```
Copies all repository skills into `~/.gemini/config/skills/` and `~/.claude/skills/` instantly.

### D. Pull Upstream Updates from GitHub
```bash
skills-audit-update --pull
```
Executes a safe `git pull --rebase origin main` and automatically triggers a multi-CLI `--sync`.

### E. Machine-Readable JSON Telemetry
```bash
skills-audit-update --json
```
Emits a structured JSON payload for autonomous subagent verification or statusline integration.

---

## 3. Best Practices for Maintaining Freshness

1. **Pre-Session Verification:** Run `skills-audit-update` when starting large multi-step projects to ensure all toolchain dependencies are available on the host.
2. **Post-Git Pull:** Always run `skills-audit-update --sync` or `./install.sh --all` after merging changes or pulling from GitHub.
3. **Adding New Skills:** After creating a new skill folder in `config/skills/<skill-name>`, run `skills-audit-update --fix --sync` to validate frontmatter and immediately deploy it to both active CLIs.
4. **In-Flight Evolution & Script Promotion (`self-evolving-skill-synthesizer`):** Use `skill-evolve --hot-patch <skill>`, `skill-evolve --promote <script> --to <skill>`, or `skill-evolve --scaffold <name> "<desc>"` during active tasks to update stale instructions or crystallize verified `/tmp` scripts into permanent skill tools in `<50ms`.

