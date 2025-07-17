from typing import Any, Optional
from models.schemas import APIResponse

def create_response(
    success: bool,
    message: str,
    data: Optional[Any] = None,
    error: Optional[str] = None
) -> dict:
    """Create a standardized API response."""
    return {
        "success": success,
        "message": message,
        "data": data,
        "error": error
    }

def success_response(message: str, data: Optional[Any] = None) -> dict:
    """Create a success response."""
    return create_response(success=True, message=message, data=data)

def error_response(message: str, error: Optional[str] = None) -> dict:
    """Create an error response."""
    return create_response(success=False, message=message, error=error)

def validation_error_response(errors: list) -> dict:
    """Create a validation error response."""
    return create_response(
        success=False,
        message="Validation failed",
        error=errors
    )

def not_found_response(resource: str = "Resource") -> dict:
    """Create a not found response."""
    return create_response(
        success=False,
        message=f"{resource} not found",
        error="NOT_FOUND"
    )

def unauthorized_response() -> dict:
    """Create an unauthorized response."""
    return create_response(
        success=False,
        message="Unauthorized access",
        error="UNAUTHORIZED"
    )

def forbidden_response() -> dict:
    """Create a forbidden response."""
    return create_response(
        success=False,
        message="Access forbidden",
        error="FORBIDDEN"
    )

def internal_server_error_response(error_message: str = "Internal server error") -> dict:
    """Create an internal server error response."""
    return create_response(
        success=False,
        message=error_message,
        error="INTERNAL_SERVER_ERROR"
    )
