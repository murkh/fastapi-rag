from fastapi import APIRouter, FastAPI
from .config import (
    AppSettings,
    DatabaseSettings,
    EnvironmentSettings
)


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

    return application
