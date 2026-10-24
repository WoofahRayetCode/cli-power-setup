#!/usr/bin/env python3
"""
Game DLL Proxy Generator & Internal Hook Architect (dll_proxy_generator.py)
Automates generating proxy DLL source code (dinput8, dxgi, version, winmm),
export forwarding tables, MinHook detours, and Wine/Proton launch configs.
"""

import argparse
import os
import sys
from pathlib import Path

KNOWN_EXPORTS = {
    "dinput8": [
        ("HRESULT", "DirectInput8Create", "HINSTANCE hinst, DWORD dwVersion, REFIID riidltf, LPVOID *ppvOut, LPUNKNOWN punkOuter", "hinst, dwVersion, riidltf, ppvOut, punkOuter")
    ],
    "version": [
        ("BOOL", "GetFileVersionInfoA", "LPCSTR lptstrFilename, DWORD dwHandle, DWORD dwLen, LPVOID lpData", "lptstrFilename, dwHandle, dwLen, lpData"),
        ("BOOL", "GetFileVersionInfoW", "LPCWSTR lptstrFilename, DWORD dwHandle, DWORD dwLen, LPVOID lpData", "lptstrFilename, dwHandle, dwLen, lpData"),
        ("DWORD", "GetFileVersionInfoSizeA", "LPCSTR lptstrFilename, LPDWORD lpdwHandle", "lptstrFilename, lpdwHandle"),
        ("DWORD", "GetFileVersionInfoSizeW", "LPCWSTR lptstrFilename, LPDWORD lpdwHandle", "lptstrFilename, lpdwHandle"),
        ("BOOL", "VerQueryValueA", "LPCVOID pBlock, LPCSTR lpSubBlock, LPVOID *lplpBuffer, PUINT puLen", "pBlock, lpSubBlock, lplpBuffer, puLen"),
        ("BOOL", "VerQueryValueW", "LPCVOID pBlock, LPCWSTR lpSubBlock, LPVOID *lplpBuffer, PUINT puLen", "pBlock, lpSubBlock, lplpBuffer, puLen")
    ],
    "dxgi": [
        ("HRESULT", "CreateDXGIFactory", "REFIID riid, void **ppFactory", "riid, ppFactory"),
        ("HRESULT", "CreateDXGIFactory1", "REFIID riid, void **ppFactory", "riid, ppFactory"),
        ("HRESULT", "CreateDXGIFactory2", "UINT Flags, REFIID riid, void **ppFactory", "Flags, riid, ppFactory"),
        ("HRESULT", "DXGIDeclareAdapterRemovalSupport", "void", "")
    ],
    "winmm": [
        ("DWORD", "timeGetTime", "void", ""),
        ("MMRESULT", "timeBeginPeriod", "UINT uPeriod", "uPeriod"),
        ("MMRESULT", "timeEndPeriod", "UINT uPeriod", "uPeriod")
    ]
}


def generate_proxy_source(dll_name, with_minhook=False, with_imgui=False):
    target = dll_name.lower().replace(".dll", "")
    exports = KNOWN_EXPORTS.get(target, [("void", "UnknownExport", "void", "")])

    lines = [
        "// Auto-generated Game Proxy DLL by game-dll-proxy-generator",
        "// Target: " + dll_name,
        "#define WIN32_LEAN_AND_MEAN",
        "#include <windows.h>",
        "#include <stdio.h>",
        ""
    ]

    if with_minhook:
        lines.append("// #include \"MinHook.h\" // Uncomment when MinHook library is linked")

    lines.append("")
    lines.append(f"static HMODULE hOriginalDll = NULL;")
    lines.append("")

    # Generate function pointer types and stubs
    lines.append("// --- Original Function Pointers ---")
    for ret_type, fn_name, params, call_args in exports:
        lines.append(f"typedef {ret_type} (WINAPI *fn_{fn_name}_t)({params});")
        lines.append(f"static fn_{fn_name}_t o_{fn_name} = NULL;")
    lines.append("")

    # Exported forwarding wrappers
    lines.append("// --- Exported Proxy Functions ---")
    lines.append("extern \"C\" {")
    for ret_type, fn_name, params, call_args in exports:
        lines.append(f"__declspec(dllexport) {ret_type} WINAPI {fn_name}({params}) {{")
        lines.append(f"    if (!o_{fn_name}) {{")
        lines.append(f"        char sysPath[MAX_PATH];")
        lines.append(f"        GetSystemDirectoryA(sysPath, MAX_PATH);")
        lines.append(f"        strcat(sysPath, \"\\\\{dll_name}.dll\");")
        lines.append(f"        hOriginalDll = LoadLibraryA(sysPath);")
        lines.append(f"        if (hOriginalDll) {{")
        lines.append(f"            o_{fn_name} = (fn_{fn_name}_t)GetProcAddress(hOriginalDll, \"{fn_name}\");")
        lines.append(f"        }}")
        lines.append(f"    }}")
        if ret_type == "void":
            lines.append(f"    if (o_{fn_name}) o_{fn_name}({call_args});")
        else:
            lines.append(f"    if (o_{fn_name}) return o_{fn_name}({call_args});")
            lines.append(f"    return ({ret_type})0;")
        lines.append("}")
        lines.append("")
    lines.append("}")
    lines.append("")

    # Background thread and DllMain
    lines.append("// --- Trainer Logic Thread ---")
    lines.append("DWORD WINAPI TrainerMainThread(LPVOID lpParam) {")
    lines.append("    // Wait for game window and modules to initialize")
    lines.append("    Sleep(2000);")
    lines.append(f"    OutputDebugStringA(\"[{dll_name} Proxy] Trainer injected successfully!\\n\");")
    lines.append("")
    lines.append("    // Example: Put your memory patches, MinHook detours, or ImGui overlay setup here")
    lines.append("    while (true) {")
    lines.append("        // Example hotkey: NUMPAD1 for God Mode toggle")
    lines.append("        if (GetAsyncKeyState(VK_NUMPAD1) & 1) {")
    lines.append("            OutputDebugStringA(\"[{dll_name} Proxy] Hotkey triggered!\\n\");")
    lines.append("        }")
    lines.append("        Sleep(100);")
    lines.append("    }")
    lines.append("    return 0;")
    lines.append("}")
    lines.append("")
    lines.append("BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {")
    lines.append("    switch (ul_reason_for_call) {")
    lines.append("    case DLL_PROCESS_ATTACH:")
    lines.append("        DisableThreadLibraryCalls(hModule);")
    lines.append("        CreateThread(NULL, 0, TrainerMainThread, NULL, 0, NULL);")
    lines.append("        break;")
    lines.append("    case DLL_PROCESS_DETACH:")
    lines.append("        if (hOriginalDll) FreeLibrary(hOriginalDll);")
    lines.append("        break;")
    lines.append("    }")
    lines.append("    return TRUE;")
    lines.append("}")

    return "\n".join(lines)


