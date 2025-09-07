from src.database.db import create_engine, Base, Session
import pytest


@pytest.fixture(scope="session")
def test_engine():
    """Create a dedicated in-memory test engine."""
    url = "sqlite:///:memory:"
    engine = create_engine(url, echo=True, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return engine


@pytest.fixture(scope="function")
def db_session(test_engine):
    """New transaction for each test."""
    with Session(test_engine) as session:
        yield session
        session.rollback()  # clean slate each test


@pytest.fixture(autouse=True)
def _clean_db(db_session, test_engine):
    print("Cleaning database")
    Base.metadata.drop_all(test_engine)
    Base.metadata.create_all(test_engine)
