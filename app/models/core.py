"""Core models with proper relationship configuration."""

from typing import TYPE_CHECKING
from pydantic import EmailStr, computed_field, BaseModel as PydanticBaseModel
from sqlmodel import SQLModel, Field, Relationship

from .base import StatusEnum, BaseModel

# Association model (defined first)
class CustomerPlan(SQLModel, table=True):
    """Association model for Customer-Plan many-to-many relationship."""
    customer_id: int = Field(foreign_key="customer.id", primary_key=True)
    plan_id: int = Field(foreign_key="plan.id", primary_key=True)
    status: StatusEnum = Field(default=StatusEnum.active)

# Base models
class CustomerBase(SQLModel):
    """Base customer model with shared fields."""
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(default=None, max_length=255)
    age: int = Field(..., gt=0, lt=150)
    email: EmailStr = Field(default=None, unique=True)

class PlanBase(SQLModel):
    """Base plan model with shared fields."""
    name: str = Field(..., min_length=3, max_length=50)
    price: int | None = Field(default=None, description="Price in cents")
    description: str = Field(..., max_length=255)

class TransactionBase(SQLModel):
    """Base transaction model with shared fields."""
    amount: int = Field(..., description="Transaction amount in cents")
    description: str = Field(..., max_length=255)

# Create/Update models
class CustomerCreate(CustomerBase):
    """Model for creating a new customer."""
    pass

class CustomerUpdate(CustomerBase):
    """Model for updating an existing customer."""
    pass

class PlanCreate(PlanBase):
    """Model for creating a new plan."""
    pass

class PlanUpdate(PlanBase):
    """Model for updating an existing plan."""
    pass

class TransactionCreate(TransactionBase):
    """Model for creating a new transaction."""
    customer_id: int = Field(..., foreign_key="customer.id")

class TransactionUpdate(TransactionBase):
    """Model for updating an existing transaction."""
    pass

# Table models (defined with proper relationships)
class Customer(CustomerBase, table=True):
    """Customer database model."""
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list["Plan"] = Relationship(back_populates="customers", link_model=CustomerPlan)

class Plan(PlanBase, table=True):
    """Plan database model."""
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    customers: list[Customer] = Relationship(back_populates="plans", link_model=CustomerPlan)

class Transaction(TransactionBase, table=True):
    """Transaction database model."""
    id: int | None = Field(default=None, primary_key=True)
    customer_id: int = Field(..., foreign_key="customer.id")
    
    # Relationships
    customer: Customer = Relationship(back_populates="transactions")

# Invoice model
class Invoice(PydanticBaseModel):
    """Invoice model for billing purposes."""
    id: int
    customer: Customer
    transactions: list[Transaction]
    
    @computed_field
    @property
    def total(self) -> int:
        """Calculate total amount from all transactions."""
        return sum(transaction.amount for transaction in self.transactions)
    
    @computed_field
    @property
    def amount_total(self) -> int:
        """Alias for total amount (backward compatibility)."""
        return self.total