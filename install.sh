#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# CLI Power Setup Installer (cli-power-setup)
# Native Configuration for Google Antigravity (agy) & Local Model Fleet
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BIN_DEST="${HOME}/.local/bin"

GEMINI_DIR="${HOME}/.gemini"
GEMINI_CONFIG="${GEMINI_DIR}/config"
GEMINI_SKILLS="${GEMINI_CONFIG}/skills"
GEMINI_RULES="${GEMINI_CONFIG}/GEMINI.md"
GEMINI_CLI_SETTINGS="${GEMINI_DIR}/antigravity-cli/settings.json"

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
        mkdir -p "${backup_dir}/gemini"
        cp "${GEMINI_RULES}" "${backup_dir}/gemini/GEMINI.md"
    fi
    if [ -f "${GEMINI_CLI_SETTINGS}" ]; then
        mkdir -p "${backup_dir}/gemini"
        cp "${GEMINI_CLI_SETTINGS}" "${backup_dir}/gemini/settings.json"
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

    # Symlinks and Aliases
    ln -sf "${BIN_DEST}/agy-cheatsheet" "${BIN_DEST}/cs"
    if [ -f "${SCRIPT_DIR}/config/skills/linux-systems-engineering/scripts/laptop_performance_controller.py" ]; then
        ln -sf "${SCRIPT_DIR}/config/skills/linux-systems-engineering/scripts/laptop_performance_controller.py" "${BIN_DEST}/laptop-perf"
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
    log_done "Synchronized ${count} skills in ${GEMINI_SKILLS}."

    # 2. Global Rules
    mkdir -p "${GEMINI_CONFIG}"
    cp "${SCRIPT_DIR}/config/GEMINI.md" "${GEMINI_RULES}"
    log_done "Installed lean global rules in ${GEMINI_RULES}."

    # 3. Settings / Statusline / Trusted Workspaces
    mkdir -p "$(dirname "${GEMINI_CLI_SETTINGS}")"
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
trusted = data.setdefault("trustedWorkspaces", [])
for w in [os.path.expanduser("~"), os.path.expanduser("~/Documents/GitHub")]:
    if w not in trusted:
        trusted.append(w)

with open(p, "w") as f:
    json.dump(data, f, indent=2)
EOF
    log_done "Configured statusLine, quota telemetry, and trusted workspaces in Antigravity settings.json."

    # 4. Configure shell aliases (.bashrc and .zshrc)
    for shrc in "$HOME/.bashrc" "$HOME/.zshrc"; do
        if [ -f "$shrc" ]; then
            if ! grep -q "agy-yolo" "$shrc"; then
                echo "" >> "$shrc"
                echo "# Antigravity (agy) aliases" >> "$shrc"
                echo "alias yolo='$BIN_DEST/agy-yolo'" >> "$shrc"
                echo "alias agy-yolo='$BIN_DEST/agy-yolo'" >> "$shrc"
                echo "alias agy-turbo='$BIN_DEST/agy-turbo'" >> "$shrc"
                echo "alias agy-eco='$BIN_DEST/agy-eco'" >> "$shrc"
                echo "alias cs='$BIN_DEST/cs'" >> "$shrc"
            fi
        fi
    done
    log_done "Configured shell aliases (yolo, agy-yolo, agy-turbo, agy-eco, cs)."

    # 5. Desktop Shortcuts and Dolphin Service Menus
    if [ -d "${SCRIPT_DIR}/config/desktop" ]; then
        mkdir -p "$HOME/Desktop" "$HOME/.local/share/applications" "$HOME/.local/share/kio/servicemenus"
        cp -f "${SCRIPT_DIR}/config/desktop/agy-yolo.desktop" "$HOME/Desktop/" 2>/dev/null || true
        cp -f "${SCRIPT_DIR}/config/desktop/agy-turbo.desktop" "$HOME/Desktop/" 2>/dev/null || true
        chmod +x "$HOME/Desktop/agy-yolo.desktop" "$HOME/Desktop/agy-turbo.desktop" 2>/dev/null || true
        cp -f "${SCRIPT_DIR}/config/desktop/agy-yolo.desktop" "$HOME/.local/share/applications/" 2>/dev/null || true
        cp -f "${SCRIPT_DIR}/config/desktop/agy-turbo.desktop" "$HOME/.local/share/applications/" 2>/dev/null || true
        cp -f "${SCRIPT_DIR}/config/desktop/agy-yolo-servicemenu.desktop" "$HOME/.local/share/kio/servicemenus/" 2>/dev/null || true
        chmod +x "$HOME/.local/share/kio/servicemenus/agy-yolo-servicemenu.desktop" 2>/dev/null || true
        command -v kbuildsycoca6 >/dev/null 2>&1 && kbuildsycoca6 2>/dev/null || true
        command -v update-desktop-database >/dev/null 2>&1 && update-desktop-database "$HOME/.local/share/applications" 2>/dev/null || true
        log_done "Installed Antigravity desktop shortcuts and Dolphin context service menu."
    fi
}

