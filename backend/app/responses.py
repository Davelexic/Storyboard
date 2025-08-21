"""
Standardized response formats for the Cinei-Reader API.
Provides consistent success and error response structures.
"""

from typing import Any, Dict, List, Optional, Union
from datetime import datetime
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from .exceptions import CineiReaderException


class ErrorResponse(BaseModel):
    """Standard error response format."""
    
    error: str
    message: str
    timestamp: datetime
    path: Optional[str] = None
    method: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    field: Optional[str] = None
    retry_after: Optional[int] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class SuccessResponse(BaseModel):
    """Standard success response format."""
    
    success: bool = True
    message: str
    data: Optional[Any] = None
    timestamp: datetime
    meta: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class PaginatedResponse(BaseModel):
    """Standard paginated response format."""
    
    success: bool = True
    message: str
    data: List[Any]
    pagination: Dict[str, Any]
    timestamp: datetime
    meta: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class ValidationErrorResponse(BaseModel):
    """Standard validation error response format."""
    
    error: str = "VALIDATION_ERROR"
    message: str = "Validation failed"
    timestamp: datetime
    field_errors: List[Dict[str, Any]]
    path: Optional[str] = None
    method: Optional[str] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


def create_error_response(
    error_code: str,
    message: str,
    status_code: int = 400,
    details: Optional[Dict[str, Any]] = None,
    field: Optional[str] = None,
    retry_after: Optional[int] = None,
    resource_type: Optional[str] = None,
    resource_id: Optional[str] = None,
    path: Optional[str] = None,
    method: Optional[str] = None
) -> JSONResponse:
    """
    Create a standardized error response.
    
    Args:
        error_code: Error code identifier
        message: Human-readable error message
        status_code: HTTP status code
        details: Additional error details
        field: Field name if validation error
        retry_after: Retry after seconds for rate limiting
        resource_type: Type of resource if not found
        resource_id: ID of resource if not found
        path: Request path
        method: HTTP method
        
    Returns:
        JSONResponse with standardized error format
    """
    error_response = ErrorResponse(
        error=error_code,
        message=message,
        timestamp=datetime.utcnow(),
        path=path,
        method=method,
        details=details,
        field=field,
        retry_after=retry_after,
        resource_type=resource_type,
        resource_id=resource_id
    )
    
    headers = {}
    if retry_after:
        headers["Retry-After"] = str(retry_after)
    
    if error_code == "AUTH_ERROR":
        headers["WWW-Authenticate"] = "Bearer"
    
    return JSONResponse(
        status_code=status_code,
        content=error_response.dict(exclude_none=True),
        headers=headers
    )


def create_success_response(
    message: str,
    data: Optional[Any] = None,
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        message: Success message
        data: Response data
        meta: Additional metadata
        
    Returns:
        Dictionary with standardized success format
    """
    success_response = SuccessResponse(
        message=message,
        data=data,
        timestamp=datetime.utcnow(),
        meta=meta
    )
    
    return success_response.dict(exclude_none=True)


def create_paginated_response(
    message: str,
    data: List[Any],
    page: int,
    per_page: int,
    total: int,
    meta: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a standardized paginated response.
    
    Args:
        message: Success message
        data: List of items
        page: Current page number
        per_page: Items per page
        total: Total number of items
        meta: Additional metadata
        
    Returns:
        Dictionary with standardized paginated format
    """
    total_pages = (total + per_page - 1) // per_page
    
    pagination = {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": total_pages,
        "has_next": page < total_pages,
        "has_prev": page > 1
    }
    
    paginated_response = PaginatedResponse(
        message=message,
        data=data,
        pagination=pagination,
        timestamp=datetime.utcnow(),
        meta=meta
    )
    
    return paginated_response.dict(exclude_none=True)


def create_validation_error_response(
    field_errors: List[Dict[str, Any]],
    path: Optional[str] = None,
    method: Optional[str] = None
) -> JSONResponse:
    """
    Create a standardized validation error response.
    
    Args:
        field_errors: List of field-specific errors
        path: Request path
        method: HTTP method
        
    Returns:
        JSONResponse with standardized validation error format
    """
    validation_response = ValidationErrorResponse(
        message="Validation failed",
        timestamp=datetime.utcnow(),
        field_errors=field_errors,
        path=path,
        method=method
    )
    
    return JSONResponse(
        status_code=400,
        content=validation_response.dict(exclude_none=True)
    )


def format_exception_response(exc: CineiReaderException, path: Optional[str] = None, method: Optional[str] = None) -> JSONResponse:
    """
    Format a CineiReaderException into a standardized response.
    
    Args:
        exc: CineiReaderException instance
        path: Request path
        method: HTTP method
        
    Returns:
        JSONResponse with standardized error format
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
    
    return create_error_response(
        error_code=exc.error_code,
        message=exc.message,
        status_code=status_code,
        details=exc.details,
        field=getattr(exc, 'field', None),
        retry_after=getattr(exc, 'retry_after', None),
        resource_type=getattr(exc, 'resource_type', None),
        resource_id=getattr(exc, 'resource_id', None),
        path=path,
        method=method
    )


def format_pydantic_validation_errors(validation_errors: List[Dict[str, Any]], path: Optional[str] = None, method: Optional[str] = None) -> JSONResponse:
    """
    Format Pydantic validation errors into a standardized response.
    
    Args:
        validation_errors: List of Pydantic validation errors
        path: Request path
        method: HTTP method
        
    Returns:
        JSONResponse with standardized validation error format
    """
    field_errors = []
    
    for error in validation_errors:
        field = '.'.join(str(loc) for loc in error['loc']) if error['loc'] else 'unknown'
        field_errors.append({
            "field": field,
            "message": error['msg'],
            "type": error['type'],
            "value": error.get('input')
        })
    
    return create_validation_error_response(field_errors, path, method)


# Convenience functions for common response types
def not_found_response(resource_type: str, resource_id: str, path: Optional[str] = None, method: Optional[str] = None) -> JSONResponse:
    """Create a standardized 404 response."""
    return create_error_response(
        error_code="RESOURCE_NOT_FOUND",
        message=f"{resource_type.title()} not found",
        status_code=404,
        resource_type=resource_type,
        resource_id=resource_id,
        path=path,
        method=method
    )


def unauthorized_response(message: str = "Authentication required", path: Optional[str] = None, method: Optional[str] = None) -> JSONResponse:
    """Create a standardized 401 response."""
    return create_error_response(
        error_code="AUTH_ERROR",
        message=message,
        status_code=401,
        path=path,
        method=method
    )


def forbidden_response(message: str = "Access denied", path: Optional[str] = None, method: Optional[str] = None) -> JSONResponse:
    """Create a standardized 403 response."""
    return create_error_response(
        error_code="AUTHORIZATION_ERROR",
        message=message,
        status_code=403,
        path=path,
        method=method
    )


def rate_limit_response(retry_after: int, path: Optional[str] = None, method: Optional[str] = None) -> JSONResponse:
    """Create a standardized 429 response."""
    return create_error_response(
        error_code="RATE_LIMIT_ERROR",
        message="Rate limit exceeded",
        status_code=429,
        retry_after=retry_after,
        path=path,
        method=method
    )


def internal_error_response(message: str = "An unexpected error occurred", path: Optional[str] = None, method: Optional[str] = None) -> JSONResponse:
    """Create a standardized 500 response."""
    return create_error_response(
        error_code="INTERNAL_SERVER_ERROR",
        message=message,
        status_code=500,
        path=path,
        method=method
    )
