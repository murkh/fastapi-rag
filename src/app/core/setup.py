from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI
from .config import (
    AppSettings,
    DatabaseSettings,
    EnvironmentSettings
)
from .db.database import async_engine
from .middleware import RequestLoggingMiddleware


def create_application(
    router: APIRouter,
    settings: (
        DatabaseSettings |
        AppSettings |
        EnvironmentSettings
    )
):
    application = FastAPI()

    application.add_middleware(RequestLoggingMiddleware)

    application.include_router(router)

    return application
