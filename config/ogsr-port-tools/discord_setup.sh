#!/usr/bin/env bash
# Stores the Discord bot token and your user id for tools/discord_bot.py (docs/DISCORD_BOT.md). Nothing is echoed.
d="$HOME/.config/stalker-discord"; mkdir -p "$d"; chmod 700 "$d"
read -r -s -p "Bot token (hidden): " tok; echo; read -r -p "Your Discord user id (numbers): " uid
[[ "$uid" =~ ^[0-9]+$ && -n "$tok" ]] || { echo "need a token and a numeric user id"; exit 1; }
printf '%s' "$tok" > "$d/token"; printf '%s' "$uid" > "$d/owner_id"; chmod 600 "$d/token" "$d/owner_id"; echo "saved; the guardian starts the bot within 30 s"
