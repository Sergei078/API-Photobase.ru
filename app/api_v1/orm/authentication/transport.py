from fastapi_users.authentication import BearerTransport

from app.api_v1.orm.config_db import settings

bearer_transport = BearerTransport(tokenUrl=settings.bearer_token_url)
