import logging
from time import perf_counter

from fastapi import FastAPI, Request

from app.config import settings
from app.core.errors import register_exception_handlers
from app.routers.appointment import router as appointment_router
from app.routers.auth import router as auth_router
from app.routers.medical_history import router as medical_history_router
from app.routers.patient import router as patient_router
from app.routers.prediction import router as prediction_router


app = FastAPI(title=settings.app_name, version=settings.app_version, debug=settings.debug)
logger = logging.getLogger("careportal.api")

# Add global error handlers so all routes return errors in one format.
register_exception_handlers(app)
# Add auth routes (register, login, and protected user endpoint).
app.include_router(auth_router)
app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(medical_history_router)
app.include_router(prediction_router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = perf_counter()
    response = await call_next(request)
    elapsed_ms = (perf_counter() - start) * 1000
    logger.info(
        "%s %s -> %s (%.2f ms)",
        request.method,
        request.url.path,
        response.status_code,
        elapsed_ms,
    )
    return response


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    # Quick endpoint to confirm API is running.
    return {"status": "ok"}
