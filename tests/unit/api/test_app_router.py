import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from app.main import app


@pytest.mark.asyncio
async def test_health_endpoint():
	async with AsyncClient(app=app, base_url="http://test") as client:
		response = await client.get(url="/health")
		json_response = response.json()

		assert response.status_code == HTTP_200_OK
		assert json_response["message"] == "It's running!"
