from tests.http.conftest import client, get_user_one_otp
from tests.utils.basic_auth import get_basic_auth_header


def test_a_password_reset_validate_otp_fail(client, test_data, get_user_one_otp):
    """Test password reset with valid user email"""
    user_one = test_data["user_one"]
    new_password = "NewPassword123"

    headers = get_basic_auth_header(
        username=user_one["email"],
        password=new_password,
    )

    response = client.patch(
        "/user/password-reset/validate-otp",
        headers=headers,
        json={"otp": get_user_one_otp + "FGWSE"},
    )

    assert response.status_code in [400, 401, 402]
    json_data = response.json()

    assert "detail" in json_data
    assert json_data["detail"]["message"] == "Invalid OTP"
    assert json_data["detail"]["error"] == "Invalid OTP, does not match or expired"


def test_b_password_reset_validate_otp_success(client, test_data, get_user_one_otp):
    """Test password reset with valid user email"""
    user_one = test_data["user_one"]
    new_password = "NewPassword123"

    headers = get_basic_auth_header(
        username=user_one["email"],
        password=new_password,
    )

    response = client.patch(
        "/user/password-reset/validate-otp",
        headers=headers,
        json={"otp": get_user_one_otp},
    )

    assert response.status_code in [200, 201, 202]
    json_data = response.json()

    assert "message" in json_data
    assert json_data["message"] == "Password changed successfully"

    assert "data" in json_data
    assert json_data["data"] is None
