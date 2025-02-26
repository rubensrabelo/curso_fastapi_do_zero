from http import HTTPStatus
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )

from main import app  # noqa: E402


def test_root_should_return_ok_and_hello_world():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"Message": "Hello, world!"}
