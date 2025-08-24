from db import engine
from enum import Enum
from pydantic import BaseModel, EmailStr, field_validator
from sqlmodel import SQLModel, Field, Relationship, Session, select

class StatusEnum(str, Enum):
    active = "active"
    inactive = "inactive"

class CustomerPlan(SQLModel, table=True):
    id: int = Field(primary_key=True)
    customer_id: int = Field(foreign_key="customer.id", primary_key=True)
    plan_id: int = Field(foreign_key="plan.id", primary_key=True)
    status: StatusEnum = Field(default=StatusEnum.active)


class Plan(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str = Field(..., min_length=3, max_length=50)
    price: int | None = Field(default=None)
    description: str = Field(..., max_length=255)
    customers: list["Customer"] = Relationship(back_populates="plans", link_model=CustomerPlan)

class CustomerBase(SQLModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str | None = Field(..., max_length=255)
    age: int = Field(..., gt=0, lt=150)
    email: EmailStr = Field(default=None, unique=True)
    # email: EmailStr = Field(..., max_length=100)

    # @field_validator("email")
    # @classmethod
    # def validate_email(cls, value):
    #     session = Session(engine)
    #     query = select(Customer).where(Customer.email == value)
    #     result = session.exec(query).first
    #     if result:
    #         raise ValueError("Email already exists")
    #     return value

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(CustomerBase):
    pass

class Customer(CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    transactions: list["Transaction"] = Relationship(back_populates="customer")
    plans: list[Plan] = Relationship(back_populates="customers", link_model=CustomerPlan)

class TransactionBase(SQLModel):
    ammount: int
    description: str    

class Transaction(TransactionBase, table=True):
    id: int | None = Field(primary_key=True)
    customer_id: int = Field(..., foreign_key="customer.id")
    customer: Customer = Relationship(back_populates="transactions")

class TransactionCreate(TransactionBase):
        customer_id: int = Field(..., foreign_key="customer.id")

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum([t.ammount for t in self.transactions])