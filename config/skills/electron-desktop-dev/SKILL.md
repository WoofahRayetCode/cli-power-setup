---
name: electron-desktop-dev
description: Electron desktop application engineering, IPC security, context isolation, preload scripts, multi-window lifecycles, and cross-platform packaging with electron-builder.
---

# Electron Desktop Application Engineering

This skill establishes production engineering and security standards for building desktop applications and custom web browsers using Electron and Node.js.

---

## 🔒 1. Electron Security Best Practices

Default Electron configurations can expose full Node.js system access to web content. All windows must enforce strict isolation boundaries:

### Secure Window Construction
```javascript
const mainWindow = new BrowserWindow({
  width: 1200,
  height: 800,
  webPreferences: {
    nodeIntegration: false,          // Never expose raw Node.js in renderer
    contextIsolation: true,          // Isolate preload scripts from page JS
    sandbox: true,                   // Enable Chromium process sandboxing
    enableRemoteModule: false,       // Prevent remote code execution
    preload: path.join(__dirname, 'preload.js')
  }
});
```

### Typed Context Bridge (`preload.js`)
Expose only strictly validated, minimal APIs to the frontend UI:
```javascript
const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  sendMessage: (channel, data) => {
    const validChannels = ['to-main', 'open-file'];
    if (validChannels.includes(channel)) {
      ipcRenderer.send(channel, data);
    }
  },
  onReceive: (channel, callback) => {
    const validChannels = ['from-main'];
    if (validChannels.includes(channel)) {
      ipcRenderer.on(channel, (event, ...args) => callback(...args));
    }
  }
});
```

---

## ⚡ 2. Memory & Performance Optimization

* **Background Window Throttling:** Enable background throttling for hidden windows to suspend rendering ticks and save CPU cycles.
* **Tray & Hide-to-Tray Lifecycle:** When closing the main window, intercept the `close` event to hide rather than terminate the process if the app lives in the system tray:
  ```javascript
  mainWindow.on('close', (event) => {
    if (!app.isQuitting) {
      event.preventDefault();
      mainWindow.hide();
    }
  });
  ```
* **Process Separation:** Heavy computations (file hashing, compression, image processing) belong in Node.js utility processes (`utilityProcess`) or web workers, never in the main UI thread.

---

## 📦 3. Packaging & Distribution (`electron-builder`)

* Configure clean multi-target builds in `package.json`:
  ```json
  "build": {
    "appId": "com.wlfryt.app",
    "linux": {
      "target": ["AppImage", "tar.gz"],
      "category": "Utility"
    },
    "win": {
      "target": ["nsis", "portable"]
    }
  }
  ```
* Verify builds with `npx electron-builder --linux` or `--dir` for fast unpacking checks.

## Cross-OS Windows 10/11 & Linux Runtime Bridge (`windows-linux-cross-os-runtime-bridge`)
- **Unified Windows & Linux Execution:** Pair with `windows-linux-cross-os-runtime-bridge` for portable CPU thread saturation (`os.cpu_count()` / `$env:NUMBER_OF_PROCESSORS` / `$(nproc)`), scratch staging (`Path(tempfile.gettempdir())` / `R:\` RAMDisk / `/dev/shm`), and dual-GPU routing (Windows `UserGpuPreferences` vs Linux `DRI_PRIME`).
- **Dynamic Cheat Sheet, Git Sync & Self-Evolution:** Consult `agy-cheatsheet` (`cs` / `dynamic-repo-model-cheatsheet`) for live per-repo model/effort selection, commit verified milestones via `repo-auto-sync <repo> --checkpoint --push` (`autonomous-git-repo-sync-governor`), and promote reusable cross-OS scripts via `skill-evolve` (`self-evolving-skill-synthesizer`).
