from typing import Optional
try:
    import win32crypt  # type: ignore
except Exception:  # pragma: no cover
    win32crypt = None  # type: ignore

from cryptography.fernet import Fernet


def protect(data: bytes) -> bytes:
    if win32crypt:
        return win32crypt.CryptProtectData(data, None, None, None, None, 0)
    key = Fernet.generate_key()
    return Fernet(key).encrypt(data)


def unprotect(data: bytes) -> bytes:
    if win32crypt:
        return win32crypt.CryptUnprotectData(data, None, None, None, 0)[1]
    # Note: For non-Windows fallback, caller must manage key storage.
    raise RuntimeError("Fernet fallback requires managed key")

