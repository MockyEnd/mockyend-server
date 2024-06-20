from fastapi import APIRouter, status, HTTPException

from app.api.mappers.operation import OperationMapper
from app.api.schemas.operation import RegisteredEndpoint, CreateEndpointRequest
from app.domain.services.http.endpoint import register_endpoint

router = APIRouter(prefix="/operation", tags=["Operation"])


@router.post(
    path="/register",
    responses={
        status.HTTP_201_CREATED: {"description": "Register new operation OK"},
        status.HTTP_400_BAD_REQUEST: {"description": "Register new operation Failed"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Register new operation Failed unexpectedly"},
    },
    response_model=RegisteredEndpoint,
    status_code=status.HTTP_201_CREATED,
)
async def register_operation(request: CreateEndpointRequest):
    from app.main import app

    try:
        operation = OperationMapper.mapping(request=request)
        register_endpoint(operation=operation, app=app)
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(err),
        ) from err

    return RegisteredEndpoint(
        endpoint=operation.path,
        status="registered"
    )

