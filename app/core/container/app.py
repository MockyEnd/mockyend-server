import httpx
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import create_async_engine

from app.adapters.repositories.database import DatabaseRepositoryImpl
from app.adapters.repositories.operation_repository import OperationRepositoryImpl
from app.core.settings import get_settings
from app.domain.services.operation.register_operation import CreateOperationService


class AppContainer(containers.DeclarativeContainer):
	wiring_config = containers.WiringConfiguration(packages=["app.api.v1"])

	config = providers.Configuration()
	settings = get_settings()
	config.from_dict(settings.model_dump())

	db = providers.Singleton(
		create_async_engine,
		settings.db_dsn,
		isolation_level=config.get("isolation_level"),
		pool_size=config.get("db_max_pool_size"),
		max_overflow=config.get("db_overflow_size"),
		pool_recycle=config.get("db_pool_recycle"),
		pool_pre_ping=True,
		echo=config.get("db_echo"),
		echo_pool=config.get("db_echo_pool"),
	)

	db_transaction = providers.Singleton(
		create_async_engine,
		settings.db_dsn,
		isolation_level=config.get("isolation_level_transaction"),
		pool_size=config.get("db_max_pool_size"),
		max_overflow=config.get("db_overflow_size"),
		pool_recycle=config.get("db_pool_recycle"),
		pool_pre_ping=True,
		echo=config.get("db_echo"),
		echo_pool=config.get("db_echo_pool"),
	)

	async_http_client = providers.Resource(
		httpx.AsyncClient,
	)

	# Database Repositories
	db_repository = providers.Factory(DatabaseRepositoryImpl, db=db)
	operation_repository = providers.Factory(OperationRepositoryImpl, database=db_repository)

	# Services
	create_operation_service = providers.Factory(
		CreateOperationService, repository=operation_repository
	)
