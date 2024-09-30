from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.orm.models import AttractionsInfoORM, CityORM, InfoCityORM
from app.api_v1.orm.schemes.schemes_admin import (
    CityAttractionPost,
)


async def create_new_entry_info_city(
    session: AsyncSession, data_city: dict, data_info_city: dict
) -> bool:
    try:
        save_city = CityORM(**data_city)
        save_info_city = InfoCityORM(**data_info_city)
        session.add(save_city)
        session.add(save_info_city)
        await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        return False


async def create_new_entry_attraction_city(
    session: AsyncSession, data: CityAttractionPost
) -> bool:
    try:
        json_convert = data.model_dump()
        new_info_record_db = AttractionsInfoORM(**json_convert)
        session.add(new_info_record_db)
        await session.commit()
        return True
    except IntegrityError:
        await session.rollback()
        return False


async def delete_recording(session: AsyncSession, data_class) -> bool:
    await session.delete(data_class)
    await session.commit()
    return True


# Функция для обновления данных в базе данных
async def update_data(
    session: AsyncSession,
    data_class,  # Получаем класс с данными которые нужно обновить
    data_update,  # Получаем класс, для заполнения новыми данными
    exclude_unset: bool,
) -> bool:
    for name, value in data_update.model_dump(exclude_unset=exclude_unset).items():
        setattr(data_class, name, value)
    await session.commit()
    return True


async def get_one_attractions(session: AsyncSession, title_attraction: str):
    query_attractions = await session.execute(
        select(AttractionsInfoORM).where(
            AttractionsInfoORM.title_attractions == title_attraction
        )
    )
    query_result = query_attractions.scalars().all()
    return query_result
