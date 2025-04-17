import jwt
from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.repository.user_repository import UserRepository
from app.utils.db import get_db
from app.utils.token_manager import TokenManager


def get_current_user(
    authorization: str = Header(None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid token"
        )

    token = authorization.split(" ", 1)[1]
    try:
        payload = TokenManager.decode_access_token(token)
        user_id = int(payload["sub"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        )
    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        )

    user = UserRepository(db).get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user
