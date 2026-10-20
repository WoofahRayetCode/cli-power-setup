#!/usr/bin/env python3
import sys
import argparse
from typing import Dict, List

# Discord Gateway Intents (API v10)
INTENTS: Dict[str, int] = {
    "GUILDS": 1 << 0,
    "GUILD_MEMBERS": 1 << 1,           # Privileged
    "GUILD_MODERATION": 1 << 2,
    "GUILD_EMOJIS_AND_STICKERS": 1 << 3,
    "GUILD_INTEGRATIONS": 1 << 4,
    "GUILD_WEBHOOKS": 1 << 5,
    "GUILD_INVITES": 1 << 6,
    "GUILD_VOICE_STATES": 1 << 7,
    "GUILD_PRESENCES": 1 << 8,          # Privileged
    "GUILD_MESSAGES": 1 << 9,
    "GUILD_MESSAGE_REACTIONS": 1 << 10,
    "GUILD_MESSAGE_TYPING": 1 << 11,
    "DIRECT_MESSAGES": 1 << 12,
    "DIRECT_MESSAGE_REACTIONS": 1 << 13,
    "DIRECT_MESSAGE_TYPING": 1 << 14,
    "MESSAGE_CONTENT": 1 << 15,         # Privileged
    "GUILD_SCHEDULED_EVENTS": 1 << 16,
    "AUTO_MODERATION_CONFIGURATION": 1 << 20,
    "AUTO_MODERATION_EXECUTION": 1 << 21,
}

# Discord Permissions (API v10)
PERMISSIONS: Dict[str, int] = {
    "CREATE_INSTANT_INVITE": 1 << 0,
    "KICK_MEMBERS": 1 << 1,
    "BAN_MEMBERS": 1 << 2,
    "ADMINISTRATOR": 1 << 3,
    "MANAGE_CHANNELS": 1 << 4,
    "MANAGE_GUILD": 1 << 5,
    "ADD_REACTIONS": 1 << 6,
    "VIEW_AUDIT_LOG": 1 << 7,
    "PRIORITY_SPEAKER": 1 << 8,
    "STREAM": 1 << 9,
    "VIEW_CHANNEL": 1 << 10,
    "SEND_MESSAGES": 1 << 11,
    "SEND_TTS_MESSAGES": 1 << 12,
    "MANAGE_MESSAGES": 1 << 13,
    "EMBED_LINKS": 1 << 14,
    "ATTACH_FILES": 1 << 15,
    "READ_MESSAGE_HISTORY": 1 << 16,
    "MENTION_EVERYONE": 1 << 17,
    "USE_EXTERNAL_EMOJIS": 1 << 18,
    "VIEW_GUILD_INSIGHTS": 1 << 19,
    "CONNECT": 1 << 20,
    "SPEAK": 1 << 21,
    "MUTE_MEMBERS": 1 << 22,
    "DEAFEN_MEMBERS": 1 << 23,
    "MOVE_MEMBERS": 1 << 24,
    "USE_VAD": 1 << 25,
    "CHANGE_NICKNAME": 1 << 26,
    "MANAGE_NICKNAMES": 1 << 27,
    "MANAGE_ROLES": 1 << 28,
    "MANAGE_WEBHOOKS": 1 << 29,
    "MANAGE_GUILD_EXPRESSIONS": 1 << 30,
    "USE_APPLICATION_COMMANDS": 1 << 31,
    "REQUEST_TO_SPEAK": 1 << 32,
    "MANAGE_EVENTS": 1 << 33,
    "MANAGE_THREADS": 1 << 34,
    "CREATE_PUBLIC_THREADS": 1 << 35,
    "CREATE_PRIVATE_THREADS": 1 << 36,
    "USE_EXTERNAL_STICKERS": 1 << 37,
    "SEND_MESSAGES_IN_THREADS": 1 << 38,
    "USE_EMBEDDED_ACTIVITIES": 1 << 39,
    "MODERATE_MEMBERS": 1 << 40,
}

def decode_bitmask(bitmask: int, mapping: Dict[str, int]) -> List[str]:
    enabled = []
    for name, value in mapping.items():
        if (bitmask & value) == value:
            enabled.append(name)
    return enabled

