from datetime import datetime, timedelta, timezone
import re

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def validate_password_strength(password: str) -> tuple[bool, str]:
    if len(password) < 10:
        return False, "Mật khẩu phải có ít nhất 10 ký tự"
    if not re.search(r"[A-Z]", password):
        return False, "Mật khẩu phải có chữ hoa"
    if not re.search(r"[a-z]", password):
        return False, "Mật khẩu phải có chữ thường"
    if not re.search(r"\d", password):
        return False, "Mật khẩu phải có số"
    if not re.search(r"[^A-Za-z0-9]", password):
        return False, "Mật khẩu phải có ký tự đặc biệt"
    return True, "ok"


def create_access_token(subject: str) -> str:
    expires_delta = timedelta(minutes=settings.access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"exp": expire, "sub": subject}
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
