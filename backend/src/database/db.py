import os

from dotenv import load_dotenv
from typing import Annotated

from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.orm import sessionmaker

from fastapi import Depends

from src.models import *
from src.core import settings


load_dotenv()

# Define choosing the settings
if settings.ENV == "testing":
    DATABASE_URL = "sqlite:///:memory:"
elif settings.ENV == "production":
    DATABASE_URL = os.getenv("POSTGRES_URL")
    if not DATABASE_URL:
        raise RuntimeError("POSTGRES_URL must be set in production mode")
elif settings.ENV == "dev":
    raise NotImplementedError("Development database is not ready yet")
else:
    raise ValueError(f"Unknown environment: {settings.ENV}")


settings.DATABASE_URI = DATABASE_URL


engine = create_engine(
    url=settings.DATABASE_URI,
    echo=True,
    connect_args={"check_same_thread": False},  # Only needed for SQLite
)
Base = SQLModel


def create_db_and_tables():
    Base.metadata.create_all(engine)
    return engine


def get_session():
    with Session(engine) as session:
        yield session


SessionType = Annotated[Session, Depends(get_session)]
