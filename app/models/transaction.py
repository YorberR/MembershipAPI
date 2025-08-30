"""Transaction related models."""

from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .customer import Customer


class TransactionBase(SQLModel):
    """Base transaction model with shared fields."""
    amount: int = Field(..., description="Transaction amount in cents")
    description: str = Field(..., max_length=255)


class TransactionCreate(TransactionBase):
    """Model for creating a new transaction."""
    customer_id: int = Field(..., foreign_key="customer.id")


class TransactionUpdate(TransactionBase):
    """Model for updating an existing transaction."""
    pass


class Transaction(TransactionBase, table=True):
    """Transaction database model."""
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(..., foreign_key="customer.id")
    
    # Relationships
    customer: "Customer" = Relationship(back_populates="transactions")