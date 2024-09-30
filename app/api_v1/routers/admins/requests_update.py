from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.database.database_admin import update_data
from app.api_v1.orm.models import db_helper
from app.api_v1.orm.schemes.schemes_admin import (
    ResultResponse,
    UpdateAttractions,
    UpdateCity,
    UpdateCityInfo,
    UpdatePartialAttractions,
    UpdatePartialCity,
    UpdatePartialCityInfo,
)
from app.api_v1.orm.schemes.schemes_user import GetAttractions, GetCity, GetInfoCity
from app.api_v1.project_dependencies.auth.fastapi_users_router import current_moderator
from app.api_v1.project_dependencies.db.functions_db import (
    get_city_by_name,
    get_city_info_result,
    get_city_one_attractions,
)

router = APIRouter(tags=["Data update"])


@router.put(
    "/full-update/city/{city_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse,
    dependencies=[Depends(current_moderator)],
)
async def put_data_city(
    city_update: UpdateCity,
    city: GetCity = Depends(get_city_by_name),
    session: AsyncSession = Depends(db_helper.session_depends),
):
    return await update_data(
        session=session,
        data_class=city,
        data_update=city_update,
        exclude_unset=False,
    )


@router.put(
    "/full-update-city-info/{city_name}/",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse,
    dependencies=[Depends(current_moderator)],
)
async def put_data_city_info(
    city_info_update: UpdateCityInfo,
    city_info: GetInfoCity = Depends(get_city_info_result),
    session: AsyncSession = Depends(db_helper.session_depends),
):
    return await update_data(
        session=session,
        data_class=city_info,
        data_update=city_info_update,
        exclude_unset=False,
    )


@router.put(
    "/full-update-city-attractions/{title_attraction}/",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse,
    dependencies=[Depends(current_moderator)],
)
async def put_data_attractions(
    attractions_update: UpdateAttractions,
    city_attraction: GetAttractions = Depends(get_city_one_attractions),
    session: AsyncSession = Depends(db_helper.session_depends),
):
    return await update_data(
        session=session,
        data_class=city_attraction,
        data_update=attractions_update,
        exclude_unset=False,
    )


@router.patch(
    "/partial-update/city",
    dependencies=[Depends(current_moderator)],
)
async def patch_data_city_info(
    city_update: UpdatePartialCity,
    city: GetCity = Depends(get_city_by_name),
    session: AsyncSession = Depends(db_helper.session_depends),
):
    return await update_data(
        session=session,
        data_class=city,
        data_update=city_update,
        exclude_unset=True,
    )


@router.patch(
    "/partial/update/city-info",
    dependencies=[Depends(current_moderator)],
)
async def patch_data_city_info(
    city_info_update: UpdatePartialCityInfo,
    city_info: GetInfoCity = Depends(get_city_info_result),
    session: AsyncSession = Depends(db_helper.session_depends),
):
    return await update_data(
        session=session,
        data_class=city_info,
        data_update=city_info_update,
        exclude_unset=True,
    )


@router.patch(
    "/partial/update/city-attraction",
    dependencies=[Depends(current_moderator)],
)
async def patch_data_attractions(
    attractions_update: UpdatePartialAttractions,
    city_attraction: GetAttractions = Depends(get_city_one_attractions),
    session: AsyncSession = Depends(db_helper.session_depends),
):
    return await update_data(
        session=session,
        data_class=city_attraction,
        data_update=attractions_update,
        exclude_unset=False,
    )
