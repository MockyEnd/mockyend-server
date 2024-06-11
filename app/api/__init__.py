from fastapi import APIRouter

from app.api.app_router import router as app_router
from app.api.v1.operation import router as operation_router

router = APIRouter(prefix="")

router.include_router(app_router)
router.include_router(operation_router)
