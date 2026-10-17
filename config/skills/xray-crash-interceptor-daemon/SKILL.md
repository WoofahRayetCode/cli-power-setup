---
name: xray-crash-interceptor-daemon
description: Background sweep daemon that intercepts and dismisses Wine/Proton crash modals (BugTrap, Notepad log windows) during unattended S.T.A.L.K.E.R./OGSR YOLO runs.
---

# X-Ray Crash Interceptor Daemon (`xray-crash-interceptor-daemon`)

During autonomous, unattended playtesting of S.T.A.L.K.E.R. / OGSR under Wine or Steam Proton, fatal engine crashes default to Windows modal dialogs:
- `xray_<user>.log - Notepad`
- `BugTrap: A crash has been detected`
- Windows Error Reporting modal (`winedbg`)

Because these are interactive graphical modals waiting for an `OK` or `Close` click, the underlying shell command (`tools/save_fps.sh`, `xrEngine.exe`) blocks and never exits. In YOLO mode, this causes the autonomous agent to hang indefinitely.

This skill provides an automated background sweep daemon to intercept, extract, and dismiss crash modals within milliseconds.

---

## 1. Automated Modal Interceptor Daemon

Run in the background before launching long playtests or overnight autonomous runs:

```bash
#!/usr/bin/env bash
# xray_crash_sweep.sh: Intercepts hanging crash dialogs
while true; do
    # Check for spawned Notepad crash log viewer
    if pgrep -f "notepad.exe" > /dev/null 2>&1; then
        echo "[!] Detected spawned crash viewer (notepad.exe). Extracting stack trace..."
        
        # Isolate newest crash log
        LATEST_LOG=$(ls -t "${HOME}/.wine/drive_c/users"/*/AppData/Local/OGSR/logs/xray_*.log 2>/dev/null | head -1)
        if [ -n "${LATEST_LOG}" ]; then
            grep -A 20 -i "fatal error" "${LATEST_LOG}" > /tmp/xray_fatal_extracted.log 2>/dev/null || true
        fi
        
        # Terminate notepad to unblock the test runner
        pkill -f "notepad.exe" 2>/dev/null || true
    fi
    
    # Check for BugTrap or winedbg modals
    if pgrep -f "winedbg" > /dev/null 2>&1; then
        echo "[!] Terminating winedbg modal..."
        pkill -9 -f "winedbg" 2>/dev/null || true
    fi
    
    sleep 2
done
```

---

## 2. Integration into Autonomous Playtest Runners

Before executing any Wine/Proton engine test command:
1. Ensure the background sweep is active or invoke `xray_crash_sweep.sh &`.
2. Wrap engine launches with a hard timeout:
   ```bash
   timeout 120s wine bin/xrEngine.exe -nowait -nosound || [ $? -eq 124 ]
   ```
3. If an error occurs, inspect `/tmp/xray_fatal_extracted.log` directly. Argon immediately begins root-cause diagnosis without hanging.
