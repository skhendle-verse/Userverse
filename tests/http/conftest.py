# tests/conftest.py
import os
import json
import pytest
from tests.utils.basic_auth import get_basic_auth_header
from fastapi.testclient import TestClient
from app.main import create_app

@pytest.fixture(scope="session")
def client():
    os.environ["ENV"] = "testing"
    app = create_app()
    return TestClient(app)

@pytest.fixture(scope="session")
def test_data():
    """Fixture to load test data from JSON file."""
    with open("tests/data/http/user.json") as f:
        data = json.load(f)
    return data


@pytest.fixture
def login_token(client, test_data):
    """Fixture to log in the user and provide the Bearer token for tests."""
    user_one = test_data["user_one"]
    response = client.patch(
        "/user/login",
        headers=get_basic_auth_header(
            username=user_one["email"],
            password=user_one["password"],
        ),
    )
    assert response.status_code in [200, 201, 202]
    json_data = response.json()
    token = json_data["data"]["access_token"]
    return token


@pytest.fixture
def login_token_user_two(client, test_data):
    """Fixture to log in the second user and provide the Bearer token."""
    user_two = test_data["user_two"]
    response = client.patch(
        "/user/login",
        headers=get_basic_auth_header(
            username=user_two["email"],
            password=user_two["password"],
        ),
    )
    assert response.status_code in [200, 201, 202]
    json_data = response.json()
    token = json_data["data"]["access_token"]
    return token
