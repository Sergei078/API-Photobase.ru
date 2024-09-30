from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import Field
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.database.database_user import get_information_city
from app.api_v1.orm.models import db_helper
from app.api_v1.orm.schemes.schemes_user import (
    CityDataSchema,
    GetAttractions,
    GetCity,
    GetInfoCity,
)
from app.api_v1.project_dependencies.auth.fastapi_users_router import current_users
from app.api_v1.project_dependencies.db.functions_db import (
    extract_data_db,
    get_attraction_city_list,
    get_city_by_name,
    get_city_info_result,
)

router = APIRouter(tags=["Get data"])


@router.get(
    "/receive/full-information/city/",
    response_model=CityDataSchema,
    dependencies=[Depends(current_users)],
)
async def get_data_by_city_id(
    city_name: Annotated[str, Field(max_length=50)],
    session: AsyncSession = Depends(db_helper.session_depends),
):
    result_db = await get_information_city(session=session, city_name=city_name)
    unpack_data = await extract_data_db(result_db)
    if unpack_data is None:
        raise HTTPException(status_code=500, detail="Invalid ID")
    return unpack_data


@router.get(
    "/receive/city/{city_name}/",
    response_model=GetCity,
    dependencies=[Depends(current_users)],
)
async def get_city(
    city: GetCity = Depends(get_city_by_name),
) -> GetCity:
    return city


@router.get(
    "/receive/city-information/{city_name}/",
    response_model=GetInfoCity,
    dependencies=[Depends(current_users)],
)
async def get_info_city_by_id(
    city_info: GetInfoCity = Depends(get_city_info_result),
) -> GetInfoCity:
    return city_info


@router.get(
    "/receive/attractions/{city_name}/",
    response_model=list[GetAttractions],
    dependencies=[Depends(current_users)],
)
async def get_attractions_id(
    city_attractions: GetAttractions = Depends(get_attraction_city_list),
) -> GetAttractions:
    if not city_attractions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return city_attractions
