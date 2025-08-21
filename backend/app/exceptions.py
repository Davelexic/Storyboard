"""
Custom exception classes for the Cinei-Reader API.
Provides specific, meaningful error types to replace generic exception handling.
"""

from typing import Optional, Dict, Any
from fastapi import HTTPException


class CineiReaderException(Exception):
    """Base exception class for Cinei-Reader application."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.details = details or {}


class AuthenticationError(CineiReaderException):
    """Raised when authentication fails."""
    
    def __init__(self, message: str = "Authentication failed", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTH_ERROR", details)


class AuthorizationError(CineiReaderException):
    """Raised when user is not authorized to perform an action."""
    
    def __init__(self, message: str = "Access denied", details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "AUTHORIZATION_ERROR", details)


class ValidationError(CineiReaderException):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "VALIDATION_ERROR", details)
        self.field = field


class FileProcessingError(CineiReaderException):
    """Raised when file processing fails."""
    
    def __init__(self, message: str, file_type: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "FILE_PROCESSING_ERROR", details)
        self.file_type = file_type


class BookProcessingError(CineiReaderException):
    """Raised when book processing fails."""
    
    def __init__(self, message: str, book_id: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "BOOK_PROCESSING_ERROR", details)
        self.book_id = book_id


class DatabaseError(CineiReaderException):
    """Raised when database operations fail."""
    
    def __init__(self, message: str, operation: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "DATABASE_ERROR", details)
        self.operation = operation


class RateLimitError(CineiReaderException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, message: str = "Rate limit exceeded", retry_after: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "RATE_LIMIT_ERROR", details)
        self.retry_after = retry_after


class ServiceUnavailableError(CineiReaderException):
    """Raised when a required service is unavailable."""
    
    def __init__(self, message: str, service: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "SERVICE_UNAVAILABLE", details)
        self.service = service


class ConfigurationError(CineiReaderException):
    """Raised when there's a configuration issue."""
    
    def __init__(self, message: str, config_key: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "CONFIGURATION_ERROR", details)
        self.config_key = config_key


class ResourceNotFoundError(CineiReaderException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, message: str, resource_type: Optional[str] = None, resource_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "RESOURCE_NOT_FOUND", details)
        self.resource_type = resource_type
        self.resource_id = resource_id


class ConflictError(CineiReaderException):
    """Raised when there's a conflict with existing data."""
    
    def __init__(self, message: str, conflict_type: Optional[str] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "CONFLICT_ERROR", details)
        self.conflict_type = conflict_type


class ExternalServiceError(CineiReaderException):
    """Raised when an external service call fails."""
    
    def __init__(self, message: str, service: Optional[str] = None, status_code: Optional[int] = None, details: Optional[Dict[str, Any]] = None):
        super().__init__(message, "EXTERNAL_SERVICE_ERROR", details)
        self.service = service
        self.status_code = status_code


def convert_to_http_exception(exc: CineiReaderException) -> HTTPException:
    """
    Convert a CineiReaderException to an HTTPException with appropriate status code.
    
    Args:
        exc: CineiReaderException instance
        
    Returns:
        HTTPException with appropriate status code and details
    """
    status_code_map = {
        "AUTH_ERROR": 401,
        "AUTHORIZATION_ERROR": 403,
        "VALIDATION_ERROR": 400,
        "FILE_PROCESSING_ERROR": 400,
        "BOOK_PROCESSING_ERROR": 400,
        "DATABASE_ERROR": 500,
        "RATE_LIMIT_ERROR": 429,
        "SERVICE_UNAVAILABLE": 503,
        "CONFIGURATION_ERROR": 500,
        "RESOURCE_NOT_FOUND": 404,
        "CONFLICT_ERROR": 409,
        "EXTERNAL_SERVICE_ERROR": 502,
    }
    
    status_code = status_code_map.get(exc.error_code, 500)
    
    # Build response content
    content = {
        "error": exc.error_code,
        "message": exc.message,
    }
    
    if exc.details:
        content["details"] = exc.details
    
    # Add specific fields based on exception type
    if hasattr(exc, 'field') and exc.field:
        content["field"] = exc.field
    
    if hasattr(exc, 'retry_after') and exc.retry_after:
        content["retry_after"] = exc.retry_after
    
    if hasattr(exc, 'resource_type') and exc.resource_type:
        content["resource_type"] = exc.resource_type
    
    if hasattr(exc, 'resource_id') and exc.resource_id:
        content["resource_id"] = exc.resource_id
    
    # Add headers for specific error types
    headers = {}
    if isinstance(exc, AuthenticationError):
        headers["WWW-Authenticate"] = "Bearer"
    elif isinstance(exc, RateLimitError):
        if exc.retry_after:
            headers["Retry-After"] = str(exc.retry_after)
    
    return HTTPException(
        status_code=status_code,
        detail=content,
        headers=headers
    )


def handle_exception(exc: Exception) -> HTTPException:
    """
    Handle any exception and convert it to an appropriate HTTPException.
    
    Args:
        exc: Any exception
        
    Returns:
        HTTPException with appropriate status code and details
    """
    if isinstance(exc, CineiReaderException):
        return convert_to_http_exception(exc)
    
    if isinstance(exc, HTTPException):
        return exc
    
    # Handle other common exceptions
    if isinstance(exc, ValueError):
        return HTTPException(status_code=400, detail={
            "error": "VALIDATION_ERROR",
            "message": str(exc)
        })
    
    if isinstance(exc, FileNotFoundError):
        return HTTPException(status_code=404, detail={
            "error": "RESOURCE_NOT_FOUND",
            "message": "File not found",
            "details": {"file": str(exc)}
        })
    
    if isinstance(exc, PermissionError):
        return HTTPException(status_code=403, detail={
            "error": "AUTHORIZATION_ERROR",
            "message": "Permission denied",
            "details": {"reason": str(exc)}
        })
    
    # Default to internal server error
    return HTTPException(status_code=500, detail={
        "error": "INTERNAL_SERVER_ERROR",
        "message": "An unexpected error occurred"
    })
