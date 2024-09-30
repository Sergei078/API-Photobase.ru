from typing import Annotated
import logging
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.database.database_admin import (
    create_new_entry_attraction_city,
    create_new_entry_info_city,
)
from app.api_v1.orm.models import db_helper
from app.api_v1.orm.schemes.schemes_admin import (
    CityAttractionPost,
    CityInfoDataPost,
    ResultResponse,
)
from app.api_v1.project_dependencies.auth.fastapi_users_router import (
    current_redactor,
)
from app.api_v1.orm.config_db import settings

logging.basicConfig(
    level=logging.INFO,
    filename=settings.filename_log,
    filemode=settings.filemod,
    format=settings.format_log,
    encoding="UTF-8",
)
router = APIRouter(tags=["Add data"])


@router.post(
    "/send/form/city/",
    response_model=ResultResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_redactor)],
)
async def post_add_city_info(
    data: Annotated[CityInfoDataPost, Depends()],
    session: AsyncSession = Depends(db_helper.session_depends),
):
    result = data.model_dump()
    dict_result_city: dict = {
        key: value
        for key, value in result.items()
        if key in ("city", "region_code", "country")
    }
    dict_result_city_info: dict = {
        key: value
        for key, value in result.items()
        if key
        in (
            "description_city",
            "language",
            "status",
            "timezone",
            "photo",
            "city_name",
        )
    }
    dict_result_city_info["city_name"] = dict_result_city.get("city")

    send_result = await create_new_entry_info_city(
        session=session,
        data_city=dict_result_city,
        data_info_city=dict_result_city_info,
    )
    if send_result is True:
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=False,
        )


@router.post(
    "/send/form/city-landmark/",
    response_model=ResultResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(current_redactor)],
)
async def post_add_city_info(
    data: Annotated[CityAttractionPost, Depends()],
    session: AsyncSession = Depends(db_helper.session_depends),
):
    send_result = await create_new_entry_attraction_city(session=session, data=data)
    if send_result is True:
        raise HTTPException(status_code=status.HTTP_201_CREATED, detail=True)
    else:
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail=False,
        )
