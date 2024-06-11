from fastapi import FastAPI

from app.api import router as main_router
from app.core.settings import get_settings


def create_app() -> FastAPI:
    settings = get_settings()

    _app = FastAPI(
        debug=settings.DEBUG,
        title=settings.name,
        version=settings.version,
        description="Mockend is your best friend for mocking everything for your backend services",
        openapi_url=f"/openapi.json",
    )

    _app.include_router(main_router)

    return _app


app = create_app()
