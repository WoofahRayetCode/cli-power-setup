#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# CLI Power Setup Installer (cli-power-setup)
# Dual-CLI configuration for Google Antigravity (agy) and Claude Code
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DEST="${HOME}/.local/bin"

GEMINI_DIR="${HOME}/.gemini"
GEMINI_SKILLS="${GEMINI_DIR}/config/skills"
GEMINI_RULES="${GEMINI_DIR}/config/GEMINI.md"
GEMINI_CLI_SETTINGS="${GEMINI_DIR}/antigravity-cli/settings.json"

CLAUDE_DIR="${HOME}/.claude"
CLAUDE_SKILLS="${CLAUDE_DIR}/skills"
CLAUDE_RULES="${CLAUDE_DIR}/CLAUDE.md"
CLAUDE_SETTINGS="${CLAUDE_DIR}/settings.json"

CURSOR_DIR="${HOME}/.cursor"
CURSOR_RULES="${CURSOR_DIR}/rules"
CURSOR_GLOBAL_RULES="${HOME}/.cursorrules"
CURSOR_SETTINGS="${HOME}/.config/Cursor/User/settings.json"

COLOR_GREEN="\033[0;32m"
COLOR_CYAN="\033[0;36m"
COLOR_YELLOW="\033[1;33m"
COLOR_RED="\033[0;31m"
COLOR_BOLD="\033[1m"
COLOR_RESET="\033[0m"

log_info()  { echo -e "${COLOR_CYAN}[→]${COLOR_RESET} $1"; }
log_done()  { echo -e "${COLOR_GREEN}[✓]${COLOR_RESET} $1"; }
log_warn()  { echo -e "${COLOR_YELLOW}[!]${COLOR_RESET} $1"; }
log_err()   { echo -e "${COLOR_RED}[✗]${COLOR_RESET} $1"; }

backup_existing() {
    local timestamp
    timestamp="$(date +%Y%m%d_%H%M%S)"
    local backup_dir="${HOME}/.cli_power_setup_backups/backup_${timestamp}"
    log_info "Creating configuration backup in ${backup_dir}..."
    mkdir -p "${backup_dir}"
    
    if [ -d "${GEMINI_SKILLS}" ]; then
        mkdir -p "${backup_dir}/gemini"
        cp -r "${GEMINI_SKILLS}" "${backup_dir}/gemini/skills"
    fi
    if [ -f "${GEMINI_RULES}" ]; then
        cp "${GEMINI_RULES}" "${backup_dir}/gemini/GEMINI.md"
    fi
    if [ -f "${GEMINI_CLI_SETTINGS}" ]; then
        cp "${GEMINI_CLI_SETTINGS}" "${backup_dir}/gemini/settings.json"
    fi
    if [ -d "${CLAUDE_SKILLS}" ]; then
        mkdir -p "${backup_dir}/claude"
        cp -r "${CLAUDE_SKILLS}" "${backup_dir}/claude/skills"
    fi
    if [ -f "${CLAUDE_RULES}" ]; then
        cp "${CLAUDE_RULES}" "${backup_dir}/claude/CLAUDE.md"
    fi
    if [ -f "${CLAUDE_SETTINGS}" ]; then
        cp "${CLAUDE_SETTINGS}" "${backup_dir}/claude/settings.json"
    fi
    if [ -d "${CURSOR_RULES}" ]; then
        mkdir -p "${backup_dir}/cursor"
        cp -r "${CURSOR_RULES}" "${backup_dir}/cursor/rules"
    fi
    if [ -f "${CURSOR_GLOBAL_RULES}" ]; then
        cp "${CURSOR_GLOBAL_RULES}" "${backup_dir}/cursor/.cursorrules"
    fi
    if [ -f "${CURSOR_SETTINGS}" ]; then
        cp "${CURSOR_SETTINGS}" "${backup_dir}/cursor/settings.json"
    fi
    log_done "Backup created successfully."
}

