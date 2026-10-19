import os
os.environ.setdefault("SECRET_KEY", "test_secret_key_for_tests_only_123456")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from main import app
from Services.database import base, get_db

# a separate throw-away database, only for tests
engine = create_engine(
    "sqlite://", 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
    )

TestingSession = sessionmaker(bind=engine)


@pytest.fixture()
def client():
    base.metadata.create_all(engine)          # fresh empty tables for every test

    def override_get_db():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
    base.metadata.drop_all(engine)            # clean up