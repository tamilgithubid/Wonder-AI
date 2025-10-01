"""
Global exception handlers for the FastAPI application
Provides consistent error responses and logging
"""

import traceback
from typing import Any, Dict
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from loguru import logger

from app.core.config import settings


class WonderAIException(Exception):
    """Base exception for WonderAI application"""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500, 
        error_code: str = "INTERNAL_ERROR",
        details: Dict[str, Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(message)


class ValidationException(WonderAIException):
    """Exception for validation errors"""
    
    def __init__(self, message: str, details: Dict[str, Any] = None):
        super().__init__(
            message=message,
            status_code=422,
            error_code="VALIDATION_ERROR",
            details=details
        )


class AuthenticationException(WonderAIException):
    """Exception for authentication errors"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=401,
            error_code="AUTHENTICATION_ERROR"
        )


class AuthorizationException(WonderAIException):
    """Exception for authorization errors"""
    
    def __init__(self, message: str = "Access denied"):
        super().__init__(
            message=message,
            status_code=403,
            error_code="AUTHORIZATION_ERROR"
        )


class ResourceNotFoundException(WonderAIException):
    """Exception for resource not found errors"""
    
    def __init__(self, message: str = "Resource not found"):
        super().__init__(
            message=message,
            status_code=404,
            error_code="RESOURCE_NOT_FOUND"
        )


class ExternalServiceException(WonderAIException):
    """Exception for external service errors (OpenAI, etc.)"""
    
    def __init__(self, message: str, service: str = "unknown"):
        super().__init__(
            message=message,
            status_code=502,
            error_code="EXTERNAL_SERVICE_ERROR",
            details={"service": service}
        )


class RateLimitException(WonderAIException):
    """Exception for rate limiting"""
    
    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(
            message=message,
            status_code=429,
            error_code="RATE_LIMIT_EXCEEDED"
        )


def create_error_response(
    status_code: int,
    message: str,
    error_code: str = "UNKNOWN_ERROR",
    details: Dict[str, Any] = None,
    request_id: str = None
) -> JSONResponse:
    """Create standardized error response"""
    
    error_response = {
        "error": {
            "message": message,
            "code": error_code,
            "status_code": status_code,
        }
    }
    
    if details:
        error_response["error"]["details"] = details
    
    if request_id:
        error_response["error"]["request_id"] = request_id
    
    if settings.DEBUG:
        error_response["error"]["timestamp"] = None  # Will be added by FastAPI
    
    return JSONResponse(
        status_code=status_code,
        content=error_response
    )


async def wonderai_exception_handler(request: Request, exc: WonderAIException):
    """Handler for custom WonderAI exceptions"""
    
    logger.error(
        f"WonderAI Exception: {exc.error_code} - {exc.message}",
        extra={
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "details": exc.details,
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return create_error_response(
        status_code=exc.status_code,
        message=exc.message,
        error_code=exc.error_code,
        details=exc.details if settings.DEBUG else None
    )


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler for HTTP exceptions"""
    
    logger.warning(
        f"HTTP Exception: {exc.status_code} - {exc.detail}",
        extra={
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return create_error_response(
        status_code=exc.status_code,
        message=exc.detail,
        error_code="HTTP_ERROR"
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler for request validation errors"""
    
    logger.warning(
        f"Validation Error: {exc.errors()}",
        extra={
            "errors": exc.errors(),
            "path": request.url.path,
            "method": request.method,
        }
    )
    
    return create_error_response(
        status_code=422,
        message="Request validation failed",
        error_code="VALIDATION_ERROR",
        details={"errors": exc.errors()} if settings.DEBUG else None
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handler for unexpected exceptions"""
    
    logger.error(
        f"Unexpected Exception: {str(exc)}",
        extra={
            "exception_type": type(exc).__name__,
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc() if settings.DEBUG else None,
        }
    )
    
    return create_error_response(
        status_code=500,
        message="Internal server error" if not settings.DEBUG else str(exc),
        error_code="INTERNAL_SERVER_ERROR",
        details={"traceback": traceback.format_exc()} if settings.DEBUG else None
    )


def setup_exception_handlers(app: FastAPI):
    """Setup all exception handlers for the FastAPI app"""
    
    app.add_exception_handler(WonderAIException, wonderai_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("🛡️ Exception handlers configured")
