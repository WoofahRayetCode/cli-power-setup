#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# CLI Power Setup Installer (cli-power-setup)
# Configuration for Google Antigravity (agy) and Cursor IDE
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DEST="${HOME}/.local/bin"

GEMINI_DIR="${HOME}/.gemini"
GEMINI_SKILLS="${GEMINI_DIR}/config/skills"
GEMINI_RULES="${GEMINI_DIR}/config/GEMINI.md"
GEMINI_CLI_SETTINGS="${GEMINI_DIR}/antigravity-cli/settings.json"

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

    local installed_count=0
    for bin_file in "${SCRIPT_DIR}/bin/"*; do
        if [ -f "${bin_file}" ]; then
            local bname
            bname="$(basename "${bin_file}")"
            if [ -L "${BIN_DEST}/${bname}" ] || [ -f "${BIN_DEST}/${bname}" ]; then
                rm -f "${BIN_DEST}/${bname}"
            fi
            cp "${bin_file}" "${BIN_DEST}/${bname}"
            chmod +x "${BIN_DEST}/${bname}"
            installed_count=$((installed_count + 1))
        fi
    done
    log_done "Installed ${installed_count} CLI utilities into ${BIN_DEST}."

    # Create convenient command aliases & symlinks
    ln -sf "${BIN_DEST}/agy-cheatsheet" "${BIN_DEST}/cs"
    if [ -f "${SCRIPT_DIR}/config/skills/laptop-performance-profile/scripts/laptop_performance_controller.py" ]; then
        ln -sf "${SCRIPT_DIR}/config/skills/laptop-performance-profile/scripts/laptop_performance_controller.py" "${BIN_DEST}/laptop-perf"
    fi

    # Initialize universal lifetime token ledger
    mkdir -p "${HOME}/.cli_power_setup"
    if [ ! -f "${HOME}/.cli_power_setup/token_ledger.json" ] && [ -f "${SCRIPT_DIR}/config/token_ledger.json" ]; then
        cp "${SCRIPT_DIR}/config/token_ledger.json" "${HOME}/.cli_power_setup/token_ledger.json"
        log_done "Initialized global token ledger: ${HOME}/.cli_power_setup/token_ledger.json"
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

    local agy_count=0 cursor_count=0
    [ -d "${GEMINI_SKILLS}" ] && agy_count="$(find "${GEMINI_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l)"
    [ -d "${CURSOR_RULES}" ] && cursor_count="$(find "${CURSOR_RULES}" -name "*.mdc" | wc -l)"

    local model_count=0
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        model_count="$(curl -s http://localhost:11434/api/tags | grep -o '"name":' | wc -l || echo 0)"
    fi

    echo ""
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "${COLOR_GREEN} CLI Power Setup Successfully Installed!             ${COLOR_RESET}"
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "Antigravity Skills:   ${COLOR_CYAN}${agy_count} active (${GEMINI_SKILLS})${COLOR_RESET}"
    echo -e "Cursor Rules:         ${COLOR_CYAN}${cursor_count} active (${CURSOR_RULES})${COLOR_RESET}"
    echo -e "Local Model Fleet:    ${COLOR_CYAN}${model_count} models registered in Ollama${COLOR_RESET}"
    echo -e "Statusline monitor:   ${COLOR_CYAN}agy-quota-statusline${COLOR_RESET}"
    echo -e "Launchers:            ${COLOR_CYAN}agy-yolo & agy-turbo${COLOR_RESET}"
    echo -e "Fleet Manager:        ${COLOR_CYAN}setup-local-model-fleet (--status, --all, --detect-system)${COLOR_RESET}"
    echo -e "Hardware Optimizer:   ${COLOR_CYAN}ultra-model-manager (detect, status, download-all, optimize-all)${COLOR_RESET}"
    echo -e "Auditor & Updater:    ${COLOR_CYAN}skills-audit-update (--audit, --sync, --fix, --pull)${COLOR_RESET}"
    echo ""
}

