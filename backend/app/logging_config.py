"""
Logging configuration for the Cinei-Reader API.
Provides structured logging with different levels and handlers.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

from .config import settings


class CustomFormatter(logging.Formatter):
    """Custom formatter with colors and structured output."""
    
    # Color codes for different log levels
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }
    
    def format(self, record):
        # Add timestamp
        record.timestamp = datetime.utcnow().isoformat()
        
        # Add color if terminal supports it
        if hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
            reset_color = self.COLORS['RESET']
            record.levelname = f"{level_color}{record.levelname}{reset_color}"
        
        # Add extra fields if present
        extra_fields = []
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'lineno', 'funcName', 'created', 
                          'msecs', 'relativeCreated', 'thread', 'threadName', 
                          'processName', 'process', 'getMessage', 'exc_info', 
                          'exc_text', 'stack_info', 'timestamp']:
                extra_fields.append(f"{key}={value}")
        
        if extra_fields:
            record.extra_info = f" | {' | '.join(extra_fields)}"
        else:
            record.extra_info = ""
        
        return super().format(record)


def setup_logging(
    log_level: str = "INFO",
    log_file: Optional[str] = None,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> None:
    """
    Setup logging configuration for the application.
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file (optional)
        max_file_size: Maximum size of log file before rotation
        backup_count: Number of backup files to keep
    """
    # Create logs directory if it doesn't exist
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    console_formatter = CustomFormatter(
        '%(timestamp)s | %(levelname)s | %(name)s | %(message)s%(extra_info)s'
    )
    
    file_formatter = logging.Formatter(
        '%(timestamp)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(funcName)s | %(message)s%(extra_info)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (if log_file is specified)
    if log_file:
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
    
    # Set specific logger levels
    logging.getLogger('uvicorn').setLevel(logging.WARNING)
    logging.getLogger('uvicorn.access').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.engine').setLevel(logging.WARNING)
    logging.getLogger('sqlalchemy.pool').setLevel(logging.WARNING)
    logging.getLogger('alembic').setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)


class RequestLogger:
    """Middleware for logging HTTP requests."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_request(self, request, response=None, duration=None, error=None):
        """Log HTTP request details."""
        log_data = {
            'method': request.method,
            'url': str(request.url),
            'client_ip': request.client.host if request.client else 'unknown',
            'user_agent': request.headers.get('user-agent', 'unknown'),
            'status_code': response.status_code if response else None,
            'duration_ms': round(duration * 1000, 2) if duration else None,
        }
        
        if error:
            log_data['error'] = str(error)
            self.logger.error(f"Request failed: {log_data}")
        else:
            self.logger.info(f"Request completed: {log_data}")


class DatabaseLogger:
    """Logger for database operations."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_query(self, query, params=None, duration=None):
        """Log database query."""
        self.logger.debug(f"Database query: {query} | Params: {params} | Duration: {duration}ms")
    
    def log_connection(self, action, details=None):
        """Log database connection events."""
        self.logger.info(f"Database {action}: {details}")
    
    def log_error(self, error, context=None):
        """Log database errors."""
        self.logger.error(f"Database error: {error} | Context: {context}")


class SecurityLogger:
    """Logger for security-related events."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_auth_attempt(self, email, success, ip_address, user_agent):
        """Log authentication attempts."""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"Authentication {status}: {email} | IP: {ip_address} | UA: {user_agent}")
    
    def log_rate_limit(self, ip_address, endpoint, limit_exceeded):
        """Log rate limiting events."""
        action = "EXCEEDED" if limit_exceeded else "CHECKED"
        self.logger.warning(f"Rate limit {action}: {ip_address} | Endpoint: {endpoint}")
    
    def log_suspicious_activity(self, activity_type, details, ip_address):
        """Log suspicious activities."""
        self.logger.warning(f"Suspicious activity: {activity_type} | Details: {details} | IP: {ip_address}")


class PerformanceLogger:
    """Logger for performance metrics."""
    
    def __init__(self, logger: logging.Logger):
        self.logger = logger
    
    def log_operation_time(self, operation, duration, details=None):
        """Log operation execution time."""
        self.logger.info(f"Performance: {operation} took {duration}ms | Details: {details}")
    
    def log_memory_usage(self, memory_usage, context=None):
        """Log memory usage."""
        self.logger.debug(f"Memory usage: {memory_usage}MB | Context: {context}")
    
    def log_slow_operation(self, operation, duration, threshold=1000):
        """Log slow operations."""
        if duration > threshold:
            self.logger.warning(f"Slow operation: {operation} took {duration}ms (threshold: {threshold}ms)")


# Initialize logging on module import
def initialize_logging():
    """Initialize logging with default configuration."""
    log_level = os.getenv('LOG_LEVEL', 'INFO')
    log_file = os.getenv('LOG_FILE', 'logs/cinei_reader.log')
    
    setup_logging(
        log_level=log_level,
        log_file=log_file
    )


# Create default loggers
initialize_logging()
app_logger = get_logger('cinei_reader')
request_logger = RequestLogger(get_logger('cinei_reader.requests'))
db_logger = DatabaseLogger(get_logger('cinei_reader.database'))
security_logger = SecurityLogger(get_logger('cinei_reader.security'))
performance_logger = PerformanceLogger(get_logger('cinei_reader.performance'))
