from app.api.mappers.operation import OperationMapper


def test_operation_mapper(create_endpoint_request):
    # When
    operation = OperationMapper.mapping(request=create_endpoint_request)

    # Then
    assert operation.name == create_endpoint_request.name
    assert operation.summary == create_endpoint_request.summary
    assert operation.description == create_endpoint_request.description
    assert operation.method == create_endpoint_request.method
    assert operation.path == create_endpoint_request.path
    assert isinstance(operation.response, list)
    assert len(operation.response) == len(create_endpoint_request.response.list_value.values)
