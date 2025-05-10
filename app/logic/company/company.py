from fastapi import status

# utils
from app.security.jwt import JWTManager
from app.utils.app_error import AppError

# repository
from app.logic.company.repository.company import CompanyRepository

# models
from app.models.company.company import (
    CompanyCreate,
    CompanyUpdate,
    CompanyRead,
)

from app.models.user.user import UserRead


from app.models.company.response_messages import CompanyResponseMessages


class CompanyService:

    @staticmethod
    def create_company(payload: CompanyCreate, created_by: UserRead) -> CompanyRead:
        """
        Create a new company and store its address in primary_meta_data.
        Also sets up default roles (Administrator, Viewer).
        """
        # TODO: Add logic to create default roles
        # Link the company to the user who created it
        company_repository = CompanyRepository()
        company = company_repository.create_company(payload, created_by)
        if not company:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.COMPANY_CREATION_FAILED.value,
            )
        return company
