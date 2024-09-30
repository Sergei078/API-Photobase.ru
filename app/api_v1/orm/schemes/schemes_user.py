from typing import List

from pydantic import BaseModel, Field


class AttractionsInfoSchema(BaseModel):
    title_attractions: str = Field(
        examples=["string"], default=None, description="Название достопримечательности"
    )
    description_attractions: str = Field(
        examples=["string"], default=None, description="Описание достопримечательности"
    )
    photo_attractions: str | None = Field(
        examples=["string"], default=None, description="Фото достопримечательности"
    )
    address: str | None = Field(
        examples=["string"], default=None, description="Адрес достопримечательности"
    )


class InfoCitySchema(BaseModel):
    description_city: str = Field(
        examples=["string"], default=None, description="Описание города"
    )
    language: str = Field(
        examples=["string"], default=None, description="Официальный язык города"
    )
    status: str = Field(
        examples=["string"], default=None, description="Официальный статус города"
    )
    timezone: str | None = Field(
        examples=["string"], default=None, description="Часовой пояс"
    )
    photo: str | None = Field(
        examples=["string"], default=None, description="Фотография города"
    )


class CityDataSchema(BaseModel):
    city: str = Field(examples=["string"], default=None, description="Название города")
    region_code: int = Field(
        examples=[0], default=None, description="Официальный код города"
    )
    country: str = Field(
        examples=["string"],
        default=None,
        description="Страна в которой находится город",
    )
    city_information: List[InfoCitySchema] = Field(default=None)
    attraction_city: List[AttractionsInfoSchema] = Field(default=None)


class GetCity(BaseModel):
    city: str
    region_code: int
    country: str


class GetInfoCity(BaseModel):
    description_city: str
    language: str
    status: str
    timezone: str
    photo: str


class GetAttractions(BaseModel):
    title_attractions: str
    description_attractions: str
    photo_attractions: str
    address: str
