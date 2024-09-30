from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.orm.models import AttractionsInfoORM, CityORM, InfoCityORM


async def get_information_city(session: AsyncSession, city_name: str) -> tuple:
    # Запрос на выборку данных города из двух таблиц, с помощью JOIN
    query_city_the_info = await session.execute(
        select(CityORM, InfoCityORM)
        .where(CityORM.city == city_name)
        .join(CityORM, CityORM.city == InfoCityORM.city_name)
    )
    query_result = query_city_the_info.all()
    # Запрос на выборку данных достопримечательностей города
    query_attractions = await session.execute(
        select(AttractionsInfoORM).where(AttractionsInfoORM.city_name == city_name)
    )
    query_result_attractions = query_attractions.scalars().all()
    return query_result, query_result_attractions


async def get_city(session: AsyncSession, city_name: str):
    query_city = await session.execute(select(CityORM).where(CityORM.city == city_name))
    query_result = query_city.scalars().all()
    return query_result


async def get_info_city(session: AsyncSession, city_name: str):
    query_info_city = await session.execute(
        select(InfoCityORM).where(InfoCityORM.city_name == city_name)
    )
    query_result = query_info_city.scalars().all()
    return query_result


async def get_attractions(session: AsyncSession, city_name: str):
    query_attractions = await session.execute(
        select(AttractionsInfoORM).where(AttractionsInfoORM.city_name == city_name)
    )
    query_result = query_attractions.scalars().all()
    return query_result
