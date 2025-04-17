from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.schemas.user_schemas import TokenOut, UserLogin, UserOut, UserRegister
from app.services.user_service import UserService
from app.utils.dependencies import get_current_user, get_db

router = APIRouter()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_in: UserRegister,
    service: UserService = Depends(get_user_service),
):
    return service.register(user_in)


@router.post(
    "/login",
    response_model=TokenOut,
)
def login_user(
    credentials: UserLogin,
    service: UserService = Depends(get_user_service),
):
    return service.authenticate(credentials)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout_user(
    current_user=Depends(get_current_user),
    service: UserService = Depends(get_user_service),
):
    service.logout(current_user.id)
