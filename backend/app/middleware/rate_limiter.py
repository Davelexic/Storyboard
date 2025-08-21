"""
Rate limiting middleware for the Cinei-Reader API.
Provides protection against abuse and ensures fair usage of the API.
"""

import time
from typing import Dict, Tuple, Optional
from collections import defaultdict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter.
    
    For production, consider using Redis or a dedicated rate limiting service.
    """
    
    def __init__(self):
        self.requests: Dict[str, list] = defaultdict(list)
        self.limits = {
            "default": {"requests": 100, "window": 60},  # 100 requests per minute
            "auth": {"requests": 5, "window": 60},       # 5 auth attempts per minute
            "upload": {"requests": 10, "window": 300},   # 10 uploads per 5 minutes
            "analytics": {"requests": 50, "window": 60}, # 50 analytics events per minute
        }
    
    def _get_client_ip(self, request: Request) -> str:
        """Extract client IP address from request."""
        # Check for forwarded headers (when behind proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to direct connection
        return request.client.host if request.client else "unknown"
    
    def _get_rate_limit_key(self, request: Request, endpoint_type: str = "default") -> str:
        """Generate rate limit key for the request."""
        client_ip = self._get_client_ip(request)
        return f"{client_ip}:{endpoint_type}"
    
    def _cleanup_old_requests(self, key: str, window: int):
        """Remove requests older than the window."""
        current_time = time.time()
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if current_time - req_time < window
        ]
    
    def is_allowed(self, request: Request, endpoint_type: str = "default") -> Tuple[bool, Dict]:
        """
        Check if the request is allowed based on rate limits.
        
        Args:
            request: FastAPI request object
            endpoint_type: Type of endpoint for different rate limits
        
        Returns:
            Tuple of (is_allowed, rate_limit_info)
        """
        key = self._get_rate_limit_key(request, endpoint_type)
        limit_config = self.limits.get(endpoint_type, self.limits["default"])
        
        # Clean up old requests
        self._cleanup_old_requests(key, limit_config["window"])
        
        # Check if limit exceeded
        current_requests = len(self.requests[key])
        is_allowed = current_requests < limit_config["requests"]
        
        if is_allowed:
            # Add current request
            self.requests[key].append(time.time())
        
        # Calculate remaining requests and reset time
        remaining = max(0, limit_config["requests"] - current_requests - (1 if is_allowed else 0))
        reset_time = int(time.time() + limit_config["window"])
        
        rate_limit_info = {
            "limit": limit_config["requests"],
            "remaining": remaining,
            "reset": reset_time,
            "window": limit_config["window"]
        }
        
        return is_allowed, rate_limit_info
    
    def get_rate_limit_headers(self, rate_limit_info: Dict) -> Dict[str, str]:
        """Generate rate limit headers for response."""
        return {
            "X-RateLimit-Limit": str(rate_limit_info["limit"]),
            "X-RateLimit-Remaining": str(rate_limit_info["remaining"]),
            "X-RateLimit-Reset": str(rate_limit_info["reset"]),
            "X-RateLimit-Window": str(rate_limit_info["window"])
        }


# Global rate limiter instance
rate_limiter = RateLimiter()


async def rate_limit_middleware(request: Request, call_next):
    """
    FastAPI middleware for rate limiting.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint function
    
    Returns:
        FastAPI response
    """
    # Determine endpoint type based on path
    path = request.url.path
    
    if path.startswith("/users/login") or path.startswith("/users/register"):
        endpoint_type = "auth"
    elif path.startswith("/books/upload"):
        endpoint_type = "upload"
    elif path.startswith("/analytics"):
        endpoint_type = "analytics"
    else:
        endpoint_type = "default"
    
    # Check rate limit
    is_allowed, rate_limit_info = rate_limiter.is_allowed(request, endpoint_type)
    
    if not is_allowed:
        logger.warning(f"Rate limit exceeded for {request.client.host} on {path}")
        
        # Return rate limit exceeded response
        headers = rate_limiter.get_rate_limit_headers(rate_limit_info)
        headers["Retry-After"] = str(rate_limit_info["window"])
        
        return JSONResponse(
            status_code=429,
            content={
                "error": "Rate limit exceeded",
                "message": f"Too many requests. Limit: {rate_limit_info['limit']} per {rate_limit_info['window']} seconds",
                "retry_after": rate_limit_info["window"]
            },
            headers=headers
        )
    
    # Process the request
    response = await call_next(request)
    
    # Add rate limit headers to response
    headers = rate_limiter.get_rate_limit_headers(rate_limit_info)
    for key, value in headers.items():
        response.headers[key] = value
    
    return response


def get_rate_limit_info(request: Request, endpoint_type: str = "default") -> Dict:
    """
    Get current rate limit information for a request.
    
    Args:
        request: FastAPI request object
        endpoint_type: Type of endpoint
    
    Returns:
        Rate limit information dictionary
    """
    _, rate_limit_info = rate_limiter.is_allowed(request, endpoint_type)
    return rate_limit_info
