from abc import ABC, abstractmethod
from typing import Dict

from sqlalchemy import TextClause

from app.adapters.repositories.base_repository import not_implemented_error
from app.adapters.repositories.database import DatabaseRepository
from app.core.container.app import AppContainer


class DatabaseResult:
	def __init__(self, stored_data: Dict):
		self._mapping = stored_data


class Fetcher(ABC):
	pass


class FetchOne(Fetcher, ABC):
	@abstractmethod
	def fetchone(self) -> DatabaseResult:
		raise not_implemented_error(method_name=f"{self.__class__.__name__}.fetchone")


class FakeDatabaseRepository(DatabaseRepository):
	def __init__(self, fetcher: Fetcher):
		self.fetcher = fetcher

	async def read(self, stmt: TextClause):
		return self.fetcher

	async def write(self, stmt: TextClause):
		return self.fetcher


def override_db_repository(fetcher: Fetcher):
	test_container = AppContainer()
	test_container.db_repository.override(FakeDatabaseRepository(fetcher=fetcher))
