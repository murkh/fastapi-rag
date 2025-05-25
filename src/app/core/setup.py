from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from .config import (
    AppSettings,
    DatabaseSettings,
    EnvironmentSettings
)
from .db.database import async_engine
from .db.models import Document
from .middleware import RequestLoggingMiddleware


async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Document.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for FastAPI application."""
    await init_db()
    yield


def create_application(
    router: APIRouter,
    settings: (
        DatabaseSettings |
        AppSettings |
        EnvironmentSettings
    )
):
    application = FastAPI(lifespan=lifespan)

    application.add_middleware(RequestLoggingMiddleware)

    application.include_router(router)

    return application
