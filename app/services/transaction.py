"""Transaction service."""

from typing import List
from sqlmodel import Session, select

from app.models import Transaction, TransactionCreate, TransactionUpdate, Customer
from app.services.base import BaseService
from app.api.exceptions import NotFoundError
from app.core.logging import get_logger

logger = get_logger(__name__)


class TransactionService(BaseService[Transaction, TransactionCreate, TransactionUpdate]):
    """Transaction service with business logic."""
    
    def __init__(self):
        super().__init__(Transaction)
    
    def create(self, db: Session, obj_in: TransactionCreate) -> Transaction:
        """Create transaction with customer validation."""
        # Verify customer exists
        customer = db.get(Customer, obj_in.customer_id)
        if not customer:
            raise NotFoundError("Customer", obj_in.customer_id)
        
        return super().create(db, obj_in)
    
    def get_by_customer(
        self, 
        db: Session, 
        customer_id: int, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Transaction]:
        """Get transactions for a specific customer."""
        # Verify customer exists
        customer = db.get(Customer, customer_id)
        if not customer:
            raise NotFoundError("Customer", customer_id)
        
        statement = (
            select(Transaction)
            .where(Transaction.customer_id == customer_id)
            .offset(skip)
            .limit(limit)
        )
        return db.exec(statement).all()
    
    def get_customer_total(self, db: Session, customer_id: int) -> int:
        """Get total transaction amount for a customer."""
        transactions = self.get_by_customer(db, customer_id, skip=0, limit=1000)
        return sum(t.amount for t in transactions)


# Service instance
transaction_service = TransactionService()