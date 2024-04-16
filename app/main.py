import logging
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, HTTPException
from fastapi.exception_handlers import http_exception_handler

from app.config import setup_logging
from app.routers.pokemon import router as pokemon_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(CorrelationIdMiddleware)

app.include_router(pokemon_router)

logger = logging.getLogger(__name__)


@app.exception_handler(HTTPException)
async def http_exception_handler_logger(request, exc):
    logger.error(f"HTTPException: {exc.status_code} {exc.detail}")
    return await http_exception_handler(request, exc)


@app.get("/health")
async def health_check():
    logger.info("Health check")
    return {"status": "ok"}
