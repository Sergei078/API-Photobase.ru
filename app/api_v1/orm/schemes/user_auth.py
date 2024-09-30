from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr


class UserRead(schemas.BaseUser[int]):
    username: str
    is_redactor: bool | None = False
    is_moderator: bool | None = False


class UserCreate(schemas.BaseUserCreate):
    username: str
    is_redactor: bool | None = False
    is_moderator: bool | None = False


class UserUpdate(schemas.BaseUserUpdate):
    username: str
    is_redactor: bool | None = False
    is_moderator: bool | None = False
