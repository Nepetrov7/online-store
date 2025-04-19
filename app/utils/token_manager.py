from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.utils.config import settings

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


class TokenManager:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_ctx.hash(password)

    @staticmethod
    def verify_password(plain: str, hashed: str) -> bool:
        return pwd_ctx.verify(plain, hashed)

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        to_encode.update({"exp": expire, "sub": str(data.get("sub"))})
        # возвращает строку токена
        return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)

    @staticmethod
    def decode_access_token(token: str) -> dict:
        """
        Декодирует и проверяет подпись/срок жизни.
        Бросает jwt.ExpiredSignatureError или jwt.InvalidTokenError.
        """
        return jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM],
            options={"require_sub": True},
        )
