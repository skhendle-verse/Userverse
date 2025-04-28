# tests/http/user/test_b_get_user_api.py
from tests.http.client import client
from app.models.user.messages import UserResponseMessages


def test_get_user_success(login_token, test_data):
    """Test fetching user details with valid token"""
    user = test_data["user_one"]
    # Assuming the login_token is valid and corresponds to user_one
    headers = {"Authorization": f"Bearer {login_token}"}
    response = client.get("/user", headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert "data" in json_data
    assert "email" in json_data["data"]
    assert "first_name" in json_data["data"]
    assert "last_name" in json_data["data"]
    assert "phone_number" in json_data["data"]
    assert json_data["message"] == UserResponseMessages.USER_FOUND.value
    # Check if the user data matches the expected data
    assert json_data["data"]["email"] == user["email"]
    assert json_data["data"]["first_name"] == user["first_name"]
    assert json_data["data"]["last_name"] == user["last_name"]
    assert json_data["data"]["phone_number"] == user["phone_number"]
