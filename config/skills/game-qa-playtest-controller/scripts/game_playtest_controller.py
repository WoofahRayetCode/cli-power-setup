#!/usr/bin/env python3
"""
Game QA Playtest Automation & Locomotion Controller (game_playtest_controller.py)
Injects multi-axis character movement, circle-strafing, 360° panoramic camera sweeps,
obstacle wandering, and action stress sequences via Linux uinput / evdev.
"""

import argparse
import math
import os
import random
import sys
import time
from pathlib import Path

# Optional evdev support
HAVE_EVDEV = False
try:
    import evdev
    from evdev import UInput, ecodes
    HAVE_EVDEV = True
except ImportError:
    pass

class VirtualGamepad:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.uinput = None
        
        if not dry_run and HAVE_EVDEV:
            try:
                all_keys = [
                    getattr(ecodes, f"KEY_{c}") for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
                    if hasattr(ecodes, f"KEY_{c}")
                ]
                special_keys = [
                    ecodes.KEY_LEFTSHIFT, ecodes.KEY_SPACE, ecodes.KEY_LEFTCTRL,
                    ecodes.KEY_TAB, ecodes.KEY_ESC, ecodes.KEY_ENTER, ecodes.KEY_BACKSPACE,
                    ecodes.KEY_GRAVE, ecodes.KEY_MINUS, ecodes.KEY_EQUAL,
                    ecodes.KEY_F1, ecodes.KEY_F5, ecodes.KEY_F9, ecodes.KEY_F12,
                    ecodes.BTN_LEFT, ecodes.BTN_RIGHT, ecodes.BTN_MIDDLE
                ]
                cap = {
                    ecodes.EV_KEY: list(set(all_keys + special_keys)),
                    ecodes.EV_REL: [
                        ecodes.REL_X, ecodes.REL_Y, ecodes.REL_WHEEL
                    ]
                }
                self.uinput = UInput(cap, name="Virtual-QA-Playtest-Controller")
            except (PermissionError, OSError) as e:
                print(f"[!] Warning: Cannot access /dev/uinput ({e}). Falling back to simulation mode.", file=sys.stderr)
                self.dry_run = True

    def key(self, key_code, press=True):
        if self.dry_run:
            return
        if self.uinput and HAVE_EVDEV and key_code is not None:
            self.uinput.write(ecodes.EV_KEY, key_code, 1 if press else 0)
            self.uinput.syn()

    def type_text(self, text, delay=0.03):
        if self.dry_run:
            print(f"  [Sim Type]: '{text}'")
            return
        if not HAVE_EVDEV:
            return
        for ch in text:
            upper = ch.upper()
            if ch == "\n":
                kc = ecodes.KEY_ENTER
            elif ch == " ":
                kc = ecodes.KEY_SPACE
            elif ch in ("-", "_"):
                kc = ecodes.KEY_MINUS
            elif ch in ("`", "~"):
                kc = ecodes.KEY_GRAVE
            elif hasattr(ecodes, f"KEY_{upper}"):
                kc = getattr(ecodes, f"KEY_{upper}")
            else:
                continue
            self.key(kc, True)
            time.sleep(delay)
            self.key(kc, False)
            time.sleep(delay)

    def mouse_move(self, dx, dy):
        if self.dry_run:
            # print(f"[Sim] Mouse Move dx={dx}, dy={dy}")
            return
        if self.uinput and HAVE_EVDEV:
            self.uinput.write(ecodes.EV_REL, ecodes.REL_X, int(dx))
            self.uinput.write(ecodes.EV_REL, ecodes.REL_Y, int(dy))
            self.uinput.syn()

    def mouse_click(self, btn_code, duration=0.08):
        self.key(btn_code, True)
        time.sleep(duration)
        self.key(btn_code, False)

    def close(self):
        if self.uinput:
            self.uinput.close()

def cmd_orbit(args, pad: VirtualGamepad):
    direction = args.direction.lower()
    strafe_key = ecodes.KEY_D if direction == "right" else ecodes.KEY_A if HAVE_EVDEV else 32
    mouse_yaw = -args.mouse_speed if direction == "right" else args.mouse_speed
    
    print(f"\n[🎮 QA Orbit] Executing Circle-Strafe ({direction}) for {args.duration}s...")
    pad.key(strafe_key, True)
    
    start_time = time.time()
    tick_rate = 0.02
    try:
        while time.time() - start_time < args.duration:
            pad.mouse_move(mouse_yaw, 0)
            time.sleep(tick_rate)
    finally:
        pad.key(strafe_key, False)
        print("[✓] Orbit maneuver complete.")

