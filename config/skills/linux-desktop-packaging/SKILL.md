---
name: linux-desktop-packaging
description: Linux desktop integration and packaging standards, XDG Base Directory specs, FreeDesktop .desktop entries, AppStream metadata, Flatpak manifests, and AppImage bundling.
---

# Linux Desktop Packaging & FreeDesktop Standards

This skill guides the creation of distribution-agnostic Linux desktop applications, system integrations, and sandboxed packaging formats.

---

## 📦 Core Standards

1. **FreeDesktop Integration:** `.desktop` entry specifications, scalable icon themes, and MIME-type registrations.
2. **XDG Base Directory Compliance:** Strict separation of `$XDG_CONFIG_HOME`, `$XDG_DATA_HOME`, `$XDG_CACHE_HOME`, and `$XDG_STATE_HOME`.
3. **AppStream Metadata:** Validated `metainfo.xml` metadata for software centers (Flathub, GNOME Software, Discover).
4. **Flatpak Packaging:** Sandboxed `flatpak-builder` JSON/YAML manifests, runtime selections, and fine-grained portal permissions.
5. **AppImage Packaging:** Self-contained bundles using `appimagetool` and `linuxdeploy` with glibc backwards-compatibility.

---

## 🖥️ 1. FreeDesktop `.desktop` File Specification

Place desktop entries in `usr/share/applications/<app-id>.desktop`:

```ini
[Desktop Entry]
Version=1.5
Type=Application
Name=Omen Space
GenericName=System Hardware Controller
Comment=Hardware and fan control daemon for HP Omen laptops
Exec=omen-gui %u
Icon=omen-space
Terminal=false
Categories=System;Settings;HardwareSettings;
Keywords=omen;fan;hardware;cooling;acpi;
StartupNotify=true
StartupWMClass=omen-gui
```

---

## 🛡️ 2. Sandboxed Flatpak Manifest

Author clean, reproducible Flatpak manifests (`io.github.woofahrayet.OmenSpace.yml`):

```yaml
app-id: io.github.woofahrayet.OmenSpace
runtime: org.freedesktop.Platform
runtime-version: '24.08'
sdk: org.freedesktop.Sdk
command: omen-gui

finish-args:
  - --socket=wayland
  - --socket=fallback-x11
  - --share=ipc
  - --share=network
  - --filesystem=xdg-config/omen-space:create
  - --system-talk-name=org.freedesktop.systemd1

modules:
  - name: omen-space
    buildsystem: simple
    build-commands:
      - install -Dm755 omen-gui /app/bin/omen-gui
      - install -Dm644 data/omen-space.svg /app/share/icons/hicolor/scalable/apps/omen-space.svg
      - install -Dm644 data/io.github.woofahrayet.OmenSpace.desktop /app/share/applications/io.github.woofahrayet.OmenSpace.desktop
      - install -Dm644 data/io.github.woofahrayet.OmenSpace.metainfo.xml /app/share/metainfo/io.github.woofahrayet.OmenSpace.metainfo.xml
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `linux-systems-engineering`:** For system daemon integration, D-Bus interfaces, and Polkit policy configuration.
* **Handoff to `cachyos-arch-packaging`:** For native Arch/CachyOS PKGBUILD packaging.
* **Handoff to `avalonia-cross-platform-dev` / `tauri-multiplatform-dev`:** For the underlying UI binaries packaged into Flatpak/AppImage.\n