import json
from app.models.user.messages import UserResponseMessages
from tests.http.client import client
from tests.utils.basic_auth import get_basic_auth_header

# Load the test data from JSON file
with open("tests/data/http/user.json") as f:
    TEST_DATA = json.load(f)


def test_create_user_one_success():
    """Test user creation with valid payload (user one)"""
    use_one = TEST_DATA["user_one"]
    payload = {
        "first_name": use_one["first_name"],
        "last_name": use_one["last_name"],
        "phone_number": use_one["phone_number"],
    }
    response = client.post(
        "/user",
        json=payload,
        headers=get_basic_auth_header(
            username=use_one["email"],
            password=use_one["password"],
        )
    )
    assert response.status_code in [200, 201]
    json_data = response.json()

    # Adjusted based on your actual API response structure
    assert "message" in json_data
    assert json_data["message"] == UserResponseMessages.USER_CREATED.value

    user_data = json_data["data"]
    assert "id" in user_data
    assert user_data["email"] == use_one["email"]
    assert user_data["first_name"] == use_one["first_name"]
    assert user_data["last_name"] == use_one["last_name"]


def test_create_user_two_success_and_unique_key_fail():
    """Test user creation with valid payload (user two), and then attempt to create the same user again"""
    use_two = TEST_DATA["user_two"]
    payload = {
        "first_name": use_two["first_name"],
        "last_name": use_two["last_name"],
        "phone_number": use_two["phone_number"],
    }
    response = client.post(
        "/user",
        json=payload,
        headers=get_basic_auth_header(
            username=use_two["email"],
            password=use_two["password"],
        )
    )
    assert response.status_code in [200, 201]
    json_data = response.json()

    # Adjusted based on your actual API response structure
    assert "message" in json_data
    assert json_data["message"] == UserResponseMessages.USER_CREATED.value

    user_data = json_data["data"]
    assert "id" in user_data
    assert user_data["email"] == use_two["email"]
    assert user_data["first_name"] == use_two["first_name"]
    assert user_data["last_name"] == use_two["last_name"]

    # Attempt to create the same user again
    response = client.post(
        "/user",
        json=payload,
        headers=get_basic_auth_header(
            username=use_two["email"],
            password=use_two["password"],
        )
    )
    assert response.status_code in [400, 422]
    json_data = response.json()
    assert "message" in json_data or "detail" in json_data
    assert json_data["message"] == UserResponseMessages.USER_CREATION_FAILED.value


def test_create_user_missing_name_should_fail():
    """Test user creation failure when first_name is missing"""
    data = TEST_DATA["missing_name"]
    user = TEST_DATA["user_two"]
    headers = get_basic_auth_header(username=user["email"], password=user["password"])

    response = client.post("/user", json=data, headers=headers)
    assert response.status_code in [400, 422]

    json_data = response.json()
    assert "message" in json_data or "detail" in json_data


def test_create_user_invalid_phone_should_fail():
    """Test user creation failure when phone number is invalid"""
    data = TEST_DATA["invalid_phone"]
    user = TEST_DATA["user_two"]
    headers = get_basic_auth_header(username=user["email"], password=user["password"])
    response = client.post("/user", json=data, headers=headers)
    assert response.status_code in [400, 422]

    json_data = response.json()
    assert "message" in json_data or "detail" in json_data
