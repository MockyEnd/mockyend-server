from fastapi import FastAPI

from app.api import router as main_router
from app.core.container.app import AppContainer
from app.core.settings import get_settings


def create_app() -> FastAPI:
	settings = get_settings()
	container = AppContainer()

	_app = FastAPI(
		debug=settings.DEBUG,
		title=settings.name,
		version=settings.version,
		description="MockyEnd is your best friend for mocking everything for your backend services",
		openapi_url="/openapi.json",
	)

	_app.container = container

	_app.include_router(main_router)

	return _app


app = create_app()
