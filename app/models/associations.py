"""Association models for many-to-many relationships."""

from sqlmodel import SQLModel, Field

from .base import StatusEnum


class CustomerPlan(SQLModel, table=True):
    """Association model for Customer-Plan many-to-many relationship."""
    customer_id: int = Field(foreign_key="customer.id", primary_key=True)
    plan_id: int = Field(foreign_key="plan.id", primary_key=True)
    status: StatusEnum = Field(default=StatusEnum.active)