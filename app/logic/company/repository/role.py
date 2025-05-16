from app.models.company.address import CompanyAddress
from fastapi import status

# utils
from app.utils.app_error import AppError

# database
from app.database import DatabaseSessionManager
from app.database.company import Company
from app.database.role import Role
from app.database.association_user_company import AssociationUserCompany

# models
from app.models.company.roles import (
    RoleCreate,
    RoleRead,
    RoleUpdate,
    CompanyDefaultRoles,
)
from app.models.user.user import UserRead
from app.models.company.roles import CompanyDefaultRoles

from app.models.company.response_messages import CompanyResponseMessages


class RoleRepository:
    def __init__(self, company_id: int):
        self.company_id = company_id
        self.db_manager = DatabaseSessionManager()

    def create_role(
        self,
        payload: RoleCreate,
        created_by: UserRead,
    ) -> RoleRead:
        """
        Create a new role for a company.

        Args:
            payload: The role data to be created
            created_by: The user who is creating the role
            company_id: The ID of the company

        Returns:
            RoleRead: The created role data

        Raises:
            AppError: If role creation fails
        """
        with self.db_manager.session_object() as session:
            # 1. Create the role
            role = self._create_role_record(session, payload, created_by)

            # 2. Get the registered role with complete data
            registered_role = self._get_registered_role(session, role["name"])

            return RoleRead(**registered_role)

    def _create_role_record(
        self, session, payload: RoleCreate, created_by: UserRead
    ) -> dict:
        """
        Create a new role record in the database.

        Args:
            session: The database session
            payload: The role data to be created
            created_by: The user who is creating the role
            company_id: The ID of the company

        Returns:
            dict: The created role data
        """
        try:
            new_role = Role(
                name=payload.name,
                description=payload.description,
                company_id=self.company_id,
            )
            session.add(new_role)
            session.commit()
            new_role.update_json_field(
                session=session,
                company_id=new_role.company_id,
                name=new_role.name,
                column_name="primary_meta_data",
                key="created_by",
                value=created_by.model_dump(),
            )
            session.refresh(new_role)
            return new_role.to_dict(new_role)
        except Exception as e:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.ROLE_CREATION_FAILED.value,
                error=str(e),
            ) from e

    def _get_registered_role(self, session, role_name: str) -> dict:
        """
        Get the registered role with complete data.

        Args:
            session: The database session
            role_id: The ID of the role

        Returns:
            dict: The registered role data
        """
        try:

            role = session.query(Role).filter(Role.name == role_name).first()
            if not role:
                raise AppError(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message=CompanyResponseMessages.ROLE_NOT_FOUND.value,
                )
            return role.to_dict(role)
        except Exception as e:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=str(e),
            ) from e
