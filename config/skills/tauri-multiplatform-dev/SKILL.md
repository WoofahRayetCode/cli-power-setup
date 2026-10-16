---
name: tauri-multiplatform-dev
description: Lightweight cross-platform desktop and mobile engineering with Tauri 2.0, Rust backend, web frontend, secure IPC commands, low RAM usage, and native system integration.
---

# Tauri 2.0 Multiplatform Engineering

This skill establishes best practices for building secure, ultra-lightweight desktop and mobile applications using Tauri 2.0 (Rust core + Web frontend).

---

## ⚡ Why Tauri 2.0?

* **Ultra-Low Memory:** Consumes 15–30 MB RAM (vs. 150+ MB for Electron).
* **Native WebViews:** Leverages the OS web engine (WebKitGTK on Linux, WebView2 on Windows, WKWebView on macOS).
* **Cross-Platform Target Matrix:** Single codebase targets Linux, Windows, macOS, Android, and iOS.

---

## 🛡️ 1. Secure IPC Command Pattern

Implement typed, secure commands in Rust and invoke them cleanly from TypeScript:

### Rust Backend (`src-tauri/src/lib.rs`)
```rust
#[tauri::command]
async fn execute_device_action(device_id: String, action: String) -> Result<String, String> {
    if device_id.is_empty() {
        return Err("Device ID cannot be empty".to_string());
    }
    // Perform systems operation safely in Rust
    Ok(format!("Action '{}' executed on {}", action, device_id))
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .invoke_handler(tauri::generate_handler![execute_device_action])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### TypeScript Frontend
```typescript
import { invoke } from '@tauri-apps/api/core';

async function triggerAction(id: string) {
    try {
        const response = await invoke<string>('execute_device_action', {
            deviceId: id,
            action: 'reboot'
        });
        console.log(response);
    } catch (err) {
        console.error('IPC Command Failed:', err);
    }
}
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `rust-engineering`:** For Rust backend crate architecture, lifetimes, and performance tuning.
* **Handoff to `electron-desktop-dev`:** When evaluating migrations from Electron to Tauri or comparing resource profiles.
* **Handoff to `linux-desktop-packaging`:** When packaging Tauri Linux builds into Flatpaks or distribution packages.\n