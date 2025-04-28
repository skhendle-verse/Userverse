# tests/conftest.py
import json
import pytest
from tests.http.client import client
from tests.utils.basic_auth import get_basic_auth_header

@pytest.fixture(scope="session")
def test_data():
    """Fixture to load test data from JSON file."""
    with open("tests/data/http/user.json") as f:
        data = json.load(f)
    return data

@pytest.fixture
def login_token(test_data):
    """Fixture to log in the user and provide the Bearer token for tests."""
    user_one = test_data["user_one"]
    response = client.patch(
        "/user/login",
        headers=get_basic_auth_header(
            username=user_one["email"],
            password=user_one["password"],
        )
    )
    assert response.status_code in [200, 201, 202]
    json_data = response.json()
    token = json_data["data"]["access_token"]
    return token
