from app.db.db import SessionDep
from sqlmodel import select
from fastapi import APIRouter, status, HTTPException, Query
from app.models import Customer, CustomerCreate, CustomerUpdate, Plan, CustomerPlan, StatusEnum
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags = ['customers'])

@router.post("/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    try:
        session.add(customer)
        session.commit()
        session.refresh(customer)
        return customer
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400, 
            detail="A customer with this email already exists."
        )

@router.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_db

@router.patch(
    "/customers/{customer_id}",
    response_model=Customer,
    status_code=status.HTTP_201_CREATED
)
async def read_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep): #customer_data: CustomerCreate, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    customer_db.sqlmodel_update(customer_data_dict)
    session.add(customer_db)
    session.commit()
    session.refresh(customer_db)
    return customer_db

@router.delete("/customers/{customer_id}")
async def delete_customer(customer_id: int, session: SessionDep):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer_db)
    session.commit()
    session.refresh(customer_db)
    return {"datail": "ok"}

@router.get("/customers", response_model=list[Customer])
async def get_customers(session: SessionDep):
    return session.exec(select(Customer)).all()

@router.post("/customers/{customer_id}/plans/{plan_id}", status_code=status.HTTP_201_CREATED)
async def subscribe_customer_to_plan(
    customer_id: int, plan_id: int, session: SessionDep, plan_status: StatusEnum =Query()
):
    customer_db = session.get(Customer, customer_id)
    plan_db = session.get(Plan, plan_id)
    if not customer_db or not plan_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the customer or plan not found")
    customer_plan_db = CustomerPlan(customer_id=customer_id, plan_id=plan_id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db

@router.get("/customers/{customer_id}/plans", status_code=status.HTTP_201_CREATED)
async def subscribe_customer_to_plan(customer_id: int, session: SessionDep, plan_status: StatusEnum = Query()):
    customer_db = session.get(Customer, customer_id)
    if not customer_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the customer not found")
    query = select(CustomerPlan).where(CustomerPlan.customer_id == customer_id).where
    (CustomerPlan.status == plan_status)
    customer_plans = session.exec(query).all()
    return customer_plans