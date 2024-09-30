import random
from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.database.database_admin import get_one_attractions
from app.api_v1.database.database_user import get_attractions, get_city, get_info_city
from app.api_v1.orm.models import db_helper


async def get_city_by_name(
    city_name: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_depends),
):
    result_query_db = await get_city(session=session, city_name=city_name)
    if not result_query_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID does not exist",
        )
    return result_query_db[0]


async def get_city_info_result(
    city_name: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_depends),
):
    result_query_db = await get_info_city(session=session, city_name=city_name)
    if not result_query_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID does not exist",
        )
    return result_query_db[0]


async def get_city_one_attractions(
    title_attraction: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_depends),
):
    result_query_db = await get_one_attractions(
        session=session, title_attraction=title_attraction
    )
    if not result_query_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The name is not valid",
        )
    return result_query_db[0]


async def get_attraction_city_list(
    city_name: Annotated[str, Path],
    session: AsyncSession = Depends(db_helper.session_depends),
):
    result_query_db = await get_attractions(session=session, city_name=city_name)
    if not result_query_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ID does not exist",
        )
    return result_query_db


async def extract_data_db(tuple_result: tuple) -> dict | None:
    result_info = tuple_result[0]
    if not result_info:
        return None
    data_list_attractions = tuple_result[1]
    task_list = True
    result_list = [None, None, None, None]
    if not data_list_attractions:
        task_list = False
    else:
        random_result = random.choice(data_list_attractions)
        result_list = [
            random_result.title_attractions,
            random_result.description_attractions,
            random_result.photo_attractions,
            random_result.address,
        ]
    keys = [
        "city",
        "region_code",
        "country",
        "description_city",
        "language",
        "status",
        "timezone",
        "photo",
        "title_attractions",
        "description_attractions",
        "photo_attractions",
        "address",
    ]
    data = [
        result_info[0][0].city,
        result_info[0][0].region_code,
        result_info[0][0].country,
        result_info[0][1].description_city,
        result_info[0][1].language,
        result_info[0][1].status,
        result_info[0][1].timezone,
        result_info[0][1].photo,
        result_list[0],
        result_list[1],
        result_list[2],
        result_list[3],
    ]
    result_city_main_dict = {}
    result_info_dict = {}
    result_attraction_dict = {}
    for i in range(0, 12):
        if i <= 2:
            result_city_main_dict.update({keys[i]: data[i]})
        elif 2 < i <= 7:
            result_info_dict.update({keys[i]: data[i]})
            result_city_main_dict.update({"city_information": [result_info_dict]})
        elif i > 7 and task_list is True:
            result_attraction_dict.update({keys[i]: data[i]})
            result_city_main_dict.update({"attraction_city": [result_attraction_dict]})
        else:
            break
    return dict(result_city_main_dict)
