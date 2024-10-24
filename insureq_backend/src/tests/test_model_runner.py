from database.model_performance import ModelPerformance
from services.ml_models.model_runner import run_evaluation
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database.database import Base, SessionLocal


# Setup test database
TEST_DATABASE_URL = "sqlite:///./test.db"


@pytest.fixture(scope="module")
def test_db():
    # Create a new database engine
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

    # Create the tables
    Base.metadata.create_all(bind=engine)

    # Create a new session
    session = sessionmaker(bind=engine)()

    yield session  # This allows the test functions to use the session

    # Cleanup after tests
    session.close()
    Base.metadata.drop_all(bind=engine)  # Clean up the test database


def test_model_evaluation(test_db: Session):
    initial_count = len(test_db.query(ModelPerformance).all())

    # Run model evaluation
    run_evaluation()

    # Check that new entries were added
    new_count = len(test_db.query(ModelPerformance).all())
    assert new_count > initial_count

    test_db.close()