def cmd_sweep(args, pad: VirtualGamepad):
    print(f"\n[📷 QA Sweep] Performing 360° Panoramic Camera Sweep for {args.duration}s...")
    yaw_step = args.speed
    pitch_amplitude = 12 if args.pitch else 0
    
    start_time = time.time()
    tick_rate = 0.02
    angle = 0.0
    try:
        while time.time() - start_time < args.duration:
            pitch_delta = int(math.sin(angle) * pitch_amplitude) if args.pitch else 0
            pad.mouse_move(yaw_step, pitch_delta)
            angle += 0.1
            time.sleep(tick_rate)
    finally:
        print("[✓] 360° Panoramic sweep complete.")

def cmd_wander(args, pad: VirtualGamepad):
    print(f"\n[🧭 QA Wander] Executing Autonomous Frontier Wandering for {args.duration}s...")
    start_time = time.time()
    
    key_w = ecodes.KEY_W if HAVE_EVDEV else 17
    key_a = ecodes.KEY_A if HAVE_EVDEV else 30
    key_d = ecodes.KEY_D if HAVE_EVDEV else 32
    key_shift = ecodes.KEY_LEFTSHIFT if HAVE_EVDEV else 42
    key_space = ecodes.KEY_SPACE if HAVE_EVDEV else 57
    key_s = ecodes.KEY_S if HAVE_EVDEV else 31

    pad.key(key_w, True)
    try:
        while time.time() - start_time < args.duration:
            # Action probability distribution
            r = random.random()
            if r < 0.25:
                # Steer left
                pad.key(key_a, True)
                pad.mouse_move(-15, 0)
                time.sleep(0.3)
                pad.key(key_a, False)
            elif r < 0.50:
                # Steer right
                pad.key(key_d, True)
                pad.mouse_move(15, 0)
                time.sleep(0.3)
                pad.key(key_d, False)
            elif r < 0.70:
                # Sprint burst
                pad.key(key_shift, True)
                time.sleep(0.5)
                pad.key(key_shift, False)
            elif r < 0.85:
                # Jump over terrain obstacle
                pad.key(key_space, True)
                time.sleep(0.1)
                pad.key(key_space, False)
            else:
                # Stuck-recovery / turn-around check
                pad.key(key_w, False)
                pad.key(key_s, True)
                time.sleep(0.3)
                pad.key(key_s, False)
                pad.mouse_move(80, 0)  # 180 snap
                time.sleep(0.2)
                pad.key(key_w, True)
            time.sleep(0.2)
    finally:
        pad.key(key_w, False)
        pad.key(key_a, False)
        pad.key(key_d, False)
        pad.key(key_shift, False)
        print("[✓] Frontier wandering exploration complete.")

def cmd_stress_locomotion(args, pad: VirtualGamepad):
    print(f"\n[⚡ QA Locomotion Stress] Executing rapid movement state transitions for {args.duration}s...")
    start_time = time.time()
    
    key_w = ecodes.KEY_W if HAVE_EVDEV else 17
    key_s = ecodes.KEY_S if HAVE_EVDEV else 31
    key_a = ecodes.KEY_A if HAVE_EVDEV else 30
    key_d = ecodes.KEY_D if HAVE_EVDEV else 32
    key_space = ecodes.KEY_SPACE if HAVE_EVDEV else 57
    key_ctrl = ecodes.KEY_LEFTCTRL if HAVE_EVDEV else 29
    
    try:
        while time.time() - start_time < args.duration:
            # Rapid direction flipping
            pad.key(key_w, True)
            time.sleep(0.15)
            pad.key(key_w, False)
            pad.key(key_s, True)
            time.sleep(0.15)
            pad.key(key_s, False)
            
            # Rapid strafe wiggle
            pad.key(key_a, True)
            pad.mouse_move(-20, 0)
            time.sleep(0.12)
            pad.key(key_a, False)
            pad.key(key_d, True)
            pad.mouse_move(20, 0)
            time.sleep(0.12)
            pad.key(key_d, False)
            
            # Crouch-jump sequence
            pad.key(key_space, True)
            pad.key(key_ctrl, True)
            time.sleep(0.2)
            pad.key(key_space, False)
            pad.key(key_ctrl, False)
            time.sleep(0.1)
    finally:
        print("[✓] Locomotion stress test complete.")

