import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from sqlalchemy import TIMESTAMP, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api_v1.orm.models import Base


class User(Base, SQLAlchemyBaseUserTable[int]):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        unique=True,
    )
    registration_date: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        default=datetime.datetime.now(),
    )
    is_redactor: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_moderator: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    connection_delete_access_token = relationship("AccessToken", cascade="delete, all")

    @classmethod
    def get_user_db(cls, session: AsyncSession):
        return SQLAlchemyUserDatabase(session, cls)