install_binaries() {
    log_info "Installing utility scripts into ${BIN_DEST}..."
    mkdir -p "${BIN_DEST}"
    cp "${SCRIPT_DIR}/bin/agy-quota-statusline" "${BIN_DEST}/agy-quota-statusline"
    chmod +x "${BIN_DEST}/agy-quota-statusline"
    log_done "Installed executable: ${BIN_DEST}/agy-quota-statusline"

    if [ -f "${SCRIPT_DIR}/bin/claude-statusline" ]; then
        cp "${SCRIPT_DIR}/bin/claude-statusline" "${BIN_DEST}/claude-statusline"
        chmod +x "${BIN_DEST}/claude-statusline"
        log_done "Installed executable: ${BIN_DEST}/claude-statusline"
    fi

    if [ -f "${SCRIPT_DIR}/bin/agy-turbo" ]; then
        cp "${SCRIPT_DIR}/bin/agy-turbo" "${BIN_DEST}/agy-turbo"
        chmod +x "${BIN_DEST}/agy-turbo"
        log_done "Installed executable: ${BIN_DEST}/agy-turbo"
    fi

    if [ -f "${SCRIPT_DIR}/bin/claude-turbo" ]; then
        cp "${SCRIPT_DIR}/bin/claude-turbo" "${BIN_DEST}/claude-turbo"
        chmod +x "${BIN_DEST}/claude-turbo"
        log_done "Installed executable: ${BIN_DEST}/claude-turbo"
    fi

    if [ -f "${SCRIPT_DIR}/bin/skills-audit-update" ]; then
        cp "${SCRIPT_DIR}/bin/skills-audit-update" "${BIN_DEST}/skills-audit-update"
        chmod +x "${BIN_DEST}/skills-audit-update"
        log_done "Installed executable: ${BIN_DEST}/skills-audit-update"
    fi

    if [ -f "${SCRIPT_DIR}/bin/stalker-playtest-runner" ]; then
        cp "${SCRIPT_DIR}/bin/stalker-playtest-runner" "${BIN_DEST}/stalker-playtest-runner"
        chmod +x "${BIN_DEST}/stalker-playtest-runner"
        log_done "Installed executable: ${BIN_DEST}/stalker-playtest-runner"
    fi

    if [ -f "${SCRIPT_DIR}/bin/context-watchdog" ]; then
        cp "${SCRIPT_DIR}/bin/context-watchdog" "${BIN_DEST}/context-watchdog"
        chmod +x "${BIN_DEST}/context-watchdog"
        log_done "Installed executable: ${BIN_DEST}/context-watchdog"
    fi

    if [ -f "${SCRIPT_DIR}/bin/game-test-watchdog" ]; then
        cp "${SCRIPT_DIR}/bin/game-test-watchdog" "${BIN_DEST}/game-test-watchdog"
        chmod +x "${BIN_DEST}/game-test-watchdog"
        log_done "Installed executable: ${BIN_DEST}/game-test-watchdog"
    fi

    if [ -f "${SCRIPT_DIR}/bin/game-texture-editor" ]; then
        cp "${SCRIPT_DIR}/bin/game-texture-editor" "${BIN_DEST}/game-texture-editor"
        chmod +x "${BIN_DEST}/game-texture-editor"
        log_done "Installed executable: ${BIN_DEST}/game-texture-editor"
    fi

    if [ -f "${SCRIPT_DIR}/bin/cursor-rules-sync" ]; then
        cp "${SCRIPT_DIR}/bin/cursor-rules-sync" "${BIN_DEST}/cursor-rules-sync"
        chmod +x "${BIN_DEST}/cursor-rules-sync"
        log_done "Installed executable: ${BIN_DEST}/cursor-rules-sync"
    fi

    if [ -f "${SCRIPT_DIR}/bin/game-dialogue-tool" ]; then
        cp "${SCRIPT_DIR}/bin/game-dialogue-tool" "${BIN_DEST}/game-dialogue-tool"
        chmod +x "${BIN_DEST}/game-dialogue-tool"
        log_done "Installed executable: ${BIN_DEST}/game-dialogue-tool"
    fi

    if [ -f "${SCRIPT_DIR}/bin/weather-lighting-tuner" ]; then
        cp "${SCRIPT_DIR}/bin/weather-lighting-tuner" "${BIN_DEST}/weather-lighting-tuner"
        chmod +x "${BIN_DEST}/weather-lighting-tuner"
        log_done "Installed executable: ${BIN_DEST}/weather-lighting-tuner"
    fi

    if [ -f "${SCRIPT_DIR}/bin/mangohud-configurator" ]; then
        cp "${SCRIPT_DIR}/bin/mangohud-configurator" "${BIN_DEST}/mangohud-configurator"
        chmod +x "${BIN_DEST}/mangohud-configurator"
        log_done "Installed executable: ${BIN_DEST}/mangohud-configurator"
    fi

    if [ -f "${SCRIPT_DIR}/bin/game-window-helper" ]; then
        cp "${SCRIPT_DIR}/bin/game-window-helper" "${BIN_DEST}/game-window-helper"
        chmod +x "${BIN_DEST}/game-window-helper"
        log_done "Installed executable: ${BIN_DEST}/game-window-helper"
    fi

    if [ -f "${SCRIPT_DIR}/bin/nav-graph-recorder" ]; then
        cp "${SCRIPT_DIR}/bin/nav-graph-recorder" "${BIN_DEST}/nav-graph-recorder"
        chmod +x "${BIN_DEST}/nav-graph-recorder"
        log_done "Installed executable: ${BIN_DEST}/nav-graph-recorder"
    fi

    if [ -f "${SCRIPT_DIR}/bin/self-improving-qa" ]; then
        cp "${SCRIPT_DIR}/bin/self-improving-qa" "${BIN_DEST}/self-improving-qa"
        chmod +x "${BIN_DEST}/self-improving-qa"
        log_done "Installed executable: ${BIN_DEST}/self-improving-qa"
    fi
}

