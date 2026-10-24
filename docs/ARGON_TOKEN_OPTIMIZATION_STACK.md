# Gemini 4 Argon & Antigravity CLI (agy) Token Optimization Stack

This guide details the complete local and workspace token-saving architecture configured for Google Antigravity CLI (`agy`) and Gemini 4 Argon / Gemini 3.8 Flash, minimizing cloud token consumption and preventing quota depletion.

---

## 1. Architecture Overview

```
                      [ User Input / Shell Command ]
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │    Rust Token Killer (rtk)   │ <── Output Compression Hook
                     │  filters/summarizes CLI logs │
                     └──────────────┬───────────────┘
                                    │
                                    ▼
                     ┌──────────────────────────────┐
                     │ Antigravity CLI / Gemini API │
                     └───────┬──────────────┬───────┘
                             │              │
                AST / Symbols│              │ Semantic / Vector Search
                             ▼              ▼
                    ┌────────────────┐ ┌─────────────────────────┐
                    │ sigmap / AST   │ │   cce (Code Context)    │
                    │ slice-reader   │ │   jcodemunch-mcp        │
                    └────────────────┘ └────────────┬────────────┘
                                                    │
                                                    ▼
                                       ┌─────────────────────────┐
                                       │ Local SQLite-Vec + ONNX │
                                       │  (FastEmbed / Ollama)   │
                                       └─────────────────────────┘
```

---

## 2. Arch Linux CLI Dependencies

Ensure core system dependencies are installed:

```bash
sudo pacman -S --needed uv ripgrep fd tree-sitter-cli jq
```

### Rust Token Killer (`rtk`)
`rtk` is a high-performance CLI proxy that transparently compresses command and tool outputs before they enter the LLM context window.

```bash
# Check if rtk is installed; if not, install via AUR or Cargo:
yay -S --needed rtk-git
# or: cargo install --git https://github.com/rtk-ai/rtk --branch master rtk

# Initialize global transparent Gemini output-compression hook:
rtk init -g --gemini --auto-patch
```

Hook location: `~/.gemini/hooks/rtk-hook-gemini.sh` and instructions in `~/.gemini/GEMINI.md`.

---

## 3. Local Code Indexers & Quota Utilities

### Code Context Engine (`cce`)
Installs local ONNX vector embeddings (`BAAI/bge-small-en-v1.5`, 384-d) with tree-sitter AST and SQLite-Vec index:

```bash
uv tool install --force "code-context-engine[local]"
```

If Ollama is running on `localhost:11434`, pull `nomic-embed-text`:
```bash
ollama pull nomic-embed-text
```

### jCodeMunch MCP (`jcodemunch`)
AST-aware symbol extraction and semantic code munching without telemetry:

```bash
uv tool install "jcodemunch-mcp[semantic]"
jcodemunch-mcp init --client none --no-share-savings --yes
```

### Sigmap & Antigravity Usage
Fast structural signature mapping and quota monitoring:

```bash
npm install -g sigmap antigravity-usage
# Ensure ~/.local/bin has links if using custom npm prefix
```

---

## 4. Zero-Token Quota Guard Plugin

Install the Antigravity CLI usage check plugin:

```bash
agy plugin install https://github.com/tanaikech/antigravity-cli-check-usage-plugin
```

---

## 5. Global MCP Configuration (`~/.gemini/config/mcp_config.json`)

Configure Model Context Protocol servers in `~/.gemini/config/mcp_config.json`:

```json
{
  "mcpServers": {
    "cce": {
      "command": "cce",
      "args": ["serve"]
    },
    "jcodemunch": {
      "command": "uvx",
      "args": ["--from", "jcodemunch-mcp[semantic]", "jcodemunch-mcp"],
      "env": {
        "JCODEMUNCH_EMBED_MODEL": "all-MiniLM-L6-v2",
        "JCODEMUNCH_SHARE_SAVINGS": "0"
      }
    },
    "sigmap": {
      "command": "sigmap",
      "args": ["--mcp"]
    }
  }
}
```

---

## 6. Repository Indexing & Ignore Configuration

Within your target git repository (e.g. `zoneforge`):

1. Create `.geminiignore` to avoid indexing heavy build artifacts and caches:
```gitignore
node_modules/
target/
dist/
build/
.venv/
*.lock
```

2. Initialize CCE local vector and FTS index:
```bash
cce init
```
