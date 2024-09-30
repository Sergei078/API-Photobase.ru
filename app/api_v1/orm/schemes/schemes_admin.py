from enum import Enum

from pydantic import BaseModel, Field


class TimezoneCity(str, Enum):
    zona_1 = "UTC+2"
    zona_2 = "UTC+3"
    zona_3 = "UTC+4"
    zona_4 = "UTC+5"
    zona_5 = "UTC+6"
    zona_6 = "UTC+7"
    zona_7 = "UTC+8"
    zona_8 = "UTC+9"
    zona_9 = "UTC+10"
    zona_10 = "UTC+11"
    zona_11 = "UTC+12"


class StatusCity(str, Enum):
    status_1 = "Город"
    status_2 = "Поселок"
    status_3 = "Посёлок городского типа"
    status_4 = "Село"
    status_5 = "Деревня"


class CountryList(str, Enum):
    country_1 = "Россия"


class CityDataFormPost(BaseModel):
    city: str = Field(max_length=60, min_length=1, strict=True)
    region_code: int = Field(gt=0, lt=95)
    country: CountryList


class CityInfoDataPost(CityDataFormPost):
    description_city: str = Field(max_length=100, min_length=20, strict=True)
    language: str = Field(max_length=60, min_length=3, strict=True)
    status: StatusCity
    timezone: TimezoneCity
    photo: str = Field(max_length=200, min_length=1, strict=True)


class InfoCity(BaseModel):
    description_city: str
    language: str
    status: StatusCity
    timezone: TimezoneCity
    photo: str
    city_name: str


class CityAttractionPost(BaseModel):
    title_attractions: str
    description_attractions: str
    photo_attractions: str | None = "None"
    address: str | None = "None"
    city_name: str


class ResultResponse(BaseModel):
    detail: bool


# Схемы на частичное обновление данных
class UpdateCity(BaseModel):
    region_code: int
    country: str


class UpdateCityInfo(BaseModel):
    description_city: str
    language: str
    status: StatusCity
    timezone: TimezoneCity
    photo: str


class UpdateAttractions(BaseModel):
    title_attractions: str
    description_attractions: str
    photo_attractions: str
    address: str


# Схемы на полное обновление данных
class UpdatePartialCity(BaseModel):
    region_code: int | None = None
    country: str | None = None


class UpdatePartialCityInfo(BaseModel):
    description_city: str | None = None
    language: str | None = None
    status: StatusCity = None
    timezone: TimezoneCity = None
    photo: str | None = None


class UpdatePartialAttractions(BaseModel):
    title_attractions: str | None = None
    description_attractions: str | None = None
    photo_attractions: str | None = None
    address: str | None = None
