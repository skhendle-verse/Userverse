from fastapi import status

# utils
from app.utils.app_error import AppError

# database
from app.database import DatabaseSessionManager
from app.database.company import Company
from app.database.user import User
from app.database.role import Role
from app.database.association_user_company import AssociationUserCompany

# models
from app.models.company.company import CompanyRead, CompanyCreate, CompanyUpdate
from app.models.user.user import UserRead
from app.models.company.roles import CompanyDefaultRoles

from app.models.company.response_messages import CompanyResponseMessages


class CompanyRepository:
    def __init__(self):
        self.db_manager = DatabaseSessionManager()

    def create_company(
        self, payload: CompanyCreate, created_by: UserRead
    ) -> CompanyRead:
        with self.db_manager.session_object() as session:
            try:
                # 1. Create company
                company = self._create_company_record(session, payload)

                # 2. Add address to primary_meta_data
                if payload.address:
                    self._add_company_address(session, company["id"], payload.address)

                # 3. Create default roles
                self._create_default_roles(session, company["id"])

                # 4. Associate creator as Administrator
                self._associate_creator(session, created_by.id, company["id"])

                # 5. Get the registered company with complete data
                registered_company = self._get_registered_company(session, company["id"])

                return CompanyRead(**registered_company)

            except Exception as e:
                session.rollback()
                raise e

    def get_company_by_id(self, company_id: str) -> CompanyRead:
        """
        Retrieve a company by its ID.

        Args:
            company_id: The unique identifier of the company

        Returns:
            CompanyRead: The company data

        Raises:
            AppError: If company not found
        """
        with self.db_manager.session_object() as session:
            company = self._get_registered_company(session, company_id)

            if not company:
                raise AppError(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message=CompanyResponseMessages.COMPANY_NOT_FOUND.value,
                )

            return CompanyRead(**company)

    def get_company_by_email(self, email: str) -> CompanyRead:
        """
        Retrieve a company by its email address.

        Args:
            email: The email address of the company

        Returns:
            CompanyRead: The company data

        Raises:
            AppError: If company not found
        """
        with self.db_manager.session_object() as session:
            company = Company.get_company_by_email(session, email)

            if not company:
                raise AppError(
                    status_code=status.HTTP_404_NOT_FOUND,
                    message=CompanyResponseMessages.COMPANY_NOT_FOUND.value,
                )

            # Reuse the method to get complete company data
            return CompanyRead(**self._get_registered_company(session, company["id"]))

    
    def _create_company_record(self, session, payload: CompanyCreate) -> dict:
        """Create the company record in the database"""
        company = Company.create(
            session, **payload.model_dump(exclude={"address"})
        )

        if not company:
            raise AppError(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=CompanyResponseMessages.COMPANY_CREATION_FAILED.value,
            )

        return company

    def _add_company_address(self, session, company_id: str, address) -> None:
        """Add address to the company's primary_meta_data"""
        Company.update_json_field(
            session,
            record_id=company_id,
            column_name="primary_meta_data",
            key="address",
            value=address.model_dump(),
        )

    def _create_default_roles(self, session, company_id: str) -> None:
        """Create default roles for the company"""
        for role in CompanyDefaultRoles:
            Role.create(
                session,
                company_id=company_id,
                name=role.name_value,
                description=role.description,
            )

    def _associate_creator(self, session, user_id: str, company_id: str) -> None:
        """Associate the creator as Administrator of the company"""
        AssociationUserCompany.create(
            session,
            user_id=user_id,
            company_id=company_id,
            role_name=CompanyDefaultRoles.ADMINISTRATOR.name_value,
        )

    def _get_registered_company(self, session, company_id: str) -> dict:
        """Get the registered company with complete data"""
        registered_company = Company.get_by_id(session, company_id)

        if "primary_meta_data" in registered_company:
            primary_meta_data = registered_company.get("primary_meta_data")
            if "address" in primary_meta_data:
                address = primary_meta_data.get("address")
                registered_company["address"] = address

        return registered_company