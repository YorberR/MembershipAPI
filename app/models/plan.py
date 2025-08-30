"""Plan related models."""

from typing import TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

from .base import BaseModel

if TYPE_CHECKING:
    from .customer import Customer


class PlanBase(SQLModel):
    """Base plan model with shared fields."""
    name: str = Field(..., min_length=3, max_length=50)
    price: int | None = Field(default=None, description="Price in cents")
    description: str = Field(..., max_length=255)


class PlanCreate(PlanBase):
    """Model for creating a new plan."""
    pass


class PlanUpdate(PlanBase):
    """Model for updating an existing plan."""
    pass


class Plan(PlanBase, table=True):
    """Plan database model."""
    id: int | None = Field(default=None, primary_key=True)
    
    # Relationships
    customers: list["Customer"] = Relationship(back_populates="plans")