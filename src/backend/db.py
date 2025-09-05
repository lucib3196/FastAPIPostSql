from os import environ
from fastapi import Depends
from typing import Annotated
from sqlmodel import create_engine, Session, SQLModel

username = environ.get("POSTGRES_USER")
password = environ.get("POSTGRES_PASSWORD")
host = environ.get("POSTGRES_HOST")
db = environ.get("POSTGRES_DB")

postgress_url = f"postgresql://{username}:{password}@{host}:5432/{db}"


engine = create_engine(postgress_url)


def get_session():
    with Session(engine) as session:
        yield session
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

SessionType = Annotated[Session, Depends(get_session)]
