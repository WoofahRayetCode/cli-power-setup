---
name: windows-app-engineering
description: Native Windows desktop UI engineering, WinUI 3, Windows App SDK, WPF (.NET 8/9), C#/WinRT component interop, Fluent Design, and MSIX packaging.
---

# Windows Desktop App Engineering (WinUI 3 & WPF)

This skill standardizes native Windows desktop UI engineering using the Windows App SDK (WASDK) / WinUI 3 and modern WPF on .NET 8/9.

---

## 🪟 Core Focus Areas

1. **Modern Windows UI Frameworks:** WinUI 3 / Windows App SDK for contemporary Windows 11 Fluent experiences, and WPF (.NET 8/9) for mature enterprise and hardware tooling.
2. **App Window Customization:** Custom title bars, Mica/Acrylic material backdrops, and system tray minimization.
3. **Single-Instance Application Lifecycle:** Named pipe / mutex based instance detection and window redirection.
4. **C#/WinRT Component Interop:** Exposing high-performance C# components to WinRT consumers.
5. **MSIX & Sparse Packaging:** Modern deployment with clean installation, auto-updates, and desktop bridge capabilities.

---

## 🎨 1. WinUI 3 Window Backdrop & Titlebar Customization

Implement modern Windows 11 Mica material and custom draggable titlebars:

```csharp
using Microsoft.UI.Xaml;
using Microsoft.UI.Windowing;
using WinRT.Interop;

public sealed partial class MainWindow : Window
{
    private AppWindow _appWindow;

    public MainWindow()
    {
        this.InitializeComponent();
        
        // Enable Mica Backdrop
        this.SystemBackdrop = new Microsoft.UI.Xaml.Media.MicaBackdrop();
        
        // Extend content into title bar
        ExtendsContentIntoTitleBar = true;
        SetTitleBar(CustomTitleBar); // CustomTitleBar is a XAML UIElement

        IntPtr hWnd = WindowNative.GetWindowHandle(this);
        WindowId wndId = Microsoft.UI.Win32Interop.GetWindowIdFromWindow(hWnd);
        _appWindow = AppWindow.GetFromWindowId(wndId);
    }
}
```

---

## 🔄 Interoperability & Handoffs

* **Handoff to `avalonia-cross-platform-dev`:** If the application requires cross-platform execution on Linux and macOS.
* **Handoff to `win32-systems-engineering`:** When interacting with raw HWNDs, Win32 message hooks, or Windows Services.
* **Handoff to `csharp-dotnet-engineering`:** For core .NET memory optimization, async pipelines, and dependency injection.\n