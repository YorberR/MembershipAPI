"""
DEPRECATED: This file has been refactored into separate modules.

Please import models from the specific modules instead:
- from app.models.customer import Customer, CustomerCreate, CustomerUpdate
- from app.models.plan import Plan, PlanCreate, PlanUpdate  
- from app.models.transaction import Transaction, TransactionCreate, TransactionUpdate
- from app.models.invoice import Invoice
- from app.models.associations import CustomerPlan
- from app.models.base import StatusEnum

Or import everything from the models package:
- from app.models import Customer, Plan, Transaction, Invoice, CustomerPlan, StatusEnum
"""

import warnings

# Re-export all models for backward compatibility
from .base import StatusEnum
from .associations import CustomerPlan
from .customer import Customer, CustomerBase, CustomerCreate, CustomerUpdate
from .plan import Plan, PlanBase, PlanCreate, PlanUpdate
from .transaction import Transaction, TransactionBase, TransactionCreate, TransactionUpdate
from .invoice import Invoice

# Issue deprecation warning when this file is imported
warnings.warn(
    "Importing from app.models.models is deprecated. "
    "Please import from specific model modules or from app.models package.",
    DeprecationWarning,
    stacklevel=2
)