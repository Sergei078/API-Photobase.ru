from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.api_v1.orm.schemes.user_auth import UserCreate, UserRead
from app.api_v1.project_dependencies.auth.backend import auth_backend
from app.api_v1.project_dependencies.auth.fastapi_users_router import fastapi_user

bearer_http = HTTPBearer(auto_error=False)
router = APIRouter(
    prefix="/authorization",
    tags=["User authorization"],
    dependencies=[Depends(bearer_http)],
)

router.include_router(
    fastapi_user.get_auth_router(
        auth_backend,
        # requires_verification=True,
    )
)
router.include_router(
    router=fastapi_user.get_register_router(
        UserRead,
        UserCreate,
    ),
)

router.include_router(fastapi_user.get_verify_router(UserRead))
router.include_router(fastapi_user.get_reset_password_router())
