from fastapi import APIRouter, FastAPI
from .config import (
    AppSettings,
    DatabaseSettings,
    EnvironmentSettings
)
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
