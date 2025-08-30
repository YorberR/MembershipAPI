"""Plan service."""

from app.models import Plan, PlanCreate, PlanUpdate
from app.services.base import BaseService


class PlanService(BaseService[Plan, PlanCreate, PlanUpdate]):
    """Plan service with business logic."""
    
    def __init__(self):
        super().__init__(Plan)


# Service instance
plan_service = PlanService()