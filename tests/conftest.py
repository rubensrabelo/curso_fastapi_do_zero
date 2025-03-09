import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )

from main import app  # noqa: E402


@pytest.fixture
def client():
    return TestClient(app)
