"""Customer API routes."""

from typing import List, Optional
from fastapi import APIRouter, status, Query, Depends

from app.db.db import SessionDep
from app.models import Customer, CustomerCreate, CustomerUpdate, CustomerPlan, StatusEnum
from app.services.customer import customer_service
from app.api.responses import APIResponse, PaginatedResponse
from app.api.deps import get_current_user
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/customers", response_model=APIResponse[Customer], status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_data: CustomerCreate, 
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Create a new customer."""
    customer = customer_service.create(session, customer_data)
    logger.info(f"Customer created by {current_user}: {customer.id}")
    
    return APIResponse(
        message="Customer created successfully",
        data=customer
    )


@router.get("/customers/{customer_id}", response_model=APIResponse[Customer])
async def get_customer(customer_id: int, session: SessionDep):
    """Get a customer by ID."""
    customer = customer_service.get_or_404(session, customer_id)
    
    return APIResponse(
        message="Customer retrieved successfully",
        data=customer
    )


@router.patch("/customers/{customer_id}", response_model=APIResponse[Customer])
async def update_customer(
    customer_id: int, 
    customer_data: CustomerUpdate, 
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Update a customer."""
    customer = customer_service.get_or_404(session, customer_id)
    updated_customer = customer_service.update(session, customer, customer_data)
    logger.info(f"Customer {customer_id} updated by {current_user}")
    
    return APIResponse(
        message="Customer updated successfully",
        data=updated_customer
    )


@router.delete("/customers/{customer_id}", response_model=APIResponse[dict])
async def delete_customer(
    customer_id: int, 
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Delete a customer."""
    customer_service.delete(session, customer_id)
    logger.info(f"Customer {customer_id} deleted by {current_user}")
    
    return APIResponse(
        message="Customer deleted successfully",
        data={"deleted_id": customer_id}
    )


@router.get("/customers", response_model=APIResponse[PaginatedResponse[Customer]])
async def get_customers(
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """Get customers with pagination."""
    customers = customer_service.get_multi(session, skip=skip, limit=limit)
    total = customer_service.count(session)
    
    paginated_data = PaginatedResponse(
        items=customers,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )
    
    return APIResponse(
        message="Customers retrieved successfully",
        data=paginated_data
    )


@router.post("/customers/{customer_id}/plans/{plan_id}", response_model=APIResponse[Customer])
async def add_plan_to_customer(
    customer_id: int, 
    plan_id: int, 
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Add a plan to a customer."""
    customer = customer_service.add_plan(session, customer_id, plan_id)
    logger.info(f"Plan {plan_id} added to customer {customer_id} by {current_user}")
    
    return APIResponse(
        message="Plan added to customer successfully",
        data=customer
    )


@router.delete("/customers/{customer_id}/plans/{plan_id}", response_model=APIResponse[Customer])
async def remove_plan_from_customer(
    customer_id: int, 
    plan_id: int, 
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Remove a plan from a customer."""
    customer = customer_service.remove_plan(session, customer_id, plan_id)
    logger.info(f"Plan {plan_id} removed from customer {customer_id} by {current_user}")
    
    return APIResponse(
        message="Plan removed from customer successfully",
        data=customer
    )


@router.get("/customers/{customer_id}/plans", response_model=APIResponse[List[CustomerPlan]])
async def get_customer_plans(
    customer_id: int, 
    session: SessionDep,
    status_filter: Optional[StatusEnum] = Query(None, description="Filter by plan status")
):
    """Get all plans for a customer."""
    # Verify customer exists
    customer_service.get_or_404(session, customer_id)
    
    # Get customer plans (this would need to be implemented in the service)
    from sqlmodel import select
    query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id)
    if status_filter:
        query = query.where(CustomerPlan.status == status_filter)
    
    customer_plans = session.exec(query).all()
    
    return APIResponse(
        message="Customer plans retrieved successfully",
        data=customer_plans
    )