install_antigravity() {
    echo ""
    log_info "Configuring Antigravity (agy)..."
    
    # 1. Skills
    mkdir -p "${GEMINI_SKILLS}"
    cp -r "${SCRIPT_DIR}/config/skills/"* "${GEMINI_SKILLS}/"
    local count
    count="$(find "${GEMINI_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l)"
    log_done "Installed ${count} skills in ${GEMINI_SKILLS}."

    # 2. Rules
    mkdir -p "$(dirname "${GEMINI_RULES}")"
    if [ ! -f "${GEMINI_RULES}" ]; then
        cp "${SCRIPT_DIR}/config/GEMINI.md" "${GEMINI_RULES}"
        log_done "Installed global GEMINI.md rules."
    else
        if ! grep -q "Output Token Economy" "${GEMINI_RULES}"; then
            echo "" >> "${GEMINI_RULES}"
            cat "${SCRIPT_DIR}/config/GEMINI.md" >> "${GEMINI_RULES}"
            log_done "Appended token economy and modding rules to existing GEMINI.md."
        else
            cp "${SCRIPT_DIR}/config/GEMINI.md" "${GEMINI_RULES}"
            log_done "GEMINI.md updated with latest rules."
        fi
    fi

    # 3. Settings / Statusline
    if [ -d "$(dirname "${GEMINI_CLI_SETTINGS}")" ]; then
        python3 - <<EOF
import json, os
p = os.path.expanduser("${GEMINI_CLI_SETTINGS}")
data = {}
if os.path.exists(p):
    try:
        with open(p, "r") as f:
            data = json.load(f)
    except Exception:
        data = {}
data["statusLine"] = {
    "command": os.path.expanduser("${BIN_DEST}/agy-quota-statusline"),
    "enabled": True,
    "stack_with_default": True
}
data["model"] = "Gemini 3.8 Flash (Low)"
with open(p, "w") as f:
    json.dump(data, f, indent=2)
EOF
        log_done "Configured statusLine and low-effort Flash model in Antigravity settings.json."
    fi
}

