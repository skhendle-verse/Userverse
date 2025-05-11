from fastapi import status

# utils
from app.security.jwt import JWTManager
from app.utils.app_error import AppError

# repository
from app.logic.company.repository.company import CompanyRepository

# database
from app.database import DatabaseSessionManager
from app.database.association_user_company import AssociationUserCompany


# models
from app.models.company.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyRead,
)
from app.models.company.roles import CompanyDefaultRoles


from app.models.user.user import UserRead


from app.models.company.response_messages import CompanyResponseMessages


class CompanyService:

    @staticmethod
    def create_company(payload: CompanyCreate, created_by: UserRead) -> CompanyRead:
        """
        Create a new company and store its address in primary_meta_data.
        Also sets up default roles (Administrator, Viewer).
        """
        company_repository = CompanyRepository()
        company = company_repository.create_company(payload, created_by)
        if not company:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.COMPANY_CREATION_FAILED.value,
            )
        return company

    @staticmethod
    def get_company(
        user: UserRead, company_id: str = None, email: str = None
    ) -> CompanyRead:
        """
        Get a company by its ID.
        """
        if not company_id and not email:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.COMPANY_ID_OR_EMAIL_REQUIRED.value,
            )
        company_repository = CompanyRepository()
        company = None
        if company_id:
            company = company_repository.get_company_by_id(company_id)

        if email:
            company = company_repository.get_company_by_email(email)

        linked_company = CompanyService.check_if_user_is_in_company(
            user_id=user.id,
            company_id=company.id,
        )

        if not linked_company:
            raise AppError(
                status_code=status.HTTP_403_FORBIDDEN,
                message=CompanyResponseMessages.UNAUTHORIZED_COMPANY_ACCESS.value,
            )

        return company

    @staticmethod
    def update_company(
        payload: CompanyUpdate, company_id: str, user: UserRead
    ) -> CompanyRead:
        """
        Update a company by its ID.
        """
        linked_company = CompanyService.check_if_user_is_in_company(
            user_id=user.id,
            company_id=company_id,
            role=CompanyDefaultRoles.ADMINISTRATOR.name_value,
        )
        if not linked_company:
            raise AppError(
                status_code=status.HTTP_403_FORBIDDEN,
                message=CompanyResponseMessages.UNAUTHORIZED_COMPANY_ACCESS.value,
            )
        company_repository = CompanyRepository()
        company = company_repository.update_company(payload, company_id, user)
        if not company:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.COMPANY_UPDATE_FAILED.value,
            )
        return company

    @staticmethod
    def check_if_user_is_in_company(
        user_id: str, company_id: str, role: str = None
    ) -> bool:
        """
        Check if the user is linked to the company.
        If a role is provided, check if the user has that role.
        """
        with DatabaseSessionManager().session_object() as session:
            # Check if the user is linked to the company
            linked_company = AssociationUserCompany.is_user_linked_to_company(
                session=session,
                user_id=int(user_id),
                company_id=int(company_id),
                role_name=role,
            )

            return linked_company
