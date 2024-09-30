import os
import sys
import uvicorn

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBearer
from fastapi.middleware.cors import CORSMiddleware


root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_path)

from api_v1.orm.config_db import settings
from api_v1.routers import (
    router_admin_delete_query,
    router_admin_post_query,
    router_admin_update_query,
    router_auth,
    router_profile,
    router_user,
)


bearer_http = HTTPBearer(auto_error=False)


application = FastAPI(
    title="PhotoBase",
    description="Документация",
    version="0.1",
    dependencies=[Depends(bearer_http)],
)

application.include_router(router_auth, prefix=settings.url_path_main)
application.include_router(router_profile, prefix=settings.url_path_main)
application.include_router(router_user, prefix=settings.url_path_main)
application.include_router(router_admin_post_query, prefix=settings.url_path_admin)
application.include_router(router_admin_update_query, prefix=settings.url_path_admin)
application.include_router(router_admin_delete_query, prefix=settings.url_path_admin)

if __name__ == "__main__":
    uvicorn.run(application, host="0.0.0.0", port=8000)
