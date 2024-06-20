import pytest
from httpx import AsyncClient
from starlette.status import HTTP_201_CREATED, HTTP_422_UNPROCESSABLE_ENTITY, HTTP_400_BAD_REQUEST

from app.main import app


@pytest.mark.asyncio
async def test__register_operation(raw_operation_register_request):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(url="/operation/register", json=raw_operation_register_request)
        json_response = response.json()

        assert response.status_code == HTTP_201_CREATED
        assert json_response["endpoint"] == raw_operation_register_request["path"]
        assert json_response["status"] == "registered"


@pytest.mark.parametrize(
    "request_with_error, expected_status_error",
    [
        (
                {
                    "name": "Unprocessable request"
                },
                HTTP_422_UNPROCESSABLE_ENTITY
        ),
        (
                {
                    "name": "Bad request",
                    "summary": "Summary",
                    "description": "Description",
                    "method": "INVALID_HTTP_METHOD",
                    "path": "/invalid",
                    "response": {
                        "primitive_value": {
                            "value": "Error"
                        }
                    }
                },
                HTTP_400_BAD_REQUEST
        ),
    ]
)
@pytest.mark.asyncio
async def test__register_operation_with_unprocessable_request(request_with_error, expected_status_error):
    # When
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(url="/operation/register", json=request_with_error)
        json_response = response.json()

        # Then
        assert response.status_code == expected_status_error
        assert json_response['detail'] is not None
