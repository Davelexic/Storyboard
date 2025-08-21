"""
Input sanitization utilities for the Cinei-Reader API.
Provides functions to clean and validate user input to prevent injection attacks.
"""

import re
import html
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote, unquote
import unicodedata


class SanitizationError(Exception):
    """Raised when input fails sanitization."""
    pass


def sanitize_string(value: str, max_length: int = 1000, allow_html: bool = False) -> str:
    """
    Sanitize a string input.
    
    Args:
        value: The string to sanitize
        max_length: Maximum allowed length
        allow_html: Whether to allow HTML tags (default: False)
    
    Returns:
        Sanitized string
    
    Raises:
        SanitizationError: If input is invalid
    """
    if not isinstance(value, str):
        raise SanitizationError("Input must be a string")
    
    # Remove null bytes and control characters
    value = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)
    
    # Normalize unicode
    value = unicodedata.normalize('NFKC', value)
    
    # Trim whitespace
    value = value.strip()
    
    # Check length
    if len(value) > max_length:
        raise SanitizationError(f"String too long. Maximum length: {max_length}")
    
    # HTML escape if not allowed
    if not allow_html:
        value = html.escape(value)
    
    return value


def sanitize_email(email: str) -> str:
    """
    Sanitize and validate email address.
    
    Args:
        email: Email address to sanitize
    
    Returns:
        Sanitized email address
    
    Raises:
        SanitizationError: If email is invalid
    """
    email = sanitize_string(email, max_length=254, allow_html=False).lower()
    
    # Basic email validation
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    if not email_pattern.match(email):
        raise SanitizationError("Invalid email format")
    
    return email


def sanitize_password(password: str, min_length: int = 8) -> str:
    """
    Sanitize and validate password.
    
    Args:
        password: Password to sanitize
        min_length: Minimum password length
    
    Returns:
        Sanitized password
    
    Raises:
        SanitizationError: If password is invalid
    """
    if not isinstance(password, str):
        raise SanitizationError("Password must be a string")
    
    # Check length
    if len(password) < min_length:
        raise SanitizationError(f"Password too short. Minimum length: {min_length}")
    
    if len(password) > 128:
        raise SanitizationError("Password too long. Maximum length: 128")
    
    # Remove null bytes and control characters
    password = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', password)
    
    return password


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal attacks.
    
    Args:
        filename: Filename to sanitize
    
    Returns:
        Sanitized filename
    
    Raises:
        SanitizationError: If filename is invalid
    """
    if not isinstance(filename, str):
        raise SanitizationError("Filename must be a string")
    
    # Remove path traversal attempts
    dangerous_patterns = [
        r'\.\.',  # Directory traversal
        r'/',     # Path separators
        r'\\',    # Windows path separators
        r'[<>:"|?*]',  # Invalid filename characters
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, filename):
            raise SanitizationError("Invalid filename characters detected")
    
    # Limit length
    if len(filename) > 255:
        raise SanitizationError("Filename too long")
    
    return filename.strip()


def sanitize_integer(value: Any, min_value: Optional[int] = None, max_value: Optional[int] = None) -> int:
    """
    Sanitize and validate integer input.
    
    Args:
        value: Value to convert to integer
        min_value: Minimum allowed value
        max_value: Maximum allowed value
    
    Returns:
        Sanitized integer
    
    Raises:
        SanitizationError: If value is invalid
    """
    try:
        if isinstance(value, str):
            # Remove whitespace and check for valid integer
            value = value.strip()
            if not re.match(r'^-?\d+$', value):
                raise SanitizationError("Invalid integer format")
        
        result = int(value)
        
        if min_value is not None and result < min_value:
            raise SanitizationError(f"Value too small. Minimum: {min_value}")
        
        if max_value is not None and result > max_value:
            raise SanitizationError(f"Value too large. Maximum: {max_value}")
        
        return result
        
    except (ValueError, TypeError):
        raise SanitizationError("Invalid integer value")


def sanitize_float(value: Any, min_value: Optional[float] = None, max_value: Optional[float] = None) -> float:
    """
    Sanitize and validate float input.
    
    Args:
        value: Value to convert to float
        min_value: Minimum allowed value
        max_value: Maximum allowed value
    
    Returns:
        Sanitized float
    
    Raises:
        SanitizationError: If value is invalid
    """
    try:
        if isinstance(value, str):
            # Remove whitespace and check for valid float
            value = value.strip()
            if not re.match(r'^-?\d*\.?\d+$', value):
                raise SanitizationError("Invalid float format")
        
        result = float(value)
        
        if min_value is not None and result < min_value:
            raise SanitizationError(f"Value too small. Minimum: {min_value}")
        
        if max_value is not None and result > max_value:
            raise SanitizationError(f"Value too large. Maximum: {max_value}")
        
        return result
        
    except (ValueError, TypeError):
        raise SanitizationError("Invalid float value")


def sanitize_boolean(value: Any) -> bool:
    """
    Sanitize and validate boolean input.
    
    Args:
        value: Value to convert to boolean
    
    Returns:
        Sanitized boolean
    
    Raises:
        SanitizationError: If value is invalid
    """
    if isinstance(value, bool):
        return value
    
    if isinstance(value, str):
        value = value.lower().strip()
        if value in ('true', '1', 'yes', 'on'):
            return True
        elif value in ('false', '0', 'no', 'off'):
            return False
    
    if isinstance(value, int):
        if value == 1:
            return True
        elif value == 0:
            return False
    
    raise SanitizationError("Invalid boolean value")


def sanitize_dict(data: Dict[str, Any], allowed_keys: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Sanitize dictionary input.
    
    Args:
        data: Dictionary to sanitize
        allowed_keys: List of allowed keys (if None, all keys are allowed)
    
    Returns:
        Sanitized dictionary
    
    Raises:
        SanitizationError: If data is invalid
    """
    if not isinstance(data, dict):
        raise SanitizationError("Input must be a dictionary")
    
    result = {}
    
    for key, value in data.items():
        # Sanitize key
        if not isinstance(key, str):
            raise SanitizationError("Dictionary keys must be strings")
        
        key = sanitize_string(key, max_length=100)
        
        # Check if key is allowed
        if allowed_keys is not None and key not in allowed_keys:
            raise SanitizationError(f"Key '{key}' not allowed")
        
        # Sanitize value based on type
        if isinstance(value, str):
            result[key] = sanitize_string(value)
        elif isinstance(value, int):
            result[key] = sanitize_integer(value)
        elif isinstance(value, float):
            result[key] = sanitize_float(value)
        elif isinstance(value, bool):
            result[key] = sanitize_boolean(value)
        elif isinstance(value, dict):
            result[key] = sanitize_dict(value)
        elif isinstance(value, list):
            result[key] = sanitize_list(value)
        else:
            raise SanitizationError(f"Unsupported value type for key '{key}'")
    
    return result


