from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api_v1.orm.models import User, db_helper


async def get_user_db(session: AsyncSession = Depends(db_helper.session_depends)):
    return User.get_user_db(session=session)
