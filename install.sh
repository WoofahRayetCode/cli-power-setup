#!/usr/bin/env bash
set -euo pipefail

# ==============================================================================
# Antigravity Power Setup Installer
# Sets up skills, global engineering/quota rules, and real-time CLI statusline
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GEMINI_DIR="${HOME}/.gemini"
SKILLS_DEST="${GEMINI_DIR}/config/skills"
RULES_DEST="${GEMINI_DIR}/config/GEMINI.md"
BIN_DEST="${HOME}/.local/bin"
CLI_SETTINGS="${GEMINI_DIR}/antigravity-cli/settings.json"

COLOR_GREEN="\033[0;32m"
COLOR_CYAN="\033[0;36m"
COLOR_YELLOW="\033[1;33m"
COLOR_RED="\033[0;31m"
COLOR_RESET="\033[0m"

log_info()  { echo -e "${COLOR_CYAN}[→]${COLOR_RESET} $1"; }
log_done()  { echo -e "${COLOR_GREEN}[✓]${COLOR_RESET} $1"; }
log_warn()  { echo -e "${COLOR_YELLOW}[!]${COLOR_RESET} $1"; }
log_err()   { echo -e "${COLOR_RED}[✗]${COLOR_RESET} $1"; }

backup_existing() {
    local timestamp
    timestamp="$(date +%Y%m%d_%H%M%S)"
    local backup_dir="${GEMINI_DIR}/backups/power_setup_${timestamp}"
    log_info "Creating backup in ${backup_dir}..."
    mkdir -p "${backup_dir}"
    
    if [ -d "${SKILLS_DEST}" ]; then
        cp -r "${SKILLS_DEST}" "${backup_dir}/skills"
    fi
    if [ -f "${RULES_DEST}" ]; then
        cp "${RULES_DEST}" "${backup_dir}/GEMINI.md"
    fi
    if [ -f "${CLI_SETTINGS}" ]; then
        cp "${CLI_SETTINGS}" "${backup_dir}/settings.json"
    fi
    log_done "Backup created."
}

install_skills() {
    log_info "Installing skills into ${SKILLS_DEST}..."
    mkdir -p "${SKILLS_DEST}"
    cp -r "${SCRIPT_DIR}/config/skills/"* "${SKILLS_DEST}/"
    local count
    count="$(find "${SKILLS_DEST}" -mindepth 1 -maxdepth 1 -type d | wc -l)"
    log_done "Installed ${count} skills."
}

install_rules() {
    log_info "Configuring global rules in ${RULES_DEST}..."
    mkdir -p "$(dirname "${RULES_DEST}")"
    if [ ! -f "${RULES_DEST}" ]; then
        cp "${SCRIPT_DIR}/config/GEMINI.md" "${RULES_DEST}"
        log_done "Installed global GEMINI.md rules."
    else
        # Append rules if not already present
        if ! grep -q "Output Token Economy" "${RULES_DEST}"; then
            echo "" >> "${RULES_DEST}"
            cat "${SCRIPT_DIR}/config/GEMINI.md" >> "${RULES_DEST}"
            log_done "Appended token economy and modding rules to existing GEMINI.md."
        else
            log_done "GEMINI.md rules already up to date."
        fi
    fi
}

install_statusline() {
    log_info "Installing statusline script to ${BIN_DEST}/agy-quota-statusline..."
    mkdir -p "${BIN_DEST}"
    cp "${SCRIPT_DIR}/bin/agy-quota-statusline" "${BIN_DEST}/agy-quota-statusline"
    chmod +x "${BIN_DEST}/agy-quota-statusline"
    log_done "Installed executable: ${BIN_DEST}/agy-quota-statusline"

    # Merge statusline config into settings.json safely
    log_info "Configuring ${CLI_SETTINGS}..."
    mkdir -p "$(dirname "${CLI_SETTINGS}")"
    python3 - <<EOF
import json, os

settings_path = os.path.expanduser("${CLI_SETTINGS}")
bin_path = os.path.expanduser("${BIN_DEST}/agy-quota-statusline")

data = {}
if os.path.exists(settings_path):
    try:
        with open(settings_path, "r") as f:
            data = json.load(f)
    except Exception:
        data = {}

data["statusLine"] = {
    "command": bin_path,
    "enabled": True,
    "stack_with_default": True
}

with open(settings_path, "w") as f:
    json.dump(data, f, indent=2)
EOF
    log_done "Configured statusLine in settings.json (stack_with_default: true)."
}

verify_installation() {
    echo ""
    log_info "Running verification checks..."
    
    # 1. Statusline execution test
    if "${BIN_DEST}/agy-quota-statusline" >/dev/null 2>&1; then
        log_done "Statusline test execution: PASS"
    else
        log_warn "Statusline returned non-zero (may need agy credentials or active session)"
    fi

    # 2. Skills count check
    local skill_count
    skill_count="$(find "${SKILLS_DEST}" -mindepth 1 -maxdepth 1 -type d | wc -l)"
    log_done "Total active skills detected: ${skill_count}"
    
    echo ""
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "${COLOR_GREEN} Antigravity Power Setup Successfully Installed!     ${COLOR_RESET}"
    echo -e "${COLOR_GREEN}======================================================${COLOR_RESET}"
    echo -e "Skills directory:     ${COLOR_CYAN}${SKILLS_DEST}${COLOR_RESET}"
    echo -e "Global rules:         ${COLOR_CYAN}${RULES_DEST}${COLOR_RESET}"
    echo -e "Statusline monitor:   ${COLOR_CYAN}${BIN_DEST}/agy-quota-statusline${COLOR_RESET}"
    echo -e "CLI settings:         ${COLOR_CYAN}${CLI_SETTINGS}${COLOR_RESET}"
    echo ""
}

# Main Execution Flow
main() {
    echo -e "${COLOR_CYAN}Installing Antigravity Power Setup...${COLOR_RESET}"
    backup_existing
    install_skills
    install_rules
    install_statusline
    verify_installation
}

main "$@"