def cmd_action_cycle(args, pad: VirtualGamepad):
    print(f"\n[🎯 QA Action Cycle] Running {args.cycles} cycles of gameplay interactions...")
    key_1 = ecodes.KEY_1 if HAVE_EVDEV else 2
    key_2 = ecodes.KEY_2 if HAVE_EVDEV else 3
    key_r = ecodes.KEY_R if HAVE_EVDEV else 19
    key_f = ecodes.KEY_F if HAVE_EVDEV else 33
    key_tab = ecodes.KEY_TAB if HAVE_EVDEV else 15
    btn_l = ecodes.BTN_LEFT if HAVE_EVDEV else 272
    btn_r = ecodes.BTN_RIGHT if HAVE_EVDEV else 273
    
    for cycle in range(1, args.cycles + 1):
        print(f"  -> Cycle {cycle}/{args.cycles}: Weapon draw, aim, fire, reload, inventory toggle...")
        # 1. Switch to Primary
        pad.key(key_1, True)
        time.sleep(0.1)
        pad.key(key_1, False)
        time.sleep(0.4)
        
        # 2. Aim (RMB hold)
        pad.key(btn_r, True)
        time.sleep(0.3)
        # 3. Fire (LMB click 3-round burst)
        for _ in range(3):
            pad.mouse_click(btn_l, duration=0.06)
            time.sleep(0.1)
        pad.key(btn_r, False)
        time.sleep(0.2)
        
        # 4. Reload
        pad.key(key_r, True)
        time.sleep(0.1)
        pad.key(key_r, False)
        time.sleep(0.5)
        
        # 5. Interact / Use key
        pad.key(key_f, True)
        time.sleep(0.1)
        pad.key(key_f, False)
        time.sleep(0.2)
        
        # 6. Inventory toggle
        pad.key(key_tab, True)
        time.sleep(0.15)
        pad.key(key_tab, False)
        time.sleep(0.4)
        pad.key(key_tab, True)
        time.sleep(0.15)
        pad.key(key_tab, False)
        time.sleep(0.3)
        
    print("[✓] Gameplay action cycle stress test complete.")

def cmd_respawn_reload(args, pad):
    print("=======================================================================")
    print(" 🔄 Player Death Recovery & Save Reload Injection")
    print("=======================================================================")
    print(f"Recovery Key:     {args.key}")
    print(f"Post-Reload Wait: {args.wait_time}s | Dry Run: {pad.dry_run}")
    print("-----------------------------------------------------------------------\n")
    
    time.sleep(1.0)
    target_key = ecodes.KEY_SPACE if HAVE_EVDEV else None
    if args.key.upper() == "F9" and HAVE_EVDEV:
        target_key = ecodes.KEY_F9
    elif args.key.upper() == "ENTER" and HAVE_EVDEV:
        target_key = ecodes.KEY_ENTER
    elif args.key.upper() == "SPACE" and HAVE_EVDEV:
        target_key = ecodes.KEY_SPACE

    print(f"  -> Injecting death dismissal / reload key: {args.key}...")
    pad.key(target_key, True)
    time.sleep(0.2)
    pad.key(target_key, False)
    
    if args.key.upper() == "SPACE" and HAVE_EVDEV:
        time.sleep(0.5)
        print("  -> Secondary quickload trigger (F9)...")
        pad.key(ecodes.KEY_F9, True)
        time.sleep(0.2)
        pad.key(ecodes.KEY_F9, False)

    print(f"  -> Waiting {args.wait_time}s for game level re-hydration...")
    time.sleep(args.wait_time if not pad.dry_run else 0.5)
    print("[✓] Player death recovery sequence injected.")

def cmd_console_command(args, pad):
    print("=======================================================================")
    print(" ⌨️  In-Game Console Command Injection")
    print("=======================================================================")
    print(f"Command:          {args.cmd}")
    print(f"Console Key:      {args.console_key} | Dry Run: {pad.dry_run}")
    print("-----------------------------------------------------------------------\n")
    
    console_key = ecodes.KEY_GRAVE if HAVE_EVDEV else None
    if args.console_key.upper() == "TAB" and HAVE_EVDEV:
        console_key = ecodes.KEY_TAB

    print(f"  -> Opening game console ({args.console_key})...")
    pad.key(console_key, True)
    time.sleep(0.1)
    pad.key(console_key, False)
    time.sleep(0.3)
    
    print(f"  -> Typing console command: '{args.cmd}'...")
    pad.type_text(args.cmd + "\n", delay=0.02)
    time.sleep(0.2)
    
    print(f"  -> Closing game console...")
    pad.key(console_key, True)
    time.sleep(0.1)
    pad.key(console_key, False)
    time.sleep(0.2)
    print(f"[✓] Console command '{args.cmd}' dispatched successfully.")

