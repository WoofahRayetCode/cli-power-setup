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
    log_done "Backup created successfully."
}

install_binaries() {
    log_info "Installing utility scripts into ${BIN_DEST}..."
    mkdir -p "${BIN_DEST}"
    cp "${SCRIPT_DIR}/bin/agy-quota-statusline" "${BIN_DEST}/agy-quota-statusline"
    chmod +x "${BIN_DEST}/agy-quota-statusline"
    log_done "Installed executable: ${BIN_DEST}/agy-quota-statusline"

    if [ -f "${SCRIPT_DIR}/bin/agy-turbo" ]; then
        cp "${SCRIPT_DIR}/bin/agy-turbo" "${BIN_DEST}/agy-turbo"
        chmod +x "${BIN_DEST}/agy-turbo"
        log_done "Installed executable: ${BIN_DEST}/agy-turbo"
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
with open(p, "w") as f:
    json.dump(data, f, indent=2)
EOF
        log_done "Configured statusLine in Antigravity settings.json."
    fi
}

install_claude() {
    echo ""
    log_info "Configuring Claude Code..."

    # 1. Skills
    mkdir -p "${CLAUDE_SKILLS}"
    cp -r "${SCRIPT_DIR}/config/skills/"* "${CLAUDE_SKILLS}/"
    local count
    count="$(find "${CLAUDE_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l)"
    log_done "Synchronized ${count} skills in ${CLAUDE_SKILLS}."

    # 2. Rules
    mkdir -p "${CLAUDE_DIR}"
    cp "${SCRIPT_DIR}/config/GEMINI.md" "${CLAUDE_RULES}"
    log_done "Installed global rules in ${CLAUDE_RULES}."

    # 3. Settings / Statusline
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
    "command": os.path.expanduser("${BIN_DEST}/agy-quota-statusline")
}
with open(p, "w") as f:
    json.dump(data, f, indent=2)
EOF
    log_done "Configured statusLine in Claude Code settings.json."
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

    local agy_count=0 claude_count=0
    [ -d "${GEMINI_SKILLS}" ] && agy_count="$(find "${GEMINI_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l)"
    [ -d "${CLAUDE_SKILLS}" ] && claude_count="$(find "${CLAUDE_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l)"

    echo ""
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "${COLOR_GREEN} CLI Power Setup Successfully Installed!             ${COLOR_RESET}"
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "Antigravity Skills:   ${COLOR_CYAN}${agy_count} active (${GEMINI_SKILLS})${COLOR_RESET}"
    echo -e "Claude Code Skills:   ${COLOR_CYAN}${claude_count} active (${CLAUDE_SKILLS})${COLOR_RESET}"
    echo -e "Statusline monitor:   ${COLOR_CYAN}${BIN_DEST}/agy-quota-statusline${COLOR_RESET}"
    echo -e "Turbo Launcher:       ${COLOR_CYAN}${BIN_DEST}/agy-turbo${COLOR_RESET}"
    echo ""
}

show_menu() {
    echo -e "${COLOR_BOLD}CLI Power Setup Installer${COLOR_RESET}"
    echo "Select target CLI environment:"
    echo "  1) Dual-CLI (Both Antigravity & Claude Code) [Recommended]"
    echo "  2) Antigravity only (~/.gemini)"
    echo "  3) Claude Code only (~/.claude)"
    echo "  4) Exit"
    echo ""
    read -rp "Enter choice [1-4] (default: 1): " choice
    choice="${choice:-1}"
    case "$choice" in
        1) TARGET="all" ;;
        2) TARGET="agy" ;;
        3) TARGET="claude" ;;
        4) echo "Exiting."; exit 0 ;;
        *) echo "Invalid option, defaulting to Dual-CLI."; TARGET="all" ;;
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
            --help|-h)
                echo "Usage: ./install.sh [--all | --agy | --claude]"
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
            ;;
        agy)
            install_antigravity
            ;;
        claude)
            install_claude
            ;;
    esac

    verify_installation
}

main "$@"
