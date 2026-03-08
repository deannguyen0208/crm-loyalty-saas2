import hashlib
import hmac
import os
import re
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.core.config import settings

STRONG_PASSWORD_RE = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{10,64}$")


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)
    return f"{salt.hex()}:{digest.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
    salt_hex, digest_hex = password_hash.split(":")
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt_hex), 200_000)
    return hmac.compare_digest(digest.hex(), digest_hex)


def validate_strong_password(password: str) -> bool:
    return bool(STRONG_PASSWORD_RE.match(password))


def create_access_token(subject: str, minutes: int = 60 * 12) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=minutes)
    payload = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