def cmd_enable_cheats(args, pad):
    print("=======================================================================")
    print(" 🛡️  Testing Cheats Injection (God Mode & Infinite Ammo)")
    print("=======================================================================")
    print(f"God Mode:         {args.god_mode}")
    print(f"Infinite Ammo:    {args.infinite_ammo} | Dry Run: {pad.dry_run}")
    print("-----------------------------------------------------------------------\n")
    
    console_key = ecodes.KEY_GRAVE if HAVE_EVDEV else None
    pad.key(console_key, True)
    time.sleep(0.1)
    pad.key(console_key, False)
    time.sleep(0.3)
    
    if args.god_mode:
        print("  -> Injecting 'g_god on'...")
        pad.type_text("g_god on\n", delay=0.02)
        time.sleep(0.15)
        
    if args.infinite_ammo:
        print("  -> Injecting 'g_unlimitedammo on'...")
        pad.type_text("g_unlimitedammo on\n", delay=0.02)
        time.sleep(0.15)
        
    pad.key(console_key, True)
    time.sleep(0.1)
    pad.key(console_key, False)
    time.sleep(0.2)
    print("[✓] Testing cheats enabled.")

def main():
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument("--dry-run", action="store_true", help="Simulate input without accessing /dev/uinput")

    parser = argparse.ArgumentParser(parents=[common_parser], description="Game QA Playtest Locomotion & Action Controller")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # orbit
    p_orbit = subparsers.add_parser("orbit", parents=[common_parser], help="Execute circle-strafing orbit around target")
    p_orbit.add_argument("--duration", type=float, default=6.0, help="Duration in seconds")
    p_orbit.add_argument("--direction", choices=["left", "right"], default="right", help="Orbit direction")
    p_orbit.add_argument("--mouse-speed", type=int, default=12, help="Mouse yaw delta per tick")
    
    # sweep
    p_sweep = subparsers.add_parser("sweep", parents=[common_parser], help="Perform 360° panoramic camera sweep")
    p_sweep.add_argument("--duration", type=float, default=5.0, help="Duration in seconds")
    p_sweep.add_argument("--speed", type=int, default=15, help="Yaw speed per tick")
    p_sweep.add_argument("--pitch", action="store_true", help="Oscillate camera pitch vertically")
    
    # wander
    p_wander = subparsers.add_parser("wander", parents=[common_parser], help="Autonomous exploration with obstacle bounce")
    p_wander.add_argument("--duration", type=float, default=10.0, help="Duration in seconds")
    
    # stress-locomotion
    p_stress = subparsers.add_parser("stress-locomotion", parents=[common_parser], help="Rapid state switching (sprint/jump/crouch)")
    p_stress.add_argument("--duration", type=float, default=8.0, help="Duration in seconds")
    
    # action-cycle
    p_action = subparsers.add_parser("action-cycle", parents=[common_parser], help="Simulate weapon cycling, fire, reload & inventory")
    p_action.add_argument("--cycles", type=int, default=3, help="Number of action cycles")

    # respawn-reload
    p_respawn = subparsers.add_parser("respawn-reload", parents=[common_parser], help="Inject death recovery and save reload keys")
    p_respawn.add_argument("--key", type=str, default="SPACE", help="Dismissal key (SPACE, F9, ENTER)")
    p_respawn.add_argument("--wait-time", type=float, default=3.0, help="Wait time after reload")

    # console-command
    p_cc = subparsers.add_parser("console-command", parents=[common_parser], help="Open console, type command, and submit")
    p_cc.add_argument("--cmd", type=str, required=True, help="Console command string")
    p_cc.add_argument("--console-key", type=str, default="GRAVE", help="Console activation key (GRAVE, TAB)")

    # enable-cheats
    p_cheat = subparsers.add_parser("enable-cheats", parents=[common_parser], help="Inject god mode and unlimited ammo commands")
    p_cheat.add_argument("--god-mode", action="store_true", default=True, help="Enable god mode")
    p_cheat.add_argument("--infinite-ammo", action="store_true", default=True, help="Enable unlimited ammo")
    
    args = parser.parse_args()
    pad = VirtualGamepad(dry_run=args.dry_run)
    
    try:
        if args.command == "orbit":
            cmd_orbit(args, pad)
        elif args.command == "sweep":
            cmd_sweep(args, pad)
        elif args.command == "wander":
            cmd_wander(args, pad)
        elif args.command == "stress-locomotion":
            cmd_stress_locomotion(args, pad)
        elif args.command == "action-cycle":
            cmd_action_cycle(args, pad)
        elif args.command == "respawn-reload":
            cmd_respawn_reload(args, pad)
        elif args.command == "console-command":
            cmd_console_command(args, pad)
        elif args.command == "enable-cheats":
            cmd_enable_cheats(args, pad)
    finally:
        pad.close()

if __name__ == "__main__":
    main()
