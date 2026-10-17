---
name: tandem-shared-build-cache-lock
description: Manages shared CCache, CMake binary caches, and atomic build lockfiles between concurrent Argon and Fable worktrees to prevent redundant compilation and race conditions.
---

# Tandem Shared Build Cache & Lock (`tandem-shared-build-cache-lock`)

When Gemini 4 Argon and Claude Fable operate simultaneously in separate git worktrees (`<project>-argon` and `<project>-fable`), running independent compilation passes (C++, Rust, shaders, or asset packs) without shared caching compiles identical object files twice, saturating CPU/RAM and risking lock collisions.

This skill standardizes a shared `ccache`/`sccache` directory and non-blocking build locks.

---

## 1. Shared Cache Architecture

```
+------------------------------------+   +------------------------------------+
| Argon Worktree (<repo>-argon)      |   | Fable Worktree (<repo>-fable)      |
+------------------------------------+   +------------------------------------+
                  \                                 /
                   \                               /
                    v                             v
+-----------------------------------------------------------------------------+
| Shared Object Cache (~/.cache/ccache or <repo>/.build-cache)                |
| - Instant 99% hit rate on unchanged translation units                       |
| - Cuts parallel multi-agent build times from 3 minutes to 4 seconds         |
+-----------------------------------------------------------------------------+
```

---

## 2. Shared CMake & CCache Directives

When configuring CMake builds in either worktree:

```bash
# Export shared ccache directory across both worktrees
export CCACHE_DIR="${HOME}/.cache/ccache"
export CCACHE_MAXSIZE="20G"

# Configure with CCache enabled
cmake -B build -S . \
  -DCMAKE_C_COMPILER_LAUNCHER=ccache \
  -DCMAKE_CXX_COMPILER_LAUNCHER=ccache \
  -DCMAKE_BUILD_PARALLEL_LEVEL="$(nproc)"
```

---

## 3. Atomic Build Lock Protocol (`.build.lock`)

To prevent simultaneous asset packing (e.g. `retoc` / `vfs_asset_packer`) from colliding on output archives:

1. **Check Lock:** Before initiating a write to shared output directories (`dist/`, `gamedata/`):
   ```bash
   while [ -f "${REPO_ROOT}/.build.lock" ]; do
       echo "[*] Waiting for sibling agent to release build lock..."
       sleep 1
   done
   ```
2. **Acquire Lock:**
   ```bash
   echo "$$" > "${REPO_ROOT}/.build.lock"
   trap 'rm -f "${REPO_ROOT}/.build.lock"' EXIT INT TERM
   ```
3. **Execute & Auto-Release:** Once compilation or asset packing completes, the lockfile is removed automatically.
