from sqlmodel import SQLModel, Session, create_engine
from typing import Annotated
from fastapi import Depends, FastAPI

sqlite_name = "db.sqlite"
sqlite_url = f"sqlite:///{sqlite_name}"

engine = create_engine(sqlite_url)

def create_db_and_tables(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield    

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]