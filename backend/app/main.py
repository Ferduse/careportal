from fastapi import FastAPI

from app.config import settings
from app.core.errors import register_exception_handlers
from app.routers.auth import router as auth_router


app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

register_exception_handlers(app)
app.include_router(auth_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    return {"status": "ok"}
