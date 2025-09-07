from src.database.db import create_engine, Base, create_db_and_tables, get_session
from src.core.app_config import settings
import pytest


@pytest.fixture(scope="session")
def engine():
    """Create a dedicated in-memory test engine."""
    settings.ENV = "testing"  # hardcode testing
    print(f"Created Database {settings.ENV} {settings.DATABASE_URI}")
    return create_db_and_tables()


@pytest.fixture(scope="function")
def db_session():
    session_gen = get_session()
    session = next(session_gen)  # get the actual Session object
    try:
        yield session
    finally:
        session_gen.close()


@pytest.fixture(autouse=True)
def _clean_db(db_session, engine):
    print("Cleaning database")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
