"""Transaction API routes."""

from typing import List
from fastapi import APIRouter, status, Query, Depends

from app.db.db import SessionDep
from app.models import Transaction, TransactionCreate, TransactionUpdate
from app.services.transaction import transaction_service
from app.api.responses import APIResponse, PaginatedResponse
from app.api.deps import get_current_user
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/transactions", response_model=APIResponse[Transaction], status_code=status.HTTP_201_CREATED)
async def create_transaction(
    transaction_data: TransactionCreate, 
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Create a new transaction."""
    transaction = transaction_service.create(session, transaction_data)
    logger.info(f"Transaction created by {current_user}: {transaction.id}")
    
    return APIResponse(
        message="Transaction created successfully",
        data=transaction
    )


@router.get("/transactions/{transaction_id}", response_model=APIResponse[Transaction])
async def get_transaction(transaction_id: int, session: SessionDep):
    """Get a transaction by ID."""
    transaction = transaction_service.get_or_404(session, transaction_id)
    
    return APIResponse(
        message="Transaction retrieved successfully",
        data=transaction
    )


@router.patch("/transactions/{transaction_id}", response_model=APIResponse[Transaction])
async def update_transaction(
    transaction_id: int,
    transaction_data: TransactionUpdate,
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Update a transaction."""
    transaction = transaction_service.get_or_404(session, transaction_id)
    updated_transaction = transaction_service.update(session, transaction, transaction_data)
    logger.info(f"Transaction {transaction_id} updated by {current_user}")
    
    return APIResponse(
        message="Transaction updated successfully",
        data=updated_transaction
    )


@router.delete("/transactions/{transaction_id}", response_model=APIResponse[dict])
async def delete_transaction(
    transaction_id: int,
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Delete a transaction."""
    transaction_service.delete(session, transaction_id)
    logger.info(f"Transaction {transaction_id} deleted by {current_user}")
    
    return APIResponse(
        message="Transaction deleted successfully",
        data={"deleted_id": transaction_id}
    )


@router.get("/transactions", response_model=APIResponse[PaginatedResponse[Transaction]])
async def get_transactions(
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """Get transactions with pagination."""
    transactions = transaction_service.get_multi(session, skip=skip, limit=limit)
    total = transaction_service.count(session)
    
    paginated_data = PaginatedResponse(
        items=transactions,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )
    
    return APIResponse(
        message="Transactions retrieved successfully",
        data=paginated_data
    )


@router.get("/customers/{customer_id}/transactions", response_model=APIResponse[List[Transaction]])
async def get_customer_transactions(
    customer_id: int,
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """Get all transactions for a specific customer."""
    transactions = transaction_service.get_by_customer(session, customer_id, skip, limit)
    
    return APIResponse(
        message="Customer transactions retrieved successfully",
        data=transactions
    )


@router.get("/customers/{customer_id}/transactions/total", response_model=APIResponse[dict])
async def get_customer_transaction_total(customer_id: int, session: SessionDep):
    """Get total transaction amount for a customer."""
    total = transaction_service.get_customer_total(session, customer_id)
    
    return APIResponse(
        message="Customer transaction total calculated successfully",
        data={
            "customer_id": customer_id,
            "total_amount": total,
            "currency": "cents"
        }
    )