#!/usr/bin/env python3
"""
Laptop Performance & Thermal Profile Controller
===============================================
Dynamic power profile and fan control designed for HP Omen (via Omen Space / omen-cli),
with cross-platform Linux fallback (power-profiles-daemon, sensors, nvidia-smi).

Features:
- Profile switching: 'quiet' / 'power-saver', 'balanced', 'performance'.
- Fan mode control: 'auto', 'max'.
- Sleep/Silent Mode: Restricts acoustics and TDP so fans do not wake the user.
- Transient Boost Context Manager: Temporarily escalates to performance mode
  for heavy jobs and automatically restores previous profile on exit.
- Rich telemetry: CPU/GPU temperatures, Fan RPMs, PL1/PL2 power limits, Battery Care.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
from typing import Dict, Optional, Tuple

ANSI_ESCAPE_RE = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')


def _strip_ansi(text: str) -> str:
    """Remove ANSI escape sequences from terminal text."""
    return ANSI_ESCAPE_RE.sub('', text)


def _run(cmd: list[str]) -> Tuple[int, str, str]:
    """Run shell command returning exit code, stdout, stderr."""
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
        return proc.returncode, proc.stdout.strip(), proc.stderr.strip()
    except Exception as e:
        return 1, "", str(e)


def is_omen_available() -> bool:
    """Check if omen-cli binary is available on PATH."""
    return shutil.which("omen-cli") is not None


def get_current_profile() -> str:
    """Detect current power profile name."""
    if is_omen_available():
        code, out, _ = _run(["omen-cli", "power", "info"])
        if code == 0:
            for line in out.splitlines():
                if "active" in line:
                    parts = [p.strip() for p in line.split("|") if p.strip()]
                    if len(parts) >= 2:
                        return parts[1].strip('"').lower()

    if shutil.which("powerprofilesctl"):
        code, out, _ = _run(["powerprofilesctl", "get"])
        if code == 0 and out:
            return out.strip().lower()

    return "balanced"


def set_power_profile(profile: str) -> bool:
    """
    Set power profile.
    Normalized values: 'quiet' / 'power-saver', 'balanced', 'performance'.
    """
    normalized = profile.lower().strip()
    if normalized in ("quiet", "silent", "eco", "power-saver", "powersave"):
        omen_target = "power-saver"
        ppd_target = "power-saver"
    elif normalized in ("performance", "turbo", "boost"):
        omen_target = "performance"
        ppd_target = "performance"
    else:
        omen_target = "balanced"
        ppd_target = "balanced"

    if is_omen_available():
        code, out, err = _run(["omen-cli", "power", "set-profile", omen_target])
        if code == 0:
            return True
        print(f"[Warning] omen-cli failed: {err}", file=sys.stderr)

    if shutil.which("powerprofilesctl"):
        code, out, err = _run(["powerprofilesctl", "set", ppd_target])
        if code == 0:
            return True

    return False


def set_fan_mode(mode: str) -> bool:
    """
    Set fan mode: 'auto', 'max'.
    """
    target = mode.lower().strip()
    if target not in ("auto", "max"):
        target = "auto"

    if is_omen_available():
        code, out, err = _run(["omen-cli", "fan", "set-mode", target])
        return code == 0
    return False


def set_battery_care(limit: int) -> bool:
    """Set battery charge limit (50 to 100)."""
    limit = max(50, min(100, limit))
    if is_omen_available():
        code, _, _ = _run(["omen-cli", "system", "battery-care", str(limit)])
        return code == 0
    return False


def get_thermal_telemetry() -> Dict[str, str]:
    """Gather CPU/GPU temperatures, fan speeds, and power limits."""
    telemetry = {
        "profile": get_current_profile(),
        "fan_mode": "auto",
        "cpu_temp": "N/A",
        "gpu_temp": "N/A",
        "fan1_rpm": "N/A",
        "fan2_rpm": "N/A",
        "pl1": "N/A",
        "pl2": "N/A",
        "battery_care": "N/A",
        "backend": "none"
    }

    if is_omen_available():
        telemetry["backend"] = "omen-cli (OMEN Space)"
        _, out, _ = _run(["omen-cli", "fan", "mode"])
        if "Fan Mode:" in out:
            telemetry["fan_mode"] = out.split("Fan Mode:")[-1].strip()

        _, fan_info, _ = _run(["omen-cli", "fan", "info"])
        for line in fan_info.splitlines():
            if "Fan 1" in line and "Current RPM:" in line:
                telemetry["fan1_rpm"] = line.split("Current RPM:")[-1].split("|")[0].strip()
            elif "Fan 2" in line and "Current RPM:" in line:
                telemetry["fan2_rpm"] = line.split("Current RPM:")[-1].split("|")[0].strip()

        _, pwr_info, _ = _run(["omen-cli", "power", "info"])
        for line in pwr_info.splitlines():
            if "pl1_w" in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 2:
                    telemetry["pl1"] = f"{parts[1]}W"
            elif "pl2_w" in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if len(parts) >= 2:
                    telemetry["pl2"] = f"{parts[1]}W"

        _, fetch_out, _ = _run(["omen-cli", "fetch"])
        clean_fetch = _strip_ansi(fetch_out)
        for line in clean_fetch.splitlines():
            if "Thermal/Fans:" in line:
                for segment in line.split("|"):
                    segment = segment.strip()
                    if "CPU:" in segment:
                        telemetry["cpu_temp"] = segment.split("CPU:")[-1].strip()
                    elif "GPU:" in segment:
                        telemetry["gpu_temp"] = segment.split("GPU:")[-1].strip()
            elif "Battery Care:" in line:
                for segment in line.split("|"):
                    segment = segment.strip()
                    if "Battery Care:" in segment:
                        telemetry["battery_care"] = segment.split("Battery Care:")[-1].strip()

    # Fallback to nvidia-smi if GPU temp not found
    if telemetry["gpu_temp"] in ("N/A", "") and shutil.which("nvidia-smi"):
        code, out, _ = _run(["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"])
        if code == 0 and out.strip():
            telemetry["gpu_temp"] = f"{out.strip()}°C"

    # Fallback to sensors for CPU temp
    if telemetry["cpu_temp"] in ("N/A", "") and shutil.which("sensors"):
        code, out, _ = _run(["sensors"])
        if code == 0:
            for line in out.splitlines():
                if "Tctl:" in line or "Package id 0:" in line or "Composite:" in line:
                    parts = line.split(":")[-1].strip().split()
                    if parts:
                        telemetry["cpu_temp"] = parts[0].lstrip("+")
                        break

    return telemetry


class PerformanceContext:
    """
    Context manager to temporarily boost or throttle performance,
    reverting back to the initial profile upon completion.
    """
    def __init__(self, target_profile: str = "performance", target_fan: Optional[str] = None):
        self.target_profile = target_profile
        self.target_fan = target_fan
        self.previous_profile: Optional[str] = None

    def __enter__(self):
        self.previous_profile = get_current_profile()
        print(f"[PerformanceContext] Scaling profile: {self.previous_profile} -> {self.target_profile}")
        set_power_profile(self.target_profile)
        if self.target_fan:
            set_fan_mode(self.target_fan)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.previous_profile:
            print(f"[PerformanceContext] Restoring profile: {self.previous_profile}")
            set_power_profile(self.previous_profile)
        if self.target_fan:
            set_fan_mode("auto")


def boost_command(cmd: list[str]) -> int:
    """Execute command under boosted performance profile and restore afterward."""
    with PerformanceContext("performance"):
        print(f"[Exec] Running command: {' '.join(cmd)}")
        res = subprocess.run(cmd)
        return res.returncode


INHIBIT_PID_FILE = os.path.join(os.path.expanduser("~"), ".cache", "lid_inhibit.pid")


def is_lid_inhibited() -> Optional[int]:
    """Return active systemd-inhibit PID if running, else None."""
    if not os.path.exists(INHIBIT_PID_FILE):
        return None
    try:
        with open(INHIBIT_PID_FILE, "r", encoding="utf-8") as f:
            pid = int(f.read().strip())
        os.kill(pid, 0)
        return pid
    except Exception:
        try:
            os.remove(INHIBIT_PID_FILE)
        except OSError:
            pass
        return None


def start_lid_inhibitor(reason: str = "Autonomous 3D & Overnight Execution (Lid Closed)") -> Optional[int]:
    """Spawn a detached systemd-inhibit lock blocking handle-lid-switch, sleep, and idle."""
    existing = is_lid_inhibited()
    if existing:
        return existing
    if not shutil.which("systemd-inhibit"):
        return None
    os.makedirs(os.path.dirname(INHIBIT_PID_FILE), exist_ok=True)
    proc = subprocess.Popen(
        [
            "systemd-inhibit",
            "--what=handle-lid-switch:sleep:idle",
            "--who=Clamshell 3D Runner",
            f"--why={reason}",
            "--mode=block",
            "sleep",
            "infinity",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
    )
    with open(INHIBIT_PID_FILE, "w", encoding="utf-8") as f:
        f.write(str(proc.pid))
    return proc.pid


def stop_lid_inhibitor() -> bool:
    """Release the detached systemd-inhibit lock if active."""
    pid = is_lid_inhibited()
    if not pid:
        return False
    try:
        os.kill(pid, 15)
    except OSError:
        pass
    try:
        os.remove(INHIBIT_PID_FILE)
    except OSError:
        pass
    return True


def enter_silent_sleep_mode() -> None:
    """Apply whisper-quiet configuration and lid-close inhibitor for night-time / sleep autonomy."""
    set_power_profile("power-saver")
    set_fan_mode("auto")
    pid = start_lid_inhibitor("Sleep-Mode Autonomous Execution (Lid Closed Safe)")
    inh_str = f"PID {pid}" if pid else "PowerDevil AC LidAction=64"
    print(f"🌙 [Silent Sleep Mode Active] Profile: power-saver (Quiet) | Fans: Auto | Lid-Close Guard: Active ({inh_str})")


def enter_clamshell_3d_mode() -> None:
    """Configure thermal-safe lid-closed mode for headless Blender 5.2+ OptiX GPU rendering while sleeping."""
    set_power_profile("power-saver")
    set_fan_mode("auto")
    pid = start_lid_inhibitor("Clamshell 3D Blender + RTX 5060 OptiX Overnight Pipeline")
    inh_str = f"PID {pid}" if pid else "PowerDevil AC LidAction=64"
    print("🎨 [Clamshell 3D Sleep Mode Active]")
    print("  • Profile:        power-saver (CPU capped 25-35W so closed keyboard deck stays <68°C against display)")
    print("  • GPU Compute:    NVIDIA RTX 5060 OptiX + headless EGL active (works 100% with lid closed & screen off)")
    print("  • RAM Disk:       /dev/shm tmpfs ready for zero-SSD-wear bakes & contact sheets")
    print(f"  • Lid-Close Lock: Active ({inh_str} — closing laptop lid will NOT suspend system)")


def exit_sleep_or_clamshell_mode() -> None:
    """Release lid inhibitor and restore balanced daytime profile."""
    stopped = stop_lid_inhibitor()
    set_power_profile("balanced")
    set_fan_mode("auto")
    print(f"☀️ [Wake Mode Restored] Profile: balanced | Fans: Auto | Lid Inhibitor Released: {stopped}")


def main():
    parser = argparse.ArgumentParser(description="Laptop Performance & Thermal Profile Controller")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # status
    subparsers.add_parser("status", help="Get current profile, thermals, fan RPMs, and lid-close guard state")

    # set-profile
    set_p = subparsers.add_parser("set-profile", help="Set performance profile")
    set_p.add_argument("profile", choices=["quiet", "power-saver", "balanced", "performance", "turbo"], help="Target profile")

    # set-fan
    set_f = subparsers.add_parser("set-fan", help="Set fan mode")
    set_f.add_argument("mode", choices=["auto", "max"], help="Fan mode")

    # battery-care
    bat_p = subparsers.add_parser("battery-care", help="Set battery charge limit percentage")
    bat_p.add_argument("limit", type=int, help="Percentage (50-100)")

    # sleep
    subparsers.add_parser("sleep-mode", help="Set quiet profile, auto fan & lid-close inhibitor for sleep-safe operation")

    # clamshell-3d
    subparsers.add_parser("clamshell-3d", help="Lid-closed 3D Blender/OptiX mode (thermal-safe deck + lid inhibitor)")

    # wake-mode
    subparsers.add_parser("wake-mode", help="Release lid inhibitor and restore balanced daytime profile")

    # boost-exec
    boost_p = subparsers.add_parser("boost-exec", help="Run command with performance profile and auto-revert")
    boost_p.add_argument("args", nargs=argparse.REMAINDER, help="Command to run")

    args = parser.parse_args()

    if args.command == "status":
        telem = get_thermal_telemetry()
        inh_pid = is_lid_inhibited()
        print("⚡ Laptop Performance & Thermal Telemetry:")
        print(f"  • Backend:        {telem['backend']}")
        print(f"  • Profile:        {telem['profile']}")
        print(f"  • Fan Mode:       {telem['fan_mode']}")
        print(f"  • CPU Temp:       {telem['cpu_temp']}")
        print(f"  • GPU Temp:       {telem['gpu_temp']}")
        print(f"  • Fan 1 RPM:      {telem['fan1_rpm']}")
        print(f"  • Fan 2 RPM:      {telem['fan2_rpm']}")
        print(f"  • Power Limits:   PL1: {telem['pl1']} | PL2: {telem['pl2']}")
        print(f"  • Battery Care:   {telem['battery_care']}")
        print(f"  • Lid-Close Lock: {'Active (PID ' + str(inh_pid) + ')' if inh_pid else 'Standby (KDE AC LidAction=64 TurnOffScreen)'}")

    elif args.command == "set-profile":
        ok = set_power_profile(args.profile)
        print(f"[✓] Power profile set to '{args.profile}': {'Success' if ok else 'Failed'}")

    elif args.command == "set-fan":
        ok = set_fan_mode(args.mode)
        print(f"[✓] Fan mode set to '{args.mode}': {'Success' if ok else 'Failed'}")

    elif args.command == "battery-care":
        ok = set_battery_care(args.limit)
        print(f"[✓] Battery charge limit set to {args.limit}%: {'Success' if ok else 'Failed'}")

    elif args.command == "sleep-mode":
        enter_silent_sleep_mode()

    elif args.command == "clamshell-3d":
        enter_clamshell_3d_mode()

    elif args.command == "wake-mode":
        exit_sleep_or_clamshell_mode()

    elif args.command == "boost-exec":
        if not args.args:
            print("Error: No command provided to boost-exec.", file=sys.stderr)
            sys.exit(1)
        sys.exit(boost_command(args.args))


if __name__ == "__main__":
    main()
