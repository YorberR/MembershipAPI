"""Plan API routes."""

from fastapi import APIRouter, status, Query, Depends

from app.db.db import SessionDep
from app.models import Plan, PlanCreate, PlanUpdate
from app.services.plan import plan_service
from app.api.responses import APIResponse, PaginatedResponse
from app.api.deps import get_current_user
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()


@router.post("/plans", response_model=APIResponse[Plan], status_code=status.HTTP_201_CREATED)
async def create_plan(
    plan_data: PlanCreate, 
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Create a new plan."""
    plan = plan_service.create(session, plan_data)
    logger.info(f"Plan created by {current_user}: {plan.id}")
    
    return APIResponse(
        message="Plan created successfully",
        data=plan
    )


@router.get("/plans/{plan_id}", response_model=APIResponse[Plan])
async def get_plan(plan_id: int, session: SessionDep):
    """Get a plan by ID."""
    plan = plan_service.get_or_404(session, plan_id)
    
    return APIResponse(
        message="Plan retrieved successfully",
        data=plan
    )


@router.patch("/plans/{plan_id}", response_model=APIResponse[Plan])
async def update_plan(
    plan_id: int,
    plan_data: PlanUpdate,
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Update a plan."""
    plan = plan_service.get_or_404(session, plan_id)
    updated_plan = plan_service.update(session, plan, plan_data)
    logger.info(f"Plan {plan_id} updated by {current_user}")
    
    return APIResponse(
        message="Plan updated successfully",
        data=updated_plan
    )


@router.delete("/plans/{plan_id}", response_model=APIResponse[dict])
async def delete_plan(
    plan_id: int,
    session: SessionDep,
    current_user: str = Depends(get_current_user)
):
    """Delete a plan."""
    plan_service.delete(session, plan_id)
    logger.info(f"Plan {plan_id} deleted by {current_user}")
    
    return APIResponse(
        message="Plan deleted successfully",
        data={"deleted_id": plan_id}
    )


@router.get("/plans", response_model=APIResponse[PaginatedResponse[Plan]])
async def get_plans(
    session: SessionDep,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Number of records to return")
):
    """Get plans with pagination."""
    plans = plan_service.get_multi(session, skip=skip, limit=limit)
    total = plan_service.count(session)
    
    paginated_data = PaginatedResponse(
        items=plans,
        total=total,
        page=skip // limit + 1,
        size=limit,
        pages=(total + limit - 1) // limit
    )
    
    return APIResponse(
        message="Plans retrieved successfully",
        data=paginated_data
    )