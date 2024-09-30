from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.api_v1.orm.schemes.user_auth import UserRead, UserUpdate
from app.api_v1.project_dependencies.auth.fastapi_users_router import \
    fastapi_user

bearer_http = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/authorization",
    tags=["User profile"],
    dependencies=[Depends(bearer_http)],
)


router.include_router(
    router=fastapi_user.get_users_router(
        UserRead,
        UserUpdate,
    ),
)
