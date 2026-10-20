#!/bin/bash
# Run at login: restore everything that was running before a reboot/crash, from the repo's own state.
cd "$(dirname "$0")/.." || exit 1
LOG=.agents/resume.log; echo "$(date '+%F %T') login resume" >> $LOG
systemctl --user start stalker-guardian.service 2>>$LOG     # guardian then restarts sysguard, statusweb, joplin watchdog, night walk
pgrep -f 'Joplin' >/dev/null || (nohup joplin-desktop >/dev/null 2>&1 & ) 
{ echo "== resumed $(date '+%F %T') after login; last checkpoint:"; cat .agents/checkpoints/auto_latest.txt 2>/dev/null; } >> .agents/memory/activeContext.md
