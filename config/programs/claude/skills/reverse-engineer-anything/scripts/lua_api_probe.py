#!/usr/bin/env python3
"""lua_api_probe: which Lua-exposed engine functions does an X-Ray engine binary really have? (luabind registers names as plain strings in the .exe)
  lua_api_probe.py EXE --scripts FILE_OR_DIR ... [--defs GAME_SCRIPT_DIR]   report every level.X / obj:method() / table.func name used by the scripts that is NOT a string in the exe
  lua_api_probe.py EXE --has name [name ...]         present / missing per name
  lua_api_probe.py EXE --dump [--grep REGEX]         every identifier-like string in the exe's registration area (rough API list)
  lua_api_probe.py EXE --diff OTHER_EXE              API names present in one exe and not the other (e.g. OGSR vs a Steam EE engine)
Names defined by the game's own scripts (_g.script helpers, mod functions) are filtered out when --scripts includes the game's script folder, so only real engine gaps remain.
Caveat: a string hit means the name is registered somewhere (class or method), not that this class has it; a miss is reliable."""
import argparse, re, sys
from pathlib import Path
IDENT = re.compile(rb"[A-Za-z_][A-Za-z0-9_]{2,}")
def names_in(exe): return {m.group().decode() for m in IDENT.finditer(Path(exe).read_bytes())}
def script_text(paths):
    out = {}
    for p in paths:
        p = Path(p)
        for f in ([p] if p.is_file() else sorted(p.rglob("*.script")) + sorted(p.rglob("*.lua"))): out[str(f)] = f.read_text(errors="ignore")
    return out
LUA_STD = set("insert remove format floor ceil sqrt random abs max min sin cos atan2 pairs ipairs tostring tonumber type pcall unpack sort concat match find gsub gmatch sub len lower upper rep time clock date setmetatable getmetatable print error assert select next rawget rawset tan acos asin atan exp log pow fmod huge pi".split())
def used(texts):
    u = {}
    for f, t in texts.items():
        t = re.sub(r"--.*", "", t)
        for m in re.finditer(r"\b(?:level|game|alife|db|device)\.([A-Za-z_]\w+)|[:\.]([A-Za-z_]\w{2,})\s*\(", t):
            n = m.group(1) or m.group(2)
            if n not in LUA_STD: u.setdefault(n, set()).add(Path(f).name)
    return u
def defined(texts):
    d = set()
    for t in texts.values():
        d |= set(re.findall(r"class\s*\(?\s*[\"']([A-Za-z_]\w*)", t)) | set(re.findall(r"^\s*(?:local\s+)?([A-Za-z_]\w*)\s*=", t, re.M)) | set(re.findall(r"function\s+(?:[A-Za-z_]\w*[.:])?([A-Za-z_]\w*)", t)) | set(re.findall(r"^\s*(?:local\s+)?([A-Za-z_]\w*)\s*=\s*function", t, re.M))
    return d
def main():
    a = argparse.ArgumentParser(); a.add_argument("exe"); a.add_argument("--scripts", nargs="*"); a.add_argument("--defs", nargs="*", help="the game's own script folder(s): names they define are not engine gaps"); a.add_argument("--has", nargs="*"); a.add_argument("--dump", action="store_true"); a.add_argument("--grep"); a.add_argument("--diff")
    a = a.parse_args(); have = names_in(a.exe)
    if a.has:
        for n in a.has: print(("present " if n in have else "MISSING ") + n)
    if a.diff:
        other = names_in(a.diff); rx = re.compile(a.grep) if a.grep else None
        for label, s in (("only in " + Path(a.exe).name, have - other), ("only in " + Path(a.diff).name, other - have)):
            xs = sorted(n for n in s if (rx.search(n) if rx else "_" in n and n.islower()))
            print(f"== {label}: {len(xs)}"); print(" ".join(xs[:400]))
    if a.dump:
        rx = re.compile(a.grep) if a.grep else None
        print("\n".join(sorted(n for n in have if (rx.search(n) if rx else "_" in n and n.islower()))))
    if a.scripts:
        texts = script_text(a.scripts); u = used(texts); d = defined(texts) | defined(script_text(a.defs or []))
        miss = sorted(n for n in u if n not in have and n not in d)
        print(f"{len(u)} names used by {len(texts)} script file(s); {len(miss)} not in the engine and not defined by the scripts:")
        for n in miss: print(f"  {n:32} used in {', '.join(sorted(u[n])[:3])}")
main()
