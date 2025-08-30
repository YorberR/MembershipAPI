"""Invoice related models."""

from pydantic import BaseModel, computed_field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .customer import Customer
    from .transaction import Transaction


class Invoice(BaseModel):
    """Invoice model for billing purposes."""
    id: int
    customer: "Customer"
    transactions: list["Transaction"]
    
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