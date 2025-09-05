from fastapi import Depends
from typing import Annotated
from sqlmodel import create_engine, Session, SQLModel
from dotenv import load_dotenv
import os

load_dotenv()


postgress_url = str(os.getenv("POSTGRES_URL"))


engine = create_engine(postgress_url)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


SessionType = Annotated[Session, Depends(get_session)]