def sanitize_list(data: List[Any], max_length: int = 1000) -> List[Any]:
    """
    Sanitize list input.
    
    Args:
        data: List to sanitize
        max_length: Maximum allowed list length
    
    Returns:
        Sanitized list
    
    Raises:
        SanitizationError: If data is invalid
    """
    if not isinstance(data, list):
        raise SanitizationError("Input must be a list")
    
    if len(data) > max_length:
        raise SanitizationError(f"List too long. Maximum length: {max_length}")
    
    result = []
    for item in data:
        if isinstance(item, str):
            result.append(sanitize_string(item))
        elif isinstance(item, int):
            result.append(sanitize_integer(item))
        elif isinstance(item, float):
            result.append(sanitize_float(item))
        elif isinstance(item, bool):
            result.append(sanitize_boolean(item))
        elif isinstance(item, dict):
            result.append(sanitize_dict(item))
        elif isinstance(item, list):
            result.append(sanitize_list(item))
        else:
            raise SanitizationError("Unsupported list item type")
    
    return result


def sanitize_json_string(json_str: str) -> str:
    """
    Sanitize JSON string input.
    
    Args:
        json_str: JSON string to sanitize
    
    Returns:
        Sanitized JSON string
    
    Raises:
        SanitizationError: If JSON is invalid
    """
    json_str = sanitize_string(json_str, max_length=10000)
    
    # Basic JSON validation (check for balanced braces/brackets)
    stack = []
    for char in json_str:
        if char in '{[':
            stack.append(char)
        elif char in ']}':
            if not stack:
                raise SanitizationError("Invalid JSON: unmatched closing bracket")
            if (char == '}' and stack[-1] != '{') or (char == ']' and stack[-1] != '['):
                raise SanitizationError("Invalid JSON: mismatched brackets")
            stack.pop()
    
    if stack:
        raise SanitizationError("Invalid JSON: unmatched opening bracket")
    
    return json_str


# Convenience functions for common sanitization patterns
def sanitize_user_input(value: str, field_name: str = "input") -> str:
    """Sanitize general user input."""
    try:
        return sanitize_string(value, max_length=500)
    except SanitizationError as e:
        raise SanitizationError(f"Invalid {field_name}: {str(e)}")


def sanitize_search_query(query: str) -> str:
    """Sanitize search query input."""
    try:
        return sanitize_string(query, max_length=200)
    except SanitizationError as e:
        raise SanitizationError(f"Invalid search query: {str(e)}")


def sanitize_url(url: str) -> str:
    """Sanitize URL input."""
    try:
        url = sanitize_string(url, max_length=2000)
        # Basic URL validation
        if not url.startswith(('http://', 'https://', 'ftp://')):
            raise SanitizationError("URL must start with http://, https://, or ftp://")
        return url
    except SanitizationError as e:
        raise SanitizationError(f"Invalid URL: {str(e)}")
