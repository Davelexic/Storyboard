"""
Authentication middleware for the Cinei-Reader API.
Handles JWT token validation and user authentication for protected endpoints.
"""

from typing import Optional, Dict, Any
from fastapi import Request, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
import logging

from ..db import get_session
from ..models.user import User
from ..security import decode_jwt_token

logger = logging.getLogger(__name__)

# Security scheme for JWT tokens
security = HTTPBearer(auto_error=False)


class AuthMiddleware:
    """Authentication middleware for protecting API endpoints."""
    
    def __init__(self):
        self.public_paths = {
            "/",
            "/docs",
            "/redoc",
            "/openapi.json",
            "/users/register",
            "/users/login",
            "/health",
        }
    
    def is_public_path(self, path: str) -> bool:
        """Check if the path is public (doesn't require authentication)."""
        return path in self.public_paths
    
    async def authenticate_request(self, request: Request) -> Optional[Dict[str, Any]]:
        """
        Authenticate the request and return user data if valid.
        
        Args:
            request: FastAPI request object
            
        Returns:
            User data dictionary if authenticated, None if public path
        """
        path = request.url.path
        
        # Skip authentication for public paths
        if self.is_public_path(path):
            return None
        
        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            logger.warning(f"Missing Authorization header for {path}")
            raise HTTPException(
                status_code=401,
                detail="Missing Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Validate token format
        if not auth_header.startswith("Bearer "):
            logger.warning(f"Invalid Authorization header format for {path}")
            raise HTTPException(
                status_code=401,
                detail="Invalid Authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        token = auth_header[7:]  # Remove "Bearer " prefix
        
        try:
            # Decode and validate JWT token
            payload = decode_jwt_token(token)
            user_id = payload.get("sub")
            
            if not user_id:
                logger.warning(f"Invalid token payload for {path}")
                raise HTTPException(
                    status_code=401,
                    detail="Invalid token payload",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return {"user_id": user_id, "token_payload": payload}
            
        except Exception as e:
            logger.warning(f"Token validation failed for {path}: {str(e)}")
            raise HTTPException(
                status_code=401,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Global auth middleware instance
auth_middleware = AuthMiddleware()


async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: Session = Depends(get_session)
) -> User:
    """
    Dependency to get the current authenticated user.
    
    Args:
        credentials: HTTP authorization credentials
        session: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    if not credentials:
        raise HTTPException(
            status_code=401,
            detail="Missing authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        # Decode and validate JWT token
        payload = decode_jwt_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(
                status_code=401,
                detail="Invalid token payload",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Get user from database
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        
        if not user:
            raise HTTPException(
                status_code=401,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=401,
                detail="User account is inactive",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=401,
            detail="Authentication failed",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_optional_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    session: Session = Depends(get_session)
) -> Optional[User]:
    """
    Dependency to get the current user if authenticated, None otherwise.
    
    Args:
        credentials: HTTP authorization credentials
        session: Database session
        
    Returns:
        Current authenticated user or None
    """
    if not credentials:
        return None
    
    try:
        # Decode and validate JWT token
        payload = decode_jwt_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            return None
        
        # Get user from database
        statement = select(User).where(User.id == user_id)
        user = session.exec(statement).first()
        
        if not user or not user.is_active:
            return None
        
        return user
        
    except Exception:
        return None


def require_auth(func):
    """
    Decorator to require authentication for an endpoint.
    
    Args:
        func: The endpoint function to protect
        
    Returns:
        Wrapped function with authentication
    """
    async def wrapper(*args, **kwargs):
        # This would be used in combination with FastAPI dependencies
        # The actual authentication is handled by get_current_user dependency
        return await func(*args, **kwargs)
    
    return wrapper


async def auth_middleware_func(request: Request, call_next):
    """
    FastAPI middleware function for authentication.
    
    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint function
        
    Returns:
        FastAPI response
    """
    try:
        # Authenticate request
        auth_data = await auth_middleware.authenticate_request(request)
        
        # Add authentication data to request state
        if auth_data:
            request.state.user_id = auth_data["user_id"]
            request.state.token_payload = auth_data["token_payload"]
        
        # Process the request
        response = await call_next(request)
        return response
        
    except HTTPException as e:
        # Re-raise HTTP exceptions (like 401 Unauthorized)
        raise e
    except Exception as e:
        logger.error(f"Authentication middleware error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal authentication error"
        )
