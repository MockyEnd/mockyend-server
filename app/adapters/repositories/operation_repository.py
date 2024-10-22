from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import bindparam

from app.adapters.repositories.base_repository import (
	BaseRepository,
	not_implemented_error,
)
from app.adapters.repositories.database import DatabaseRepository
from app.adapters.repositories.exceptions import DatabaseError
from app.adapters.repositories.schemas import OperationCreate
from app.domain.models.operation import Operation


class OperationRepository(BaseRepository[Operation], ABC):
	@abstractmethod
	async def save(self, operation: OperationCreate) -> Operation:
		raise not_implemented_error(method_name=f"{self.__class__.__name__}.save")


class OperationRepositoryImpl(OperationRepository):
	def __init__(self, database: DatabaseRepository):
		self._database = database

	async def save(self, operation: OperationCreate) -> Operation:
		serialized_response = self._serialize_response(operation.response_content)

		stmt = (
			text(
				"""
            INSERT INTO operation (
                name,
                summary,
                description,
                method,
                path,
                response_type,
                response_content
            ) VALUES (
                :name,
                :summary,
                :description,
                :method,
                :path,
                :response_type,
                :response_content
            )
            RETURNING *
            """
			)
			.bindparams(bindparam("response_content", type_=JSONB))
			.bindparams(
				name=operation.name,
				summary=operation.summary,
				description=operation.description,
				method=operation.method,
				path=operation.path,
				response_type=operation.response_type,
				response_content=serialized_response,
			)
		)

		# stmt = text("SELECT id, name FROM user WHERE name=:name "
		#             "AND timestamp=:timestamp")
		# stmt = stmt.bindparams(
		#     bindparam('name', type_=String),
		#     bindparam('timestamp', type_=DateTime)
		# )
		# stmt = stmt.bindparams(
		#     name='jack',
		#     timestamp=datetime.datetime(2012, 10, 8, 15, 12, 5)
		# )

		result = await self._database.write(stmt=stmt)
		row = result.fetchone()
		if row is None:
			DatabaseError("Unexpected error: Operation creation failed.")

		return Operation.model_validate(row._mapping)

	# async def save(self, operation: OperationCreate) -> Operation:
	#     serialized_response = self._serialize_response(operation.response_content)
	#
	#     stmt = text(
	#         """
	#         INSERT INTO operation (
	#             name,
	#             summary,
	#             description,
	#             method,
	#             path,
	#             response_type,
	#             response_content
	#         ) VALUES (
	#             :name,
	#             :summary,
	#             :description,
	#             :method,
	#             :path,
	#             :response_type,
	#             :response_content:::jsonb
	#         )
	#         RETURNING *
	#         """
	#     )
	#
	#     params = {
	#         'name': operation.name,
	#         'summary': operation.summary,
	#         'description': operation.description,
	#         'method': operation.method,
	#         'path': operation.path,
	#         'response_type': operation.response_type,
	#         'response_content': serialized_response
	#     }
	#
	#     result = await self._database.write(stmt=stmt.bindparams(**params))
	#     row = result.fetchone()
	#     if row is None:
	#         DatabaseError("Unexpected error: Operation creation failed.")
	#
	#     return Operation.model_validate(row._mapping)

	def _serialize_response(self, response_content: Any | None):
		if response_content:
			result = response_content
			if isinstance(response_content, list):
				result = [self._serialize_response(item) for item in response_content]
			elif isinstance(response_content, BaseModel):
				result = response_content.dict()

			return result

		return None

	async def get_by_id(self, _id: int) -> Operation:
		pass

	async def get_by_uuid(self, _id: int) -> Operation:
		pass
