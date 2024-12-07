from uuid import UUID
from abc import ABC, abstractmethod
from typing import TypeVar, Generic

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def not_implemented_error(method_name: str):
	return NotImplementedError(f"Error! {method_name} not implemented.")


class BaseRepository(ABC, Generic[T]):
	@abstractmethod
	async def get_by_id(self, _id: int) -> T:
		raise not_implemented_error(method_name=f"{self.__class__.__name__}.get_by_id")

	@abstractmethod
	async def get_by_uuid(self, uuid: UUID) -> T:
		raise not_implemented_error(method_name=f"{self.__class__.__name__}.get_by_uuid")
