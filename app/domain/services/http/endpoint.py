from typing import Callable

from fastapi import FastAPI, APIRouter

from app.domain.models.operation import Operation, Method


def publish_endpoint(operation: Operation, app: FastAPI) -> bool:
	router_builder = get_router_builder(method=operation.method)
	router = router_builder(operation)
	try:
		app.include_router(router)
	except Exception as err:
		raise Exception(
			f"Error on building new route from operation: {operation}. Stack: {str(err)}"
		) from err
	else:
		app.openapi_schema = None  # Forces a new /docs generation
	return True


def build_get_endpoint(operation: Operation):
	router = APIRouter()

	@router.get(
		path=operation.path,
		summary=operation.summary,
		description=operation.description,
	)
	async def endpoint_execution():
		return operation.response_content

	return router


ROUTER_BUILDERS_BY_METHOD = {
	Method.GET: build_get_endpoint,
}


def get_router_builder(method: Method) -> Callable:
	try:
		router = ROUTER_BUILDERS_BY_METHOD[method]
	except KeyError as err:
		raise Exception("Error, HTTP Method not implemented!") from err
	else:
		return router
