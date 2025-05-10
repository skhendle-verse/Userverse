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

    def create_company(self, payload: CompanyCreate, created_by: UserRead) -> CompanyRead:
        with self.db_manager.session_object() as session:
            try:
                # 1. Create company
                company = Company.create(session, **payload.model_dump(exclude={"address"}))

                if not company:
                    raise AppError(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        message=CompanyResponseMessages.COMPANY_CREATION_FAILED.value,
                    )

                # 2. Add address to primary_meta_data
                if payload.address:
                    Company.update_json_field(
                        session,
                        record_id=company["id"],
                        column_name="primary_meta_data",
                        key="address",
                        value=payload.address.model_dump()
                    )

                # 3. Create default roles (Administrator, Viewer)
                for role in CompanyDefaultRoles:
                    Role.create(
                        session,
                        company_id=company["id"],
                        name=role.name_value,
                        description=role.description,
                    )

                # 4. Associate creator as Administrator
                AssociationUserCompany.create(
                    session,
                    user_id=created_by.id,
                    company_id=company["id"],
                    role_name=CompanyDefaultRoles.ADMINISTRATOR.name_value,
                )

                registered_company = Company.get_by_id(session, company["id"])
                if 'primary_meta_data' in registered_company:
                    primary_meta_data = registered_company.get(
                        'primary_meta_data'
                    )
                    if 'address' in primary_meta_data:
                        address = primary_meta_data.get('address')
                        registered_company['address'] = address


                return CompanyRead(**registered_company)

            except Exception as e:
                session.rollback()
                raise AppError.internal(str(e))
