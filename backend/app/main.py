from fastapi import FastAPI

from app.config import settings
from app.core.errors import register_exception_handlers
from app.routers.auth import router as auth_router


app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)

# Add global error handlers so all routes return errors in one format.
register_exception_handlers(app)
# Add auth routes (register, login, and protected user endpoint).
app.include_router(auth_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    # Quick endpoint to confirm API is running.
    return {"status": "ok"}
