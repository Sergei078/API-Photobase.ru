from typing import Optional, Union

from fastapi import HTTPException, Request, status
from fastapi_users import (
    BaseUserManager,
    IntegerIDMixin,
    InvalidPasswordException,
    exceptions,
    models,
    schemas,
)

from app.api_v1.orm.config_db import settings
from app.api_v1.orm.models import User
from app.api_v1.orm.schemes.user_auth import UserCreate


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = settings.password_secret
    verification_token_secret = settings.verification_secret

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < 10:
            raise InvalidPasswordException(
                reason="Password should be at least 10 characters"
            )
        if user.email in password:
            raise InvalidPasswordException(reason="Password should not contain e-mail")
        if len(user.username) < 3:
            raise InvalidPasswordException(
                reason="The name cannot be less than 3 characters"
            )

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        raise HTTPException(
            status_code=status.HTTP_201_CREATED,
            detail={"done": True},
        )

    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:
        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["is_redactor"] = False
        user_dict["is_moderator"] = False

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user