def generate_cmakelists(dll_name):
    target = dll_name.lower().replace(".dll", "")
    return f"""cmake_minimum_required(VERSION 3.20)
project({target}_proxy CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library({target} SHARED dllmain.cpp)
set_target_properties({target} PROPERTIES PREFIX "" SUFFIX ".dll")
target_link_libraries({target} PRIVATE user32)
"""


def cmd_generate(args):
    target_dll = args.target.lower().replace(".dll", "")
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    src_content = generate_proxy_source(target_dll, with_minhook=args.with_minhook, with_imgui=args.with_imgui)
    (out_dir / "dllmain.cpp").write_text(src_content)

    cmake_content = generate_cmakelists(target_dll)
    (out_dir / "CMakeLists.txt").write_text(cmake_content)

    build_sh = f"""#!/usr/bin/env bash
# Cross-compile {target_dll}.dll using MinGW (Linux to Windows x64)
x86_64-w64-mingw32-g++ -shared -O2 -s -o {target_dll}.dll dllmain.cpp -luser32 -static-libgcc -static-libstdc++
echo "[✓] Built {target_dll}.dll successfully."
"""
    (out_dir / "build_mingw.sh").write_text(build_sh)
    os.chmod(out_dir / "build_mingw.sh", 0o755)

    print(f"[✓] Generated proxy DLL scaffold in: {out_dir}")
    print(f"  -> {out_dir / 'dllmain.cpp'} (Export table & trainer thread)")
    print(f"  -> {out_dir / 'CMakeLists.txt'} (CMake build config)")
    print(f"  -> {out_dir / 'build_mingw.sh'} (One-step cross-compiler script)")


def cmd_proton_config(args):
    dll = args.dll.lower().replace(".dll", "")
    print(f"--- Steam Proton Launch Configuration for {dll}.dll ---")
    print(f"\n1. Place {dll}.dll into the game's executable directory (next to .exe).")
    print(f"\n2. In Steam Game Properties -> Launch Options, set:")
    print(f"   WINEDLLOVERRIDES=\"{dll}=n,b\" %command%")
    print(f"\n(Wine will load your native '{dll}.dll' first, executing your trainer automatically on launch.)")


def main():
    parser = argparse.ArgumentParser(description="Game DLL Proxy Generator & Internal Hook Architect")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # generate
    p_gen = subparsers.add_parser("generate", help="Generate proxy DLL source and build configuration")
    p_gen.add_argument("--target", required=True, choices=["dinput8", "version", "dxgi", "winmm"], help="Target system DLL to proxy")
    p_gen.add_argument("--out-dir", default="proxy_dll", help="Output directory for generated source")
    p_gen.add_argument("--with-minhook", action="store_true", help="Include MinHook header stub")
    p_gen.add_argument("--with-imgui", action="store_true", help="Include ImGui overlay stub")

    # proton-config
    p_cfg = subparsers.add_parser("proton-config", help="Print Steam Proton DLL override configuration")
    p_cfg.add_argument("--dll", required=True, help="DLL name (e.g. dinput8)")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "proton-config":
        cmd_proton_config(args)


if __name__ == "__main__":
    main()
