from fastapi import APIRouter, HTTPException, status
from sqlmodel import select

from db import SessionDep
from models import Customer, CustomerCreate, CustomerUpdate

router = APIRouter()
    
@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(customer_data: CustomerCreate, session: SessionDep):
    customer = Customer.model_validate(customer_data.model_dump())
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

@router.get("/customers/{customer_id}", response_model=Customer, tags=["customers"])
async def get_customer(customer_id: int, session: SessionDep):
    db_customer = session.get(Customer, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return db_customer

@router.delete("/customers/{customer_id}", response_model=dict, tags=["customers"])
async def delete_customer(customer_id: int, session: SessionDep):
    db_customer = session.get(Customer, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(db_customer)
    session.commit()
    return {"message": "Customer deleted"}

@router.put("/customers/{customer_id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def update_customer(customer_id: int, customer_data: CustomerUpdate, session: SessionDep):
    db_customer = session.get(Customer, customer_id)
    if db_customer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_data_dict = customer_data.model_dump(exclude_unset=True)
    db_customer.sqlmodel_update(customer_data_dict)
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)

    return db_customer

@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def get_customers(session: SessionDep):
    db_customers = session.exec(select(Customer)).all()
    return db_customers
