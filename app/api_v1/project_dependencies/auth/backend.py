from fastapi_users.authentication import AuthenticationBackend

from app.api_v1.orm.authentication.transport import bearer_transport
from app.api_v1.project_dependencies.auth.strategy import get_database_strategy

auth_backend = AuthenticationBackend(
    name="database-tokens-access",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)
