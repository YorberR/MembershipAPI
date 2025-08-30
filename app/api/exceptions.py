"""Custom API exceptions."""

from typing import Optional, Any, Dict
from fastapi import HTTPException, status


class APIException(HTTPException):
    """Base API exception."""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None,
    ):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=message, headers=headers)


class NotFoundError(APIException):
    """Resource not found exception."""
    
    def __init__(self, resource: str, identifier: Any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=f"{resource} with id '{identifier}' not found",
            error_code="RESOURCE_NOT_FOUND"
        )


class ValidationError(APIException):
    """Validation error exception."""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            error_code="VALIDATION_ERROR"
        )


class ConflictError(APIException):
    """Resource conflict exception."""
    
    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            error_code="RESOURCE_CONFLICT"
        )