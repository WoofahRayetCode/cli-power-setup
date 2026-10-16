---
name: cryptographic-security-engineering
description: Applied modern cryptography and secure protocol implementations. Covers Ed25519 digital signatures (Discord interaction webhooks, Git commit signing), AES-256-GCM / ChaCha20-Poly1305 authenticated encryption, HKDF key derivation, constant-time comparison discipline, and hardware security module (TPM2/Keystore) integration.
---

# Cryptographic Security Engineering

This skill governs the correct implementation and auditing of cryptographic operations, digital signatures, authenticated encryption, and key derivation across applications, bots, and games.

---

## 1. Modern Cryptographic Primitives Standards

| Purpose | Standard Primitive | Deprecated / Broken (Banned) |
| :--- | :--- | :--- |
| **Digital Signatures** | **Ed25519** (RFC 8032) / ECDSA P-256 | RSA-1024, DSA, MD5/SHA-1 signatures |
| **Authenticated Encryption** | **AES-256-GCM** / **ChaCha20-Poly1305** | AES-CBC (padding oracle risks), AES-ECB, RC4 |
| **Key Derivation (Passwords)** | **Argon2id** (RFC 9106) | MD5, SHA-1, plain SHA-256, DES |
| **Key Derivation (Keys/PRK)** | **HKDF-SHA256** (RFC 5869) | Custom truncation, string concatenation |
| **Hash Functions** | **SHA-256**, **SHA-3**, **BLAKE3** | MD5, SHA-1 |

---

## 2. Ed25519 Webhook Signature Verification (Discord API v10)

Discord HTTP interactions require verifying incoming requests before parsing JSON:
```python
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError

def verify_discord_interaction(raw_body: bytes, signature_hex: str, timestamp: str, public_key_hex: str) -> bool:
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key_hex))
        message = timestamp.encode("utf-8") + raw_body
        verify_key.verify(message, bytes.fromhex(signature_hex))
        return True
    except (BadSignatureError, ValueError):
        return False
```

---

## 3. Authenticated Encryption with Associated Data (AEAD)

Always use AEAD (AES-256-GCM) rather than unauthenticated encryption:
* **Unique Nonce Requirement:**
  Never reuse an IV/nonce with the same key. Generate a 12-byte cryptographically secure random nonce (`secrets.token_bytes(12)`) per encryption operation and prepend it to the ciphertext:
  $$	ext{Ciphertext} = 	ext{Nonce (12B)} \parallel 	ext{AES-GCM-Encrypt}(K, 	ext{Nonce}, 	ext{Payload}, 	ext{AAD}) \parallel 	ext{Tag (16B)}$$

---

## 4. Constant-Time Comparison Discipline

Standard string equality operators (`==`) terminate early on the first mismatched byte, creating millisecond-level timing discrepancies that leak cryptographic secrets to remote network attackers.
* **Rule:** Always use constant-time comparisons for HMACs, API keys, password hashes, and auth tokens:
  * Python: `secrets.compare_digest(a, b)` / `hmac.compare_digest(a, b)`
  * C/C++: `CRYPTO_memcmp(a, b, len)` or OpenSSL `constant_time_memcmp`
  * Node.js / TypeScript: `crypto.timingSafeEqual(bufA, bufB)`

---

## 5. Standalone Cryptographic Guard Tool

Use `scripts/crypto_guard.py` for generating cryptographically secure entropy keys, calculating HMAC-SHA256 seals, deriving subkeys with HKDF, and testing constant-time verification.
