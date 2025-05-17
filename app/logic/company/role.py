from fastapi import status

# utils
from app.utils.app_error import AppError

# repository
from app.logic.company.repository.role import RoleRepository


# models
from app.models.company.company import CompanyRead
from app.models.company.roles import CompanyDefaultRoles
from app.models.company.roles import (
    RoleCreate,
    RoleRead,
    RoleUpdate,
    CompanyDefaultRoles,
)
from app.models.user.user import UserRead
from app.models.company.response_messages import CompanyResponseMessages


class RoleService:

    @staticmethod
    def update_role_description(company_id: int, name: str, description: str) -> RoleRead:
        """
        Update the description of a role for a company.
        """
        role_repository = RoleRepository(company_id=company_id)
        role = role_repository.update_role_description(name=name, description=description)
        if not role:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.ROLE_UPDATE_FAILED.value,
            )
        return role

    @staticmethod
    def create_role(
        payload: RoleCreate, created_by: UserRead, company_id: int
    ) -> RoleRead:
        """
        Create a new company role and store its creator in primary_meta_data.
        """
        role_repository = RoleRepository(company_id=company_id)
        role = role_repository.create_role(payload, created_by)
        if not role:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.ROLE_CREATION_FAILED.value,
            )
        return role
