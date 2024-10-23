from uuid import uuid4

import pytest
from httpx import AsyncClient
from starlette.status import (
	HTTP_201_CREATED,
	HTTP_422_UNPROCESSABLE_ENTITY,
	HTTP_400_BAD_REQUEST,
)

from app.domain.models.operation import DataType, Method
from app.main import app
from tests.unit import override_db_repository, FetchOne, DatabaseResult


@pytest.mark.asyncio
async def test__register_operation(raw_operation_register_request):
	class OperationFetch(FetchOne):
		def fetchone(self) -> DatabaseResult:
			return DatabaseResult(
				{
					"id": 1,
					"uuid": uuid4(),
					"name": raw_operation_register_request["name"],
					"summary": raw_operation_register_request["summary"],
					"description": raw_operation_register_request["description"],
					"method": Method.GET,
					"path": raw_operation_register_request["path"],
					"response_type": DataType.LIST,
					"response_content": True,
				}
			)

	override_db_repository(fetcher=OperationFetch())

	async with AsyncClient(app=app, base_url="http://test") as client:
		response = await client.post(url="/operation/register", json=raw_operation_register_request)
		json_response = response.json()

		assert response.status_code == HTTP_201_CREATED
		assert json_response["endpoint"] == raw_operation_register_request["path"]
		assert json_response["status"] == "registered"


@pytest.mark.parametrize(
	"request_with_error, expected_status_error",
	[
		({"name": "Unprocessable request"}, HTTP_422_UNPROCESSABLE_ENTITY),
		(
			{
				"name": "Bad request",
				"summary": "Summary",
				"description": "Description",
				"method": "INVALID_HTTP_METHOD",
				"path": "/invalid",
				"response": {"primitive_value": {"value": "Error"}},
			},
			HTTP_400_BAD_REQUEST,
		),
	],
)
@pytest.mark.asyncio
async def test__register_operation_with_unprocessable_request(
	request_with_error, expected_status_error
):
	# When
	async with AsyncClient(app=app, base_url="http://test") as client:
		response = await client.post(url="/operation/register", json=request_with_error)
		json_response = response.json()

		# Then
		assert response.status_code == expected_status_error
		assert json_response["detail"] is not None
