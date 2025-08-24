from db import SessionDep
from sqlmodel import select
from app.models.models import Plan
from fastapi import APIRouter, Depends, status, HTTPException, Response

router = APIRouter(tags = ['plans'])

@router.post("/plans", status_code=status.HTTP_201_CREATED)
def create_plan(plan_data: Plan, session: SessionDep):
    plan_db = Plan.model_validate(plan_data.model_dump())
    session.add(plan_db)
    session.commit()
    session.refresh(plan_db)
    return plan_db

@router.get("/plans", response_model=list[Plan])
def list_plans(session: SessionDep):
    plans = session.exec(select(Plan)).all()
    return plans