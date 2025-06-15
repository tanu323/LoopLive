# app/core/handlers.py

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import ValidationError
from app.core.exceptions import AppException
import traceback
import logging

logger = logging.getLogger(__name__)


async def app_exception_handler(request: Request, exc: AppException):
    logger.warning(f"AppException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "Application Error", "message": exc.detail}
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    logger.warning(f"HTTPException: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "HTTP Error", "message": exc.detail}
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.warning("Validation error", exc_info=exc)
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "details": exc.errors()
        }
    )


async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    logger.warning("Pydantic model validation error", exc_info=exc)
    return JSONResponse(
        status_code=422,
        content={
            "error": "Model Validation Error",
            "details": exc.errors()
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "trace": traceback.format_exc()
        }
    )
