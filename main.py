from fastapi import FastAPI
from app.core.settings import settings
from app.api.endpoints import health

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION
)

# Include routers
app.include_router(health.router, tags=["health"]) 