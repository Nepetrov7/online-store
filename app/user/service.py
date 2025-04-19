from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.user.repository import UserRepository
from app.user.schema import TokenOut, UserLogin, UserRegister
from app.utils.token_manager import TokenManager


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserRegister):
        # проверяем, что username свободен
        if self.repo.get_by_username(data.username):
            raise HTTPException(status_code=400, detail="Username already exists")

        # хэшируем пароль
        password_hash = TokenManager.hash_password(data.password)

        # создаём нового пользователя
        user = self.repo.create(
            first_name=data.first_name,
            last_name=data.last_name,
            username=data.username,
            password_hash=password_hash,
            role=data.role,
        )

        # выдаём токен
        token = TokenManager.create_access_token({"sub": str(user.id)})
        return TokenOut(access_token=token, token_type="bearer")

    def authenticate(self, data: UserLogin) -> TokenOut:
        # ищем пользователя
        user = self.repo.get_by_username(data.username)
        if not user or not TokenManager.verify_password(
            data.password, user.password_hash
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
        # создаём токен
        token = TokenManager.create_access_token({"sub": str(user.id)})
        return TokenOut(access_token=token, token_type="bearer")

    def logout(self, user_id: int):
        # например, можно занести токен в blacklist — здесь просто заглушка
        return
