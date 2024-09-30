from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.api_v1.orm.models.base import Base


class CityORM(Base):
    __tablename__ = "city_data"

    city: Mapped[str] = mapped_column(primary_key=True, unique=True)
    region_code: Mapped[int] = mapped_column(nullable=False)
    country: Mapped[str]
    connection_delete_city_info = relationship("InfoCityORM", cascade="delete, all")
    connection_delete_attractions = relationship(
        "AttractionsInfoORM", cascade="delete, all"
    )


class InfoCityORM(Base):
    __tablename__ = "city_info"

    description_city: Mapped[str]
    language: Mapped[str]
    status: Mapped[str]
    timezone: Mapped[str]
    photo: Mapped[str]
    city_name: Mapped[str] = mapped_column(
        ForeignKey("city_data.city", ondelete="CASCADE"),
        unique=True,
        primary_key=True,
    )


class AttractionsInfoORM(Base):
    __tablename__ = "city_attractions"

    title_attractions: Mapped[str] = mapped_column(primary_key=True, unique=True)
    description_attractions: Mapped[str]
    photo_attractions: Mapped[str]
    address: Mapped[str] = mapped_column(nullable=True)
    city_name: Mapped[str] = mapped_column(
        ForeignKey("city_data.city", ondelete="CASCADE")
    )
