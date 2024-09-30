import datetime

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship


class UserIdMixin:
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        unique=True,
    )
    registration_date: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        default=datetime.datetime.now(),
    )
    connection_delete_city_info = relationship("AccessToken", cascade="delete, all")
