from fastapi import APIRouter, FastAPI
from .config import (
    AppSettings,
    DatabaseSettings,
    EnvironmentSettings
)
from .db.database import async_engine
from .db.models import Document


async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Document.metadata.create_all)


def create_application(
    router: APIRouter,
    settings: (
        DatabaseSettings |
        AppSettings |
        EnvironmentSettings
    )
):
    application = FastAPI()
    application.include_router(router)

    @application.on_event("startup")
    async def startup_event():
        await init_db()

    return application
