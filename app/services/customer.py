"""Customer service."""

from typing import Optional, List
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

from app.models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan
from app.services.base import BaseService
from app.api.exceptions import ConflictError, NotFoundError
from app.core.logging import get_logger

logger = get_logger(__name__)


class CustomerService(BaseService[Customer, CustomerCreate, CustomerUpdate]):
    """Customer service with business logic."""
    
    def __init__(self):
        super().__init__(Customer)
    
    def get_by_email(self, db: Session, email: str) -> Optional[Customer]:
        """Get customer by email."""
        statement = select(Customer).where(Customer.email == email)
        return db.exec(statement).first()
    
    def create(self, db: Session, obj_in: CustomerCreate) -> Customer:
        """Create customer with email validation."""
        # Check if email already exists
        existing = self.get_by_email(db, obj_in.email)
        if existing:
            raise ConflictError(f"Customer with email '{obj_in.email}' already exists")
        
        return super().create(db, obj_in)
    
    def add_plan(self, db: Session, customer_id: int, plan_id: int) -> Customer:
        """Add a plan to a customer."""
        customer = self.get_or_404(db, customer_id)
        
        # Check if plan exists
        plan = db.get(Plan, plan_id)
        if not plan:
            raise NotFoundError("Plan", plan_id)
        
        # Check if customer already has this plan
        existing_relation = db.exec(
            select(CustomerPlan).where(
                CustomerPlan.customer_id == customer_id,
                CustomerPlan.plan_id == plan_id
            )
        ).first()
        
        if existing_relation:
            raise ConflictError("Customer already has this plan")
        
        # Create the relationship
        customer_plan = CustomerPlan(customer_id=customer_id, plan_id=plan_id)
        db.add(customer_plan)
        db.commit()
        db.refresh(customer)
        
        logger.info(f"Added plan {plan_id} to customer {customer_id}")
        return customer
    
    def remove_plan(self, db: Session, customer_id: int, plan_id: int) -> Customer:
        """Remove a plan from a customer."""
        customer = self.get_or_404(db, customer_id)
        
        # Find the relationship
        relation = db.exec(
            select(CustomerPlan).where(
                CustomerPlan.customer_id == customer_id,
                CustomerPlan.plan_id == plan_id
            )
        ).first()
        
        if not relation:
            raise NotFoundError("Customer-Plan relationship", f"{customer_id}-{plan_id}")
        
        db.delete(relation)
        db.commit()
        db.refresh(customer)
        
        logger.info(f"Removed plan {plan_id} from customer {customer_id}")
        return customer


# Service instance
customer_service = CustomerService()