"""Ctrl+V in kitty: a screenshot/image on the clipboard goes to Antigravity as a real Ctrl+V key press;
plain text on the clipboard is pasted as text (bracketed paste), exactly like kitty's own paste_from_clipboard. Needs wl-clipboard (wl-paste)."""
import subprocess
from kittens.tui.handler import result_handler

def main(args):
    pass

def clip_types():
    try: return subprocess.run(["wl-paste", "-l"], capture_output=True, text=True, timeout=3).stdout.split()
    except Exception: return []

@result_handler(no_ui=True)
def handle_result(args, answer, target_window_id, boss):
    w = boss.window_id_map.get(target_window_id)
    if w is None: return
    types = clip_types()
    has_image = any(t.startswith("image/") for t in types)
    has_text = any(t.startswith("text/") or t in ("STRING", "UTF8_STRING", "TEXT") for t in types)
    if has_image and not has_text:
        try: flags = w.screen.current_key_encoding_flags()
        except Exception: flags = 0
        w.write_to_child(b"\x1b[118;5u" if flags & 1 else b"\x16")      # Ctrl+V as the app negotiated it (kitty keyboard protocol or legacy)
    else:
        try: txt = subprocess.run(["wl-paste", "-n"], capture_output=True, text=True, timeout=3).stdout
        except Exception: txt = ""
        if txt: w.paste_text(txt)
