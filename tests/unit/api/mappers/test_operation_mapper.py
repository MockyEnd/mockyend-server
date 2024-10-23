from app.api.mappers.operation import CreateOperationMapper
from app.domain.models.operation import DataType


def test_create_operation_mapper(create_endpoint_request):
	# When
	operation = CreateOperationMapper.mapping(request=create_endpoint_request)

	# Then
	assert operation.name == create_endpoint_request.name
	assert operation.summary == create_endpoint_request.summary
	assert operation.description == create_endpoint_request.description
	assert operation.method == create_endpoint_request.method
	assert operation.path == create_endpoint_request.path
	assert operation.response_type == DataType.LIST
	assert isinstance(operation.response_content, list)
	assert len(operation.response_content) == len(
		create_endpoint_request.response.list_value.values
	)
