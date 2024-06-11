from fastapi import APIRouter, status
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    message: str


@router.get(
    path="/health",
    responses={
        status.HTTP_200_OK: {"description": "Health response OK"}
    },
    response_model=HealthResponse,
)
async def health():
    return HealthResponse(message="It's running!")


class APIMock(BaseModel):
    method: str
    path: str
    request: str
    response: str


class RegisteredEndpoint(BaseModel):
    endpoint: str
    status: str


@router.get(
    path="/prepare_mock",
    responses={
        status.HTTP_200_OK: {"description": "Health response OK"}
    },
    response_model=None,
)
async def prepare_mock():
    api_mock = APIMock(
        method="GET",
        path="/rafael",
        request="",
        response="Funcionou!"
    )

    result = await register_endpoint(api_mock=api_mock)
    return RegisteredEndpoint(
        endpoint=api_mock.path,
        status=result
    )


async def register_endpoint(api_mock: APIMock):
    from app.main import app

    new_router = APIRouter()

    @new_router.get(
        path=api_mock.path,
        summary="Test",
        description="Description Test",
    )
    async def _():
        return api_mock.response

    app.include_router(new_router)

    return "registered"
