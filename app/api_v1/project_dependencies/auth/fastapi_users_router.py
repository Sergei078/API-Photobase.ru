from fastapi import Depends, HTTPException, status
from fastapi_users import FastAPIUsers

from app.api_v1.orm.models import User
from app.api_v1.project_dependencies.auth.backend import auth_backend
from app.api_v1.project_dependencies.auth.user_manager import get_user_manager

fastapi_user = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


# Функция для проверки на права пользователя
def current_users(
    user: User = Depends(
        fastapi_user.current_user(
            active=True,
        )
    ),
) -> User:
    return user


# Функция для проверки на права редактора
def current_redactor(
    user: User = Depends(
        fastapi_user.current_user(
            active=True,
            verified=True,
        )
    ),
) -> User:
    if user.is_redactor is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return user


# Функция для проверки на права модератора
def current_moderator(
    user: User = Depends(
        fastapi_user.current_user(
            active=True,
            verified=True,
        )
    ),
) -> User:
    if user.is_moderator is False:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
        )
    return user


# Функция для проверки на права супер администратора
def current_super_admin(
    user: User = Depends(
        fastapi_user.current_user(
            superuser=True,
            active=True,
            verified=True,
        )
    ),
) -> User:
    return user
