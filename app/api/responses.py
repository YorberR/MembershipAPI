"""API response models."""

from typing import Generic, TypeVar, Optional, Any, List
from pydantic import BaseModel

T = TypeVar('T')


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper."""
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[T] = None
    errors: Optional[List[str]] = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response model."""
    items: List[T]
    total: int
    page: int
    size: int
    pages: int


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    message: str
    errors: List[str]
    error_code: Optional[str] = None