def calculate_bitmask(names: List[str], mapping: Dict[str, int]) -> int:
    mask = 0
    for name in names:
        key = name.upper().strip()
        if key in mapping:
            mask |= mapping[key]
        else:
            print(f"[!] Warning: Unknown flag '{name}'", file=sys.stderr)
    return mask

def main():
    parser = argparse.ArgumentParser(description="Discord API v10 Intent & Permission Bitmask Calculator")
    parser.add_argument("--decode-intents", type=int, help="Decode an integer Gateway Intents bitmask")
    parser.add_argument("--decode-perms", type=int, help="Decode an integer Permissions bitmask")
    parser.add_argument("--intents", nargs="+", help="Calculate bitmask from intent names (e.g. GUILDS GUILD_MESSAGES)")
    parser.add_argument("--perms", nargs="+", help="Calculate bitmask from permission names (e.g. SEND_MESSAGES EMBED_LINKS)")
    parser.add_argument("--invite", type=str, help="Generate bot invite link with client ID (combine with --perms or preset)")
    parser.add_argument("--preset", choices=["mod", "music", "standard"], help="Use a standard permission preset")

    args = parser.parse_args()

    if args.decode_intents is not None:
        enabled = decode_bitmask(args.decode_intents, INTENTS)
        print("=" * 60)
        print(f" 🤖 Decoded Gateway Intents: {args.decode_intents} (0x{args.decode_intents:X})")
        print("=" * 60)
        for name in enabled:
            priv = " [PRIVILEGED]" if name in ("GUILD_MEMBERS", "GUILD_PRESENCES", "MESSAGE_CONTENT") else ""
            print(f"  ✓ {name}{priv}")
        print("=" * 60)
        return

    if args.decode_perms is not None:
        enabled = decode_bitmask(args.decode_perms, PERMISSIONS)
        print("=" * 60)
        print(f" 🛡️  Decoded Permissions: {args.decode_perms} (0x{args.decode_perms:X})")
        print("=" * 60)
        for name in enabled:
            admin = " [HIGH RISK]" if name in ("ADMINISTRATOR", "MANAGE_GUILD", "MANAGE_ROLES") else ""
            print(f"  ✓ {name}{admin}")
        print("=" * 60)
        return

    perm_mask = 0
    if args.preset == "mod":
        perm_mask = calculate_bitmask(
            ["VIEW_CHANNEL", "SEND_MESSAGES", "EMBED_LINKS", "KICK_MEMBERS", "BAN_MEMBERS", "MODERATE_MEMBERS", "MANAGE_MESSAGES", "READ_MESSAGE_HISTORY", "USE_APPLICATION_COMMANDS"],
            PERMISSIONS
        )
    elif args.preset == "music":
        perm_mask = calculate_bitmask(
            ["VIEW_CHANNEL", "SEND_MESSAGES", "EMBED_LINKS", "CONNECT", "SPEAK", "USE_VAD", "READ_MESSAGE_HISTORY", "USE_APPLICATION_COMMANDS"],
            PERMISSIONS
        )
    elif args.preset == "standard":
        perm_mask = calculate_bitmask(
            ["VIEW_CHANNEL", "SEND_MESSAGES", "EMBED_LINKS", "ATTACH_FILES", "READ_MESSAGE_HISTORY", "ADD_REACTIONS", "USE_APPLICATION_COMMANDS"],
            PERMISSIONS
        )
    elif args.perms:
        perm_mask = calculate_bitmask(args.perms, PERMISSIONS)

    if args.intents:
        intent_mask = calculate_bitmask(args.intents, INTENTS)
        print(f"[✓] Calculated Gateway Intents Bitmask: {intent_mask} (0x{intent_mask:X})")

    if perm_mask > 0:
        print(f"[✓] Calculated Permissions Bitmask: {perm_mask} (0x{perm_mask:X})")

    if args.invite:
        client_id = args.invite.strip()
        url = f"https://discord.com/oauth2/authorize?client_id={client_id}&permissions={perm_mask}&scope=bot%20applications.commands"
        print("=" * 60)
        print(" 🔗 Discord Bot Authorization Invite URL:")
        print(f" {url}")
        print("=" * 60)

    if not any([args.decode_intents is not None, args.decode_perms is not None, args.intents, args.perms, args.invite, args.preset]):
        parser.print_help()

if __name__ == "__main__":
    main()
