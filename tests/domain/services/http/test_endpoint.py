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


def test_register_more_than_one_get_endpoint():
    # Given
    total_routes = len(app.routes)
    ping_operation = Operation(
        name="Ping",
        method=Method.GET,
        path="/v1/ping",
        response="pong"
    )

    health_operation = Operation(
        name="Health",
        method=Method.GET,
        path="/v1/Health",
        response="Ok"
    )

    # When
    is_ping_registered = register_endpoint(operation=ping_operation, app=app)
    is_health_registered = register_endpoint(operation=health_operation, app=app)

    # Then
    assert is_ping_registered is True
    assert is_health_registered is True
    assert app.openapi_schema is None
    assert len(app.routes) == total_routes + 2