install_models() {
    echo ""
    log_info "Detecting host system hardware and synchronizing local model fleet..."

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

verify_installation() {
    echo ""
    log_info "Running verification checks..."

    local agy_count=0
    [ -d "${GEMINI_SKILLS}" ] && agy_count="$(find "${GEMINI_SKILLS}" -mindepth 1 -maxdepth 1 -type d | wc -l)"

    local model_count=0
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        model_count="$(curl -s http://localhost:11434/api/tags | grep -o '"name":' | wc -l || echo 0)"
    fi

    echo ""
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "${COLOR_GREEN} CLI Power Setup Successfully Installed!             ${COLOR_RESET}"
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "Primary Platform:     ${COLOR_CYAN}Google Antigravity (agy)${COLOR_RESET}"
    echo -e "Antigravity Skills:   ${COLOR_CYAN}${agy_count} active (${GEMINI_SKILLS})${COLOR_RESET}"
    echo -e "Global Rules:         ${COLOR_CYAN}${GEMINI_RULES}${COLOR_RESET}"
    echo -e "Local Model Fleet:    ${COLOR_CYAN}${model_count} models registered in Ollama${COLOR_RESET}"
    echo -e "Statusline:           ${COLOR_CYAN}agy-quota-statusline${COLOR_RESET}"
    echo -e "Launchers:            ${COLOR_CYAN}yolo, agy-yolo, agy-turbo, agy-eco, cs${COLOR_RESET}"
    echo -e "Diagnostics:          ${COLOR_CYAN}agy-doctor${COLOR_RESET}"
    echo -e "Multi-Tool Export:    ${COLOR_CYAN}export-skills (--target cursor | agents | agy-workspace | windsurf | custom)${COLOR_RESET}"
    echo ""
}

show_menu() {
    echo -e "${COLOR_BOLD}CLI Power Setup Installer (Antigravity agy Edition)${COLOR_RESET}"
    echo "Select target installation option:"
    echo "  1) Full Setup (Antigravity agy + CLI Utilities) [Recommended]"
    echo "  2) Full Setup + Local Model Fleet Download & Optimization"
    echo "  3) Local Model Fleet Only (Hardware Detection & Download)"
    echo "  4) Exit"
    echo ""
    read -rp "Enter choice [1-4] (default: 1): " choice
    choice="${choice:-1}"
    case "$choice" in
        1) TARGET="all"; SYNC_MODELS=0 ;;
        2) TARGET="all"; SYNC_MODELS=1 ;;
        3) TARGET="models"; SYNC_MODELS=1 ;;
        4) echo "Exiting."; exit 0 ;;
        *) echo "Invalid option, defaulting to Full Setup."; TARGET="all"; SYNC_MODELS=0 ;;
    esac
}

main() {
    local TARGET="all"
    local SYNC_MODELS=0
    
    if [ "$#" -gt 0 ]; then
        while [ "$#" -gt 0 ]; do
            case "$1" in
                --all|-a)           TARGET="all" ;;
                --models|-m)        TARGET="models"; SYNC_MODELS=1 ;;
                --with-models)      TARGET="all"; SYNC_MODELS=1 ;;
                --help|-h)
                    echo "Usage: ./install.sh [--all | --models | --with-models]"
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

    echo -e "${COLOR_CYAN}Installing CLI Power Setup (Target: ${TARGET}, Sync Models: ${SYNC_MODELS})...${COLOR_RESET}"
    
    case "${TARGET}" in
        all)
            backup_existing
            install_binaries
            install_antigravity
            if [ "${SYNC_MODELS}" -eq 1 ]; then
                install_models
            fi
            ;;
        models)
            install_binaries
            install_models
            ;;
    esac

    verify_installation
}

main "$@"
