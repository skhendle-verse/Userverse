# tests/conftest.py
import os
import json
import pytest
from unittest.mock import patch
from tests.utils.basic_auth import get_basic_auth_header
from fastapi.testclient import TestClient

from app.main import create_app
from app.utils.config.loader import ConfigLoader
from app.database import DatabaseSessionManager
from app.database.user import User


@pytest.fixture(scope="session")
def client():
    os.environ["ENV"] = "testing"

    default_config = ConfigLoader(
        environment="testing"
    ).get_config()  # pulls the default from your updated loader
    print(f"Default config: {default_config}")
    with patch.object(ConfigLoader, "get_config", return_value=default_config):
        app = create_app()
        return TestClient(app)


@pytest.fixture(scope="session")
def test_user_data():
    """Fixture to load test data from JSON file."""
    with open("tests/data/http/user.json") as f:
        data = json.load(f)
    return data


# Get user row based on email, and extract OTP
@pytest.fixture
def get_user_one_otp(test_user_data):
    """Get user row based on email, and extract OTP."""
    user_one = test_user_data["user_one"]
    email = user_one["email"]
    db = DatabaseSessionManager()
    session = db.session_object()
    user = session.query(User).filter_by(email=email).first()
    if user:
        password_reset_data = user.primary_meta_data.get("password_reset", {})
        return password_reset_data.get("password_reset_token")
    return None


@pytest.fixture
def login_token(client, test_user_data):
    """Fixture to log in the user and provide the Bearer token for tests."""
    user_one = test_user_data["user_one"]
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
def login_token_user_two(client, test_user_data):
    """Fixture to log in the second user and provide the Bearer token."""
    user_two = test_user_data["user_two"]
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
