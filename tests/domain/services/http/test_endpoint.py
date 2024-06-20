import pytest
from httpx import AsyncClient
from starlette.status import HTTP_200_OK

from app.domain.models.operation import Operation, Method
from app.domain.services.http.endpoint import build_get_endpoint, register_endpoint
from app.main import app


def test_build_get_endpoint():
    # Given
    operation = Operation(
        name="Ping",
        summary="A ping endpoint",
        description="Ping and pong",
        method=Method.GET,
        path="/v1/ping",
        response="pong"
    )

    # When
    router = build_get_endpoint(operation=operation)

    # Then
    assert len(router.routes) == 1
    assert router.include_in_schema is True
    ping_route = router.routes[0]

    assert ping_route.summary == operation.summary
    assert ping_route.description == operation.description
    assert len(ping_route.methods) == 1
    assert Method.GET in ping_route.methods
    assert ping_route.path == operation.path


def test_register_endpoint():
    # Given
    total_routes = len(app.routes)
    operation = Operation(
        name="Ping",
        method=Method.GET,
        path="/v1/ping",
        response="pong"
    )

    # When
    registered = register_endpoint(operation=operation, app=app)

    # Then
    assert registered is True
    assert app.openapi_schema is None
    assert len(app.routes) == total_routes + 1


PING_URL = "/v1/ping"
HEALTH_URL = "/v1/health"


def _register_ping_endpoint():
    ping_operation = Operation(
        name="Ping",
        method=Method.GET,
        path=PING_URL,
        response="pong"
    )

    return register_endpoint(operation=ping_operation, app=app)


def _register_health_endpoint():
    health_operation = Operation(
        name="Health",
        method=Method.GET,
        path=HEALTH_URL,
        response="Ok"
    )

    return register_endpoint(operation=health_operation, app=app)


def test__register_more_than_one_get_endpoint():
    # Given
    total_routes = len(app.routes)

    # When
    is_ping_registered = _register_ping_endpoint()
    is_health_registered = _register_health_endpoint()

    # Then
    assert is_ping_registered is True
    assert is_health_registered is True
    assert app.openapi_schema is None
    assert len(app.routes) == total_routes + 2


@pytest.mark.asyncio
async def test__call_registered_endpoints():
    _register_ping_endpoint()
    _register_health_endpoint()

    async with AsyncClient(app=app, base_url="http://test") as client:
        ping_response = await client.get(url=PING_URL)

        assert ping_response.status_code == HTTP_200_OK
        assert ping_response.json() == "pong"

        health_response = await client.get(url=HEALTH_URL)
        assert health_response.status_code == HTTP_200_OK
        assert health_response.json() == "Ok"