install_claude() {
    echo ""
    log_info "Configuring Claude Code..."

    # 1. Skills
    mkdir -p "${CLAUDE_SKILLS}"
    cp -r "${SCRIPT_DIR}/config/skills/"* "${CLAUDE_SKILLS}/"
    local count
    count="$(find "${CLAUDE_SKILLS}" -mindepth 1 -maxdepth 1 -type d ! -name "synced" | wc -l)"
    log_done "Synchronized ${count} skills in ${CLAUDE_SKILLS}."

    # 2. Rules
    mkdir -p "${CLAUDE_DIR}"
    cp "${SCRIPT_DIR}/config/GEMINI.md" "${CLAUDE_RULES}"
    log_done "Installed global rules in ${CLAUDE_RULES}."

    # 3. Settings / Statusline / Effort
    python3 - <<EOF
import json, os
p = os.path.expanduser("${CLAUDE_SETTINGS}")
data = {}
if os.path.exists(p):
    try:
        with open(p, "r") as f:
            data = json.load(f)
    except Exception:
        data = {}
data["statusLine"] = {
    "type": "command",
    "command": os.path.expanduser("${BIN_DEST}/claude-statusline")
}
data["effort"] = "low"
with open(p, "w") as f:
    json.dump(data, f, indent=2)
EOF
    log_done "Configured statusLine and low-effort thinking in Claude Code settings.json."
}

install_cursor() {
    echo ""
    log_info "Configuring Cursor IDE & Multi-Model Rules..."

    # 1. Generate and synchronize rules and unified .cursorrules
    if [ -f "${SCRIPT_DIR}/bin/cursor-rules-sync" ]; then
        python3 "${SCRIPT_DIR}/bin/cursor-rules-sync"
    fi
    local count=0
    [ -d "${CURSOR_RULES}" ] && count="$(find "${CURSOR_RULES}" -name "*.mdc" | wc -l)"
    log_done "Installed ${count} Cursor rules (.mdc) in ${CURSOR_RULES}."
    log_done "Configured global rules in ${CURSOR_GLOBAL_RULES}."

    # 2. Configure Cursor User settings
    mkdir -p "$(dirname "${CURSOR_SETTINGS}")"
    python3 - <<EOF
import json, os
p = os.path.expanduser("${CURSOR_SETTINGS}")
data = {}
if os.path.exists(p):
    try:
        with open(p, "r") as f:
            data = json.load(f)
    except Exception:
        data = {}
data["cursor.general.userRules"] = "Adhere strictly to ~/.cursorrules and .cursor/rules/*.mdc. Follow Output Token Economy (zero conversational fluff, high-density status, surgical edits). Never restate user prompts. Use installed CLI tools in ~/.local/bin (game-texture-editor, stalker-playtest-runner, game-test-watchdog, skills-audit-update)."
data["cursor.composer.agentFlag"] = True
data["cursor.composer.showAgent"] = True
data["cursor.chat.model"] = "grok-4.7"
data["cursor.general.preferredModels"] = [
    "grok-4.7",
    "grok-4.7-fast",
    "grok-4.5",
    "claude-3-7-sonnet",
    "claude-3-5-sonnet",
    "claude-3-5-haiku",
    "o3-mini",
    "o1",
    "gpt-4o",
    "gpt-4o-mini",
    "deepseek-r1",
    "deepseek-v3",
    "gemini-2.0-flash",
    "gemini-1.5-pro",
    "llama-3.3-70b",
    "qwen-2.5-coder-32b",
    "codestral-2501"
]
env_linux = data.get("terminal.integrated.env.linux", {})
env_linux["PATH"] = "\${env:HOME}/.local/bin:\${env:PATH}"
data["terminal.integrated.env.linux"] = env_linux
with open(p, "w") as f:
    json.dump(data, f, indent=2)
EOF
    log_done "Configured Grok 4.7, agent mode, user rules, and CLI path in Cursor settings.json."
}

