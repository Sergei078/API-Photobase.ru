from fastapi import Depends
from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)

from app.api_v1.orm.config_db import settings
from app.api_v1.orm.models import AccessToken
from app.api_v1.project_dependencies.auth.access_token import get_access_token_db


def get_database_strategy(
    access_token_db: AccessTokenDatabase["AccessToken"] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(
        access_token_db,
        lifetime_seconds=settings.lifetime_seconds,
    )
