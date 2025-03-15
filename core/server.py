from fastapi import APIRouter
from fastapi.responses import JSONResponse

from .router_core import router as core_router
from features.dog.router import router as dog_router

# global route collection
api_router = APIRouter(default_response_class=JSONResponse)
api_router.include_router(core_router, prefix="", tags=[])
api_router.include_router(dog_router, prefix="/dogs", tags=["Dogs"])
