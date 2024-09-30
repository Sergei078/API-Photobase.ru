from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.database.database_admin import delete_recording
from app.api_v1.orm.models import db_helper, User
from app.api_v1.orm.schemes.schemes_admin import ResultResponse
from app.api_v1.orm.schemes.schemes_user import GetAttractions, GetCity
from app.api_v1.project_dependencies.auth.fastapi_users_router import (
    current_super_admin,
)
from app.api_v1.project_dependencies.db.functions_db import (
    get_city_by_name,
    get_city_one_attractions,
)

router = APIRouter(tags=["Data delete"])


@router.delete(
    "/delete/city/",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse,
    description="Внимание, удаление города приведет к удаление всей информации о нем, включая достопримечательности",
    dependencies=[Depends(current_super_admin)],
)
async def delete_city_by_id(
    admin_user: Annotated[User, Depends(current_super_admin)],
    city: GetCity = Depends(get_city_by_name),
    session: AsyncSession = Depends(db_helper.session_depends),
):
    delete_result = await delete_recording(session=session, data_class=city)
    return {"done": delete_result, "name_admin": admin_user.username}


@router.delete(
    "/delete/city-attraction/",
    status_code=status.HTTP_200_OK,
    response_model=ResultResponse,
    dependencies=[Depends(current_super_admin)],
)
async def delete_city_attractions(
    admin_user: Annotated[User, Depends(current_super_admin)],
    city_attraction: GetAttractions = Depends(get_city_one_attractions),
    session: AsyncSession = Depends(db_helper.session_depends),
):
    delete_result = await delete_recording(session=session, data_class=city_attraction)
    return {"done": delete_result, "name_admin": admin_user.username}
