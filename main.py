import time
from contextlib import asynccontextmanager

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
import os

from common.errors import BaseHTTPError
from common.schemas import ErrorSchema
from core import cfg, injection, logging, main_router
from db.core import db  
# from auth.service import AuthService


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.configure()
    logger.info("Starting...")      
    await injection.configure()
    await db.connect()
    # # Ensure admin user exists
    # auth_service = injection.injector.get(AuthService)
    # await auth_service.ensure_admin_user_exists()
    yield
    logger.info("Shuting down...")
    await db.disconnect()


app = FastAPI(
    title=cfg.PROJECT_NAME,
    description="API for demo",
    openapi_url=f"{cfg.API_PREFIX_STR}/openapi.json",
    version=cfg.API_VERSION,
    lifespan=lifespan,
)


# origins = cfg.BACKEND_CORS_ORIGINS

# origins = os.getenv("BACKEND_CORS_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(CorrelationIdMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=1000)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(BaseHTTPError)
async def common_exception_handler(request: Request, exc: BaseHTTPError):
    """
    Common exception handler for custom BaseHTTPError
    """
    return ORJSONResponse(
        status_code=exc.code,
        headers=exc.headers,
        content=ErrorSchema(message=exc.message, data=exc.dict()).model_dump(),
    )


@app.get("/")
async def root():
    logger.info("Root")
    return {"ping": "pong"}


app.include_router(main_router, prefix=cfg.API_PREFIX_STR)