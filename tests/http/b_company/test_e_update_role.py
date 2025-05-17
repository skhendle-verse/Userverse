import pytest
from app.models.company.response_messages import CompanyResponseMessages
from tests.http.conftest import client, test_company_data, login_token


def test_update_role_description_success(client, login_token, test_company_data):
    """
    Test updating a role's description successfully.
    """
    headers = {"Authorization": f"Bearer {login_token}"}
    # Assume company 1 and role 'Admin' exist
    payload = {"description": "Updated admin description"}
    response = client.patch("/1/role/Admin", json=payload, headers=headers)
    assert response.status_code == 200
    json_data = response.json()
    assert "message" in json_data
    assert json_data["message"] == CompanyResponseMessages.ROLE_UPDATED.value
    assert "data" in json_data
    assert json_data["data"]["description"] == payload["description"]


def test_update_role_description_forbidden(
    client, login_token_user_two, test_company_data
):
    """
    Test updating a role's description fails if not admin.
    """
    headers = {"Authorization": f"Bearer {login_token_user_two}"}
    payload = {"description": "Should not update"}
    response = client.patch("/1/role/Admin", json=payload, headers=headers)
    assert response.status_code in [400, 403]
    json_data = response.json()
    assert "detail" in json_data
    assert (
        json_data["detail"]["message"]
        == CompanyResponseMessages.ROLE_CREATION_FORBIDDEN.value
    )


def test_update_role_description_not_found(client, login_token, test_company_data):
    """
    Test updating a non-existent role returns not found.
    """
    headers = {"Authorization": f"Bearer {login_token}"}
    payload = {"description": "Does not exist"}
    response = client.patch("/1/role/NonExistentRole", json=payload, headers=headers)
    assert response.status_code in [400, 404]
    json_data = response.json()
    assert "detail" in json_data
    # Could be ROLE_UPDATE_FAILED or ROLE_NOT_FOUND depending on error handling
