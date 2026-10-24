#!/usr/bin/env python3
import sys
import hmac
import hashlib
import secrets
import argparse
from pathlib import Path

def generate_key(length_bytes: int = 32, fmt: str = "hex") -> str:
    key_bytes = secrets.token_bytes(length_bytes)
    if fmt == "hex":
        return key_bytes.hex()
    elif fmt == "base64":
        import base64
        return base64.b64encode(key_bytes).decode("ascii")
    return key_bytes.hex()

def compute_hmac(file_path: Path, key: bytes) -> str:
    data = file_path.read_bytes()
    tag = hmac.new(key, data, hashlib.sha256).hexdigest()
    return tag

def verify_hmac(file_path: Path, key: bytes, expected_tag: str) -> bool:
    actual_tag = compute_hmac(file_path, key)
    return hmac.compare_digest(actual_tag, expected_tag.strip().lower())

def derive_hkdf(master_key: bytes, info: bytes, salt: bytes = b"", length: int = 32) -> str:
    derived = hashlib.hkdf(
        data=master_key,
        length=length,
        salt=salt or b"\x00" * 32,
        info=info,
        hash_func=hashlib.sha256
    )
    return derived.hex()

def main():
    parser = argparse.ArgumentParser(description="Cryptographic Guard & Integrity Tool")
    parser.add_argument("--gen-key", action="store_true", help="Generate secure 256-bit entropy key")
    parser.add_argument("--length", type=int, default=32, help="Key length in bytes (default: 32)")
    parser.add_argument("--format", choices=["hex", "base64"], default="hex", help="Output format")
    parser.add_argument("--hmac-sign", type=Path, help="Sign a file with HMAC-SHA256")
    parser.add_argument("--hmac-verify", type=Path, help="Verify a file against an HMAC-SHA256 tag")
    parser.add_argument("--key", type=str, help="Secret key (hex or string)")
    parser.add_argument("--tag", type=str, help="Expected HMAC tag for verification")
    parser.add_argument("--derive-subkeys", type=str, help="Derive domain-separated subkey with HKDF")

    args = parser.parse_args()

    if args.gen_key:
        key = generate_key(args.length, args.format)
        print("=" * 60)
        print(f" 🔑 Secure Random Key ({args.length * 8}-bit):")
        print(f" {key}")
        print("=" * 60)
        return

    if args.hmac_sign and args.key:
        key_bytes = bytes.fromhex(args.key) if len(args.key) == 64 else args.key.encode("utf-8")
        tag = compute_hmac(args.hmac_sign, key_bytes)
        print(f"[✓] HMAC-SHA256 ({args.hmac_sign.name}): {tag}")
        return

    if args.hmac_verify and args.key and args.tag:
        key_bytes = bytes.fromhex(args.key) if len(args.key) == 64 else args.key.encode("utf-8")
        valid = verify_hmac(args.hmac_verify, key_bytes, args.tag)
        if valid:
            print(f"[✓] Integrity Verified: HMAC match for {args.hmac_verify.name}")
            sys.exit(0)
        else:
            print(f"[!] Integrity Failure: HMAC mismatch for {args.hmac_verify.name}", file=sys.stderr)
            sys.exit(1)

    if args.derive_subkeys and args.key:
        key_bytes = bytes.fromhex(args.key) if len(args.key) == 64 else args.key.encode("utf-8")
        derived = derive_hkdf(key_bytes, args.derive_subkeys.encode("utf-8"))
        print(f"[✓] HKDF Derived Subkey for '{args.derive_subkeys}': {derived}")
        return

    parser.print_help()

if __name__ == "__main__":
    main()
