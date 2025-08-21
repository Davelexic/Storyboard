"""
Comprehensive input validation for the Cinei-Reader API.
Provides detailed validation rules and schemas beyond basic sanitization.
"""

import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta
from pydantic import BaseModel, validator, ValidationError as PydanticValidationError

from .exceptions import ValidationError
from .utils.sanitization import sanitize_string, sanitize_email, sanitize_password


class ValidationSchema:
    """Base validation schema with common validation methods."""
    
    @staticmethod
    def validate_email(email: str) -> str:
        """Validate email format and domain."""
        try:
            sanitized_email = sanitize_email(email)
            
            # Additional domain validation
            domain = sanitized_email.split('@')[1]
            if len(domain) < 3:
                raise ValidationError("Invalid email domain", field="email")
            
            # Check for common disposable email domains
            disposable_domains = {
                'tempmail.org', '10minutemail.com', 'guerrillamail.com',
                'mailinator.com', 'throwaway.email', 'temp-mail.org'
            }
            if domain.lower() in disposable_domains:
                raise ValidationError("Disposable email addresses are not allowed", field="email")
            
            return sanitized_email
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Invalid email format: {str(e)}", field="email")
    
    @staticmethod
    def validate_password(password: str) -> str:
        """Validate password strength."""
        try:
            sanitized_password = sanitize_password(password, min_length=8)
            
            # Check password complexity
            if not re.search(r'[A-Z]', sanitized_password):
                raise ValidationError("Password must contain at least one uppercase letter", field="password")
            
            if not re.search(r'[a-z]', sanitized_password):
                raise ValidationError("Password must contain at least one lowercase letter", field="password")
            
            if not re.search(r'\d', sanitized_password):
                raise ValidationError("Password must contain at least one digit", field="password")
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', sanitized_password):
                raise ValidationError("Password must contain at least one special character", field="password")
            
            return sanitized_password
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Invalid password: {str(e)}", field="password")
    
    @staticmethod
    def validate_filename(filename: str) -> str:
        """Validate filename for security and format."""
        try:
            sanitized_filename = sanitize_string(filename, max_length=255)
            
            # Check for valid file extensions
            allowed_extensions = {'.epub', '.txt', '.pdf'}
            if not any(sanitized_filename.lower().endswith(ext) for ext in allowed_extensions):
                raise ValidationError("Invalid file type. Only EPUB, TXT, and PDF files are allowed", field="filename")
            
            # Check for suspicious patterns
            suspicious_patterns = [
                r'\.\.',  # Directory traversal
                r'[<>:"|?*]',  # Invalid characters
                r'^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])\.',  # Reserved names
            ]
            
            for pattern in suspicious_patterns:
                if re.search(pattern, sanitized_filename, re.IGNORECASE):
                    raise ValidationError("Invalid filename pattern detected", field="filename")
            
            return sanitized_filename
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Invalid filename: {str(e)}", field="filename")
    
    @staticmethod
    def validate_file_size(size_bytes: int, max_size_mb: int = 100) -> int:
        """Validate file size."""
        max_size_bytes = max_size_mb * 1024 * 1024
        
        if size_bytes <= 0:
            raise ValidationError("File size must be greater than 0", field="file_size")
        
        if size_bytes > max_size_bytes:
            raise ValidationError(
                f"File size exceeds maximum limit of {max_size_mb}MB",
                field="file_size"
            )
        
        return size_bytes
    
    @staticmethod
    def validate_user_preferences(preferences: Dict[str, Any]) -> Dict[str, Any]:
        """Validate user preferences."""
        validated = {}
        
        # Font size validation
        if 'fontSize' in preferences:
            try:
                font_size = int(preferences['fontSize'])
                if font_size < 8 or font_size > 72:
                    raise ValidationError("Font size must be between 8 and 72", field="fontSize")
                validated['fontSize'] = font_size
            except (ValueError, TypeError):
                raise ValidationError("Font size must be a valid integer", field="fontSize")
        
        # Brightness validation
        if 'brightness' in preferences:
            try:
                brightness = float(preferences['brightness'])
                if brightness < 0.1 or brightness > 2.0:
                    raise ValidationError("Brightness must be between 0.1 and 2.0", field="brightness")
                validated['brightness'] = brightness
            except (ValueError, TypeError):
                raise ValidationError("Brightness must be a valid number", field="brightness")
        
        # Effects validation
        if 'effects' in preferences:
            if not isinstance(preferences['effects'], dict):
                raise ValidationError("Effects must be a dictionary", field="effects")
            
            validated['effects'] = {}
            for effect_name, effect_config in preferences['effects'].items():
                if not isinstance(effect_config, dict):
                    raise ValidationError(f"Effect config for '{effect_name}' must be a dictionary", field="effects")
                
                validated_effect = {}
                
                # Validate enabled flag
                if 'enabled' in effect_config:
                    if not isinstance(effect_config['enabled'], bool):
                        raise ValidationError(f"Effect enabled flag for '{effect_name}' must be a boolean", field="effects")
                    validated_effect['enabled'] = effect_config['enabled']
                
                # Validate intensity
                if 'intensity' in effect_config:
                    try:
                        intensity = float(effect_config['intensity'])
                        if intensity < 0.0 or intensity > 1.0:
                            raise ValidationError(f"Effect intensity for '{effect_name}' must be between 0.0 and 1.0", field="effects")
                        validated_effect['intensity'] = intensity
                    except (ValueError, TypeError):
                        raise ValidationError(f"Effect intensity for '{effect_name}' must be a valid number", field="effects")
                
                validated['effects'][effect_name] = validated_effect
        
        return validated
    
    @staticmethod
    def validate_analytics_event(event_name: str, payload: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
        """Validate analytics event data."""
        # Validate event name
        try:
            sanitized_name = sanitize_string(event_name, max_length=100)
            
            # Check for valid event name pattern
            if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', sanitized_name):
                raise ValidationError("Event name must start with a letter or underscore and contain only alphanumeric characters and underscores", field="event_name")
            
            # Check for reserved event names
            reserved_names = {'error', 'exception', 'debug', 'internal', 'system'}
            if sanitized_name.lower() in reserved_names:
                raise ValidationError("Event name is reserved and cannot be used", field="event_name")
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Invalid event name: {str(e)}", field="event_name")
        
        # Validate payload
        try:
            if not isinstance(payload, dict):
                raise ValidationError("Payload must be a dictionary", field="payload")
            
            if len(payload) > 50:
                raise ValidationError("Payload cannot contain more than 50 keys", field="payload")
            
            validated_payload = {}
            for key, value in payload.items():
                # Validate key
                if not isinstance(key, str):
                    raise ValidationError("Payload keys must be strings", field="payload")
                
                if len(key) > 50:
                    raise ValidationError("Payload key names cannot exceed 50 characters", field="payload")
                
                if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', key):
                    raise ValidationError("Payload key names must start with a letter or underscore and contain only alphanumeric characters and underscores", field="payload")
                
                # Validate value
                if isinstance(value, str):
                    validated_payload[key] = sanitize_string(value, max_length=500)
                elif isinstance(value, (int, float, bool)):
                    validated_payload[key] = value
                elif isinstance(value, list):
                    if len(value) > 100:
                        raise ValidationError("Payload list values cannot exceed 100 items", field="payload")
                    validated_payload[key] = value[:100]  # Limit to 100 items
                elif isinstance(value, dict):
                    if len(value) > 20:
                        raise ValidationError("Payload nested dictionaries cannot exceed 20 keys", field="payload")
                    validated_payload[key] = value
                else:
                    raise ValidationError(f"Unsupported payload value type for key '{key}'", field="payload")
            
        except Exception as e:
            if isinstance(e, ValidationError):
                raise
            raise ValidationError(f"Invalid payload: {str(e)}", field="payload")
        
        return sanitized_name, validated_payload


class UserValidationSchema(BaseModel):
    """Validation schema for user-related data."""
    
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        return ValidationSchema.validate_email(v)
    
    @validator('password')
    def validate_password(cls, v):
        return ValidationSchema.validate_password(v)


class FileUploadValidationSchema(BaseModel):
    """Validation schema for file uploads."""
    
    filename: str
    file_size: int
    content_type: Optional[str] = None
    
    @validator('filename')
    def validate_filename(cls, v):
        return ValidationSchema.validate_filename(v)
    
    @validator('file_size')
    def validate_file_size(cls, v):
        return ValidationSchema.validate_file_size(v)
    
    @validator('content_type')
    def validate_content_type(cls, v):
        if v is not None:
            allowed_types = {
                'application/epub+zip',
                'application/pdf',
                'text/plain',
                'application/octet-stream'  # For some EPUB files
            }
            if v not in allowed_types:
                raise ValidationError(f"Unsupported content type: {v}", field="content_type")
        return v


class PreferencesValidationSchema(BaseModel):
    """Validation schema for user preferences."""
    
    fontSize: Optional[int] = 16
    brightness: Optional[float] = 1.0
    adaptiveBrightness: Optional[bool] = False
    effectsEnabled: Optional[bool] = True
    effects: Optional[Dict[str, Dict[str, Any]]] = None
    
    @validator('fontSize')
    def validate_font_size(cls, v):
        if v is not None and (v < 8 or v > 72):
            raise ValidationError("Font size must be between 8 and 72", field="fontSize")
        return v
    
    @validator('brightness')
    def validate_brightness(cls, v):
        if v is not None and (v < 0.1 or v > 2.0):
            raise ValidationError("Brightness must be between 0.1 and 2.0", field="brightness")
        return v


class AnalyticsEventValidationSchema(BaseModel):
    """Validation schema for analytics events."""
    
    name: str
    payload: Dict[str, Any] = {}
    
    @validator('name')
    def validate_name(cls, v):
        return ValidationSchema.validate_analytics_event(v, {})[0]
    
    @validator('payload')
    def validate_payload(cls, v):
        return ValidationSchema.validate_analytics_event("temp", v)[1]


def validate_user_data(email: str, password: str) -> tuple[str, str]:
    """Validate user registration/login data."""
    try:
        schema = UserValidationSchema(email=email, password=password)
        return schema.email, schema.password
    except PydanticValidationError as e:
        # Convert Pydantic validation errors to our custom exceptions
        for error in e.errors():
            field = error['loc'][0] if error['loc'] else 'unknown'
            message = error['msg']
            raise ValidationError(message, field=field)


def validate_file_upload(filename: str, file_size: int, content_type: Optional[str] = None) -> tuple[str, int, Optional[str]]:
    """Validate file upload data."""
    try:
        schema = FileUploadValidationSchema(
            filename=filename,
            file_size=file_size,
            content_type=content_type
        )
        return schema.filename, schema.file_size, schema.content_type
    except PydanticValidationError as e:
        for error in e.errors():
            field = error['loc'][0] if error['loc'] else 'unknown'
            message = error['msg']
            raise ValidationError(message, field=field)


def validate_preferences(preferences: Dict[str, Any]) -> Dict[str, Any]:
    """Validate user preferences."""
    try:
        schema = PreferencesValidationSchema(**preferences)
        return schema.dict(exclude_none=True)
    except PydanticValidationError as e:
        for error in e.errors():
            field = error['loc'][0] if error['loc'] else 'unknown'
            message = error['msg']
            raise ValidationError(message, field=field)


def validate_analytics_event_data(name: str, payload: Dict[str, Any]) -> tuple[str, Dict[str, Any]]:
    """Validate analytics event data."""
    try:
        schema = AnalyticsEventValidationSchema(name=name, payload=payload)
        return schema.name, schema.payload
    except PydanticValidationError as e:
        for error in e.errors():
            field = error['loc'][0] if error['loc'] else 'unknown'
            message = error['msg']
            raise ValidationError(message, field=field)
