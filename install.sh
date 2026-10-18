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

install_claude() {
    echo ""
    log_info "Configuring Claude Code..."

    # Ensure @anthropic-ai/claude-code is installed
    if ! command -v claude >/dev/null 2>&1; then
        log_info "Claude Code CLI not found in PATH. Installing via npm..."
        if command -v npm >/dev/null 2>&1; then
            npm install -g --prefix "${HOME}/.local" --allow-scripts=@anthropic-ai/claude-code @anthropic-ai/claude-code || true
        fi
    fi

    # 1. Skills
    mkdir -p "${CLAUDE_SKILLS}"
    cp -r "${SCRIPT_DIR}/config/skills/"* "${CLAUDE_SKILLS}/"
    local count
    count="$(find "${CLAUDE_SKILLS}" -mindepth 1 -maxdepth 1 -type d ! -name "synced" | wc -l)"
    log_done "Synchronized ${count} skills in ${CLAUDE_SKILLS}."

    # 2. Rules
    mkdir -p "${CLAUDE_DIR}"
    if [ -f "${SCRIPT_DIR}/config/CLAUDE.md" ]; then
        cp "${SCRIPT_DIR}/config/CLAUDE.md" "${CLAUDE_RULES}"
    else
        cp "${SCRIPT_DIR}/config/GEMINI.md" "${CLAUDE_RULES}"
    fi
    ln -sf "${CLAUDE_RULES}" "${HOME}/.claude.md"
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

    # Configure Claude Code aliases in bash
    if [ -f "$HOME/.bashrc" ] && ! grep -q "claude-eco" "$HOME/.bashrc"; then
        echo "" >> "$HOME/.bashrc"
        echo "# Claude Code aliases" >> "$HOME/.bashrc"
        echo "alias claude-eco='$BIN_DEST/claude-eco'" >> "$HOME/.bashrc"
        echo "alias claude-turbo='$BIN_DEST/claude-turbo'" >> "$HOME/.bashrc"
        echo "alias claude-yolo='$BIN_DEST/claude-yolo'" >> "$HOME/.bashrc"
        echo "alias claude-cheatsheet='$BIN_DEST/claude-cheatsheet'" >> "$HOME/.bashrc"
    fi

    # Install Desktop Shortcuts and Dolphin Service Menus
    if [ -d "${SCRIPT_DIR}/config/desktop" ]; then
        mkdir -p "$HOME/Desktop" "$HOME/.local/share/applications" "$HOME/.local/share/kio/servicemenus"
        cp -f "${SCRIPT_DIR}/config/desktop/Claude-Code.desktop" "$HOME/Desktop/" 2>/dev/null || true
        cp -f "${SCRIPT_DIR}/config/desktop/Claude-Eco.desktop" "$HOME/Desktop/" 2>/dev/null || true
        chmod +x "$HOME/Desktop/Claude-Code.desktop" "$HOME/Desktop/Claude-Eco.desktop" 2>/dev/null || true
        cp -f "${SCRIPT_DIR}/config/desktop/Claude-Code.desktop" "$HOME/.local/share/applications/" 2>/dev/null || true
        cp -f "${SCRIPT_DIR}/config/desktop/Claude-Eco.desktop" "$HOME/.local/share/applications/" 2>/dev/null || true
        cp -f "${SCRIPT_DIR}/config/desktop/claude-code-servicemenu.desktop" "$HOME/.local/share/kio/servicemenus/" 2>/dev/null || true
        command -v gio >/dev/null 2>&1 && gio set "$HOME/Desktop/Claude-Code.desktop" metadata::trusted true 2>/dev/null || true
        command -v gio >/dev/null 2>&1 && gio set "$HOME/Desktop/Claude-Eco.desktop" metadata::trusted true 2>/dev/null || true
        command -v kbuildsycoca6 >/dev/null 2>&1 && kbuildsycoca6 2>/dev/null || true
        log_done "Installed Claude Code desktop shortcuts and Dolphin context service menu."
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
    log_done "Configured Grok 4.7, Claude 3.7, agent mode, user rules, and CLI path in Cursor settings.json."
}

verify_installation() {
    echo ""
    log_info "Running verification checks..."

    if "${BIN_DEST}/agy-quota-statusline" >/dev/null 2>&1; then
        local st
        st="$("${BIN_DEST}/agy-quota-statusline")"
        log_done "Antigravity Statusline: ${st}"
    else
        log_warn "Antigravity Statusline test executed with warning (normal if no active session yet)."
    fi

    if [ -f "${BIN_DEST}/claude-statusline" ]; then
        log_done "Claude Code Statusline: ${BIN_DEST}/claude-statusline installed."
    fi

    local agy_count=0 claude_count=0 cursor_count=0
    [ -d "${GEMINI_SKILLS}" ] && agy_count="$(find "${GEMINI_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l)"
    [ -d "${CLAUDE_SKILLS}" ] && claude_count="$(find "${CLAUDE_SKILLS}" -mindepth 1 -maxdepth 1 -type d ! -name "synced" | wc -l)"
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
    echo -e "Claude Code Skills:   ${COLOR_CYAN}${claude_count} active (${CLAUDE_SKILLS})${COLOR_RESET}"
    echo -e "Cursor Rules:         ${COLOR_CYAN}${cursor_count} active (${CURSOR_RULES})${COLOR_RESET}"
    echo -e "Local Model Fleet:    ${COLOR_CYAN}${model_count} models registered in Ollama${COLOR_RESET}"
    echo -e "Statusline monitors:  ${COLOR_CYAN}agy-quota-statusline & claude-statusline${COLOR_RESET}"
    echo -e "Launchers:            ${COLOR_CYAN}agy-yolo, agy-turbo, claude-yolo, claude-turbo${COLOR_RESET}"
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
    echo "  1) Full Setup (Antigravity, Claude Code & Cursor) [Recommended]"
    echo "  2) Full Setup + Local Model Fleet Download & Optimization (42 Models)"
    echo "  3) Antigravity only (~/.gemini)"
    echo "  4) Claude Code only (~/.claude)"
    echo "  5) Cursor only (~/.cursor, ~/.cursorrules)"
    echo "  6) Local Model Fleet Only (Hardware Detection, Download & Optimization)"
    echo "  7) Exit"
    echo ""
    read -rp "Enter choice [1-7] (default: 1): " choice
    choice="${choice:-1}"
    case "$choice" in
        1) TARGET="all"; SYNC_MODELS=0 ;;
        2) TARGET="all"; SYNC_MODELS=1 ;;
        3) TARGET="agy"; SYNC_MODELS=0 ;;
        4) TARGET="claude"; SYNC_MODELS=0 ;;
        5) TARGET="cursor"; SYNC_MODELS=0 ;;
        6) TARGET="models"; SYNC_MODELS=1 ;;
        7) echo "Exiting."; exit 0 ;;
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
                --claude|-c)        TARGET="claude" ;;
                --cursor|-u)        TARGET="cursor" ;;
                --models|-m)        TARGET="models"; SYNC_MODELS=1 ;;
                --with-models)      TARGET="all"; SYNC_MODELS=1 ;;
                --help|-h)
                    echo "Usage: ./install.sh [--all | --agy | --claude | --cursor | --models | --with-models]"
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
            install_claude
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
        claude)
            backup_existing
            install_binaries
            install_claude
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
