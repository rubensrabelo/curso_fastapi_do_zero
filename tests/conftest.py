import pytest
from fastapi.testclient import TestClient
from contextlib import contextmanager
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session
from datetime import datetime
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )

from main import app  # noqa: E402
from models import table_registry  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)


@contextmanager
def _mock_db_time(*, model, time=datetime(2025, 1, 1)):
    def fake_time_hook(mapper, connection, target):
        if hasattr(target, "created_at"):
            target.created_at = time
        if hasattr(target, "updated_at"):
            target.updated_at = time

    event.listen(model, "before_insert", fake_time_hook)

    yield time

    event.remove(model, "before_insert", fake_time_hook)


@pytest.fixture
def mock_db_time():
    return _mock_db_time
