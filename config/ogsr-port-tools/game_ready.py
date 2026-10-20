#!/usr/bin/env python3
"""Is a Steam game fully downloaded? Use BEFORE reading/porting anything from a game folder.
  game_ready.py            table of every installed/partial game in all Steam libraries
  game_ready.py <appid|name fragment>   exit 0 only if that game is complete (StateFlags 4 = fully installed, nothing left to download/update, no leftover downloading dir)
A paused download shows as StateFlags != 4 or BytesDownloaded < BytesToDownload, or a non-empty steamapps/downloading/<appid>."""
import re, sys
from pathlib import Path
libs = {Path.home() / ".local/share/Steam"}
try:
    for m in re.finditer(r'"path"\s+"([^"]+)"', (Path.home() / ".local/share/Steam/steamapps/libraryfolders.vdf").read_text()): libs.add(Path(m.group(1)))
except Exception: pass
def games():
    for lib in sorted(libs):
        for mf in sorted((lib / "steamapps").glob("appmanifest_*.acf")):
            t = mf.read_text(errors="ignore"); g = lambda k: (re.search(r'"%s"\s+"([^"]*)"' % k, t) or [0, ""])[1]
            app = g("appid"); dl = lib / "steamapps/downloading" / app
            done, need = int(g("BytesDownloaded") or 0), int(g("BytesToDownload") or 0)
            ok = g("StateFlags") == "4" and not (dl.exists() and any(dl.iterdir()))
            why = "complete" if ok else f"NOT complete: StateFlags={g('StateFlags')} downloaded {done}/{need} bytes" + (", partial files in downloading/" if dl.exists() and any(dl.iterdir()) else "")
            yield app, g("name"), ok, why, lib
if __name__ == "__main__":
    q = " ".join(sys.argv[1:]).lower(); rc = 2
    for app, name, ok, why, lib in games():
        if q and q != app and q not in name.lower(): continue
        print(f"{app:>8}  {name[:44]:44} {why}  [{lib}]"); rc = 0 if ok and rc != 1 else 1
    if q and rc == 2: print("no such game in the Steam manifests: treat as NOT downloaded")
    sys.exit(rc if q else 0)
