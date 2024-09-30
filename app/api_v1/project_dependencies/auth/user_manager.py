from fastapi import Depends

from app.api_v1.orm.authentication.user_manager import UserManager
from app.api_v1.project_dependencies.auth.users import get_user_db


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
