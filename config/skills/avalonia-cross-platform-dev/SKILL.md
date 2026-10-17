---
name: avalonia-cross-platform-dev
description: Cross-platform XAML GUI development with Avalonia UI (.NET 8/9), MVVM pattern, CompiledBindings, Native AOT compilation, and native OS desktop integration.
---

# Avalonia UI Cross-Platform Development (.NET 8/9)

This skill standardizes cross-platform desktop UI engineering using Avalonia UI 11+ and modern .NET, targeting Windows, Linux, and macOS with shared UI and Native AOT compilation.

---

## 🎨 Core Principles

1. **Strict MVVM Pattern:** Implement ViewModels with `CommunityToolkit.Mvvm` (`[ObservableProperty]`, `[RelayCommand]`).
2. **Compiled Bindings:** Enforce `x:DataType` and compiled bindings to eliminate reflection overhead and catch binding errors at build time.
3. **Cross-Platform OS Integration:** Use Avalonia's `StorageProvider` for native file/folder pickers, system tray icons, and system notifications without platform-specific code.
4. **Native AOT & Trimming:** Build self-contained, Native Ahead-Of-Time (AOT) binaries for zero-dependency distribution and sub-second startup times.

---

## 🚀 1. Project Configuration & Native AOT

Configure `.csproj` for multiplatform compilation and Native AOT (as seen in [`PS-Multi-Tools`](file:///home/ericparsley/Documents/GitHub/PS-Multi-Tools/PSMultiTools/PSMultiTools.csproj)):

```xml
<Project Sdk="Microsoft.NET.Sdk">
  <PropertyGroup>
    <OutputType>WinExe</OutputType>
    <TargetFramework>net9.0</TargetFramework>
    <Nullable>enable</Nullable>
    <BuiltInComInteropSupport>true</BuiltInComInteropSupport>
    <ApplicationManifest>app.manifest</ApplicationManifest>
    <AvaloniaUseCompiledBindingsByDefault>true</AvaloniaUseCompiledBindingsByDefault>
    <RuntimeIdentifiers>win-x64;linux-x64;osx-x64</RuntimeIdentifiers>
  </PropertyGroup>

  <ItemGroup>
    <PackageReference Include="Avalonia" Version="11.2.0" />
    <PackageReference Include="Avalonia.Desktop" Version="11.2.0" />
    <PackageReference Include="Avalonia.Themes.Fluent" Version="11.2.0" />
    <PackageReference Include="CommunityToolkit.Mvvm" Version="8.3.2" />
  </ItemGroup>
</Project>
```

---

## 📁 2. Cross-Platform Native File Picker (`StorageProvider`)

Avoid legacy Windows `OpenFileDialog` or WinForms wrappers; use Avalonia's abstract storage provider:

```csharp
using Avalonia.Platform.Storage;

public async Task<string?> OpenBackupFolderAsync(TopLevel topLevel)
{
    var options = new FolderPickerOpenOptions
    {
        Title = "Select Game Backup Directory",
        AllowMultiple = false
    };
    
    var result = await topLevel.StorageProvider.OpenFolderPickerAsync(options);
    return result.Count > 0 ? result[0].Path.LocalPath : null;
}
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `csharp-dotnet-engineering`:** For backend domain logic, thread-safe collections, and serialization.
* **Handoff to `linux-desktop-packaging`:** For packaging Avalonia Linux binaries into Flatpaks or AppImages.
* **Handoff to `win32-systems-engineering`:** If Windows-specific features (Registry, direct P/Invoke) are conditionally required.

## Cross-OS Windows 10/11 & Linux Runtime Bridge (`windows-linux-cross-os-runtime-bridge`)
- **Unified Windows & Linux Execution:** Pair with `windows-linux-cross-os-runtime-bridge` for portable CPU thread saturation (`os.cpu_count()` / `$env:NUMBER_OF_PROCESSORS` / `$(nproc)`), scratch staging (`Path(tempfile.gettempdir())` / `R:\` RAMDisk / `/dev/shm`), and dual-GPU routing (Windows `UserGpuPreferences` vs Linux `DRI_PRIME`).
- **Dynamic Cheat Sheet, Git Sync & Self-Evolution:** Consult `agy-cheatsheet` (`cs` / `dynamic-repo-model-cheatsheet`) for live per-repo model/effort selection, commit verified milestones via `repo-auto-sync <repo> --checkpoint --push` (`autonomous-git-repo-sync-governor`), and promote reusable cross-OS scripts via `skill-evolve` (`self-evolving-skill-synthesizer`).
