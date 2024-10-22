from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi import HTTPException

from app.api.mappers.operation import CreateOperationMapper
from app.api.schemas.operation import RegisteredEndpoint, CreateEndpointRequest
from app.core.container.app import AppContainer
from app.domain.services.http.endpoint import publish_endpoint
from app.domain.services.operation.register_operation import CreateOperationService

router = APIRouter(prefix="/operation", tags=["Operation"])


@router.post(
	path="/register",
	responses={
		status.HTTP_201_CREATED: {"description": "Register new operation OK"},
		status.HTTP_400_BAD_REQUEST: {"description": "Register new operation Failed"},
		status.HTTP_500_INTERNAL_SERVER_ERROR: {
			"description": "Register new operation Failed unexpectedly"
		},
	},
	response_model=RegisteredEndpoint,
	status_code=status.HTTP_201_CREATED,
)
@inject
async def register_operation(
	request: CreateEndpointRequest,
	create_operation_service: CreateOperationService = Depends(
		Provide[AppContainer.create_operation_service]
	),
):
	from app.main import app

	try:
		operation_create = CreateOperationMapper.mapping(request=request)

		operation = await create_operation_service.create(operation_create=operation_create)
		publish_endpoint(operation=operation, app=app)
	except Exception as err:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(err),
		) from err

	return RegisteredEndpoint(endpoint=operation.path, uuid=operation.uuid, status="registered")
