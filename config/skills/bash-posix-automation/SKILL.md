---
name: bash-posix-automation
description: Defensive Bash and POSIX shell engineering, strict runtime error handling, signal cleanup traps, argument parsing with getopts, atomic file operations, and ShellCheck compliance.
---

# Defensive Bash & POSIX Automation

This skill enforces bulletproof, defensive shell scripting practices across Linux, macOS, and POSIX environments.

---

## 🐚 Core Principles

1. **Strict Runtime Safeguards:** Mandatory `set -euo pipefail` and `IFS=$'\n\t'` to prevent silent failures and word splitting.
2. **Safe Signal Trapping:** Guaranteed cleanup of temporary files, sockets, and child processes via `trap cleanup EXIT INT TERM`.
3. **Deterministic CLI Interfaces:** Portable argument parsing with standard `getopts`, supporting `--help`, `--dry-run`, and `--verbose`.
4. **Atomic Operations & Concurrency:** Race-free file operations using `mktemp` and lockfiles via `flock`.
5. **Static Verification:** Enforce 100% clean ShellCheck (`shellcheck -s bash`) runs on all automation scripts.

---

## 🛠️ 1. Canonical Production Script Template

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'

# --- Configuration & Defaults ---
SCRIPT_NAME="$(basename "$0")"
VERBOSE=0
DRY_RUN=0
TEMP_DIR=""

# --- Cleanup Trap ---
cleanup() {
    local exit_code=$?
    if [[ -n "${TEMP_DIR:-}" && -d "${TEMP_DIR}" ]]; then
        rm -rf "${TEMP_DIR}"
    fi
    exit "${exit_code}"
}
trap cleanup EXIT INT TERM

# --- Helper Logging ---
log_info() { echo "[INFO] $*" >&2; }
log_err()  { echo "[ERROR] $*" >&2; }
log_debug() { [[ "${VERBOSE}" -eq 1 ]] && echo "[DEBUG] $*" >&2 || true; }

# --- Usage ---
usage() {
    cat <<EOF
Usage: ${SCRIPT_NAME} [OPTIONS] <TARGET>

Options:
  -h, --help       Show this help message
  -v, --verbose    Enable verbose debug output
  -n, --dry-run    Simulate actions without modifying files

EOF
    exit 0
}

# --- Argument Parsing ---
while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help) usage ;;
        -v|--verbose) VERBOSE=1; shift ;;
        -n|--dry-run) DRY_RUN=1; shift ;;
        --) shift; break ;;
        -*) log_err "Unknown option: $1"; usage ;;
        *) break ;;
    esac
done

TEMP_DIR="$(mktemp -d -t "${SCRIPT_NAME}.XXXXXX")"
log_debug "Created temp directory at ${TEMP_DIR}"
```

---

## 🔒 2. Concurrency & Lockfiles

Prevent concurrent script execution using `flock`:
```bash
LOCK_FILE="/var/lock/my_automation.lock"
exec 200>"${LOCK_FILE}"
flock -n 200 || { log_err "Another instance is already running."; exit 1; }
```

---

## 🔄 Interoperability & Handoffs

* **Parity with `powershell-windows-automation`:** When authoring multiplatform repos, provide a matching `setup.ps1` with identical CLI parameters (`--help`, `--dry-run`, `--verbose`).
* **Handoff to `cachyos-arch-packaging`:** For PKGBUILD `package()` and `build()` functions.
* **Handoff to `linux-systems-engineering`:** When scripts interact with kernel parameters, D-Bus interfaces, or systemd services.\n