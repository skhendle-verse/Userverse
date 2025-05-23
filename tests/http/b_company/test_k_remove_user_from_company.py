import pytest
from tests.http.conftest import client, login_token, login_token_user_two
from app.models.company.response_messages import CompanyResponseMessages, CompanyUserResponseMessages


@pytest.mark.parametrize(
    "login_token_key, company_id, user_id, expected_status, expected_message",
    [
        # ✅ Admin removes a user from company 1
        (
            "login_token_user_two",
            1,
            3,  # user.three@email.com
            200,
            CompanyUserResponseMessages.REMOVE_USER_SUCCESS.value,
        ),
        # ❌ Non-admin tries to remove a user from company 1
        (
            "login_token_user_two",
            1,
            3,
            403,
            CompanyResponseMessages.UNAUTHORIZED_COMPANY_ACCESS.value,
        ),
        # ❌ Admin tries to remove the last admin
        (
            "login_token",
            1,
            1,  # Assume user.one@email.com is the last admin
            400,
            CompanyUserResponseMessages.LAST_ADMIN_REMOVE_FORBIDDEN.value,
        ),
    ],
)
def test_remove_user_from_company(
    client,
    login_token,
    login_token_user_two,
    login_token_key,
    company_id,
    user_id,
    expected_status,
    expected_message,
):
    """
    Test /company/{company_id}/user/{user_id} for removing users with various scenarios:
    - valid user removal
    - unauthorized user attempt
    - last admin removal forbidden
    """
    token_map = {
        "login_token": login_token,
        "login_token_user_two": login_token_user_two,
    }

    headers = {
        "Authorization": f"Bearer {token_map[login_token_key]}",
        "accept": "application/json",
    }

    response = client.delete(
        f"/company/{company_id}/user/{user_id}", headers=headers
    )
    assert response.status_code == expected_status
    json_data = response.json()
    assert expected_message in json_data["message"] or expected_message in str(json_data)
    if expected_status == 201:
        assert "data" in json_data
        assert isinstance(json_data["data"], (list, dict))