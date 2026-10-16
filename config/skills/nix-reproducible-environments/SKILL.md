---
name: nix-reproducible-environments
description: Hermetic developer environments using Nix Flakes (flake.nix), declarative dependencies, reproducible devShells, and cross-platform isolation.
---

# Nix Reproducible Environments & Flakes

This skill standardizes hermetic, bit-for-bit reproducible developer environments using **Nix Flakes**. It eliminates "works on my machine" issues across Linux and macOS without the overhead of heavy Docker containers.

---

## ❄️ 1. Modern Hermetic Flake (`flake.nix`)

Define isolated, reproducible development shells (as used in projects like `omen-space`):

```nix
{
  description = "Hermetic Development Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            rustc
            cargo
            clippy
            rustfmt
            pkg-config
            openssl
            cmake
            ninja
          ];

          shellHook = ''
            echo "[❄️] Entering hermetic Nix development shell."
            export RUST_BACKTRACE=1
          '';
        };
      });
}
```

---

## ⚡ 2. Instant Shell Activation

Enter the isolated environment with zero system package pollution:

```bash
# Launch development shell
nix develop

# Or run a command inside the flake environment directly
nix develop --command cargo build --release
```

---

## 🔄 Interoperability & Handoffs

* **Pairing with [`omen-space`](file:///home/ericparsley/Documents/GitHub/omen-space/flake.nix):** Directly maintains and validates the project's native Flake configuration.
* **Handoff to `cachyos-arch-packaging`:** For translating flake builds into Arch/CachyOS PKGBUILDs.
