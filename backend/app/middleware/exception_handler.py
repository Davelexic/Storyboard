"""
Global exception handler middleware for the Cinei-Reader API.
Catches and properly formats all exceptions using custom exception classes.
"""

import logging
from fastapi import Request
from fastapi.responses import JSONResponse

from ..exceptions import handle_exception, CineiReaderException

logger = logging.getLogger(__name__)


async def exception_handler_middleware(request: Request, call_next):
    """
    Global exception handler middleware.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint function
        
    Returns:
        FastAPI response
    """
    try:
        # Process the request
        response = await call_next(request)
        return response
        
    except Exception as exc:
        # Log the exception
        logger.error(f"Unhandled exception in {request.url.path}: {str(exc)}", exc_info=True)
        
        # Convert to HTTPException
        http_exc = handle_exception(exc)
        
        # Return JSON response
        return JSONResponse(
            status_code=http_exc.status_code,
            content=http_exc.detail,
            headers=http_exc.headers
        )


def setup_exception_handlers(app):
    """
    Setup exception handlers for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    
    @app.exception_handler(CineiReaderException)
    async def cinei_reader_exception_handler(request: Request, exc: CineiReaderException):
        """Handle CineiReaderException instances."""
        logger.warning(f"CineiReaderException in {request.url.path}: {exc.message}")
        
        from ..exceptions import convert_to_http_exception
        http_exc = convert_to_http_exception(exc)
        
        return JSONResponse(
            status_code=http_exc.status_code,
            content=http_exc.detail,
            headers=http_exc.headers
        )
    
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """Handle ValueError instances."""
        logger.warning(f"ValueError in {request.url.path}: {str(exc)}")
        
        return JSONResponse(
            status_code=400,
            content={
                "error": "VALIDATION_ERROR",
                "message": str(exc)
            }
        )
    
    @app.exception_handler(FileNotFoundError)
    async def file_not_found_handler(request: Request, exc: FileNotFoundError):
        """Handle FileNotFoundError instances."""
        logger.warning(f"FileNotFoundError in {request.url.path}: {str(exc)}")
        
        return JSONResponse(
            status_code=404,
            content={
                "error": "RESOURCE_NOT_FOUND",
                "message": "File not found",
                "details": {"file": str(exc)}
            }
        )
    
    @app.exception_handler(PermissionError)
    async def permission_error_handler(request: Request, exc: PermissionError):
        """Handle PermissionError instances."""
        logger.warning(f"PermissionError in {request.url.path}: {str(exc)}")
        
        return JSONResponse(
            status_code=403,
            content={
                "error": "AUTHORIZATION_ERROR",
                "message": "Permission denied",
                "details": {"reason": str(exc)}
            }
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handle all other exceptions."""
        logger.error(f"Unhandled exception in {request.url.path}: {str(exc)}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred"
            }
        )
