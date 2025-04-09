from fastapi import APIRouter, Depends, Header, HTTPException, status
from passlib.hash import bcrypt
from sqlalchemy.orm import Session

from app.repository.user_repository import UserRepository
from app.schemas.auth_schemas import TokenOut, UserLogin, UserOut, UserRegister
from app.utils.db import get_db
from app.utils.dependencies import get_current_user
from app.utils.token_manager import create_token_for_user, delete_token

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    if not user_data.password.strip():
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Password cannot be empty",
        )

    repo = UserRepository(db)
    existing = repo.get_user_by_username(user_data.username)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken"
        )
    # Хэшируем пароль (passlib + bcrypt)
    password_hash = bcrypt.hash(user_data.password)
    new_user = repo.create_user(
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        username=user_data.username,
        password_hash=password_hash,
        role=user_data.role,
    )
    return new_user  # Pydantic преобразует User -> UserOut


@router.post("/login", response_model=TokenOut)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_user_by_username(credentials.username)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    # Проверяем пароль
    if not bcrypt.verify(credentials.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    # Создаём токен
    token = create_token_for_user(user.id)
    return TokenOut(access_token=token)


@router.post("/logout")
def logout_user(
    authorization: str = Header(None), current_user=Depends(get_current_user)
):
    """
    Ожидаем заголовок Authorization: Bearer <token>
    Удаляем токен из in_memory_tokens
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = authorization.split(" ")[1]
    delete_token(token)
    return {"message": "Successfully logged out"}
