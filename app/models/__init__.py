"""Models package for the application."""

# Base models and enums
from .base import StatusEnum, BaseModel

# Import all models from core (properly configured)
from .core import (
    CustomerPlan,
    Customer, CustomerBase, CustomerCreate, CustomerUpdate,
    Plan, PlanBase, PlanCreate, PlanUpdate,
    Transaction, TransactionBase, TransactionCreate, TransactionUpdate,
    Invoice
)

# Export all models
__all__ = [
    # Base
    "StatusEnum",
    "BaseModel",
    
    # Associations
    "CustomerPlan",
    
    # Customer models
    "Customer",
    "CustomerBase", 
    "CustomerCreate",
    "CustomerUpdate",
    
    # Plan models
    "Plan",
    "PlanBase",
    "PlanCreate", 
    "PlanUpdate",
    
    # Transaction models
    "Transaction",
    "TransactionBase",
    "TransactionCreate",
    "TransactionUpdate",
    
    # Invoice models
    "Invoice",
]