from fastapi import FastAPI
from datetime import datetime

from sqlmodel import select
from app.routers import customers
from db import SessionDep, create_db_and_tables
from models import Invoice, Transaction

app = FastAPI(lifespan=create_db_and_tables)
app.include_router(customers.router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/time")
async def time():
    return {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@app.post("/transactions")
async def create_transaction(transaction_data: Transaction):
    return transaction_data

@app.post("/invoices")
async def create_invoice(invoice_data: Invoice):
    return invoice_data

