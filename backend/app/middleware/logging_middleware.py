"""
Logging middleware for the Cinei-Reader API.
Automatically logs HTTP requests and responses with timing information.
"""

import time
from fastapi import Request
from fastapi.responses import Response

from ..logging_config import request_logger


async def logging_middleware(request: Request, call_next):
    """
    Middleware to log HTTP requests and responses.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint function
        
    Returns:
        FastAPI response
    """
    start_time = time.time()
    
    # Log request start
    request_logger.log_request(
        request=request,
        response=None,
        duration=None,
        error=None
    )
    
    try:
        # Process the request
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log successful response
        request_logger.log_request(
            request=request,
            response=response,
            duration=duration,
            error=None
        )
        
        return response
        
    except Exception as e:
        # Calculate duration
        duration = time.time() - start_time
        
        # Log error
        request_logger.log_request(
            request=request,
            response=None,
            duration=duration,
            error=str(e)
        )
        
        # Re-raise the exception
        raise
