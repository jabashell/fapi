
from pydantic import BaseModel, EmailStr
from sqlmodel import Field, SQLModel


class CustomerBase (SQLModel):
    name: str = Field(default=None)
    description: str | None = Field(default=None)
    email : EmailStr = Field(default=None)
    age: int = Field(default=None)

class CustomerCreate (CustomerBase):
    pass

class CustomerUpdate (CustomerBase):
    pass

class Customer (CustomerBase, table=True):
    id: int | None = Field(default=None, primary_key= True)



class Transaction (BaseModel):
    id: int
    amount: int
    description: str 

class Invoice (BaseModel):
    id: int
    customer: Customer
    transaction: list[Transaction]
    total: int

    @property
    def amount_total(self):
        return sum([t.amount for t in self.transaction])    
