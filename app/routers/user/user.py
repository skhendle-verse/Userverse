import traceback
from fastapi import APIRouter, Depends, status
from app.configs import configs
from app.database import CustomSession
from app.database.company import Company
from app.models.company.company import CompanyRegistrationModel
from app.security.api_security import get_current_user
from app.security.company_security import authenticate_company
from app.models.company_security import CompanySecurityModel
from app.exceptions import AppError
from app.security.permissions_check import company_validation
from app.services.accounting.register_accounts import RegisterAccountService
from app.utils.enums import Errors, UserPermissions

router = APIRouter()
tag = "Company"


@router.post("/company", tags=[tag])
def create_company_api(
    company_reg_model: CompanyRegistrationModel,
    company: CompanySecurityModel = Depends(authenticate_company),
    user: dict = Depends(get_current_user),
):
    try:
        company_data = company_validation(
            data=user["companies"],
            company_id=company.id,
            permissions=[
                UserPermissions.SUPER_ADMIN.value,
                UserPermissions.ADMIN.value,
            ],
        )

        with CustomSession(configs).session_object() as db:
            new_company = Company.create(
                db,
                id=company.id,
                name=company_reg_model.name,
                tax_id=company_reg_model.tax_number,
                secondary_meta={
                    "financial_reporting_date": company_reg_model.financial_reporting_date,
                    "registration_number": company_reg_model.registration_number,
                    "industry": company_reg_model.industry,
                    "db_name": company.db_name,
                },
            )
            print(f"\n  company_data:{company_data} \n")
            accounts = RegisterAccountService(
                configs=configs,
                company_data=company_data,
            )
            accounts.get_entity()
        return new_company
    except Exception as e:
        traceback.print_exc()
        raise AppError(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=Errors.INVALID_REQUEST_MESSAGE.name,
            error=str(e),
        )


# @router.get("/company", tags=[tag])
# def get_company_api(
#     company: CompanySecurityModel = Depends(authenticate_company),
#     user: dict = Depends(get_current_user),
# ):
#     try:
#         pass
#     except Exception as e:
#         raise AppError(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             message=invalid_request_message,
#             error=str(e),
#         )


# @router.patch("/company", tags=[tag])
# def update_company_api(
#     company: CompanySecurityModel = Depends(authenticate_company),
#     user: dict = Depends(get_current_user),
# ):
#     try:
#         pass
#     except Exception as e:
#         raise AppError(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             message=invalid_request_message,
#             error=str(e),
#         )


# @router.delete("/company", tags=[tag])
# def delete_company_api(
#     company: CompanySecurityModel = Depends(authenticate_company),
#     user: dict = Depends(get_current_user),
# ):
#     try:
#         pass
#     except Exception as e:
#         raise AppError(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             message=invalid_request_message,
#             error=str(e),
#         )
