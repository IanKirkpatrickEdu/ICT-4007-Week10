from fastapi import FastAPI
from loguru import logger

from core.server import api_router
from core.settings import Settings, get_settings

import contextlib
from typing import AsyncGenerator

import fastapi
from features.dog.singletons import get_dog_service


settings: Settings = get_settings()


@contextlib.asynccontextmanager
async def app_lifespan(
    _app: fastapi.FastAPI, 
) -> AsyncGenerator:
    """Application lifespan."""
    # Startup commands can go here.
    #   if you need to say connect to a database, do it now
    dog_service = get_dog_service()
    logger.info("Application setup started!")
    await dog_service.dog_repo.setup()
    logger.info("Application setup complete!")
    yield
    # Shutdown commands go here.
    #   if you need to close database connections, do it now
    logger.info("Application teardown started!")
    await dog_service.dog_repo.teardown()
    logger.info("Application teardown complete!")


def init_app() -> fastapi.FastAPI:
    """Create FastAPI application."""

    server = fastapi.FastAPI(
        title=settings.API_NAME,
        docs_url=settings.SWAGGER_URL,
        redoc_url=settings.REDOC_URL,
        lifespan=app_lifespan,
        # terms_of_service="http://example.com/terms/",
        contact={
            "name": "<YOUR NAME HERE>",
            "email": "<YOUR EMAIL HERE>",
        },
        license_info={
            "name": "GNU General Public License v3.0",
            "identifier": "GPL-3.0-only",
            "url": "https://www.gnu.org/licenses/gpl-3.0.html",
        }
    )
    server.include_router(api_router)
    return server


app = init_app()