verify_installation() {
    echo ""
    log_info "Running verification checks..."

    if "${BIN_DEST}/agy-quota-statusline" >/dev/null 2>&1; then
        local st
        st="$("${BIN_DEST}/agy-quota-statusline")"
        log_done "Statusline verification: ${st}"
    else
        log_warn "Statusline test executed with warning (normal if no active session yet)."
    fi

    local agy_count=0 claude_count=0 cursor_count=0
    [ -d "${GEMINI_SKILLS}" ] && agy_count="$(find "${GEMINI_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l)"
    [ -d "${CLAUDE_SKILLS}" ] && claude_count="$(find "${CLAUDE_SKILLS}" -mindepth 1 -maxdepth 1 -type d ! -name "synced" | wc -l)"
    [ -d "${CURSOR_RULES}" ] && cursor_count="$(find "${CURSOR_RULES}" -name "*.mdc" | wc -l)"

    echo ""
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "${COLOR_GREEN} CLI Power Setup Successfully Installed!             ${COLOR_RESET}"
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "Antigravity Skills:   ${COLOR_CYAN}${agy_count} active (${GEMINI_SKILLS})${COLOR_RESET}"
    echo -e "Claude Code Skills:   ${COLOR_CYAN}${claude_count} active (${CLAUDE_SKILLS})${COLOR_RESET}"
    echo -e "Cursor Rules:         ${COLOR_CYAN}${cursor_count} active (${CURSOR_RULES})${COLOR_RESET}"
    echo -e "Statusline monitors: ${COLOR_CYAN}agy-quota-statusline & claude-statusline${COLOR_RESET}"
    echo -e "Turbo Launchers:      ${COLOR_CYAN}agy-turbo & claude-turbo (Low Thinking Effort)${COLOR_RESET}"
    echo -e "Auditor & Updater:    ${COLOR_CYAN}skills-audit-update (--audit, --sync, --fix, --pull)${COLOR_RESET}"
    echo ""
}

show_menu() {
    echo -e "${COLOR_BOLD}CLI Power Setup Installer${COLOR_RESET}"
    echo "Select target environment:"
    echo "  1) Tri-Environment (Antigravity, Claude Code, & Cursor) [Recommended]"
    echo "  2) Antigravity only (~/.gemini)"
    echo "  3) Claude Code only (~/.claude)"
    echo "  4) Cursor only (~/.cursor, ~/.cursorrules)"
    echo "  5) Exit"
    echo ""
    read -rp "Enter choice [1-5] (default: 1): " choice
    choice="${choice:-1}"
    case "$choice" in
        1) TARGET="all" ;;
        2) TARGET="agy" ;;
        3) TARGET="claude" ;;
        4) TARGET="cursor" ;;
        5) echo "Exiting."; exit 0 ;;
        *) echo "Invalid option, defaulting to Tri-Environment."; TARGET="all" ;;
    esac
}

main() {
    local TARGET="all"
    
    # Parse CLI flags if passed
    if [ "$#" -gt 0 ]; then
        case "$1" in
            --all|-a)       TARGET="all" ;;
            --agy|-g)       TARGET="agy" ;;
            --claude|-c)    TARGET="claude" ;;
            --cursor|-u)    TARGET="cursor" ;;
            --help|-h)
                echo "Usage: ./install.sh [--all | --agy | --claude | --cursor]"
                exit 0
                ;;
            *)
                log_warn "Unknown option '$1', opening menu..."
                show_menu
                ;;
        esac
    elif [ -t 0 ]; then
        show_menu
    fi

    echo -e "${COLOR_CYAN}Installing CLI Power Setup (Target: ${TARGET})...${COLOR_RESET}"
    backup_existing
    install_binaries

    case "${TARGET}" in
        all)
            install_antigravity
            install_claude
            install_cursor
            ;;
        agy)
            install_antigravity
            ;;
        claude)
            install_claude
            ;;
        cursor)
            install_cursor
            ;;
    esac

    verify_installation
}

main "$@"