install_models() {
    echo ""
    log_info "Detecting host system hardware and synchronizing local model fleet..."

    # Ensure Ollama service is reachable
    if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        log_warn "Ollama service is not responding on http://localhost:11434."
        if command -v systemctl >/dev/null 2>&1; then
            log_info "Attempting to start Ollama service via systemctl..."
            sudo systemctl start ollama 2>/dev/null || systemctl --user start ollama 2>/dev/null || true
            sleep 2
        fi
    fi

    local fleet_runner="${BIN_DEST}/setup-local-model-fleet"
    if [ ! -f "${fleet_runner}" ]; then
        fleet_runner="${SCRIPT_DIR}/bin/setup-local-model-fleet"
    fi

    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        python3 "${fleet_runner}" --all
        log_done "Local model fleet synchronized and hardware-optimized!"
    else
        log_warn "Ollama is offline. Start the service ('ollama serve' or 'systemctl start ollama') and run 'setup-local-model-fleet --all' at any time."
    fi
}

show_menu() {
    echo -e "${COLOR_BOLD}CLI Power Setup Installer${COLOR_RESET}"
    echo "Select target installation option:"
    echo "  1) Full Setup (Antigravity & Cursor) [Recommended]"
    echo "  2) Full Setup + Local Model Fleet Download & Optimization (37 Models)"
    echo "  3) Antigravity only (~/.gemini)"
    echo "  4) Cursor only (~/.cursor, ~/.cursorrules)"
    echo "  5) Local Model Fleet Only (Hardware Detection, Download & Optimization)"
    echo "  6) Exit"
    echo ""
    read -rp "Enter choice [1-6] (default: 1): " choice
    choice="${choice:-1}"
    case "$choice" in
        1) TARGET="all"; SYNC_MODELS=0 ;;
        2) TARGET="all"; SYNC_MODELS=1 ;;
        3) TARGET="agy"; SYNC_MODELS=0 ;;
        4) TARGET="cursor"; SYNC_MODELS=0 ;;
        5) TARGET="models"; SYNC_MODELS=1 ;;
        6) echo "Exiting."; exit 0 ;;
        *) echo "Invalid option, defaulting to Full Setup."; TARGET="all"; SYNC_MODELS=0 ;;
    esac
}

main() {
    local TARGET="all"
    local SYNC_MODELS=0
    
    # Parse CLI flags if passed
    if [ "$#" -gt 0 ]; then
        while [ "$#" -gt 0 ]; do
            case "$1" in
                --all|-a)           TARGET="all" ;;
                --agy|-g)           TARGET="agy" ;;
                --cursor|-u)        TARGET="cursor" ;;
                --models|-m)        TARGET="models"; SYNC_MODELS=1 ;;
                --with-models)      TARGET="all"; SYNC_MODELS=1 ;;
                --help|-h)
                    echo "Usage: ./install.sh [--all | --agy | --cursor | --models | --with-models]"
                    exit 0
                    ;;
                *)
                    log_warn "Unknown option '$1', opening menu..."
                    show_menu
                    break
                    ;;
            esac
            shift
        done
    elif [ -t 0 ]; then
        show_menu
    fi

    echo -e "${COLOR_CYAN}Installing CLI Power Setup (Target: ${TARGET}, Models: ${SYNC_MODELS})...${COLOR_RESET}"
    
    case "${TARGET}" in
        all)
            backup_existing
            install_binaries
            install_antigravity
            install_cursor
            if [ "${SYNC_MODELS}" -eq 1 ]; then
                install_models
            fi
            ;;
        agy)
            backup_existing
            install_binaries
            install_antigravity
            ;;
        cursor)
            backup_existing
            install_binaries
            install_cursor
            ;;
        models)
            install_binaries
            install_models
            ;;
    esac

    verify_installation
}

main "$@"
