import urllib.parse
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

from app import __version__


# !/usr/bin/env python
# mypy: ignore-errors


class Settings(BaseSettings):
	# Application
	name: str = "MockyEnd"
	version: str = __version__
	API_V1_STR: str = "v1"
	DEBUG: bool = True

	# Database configuration
	# For more information on pool configuration, read:
	# https://docs.sqlalchemy.org/en/20/core/pooling.html
	db_max_pool_size: int = 5
	db_overflow_size: int = 10
	db_pool_recycle: int = 3600  # The connection pool will be recycled every 1 hour
	db_name: str
	db_host: str
	db_port: int
	db_user: str
	db_password: str
	# db_default_query_timeout_ms: int
	tracking_lock_duration: int = 120
	# isolation_level: str
	# isolation_level_transaction: str

	# Application configuration
	env: str  # dev, test, ci, prod

	model_config = SettingsConfigDict(
		env_prefix="APP_", env_file=".env", env_file_encoding="utf-8", extra="ignore"
	)

	@property
	def db_dsn(self) -> URL:
		return URL.create(
			drivername="postgresql+asyncpg",
			username=self.db_user,
			password=self.db_password,
			host=self.db_host,
			port=self.db_port,
			database=self.db_name,
		)

	@property
	def _db_password_escaped_for_alembic(self) -> str:
		"""Return the password escaping the special characters as required for Alembic.
		Follows recomendation on https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls.
		"""
		return urllib.parse.quote_plus(self.db_password).replace("%", "%%")

	@property
	def db_dsn_sync(self) -> str:
		return f"postgresql://{self.db_user}:{self._db_password_escaped_for_alembic}@{self.db_host}/{self.db_name}"


@lru_cache
def get_settings(env: str | None = None) -> Settings:
	return Settings()  # type: ignore
