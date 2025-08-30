"""Base models and enums for the application."""

from enum import Enum
from sqlmodel import SQLModel


class StatusEnum(str, Enum):
    """Status enumeration for various entities."""
    active = "active"
    inactive = "inactive"


class BaseModel(SQLModel):
    """Base model with common functionality."""
    pass