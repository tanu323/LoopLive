from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from contextlib import asynccontextmanager
from app.db.mongo import get_database, close_mongo_connection
import uuid
import structlog

from app.core.config import settings, get_config
from app.core.logging import setup_logging, get_logger
setup_logging()

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.exceptions import AppException
from app.core.handlers import (
    app_exception_handler,
    http_exception_handler,
    validation_exception_handler,
    pydantic_validation_exception_handler,
    generic_exception_handler
)
from app.api.auth.router import router as auth_router
from app.api.video import router as video_router
from app.api.comment.router import router as comment_router
from app.api.like.router import router as like_router
from app.api.user.router import router as user_router
from app.api.websocket.router import router as websocket_router
from app.api.deps import initialize_dependencies

config = get_config()

@asynccontextmanager
async def lifespan(app: FastAPI):

    logger = get_logger(__name__)

    # Startup actions
    try:
        db = get_database()
        await db.command("ping")  # Verifies connection is working
        logger.info("✅ MongoDB connected successfully.")

        yield  # Application is running
    
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

    finally:
        await close_mongo_connection()
        logger.info("MongoDB connection closed.")

app = FastAPI(
    title="Reels API",
    description="Backend API for Short Video Sharing App",
    version="1.0.0",
    lifespan=lifespan,
)

# --- Exception Handlers ---
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(ValidationError, pydantic_validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)


# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Request ID Middleware ---
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(request_id=request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# --- API Routes ---
app.include_router(auth_router, prefix=f"{config.API_PREFIX}/auth", tags=["auth"])
app.include_router(video_router, prefix=f"{config.API_PREFIX}/videos", tags=["videos"])
app.include_router(comment_router, prefix=f"{config.API_PREFIX}/comments", tags=["comments"])
app.include_router(like_router, prefix=f"{config.API_PREFIX}/likes", tags=["likes"])
app.include_router(user_router, prefix=f"{config.API_PREFIX}/users", tags=["users"])
app.include_router(websocket_router, prefix=f"{config.API_PREFIX}/ws", tags=["websockets"])

# --- Health Check Endpoint ---
@app.get("/health")
async def health_check():
    return {"status": "healthy"}
