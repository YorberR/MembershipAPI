from pydantic import BaseModel

class CustomerBase(BaseModel):
    name: str
    description: str | None
    age: int
    email: str

class CustomerCreate(CustomerBase):
    pass

class Customer(CustomerBase):
    id: int | None
    
class Transaction(BaseModel):
    id: int
    ammount: int
    description: str

class Invoice(BaseModel):
    id: int
    customer: Customer
    transactions: list[Transaction]
    total: int

    @property
    def ammount_total(self):
        return sum([t.ammount for t in self.transactions])