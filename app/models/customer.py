"""Customer related models."""

from typing import TYPE_CHECKING, ForwardRef
from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .transaction import Transaction
    from .plan import Plan


class CustomerBase(SQLModel):
    """Base customer model with shared fields."""
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    age: int = Field(..., gt=0, lt=150)
    email: EmailStr = Field(default=None, unique=True)


class CustomerCreate(CustomerBase):
    """Model for creating a new customer."""
    pass


class CustomerUpdate(CustomerBase):
    """Model for updating an existing customer."""
    pass


class Customer(CustomerBase, table=True):
    """Customer database model."""
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list["Plan"] = Relationship(back_populates="customers")